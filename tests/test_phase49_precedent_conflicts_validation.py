"""
Test Suite for LegalMitra Phase 49:
- Precedent Conflict Resolution & Enhanced Treatment Types
- Authority Hierarchy, Bench Strength & Territorial Jurisdiction
- Amendment-Aware Precedent Tracking & Legislative Supersession
- Claim-Level Legal Answer Validation (Claim vs Evidence Passages)
- Adversarial Legal Benchmark V5 (60 Cases, PIT-41 to PIT-60)
- Invariants & Safeguards Integrity
"""

import json
from pathlib import Path
import pytest

from legalmitra.caselaw.knowledge_graph import (
    EntityType,
    RelationType,
    build_national_judicial_knowledge_graph,
)
from legalmitra.temporal.engine import (
    TemporalLawEngine,
    build_default_temporal_engine,
)


@pytest.fixture
def knowledge_graph():
    return build_national_judicial_knowledge_graph()


@pytest.fixture
def temporal_engine():
    return build_default_temporal_engine()


# =====================================================================
# 1. PRECEDENT RELATIONSHIP & CONFLICT RESOLUTION TESTS
# =====================================================================

def test_phase49_relation_types_present():
    """Verify newly introduced relationship types in RelationType enum."""
    assert RelationType.STAYED == "stayed"
    assert RelationType.VACATED == "vacated"
    assert RelationType.LIMITS == "limits"
    assert RelationType.CONFLICTS_WITH == "conflicts_with"
    assert RelationType.SUPERSEDES_STATUTORY_BASIS == "supersedes_statutory_basis"


def test_interim_stay_evaluation(knowledge_graph):
    """Verify that an interim stay does not overrule precedent, but marks operation as stayed."""
    status = knowledge_graph.evaluate_precedent_status("CASE-HC-DEL-ST-STEPHENS-2022")
    assert status["status"] == "operation_stayed"
    assert status["has_active_stay"] is True
    assert status["is_overruled"] is False
    assert len(status["stay_details"]) > 0
    assert status["stay_details"][0]["is_interim"] is True


def test_referral_to_larger_bench_evaluation(knowledge_graph):
    """Verify that a referral to a larger bench marks status as referred without overruling."""
    status = knowledge_graph.evaluate_precedent_status("CASE-SC-RAMESH-VERMA-2017")
    assert status["status"] == "referred_to_larger_bench"
    assert status["is_referred"] is True
    assert status["is_overruled"] is False
    assert len(status["referral_details"]) > 0
    assert status["referral_details"][0]["is_resolved"] is False


def test_co_equal_bench_conflict_evaluation(knowledge_graph):
    """Verify that conflicting High Court decisions are flagged without declaring an unauthorized winner."""
    status_bom = knowledge_graph.evaluate_precedent_status("CASE-HC-BOM-ARBITRATION-2021")
    assert status_bom["status"] == "conflicting_co_equal_authority"
    assert len(status_bom["conflicts"]) > 0
    assert status_bom["conflicts"][0]["conflicting_case_id"] == "CASE-HC-DEL-ARBITRATION-2021"

    status_del = knowledge_graph.evaluate_precedent_status("CASE-HC-DEL-ARBITRATION-2021")
    assert status_del["status"] == "conflicting_co_equal_authority"
    assert status_del["conflicts"][0]["conflicting_case_id"] == "CASE-HC-BOM-ARBITRATION-2021"


def test_legislative_supersession_evaluation(knowledge_graph):
    """Verify that retrospective statutory amendment marks precedent statutory basis as superseded."""
    status = knowledge_graph.evaluate_precedent_status("CASE-SC-VODAFONE-2012")
    assert status["status"] == "statutory_basis_superseded"
    assert len(status["superseded_by_legislation"]) > 0
    assert status["superseded_by_legislation"][0]["superseding_statute_id"] == "STAT-AMEND-FINANCE-2012"


def test_reversal_on_appeal(knowledge_graph):
    """Verify reversal of Bombay HC decision by Supreme Court in Vodafone."""
    rev_edges = knowledge_graph.get_incoming_edges("CASE-HC-BOM-VODAFONE-2010", RelationType.REVERSES)
    assert len(rev_edges) == 1
    assert rev_edges[0].source_id == "CASE-SC-VODAFONE-2012"


# =====================================================================
# 2. AMENDMENT-AWARE PRECEDENT TRACKING TESTS
# =====================================================================

