"""
LegalMitra Phase 15 National Legal Corpus Expansion Scale Test Suite
Validates:
1. Acquisition checkpointing and source verification.
2. Central Acts structural fidelity (Pydantic schema, subsections, provisos, explanations).
3. Amendment relationships and instrument registry.
4. Temporal law transitions (SRA 2018, Arbitration 2015, CPA 2019, BNS 2023).
5. Knowledge Base indexing and retrieval of Central Acts with quarantine safety.
"""

from datetime import date
from pathlib import Path
import json
import pytest

from legalmitra.corpus.amendments import (
    AmendmentAction,
    AmendmentHistoryManager,
    AmendmentInstrument,
    AmendmentRelationship,
    build_default_amendment_manager,
)
from legalmitra.ingestion.acquisition import LegislationAcquisitionManager
from legalmitra.ingestion.central_acts import (
    get_arbitration_document,
    get_bns_document,
    get_constitution_document,
    get_contract_document,
    get_cpa_document,
    get_cpc_document,
    get_limitation_document,
    get_sra_document,
    list_central_act_documents,
)
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
from legalmitra.knowledge.models import SearchFilters
from legalmitra.schemas.statute import StatuteDocument
from legalmitra.temporal.engine import build_default_temporal_engine


# =============================================================================
# 1. ACQUISITION PIPELINE TESTS
# =============================================================================

def test_acquisition_checkpoint_operations(tmp_path: Path):
    checkpoint_file = tmp_path / "checkpoint.json"
    mgr = LegislationAcquisitionManager(storage_dir=tmp_path / "raw", checkpoint_file=checkpoint_file)

    # Initial empty checkpoint
    assert mgr.get_completed_count() == 0
    assert not mgr.is_acquired("IND-TEST-001")

    # Record acquisition
    mgr.record_acquisition(
        source_id="IND-TEST-001",
        official_title="Test Act, 2026",
        source_url="https://indiacode.gov.in/test",
        file_path="raw/test.pdf",
        sha256="abc1234567890",
        byte_size=1024,
    )

    assert mgr.is_acquired("IND-TEST-001")
    assert mgr.get_completed_count() == 1

    # Reload from disk
    mgr2 = LegislationAcquisitionManager(storage_dir=tmp_path / "raw", checkpoint_file=checkpoint_file)
    assert mgr2.is_acquired("IND-TEST-001")
    record = mgr2.get_record("IND-TEST-001")
    assert record["official_title"] == "Test Act, 2026"
    assert record["checksum"] == "abc1234567890"



# =============================================================================
# 2. CENTRAL ACTS STRUCTURAL FIDELITY TESTS
# =============================================================================

def test_central_acts_document_generation():
    acts = list_central_act_documents()
    assert len(acts) == 8

    expected_ids = {
        "IND-CONST-1950",
        "IND-STAT-BNS-2023",
        "IND-STAT-CPC-1908",
        "IND-STAT-LIMIT-1963",
        "IND-STAT-ICA-1872",
        "IND-STAT-SRA-1963",
        "IND-STAT-ARB-1996",
        "IND-STAT-CPA-2019",
    }
    actual_ids = {act.source_id for act in acts}
    assert actual_ids == expected_ids

    # Validate each document against Pydantic schema
    for act in acts:
        assert isinstance(act, StatuteDocument)
        assert act.source_id.startswith("IND-")
        assert len(act.act_title) > 0
        assert len(act.sections) > 0
        for sec in act.sections:
            assert sec.section_id.startswith(act.source_id)
            assert sec.source_id == act.source_id
            assert len(sec.section_number) > 0
            assert len(sec.section_title) > 0
            assert len(sec.full_verbatim_text) > 0


def test_constitution_structural_elements():
    const = get_constitution_document()
    assert const.source_id == "IND-CONST-1950"
    assert len(const.sections) >= 10

    sec_numbers = [s.section_number for s in const.sections]
    assert "Preamble" in sec_numbers
    assert "Article 14" in sec_numbers
    assert "Article 19" in sec_numbers
    assert "Article 21" in sec_numbers
    assert "Article 21A" in sec_numbers
    assert "Article 32" in sec_numbers
    assert "Article 226" in sec_numbers
    assert "Article 330A" in sec_numbers

    # Verify Article 19 has sub-clauses
    art19 = next(s for s in const.sections if s.section_number == "Article 19")
    assert len(art19.subsections) >= 2


