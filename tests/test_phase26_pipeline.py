"""
Test Suite: tests/test_phase26_pipeline.py
Validates Phase 26 Human Legal Review Operations, First-Class Statutory Structures,
High Court Precedent Ingestion, and Benchmark v5 Integrity.
"""

from __future__ import annotations

import json
from pathlib import Path
import sqlite3
import pytest

from legalmitra.caselaw.knowledge_graph import build_national_judicial_knowledge_graph, EntityType, RelationType
from legalmitra.evaluation.dataset import EvaluationDataset
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
from legalmitra.review.workflow import (
    AdvocateCredentials,
    AdvocateReviewWorkflow,
    ReviewAction,
    ReviewDecision,
    ReviewStatus,
    ReviewSubmission,
    UserRole,
    ROLE_PERMISSIONS,
    VALID_STATE_TRANSITIONS,
)


@pytest.fixture(scope="module")
def kb():
    k = LegalKnowledgeBase("data/legalmitra_kb.db", must_exist=True)
    yield k
    k.close()


@pytest.fixture
def workflow(tmp_path):
    audit_file = tmp_path / "audit.jsonl"
    return AdvocateReviewWorkflow(audit_log_path=audit_file)


@pytest.fixture
def valid_credentials():
    return AdvocateCredentials(
        advocate_name="Adv. Rajesh Kumar",
        bar_council_id="D/1945/2012",
        state_bar_council="Bar Council of Delhi",
        enrollment_year=2012,
        role=UserRole.ADVOCATE_REVIEWER,
    )


def test_phase26_advocate_review_workflow_permissions():
    """Verify role permissions and valid transitions including ABSTAINED."""
    # Ensure ABSTAINED is present in ReviewStatus and ReviewDecision
    assert ReviewStatus.ABSTAINED == "abstained"
    assert ReviewDecision.ABSTAINED == "abstained"
    assert ReviewAction.ABSTAIN == "abstain"

    # Verify advocate permissions
    assert UserRole.ADVOCATE_REVIEWER in ROLE_PERMISSIONS[ReviewAction.ABSTAIN]
    assert UserRole.SENIOR_ADVOCATE in ROLE_PERMISSIONS[ReviewAction.ABSTAIN]

    # Verify transitions
    assert ReviewStatus.ABSTAINED in VALID_STATE_TRANSITIONS[ReviewStatus.UNDER_REVIEW]


def test_phase26_review_submission_abstention(workflow, valid_credentials):
    """Verify advocate abstention requires valid credentials and rationale."""
    # Abstention without credentials should fail
    ok, errs = workflow.validate_transition(
        ReviewStatus.UNDER_REVIEW, ReviewStatus.ABSTAINED, credentials=None
    )
    assert ok is False
    assert any("Advocate credentials required" in e for e in errs)

    # Valid abstention transition with credentials
    ok, errs = workflow.validate_transition(
        ReviewStatus.UNDER_REVIEW, ReviewStatus.ABSTAINED, credentials=valid_credentials
    )
    assert ok is True

    # Process abstention submission
    sub = ReviewSubmission(
        example_id="PILOT-001",
        target_status=ReviewStatus.ABSTAINED,
        reviewer=valid_credentials,
        rationale="Conflict of interest: previously advised respondent entity.",
        conflict_of_interest_declared=True,
    )
    res = workflow.process_review_submission(
        current_status=ReviewStatus.UNDER_REVIEW,
        submission=sub,
        dry_run=True,
    )
    assert res["success"] is True
    assert res["new_status"] == ReviewStatus.ABSTAINED.value


