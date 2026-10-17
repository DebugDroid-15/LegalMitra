"""
Phase 16 Test Suite: Scale, Delegated Rules, State Law, and Jurisdictional Retrieval
Verifies:
1. 8 Central Acts have expanded provisions (126 total sections).
2. Subordinate rules and commencement notifications are accurately indexed.
3. State & UT registry covers all 36 jurisdictions.
4. Delhi and Maharashtra state legislation are indexed and retrievable.
5. Jurisdictional isolation and doc_type filters work properly.
6. Quarantined synthetic scaffolds remain strictly isolated.
"""

import json
from pathlib import Path
import pytest

from legalmitra.corpus.state_registry import STATE_UT_REGISTRY
from legalmitra.corpus.delegated import get_delegated_instruments
from legalmitra.ingestion.central_acts import list_central_act_documents
from legalmitra.ingestion.state_acts import get_state_statute_documents
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
from legalmitra.knowledge.models import AuthorityLevel, SearchFilters


@pytest.fixture
def kb():
    return LegalKnowledgeBase(db_path="data/legalmitra_kb.db", must_exist=True)


def test_central_acts_provision_scale():
    """Verify all 8 Central Acts are expanded with >= 120 total sections."""
    acts = list_central_act_documents()
    assert len(acts) == 8
    total_sections = sum(len(a.sections) for a in acts)
    assert total_sections >= 120, f"Expected at least 120 sections across central acts, got {total_sections}"


def test_delegated_instruments_scale():
    """Verify delegated instruments contain 8 subordinate documents with valid text."""
    instruments = get_delegated_instruments()
    assert len(instruments) == 8
    rule_ids = [doc.source_id for doc in instruments]
    assert "IND-RULE-IT-SPDI-2011" in rule_ids
    assert "IND-RULE-IT-INTERMEDIARY-2021" in rule_ids
    assert "IND-RULE-CPA-ECOMMERCE-2020" in rule_ids
    assert "IND-NOTIF-COMMENCE-BNSS-2024" in rule_ids


def test_state_ut_registry_completeness():
    """Verify registry covers 28 States and 8 Union Territories."""
    assert len(STATE_UT_REGISTRY) == 36
    states = [r for r in STATE_UT_REGISTRY if r.category == "State"]
    uts = [r for r in STATE_UT_REGISTRY if r.category == "Union Territory"]
    assert len(states) == 28
    assert len(uts) == 8

    # Verify JSON export exists
    json_path = Path("data/08_corpus/state_ut_registry.json")
    assert json_path.exists()
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 36


def test_state_statute_documents():
    """Verify Delhi and Maharashtra state legislation models."""
    state_docs = get_state_statute_documents()
    assert len(state_docs) == 4
    doc_ids = [d.source_id for d in state_docs]
    assert "IND-DL-STAT-DRC-1958" in doc_ids
    assert "IND-DL-STAT-DPA-1978" in doc_ids
    assert "IND-MH-STAT-MRC-1999" in doc_ids
    assert "IND-MH-STAT-MPA-1951" in doc_ids


def test_jurisdictional_search_delhi_isolation(kb):
    """Verify Delhi rent control search only returns Delhi statutes."""
    filters = SearchFilters(jurisdiction="IN-DL")
    results = kb.search("rent control eviction bona fide requirement", filters=filters, limit=5)
    assert len(results) > 0
    for r in results:
        assert r.jurisdiction == "IN-DL"
        assert "Maharashtra" not in r.act_or_case_title


def test_jurisdictional_search_maharashtra_isolation(kb):
    """Verify Maharashtra rent control search only returns Maharashtra statutes."""
    filters = SearchFilters(jurisdiction="IN-MH")
    results = kb.search("rent control eviction licensee standard rent", filters=filters, limit=5)
    assert len(results) > 0
    for r in results:
        assert r.jurisdiction == "IN-MH"
        assert "Delhi" not in r.act_or_case_title


def test_doc_type_rules_regulation_filter(kb):
    """Verify filtering by doc_type='rules_regulation' returns subordinate rules."""
    filters = SearchFilters(doc_type="rules_regulation")
    results = kb.search("sensitive personal data password biometrics", filters=filters, limit=5)
    assert len(results) > 0
    for r in results:
        assert r.doc_type == "rules_regulation"
        assert "Rules" in r.act_or_case_title


def test_doc_type_notification_filter(kb):
    """Verify filtering by doc_type='notification' returns commencement notifications."""
    filters = SearchFilters(doc_type="notification")
    results = kb.search("Bharatiya Nagarik Suraksha Sanhita commencement", filters=filters, limit=5)
    assert len(results) > 0
    for r in results:
        assert r.doc_type == "notification"
        assert "Notification" in r.act_or_case_title


def test_quarantined_scaffold_exclusion(kb):
    """Verify synthetic scaffold IND-JUD-DEL-2024-BAIL is excluded by default."""
    results = kb.search("bail NDPS Act", filters=SearchFilters(include_synthetic=False), limit=20)
    for r in results:
        assert r.is_synthetic_scaffold is False
        assert r.source_id != "IND-JUD-DEL-2024-BAIL"

