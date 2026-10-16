"""
Test suite for Phase 7 Controlled Generation Pilot and Phase 7.1 Temporal Audit.
Verifies schema compliance, grounding validity, source integrity, quarantine controls,
and temporal-law consistency under G.S.R. 843(E) and S.O. 848(E).
"""

import json
from pathlib import Path
from datetime import date
import pytest

from legalmitra.core.enums import (
    LawStatusLabel,
    LegalReviewStatus,
    ProvisionCommencementStatus,
    TemporalValidationStatus,
)
from legalmitra.schemas.legal_qa import EvidencePassage, LegalQADocument
from legalmitra.ingestion.registry import SourceRegistryManager
from legalmitra.validation.grounding_validator import GroundingValidator
from legalmitra.validation.temporal_validator import TemporalValidator
from legalmitra.generation.orchestrator import GenerationOrchestrator
from legalmitra.generation.schemas import GenerationConfig


def test_pilot_20_examples_existence_and_schema():
    examples_file = Path("data/03_generated/pilot_20_examples.jsonl")
    assert examples_file.exists(), "pilot_20_examples.jsonl must exist"

    lines = [line.strip() for line in open(examples_file, "r", encoding="utf-8") if line.strip()]
    assert len(lines) == 20, f"Expected exactly 20 examples in pilot, got {len(lines)}"

    docs = []
    for line in lines:
        data = json.loads(line)
        doc = LegalQADocument(**data)
        docs.append(doc)

    # Verify ID counts and defaults
    qa_ids = [d.qa_id for d in docs]
    assert len(set(qa_ids)) == 20, "All QA IDs must be unique"

    dpdp_ids = [d for d in docs if d.qa_id.startswith("QA-PILOT-DPDP-")]
    cross_ids = [d for d in docs if d.qa_id.startswith("QA-PILOT-CROSS-")]
    assert len(dpdp_ids) == 10, f"Expected 10 DPDP examples, got {len(dpdp_ids)}"
    assert len(cross_ids) == 10, f"Expected 10 Cross-statute examples, got {len(cross_ids)}"

    for d in docs:
        assert d.legal_review_status == LegalReviewStatus.PENDING_LEGAL_REVIEW
        assert not d.flagged_unsupported
        assert len(d.supporting_source_ids) >= 1
        assert len(d.evidence_passages) >= 1
        assert "IND-JUD-DEL-2024-BAIL" not in d.supporting_source_ids
        assert d.legal_as_of_date is not None
        assert d.commencement_source_id is not None
        assert d.law_status_label is not None
        assert d.temporal_validation_status is not None


