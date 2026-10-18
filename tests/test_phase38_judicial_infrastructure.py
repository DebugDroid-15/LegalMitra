"""Tests for LegalMitra Phase 38 Judicial Knowledge Infrastructure.

Verifies:
1. Judicial System Ontology (Apex, 25 High Courts, Tribunals, Military, Historical archives)
2. 14-Domain Case Taxonomy & Procedural Posture Classification
3. Citation Normalizer (Neutral citations, SCR, AIR, SCC, ILR)
4. Typed Precedent Graph Engine & Article 141 Bench Strength Invariant
5. Judicial-Legislative Evolution Engine & Evidentiary Causation Standard
6. Restricted Records & Statutory Privacy Policy Engine
7. 11-Tier Coverage Analytics & Gap Accounting
8. Machine-Readable Artifact Integrity & Independent Benchmark
"""

import json
import os
import pytest

from legalmitra.judicial.judicial_ontology import (
    CourtEntity,
    InstitutionTier,
    JudicialSystemOntology,
    JurisdictionType,
)
from legalmitra.judicial.case_taxonomy import (
    CaseTaxonomyManager,
    ProceduralPosture,
    SubstantiveDomain,
)
from legalmitra.judicial.citation_normalizer import (
    CitationNormalizer,
    ParsedCitation,
    ReporterFamily,
)
from legalmitra.judicial.precedent_graph_engine import (
    BenchStrengthCategory,
    PrecedentEdge,
    PrecedentGraphEngine,
    PrecedentNode,
    TreatmentType,
)
from legalmitra.judicial.legislative_evolution import (
    JudicialActionOnStatute,
    JudicialStatuteInteraction,
    LegislativeActionType,
    LegislativeCausationLevel,
    LegislativeEvolutionEngine,
    LegislativeResponseToCase,
)
from legalmitra.judicial.restricted_records import (
    RedactionAuditResult,
    RestrictedRecordsPolicyEngine,
    RestrictionClassification,
)
from legalmitra.judicial.coverage_analytics import (
    CourtCoverageAssessment,
    CoverageTier,
    JudicialCoverageRegistry,
)


def test_judicial_system_ontology_tiers_and_high_courts():
    ontology = JudicialSystemOntology()

    # Apex Court
    sc = ontology.get_entity("IND-SC")
    assert sc is not None
    assert sc.tier == InstitutionTier.APEX
    assert sc.seat_city == "New Delhi"
    assert sc.neutral_citation_supported is True

    # Predecessor tracing
    preds = ontology.get_predecessor_chain("IND-SC")
    pred_ids = [p.court_id for p in preds]
    assert "HIST-FED-COURT" in pred_ids
    assert "HIST-PRIVY-COUNCIL" in pred_ids

    # 25 High Courts
    high_courts = ontology.list_entities_by_tier(InstitutionTier.CONSTITUTIONAL_HIGH_COURT)
    assert len(high_courts) == 25

    # Check key High Courts
    bombay_hc = ontology.get_entity("IND-HC-BOM")
    assert bombay_hc is not None
    assert "Nagpur" in bombay_hc.benches_and_circuits
    assert "HIST-SC-BOMBAY" in bombay_hc.predecessor_court_ids

    calcutta_hc = ontology.get_entity("IND-HC-CAL")
    assert calcutta_hc is not None
    assert "Circuit Bench at Port Blair (A&N Islands)" in calcutta_hc.benches_and_circuits

    delhi_hc = ontology.get_entity("IND-HC-DEL")
    assert delhi_hc is not None
    assert delhi_hc.established_year == 1966

    # Military Justice
    aft = ontology.get_entity("IND-MIL-AFT")
    assert aft is not None
    assert aft.tier == InstitutionTier.MILITARY_JUSTICE
    assert len(aft.benches_and_circuits) >= 5

    # Specialized Tribunals
    tribunals = ontology.list_entities_by_tier(InstitutionTier.SPECIALIZED_TRIBUNAL)
    tribunal_ids = [t.court_id for t in tribunals]
    assert "IND-TR-CAT" in tribunal_ids
    assert "IND-TR-NCLAT" in tribunal_ids
    assert "IND-TR-NGT" in tribunal_ids
    assert "IND-TR-ITAT" in tribunal_ids


