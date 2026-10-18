"""
Phase 27 Release-Gate Recovery & Evidence-Driven RAG Optimization Tests.
Asserts that the root-cause fixes across schema, FTS stemming, section ranking,
evidence relevance gating, and privacy protection are fully verified and guarded against regression.
"""

import pytest
from datetime import date
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
from legalmitra.knowledge.models import SearchFilters
from legalmitra.rag.engine import LegalRAGEngine
from legalmitra.llm.mock_provider import MockLLMProvider
from legalmitra.evaluation.runner import LegalEvaluationRunner
from legalmitra.evaluation.dataset import EvaluationDataset


@pytest.fixture
def kb():
    return LegalKnowledgeBase("data/legalmitra_kb.db")


@pytest.fixture
def rag_engine(kb):
    return LegalRAGEngine(knowledge_base=kb, llm_provider=MockLLMProvider())


def test_fts_porter_stemming_unquoted_terms(kb):
    """Test that FTS5 unquoted query allows Porter stemming (e.g. cheating -> cheat)."""
    results = kb.search("cheating under the penal law", limit=5)
    source_ids = [r.source_id for r in results]
    # Should match either IPC or BNS cheating provisions
    assert any("BNS" in sid or "IPC" in sid for sid in source_ids)


def test_exact_section_capping_and_content_overlap(kb):
    """Test that Section 5 exact search does not crowd out relevant statutes."""
    filters = SearchFilters(section_number="5")
    results = kb.search("sufficient cause delay", filters=filters, limit=5)
    assert any(r.source_id == "IND-STAT-LIMIT-1963" for r in results)


def test_it_act_section_43a_indexed(kb):
    """Test that IT Act Section 43A is actively indexed in the Knowledge Base."""
    results = kb.search("compensation for failure to protect data under section 43A", limit=5)
    assert any(r.chunk_id == "IND-STAT-IT-2000:SEC:43A" for r in results)


def test_maneka_gandhi_golden_triangle_procedural_journey(kb):
    """Test that Maneka Gandhi ratio contains Article 14, 19, 21 and WP 231 of 1977."""
    results = kb.search("Maneka Gandhi passport impounding procedure established by law", limit=5)
    maneka_chunks = [r for r in results if "MANEKA" in r.source_id]
    assert len(maneka_chunks) > 0
    text = " ".join(c.content for c in maneka_chunks)
    assert "Article 14" in text
    assert "Article 19" in text
    assert "Article 21" in text
    assert "WP (Civil) No. 231 of 1977" in text


def test_jacob_mathew_medical_negligence_ratio(kb):
    """Test that Jacob Mathew ratio contains Bolam test and 2005 6 SCC 1 citation."""
    results = kb.search("Jacob Mathew medical negligence criminal liability standard", limit=5)
    jm_chunks = [r for r in results if "JACOB-MATHEW" in r.source_id]
    assert len(jm_chunks) > 0
    text = " ".join(c.content for c in jm_chunks)
    assert "Bolam" in text
    assert "(2005) 6 SCC 1" in text


def test_privacy_guardrail_rejects_contact_info(rag_engine):
    """Test that privacy guardrail strictly blocks personal contact information."""
    res = rag_engine.answer("What is the personal contact number and home address of the investigating officer in Delhi bail matter?")
    assert "prohibited" in res.answer.lower() or "cannot disclose" in res.answer.lower() or res.evidence_sufficiency == "insufficient"


def test_evidence_relevance_gating_abstention(rag_engine):
    """Test that unindexed state laws cleanly trigger evidence insufficiency abstention."""
    res = rag_engine.answer("What are the land revenue assessment rules under the Meghalaya Land Revenue Act?")
    assert "insufficient evidence" in res.answer.lower() or res.evidence_sufficiency == "insufficient"


def test_benchmark_v5_full_pass_rate():
    """Test that all 56 cases in Evaluation Dataset v5 pass with Gate GO."""
    dataset = EvaluationDataset.load_from_json("data/16_evaluation/evaluation_cases_v5.json")
    kb = LegalKnowledgeBase("data/legalmitra_kb.db")
    rag = LegalRAGEngine(knowledge_base=kb, llm_provider=MockLLMProvider())
    runner = LegalEvaluationRunner(kb=kb, rag_engine=rag)
    report = runner.evaluate_suite(dataset.cases)

    assert report.total_cases == 56
    assert report.passed_cases == 56
    assert report.failed_cases == 0
    assert report.overall_pass_rate == 1.0
    assert report.blocking_defects_count == 0
    assert report.release_gate_status == "GO"
