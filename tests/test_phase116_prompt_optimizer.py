"""
Unit tests for Phase 116: Local GGUF Prompt Optimization & Structured Synthesis.
"""

import pytest
from legalmitra.models.prompt_optimizer import GGUFStructuredPromptBuilder, SOVEREIGN_SYSTEM_PROMPT
from legalmitra.models.gguf_adapter import LocalGGUFModelAdapter, GGUFAdapterConfig


class TestPhase116PromptOptimizer:
    def test_optimized_prompt_structure(self):
        query = "Can police arrest me without warrant for cognizable offence?"
        provisions = [
            {"act": "The Bharatiya Nagarik Suraksha Sanhita, 2023", "section": "Section 35", "text": "When police may arrest without warrant."}
        ]
        precedents = [
            {"case_title": "Arnesh Kumar v. State of Bihar", "citation": "(2014) 8 SCC 273", "ratio": "Notice under Section 41A must be served for offences up to 7 years."}
        ]

        prompt = GGUFStructuredPromptBuilder.build_optimized_prompt(
            query=query,
            provisions=provisions,
            precedents=precedents,
            include_few_shot=True
        )

        assert "<|start_header_id|>system<|end_header_id|>" in prompt
        assert "Bharatiya Nagarik Suraksha Sanhita" in prompt
        assert "Arnesh Kumar" in prompt
        assert "### ⚖️ Direct Position" in prompt  # Few-shot exemplar included
        assert "<|start_header_id|>assistant<|end_header_id|>" in prompt

    def test_gguf_adapter_uses_optimized_builder(self):
        adapter = LocalGGUFModelAdapter(GGUFAdapterConfig(enable_mock_for_testing=True))
        prompt = adapter.build_prompt(
            query="test query",
            provisions=[{"act": "BNS", "section": "318", "text": "Cheating"}],
            precedents=[]
        )
        assert "Sovereign Indian legal intelligence engine" in prompt or "LegalMitra AI" in prompt
        assert "<|start_header_id|>system<|end_header_id|>" in prompt