def test_specific_relief_act_amendment_provisions():
    sra = get_sra_document()
    assert sra.source_id == "IND-STAT-SRA-1963"
    sec10 = next(s for s in sra.sections if s.section_number == "10")
    assert "shall be enforced" in sec10.full_verbatim_text

    sec20a = next(s for s in sra.sections if s.section_number == "20A")
    assert "infrastructure project" in sec20a.section_title.lower()
    assert len(sec20a.subsections) >= 1



# =============================================================================
# 3. AMENDMENT HISTORY AND RELATIONSHIPS TESTS
# =============================================================================

def test_amendment_manager_operations(tmp_path: Path):
    mgr = build_default_amendment_manager()
    instruments = mgr.list_instruments()
    relationships = mgr.list_relationships()

    assert len(instruments) == 6
    assert len(relationships) == 9

    # SRA 2018 amendment checks
    sra_rels = mgr.get_relationships_for_act("IND-STAT-SRA-1963")
    assert len(sra_rels) == 2
    actions = {r.action for r in sra_rels}
    assert actions == {AmendmentAction.SUBSTITUTION, AmendmentAction.INSERTION}

    # Arbitration 2015 checks
    arb_rels = mgr.get_relationships_for_act("IND-STAT-ARB-1996")
    assert len(arb_rels) == 2
    provisions = {r.target_provision for r in arb_rels}
    assert provisions == {"Section 34", "Section 29A"}

    # Export / reload
    json_path = tmp_path / "amendments.json"
    mgr.export_json(json_path)
    loaded = AmendmentHistoryManager.load_json(json_path)
    assert len(loaded.list_instruments()) == 6
    assert len(loaded.list_relationships()) == 9


# =============================================================================
# 4. TEMPORAL LAW ENGINE EXTENSIONS TESTS
# =============================================================================

def test_temporal_specific_relief_transition():
    engine = build_default_temporal_engine()

    # Pre-2018 contract
    pre = engine.resolve_specific_relief_regime("2017-06-15")
    assert "Pre-2018 Amendment" in pre["regime"]
    assert "Discretionary" in pre["specific_performance_character"]
    assert pre["infrastructure_bar_active"] is False

    # Post-2018 contract
    post = engine.resolve_specific_relief_regime("2021-01-10")
    assert "Post-2018 Amendment" in post["regime"]
    assert "Mandatory" in post["specific_performance_character"]
    assert post["infrastructure_bar_active"] is True


def test_temporal_arbitration_transition():
    engine = build_default_temporal_engine()

    # Pre-2015 arbitration
    pre = engine.resolve_arbitration_regime("2014-08-01")
    assert "Pre-2015" in pre["regime"]
    assert pre["s29a_timeline_mandate"] is False
    assert pre["merits_review_expressly_barred"] is False

    # Post-2015 arbitration
    post = engine.resolve_arbitration_regime("2017-02-15")
    assert "Post-2015" in post["regime"]
    assert post["s29a_timeline_mandate"] is True
    assert post["merits_review_expressly_barred"] is True


def test_temporal_consumer_protection_transition():
    engine = build_default_temporal_engine()

    # Pre-2020 cause of action
    pre = engine.resolve_consumer_regime("2019-11-20")
    assert "1986" in pre["regime"]
    assert pre["repealed"] is True
    assert pre["product_liability_statutory_claim"] is False

    # Post-2020 cause of action
    post = engine.resolve_consumer_regime("2023-04-12")
    assert "2019" in post["regime"]
    assert post["repealed"] is False
    assert post["product_liability_statutory_claim"] is True
    assert post["central_regulator_ccpa"] is True


