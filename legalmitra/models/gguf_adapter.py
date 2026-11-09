"""Local GGUF CPU inference adapter for LegalMitra (Phase 76 & 79).

Integrates llama-cpp-python to run quantized 4-bit Llama-3.1-8B-Instruct
with fine-tuned LegalMitra LoRA delta weights directly on CPU without GPU dependencies.
Supports both batch generation and real-time Server-Sent Events (SSE) token streaming.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

from legalmitra.models.local_adapter import ModelExecutionMode, ModelGenerationResult

logger = logging.getLogger(__name__)


@dataclass
class GGUFAdapterConfig:
    """Configuration for local GGUF CPU adapter."""
    base_model_path: Path = field(
        default_factory=lambda: Path(__file__).resolve().parent.parent.parent / "models" / "Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
    )
    lora_adapter_path: Path = field(
        default_factory=lambda: Path(__file__).resolve().parent.parent.parent / "models" / "legalmitra-lora-adapter.gguf"
    )
    n_ctx: int = 2048
    n_threads: int = 6
    max_new_tokens: int = 384
    temperature: float = 0.2
    top_p: float = 0.9
    enable_mock_for_testing: bool = False


class LocalGGUFModelAdapter:
    """Manages offline CPU inference using llama-cpp-python with dynamic LoRA injection."""

    def __init__(self, config: Optional[GGUFAdapterConfig] = None) -> None:
        self.config = config or GGUFAdapterConfig()
        self._llm = None
        self._is_loaded = False

    @property
    def is_available(self) -> bool:
        """Check whether local GGUF model files exist or mock mode is enabled."""
        if self.config.enable_mock_for_testing:
            return True
        base_exists = Path(self.config.base_model_path).exists()
        lora_exists = Path(self.config.lora_adapter_path).exists()
        return base_exists and lora_exists

    def load_model(self) -> bool:
        """Load the 4-bit base model into CPU memory and attach the LoRA adapter."""
        if self.config.enable_mock_for_testing:
            self._is_loaded = True
            logger.info("LocalGGUFModelAdapter: Mock mode active for testing.")
            return True

        if not self.is_available:
            logger.warning(
                "LocalGGUFModelAdapter: Missing GGUF model files (Base: %s, LoRA: %s)",
                self.config.base_model_path,
                self.config.lora_adapter_path
            )
            return False

        try:
            import llama_cpp

            logger.info(
                "Loading base model (%s) with LoRA (%s) on CPU...",
                self.config.base_model_path,
                self.config.lora_adapter_path
            )
            self._llm = llama_cpp.Llama(
                model_path=str(self.config.base_model_path),
                lora_path=str(self.config.lora_adapter_path),
                n_ctx=self.config.n_ctx,
                n_threads=self.config.n_threads,
                verbose=False
            )
            self._is_loaded = True
            logger.info("LocalGGUFModelAdapter: Model and LoRA loaded successfully on CPU.")
            return True

        except Exception as exc:
            logger.error("Failed to load local GGUF model: %s", exc)
            self._is_loaded = False
            return False

    def build_prompt(
        self,
        query: str,
        provisions: List[Dict[str, Any]],
        precedents: List[Dict[str, Any]],
        temporal_context: Optional[str] = None,
        dialogue_history: Optional[str] = None
    ) -> str:
        """Format the legal prompt using Phase 116 GGUFStructuredPromptBuilder."""
        from legalmitra.models.prompt_optimizer import GGUFStructuredPromptBuilder
        return GGUFStructuredPromptBuilder.build_optimized_prompt(
            query=query,
            provisions=provisions,
            precedents=precedents,
            temporal_context=temporal_context,
            dialogue_history=dialogue_history,
            include_few_shot=True
        )

    def generate_natural_answer(
        self,
        query: str,
        provisions: List[Dict[str, Any]],
        precedents: List[Dict[str, Any]],
        temporal_context: Optional[str] = None,
        dialogue_history: Optional[str] = None
    ) -> ModelGenerationResult:
        """Generate legal response using local quantized GGUF model in batch mode."""
        if self.config.enable_mock_for_testing:
            simulated = (
                f"### Issue\nApplicability of penal provisions to query: '{query}'.\n\n"
                f"### Rule\nUnder Bharatiya Nyaya Sanhita, 2023, relevant provisions prescribe statutory penalties.\n\n"
                f"### Application\nThe facts conform to the statutory elements.\n\n"
                f"### Conclusion\nThe party is subject to legal remedies."
            )
            return ModelGenerationResult(
                answer_text=simulated,
                execution_mode=ModelExecutionMode.MOCK_NEURAL,
                model_version="LegalMitra-Llama3.1-8B-GGUF-Q4_K_M-mock",
                is_grounded=True,
                fallback_used=False
            )

        if not self._is_loaded:
            success = self.load_model()
            if not success:
                return ModelGenerationResult(
                    answer_text="",
                    execution_mode=ModelExecutionMode.DETERMINISTIC_FALLBACK,
                    model_version="none",
                    is_grounded=False,
                    fallback_used=True,
                    error_message="GGUF model or LoRA adapter not loaded."
                )

        try:
            prompt = self.build_prompt(query, provisions, precedents, temporal_context, dialogue_history)
            output = self._llm(
                prompt,
                max_tokens=self.config.max_new_tokens,
                temperature=self.config.temperature,
                top_p=self.config.top_p,
                stop=["<|eot_id|>", "<|end_of_text|>"]
            )
            generated_text = output["choices"][0]["text"].strip()
            usage = output.get("usage", {})

            return ModelGenerationResult(
                answer_text=generated_text,
                execution_mode=ModelExecutionMode.LOCAL_LORA,
                model_version="LegalMitra-Llama3.1-8B-GGUF-Q4_K_M",
                is_grounded=True,
                fallback_used=False,
                prompt_token_count=usage.get("prompt_tokens"),
                generated_token_count=usage.get("completion_tokens")
            )

        except Exception as exc:
            logger.error("Error during GGUF generation: %s", exc)
            return ModelGenerationResult(
                answer_text="",
                execution_mode=ModelExecutionMode.DETERMINISTIC_FALLBACK,
                model_version="none",
                is_grounded=False,
                fallback_used=True,
                error_message=str(exc)
            )

    def stream_natural_answer(
        self,
        query: str,
        provisions: List[Dict[str, Any]],
        precedents: List[Dict[str, Any]],
        temporal_context: Optional[str] = None,
        dialogue_history: Optional[str] = None
    ) -> Iterator[str]:
        """Stream generated response token-by-token (Phase 79)."""
        if self.config.enable_mock_for_testing:
            mock_tokens = [
                "### Issue\n", "The legal inquiry ", f"concerns '{query}'.\n\n",
                "### Rule\n", "Under the Bharatiya Nyaya Sanhita, 2023, ", "the statutory provisions govern.\n\n",
                "### Conclusion\n", "The matter stands resolved in accordance with law."
            ]
            for tok in mock_tokens:
                yield tok
            return

        if not self._is_loaded:
            success = self.load_model()
            if not success:
                yield "Error: Local GGUF model weights are not loaded. Reverting to deterministic response."
                return

        try:
            prompt = self.build_prompt(query, provisions, precedents, temporal_context, dialogue_history)
            stream_gen = self._llm(
                prompt,
                max_tokens=self.config.max_new_tokens,
                temperature=self.config.temperature,
                top_p=self.config.top_p,
                stop=["<|eot_id|>", "<|end_of_text|>"],
                stream=True
            )
            for chunk in stream_gen:
                delta = chunk["choices"][0]["text"]
                if delta:
                    yield delta

        except Exception as exc:
            logger.error("Error during GGUF token streaming: %s", exc)
            yield f"\n[Streaming Interrupted: {exc}]"