def test_case_taxonomy_manager():
    taxonomy = CaseTaxonomyManager()
    domains = taxonomy.list_all_domains()
    assert len(domains) == 14

    # Test classification of Bail application
    bail_sample = "This is a bail application filed under Section 439 CrPC seeking regular bail in connection with FIR No. 120."
    res_bail = taxonomy.classify_text(bail_sample)
    assert res_bail["primary_domain"] == SubstantiveDomain.CRIMINAL.value
    assert res_bail["procedural_posture"] == ProceduralPosture.BAIL_APPLICATION.value

    # Test classification of Insolvency matter
    ibc_sample = "The financial creditor filed a company petition under Section 7 IBC for initiation of corporate insolvency resolution process (CIRP)."
    res_ibc = taxonomy.classify_text(ibc_sample)
    assert res_ibc["primary_domain"] == SubstantiveDomain.COMMERCIAL_CORPORATE_INSOLVENCY.value
    assert res_ibc["procedural_posture"] == ProceduralPosture.COMPANY_PETITION_IBC.value

    # Test classification of Environmental matter
    env_sample = "Original Application before National Green Tribunal challenging environmental clearance due to severe water pollution and violation of polluter pays principle."
    res_env = taxonomy.classify_text(env_sample)
    assert res_env["primary_domain"] == SubstantiveDomain.ENVIRONMENTAL_FOREST.value


def test_citation_normalizer():
    norm = CitationNormalizer()

    # 1. Supreme Court Neutral Citation
    c1 = norm.parse_citation("2023 INSC 101")
    assert c1 is not None
    assert c1.canonical_form == "2023 INSC 101"
    assert c1.reporter_family == ReporterFamily.NEUTRAL_SUPREME_COURT
    assert c1.year == 2023
    assert c1.page_or_number == 101
    assert c1.is_neutral is True

    # 2. High Court Neutral Citation
    c2 = norm.parse_citation("2023:DHC:1234")
    assert c2 is not None
    assert c2.canonical_form == "2023:DHC:1234"
    assert c2.reporter_family == ReporterFamily.NEUTRAL_HIGH_COURT
    assert c2.court_code == "DHC"
    assert c2.page_or_number == 1234
    assert c2.is_neutral is True

    # 3. SCC Citation
    c3 = norm.parse_citation("(2017) 10 SCC 1")
    assert c3 is not None
    assert c3.canonical_form == "(2017) 10 SCC 1"
    assert c3.reporter_family == ReporterFamily.SUPREME_COURT_CASES
    assert c3.year == 2017
    assert c3.volume == 10
    assert c3.page_or_number == 1

    # 4. AIR Citation
    c4 = norm.parse_citation("AIR 1973 SC 1461")
    assert c4 is not None
    assert c4.canonical_form == "AIR 1973 SC 1461"
    assert c4.reporter_family == ReporterFamily.ALL_INDIA_REPORTER
    assert c4.year == 1973
    assert c4.court_code == "SC"
    assert c4.page_or_number == 1461

    # 5. SCR Citation
    c5 = norm.parse_citation("[1973] 4 SCR 225")
    assert c5 is not None
    assert c5.canonical_form == "[1973] 4 SCR 225"
    assert c5.reporter_family == ReporterFamily.SUPREME_COURT_REPORTS
    assert c5.year == 1973
    assert c5.volume == 4
    assert c5.page_or_number == 225

    # 6. Extract multiple citations from text
    text = (
        "In Kesavananda Bharati (AIR 1973 SC 1461), the court reconsidered Golaknath ([1967] 2 SCR 762). "
        "Later in Puttaswamy ((2017) 10 SCC 1) and recent neutral ruling 2023 INSC 500, privacy was reaffirmed."
    )
    extracted = norm.extract_citations(text)
    canonical_list = [c.canonical_form for c in extracted]
    assert "AIR 1973 SC 1461" in canonical_list
    assert "(2017) 10 SCC 1" in canonical_list
    assert "2023 INSC 500" in canonical_list


