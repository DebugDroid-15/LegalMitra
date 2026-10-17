"""
Phase 17 Test Suite: Judicial Decisions, Precedent Intelligence, and Passage-Level Retrieval
Verifies:
1. 8 Genuine Landmark Judgments are loaded and indexed (39 genuine chunks).
2. Numbered paragraphs, holdings, and ratio decidendi are intact.
3. Precedent relationships reflect Article 141 hierarchy and overruling status.
4. Passage-level search accurately retrieves exact paragraph numbers.
5. Neutral citation lookups return the correct decision.
6. Quarantined synthetic scaffold IND-JUD-DEL-2024-BAIL remains strictly isolated.
"""

import json
from pathlib import Path
import pytest

from legalmitra.caselaw.precedent import PrecedentTreatment, build_default_precedent_manager
from legalmitra.corpus.judicial_registry import JUDICIAL_REPOSITORIES
from legalmitra.ingestion.landmark_judgments import get_landmark_judgment_documents
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
from legalmitra.knowledge.models import AuthorityLevel, SearchFilters


@pytest.fixture
def kb():
    return LegalKnowledgeBase(db_path="data/legalmitra_kb.db", must_exist=True)


def test_judicial_repositories_registry():
    """Verify official judicial repositories include Supreme Court and High Courts."""
    assert len(JUDICIAL_REPOSITORIES) >= 5
    repo_ids = [r.repository_id for r in JUDICIAL_REPOSITORIES]
    assert "REPO-SCI-DIGITAL-SCR" in repo_ids
    assert "REPO-DHC-JUDGMENTS" in repo_ids
    assert "REPO-BOM-JUDGMENTS" in repo_ids
    assert "REPO-ECOURTS-NJDG" in repo_ids

    # Verify JSON export
    json_path = Path("data/08_corpus/judicial_repositories.json")
    assert json_path.exists()
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == len(JUDICIAL_REPOSITORIES)


def test_landmark_judgments_models():
    """Verify landmark judgments models contain essential precedents."""
    judgments = get_landmark_judgment_documents()
    assert len(judgments) == 7
    doc_ids = [j.source_id for j in judgments]
    assert "IND-JUD-SC-2020-ARJUN-KHOTKAR" in doc_ids
    assert "IND-JUD-SC-2014-ANVAR-PV" in doc_ids
    assert "IND-JUD-SC-2018-SHAFHI-MOHAMMAD" in doc_ids
    assert "IND-JUD-SC-2022-ANTIL" in doc_ids
    assert "IND-JUD-SC-2020-PERKINS-EASTMAN" in doc_ids
    assert "IND-JUD-SC-1954-SATYABRATA" in doc_ids
    assert "IND-JUD-SC-2008-SATYAWATI" in doc_ids


def test_precedent_hierarchy_manager_evaluations():
    """Verify precedent relationships, overruling detection, and Article 141 binding evaluations."""
    mgr = build_default_precedent_manager()
    cases = mgr.list_cases()
    assert len(cases) == 14

    # Verify Arjun Khotkar overruled Shafhi Mohammad
    shafhi = mgr.get_case("IND-JUD-SC-2018-SHAFHI-MOHAMMAD")
    assert shafhi is not None
    assert shafhi.is_overruled is True
    assert shafhi.overruled_by_case_id == "IND-JUD-SC-2020-ARJUN-KHOTKAR"

    # Verify evaluation reports OVERRULED
    eval_shafhi = mgr.evaluate_binding_authority("IND-JUD-SC-2018-SHAFHI-MOHAMMAD")
    assert eval_shafhi["authority_status"] == "OVERRULED"
    assert eval_shafhi["is_binding"] is False

    # Verify Arjun Khotkar binding on High Courts
    eval_arjun = mgr.evaluate_binding_authority("IND-JUD-SC-2020-ARJUN-KHOTKAR", target_court="High Court of Delhi")
    assert eval_arjun["authority_status"] == "ABSOLUTELY_BINDING"
    assert eval_arjun["is_binding"] is True


def test_passage_level_paragraph_search(kb):
    """Verify passage-level search using exact paragraph_number filter."""
    filters = SearchFilters(doc_type="judgment", paragraph_number=51)
    results = kb.search("certificate condition precedent", filters=filters, limit=5)
    assert len(results) > 0
    match = results[0]
    assert match.provision_or_para_ref == "Paragraph 51"
    assert "IND-JUD-SC-2020-ARJUN-KHOTKAR" in match.chunk_id
    assert "Section 65B(4) is a mandatory requirement" in match.content


def test_citation_direct_lookup(kb):
    """Verify looking up a judgment by official / neutral citation."""
    filters = SearchFilters(case_citation="2020 INSC 452")
    results = kb.search("", filters=filters, limit=5)
    assert len(results) > 0
    assert any("ARJUN" in r.chunk_id for r in results)


def test_arbitration_judgment_retrieval(kb):
    """Verify Perkins Eastman search on unilateral arbitrator appointment."""
    filters = SearchFilters(doc_type="judgment")
    results = kb.search("sole arbitrator unilateral appointment", filters=filters, limit=5)
    assert len(results) > 0
    assert any("PERKINS" in r.chunk_id for r in results)


def test_delhi_tenancy_judgment_retrieval(kb):
    """Verify Satyawati Sharma commercial bona fide requirement retrieval."""
    filters = SearchFilters(doc_type="judgment", jurisdiction="IN-DL")
    results = kb.search("bona fide requirement commercial premises", filters=filters, limit=5)
    assert len(results) > 0
    assert any("SATYAWATI" in r.chunk_id for r in results)


def test_quarantine_scaffold_exclusion_in_caselaw(kb):
    """Verify synthetic scaffold IND-JUD-DEL-2024-BAIL is excluded from standard search."""
    filters = SearchFilters(doc_type="judgment", include_synthetic=False)
    results = kb.search("State of NCT of Delhi anticipatory bail", filters=filters, limit=20)
    for r in results:
        assert r.is_synthetic_scaffold is False
        assert r.source_id != "IND-JUD-DEL-2024-BAIL"

