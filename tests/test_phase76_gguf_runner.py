"""Tests for Phase 76: Local GGUF CPU inference adapter with LoRA delta weights."""

from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

from legalmitra.models.gguf_adapter import GGUFAdapterConfig, LocalGGUFModelAdapter
from legalmitra.models.local_adapter import ModelExecutionMode


class TestPhase76GGUFRunner:
    """Test suite certifying local GGUF CPU model adapter."""

    def test_gguf_config_defaults(self):
        """Verify default filepaths and parameters."""
        config = GGUFAdapterConfig()
        assert "Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf" in str(config.base_model_path)
        assert "legalmitra-lora-adapter.gguf" in str(config.lora_adapter_path)
        assert config.n_ctx == 2048
        assert config.n_threads == 6

    def test_gguf_mock_mode_generation(self):
        """Test mock generation for pipeline test suites."""
        config = GGUFAdapterConfig(enable_mock_for_testing=True)
        adapter = LocalGGUFModelAdapter(config)
        assert adapter.is_available is True

        result = adapter.generate_natural_answer(
            query="Punishment for theft under BNS?",
            provisions=[{"act": "Bharatiya Nyaya Sanhita, 2023", "section": "Section 303(2)", "text": "Punishment for theft"}],
            precedents=[]
        )
        assert result.execution_mode == ModelExecutionMode.MOCK_NEURAL
        assert result.is_grounded is True
        assert "Bharatiya Nyaya Sanhita" in result.answer_text

    def test_gguf_prompt_structure(self):
        """Verify Llama-3.1 IRAC prompt format with system/user/assistant tags."""
        adapter = LocalGGUFModelAdapter()
        prompt = adapter.build_prompt(
            query="Can land be gifted orally?",
            provisions=[{"act": "Transfer of Property Act, 1882", "section": "Section 123", "text": "Gift of immovable property"}],
            precedents=[{"case_title": "Gomtibai v. Mattulal", "citation": "1996 SC", "ratio": "Oral gift of land is void"}],
            temporal_context="Pre-2024 Act Applies"
        )
        assert "<|start_header_id|>system<|end_header_id|>" in prompt
        assert "Transfer of Property Act, 1882 Section 123" in prompt
        assert "Gomtibai v. Mattulal (1996 SC)" in prompt
        assert "<|start_header_id|>assistant<|end_header_id|>" in prompt

    def test_gguf_real_files_detected_on_disk(self):
        """Verify that the actual base and LoRA GGUF files downloaded in models/ are detected."""
        adapter = LocalGGUFModelAdapter()
        assert adapter.is_available is True

    def test_gguf_fallback_on_missing_model(self):
        """Verify graceful fallback if model paths do not exist."""
        config = GGUFAdapterConfig(
            base_model_path=Path("non_existent_base.gguf"),
            lora_adapter_path=Path("non_existent_lora.gguf")
        )
        adapter = LocalGGUFModelAdapter(config)
        assert adapter.is_available is False

        result = adapter.generate_natural_answer("Query", [], [])
        assert result.fallback_used is True
        assert result.execution_mode == ModelExecutionMode.DETERMINISTIC_FALLBACK