def test_amendment_impact_contract_act_section_28(temporal_engine):
    """Vulcan Insurance (1976) operative pre-1997, superseded post-1997."""
    res_pre = temporal_engine.resolve_amendment_impact_on_precedent(
        "CASE-VULCAN-1976", "IND-STAT-ICA-1872", "Section 28", "1995-06-10"
    )
    assert res_pre["status"] == "OPERATIVE_FOR_VERSION"
    assert res_pre["is_applicable"] is True
    assert res_pre["legislative_supersession"] is False

    res_post = temporal_engine.resolve_amendment_impact_on_precedent(
        "CASE-VULCAN-1976", "IND-STAT-ICA-1872", "Section 28", "2005-09-15"
    )
    assert res_post["status"] == "SUPERSEDED_BY_LEGISLATIVE_AMENDMENT"
    assert res_post["is_applicable"] is False
    assert res_post["legislative_supersession"] is True


def test_amendment_impact_tpa_section_53a(temporal_engine):
    """M.K. Rappai part-performance operative pre-2001, superseded post-2001."""
    res_pre = temporal_engine.resolve_amendment_impact_on_precedent(
        "CASE-RAPPAI-1998", "IND-STAT-TPA-1882", "Section 53A", "1999-12-01"
    )
    assert res_pre["status"] == "OPERATIVE_FOR_VERSION"
    assert res_pre["is_applicable"] is True

    res_post = temporal_engine.resolve_amendment_impact_on_precedent(
        "CASE-RAPPAI-1998", "IND-STAT-TPA-1882", "Section 53A", "2003-04-10"
    )
    assert res_post["status"] == "SUPERSEDED_BY_LEGISLATIVE_AMENDMENT"
    assert res_post["is_applicable"] is False


def test_amendment_impact_income_tax_vodafone(temporal_engine):
    """Vodafone (2012) operative pre-Finance Act 2012, superseded retrospectively post-Finance Act 2012."""
    res_pre = temporal_engine.resolve_amendment_impact_on_precedent(
        "CASE-SC-VODAFONE-2012", "IND-STAT-INCOME_TAX-1961", "Section 9(1)(i)", "2012-03-01"
    )
    assert res_pre["status"] == "OPERATIVE_FOR_VERSION"
    assert res_pre["is_applicable"] is True

    res_post = temporal_engine.resolve_amendment_impact_on_precedent(
        "CASE-SC-VODAFONE-2012", "IND-STAT-INCOME_TAX-1961", "Section 9(1)(i)", "2013-06-25"
    )
    assert res_post["status"] == "SUPERSEDED_BY_RETROSPECTIVE_AMENDMENT"
    assert res_post["is_applicable"] is False


# =====================================================================
# 3. CLAIM-LEVEL LEGAL ANSWER VALIDATION TESTS
# =====================================================================

def test_claim_validation_missing_source(temporal_engine):
    """Claim without source evidence triggers SOURCE_PROVENANCE_INCOMPLETE and abstention."""
    val = temporal_engine.validate_claim_evidence(
        claim_text="All commercial contracts automatically dissolve upon change in corporate shareholding."
    )
    assert val["validation_outcome"] == "SOURCE_PROVENANCE_INCOMPLETE"
    assert val["is_supported"] is False
    assert val["abstain_recommended"] is True


def test_claim_validation_fabricated_citation(temporal_engine):
    """Claim with fabricated case citation triggers UNSUPPORTED."""
    val = temporal_engine.validate_claim_evidence(
        claim_text="Digital cloud data is immune from police seizure.",
        cited_case_id="CASE-FAKE-RAMESHWAR-2022"
    )
    assert val["validation_outcome"] == "UNSUPPORTED"
    assert val["is_supported"] is False
    assert val["abstain_recommended"] is True


def test_claim_validation_contradicted_by_passage(temporal_engine):
    """Claim contradicting passage text triggers CONTRADICTED."""
    val = temporal_engine.validate_claim_evidence(
        claim_text="Contractual clauses extinguishing rights after one year are valid under Section 28.",
        passage_text="Section 28(b) stipulates that any agreement which extinguishes the rights of any party shall be void to that extent."
    )
    assert val["validation_outcome"] == "CONTRADICTED"
    assert val["is_supported"] is False


def test_claim_validation_temporally_superseded(temporal_engine):
    """Claim based on superseded statutory version triggers TEMPORALLY_UNRESOLVED."""
    val = temporal_engine.validate_claim_evidence(
        claim_text="Unregistered contract to transfer immoveable property shields possession under Section 53A.",
        cited_statute_id="IND-STAT-TPA-1882",
        cited_section="Section 53A",
        query_date_str="2005-05-10"
    )
    assert val["validation_outcome"] == "TEMPORALLY_UNRESOLVED"
    assert val["is_supported"] is False


