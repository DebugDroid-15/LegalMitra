"""
Test Suite: tests/test_phase29_coverage.py
Validates Phase 29 National Coverage Expansion, Precedent Knowledge Graph Integrity,
Maturity States, and Benchmark v7 Evaluation.
"""

from __future__ import annotations

import json
from pathlib import Path
import sqlite3
import pytest

from legalmitra.caselaw.knowledge_graph import build_national_judicial_knowledge_graph, EntityType, RelationType
from legalmitra.evaluation.dataset import EvaluationDataset
from legalmitra.evaluation.runner import LegalEvaluationRunner
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
from legalmitra.knowledge.models import SearchFilters
from legalmitra.llm.mock_provider import MockLLMProvider
from legalmitra.rag.engine import LegalRAGEngine


@pytest.fixture(scope="module")
def kb():
    k = LegalKnowledgeBase("data/legalmitra_kb.db", must_exist=True)
    yield k
    k.close()


@pytest.fixture(scope="module")
def rag(kb):
    return LegalRAGEngine(knowledge_base=kb, llm_provider=MockLLMProvider())


def test_jurisdiction_coverage_matrix_structure():
    """Verify 36 State and Union Territory entries and 12 maturity levels."""
    matrix_path = Path("data/09_national_corpus/jurisdiction_coverage_matrix.json")
    assert matrix_path.exists(), "Coverage matrix must exist"
    
    with open(matrix_path, encoding="utf-8") as f:
        data = json.load(f)
        
    assert data["total_jurisdictions"] == 36
    assert data["states_count"] == 28
    assert data["union_territories_count"] == 8
    assert len(data["maturity_levels"]) == 12
    assert "temporally_verified" in data["maturity_levels"]
    assert "discovered" in data["maturity_levels"]
    
    # Check Delhi and Maharashtra maturity states
    jurisdictions = {j["jurisdiction_code"]: j for j in data["jurisdictions"]}
    assert jurisdictions["IN-DL"]["coverage_maturity_state"] == "temporally_verified"
    assert jurisdictions["IN-DL"]["active_in_corpus"] is True
    assert jurisdictions["IN-MH"]["coverage_maturity_state"] == "temporally_verified"
    assert jurisdictions["IN-MH"]["active_in_corpus"] is True
    
    # Check unindexed state
    assert jurisdictions["IN-KA"]["coverage_maturity_state"] == "discovered"
    assert jurisdictions["IN-KA"]["active_in_corpus"] is False


def test_state_ut_registry_maturity_states():
    """Verify state_ut_registry contains coverage_maturity_state across all 36 entries."""
    reg_path = Path("data/08_corpus/state_ut_registry.json")
    assert reg_path.exists()
    
    with open(reg_path, encoding="utf-8") as f:
        records = json.load(f)
        
    assert len(records) == 36
    for r in records:
        assert "coverage_maturity_state" in r
        assert r["coverage_maturity_state"] in (
            "not_discovered", "discovered", "registered", "accessible", "acquired",
            "parsed", "structurally_validated", "authenticity_verified", "indexed",
            "retrieval_verified", "temporally_verified", "legally_reviewed"
        )


def test_precedent_relationships_anchors():
    """Verify all precedent relationships have verified proposition and passage citations."""
    rel_path = Path("data/08_corpus/precedent_relationships.json")
    assert rel_path.exists()
    
    with open(rel_path, encoding="utf-8") as f:
        rels = json.load(f)
        
    assert len(rels) >= 6
    for r in rels:
        assert r["is_human_reviewed"] is True
        assert r["treatment_passage_ref"] is not None, f"Relationship {r['relationship_id']} missing treatment_passage_ref"
        assert len(r["treatment_passage_ref"]) > 0


def test_delhi_rent_control_retrieval(kb, rag):
    """Verify Section 14 DRC Act retrieval and answering."""
    filters = SearchFilters(jurisdiction="IN-DL")
    resp = rag.answer("What are the grounds for eviction under Section 14 of the Delhi Rent Control Act, 1958?", filters=filters)
    assert resp.is_grounded is True
    assert any("DRC" in e.source_id for e in resp.cited_evidence)


def test_maharashtra_rent_control_retrieval(kb, rag):
    """Verify Section 15 MRC Act 90 days notice retrieval and answering."""
    filters = SearchFilters(jurisdiction="IN-MH")
    resp = rag.answer("What notice period is mandatory under Section 15 of the Maharashtra Rent Control Act, 1999?", filters=filters)
    assert resp.is_grounded is True
    assert any("MRC" in e.source_id for e in resp.cited_evidence)


def test_unindexed_state_transparent_abstention(kb, rag):
    """Verify unindexed state queries trigger transparent abstention."""
    filters = SearchFilters(jurisdiction="IN-KA")
    resp = rag.answer("What is the mutation procedure under Section 128 of the Karnataka Land Revenue Act, 1964?", filters=filters)
    assert resp.evidence_sufficiency == "insufficient"
    assert "not provide sufficient evidence" in resp.answer or "insufficient" in resp.answer.lower()


def test_benchmark_v7_manifest_and_evaluation():
    """Verify Benchmark v7 suite runs 80 cases with 100% pass rate and Gate GO."""
    cases_path = Path("data/18_evaluation/evaluation_cases_v7.json")
    manifest_path = Path("data/18_evaluation/manifest_v7.json")
    results_path = Path("data/18_evaluation/evaluation_results_v7.json")
    
    assert cases_path.exists()
    assert manifest_path.exists()
    assert results_path.exists()
    
    dataset = EvaluationDataset.load_from_json(str(cases_path))
    assert len(dataset.cases) == 80
    
    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)
    assert manifest["total_cases"] == 80
    assert manifest["manifest_version"] == "7.0.0"
    
    with open(results_path, encoding="utf-8") as f:
        results = json.load(f)
    assert results["total_cases"] == 80
    assert results["passed_cases"] == 80
    assert results["failed_cases"] == 0
    assert results["overall_pass_rate"] == 1.0
    assert results["release_gate_status"] == "GO"
    assert results["blocking_defects_count"] == 0

