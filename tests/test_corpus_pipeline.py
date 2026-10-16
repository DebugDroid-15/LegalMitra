"""
LegalMitra Phase 14 Corpus Pipeline & Infrastructure Test Suite
Tests taxonomy engine, inventory management, official source catalog,
temporal law engine, precedent hierarchy, and corpus ingestion pipeline.
"""

import tempfile
from pathlib import Path
import pytest

from legalmitra.caselaw.precedent import (
    BenchStrength,
    CaseLawMetadata,
    PrecedentHierarchyManager,
    PrecedentRelationship,
    PrecedentTreatment,
    build_default_precedent_manager,
)
from legalmitra.corpus.discovery import (
    AccessMethod,
    SourceDiscoveryManager,
    SourceRepository,
    VerificationTier,
    build_default_source_catalog,
)
from legalmitra.corpus.inventory import (
    CorpusInventoryItem,
    CorpusInventoryManager,
    CorpusStatus,
    DocumentClass,
)
from legalmitra.corpus.taxonomy import (
    LegalTaxonomyManager,
    TaxonomyNode,
    build_default_indian_legal_taxonomy,
)
from legalmitra.ingestion.corpus_ingestor import CorpusIngestionPipeline, IngestionBatchResult
from legalmitra.temporal.engine import (
    ProvisionTemporalVersion,
    StatuteLifecycle,
    TemporalLawEngine,
    TemporalStatus,
    build_default_temporal_engine,
)


# =============================================================================
# TAXONOMY TESTS (Phase 14B)
# =============================================================================

def test_taxonomy_tree_structure_and_domains():
    mgr = build_default_indian_legal_taxonomy()
    nodes = mgr.list_nodes()
    root_nodes = mgr.get_root_nodes()

    assert len(root_nodes) == 8, f"Expected 8 root domains, got {len(root_nodes)}"
    assert len(nodes) >= 30, f"Expected at least 30 nodes, got {len(nodes)}"

    const_node = mgr.get_node("TAX-CONST")
    assert const_node is not None
    assert const_node.jurisdiction_scope == "CENTRAL"

    crim_children = mgr.get_children("TAX-CRIM")
    assert len(crim_children) == 4
    child_codes = [c.code for c in crim_children]
    assert "TAX-CRIM-SUB" in child_codes
    assert "TAX-CRIM-PROC" in child_codes
    assert "TAX-CRIM-EVID" in child_codes


def test_taxonomy_classification_and_search():
    mgr = build_default_indian_legal_taxonomy()

    # Search keyword
    res = mgr.search_by_keyword("privacy")
    assert len(res) > 0
    codes = [r.code for r in res]
    assert any("CONST" in c or "TECH" in c for c in codes)

    # Text classification
    text = "The certificate under section 63 for admissibility of electronic record in evidence"
    matched_codes = mgr.classify_text(text)
    assert "TAX-CRIM-EVID" in matched_codes


def test_taxonomy_export_and_load(tmp_path: Path):
    mgr = build_default_indian_legal_taxonomy()
    json_path = tmp_path / "taxonomy.json"
    mgr.export_json(json_path)
    assert json_path.exists()

    loaded = LegalTaxonomyManager.load_json(json_path)
    assert len(loaded.list_nodes()) == len(mgr.list_nodes())
    assert loaded.get_node("TAX-CIVIL-LIMIT") is not None


# =============================================================================
# INVENTORY TESTS (Phase 14A)
# =============================================================================

def test_inventory_manager_operations(tmp_path: Path):
    mgr = CorpusInventoryManager()
    item = CorpusInventoryItem(
        document_id="IND-TEST-001",
        official_title="Test Statute Act, 2026",
        jurisdiction="IN",
        document_class=DocumentClass.ACT,
        legal_domain="Civil Justice",
        corpus_status=CorpusStatus.CURRENT,
    )
    mgr.add_item(item)

    assert mgr.get_item("IND-TEST-001") is not None
    assert len(mgr.filter_by_status(CorpusStatus.CURRENT)) == 1
    assert len(mgr.filter_by_status(CorpusStatus.HISTORICAL)) == 0

    # JSON export / load
    json_path = tmp_path / "inv.json"
    mgr.export_json(json_path)
    loaded = CorpusInventoryManager.load_json(json_path)
    assert loaded.get_item("IND-TEST-001").official_title == "Test Statute Act, 2026"

    # CSV export
    csv_path = tmp_path / "inv.csv"
    mgr.export_csv(csv_path)
    assert csv_path.exists()
    assert "IND-TEST-001" in csv_path.read_text(encoding="utf-8")


# =============================================================================
# SOURCE DISCOVERY CATALOG TESTS (Phase 14C)
# =============================================================================