def test_pilot_20_grounding_validity():
    reg = SourceRegistryManager("registry/source_registry.jsonl")
    orch = GenerationOrchestrator(GenerationConfig(dry_run=True), reg)
    validator = GroundingValidator(reg)

    source_ids = [
        "IND-STAT-DPDP-2023",
        "IND-STAT-IT-2000",
        "IND-STAT-BSA-2023-SEC61",
        "IND-STAT-BSA-2023-SEC63",
        "IND-STAT-BNSS-2023",
    ]
    source_texts = {sid: orch.load_source_text(sid) for sid in source_ids}

    examples_file = Path("data/03_generated/pilot_20_examples.jsonl")
    with open(examples_file, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            doc = LegalQADocument(**json.loads(line))
            is_grounded, issues = validator.validate_grounding(doc, source_texts)
            assert is_grounded, f"Example {idx} ({doc.qa_id}) failed grounding validation: {issues}"


def test_pilot_20_manifest_consistency():
    manifest_file = Path("data/03_generated/pilot_20_manifest.json")
    assert manifest_file.exists(), "pilot_20_manifest.json must exist"

    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    assert manifest["total_examples"] == 20
    assert manifest["category_breakdown"]["dpdp_it_statutory_qa"] == 10
    assert manifest["category_breakdown"]["cross_statute_evidence_and_cybercrime"] == 10
    assert manifest["quarantine_compliance"]["synthetic_scaffold_quarantined"] is not None
    assert len(manifest["examples"]) == 20
    assert manifest["temporal_law_distribution"]["enacted_not_yet_in_force"] == 9
    assert manifest["temporal_law_distribution"]["in_force"] == 10
    assert manifest["temporal_law_distribution"]["partially_commenced"] == 1
    assert manifest["temporal_law_distribution"]["repealed_prior_enactments_saved"] == 1


def test_pilot_20_temporal_validation_all_passed():
    validator = TemporalValidator()
    examples_file = Path("data/03_generated/pilot_20_examples.jsonl")

    with open(examples_file, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            doc = LegalQADocument(**json.loads(line))
            is_temporal, issues = validator.validate_temporal_claims(doc)
            assert is_temporal, f"Example {idx} ({doc.qa_id}) failed temporal audit: {issues}"


def test_bnss_section_531_anti_conflation_regression():
    """
    Regression test ensuring BNSS provisions cannot be erroneously labeled 'repealed'
    or 'repealed_with_savings', and that repeal/savings of prior CrPC 1973 is modeled
    separately under repealed_statute_context and repealed_statute_status.
    """
    validator = TemporalValidator()

    # 1. Valid representation of BNSS Section 531(2)(a)
    valid_doc = LegalQADocument(
        qa_id="QA-TEST-BNSS-531-VALID",
        question="How does BNSS Section 531 govern pending proceedings initiated under CrPC 1973?",
        answer="Section 531(2)(a) of the BNSS provides that pending proceedings shall continue under CrPC 1973.",
        supporting_source_ids=["IND-STAT-BNSS-2023"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-BNSS-2023",
                section_or_para_ref="Section 531(2)(a)",
                verbatim_text="531. Repeal and savings.-(1) The Code of Criminal Procedure, 1973 is hereby repealed.",
            )
        ],
        legal_domain="Criminal Procedure - Transition and Savings",
        statutory_citations=["Section 531(2)(a), Bharatiya Nagarik Suraksha Sanhita, 2023"],
        legal_as_of_date=date(2026, 10, 16),
        commencement_source_id="IND-NOTIF-MHA-SO-848E-2024",
        commencement_date=date(2024, 7, 1),
        law_status_label=LawStatusLabel.IN_FORCE,  # BNSS provision is in force
        provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
        repealed_statute_context="Code of Criminal Procedure, 1973 (Act No. 2 of 1974) is repealed with savings under BNSS s. 531(2)(a)",
        repealed_statute_status=LawStatusLabel.REPEALED_WITH_SAVINGS,
    )

    is_valid, issues = validator.validate_temporal_claims(valid_doc)
    assert is_valid, f"Valid BNSS 531 document failed temporal validation: {issues}"
    assert valid_doc.temporal_validation_status == TemporalValidationStatus.VERIFIED_HISTORICAL_SAVINGS

    # 2. Conflated representation: Labeling the BNSS provision itself as repealed_with_savings
    conflated_doc = LegalQADocument(
        qa_id="QA-TEST-BNSS-531-CONFLATED",
        question="How does BNSS Section 531 govern pending proceedings?",
        answer="Section 531 of the BNSS is a savings clause.",
        supporting_source_ids=["IND-STAT-BNSS-2023"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-BNSS-2023",
                section_or_para_ref="Section 531(2)(a)",
                verbatim_text="531. Repeal and savings.-(1) The Code of Criminal Procedure, 1973 is hereby repealed.",
            )
        ],
        legal_domain="Criminal Procedure - Transition and Savings",
        statutory_citations=["Section 531(2)(a), Bharatiya Nagarik Suraksha Sanhita, 2023"],
        legal_as_of_date=date(2026, 10, 16),
        commencement_source_id="IND-NOTIF-MHA-SO-848E-2024",
        commencement_date=date(2024, 7, 1),
        law_status_label=LawStatusLabel.REPEALED_WITH_SAVINGS,  # Error: conflating CrPC with BNSS provision!
        provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
    )

    is_valid_conflated, conflated_issues = validator.validate_temporal_claims(conflated_doc)
    assert not is_valid_conflated, "TemporalValidator must reject BNSS provision labeled repealed_with_savings"
    assert any("Provision of BNSS 2023 cannot be labeled 'repealed' or 'repealed_with_savings'" in iss for iss in conflated_issues)


