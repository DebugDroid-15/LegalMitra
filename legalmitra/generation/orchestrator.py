"""
LegalMitra Generation Orchestrator
Resumable, fault-tolerant generation engine with checkpointing, retry, and rate limiting.
"""

import asyncio
import json
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
import random

from legalmitra.core.enums import SourceType
from legalmitra.core.errors import LLMProviderError
from legalmitra.core.logging import get_logger
from legalmitra.ingestion.registry import SourceRegistryManager
from legalmitra.llm.interface import BaseLLMProvider, LLMMessage
from legalmitra.llm.mock_provider import MockLLMProvider
from legalmitra.llm.nemotron import NemotronLLMProvider
from legalmitra.generation.schemas import (
    GenerationConfig,
    GenerationResult,
    GenerationSummary,
    GenerationTask,
    GenerationStatus,
    TaskType,
    GeneratedDocument,
    get_output_filename,
    task_type_to_schema,
)
from legalmitra.generation.prompts import get_prompt, build_user_prompt
from legalmitra.generation.validator import GenerationValidator, extract_json_from_response
from legalmitra.dataset.jsonl_exporter import JSONLExporter

logger = get_logger("generation_orchestrator")


class RateLimiter:
    """Token bucket rate limiter for API requests."""
    
    def __init__(self, requests_per_minute: int, tokens_per_minute: int, is_dry_run: bool = False):
        self.requests_per_minute = requests_per_minute
        self.tokens_per_minute = tokens_per_minute
        self.is_dry_run = is_dry_run
        self.request_times: List[float] = []
        self.token_usage: List[Tuple[float, int]] = []  # (timestamp, tokens)
        self._lock = asyncio.Lock()
    
    async def acquire(self, estimated_tokens: int = 1000) -> None:
        """Wait until rate limit allows the request."""
        if self.is_dry_run:
            return

        while True:
            sleep_time = 0.0
            async with self._lock:
                now = time.time()
                minute_ago = now - 60.0
                
                # Clean old entries
                self.request_times = [t for t in self.request_times if t > minute_ago]
                self.token_usage = [(t, tok) for t, tok in self.token_usage if t > minute_ago]
                
                # Check request limit
                if len(self.request_times) >= self.requests_per_minute:
                    sleep_time = max(sleep_time, 60.0 - (now - self.request_times[0]) + 0.1)
                
                # Check token limit
                current_tokens = sum(tok for _, tok in self.token_usage)
                if current_tokens + estimated_tokens > self.tokens_per_minute and self.token_usage:
                    sleep_time = max(sleep_time, 60.0 - (now - self.token_usage[0][0]) + 0.1)
                
                if sleep_time <= 0:
                    self.request_times.append(now)
                    return
            
            # Sleep OUTSIDE the lock so other tasks are not deadlocked
            if sleep_time > 0:
                logger.debug(f"Rate limit: sleeping {sleep_time:.2f}s outside lock")
                await asyncio.sleep(min(sleep_time, 2.0))
    
    def record_usage(self, prompt_tokens: int, completion_tokens: int) -> None:
        """Record actual token usage after request."""
        if self.is_dry_run:
            return
        now = time.time()
        self.token_usage.append((now, prompt_tokens + completion_tokens))