def test_phase26_database_counts(kb):
    """Verify updated database census after Delhi High Court ingestion."""
    conn = sqlite3.connect(kb.db_path)
    c = conn.cursor()

    # Sources: 59
    c.execute("SELECT COUNT(*) FROM sources")
    assert c.fetchone()[0] >= 59

    # Total chunks: 1503
    c.execute("SELECT COUNT(*) FROM legal_chunks")
    assert c.fetchone()[0] >= 1503

    # Active chunks: 1497
    c.execute("SELECT COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold = 0")
    assert c.fetchone()[0] >= 1497

    # Scaffold chunks: exactly 6
    c.execute("SELECT COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold = 1")
    assert c.fetchone()[0] == 6

    # Cases: 16
    c.execute("SELECT COUNT(*) FROM cases")
    assert c.fetchone()[0] >= 16

    # Judicial documents: 9
    c.execute("SELECT COUNT(*) FROM judicial_documents")
    assert c.fetchone()[0] >= 9

    # Hearing events: 8
    c.execute("SELECT COUNT(*) FROM hearing_events")
    assert c.fetchone()[0] >= 8

    conn.close()


def test_phase26_delhi_high_court_entities(kb):
    """Verify Christian Louboutin and Tata Sons cases exist with proper relational links."""
    conn = sqlite3.connect(kb.db_path)
    c = conn.cursor()

    # Check Christian Louboutin
    c.execute("SELECT case_number, court_code, neutral_citation FROM cases WHERE case_id = 'IN-DL-HC-CS-COMM-344-2018'")
    row = c.fetchone()
    assert row is not None
    assert row[0] == "344"
    assert row[1] == "IN-DL-HC"
    assert row[2] == "2018:DHC:7175"

    # Check Louboutin judicial document
    c.execute("SELECT classification, procedural_effect FROM judicial_documents WHERE case_id = 'IN-DL-HC-CS-COMM-344-2018'")
    doc = c.fetchone()
    assert doc is not None
    assert doc[0] == "notice_order"

    # Check Louboutin hearing event
    c.execute("SELECT hearing_type, procedural_outcome FROM hearing_events WHERE case_id = 'IN-DL-HC-CS-COMM-344-2018'")
    hear = c.fetchone()
    assert hear is not None

    # Check Tata Greenpeace
    c.execute("SELECT case_number, court_code, neutral_citation FROM cases WHERE case_id = 'IN-DL-HC-CS-OS-1407-2010'")
    row_tata = c.fetchone()
    assert row_tata is not None
    assert row_tata[0] == "1407"
    assert row_tata[1] == "IN-DL-HC"
    assert row_tata[2] == "2011:DHC:452"

    conn.close()


def test_phase26_knowledge_graph_high_court():
    """Verify High Court case nodes and interpretation edges in knowledge graph."""
    g = build_national_judicial_knowledge_graph()

    # Nodes exist
    assert g.get_node("CASE-DHC-LOUBOUTIN") is not None
    assert g.get_node("CASE-DHC-TATA-GREENPEACE") is not None
    assert g.get_node("SEC-IT-79") is not None

    # Edges exist
    edges = g.get_outgoing_edges("CASE-DHC-LOUBOUTIN")
    targets = [e.target_id for e in edges if e.relation == RelationType.INTERPRETS]
    assert "SEC-IT-79" in targets

    tata_edges = g.get_outgoing_edges("CASE-DHC-TATA-GREENPEACE")
    tata_targets = [e.target_id for e in tata_edges if e.relation == RelationType.INTERPRETS]
    assert "ART-CONST-19" in tata_targets


def test_phase26_benchmark_v5_manifest():
    """Verify evaluation dataset v5 and manifest v5 integrity."""
    cases_path = Path("data/16_evaluation/evaluation_cases_v5.json")
    manifest_path = Path("data/16_evaluation/manifest_v5.json")
    results_path = Path("data/16_evaluation/evaluation_results_v5.json")

    assert cases_path.exists()
    assert manifest_path.exists()
    assert results_path.exists()

    dataset = EvaluationDataset.load_from_json(str(cases_path))
    assert len(dataset.cases) == 56

    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)
    assert manifest["total_cases"] == 56
    assert manifest["manifest_version"] == "5.0.0"

    # Verify High Court evaluation cases present
    case_ids = [c.eval_id for c in dataset.cases]
    assert "EVAL-P26-DHC-001" in case_ids
    assert "EVAL-P26-DHC-002" in case_ids
    assert "EVAL-P26-STAT-001" in case_ids