def test_precedent_graph_engine_and_bench_strength_invariants():
    graph = PrecedentGraphEngine()

    n_gopalan = PrecedentNode(
        case_id="GOPALAN",
        canonical_citation="AIR 1950 SC 27",
        case_title="A.K. Gopalan v. State of Madras",
        court_id="IND-SC",
        decision_year=1950,
        bench_judge_count=6,
        bench_category=BenchStrengthCategory.LARGER_BENCH,
        ratio_summary="Article 21 and 19 are mutually exclusive.",
    )
    n_maneka = PrecedentNode(
        case_id="MANEKA",
        canonical_citation="AIR 1978 SC 597",
        case_title="Maneka Gandhi v. Union of India",
        court_id="IND-SC",
        decision_year=1978,
        bench_judge_count=7,
        bench_category=BenchStrengthCategory.LARGER_BENCH,
        ratio_summary="Procedure established by law must be fair, just and reasonable.",
    )
    n_two_judge = PrecedentNode(
        case_id="BENCH2",
        canonical_citation="2020 INSC 999",
        case_title="Sample Bench 2 Case",
        court_id="IND-SC",
        decision_year=2020,
        bench_judge_count=2,
        bench_category=BenchStrengthCategory.DIVISION_BENCH,
        ratio_summary="Test 2-judge bench decision.",
    )

    graph.add_node(n_gopalan)
    graph.add_node(n_maneka)
    graph.add_node(n_two_judge)

    # 7-judge bench overrules 6-judge bench: Valid
    edge_valid = PrecedentEdge(
        citing_case_id="MANEKA",
        cited_case_id="GOPALAN",
        treatment=TreatmentType.OVERRULED,
        passage_anchor="Para 56",
        treatment_context="7-judge bench overruled A.K. Gopalan.",
    )
    graph.add_edge(edge_valid)

    is_good, note = graph.is_good_law("GOPALAN")
    assert is_good is False
    assert "Overruled by AIR 1978 SC 597" in note

    is_good_m, _ = graph.is_good_law("MANEKA")
    assert is_good_m is True

    # Invariant: 2-judge bench attempting to overrule 7-judge bench MUST raise ValueError
    invalid_edge = PrecedentEdge(
        citing_case_id="BENCH2",
        cited_case_id="MANEKA",
        treatment=TreatmentType.OVERRULED,
        passage_anchor="Para 10",
        treatment_context="Improper attempt by smaller bench to overrule larger bench.",
    )
    with pytest.raises(ValueError, match="Jurisprudential Invariant Violation"):
        graph.add_edge(invalid_edge)


def test_legislative_evolution_engine_evidentiary_standards():
    engine = LegislativeEvolutionEngine()

    # Check canonical direct legislative responses
    vishaka_responses = engine.get_legislative_responses_for_case("VISHAKA-1997")
    assert len(vishaka_responses) == 1
    resp = vishaka_responses[0]
    assert resp.enacted_statute_or_amendment == "Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013"
    assert resp.causation_level == LegislativeCausationLevel.DIRECT_LEGISLATIVE_RESPONSE
    assert "Statement of Objects and Reasons" in resp.official_evidentiary_citation

    # Test that recording DIRECT_LEGISLATIVE_RESPONSE without official citation raises ValueError
    bad_response = LegislativeResponseToCase(
        response_id="RESP-TEST-BAD",
        prior_case_id="VISHAKA-1997",
        prior_case_citation="AIR 1997 SC 3011",
        enacted_statute_or_amendment="Some Unverified Act 2024",
        year_of_enactment=2024,
        legislative_action=LegislativeActionType.AMENDED_PROSPECTIVELY,
        causation_level=LegislativeCausationLevel.DIRECT_LEGISLATIVE_RESPONSE,
        official_evidentiary_citation="",  # Empty citation violates invariant!
        detailed_evolution_notes="Unfounded causal claim.",
    )
    with pytest.raises(ValueError, match="Evidentiary Invariant Violation"):
        engine.record_legislative_response(bad_response)