class GenerationOrchestrator:
    """
    Main orchestrator for source-grounded dataset generation.
    
    Features:
    - Resumable processing with checkpointing
    - Exponential backoff retry
    - Rate limiting
    - Cost/token budget enforcement
    - Structured logging and reporting
    """
    
    def __init__(
        self,
        config: GenerationConfig,
        registry_manager: SourceRegistryManager,
        llm_provider: Optional[BaseLLMProvider] = None,
    ):
        self.config = config
        self.registry = registry_manager
        self.llm_provider = llm_provider or self._create_provider()
        self.validator = GenerationValidator(registry_manager)
        self.rate_limiter = RateLimiter(
            config.requests_per_minute,
            config.tokens_per_minute,
            is_dry_run=config.dry_run,
        )
        
        # State
        self.summary = GenerationSummary(
            run_id=str(uuid.uuid4())[:8],
            started_at=datetime.utcnow(),
        )
        self.checkpoint_dir = Path(config.checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir = Path(config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Token/cost tracking
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_cost = 0.0
        
        # Load checkpoint if exists
        self._load_checkpoint()
    
    def _create_provider(self) -> BaseLLMProvider:
        """Create LLM provider from config or environment."""
        if self.config.dry_run:
            logger.info("Dry-run mode enabled: using MockLLMProvider")
            return MockLLMProvider()
        
        # Live inference via Nemotron / NVIDIA NIM provider
        provider = NemotronLLMProvider(
            api_key=None,  # Will read from NEMOTRON_API_KEY
            base_url=None,  # Will read from NEMOTRON_BASE_URL
            model_name=self.config.model_name or None,  # Will read from NEMOTRON_MODEL_NAME
        )
        
        if provider.is_available():
            logger.info(f"Using live provider: {provider.model_name} at {provider.base_url}")
            return provider
        
        raise LLMProviderError(
            "Live inference requested but NVIDIA API credentials or base URL are not configured. "
            "Please ensure NEMOTRON_API_KEY is set in your .env or environment. "
            "Mock provider will not be substituted silently in live mode."
        )
    
    def _load_checkpoint(self) -> None:
        """Load generation state from checkpoint file."""
        checkpoint_file = self.checkpoint_dir / f"checkpoint_{self.summary.run_id}.json"
        if checkpoint_file.exists():
            try:
                with open(checkpoint_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.summary = GenerationSummary(**data.get("summary", {}))
                logger.info(f"Loaded checkpoint: {self.summary.tasks_completed}/{self.summary.total_tasks} tasks")
            except Exception as e:
                logger.warning(f"Failed to load checkpoint: {e}")
    
    def _save_checkpoint(self) -> None:
        """Save generation state to checkpoint file."""
        checkpoint_file = self.checkpoint_dir / f"checkpoint_{self.summary.run_id}.json"
        try:
            data = {
                "summary": self.summary.model_dump(),
                "timestamp": datetime.utcnow().isoformat(),
            }
            with open(checkpoint_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save checkpoint: {e}")
    
    def discover_sources(
        self,
        source_type: Optional[SourceType] = None,
        processing_status: Optional[str] = None,
    ) -> List[str]:
        """Discover source IDs eligible for generation."""
        records = self.registry.filter(
            source_type=source_type,
            processing_status=processing_status,
        )
        
        # Only use normalized documents
        eligible = [r.document_id for r in records if r.processing_status.value == "normalized"]
        
        if self.config.pilot_mode:
            eligible = eligible[:self.config.pilot_max_sources]
        
        logger.info(f"Discovered {len(eligible)} eligible sources for generation")
        return eligible
    
    def load_source_text(self, source_id: str) -> Optional[str]:
        """Load normalized source text for grounding validation."""
        norm_file = Path("data/02_normalized") / f"{source_id}.json"
        if norm_file.exists():
            try:
                with open(norm_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # Extract full text from normalized document
                if "sections" in data:
                    # Statute
                    texts = []
                    for sec in data["sections"]:
                        texts.append(sec.get("full_verbatim_text", ""))
                    return "\n\n".join(texts)
                elif "paragraphs" in data:
                    # Judgment
                    texts = [p.get("verbatim_text", "") for p in data["paragraphs"]]
                    return "\n\n".join(texts)
            except Exception as e:
                logger.error(f"Failed to load source text for {source_id}: {e}")
        return None
    
    def load_source_record(self, source_id: str) -> Optional[Any]:
        """Load source registry record."""
        return self.registry.get(source_id)
    
    def create_tasks(self, source_ids: List[str]) -> List[GenerationTask]:
        """Create generation tasks for all sources and task types."""
        tasks = []
        for source_id in source_ids:
            for task_type in self.config.task_types:
                # Skip multilingual unless enabled
                if task_type == TaskType.MULTILINGUAL and not self.config.generate_multilingual:
                    continue
                
                # Skip judgment analysis for non-judgments
                if task_type == TaskType.JUDGMENT_ANALYSIS:
                    rec = self.registry.get(source_id)
                    if rec and rec.source_type != SourceType.JUDGMENT:
                        continue
                
                # Skip drafting for judgments (primarily statutory)
                if task_type == TaskType.DRAFTING:
                    rec = self.registry.get(source_id)
                    if rec and rec.source_type == SourceType.JUDGMENT:
                        continue
                
                task_id = f"GEN-{source_id}-{task_type.value}-{uuid.uuid4().hex[:8]}"
                task = GenerationTask(
                    task_id=task_id,
                    source_id=source_id,
                    task_type=task_type,
                    max_attempts=self.config.max_retries + 1,
                )
                tasks.append(task)
        
        self.summary.total_sources = len(source_ids)
        self.summary.total_tasks = len(tasks)
        self._save_checkpoint()
        return tasks
    
    async def execute_task(self, task: GenerationTask, source_text: str) -> GenerationResult:
        """Execute a single generation task with retry logic."""
        start_time = time.time()
        task.status = GenerationStatus.IN_PROGRESS
        task.updated_at = datetime.utcnow()
        
        source_record = self.load_source_record(task.source_id)
        if not source_record:
            return GenerationResult(
                task_id=task.task_id,
                source_id=task.source_id,
                task_type=task.task_type,
                success=False,
                error="Source record not found",
                duration_seconds=time.time() - start_time,
            )
        
        system_prompt = get_prompt(task.task_type)
        max_examples = self.config.max_examples_per_source_per_task
        
        for attempt in range(task.max_attempts):
            task.attempts = attempt + 1
            task.status = GenerationStatus.RETRYING if attempt > 0 else GenerationStatus.IN_PROGRESS
            
            try:
                # Build user prompt with focused excerpt to avoid context overflow
                prompt_source_text = source_text[:4000] if len(source_text) > 4000 else source_text
                num_to_request = min(max_examples - task.generated_count, 2 if self.config.pilot_mode else max_examples)
                user_prompt = build_user_prompt(
                    task.task_type,
                    prompt_source_text,
                    task.source_id,
                    existing_examples=task.generated_count,
                    max_examples=num_to_request,
                )
                
                messages = [
                    LLMMessage(role="system", content=system_prompt),
                    LLMMessage(role="user", content=user_prompt),
                ]
                
                # Set source context for mock provider
                if isinstance(self.llm_provider, MockLLMProvider):
                    self.llm_provider.set_source_context(task.source_id, source_text)
                
                # Rate limit
                await self.rate_limiter.acquire(self.config.max_tokens_per_request)
                
                # Generate
                response = self.llm_provider.generate(
                    messages,
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens_per_request,
                )
                
                # Record token usage
                usage = response.usage or {}
                prompt_tokens = usage.get("prompt_tokens", 0)
                completion_tokens = usage.get("completion_tokens", 0)
                total_tokens = usage.get("total_tokens", prompt_tokens + completion_tokens)
                
                task.prompt_tokens += prompt_tokens
                task.completion_tokens += completion_tokens
                task.total_tokens += total_tokens
                
                self.total_prompt_tokens += prompt_tokens
                self.total_completion_tokens += completion_tokens
                
                self.rate_limiter.record_usage(prompt_tokens, completion_tokens)
                
                # Check token budget
                if self.total_prompt_tokens + self.total_completion_tokens > self.config.max_total_tokens:
                    logger.warning(f"Token budget exceeded: {self.total_prompt_tokens + self.total_completion_tokens}")
                    return GenerationResult(
                        task_id=task.task_id,
                        source_id=task.source_id,
                        task_type=task.task_type,
                        success=False,
                        error="Token budget exceeded",
                        duration_seconds=time.time() - start_time,
                        tokens_used={"prompt": task.prompt_tokens, "completion": task.completion_tokens},
                    )
                
                # Parse and validate output
                json_text = extract_json_from_response(response.content)
                source_texts = {task.source_id: source_text}
                source_records = {task.source_id: source_record}
                
                documents, errors = self.validator.validate_generation_output(
                    json_text,
                    task.task_type,
                    source_texts,
                    source_records,
                )
                
                if errors and self.config.reject_ungrounded:
                    # Retry on grounding errors
                    task.last_error = "; ".join(errors[:3])
                    logger.warning(f"Task {task.task_id} attempt {attempt+1} failed grounding: {errors[:2]}")
                    if attempt < task.max_attempts - 1:
                        await self._backoff(attempt)
                        continue
                
                # Success
                task.generated_count += len(documents)
                task.status = GenerationStatus.COMPLETED
                task.completed_at = datetime.utcnow()
                
                return GenerationResult(
                    task_id=task.task_id,
                    source_id=task.source_id,
                    task_type=task.task_type,
                    success=True,
                    examples_generated=[d.model_dump() for d in documents],
                    examples_validated=len(documents),
                    examples_rejected=0,
                    validation_errors=errors,
                    tokens_used={"prompt": prompt_tokens, "completion": completion_tokens, "total": total_tokens},
                    duration_seconds=time.time() - start_time,
                    model_name=response.model_name,
                )
                
            except LLMProviderError as e:
                task.last_error = str(e)
                logger.warning(f"Task {task.task_id} attempt {attempt+1} failed: {e}")
                if attempt < task.max_attempts - 1:
                    await self._backoff(attempt)
                    continue
                return GenerationResult(
                    task_id=task.task_id,
                    source_id=task.source_id,
                    task_type=task.task_type,
                    success=False,
                    error=str(e),
                    duration_seconds=time.time() - start_time,
                )
            
            except Exception as e:
                task.last_error = str(e)
                logger.error(f"Task {task.task_id} unexpected error: {e}")
                if attempt < task.max_attempts - 1:
                    await self._backoff(attempt)
                    continue
                return GenerationResult(
                    task_id=task.task_id,
                    source_id=task.source_id,
                    task_type=task.task_type,
                    success=False,
                    error=f"Unexpected: {e}",
                    duration_seconds=time.time() - start_time,
                )
        
        task.status = GenerationStatus.FAILED
        return GenerationResult(
            task_id=task.task_id,
            source_id=task.source_id,
            task_type=task.task_type,
            success=False,
            error=task.last_error or "Max retries exceeded",
            duration_seconds=time.time() - start_time,
        )
    
    async def _backoff(self, attempt: int) -> None:
        """Exponential backoff with jitter."""
        delay = min(
            self.config.base_retry_delay_seconds * (self.config.retry_exponential_base ** attempt),
            self.config.max_retry_delay_seconds,
        )
        jitter = random.uniform(0, delay * 0.1)
        await asyncio.sleep(delay + jitter)
    
    async def run_generation(
        self,
        source_ids: Optional[List[str]] = None,
        source_type: Optional[SourceType] = None,
    ) -> GenerationSummary:
        """Run the complete generation pipeline."""
        logger.info(f"Starting generation run: {self.summary.run_id}")
        
        # Discover sources
        if source_ids is None:
            source_ids = self.discover_sources(source_type=source_type, processing_status="normalized")
        
        if not source_ids:
            logger.warning("No eligible sources found for generation")
            self.summary.completed_at = datetime.utcnow()
            return self.summary
        
        # Create tasks
        tasks = self.create_tasks(source_ids)
        
        # Process tasks with concurrency control
        semaphore = asyncio.Semaphore(self.config.max_concurrent_requests)
        
        async def process_task(task: GenerationTask) -> GenerationResult:
            async with semaphore:
                source_text = self.load_source_text(task.source_id)
                if not source_text:
                    logger.warning(f"No source text for {task.source_id}, skipping")
                    return GenerationResult(
                        task_id=task.task_id,
                        source_id=task.source_id,
                        task_type=task.task_type,
                        success=False,
                        error="No source text available",
                    )
                return await self.execute_task(task, source_text)
        
        # Execute all tasks
        results = await asyncio.gather(
            *[process_task(task) for task in tasks],
            return_exceptions=True,
        )
        
        # Process results
        for i, result in enumerate(results):
            task = tasks[i]
            if isinstance(result, Exception):
                logger.error(f"Task {task.task_id} raised exception: {result}")
                self.summary.tasks_failed += 1
                self.summary.errors.append(f"{task.task_id}: {result}")
            elif isinstance(result, GenerationResult):
                if result.success:
                    self.summary.tasks_completed += 1
                    self.summary.total_examples_generated += len(result.examples_generated)
                    self.summary.total_examples_validated += result.examples_validated
                    self.summary.total_examples_rejected += result.examples_rejected
                    self.total_cost += result.cost_estimate_usd or 0.0
                    
                    # Export generated examples
                    if result.examples_generated and not self.config.dry_run:
                        self._export_examples(result)
                else:
                    self.summary.tasks_failed += 1
                    self.summary.errors.append(f"{task.task_id}: {result.error}")
                
                # Update breakdowns
                tt = result.task_type.value
                if tt not in self.summary.task_type_breakdown:
                    self.summary.task_type_breakdown[tt] = {"completed": 0, "failed": 0, "examples": 0}
                if result.success:
                    self.summary.task_type_breakdown[tt]["completed"] += 1
                    self.summary.task_type_breakdown[tt]["examples"] += len(result.examples_generated)
                else:
                    self.summary.task_type_breakdown[tt]["failed"] += 1
                
                src = result.source_id
                if src not in self.summary.source_breakdown:
                    self.summary.source_breakdown[src] = {"completed": 0, "failed": 0, "examples": 0}
                if result.success:
                    self.summary.source_breakdown[src]["completed"] += 1
                    self.summary.source_breakdown[src]["examples"] += len(result.examples_generated)
                else:
                    self.summary.source_breakdown[src]["failed"] += 1
            
            # Checkpoint periodically
            if (self.summary.tasks_completed + self.summary.tasks_failed) % self.config.checkpoint_interval == 0:
                self._save_checkpoint()
        
        # Finalize
        self.summary.completed_at = datetime.utcnow()
        self.summary.total_duration_seconds = (self.summary.completed_at - self.summary.started_at).total_seconds()
        self.summary.total_tokens = self.total_prompt_tokens + self.total_completion_tokens
        self.summary.total_prompt_tokens = self.total_prompt_tokens
        self.summary.total_completion_tokens = self.total_completion_tokens
        self.summary.total_cost_estimate_usd = self.total_cost
        
        self._save_checkpoint()
        logger.info(f"Generation run complete: {self.summary.tasks_completed}/{self.summary.total_tasks} tasks")
        
        return self.summary
    
    def _export_examples(self, result: GenerationResult) -> None:
        """Export generated examples to JSONL files."""
        if not result.examples_generated:
            return
        
        output_file = self.output_dir / get_output_filename(result.task_type)
        
        # Convert to schema instances for export
        target_schema = task_type_to_schema(result.task_type)
        documents = [target_schema(**ex) for ex in result.examples_generated]
        
        JSONLExporter.export(documents, output_file, append=True)
        logger.info(f"Exported {len(documents)} examples to {output_file}")
    
    def run_sync(
        self,
        source_ids: Optional[List[str]] = None,
        source_type: Optional[SourceType] = None,
    ) -> GenerationSummary:
        """Synchronous wrapper for generation run."""
        return asyncio.run(self.run_generation(source_ids, source_type))


def run_generation_pipeline(
    config: Optional[GenerationConfig] = None,
    registry_file: str = "registry/source_registry.jsonl",
    source_ids: Optional[List[str]] = None,
    source_type: Optional[SourceType] = None,
    dry_run: bool = False,
    pilot_mode: bool = False,
) -> GenerationSummary:
    """
    High-level function to run generation pipeline.
    
    Args:
        config: GenerationConfig (will create default if None)
        registry_file: Path to source registry
        source_ids: Specific source IDs to process (overrides discovery)
        source_type: Filter sources by type
        dry_run: Use mock provider, no actual API calls
        pilot_mode: Limit to pilot_max_sources and pilot_max_examples
    
    Returns:
        GenerationSummary with results
    """
    if config is None:
        config = GenerationConfig()
    
    if dry_run:
        config.dry_run = True
    if pilot_mode:
        config.pilot_mode = True
    
    registry = SourceRegistryManager(registry_file)
    orchestrator = GenerationOrchestrator(config, registry)
    
    return orchestrator.run_sync(source_ids, source_type)