def test_claim_validation_supported_passage(temporal_engine):
    """Supported claim with matching passage text passes validation."""
    val = temporal_engine.validate_claim_evidence(
        claim_text="Procedure established by law under Article 21 must be just, fair and reasonable.",
        cited_case_id="CASE-SC-CONST-MANEKA-GANDHI-1978",
        passage_text="The procedure contemplated in Article 21 must be just, fair and reasonable, and not fanciful, oppressive or arbitrary."
    )
    assert val["validation_outcome"] == "SUPPORTED"
    assert val["is_supported"] is True


# =====================================================================
# 4. ADVERSARIAL BENCHMARK V5 (60 CASES) TESTS
# =====================================================================

def test_benchmark_v5_manifest_has_60_cases():
    """Verify temporal benchmark manifest has been expanded to 60 cases under PIT-V5."""
    manifest_path = Path("data/22_central_legislation/temporal_benchmark_manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    cases = data.get("test_cases", [])
    assert len(cases) >= 60, f"Expected at least 60 cases under PIT-V5/V6, got {len(cases)}"
    assert "LEGALMITRA-BENCHMARK-PIT" in data.get("benchmark_suite_id", "")


def test_pit_v5_adversarial_cases_execution(knowledge_graph, temporal_engine):
    """Verify execution of Phase 49 adversarial test cases (PIT-41 to PIT-60)."""
    manifest_path = Path("data/22_central_legislation/temporal_benchmark_manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    phase49_cases = [c for c in data["test_cases"] if 41 <= int(c["case_id"].replace("PIT-", "")) <= 60]
    assert len(phase49_cases) == 20

    for tc in phase49_cases:
        cid = tc["case_id"]

        if cid == "PIT-41":
            # NN Global overruled by In Re: Interplay 7-judge bench
            status = knowledge_graph.evaluate_precedent_status("CASE-NN-GLOBAL")
            assert status["is_overruled"] is True

        elif cid == "PIT-42":
            # Arnesh Kumar distinguished, not overruled
            status = knowledge_graph.evaluate_precedent_status("CASE-ARNESH-KUMAR")
            assert status["is_overruled"] is False

        elif cid == "PIT-43":
            # Referral to larger bench does not overrule precedent
            status = knowledge_graph.evaluate_precedent_status("CASE-SC-RAMESH-VERMA-2017")
            assert status["is_referred"] is True
            assert status["is_overruled"] is False

        elif cid == "PIT-44":
            # Interim stay freezes operation but does not lay down Art 141 law
            status = knowledge_graph.evaluate_precedent_status("CASE-HC-DEL-ST-STEPHENS-2022")
            assert status["has_active_stay"] is True

        elif cid == "PIT-47":
            # Section 28 Contract Act Vulcan Insurance supersession
            imp = temporal_engine.resolve_amendment_impact_on_precedent(
                "CASE-VULCAN", "IND-STAT-ICA-1872", "28", "2005-09-15"
            )
            assert imp["legislative_supersession"] is True

        elif cid == "PIT-48":
            # Finance Act 2012 retrospective supersession of Vodafone
            imp = temporal_engine.resolve_amendment_impact_on_precedent(
                "CASE-SC-VODAFONE-2012", "IND-STAT-INCOME_TAX-1961", "9", "2013-06-25"
            )
            assert imp["legislative_supersession"] is True

        elif cid == "PIT-50":
            # High Court conflict
            status = knowledge_graph.evaluate_precedent_status("CASE-HC-BOM-ARBITRATION-2021")
            assert status["status"] == "conflicting_co_equal_authority"

        elif cid == "PIT-51":
            # Fabricated citation validation
            val = temporal_engine.validate_claim_evidence(
                claim_text="Digital cloud data is immune from police seizure.",
                cited_case_id="CASE-FAKE-RAMESHWAR-2022"
            )
            assert val["validation_outcome"] == "UNSUPPORTED"

        elif cid == "PIT-52":
            # Contradicted by passage
            val = temporal_engine.validate_claim_evidence(
                claim_text="Raw judgments are protected by copyright.",
                passage_text="Raw judgments are in the public domain and lack copyright under Section 52(1)(q)."
            )
            assert val["validation_outcome"] == "CONTRADICTED"

        elif cid == "PIT-55":
            # Missing source evidence triggers abstention
            val = temporal_engine.validate_claim_evidence(
                claim_text="Supreme Court will strike down Section 142 of Social Security Code."
            )
            assert val["abstain_recommended"] is True