def test_restricted_records_policy_engine():
    engine = RestrictedRecordsPolicyEngine()

    # 1. POCSO case
    pocso_text = "The victim namely Sunita was a minor aged 12 years under the Protection of Children from Sexual Offences (POCSO) Act."
    res_pocso = engine.audit_record(pocso_text)
    assert res_pocso.classification == RestrictionClassification.REDACTION_REQUIRED_CHILD_PROTECTION
    assert res_pocso.requires_redaction is True
    assert res_pocso.is_eligible_for_ingestion is True
    assert "[CHILD_VICTIM_ANONYMIZED]" in (res_pocso.sanitized_text or "")
    assert "Sunita" not in (res_pocso.sanitized_text or "")

    # 2. Section 376 IPC case
    rape_text = "The prosecutrix namely Radha was subjected to sexual assault under Section 376 IPC."
    res_rape = engine.audit_record(rape_text)
    assert res_rape.classification == RestrictionClassification.REDACTION_REQUIRED_SEXUAL_OFFENCE
    assert res_rape.requires_redaction is True
    assert "[VICTIM_ANONYMIZED]" in (res_rape.sanitized_text or "")
    assert "Radha" not in (res_rape.sanitized_text or "")

    # 3. Sealed Cover / In-Camera case
    sealed_text = "The inquiry report was placed in sealed cover and proceedings held in camera."
    res_sealed = engine.audit_record(sealed_text)
    assert res_sealed.classification == RestrictionClassification.IN_CAMERA_SEALED_BARRED
    assert res_sealed.is_eligible_for_ingestion is False

    # 4. Classified National Security case
    sec_text = "The document contained classified military operation details under Official Secrets Act."
    res_sec = engine.audit_record(sec_text)
    assert res_sec.classification == RestrictionClassification.NATIONAL_SECURITY_CLASSIFIED_BARRED
    assert res_sec.is_eligible_for_ingestion is False

    # 5. Normal Public Case
    pub_text = "Civil suit for specific performance of contract for sale of commercial property."
    res_pub = engine.audit_record(pub_text)
    assert res_pub.classification == RestrictionClassification.UNRESTRICTED_PUBLIC
    assert res_pub.is_eligible_for_ingestion is True
    assert res_pub.requires_redaction is False


def test_coverage_analytics_registry():
    registry = JudicialCoverageRegistry()
    summary = registry.get_national_summary()

    assert summary["total_institutions_tracked"] >= 7
    assert summary["total_ingested_records"] > 0
    assert summary["total_verified_records"] > 0

    # Verify no institution without complete empirical acquisition is marked Tier 7+
    for assessment in registry.list_all_assessments():
        if assessment.current_tier >= CoverageTier.TIER_7_COMPREHENSIVE_ERA:
            assert len(assessment.known_coverage_gaps) == 0


def test_machine_readable_artifacts_exist_and_valid():
    target_dir = os.path.join("data", "21_judicial_infrastructure")
    expected_files = [
        "court_and_tribunal_registry.json",
        "case_type_taxonomy.json",
        "precedent_relationship_graph.json",
        "judicial_legislative_evolution_graph.json",
        "judicial_coverage_matrix.json",
        "restricted_records_policy.json",
        "independent_judicial_benchmark.json",
    ]

    for fname in expected_files:
        fpath = os.path.join(target_dir, fname)
        assert os.path.exists(fpath), f"Missing artifact: {fname}"
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert isinstance(data, dict), f"Artifact {fname} is not a valid JSON dictionary"

    # Verify independent judicial benchmark contains 25 verified cases
    bench_path = os.path.join(target_dir, "independent_judicial_benchmark.json")
    with open(bench_path, "r", encoding="utf-8") as f:
        bench_data = json.load(f)
        assert bench_data["total_test_cases"] == 25
        assert len(bench_data["cases"]) == 25
        for case in bench_data["cases"]:
            assert case["verified"] is True
            assert len(case["expected_answer"]) > 0
            assert len(case["statutory_authority"]) > 0
