"""
LegalMitra Generation Schemas
Pydantic models for generation tasks, configuration, and results.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum

from legalmitra.core.enums import Jurisdiction, LegalReviewStatus, SourceType
from legalmitra.generation.prompts import TaskType
from legalmitra.schemas.legal_qa import EvidencePassage, LegalQADocument
from legalmitra.schemas.case_analysis import CaseAnalysisDocument
from legalmitra.schemas.procedural_guide import ProceduralGuidanceDocument
from legalmitra.schemas.drafting_example import DraftingExampleDocument
from legalmitra.schemas.evaluation import EvaluationQuestionDocument


class GenerationStatus(str, Enum):
    """Status of a generation task."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    SKIPPED = "skipped"


class GenerationTask(BaseModel):
    """A single generation task for a source document."""
    task_id: str = Field(..., description="Unique task identifier")
    source_id: str = Field(..., description="Source document ID from registry")
    task_type: TaskType = Field(..., description="Type of generation task")
    status: GenerationStatus = Field(default=GenerationStatus.PENDING)
    prompt_tokens: int = Field(default=0)
    completion_tokens: int = Field(default=0)
    total_tokens: int = Field(default=0)
    attempts: int = Field(default=0)
    max_attempts: int = Field(default=3)
    last_error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    generated_count: int = Field(default=0)
    checkpoint_data: Dict[str, Any] = Field(default_factory=dict)


class GenerationConfig(BaseModel):
    """Configuration for generation runs."""
    # Task selection
    task_types: List[TaskType] = Field(
        default_factory=lambda: [
            TaskType.STATUTORY_QA,
            TaskType.JUDGMENT_ANALYSIS,
            TaskType.CASE_REASONING,
            TaskType.PROCEDURAL_GUIDANCE,
            TaskType.DRAFTING,
            TaskType.SAFETY,
        ]
    )
    
    # Generation limits
    max_examples_per_source_per_task: int = Field(default=5, ge=1, le=20)
    max_total_examples_per_source: int = Field(default=30, ge=1, le=100)
    max_concurrent_requests: int = Field(default=3, ge=1, le=10)
    request_timeout_seconds: float = Field(default=120.0, ge=30.0)
    
    # Retry & resilience
    max_retries: int = Field(default=3, ge=0, le=10)
    base_retry_delay_seconds: float = Field(default=2.0, ge=0.5, le=60.0)
    max_retry_delay_seconds: float = Field(default=60.0, ge=5.0, le=300.0)
    retry_exponential_base: float = Field(default=2.0)
    
    # Rate limiting
    requests_per_minute: int = Field(default=20, ge=1, le=100)
    tokens_per_minute: int = Field(default=50000, ge=1000, le=200000)
    
    # Cost control
    max_total_tokens: int = Field(default=100000, ge=1000, le=1000000)
    max_cost_usd: Optional[float] = Field(default=None, ge=0.0)
    
    # Checkpointing
    checkpoint_interval: int = Field(default=5, ge=1, description="Save checkpoint every N examples")
    checkpoint_dir: str = Field(default="data/03_generated/checkpoints")
    
    # Output
    output_dir: str = Field(default="data/03_generated")
    dry_run: bool = Field(default=False)
    pilot_mode: bool = Field(default=False)
    pilot_max_sources: int = Field(default=10, ge=1, le=50)
    pilot_max_examples: int = Field(default=50, ge=1, le=200)
    
    # Validation
    validate_grounding: bool = Field(default=True)
    validate_schema: bool = Field(default=True)
    reject_ungrounded: bool = Field(default=True)
    
    # Multilingual
    generate_multilingual: bool = Field(default=False)
    target_languages: List[str] = Field(default_factory=lambda: ["en-plain", "hi", "hinglish"])
    
    # LLM parameters
    temperature: float = Field(default=0.1, ge=0.0, le=1.0)
    max_tokens_per_request: int = Field(default=4096, ge=512, le=8192)
    model_name: Optional[str] = Field(default=None)


class GenerationResult(BaseModel):
    """Result of a generation task execution."""
    task_id: str
    source_id: str
    task_type: TaskType
    success: bool
    examples_generated: List[Dict[str, Any]] = Field(default_factory=list)
    examples_validated: int = Field(default=0)
    examples_rejected: int = Field(default=0)
    validation_errors: List[str] = Field(default_factory=list)
    grounding_errors: List[str] = Field(default_factory=list)
    tokens_used: Dict[str, int] = Field(default_factory=dict)
    cost_estimate_usd: Optional[float] = None
    duration_seconds: float = Field(default=0.0)
    error: Optional[str] = None
    model_name: Optional[str] = None
    generation_timestamp: datetime = Field(default_factory=datetime.utcnow)


class GenerationSummary(BaseModel):
    """Aggregate summary of a generation run."""
    run_id: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    total_sources: int = 0
    sources_processed: int = 0
    total_tasks: int = 0
    tasks_completed: int = 0
    tasks_failed: int = 0
    total_examples_generated: int = 0
    total_examples_validated: int = 0
    total_examples_rejected: int = 0
    total_tokens: int = Field(default=0)
    total_prompt_tokens: int = Field(default=0)
    total_completion_tokens: int = Field(default=0)
    total_cost_estimate_usd: float = Field(default=0.0)
    total_duration_seconds: float = Field(default=0.0)
    errors: List[str] = Field(default_factory=list)
    task_type_breakdown: Dict[str, Dict[str, int]] = Field(default_factory=dict)
    source_breakdown: Dict[str, Dict[str, int]] = Field(default_factory=dict)


# Union type for all generated document types
GeneratedDocument = Union[
    LegalQADocument,
    CaseAnalysisDocument,
    ProceduralGuidanceDocument,
    DraftingExampleDocument,
    EvaluationQuestionDocument,
]


def task_type_to_schema(task_type: TaskType) -> type:
    """Map task type to output schema class."""
    mapping = {
        TaskType.STATUTORY_QA: LegalQADocument,
        TaskType.JUDGMENT_ANALYSIS: CaseAnalysisDocument,
        TaskType.CASE_REASONING: LegalQADocument,
        TaskType.PROCEDURAL_GUIDANCE: ProceduralGuidanceDocument,
        TaskType.DRAFTING: DraftingExampleDocument,
        TaskType.MULTILINGUAL: LegalQADocument,
        TaskType.SAFETY: LegalQADocument,
    }
    return mapping.get(task_type, LegalQADocument)


def get_output_filename(task_type: TaskType) -> str:
    """Get the output JSONL filename for a task type."""
    mapping = {
        TaskType.STATUTORY_QA: "legal_qa.jsonl",
        TaskType.JUDGMENT_ANALYSIS: "case_analysis.jsonl",
        TaskType.CASE_REASONING: "legal_qa.jsonl",
        TaskType.PROCEDURAL_GUIDANCE: "procedural_guide.jsonl",
        TaskType.DRAFTING: "drafting_examples.jsonl",
        TaskType.MULTILINGUAL: "legal_qa.jsonl",
        TaskType.SAFETY: "legal_qa.jsonl",
    }
    return mapping.get(task_type, "legal_qa.jsonl")