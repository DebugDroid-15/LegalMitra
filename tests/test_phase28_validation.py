"""
Tests for Phase 28: Independent Legal Answer Validation, Claim-Level Citation Auditing,
and Temporal Integrity.
"""

import pytest
from datetime import date
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
from legalmitra.knowledge.models import SearchFilters
from legalmitra.rag.engine import LegalRAGEngine
from legalmitra.rag.schemas import ClaimType, ClaimVerificationStatus
from legalmitra.llm.mock_provider import MockLLMProvider
from legalmitra.evaluation.runner import LegalEvaluationRunner
from legalmitra.evaluation.dataset import EvaluationDataset


@pytest.fixture
def kb():
    return LegalKnowledgeBase("data/legalmitra_kb.db")


@pytest.fixture
def rag_engine(kb):
    return LegalRAGEngine(knowledge_base=kb, llm_provider=MockLLMProvider())


def test_claim_level_decomposition_populated(rag_engine):
    """Test that LegalRAGEngine produces structured claims with provenance."""
    resp = rag_engine.answer("What does Section 61 of the Bharatiya Sakshya Adhiniyam provide?")
    assert len(resp.claims) > 0
    for clm in resp.claims:
        assert clm.claim_id.startswith("CLM-")
        assert isinstance(clm.claim_type, ClaimType)
        assert clm.verification_status in (
            ClaimVerificationStatus.VERIFIED_GROUNDED,
            ClaimVerificationStatus.UNSUPPORTED,
            ClaimVerificationStatus.OUTDATED,
        )
        assert clm.jurisdiction == "IN"


def test_mva_commencement_date_verified(kb):
    """Test that Motor Vehicles Act 1988 effective_date is 1989-07-01 and NOT 2005-10-12."""
    cursor = kb.conn.cursor()
    cursor.execute("SELECT DISTINCT effective_date FROM legal_chunks WHERE source_id = 'IND-ACT-1988-MVA'")
    dates = [r[0] for r in cursor.fetchall()]
    assert dates == ["1989-07-01"]


def test_pocso_commencement_date_verified(kb):
    """Test that POCSO Act effective_date is 2012-11-14 and NOT 2005-10-12."""
    cursor = kb.conn.cursor()
    cursor.execute("SELECT DISTINCT effective_date FROM legal_chunks WHERE source_id IN ('IND-ACT-2012-POCSO', 'IND-STAT-POCSO-2012-SEC4')")
    dates = [r[0] for r in cursor.fetchall()]
    assert dates == ["2012-11-14"]


def test_it_act_2008_amendments_commencement_verified(kb):
    """Test that IT Act Section 43A and 66A-F effective_date is 2009-10-27."""
    cursor = kb.conn.cursor()
    cursor.execute("SELECT DISTINCT effective_date FROM legal_chunks WHERE source_id = 'IND-STAT-IT-2000' AND section_number IN ('43A', '66A', '66B', '66C', '66D', '66E', '66F')")
    dates = [r[0] for r in cursor.fetchall()]
    assert dates == ["2009-10-27"]


def test_anvar_pv_electronic_evidence_retrieval(kb):
    """Test retrieval of Anvar P.V. v. P.K. Basheer landmark ruling on Section 65B."""
    filters = SearchFilters(court="Supreme Court of India")
    hits = kb.search("Anvar P.V. Basheer Section 65B certificate electronic evidence", filters=filters, limit=5)
    assert any("ANVAR" in h.source_id for h in hits)


def test_arnesh_kumar_arrest_guidelines_retrieval(kb):
    """Test retrieval of Arnesh Kumar v. State of Bihar arrest guidelines under Section 41."""
    filters = SearchFilters(court="Supreme Court of India")
    hits = kb.search("Arnesh Kumar State of Bihar Section 498A arrest checklist", filters=filters, limit=5)
    assert any("ARNESH" in h.source_id for h in hits)


def test_benchmark_v6_manifest_and_evaluation():
    """Test that Benchmark v6 runs all 68 cases with 100% pass rate and Gate GO."""
    dataset = EvaluationDataset.load_from_json("data/17_evaluation/evaluation_cases_v6.json")
    assert len(dataset.cases) == 68

    kb = LegalKnowledgeBase("data/legalmitra_kb.db")
    rag = LegalRAGEngine(knowledge_base=kb, llm_provider=MockLLMProvider())
    runner = LegalEvaluationRunner(kb=kb, rag_engine=rag)
    report = runner.evaluate_suite(dataset.cases)

    assert report.total_cases == 68
    assert report.passed_cases == 68
    assert report.failed_cases == 0
    assert report.overall_pass_rate == 1.0
    assert report.blocking_defects_count == 0
    assert report.release_gate_status == "GO"
    assert report.claim_support_rate >= 0.95