def test_temporal_provision_versioning_sra_arb_const():
    engine = build_default_temporal_engine()

    # SRA Sec 10: pre-2018 version
    v_sra_pre = engine.query_provision_at_date("SRA-SEC-10", "2015-05-01")
    assert v_sra_pre is not None
    assert v_sra_pre.version_number == 1
    assert "discretion of the court" in v_sra_pre.text

    # SRA Sec 10: post-2018 version
    v_sra_post = engine.query_provision_at_date("SRA-SEC-10", "2022-05-01")
    assert v_sra_post is not None
    assert v_sra_post.version_number == 2
    assert "shall be enforced" in v_sra_post.text

    # ARB Sec 29A: does not exist prior to 2015-10-23
    v_arb_pre = engine.query_provision_at_date("ARB-SEC-29A", "2014-01-01")
    assert v_arb_pre is None

    # ARB Sec 29A: exists after 2015-10-23
    v_arb_post = engine.query_provision_at_date("ARB-SEC-29A", "2020-01-01")
    assert v_arb_post is not None
    assert "twelve months" in v_arb_post.text

    # CONST Art 330A: does not exist before 2023-09-28
    v_const_pre = engine.query_provision_at_date("CONST-ART-330A", "2022-01-01")
    assert v_const_pre is None

    # CONST Art 330A: exists after 2023-09-28
    v_const_post = engine.query_provision_at_date("CONST-ART-330A", "2024-01-01")
    assert v_const_post is not None
    assert "women" in v_const_post.text.lower()


# =============================================================================
# 5. LIVE KNOWLEDGE BASE RETRIEVAL & QUARANTINE TESTS
# =============================================================================

def test_kb_has_all_central_acts():
    kb = LegalKnowledgeBase("data/legalmitra_kb.db")
    total_sources = kb.count_sources()
    total_chunks = kb.count_chunks()

    assert total_sources >= 16
    assert total_chunks >= 1227

    # Check that each of the 8 Central Acts is indexed
    central_act_ids = [
        "IND-CONST-1950",
        "IND-STAT-BNS-2023",
        "IND-STAT-CPC-1908",
        "IND-STAT-LIMIT-1963",
        "IND-STAT-ICA-1872",
        "IND-STAT-SRA-1963",
        "IND-STAT-ARB-1996",
        "IND-STAT-CPA-2019",
    ]
    for act_id in central_act_ids:
        chunks = kb.get_chunks_for_source(act_id)
        assert len(chunks) > 0, f"Source {act_id} has no chunks indexed in KB!"


def test_kb_exact_retrieval_and_quarantine_exclusion():
    kb = LegalKnowledgeBase("data/legalmitra_kb.db")

    # 1. Constitution Article 21
    res_art21 = kb.search("protection of life and personal liberty", limit=5)
    assert any(r.source_id == "IND-CONST-1950" and "21" in r.provision_or_para_ref for r in res_art21)

    # 2. Bharatiya Nyaya Sanhita Section 103 (Punishment for murder)
    res_bns = kb.search("punishment for murder death or imprisonment for life", limit=5)
    assert any(r.source_id == "IND-STAT-BNS-2023" and "103" in r.provision_or_para_ref for r in res_bns)

    # 3. Code of Civil Procedure Section 80 (Notice against Government)
    res_cpc = kb.search("suit instituted against the Government until the expiration of two months", limit=5)
    assert any(r.source_id == "IND-STAT-CPC-1908" and "80" in r.provision_or_para_ref for r in res_cpc)

    # 4. Specific Relief Act Section 10 (Mandatory specific performance)
    filters_sra = SearchFilters(section_number="10")
    res_sra = kb.search("specific performance", filters=filters_sra, limit=5)
    assert any(r.source_id == "IND-STAT-SRA-1963" for r in res_sra)

    # 5. Limitation Act Section 5 (Condonation of delay)
    filters_limit = SearchFilters(section_number="5")
    res_limit = kb.search("sufficient cause delay", filters=filters_limit, limit=5)
    assert any(r.source_id == "IND-STAT-LIMIT-1963" for r in res_limit)

    # 6. Strict quarantine check: IND-JUD-DEL-2024-BAIL is NOT returned in standard search
    quarantine_hits = [c for c in kb.search("bail anticipatory", limit=50) if c.is_synthetic_scaffold]
    assert len(quarantine_hits) == 0, "Quarantined synthetic scaffold was leaked in search!"
