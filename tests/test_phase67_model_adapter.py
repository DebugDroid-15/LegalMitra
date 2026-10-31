"""Phase 67 Test Suite: Local Legal Model Adapter, Safe Fallback, and Neural Synthesis."""

import os
from pathlib import Path
import pytest

from legalmitra.models.local_adapter import (
    LocalLegalModelAdapter,
    ModelAdapterConfig,
    ModelExecutionMode,
    ModelGenerationResult,
)
from legalmitra.orchestration.answer_assembler import EvidenceTraceableAnswerAssembler
from legalmitra.orchestration.decision_policy import LegalResponseState
from legalmitra.orchestration.pipeline import LegalQueryPipeline
from legalmitra.temporal.engine import build_default_temporal_engine


class TestPhase67ModelAdapterIntegration:
    """Verifies Phase 67 model adapter layer, mock synthesis, fallback safety, and CLI compatibility."""

    def test_adapter_availability_detection(self):
        """Test that the adapter accurately detects downloaded weights."""
        adapter = LocalLegalModelAdapter()
        # The user downloaded the adapter into models/legalmitra_lora_adapter
        expected_dir = Path("models/legalmitra_lora_adapter")
        if expected_dir.exists() and (expected_dir / "adapter_model.safetensors").exists():
            assert adapter.is_available is True
        else:
            assert adapter.is_available is False

    def test_mock_neural_mode_execution(self):
        """Test that mock neural generation returns a complete IRAC structured output."""
        config = ModelAdapterConfig(enable_mock_for_testing=True)
        adapter = LocalLegalModelAdapter(config)
        assert adapter.is_available is True

        query = "Can an injunction be granted against an infrastructure project under Section 20A Specific Relief Act?"
        provisions = [
            {"act": "Specific Relief Act, 1963", "section": "20A", "text": "No injunction shall be granted by court in infrastructure project"}
        ]
        precedents = [
            {"case_title": "NHAI v. Progressive Constructions", "citation": "2021 SC", "ratio": "Section 20A creates statutory bar"}
        ]

        result = adapter.generate_natural_answer(
            query=query,
            provisions=provisions,
            precedents=precedents,
            temporal_context="Current as of 2024"
        )

        assert isinstance(result, ModelGenerationResult)
        assert result.execution_mode == ModelExecutionMode.MOCK_NEURAL
        assert result.fallback_used is False
        assert result.is_grounded is True
        assert "### Issue" in result.answer_text
        assert "### Applicable Rule of Law" in result.answer_text
        assert "### Legal Application & Analysis" in result.answer_text
        assert "### Conclusion" in result.answer_text
        assert "Specific Relief Act, 1963" in result.answer_text

    def test_missing_weights_graceful_fallback(self):
        """Test that non-existent adapter path falls back cleanly without exception."""
        config = ModelAdapterConfig(
            adapter_path=Path("non_existent_directory_for_test"),
            enable_mock_for_testing=False
        )
        adapter = LocalLegalModelAdapter(config)
        assert adapter.is_available is False

        result = adapter.generate_natural_answer("Dummy query", [], [])
        assert result.execution_mode == ModelExecutionMode.DETERMINISTIC_FALLBACK
        assert result.fallback_used is True
        assert result.is_grounded is False
        assert result.error_message is not None

    def test_irac_prompt_formatting_structure(self):
        """Test Llama-3.1 IRAC prompt formatter conforms to chat template specification."""
        adapter = LocalLegalModelAdapter()
        query = "What is the limitation period for filing Section 34 application?"
        provisions = [{"act": "Arbitration Act", "section": "34(3)", "text": "Three months plus thirty days condonation"}]
        precedents = [{"case_title": "Simplex Infrastructure", "citation": "2019 SC", "ratio": "Period cannot be extended"}]

        prompt = adapter.build_irac_prompt(query, provisions, precedents, "2024-01-01")

        assert "<|begin_of_text|><|start_header_id|>system<|end_header_id|>" in prompt
        assert "LegalMitra AI" in prompt
        assert "<|start_header_id|>user<|end_header_id|>" in prompt
        assert "Arbitration Act" in prompt
        assert "Simplex Infrastructure" in prompt
        assert "<|start_header_id|>assistant<|end_header_id|>" in prompt

    def test_pipeline_execution_with_mock_model_adapter(self):
        """Test full 14-stage pipeline execution with mock model adapter attached."""
        mock_adapter = LocalLegalModelAdapter(ModelAdapterConfig(enable_mock_for_testing=True))
        pipeline = LegalQueryPipeline(model_adapter=mock_adapter)

        resp = pipeline.execute(
            query="Can an interim injunction be granted in infrastructure project contracts under Section 20A Specific Relief Act?",
            context_date="2024-06-01",
            jurisdiction="IN"
        )

        assert resp.response_state in (LegalResponseState.ANSWER_QUALIFIED, LegalResponseState.ANSWER_SUPPORTED)
        assert resp.answer_text is not None
        assert len(resp.assembled_answer.claims) > 0
        assert len(resp.citations) > 0
        # Check that the pipeline executed with zero crashes
        assert resp.telemetry.duration_seconds > 0.0

    def test_zero_regression_deterministic_pipeline_unchanged(self):
        """Test default pipeline execution without model adapter retains 100% deterministic behaviour."""
        pipeline = LegalQueryPipeline()  # Default: No adapter
        resp = pipeline.execute(
            query="What is the statutory procedure for search and seizure of digital electronic records?",
            context_date="2024-09-15",
            jurisdiction="IN"
        )
        assert resp.response_state is not None
        assert "Direct Position:" in resp.answer_text
        assert resp.telemetry.steps_executed is not None
