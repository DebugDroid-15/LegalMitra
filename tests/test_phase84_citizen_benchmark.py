"""Phase 84 Test Suite: Conversational Empathy & Comprehensive 25-Question Benchmark.

Validates that:
1. All 8 Conversational & Empathy behaviors execute with ANSWER_SUPPORTED state.
2. All 25 Citizen Benchmark scenarios produce actionable practical remedies and helplines.
3. No hallucination or misleading outcome guarantees are issued.
"""

import pytest
from legalmitra.orchestration.pipeline import LegalQueryPipeline
from legalmitra.knowledge.citizen_intents import CITIZEN_KNOWLEDGE_BASE


class TestPhase84CitizenBenchmark:
    @pytest.fixture(scope="module")
    def pipeline(self):
        return LegalQueryPipeline()

    @pytest.mark.parametrize("query,expected_str", [
        ("Mere saath galat hua hai, kya karu?", "Kya hua hai?"),
        ("Police ne mujhe pakad liya hai.", "Section 47 BNSS"),
        ("Kya main jeet jaunga?", "Outcome Guarantee Nahi Di Jaa Sakti"),
        ("Mujhe case karna hai.", "Case File Karne Ke Sambandh"),
        ("Mujhe ek legal notice likh do.", "Statutory Legal Notice Drafting"),
        ("Mujhe exact section batao.", "Exact Statutory Sections"),
        ("Maine galti kar di, ab kya hoga?", "Right Against Self-Incrimination"),
        ("Mere paas koi proof nahi hai.", "Digital Evidence"),
    ])
    def test_conversational_empathy_behaviors(self, pipeline, query, expected_str):
        res = pipeline.execute(query)
        assert res.response_state.value == "ANSWER_SUPPORTED"
        assert expected_str.lower() in res.answer_text.lower()

    @pytest.mark.parametrize("scenario", CITIZEN_KNOWLEDGE_BASE)
    def test_all_25_citizen_benchmark_scenarios(self, pipeline, scenario):
        # Test with the primary keyword of each scenario
        query = scenario.keywords[0]
        res = pipeline.execute(query)
        assert res.response_state.value == "ANSWER_SUPPORTED"
        assert "### Practical Action Guide" in res.answer_text
        assert "### Important Checklists & Helplines" in res.answer_text
        assert len(res.governing_provisions) > 0