def test_source_discovery_catalog():
    mgr = build_default_source_catalog()
    repos = mgr.list_repos()

    assert len(repos) >= 10
    india_code = mgr.get_repo("REPO-INDIA-CODE")
    assert india_code is not None
    assert india_code.verification_tier == VerificationTier.PRIMARY_OFFICIAL
    assert india_code.rate_limit_per_minute == 30

    primary_repos = mgr.filter_by_tier(VerificationTier.PRIMARY_OFFICIAL)
    assert len(primary_repos) >= 4  # India Code, e-Gazette, SCI Judgments, SCI Rules


# =============================================================================
# TEMPORAL LAW ENGINE TESTS (Phase 14D)
# =============================================================================

def test_temporal_criminal_law_transition():
    engine = build_default_temporal_engine()

    # Pre-July 1, 2024 offence
    pre_result = engine.resolve_criminal_law_regime("2024-05-15")
    assert "Indian Penal Code, 1860" in pre_result["substantive_law"]
    assert "Article 20(1)" in pre_result["substantive_rationale"]

    # Post-July 1, 2024 offence
    post_result = engine.resolve_criminal_law_regime("2024-07-15")
    assert "Bharatiya Nyaya Sanhita, 2023" in post_result["substantive_law"]

    # Pending proceeding instituted before 1 July 2024 saved under BNSS s.531(2)(a)
    pending_proc = engine.resolve_criminal_law_regime("2024-03-01", "2024-04-10")
    assert "Code of Criminal Procedure, 1973" in pending_proc["procedural_law"]
    assert pending_proc["bnss_s531_savings_applied"] is True


def test_temporal_data_protection_regime():
    engine = build_default_temporal_engine()
    res = engine.resolve_data_protection_regime("2026-05-01")
    assert "Operative in law" in res["it_act_s43a_status"]
    assert "uncommenced pending s.1(2) notification" in res["dpdp_status"]


def test_temporal_provision_version_lookup():
    engine = build_default_temporal_engine()

    # IEA Section 65B on 2020-01-01 (operative)
    v_iea = engine.query_provision_at_date("IEA-SEC-65B", "2020-01-01")
    assert v_iea is not None
    assert v_iea.section_number == "65B"

    # IEA Section 65B on 2025-01-01 (repealed)
    v_iea_post = engine.query_provision_at_date("IEA-SEC-65B", "2025-01-01")
    assert v_iea_post is None

    # BSA Section 63 on 2025-01-01 (operative)
    v_bsa = engine.query_provision_at_date("BSA-SEC-63", "2025-01-01")
    assert v_bsa is not None
    assert v_bsa.section_number == "63"


# =============================================================================
# CASE LAW & PRECEDENT HIERARCHY TESTS (Phase 14F)
# =============================================================================

def test_precedent_binding_authority_evaluation():
    mgr = build_default_precedent_manager()

    # Puttaswamy is binding on Delhi High Court under Art 141
    eval_puttaswamy = mgr.evaluate_binding_authority("IND-JUD-SC-2017-PUTTASWAMY", "High Court of Delhi")
    assert eval_puttaswamy["is_binding"] is True
    assert eval_puttaswamy["authority_status"] == "ABSOLUTELY_BINDING"
    assert "Article 141" in eval_puttaswamy["rationale"]

    # ADM Jabalpur is overruled
    eval_adm = mgr.evaluate_binding_authority("IND-JUD-SC-1976-ADMJABALPUR", "High Court of Delhi")
    assert eval_adm["is_binding"] is False
    assert eval_adm["authority_status"] == "OVERRULED"
    assert eval_adm["overruled_by"] == "IND-JUD-SC-2017-PUTTASWAMY"

    # Suresh Koushal is overruled by Navtej Johar
    eval_koushal = mgr.evaluate_binding_authority("IND-JUD-SC-2014-KOUSHAL", "High Court of Bombay")
    assert eval_koushal["is_binding"] is False
    assert eval_koushal["overruled_by"] == "IND-JUD-SC-2018-NAVTEJ"


# =============================================================================
# CORPUS INGESTION PIPELINE TESTS (Phase 14E)
# =============================================================================

def test_corpus_ingestion_idempotency_and_quarantine():
    pipeline = CorpusIngestionPipeline()

    # Quarantined document check
    res = pipeline.execute_batch(
        batch_name="TEST_BATCH",
        file_paths=["data/02_normalized/IND-JUD-DEL-2024-BAIL.json"],
        force_reindex=False,
    )
    assert res.quarantined == 1
    assert res.successfully_indexed == 0

    # Idempotent skip check on already indexed normalized file
    res2 = pipeline.execute_batch(
        batch_name="TEST_BATCH_IDEMPOTENT",
        file_paths=["data/02_normalized/IND-STAT-BSA-2023-SEC61.json"],
        force_reindex=False,
    )
    assert res2.skipped_existing == 1
    assert res2.successfully_indexed == 0
    assert res2.failed == 0

