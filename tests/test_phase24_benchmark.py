"""
Test Suite: tests/test_phase24_benchmark.py
Tests Phase 24 National Legal Corpus, Judicial Records, and Evaluation Dataset v3.
"""

from __future__ import annotations

import json
from pathlib import Path
import sqlite3
import pytest

from legalmitra.caselaw.knowledge_graph import build_national_judicial_knowledge_graph
from legalmitra.evaluation.dataset import EvaluationDataset
from legalmitra.evaluation.models import AnswerExpectedType, EvaluationCase, EvaluationCategory
from legalmitra.evaluation.runner import LegalEvaluationRunner
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
from legalmitra.llm.interface import BaseLLMProvider, LLMResponse
from legalmitra.rag.engine import LegalRAGEngine


@pytest.fixture(scope="module")
def kb():
    k = LegalKnowledgeBase("data/legalmitra_kb.db", must_exist=True)
    yield k
    k.close()


def test_phase24_corpus_scale_and_integrity(kb):
    """Verify Phase 24 corpus expansion figures in SQLite."""
    conn = sqlite3.connect(kb.db_path)
    c = conn.cursor()

    # Sources: 57 total
    c.execute("SELECT COUNT(*) FROM sources")
    sources_cnt = c.fetchone()[0]
    assert sources_cnt >= 57, f"Expected at least 57 sources, found {sources_cnt}"

    # Total chunks: 1495 (1489 active + 6 quarantined scaffold)
    c.execute("SELECT COUNT(*) FROM legal_chunks")
    total_chunks = c.fetchone()[0]
    assert total_chunks >= 1495, f"Expected at least 1495 total chunks, found {total_chunks}"

    c.execute("SELECT COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold = 0")
    active_chunks = c.fetchone()[0]
    assert active_chunks >= 1489, f"Expected at least 1489 active chunks, found {active_chunks}"

    c.execute("SELECT COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold = 1")
    scaffold_chunks = c.fetchone()[0]
    assert scaffold_chunks == 6, f"Expected exactly 6 scaffold chunks, found {scaffold_chunks}"

    # Cases: 14
    c.execute("SELECT COUNT(*) FROM cases")
    cases_cnt = c.fetchone()[0]
    assert cases_cnt >= 14, f"Expected at least 14 cases, found {cases_cnt}"

    # Judicial documents: 7
    c.execute("SELECT COUNT(*) FROM judicial_documents")
    docs_cnt = c.fetchone()[0]
    assert docs_cnt >= 7, f"Expected at least 7 judicial documents, found {docs_cnt}"

    # Hearing events: 6
    c.execute("SELECT COUNT(*) FROM hearing_events")
    events_cnt = c.fetchone()[0]
    assert events_cnt >= 6, f"Expected at least 6 hearing events, found {events_cnt}"

    conn.close()


def test_phase24_central_acts_coverage(kb):
    """Verify authentic provisions for BSA, BNS, POCSO, RTI, MVA are indexed."""
    conn = sqlite3.connect(kb.db_path)
    c = conn.cursor()

    # BSA Sections
    c.execute("SELECT chunk_id FROM legal_chunks WHERE source_id = 'IND-ACT-2023-BSA'")
    bsa_chunks = [r[0] for r in c.fetchall()]
    assert any("SEC:22" in ch or "SEC:23" in ch or "SECTION_22" in ch or "SECTION_24" in ch for ch in bsa_chunks)

    # POCSO Sections
    c.execute("SELECT chunk_id FROM legal_chunks WHERE source_id = 'IND-ACT-2012-POCSO'")
    pocso_chunks = [r[0] for r in c.fetchall()]
    assert any("SECTION_19" in ch or "SECTION_21" in ch for ch in pocso_chunks)

    # RTI Sections
    c.execute("SELECT chunk_id FROM legal_chunks WHERE source_id = 'IND-ACT-2005-RTI'")
    rti_chunks = [r[0] for r in c.fetchall()]
    assert any("SECTION_7" in ch for ch in rti_chunks)

    # MVA Sections
    c.execute("SELECT chunk_id FROM legal_chunks WHERE source_id = 'IND-ACT-1988-MVA'")
    mva_chunks = [r[0] for r in c.fetchall()]
    assert any("SECTION_185" in ch for ch in mva_chunks)

    conn.close()


def test_phase24_landmark_precedents_graph():
    """Verify Phase 24 precedent relationships and Article 141 hierarchy in Knowledge Graph."""
    g = build_national_judicial_knowledge_graph()

    # Precedent nodes
    assert g.get_node("CASE-MANEKA-GANDHI") is not None
    assert g.get_node("CASE-KESAVANANDA") is not None
    assert g.get_node("CASE-DK-BASU") is not None
    assert g.get_node("CASE-LALITA-KUMARI") is not None
    assert g.get_node("CASE-ARNESH-KUMAR") is not None
    assert g.get_node("CASE-SHREYA-SINGHAL") is not None
    assert g.get_node("CASE-SUSHILA-AGGARWAL") is not None
    assert g.get_node("CASE-VIDYA-DROLIA") is not None
    assert g.get_node("CASE-JACOB-MATHEW") is not None
    assert g.get_node("CASE-ENERGY-WATCHDOG") is not None

    # Overruling checks
    is_ovr, reason = g.is_case_overruled("CASE-HIMANGNI")
    assert is_ovr is True
    assert "Vidya Drolia" in reason

    is_ovr_nn, reason_nn = g.is_case_overruled("CASE-NN-GLOBAL")
    assert is_ovr_nn is True
    assert "Arbitration Agreements & Stamp Act" in reason_nn

    # Statutory linkages
    p_art21 = g.get_precedents_for_provision("ART-CONST-21")
    names_art21 = [p.name for p in p_art21]
    assert "Maneka Gandhi v. Union of India" in names_art21
    assert "D.K. Basu v. State of West Bengal" in names_art21

    p_bnss173 = g.get_precedents_for_provision("SEC-BNSS-173")
    assert any("Lalita Kumari" in p.name for p in p_bnss173)


def test_phase24_evaluation_dataset_v3():
    """Verify evaluation dataset v3 manifest integrity and coverage."""
    v3_path = Path("data/14_evaluation/evaluation_cases_v3.json")
    assert v3_path.exists()

    manifest_path = Path("data/14_evaluation/manifest_v3.json")
    assert manifest_path.exists()

    dataset = EvaluationDataset.load_from_json(str(v3_path))
    assert len(dataset.cases) == 36

    # Verify specific Phase 24 benchmark cases
    case_ids = [c.eval_id for c in dataset.cases]
    assert "EVAL-STAT-010" in case_ids  # RTI Life or Liberty
    assert "EVAL-STAT-011" in case_ids  # POCSO Duty to Report
    assert "EVAL-STAT-012" in case_ids  # MVA Section 185
    assert "EVAL-PREC-005" in case_ids  # Jacob Mathew Gross Medical Negligence
    assert "EVAL-PREC-006" in case_ids  # Arnesh Kumar Section 41 Arrest Guidelines
    assert "EVAL-PREC-007" in case_ids  # Vidya Drolia Overruling Himangni
    assert "EVAL-PREC-008" in case_ids  # Sushila Aggarwal Anticipatory Bail
    assert "EVAL-PROC-002" in case_ids  # Maneka Gandhi Procedural Journey
    assert "EVAL-ADVR-003" in case_ids  # Shreya Singhal Section 66A Struck Down
    assert "EVAL-MISS-003" in case_ids  # Nagaland Planning Act Abstention