def test_temporal_validator_fails_on_uncommenced_as_operative():
    validator = TemporalValidator()

    # Erroneous document claiming uncommenced DPDP Section 11 is currently in force on 2026-10-16
    bad_doc = LegalQADocument(
        qa_id="QA-TEST-BAD-TEMPORAL-001",
        question="Can a Data Principal currently file a request under Section 11 of the DPDP Act today?",
        answer="Yes, under Section 11 of the Digital Personal Data Protection Act, 2023, a Data Principal currently has the operative right to obtain a summary of personal data.",
        supporting_source_ids=["IND-STAT-DPDP-2023"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-DPDP-2023",
                section_or_para_ref="Section 11(1)",
                verbatim_text="11. Right to access information about personal data.-(1) The Data Principal shall have the right to obtain from the Data Fiduciary",
            )
        ],
        legal_domain="Data Protection",
        statutory_citations=["Section 11, Digital Personal Data Protection Act, 2023"],
        legal_as_of_date=date(2026, 10, 16),
        law_status_label=LawStatusLabel.IN_FORCE,  # Incorrect!
        provision_commencement_status=ProvisionCommencementStatus.COMMENCED,  # Incorrect!
    )

    is_valid, issues = validator.validate_temporal_claims(bad_doc)
    assert not is_valid, "TemporalValidator must fail when uncommenced provision is marked in_force"
    assert any("is labeled 'in_force'" in issue for issue in issues)


def test_boundary_date_evaluations_around_may_13_2027():
    validator = TemporalValidator()

    # 1. Eve of commencement (12 May 2027): Group 3 is not yet in force
    date_eve = date(2027, 5, 12)
    comm_date, group_desc = validator.get_dpdp_commencement_date("Section 11")
    assert date_eve < comm_date
    assert comm_date == date(2027, 5, 13)

    # 2. Effective date (13 May 2027): Group 3 is in force
    date_eff = date(2027, 5, 13)
    assert date_eff >= comm_date

    # 3. Post commencement (14 May 2027)
    date_post = date(2027, 5, 14)
    assert date_post >= comm_date


def test_dpdp_commencement_groupings_separate():
    validator = TemporalValidator()

    # Group 1: ss. 2, 18-26, 35-43, 44(1), 44(3) -> 13 Nov 2025
    d1, _ = validator.get_dpdp_commencement_date("Section 2")
    assert d1 == date(2025, 11, 13)
    d1_board, _ = validator.get_dpdp_commencement_date("Section 18")
    assert d1_board == date(2025, 11, 13)
    d1_gov, _ = validator.get_dpdp_commencement_date("Section 36")
    # Section 36 is in Group 3 under Gazette footnote!
    d3_36, _ = validator.get_dpdp_commencement_date("Section 36")
    assert d3_36 == date(2027, 5, 13)

    # Group 2: s. 6(9), s. 27(1)(d) -> 13 Nov 2026
    d2_dpo, _ = validator.get_dpdp_commencement_date("Section 6(9)")
    assert d2_dpo == date(2026, 11, 13)
    d2_board_power, _ = validator.get_dpdp_commencement_date("Section 27(1)(d)")
    assert d2_board_power == date(2026, 11, 13)

    # Group 3: Section 6(1), Section 8(5), Section 11, Section 33, Section 44(2) -> 13 May 2027
    d3_consent, _ = validator.get_dpdp_commencement_date("Section 6(1)")
    assert d3_consent == date(2027, 5, 13)
    d3_security, _ = validator.get_dpdp_commencement_date("Section 8(5)")
    assert d3_security == date(2027, 5, 13)
    d3_penalties, _ = validator.get_dpdp_commencement_date("Section 33")
    assert d3_penalties == date(2027, 5, 13)
    d3_it_amend, _ = validator.get_dpdp_commencement_date("Section 44(2)")
    assert d3_it_amend == date(2027, 5, 13)
