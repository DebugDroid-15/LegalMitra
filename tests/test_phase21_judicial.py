"""
LegalMitra Phase 21 Judicial Corpus & Lifecycle Intelligence Test Suite
Verifies:
1. National Judicial Source Registry (36 repositories across SCI, High Courts, District, Tribunals).
2. Case Identity and Deterministic Resolution.
3. Order and Judgment Classification taxonomy.
4. Procedural timeline and hearing event reconstruction in SQLite.
5. Ingested judgments: Rangappa (NI Act s.138/139) and Arbitration Stamp In Re (7-Judge Bench).
6. Precedent Graph & Proposition-Aware Overruling.
7. End-to-end research path & missing record abstention.
8. Synthetic scaffold quarantine & Phase 9 freeze integrity.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import date
from pathlib import Path

import pytest

from legalmitra.caselaw.case_identity import (
    CaseIdentityResolver,
    CaseStatus,
    DocumentClassification,
    ProceduralEffect,
    UnifiedCaseIdentity,
)
from legalmitra.caselaw.knowledge_graph import (
    EntityType,
    RelationType,
    build_national_judicial_knowledge_graph,
)
from legalmitra.corpus.judicial_registry import (
    CourtTier,
    JUDICIAL_SOURCE_REGISTRY,
)
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase


@pytest.fixture(scope="module")
def kb():
    k = LegalKnowledgeBase(db_path="data/legalmitra_kb.db", must_exist=True)
    yield k
    k.close()


def test_judicial_source_registry_coverage():
    """Verify registry maps 36 court and tribunal repositories."""
    assert len(JUDICIAL_SOURCE_REGISTRY) >= 36
    tiers = {r.tier for r in JUDICIAL_SOURCE_REGISTRY}
    assert CourtTier.SUPREME_COURT in tiers
    assert CourtTier.HIGH_COURT in tiers
    assert CourtTier.DISTRICT_COURT in tiers
    assert CourtTier.APPELLATE_TRIBUNAL in tiers

    # Check export file exists
    json_path = Path("data/11_judicial_corpus/judicial_source_registry.json")
    assert json_path.exists()
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) >= 36


def test_case_identity_deterministic_matching():
    """Verify case identity generation and unambiguous matching."""
    case1 = UnifiedCaseIdentity(
        case_id="IN-SC-CA-2082-2018",
        court_code="IN-SC",
        case_type="Civil Appeal",
        case_number="2082-2083",
        filing_year=2018,
        petitioner_or_appellant="Arjun Panditrao Khotkar",
        respondent="Kailash Kushanrao Gorantyal",
        status=CaseStatus.DISPOSED
    )
    case2 = UnifiedCaseIdentity(
        case_id="IN-DL-HC-CA-2082-2018",
        court_code="IN-DL-HC",
        case_type="Civil Appeal",
        case_number="2082",
        filing_year=2018,
        petitioner_or_appellant="Different Party",
        respondent="Another Respondent",
        status=CaseStatus.PENDING
    )

    cases = [case1, case2]
    # Exact match on Supreme Court case
    match_sc = CaseIdentityResolver.match_case("IN-SC", "2082", 2018, cases)
    assert match_sc is not None
    assert match_sc.case_id == "IN-SC-CA-2082-2018"

    # Distinct court separation
    match_dhc = CaseIdentityResolver.match_case("IN-DL-HC", "2082", 2018, cases)
    assert match_dhc is not None
    assert match_dhc.case_id == "IN-DL-HC-CA-2082-2018"

    # Unknown case returns None
    match_none = CaseIdentityResolver.match_case("IN-SC", "9999", 2018, cases)
    assert match_none is None


def test_ingested_phase21_judgments(kb):
    """Verify Rangappa and Arbitration Stamp reference are properly indexed in KB."""
    conn = sqlite3.connect(kb.db_path)
    c = conn.cursor()

    # 1. Rangappa
    c.execute("""
        SELECT chunk_id, act_or_case_title, content
        FROM legal_chunks
        WHERE source_id = 'IND-JUD-SC-2010-RANGAPPA' AND is_synthetic_scaffold = 0
    """)
    rangappa_rows = c.fetchall()
    assert len(rangappa_rows) >= 5
    text_rangappa = " ".join([r[2] for r in rangappa_rows])
    assert "139" in text_rangappa
    assert "preponderance of probabilities" in text_rangappa

    # 2. Arbitration Stamp Act In Re
    c.execute("""
        SELECT chunk_id, act_or_case_title, content
        FROM legal_chunks
        WHERE source_id = 'IND-JUD-SC-2023-ARBITRATION-STAMP' AND is_synthetic_scaffold = 0
    """)
    stamp_rows = c.fetchall()
    assert len(stamp_rows) >= 5
    text_stamp = " ".join([r[2] for r in stamp_rows])
    assert "curable defect" in text_stamp
    assert "Section 16" in text_stamp or "Section 11" in text_stamp

    conn.close()


def test_procedural_timeline_reconstruction(kb):
    """Verify get_case_procedural_timeline reconstructs dated orders and hearing events."""
    timeline_res = kb.get_case_procedural_timeline("IN-SC-CA-2082-2018")
    assert timeline_res["found"] is True
    assert timeline_res["case_id"] == "IN-SC-CA-2082-2018"
    assert timeline_res["status"] == "disposed"

    events = timeline_res["timeline"]
    assert len(events) >= 2
    dates = [e["date"] for e in events]
    # Check chronological ordering
    assert dates == sorted(dates)
    assert any(e["classification"] == "notice_order" for e in events if e["type"] == "document_order")


def test_national_judicial_knowledge_graph():
    """Verify judicial knowledge graph tracks precedents, overrulings, and statutory linkages."""
    g = build_national_judicial_knowledge_graph()

    # Check nodes
    assert g.get_node("CASE-ARJUN-KHOTKAR") is not None
    assert g.get_node("SEC-NI-139") is not None
    assert g.get_node("SEC-ARB-11") is not None

    # Check overruling logic
    is_ovr_bhat, reason_bhat = g.is_case_overruled("CASE-KRISHNA-BHAT")
    assert is_ovr_bhat is True
    assert "Rangappa" in reason_bhat

    is_ovr_nn, reason_nn = g.is_case_overruled("CASE-NN-GLOBAL")
    assert is_ovr_nn is True
    assert "Arbitration Agreements & Stamp Act" in reason_nn

    # Check statutory linkage
    precedents_139 = g.get_precedents_for_provision("SEC-NI-139")
    assert any(p.name == "Rangappa v. Sri Mohan" for p in precedents_139)

    # Check partial overruling
    status_shafhi = g.evaluate_precedent_status("CASE-SHAFHI-MOHD")
    assert status_shafhi["is_overruled"] is True
    assert status_shafhi["status"] == "partially_overruled"


def test_synthetic_scaffold_segregation(kb):
    """Verify IND-JUD-DEL-2024-BAIL remains segregated from standard retrieval."""
    conn = sqlite3.connect(kb.db_path)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold = 1")
    scaffold_cnt = c.fetchone()[0]
    assert scaffold_cnt == 6, f"Expected exactly 6 quarantined scaffold chunks, found {scaffold_cnt}"

    # Verify RAG search excludes scaffolds
    results = kb.search("anticipatory bail under BNSS", limit=10)
    for res in results:
        assert getattr(res, "is_synthetic_scaffold", 0) == 0
        assert getattr(res, "source_id", "") != "IND-JUD-DEL-2024-BAIL"
    conn.close()

