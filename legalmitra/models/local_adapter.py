"""Local fine-tuned legal model adapter module for LegalMitra.

Provides an enterprise-grade inference adapter layer that loads fine-tuned
LoRA weights (Llama-3.1-8B-Instruct) for conversational, natural IRAC legal answers
grounded strictly in retrieved evidence, with complete fallback to deterministic synthesis.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ModelExecutionMode(str, Enum):
    """Execution mode of the legal model adapter."""
    DETERMINISTIC_FALLBACK = "deterministic_fallback"
    MOCK_NEURAL = "mock_neural"
    LOCAL_LORA = "local_lora"


@dataclass
class ModelAdapterConfig:
    """Configuration for local model adapter."""
    adapter_path: Path = field(
        default_factory=lambda: Path(__file__).resolve().parent.parent.parent / "models" / "legalmitra_lora_adapter"
    )
    base_model_name_or_path: str = "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit"
    max_new_tokens: int = 768
    temperature: float = 0.2
    top_p: float = 0.9
    load_in_4bit: bool = True
    device: str = "auto"
    enable_mock_for_testing: bool = False


@dataclass
class ModelGenerationResult:
    """Result of natural answer generation."""
    answer_text: str
    execution_mode: ModelExecutionMode
    model_version: str
    is_grounded: bool
    fallback_used: bool
    error_message: Optional[str] = None
    prompt_token_count: Optional[int] = None
    generated_token_count: Optional[int] = None


class LocalLegalModelAdapter:
    """Manages local fine-tuned LoRA weights and prompt synthesis."""

    def __init__(self, config: Optional[ModelAdapterConfig] = None) -> None:
        self.config = config or ModelAdapterConfig()
        self._model = None
        self._tokenizer = None
        self._is_loaded = False
        self._adapter_available = self._check_adapter_availability()

    def _check_adapter_availability(self) -> bool:
        """Verify that the required LoRA adapter files exist."""
        p = Path(self.config.adapter_path)
        if not p.exists() or not p.is_dir():
            return False
        weight_file = p / "adapter_model.safetensors"
        config_file = p / "adapter_config.json"
        return weight_file.exists() and config_file.exists()

    @property
    def is_available(self) -> bool:
        """Check whether local model can be run (or mock is active)."""
        if self.config.enable_mock_for_testing:
            return True
        return self._adapter_available

    def load_model(self) -> bool:
        """Attempt to load the base model and LoRA adapter into memory."""
        if self.config.enable_mock_for_testing:
            self._is_loaded = True
            logger.info("LocalLegalModelAdapter: Mock neural model loaded for testing.")
            return True

        if not self._adapter_available:
            logger.warning(
                "LocalLegalModelAdapter: Adapter files not found at %s. Falling back to deterministic mode.",
                self.config.adapter_path
            )
            return False

        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
            from peft import PeftModel

            logger.info("Loading tokenizer from %s...", self.config.adapter_path)
            self._tokenizer = AutoTokenizer.from_pretrained(str(self.config.adapter_path))

            logger.info("Loading base model: %s...", self.config.base_model_name_or_path)
            bnb_config = None
            if self.config.load_in_4bit and torch.cuda.is_available():
                bnb_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.float16,
                )

            base_model = AutoModelForCausalLM.from_pretrained(
                self.config.base_model_name_or_path,
                quantization_config=bnb_config,
                device_map=self.config.device,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                low_cpu_mem_usage=True
            )

            logger.info("Attaching LoRA adapter from %s...", self.config.adapter_path)
            self._model = PeftModel.from_pretrained(
                base_model,
                str(self.config.adapter_path)
            )
            self._model.eval()
            self._is_loaded = True
            logger.info("LocalLegalModelAdapter: Successfully loaded fine-tuned model.")
            return True

        except Exception as exc:
            logger.error("Failed to load local model adapter: %s. Reverting to fallback.", exc)
            self._is_loaded = False
            return False

    def build_irac_prompt(
        self,
        query: str,
        provisions: List[Dict[str, Any]],
        precedents: List[Dict[str, Any]],
        temporal_context: Optional[str] = None
    ) -> str:
        """Format the query and retrieved evidence into Llama-3.1 IRAC prompt."""
        evidence_lines = []
        if temporal_context:
            evidence_lines.append(f"Temporal Assessment: {temporal_context}")

        if provisions:
            evidence_lines.append("Statutory Provisions:")
            for p in provisions:
                act = p.get("act", "Statute")
                sec = p.get("section", "")
                text = p.get("text", "")
                evidence_lines.append(f"- {act} {sec}: {text}")

        if precedents:
            evidence_lines.append("Judicial Precedents:")
            for prec in precedents:
                title = prec.get("case_title", "Precedent")
                cit = prec.get("citation", "")
                ratio = prec.get("ratio", "")
                evidence_lines.append(f"- {title} ({cit}): {ratio}")

        evidence_str = "\n".join(evidence_lines)

        user_content = (
            f"Legal Query: {query}\n\n"
            f"Evidence and Precedents:\n{evidence_str}\n\n"
            f"Please provide an authoritative IRAC response (Issue, Rule, Application, Conclusion) "
            f"grounded strictly in the statutory provisions and precedents above."
        )

        prompt = (
            "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
            "You are LegalMitra AI, an expert Indian legal assistant. You answer queries using IRAC methodology "
            "grounded strictly in the provided statutory provisions and court precedents. Never extrapolate beyond verified facts.<|eot_id|>\n"
            f"<|start_header_id|>user<|end_header_id|>\n\n{user_content}<|eot_id|>\n"
            "<|start_header_id|>assistant<|end_header_id|>\n\n"
        )
        return prompt

    def generate_natural_answer(
        self,
        query: str,
        provisions: List[Dict[str, Any]],
        precedents: List[Dict[str, Any]],
        temporal_context: Optional[str] = None
    ) -> ModelGenerationResult:
        """Generate a natural conversational legal response grounded in evidence."""
        # 1. Handle mock testing mode
        if self.config.enable_mock_for_testing:
            simulated_answer = self._generate_mock_response(query, provisions, precedents)
            return ModelGenerationResult(
                answer_text=simulated_answer,
                execution_mode=ModelExecutionMode.MOCK_NEURAL,
                model_version="LegalMitra-Llama3.1-8B-LoRA-v1-mock",
                is_grounded=True,
                fallback_used=False
            )

        # 2. Check if model is loaded or can be loaded
        if not self._is_loaded:
            loaded = self.load_model()
            if not loaded:
                return ModelGenerationResult(
                    answer_text="",
                    execution_mode=ModelExecutionMode.DETERMINISTIC_FALLBACK,
                    model_version="none",
                    is_grounded=False,
                    fallback_used=True,
                    error_message="Model adapter not loaded or unavailable."
                )

        # 3. Real neural generation
        try:
            import torch

            prompt = self.build_irac_prompt(query, provisions, precedents, temporal_context)
            inputs = self._tokenizer(prompt, return_tensors="pt")
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}

            with torch.no_grad():
                outputs = self._model.generate(
                    **inputs,
                    max_new_tokens=self.config.max_new_tokens,
                    temperature=self.config.temperature,
                    top_p=self.config.top_p,
                    pad_token_id=self._tokenizer.eos_token_id,
                    do_sample=True if self.config.temperature > 0 else False
                )

            # Extract generated tokens
            input_len = inputs["input_ids"].shape[1]
            generated_tokens = outputs[0][input_len:]
            generated_text = self._tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()

            return ModelGenerationResult(
                answer_text=generated_text,
                execution_mode=ModelExecutionMode.LOCAL_LORA,
                model_version="LegalMitra-Llama3.1-8B-LoRA-v1",
                is_grounded=True,
                fallback_used=False,
                prompt_token_count=input_len,
                generated_token_count=len(generated_tokens)
            )

        except Exception as exc:
            logger.error("Neural generation error: %s. Falling back to deterministic assembly.", exc)
            return ModelGenerationResult(
                answer_text="",
                execution_mode=ModelExecutionMode.DETERMINISTIC_FALLBACK,
                model_version="none",
                is_grounded=False,
                fallback_used=True,
                error_message=str(exc)
            )

    def _generate_mock_response(
        self,
        query: str,
        provisions: List[Dict[str, Any]],
        precedents: List[Dict[str, Any]]
    ) -> str:
        """Produce deterministic mock IRAC text for validation and automated testing."""
        prov_summary = ", ".join(f"{p.get('act', '')} {p.get('section', '')}".strip() for p in provisions) or "Relevant Statutory Law"
        prec_summary = ", ".join(prec.get("case_title", "") for prec in precedents if prec.get("case_title")) or "Established Precedents"

        return (
            f"### Issue\n"
            f"The legal inquiry concerns: {query.strip()}\n\n"
            f"### Applicable Rule of Law\n"
            f"The governing statutory framework includes {prov_summary}. "
            f"The judicial authority governing this matter includes {prec_summary}.\n\n"
            f"### Legal Application & Analysis\n"
            f"Under the codified statutory mandate, the procedural and substantive prerequisites must be strictly adhered to. "
            f"Applying the principles settled in {prec_summary}, the rights and liabilities of the parties are governed by the authoritative text of the law.\n\n"
            f"### Conclusion\n"
            f"Based on {prov_summary} and binding precedents, the statutory requirements are satisfied and operative."
        )
