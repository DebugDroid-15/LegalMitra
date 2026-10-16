"""
Adversarial Quality-Gate Test Suite (Phase 8).
Validates that DataQualityGate actively catches and rejects all 12 edge/adversarial cases:
1. Fabricated source ID.
2. Source with invalid or missing URL.
3. Authentic quotation attributed to the wrong section.
4. Passage that matches source but omits a legally material proviso.
5. Uncommenced provision described as currently enforceable.
6. Provision with partial commencement incorrectly labeled fully commenced.
7. Quarantined scaffold referenced directly or indirectly.
8. Duplicate questions with superficially different wording.
9. Missing legal-as-of date or commencement metadata.
10. Attempted automated transition to advocate-approved status.
11. Repealed statute's status incorrectly assigned to a provision of its replacement statute.
12. Source updated after the answer's legal-as-of date without a preserved historical version.
"""

from datetime import date
from pathlib import Path
import pytest

from legalmitra.core.enums import (
    Jurisdiction,
    LawStatusLabel,
    LegalReviewStatus,
    ProcessingStatus,
    ProvisionCommencementStatus,
    SourceType,
)
from legalmitra.generation.orchestrator import GenerationOrchestrator
from legalmitra.generation.schemas import GenerationConfig
from legalmitra.ingestion.registry import SourceRegistryManager
from legalmitra.schemas.legal_qa import EvidencePassage, LegalQADocument
from legalmitra.schemas.registry import SourceRegistryRecord
from legalmitra.validation.quality_gate import DataQualityGate


@pytest.fixture
def gate_fixture():
    reg = SourceRegistryManager("registry/source_registry.jsonl")
    orch = GenerationOrchestrator(GenerationConfig(dry_run=True), reg)
    source_ids = [
        "IND-STAT-DPDP-2023",
        "IND-STAT-IT-2000",
        "IND-STAT-BSA-2023-SEC61",
        "IND-STAT-BSA-2023-SEC63",
        "IND-STAT-BNSS-2023",
    ]
    source_texts = {sid: orch.load_source_text(sid) for sid in source_ids}
    gate = DataQualityGate(registry_manager=reg, source_texts=source_texts)
    return gate, reg


def test_adv_01_fabricated_source_id(gate_fixture):
    """Case 1: Fabricated source ID not found in registry."""
    gate, _ = gate_fixture
    doc = LegalQADocument(
        qa_id="QA-ADV-001",
        question="What are data fiduciary obligations?",
        answer="Under Section 8, obligations exist.",
        supporting_source_ids=["IND-STAT-FABRICATED-9999"],  # Fabricated!
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-FABRICATED-9999",
                section_or_para_ref="Section 8",
                verbatim_text="Data Fiduciary shall protect personal data",
            )
        ],
        legal_domain="Data Protection",
        statutory_citations=["Section 8, DPDP Act, 2023"],
        legal_as_of_date=date(2026, 10, 16),
        commencement_source_id="IND-NOTIF-MEITY-GSR-843E-2025",
        commencement_date=date(2027, 5, 13),
        law_status_label=LawStatusLabel.ENACTED_NOT_YET_IN_FORCE,
        provision_commencement_status=ProvisionCommencementStatus.UNCOMMENCED,
    )

    result = gate.validate_record(doc)
    assert not result.is_valid
    assert "source_authenticity" in result.failed_checks
    assert any("not found in Source Registry" in iss for iss in result.issues)


def test_adv_02_source_with_invalid_or_missing_url(tmp_path):
    """Case 2: Source with an invalid or dummy placeholder URL."""
    reg_path = tmp_path / "bad_url_registry.jsonl"
    bad_record = SourceRegistryRecord(
        document_id="IND-STAT-TEST-BADURL",
        title="Test Statute with Placeholder URL",
        source_url="https://example.com/unsupported",  # Dummy placeholder URL!
        source_type=SourceType.STATUTE,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        document_date=date(2023, 1, 1),
        licence_or_terms="GODL-India",
        checksum="a" * 64,
        raw_file_path=str(tmp_path / "dummy.txt"),
        file_format=".txt",
        byte_size=10,
        processing_status=ProcessingStatus.NORMALIZED,
    )
    with open(reg_path, "w", encoding="utf-8") as f:
        f.write(bad_record.model_dump_json() + "\n")

    reg = SourceRegistryManager(str(reg_path))
    gate = DataQualityGate(registry_manager=reg)

    doc = LegalQADocument(
        qa_id="QA-ADV-002",
        question="What does this test statute say?",
        answer="It provides test text.",
        supporting_source_ids=["IND-STAT-TEST-BADURL"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-TEST-BADURL",
                section_or_para_ref="Section 1",
                verbatim_text="Test statutory text",
            )
        ],
        legal_domain="General Law",
        statutory_citations=["Section 1, Test Statute, 2023"],
        legal_as_of_date=date(2026, 10, 16),
        commencement_source_id="IND-NOTIF-TEST-2023",
        commencement_date=date(2023, 1, 1),
        law_status_label=LawStatusLabel.IN_FORCE,
        provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
    )

    result = gate.validate_record(doc)
    assert not result.is_valid
    assert "source_authenticity" in result.failed_checks
    assert any("lacks a valid canonical source_url" in iss for iss in result.issues)


def test_adv_03_authentic_quotation_attributed_to_wrong_section(gate_fixture):
    """Case 3: Authentic quotation text belonging to Section 11 is attributed to Section 12."""
    gate, _ = gate_fixture
    doc = LegalQADocument(
        qa_id="QA-ADV-003",
        question="What is the right of correction under Section 12?",
        answer="Section 12 provides access to personal data.",
        supporting_source_ids=["IND-STAT-DPDP-2023"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-DPDP-2023",
                section_or_para_ref="Section 12",  # Mismatched reference!
                verbatim_text="11. Right to access information about personal data.-(1) The Data Principal shall have the right",
            )
        ],
        legal_domain="Data Protection",
        statutory_citations=["Section 12, DPDP Act, 2023"],
        legal_as_of_date=date(2026, 10, 16),
        commencement_source_id="IND-NOTIF-MEITY-GSR-843E-2025",
        commencement_date=date(2027, 5, 13),
        law_status_label=LawStatusLabel.ENACTED_NOT_YET_IN_FORCE,
        provision_commencement_status=ProvisionCommencementStatus.UNCOMMENCED,
    )

    result = gate.validate_record(doc)
    assert not result.is_valid
    assert "exact_evidence_matching" in result.failed_checks
    assert any("Section attribution mismatch" in iss for iss in result.issues)


def test_adv_04_material_proviso_omission(gate_fixture):
    """Case 4: Passage quotes Section 61 BSA but claims unconditional admissibility without certificate."""
    gate, _ = gate_fixture
    doc = LegalQADocument(
        qa_id="QA-ADV-004",
        question="Are electronic records unconditionally admissible under Section 61 BSA?",
        answer="Yes, electronic records have unconditional admissibility under Section 61 without any certificate requirement, certificate is not required.",
        supporting_source_ids=["IND-STAT-BSA-2023-SEC61"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-BSA-2023-SEC61",
                section_or_para_ref="Section 61",
                verbatim_text="Nothing in this Adhiniyam shall apply to deny the admissibility of an electronic or digital record in the evidence on the ground that it is an electronic or digital record",
            )
        ],
        legal_domain="Evidence Law",
        statutory_citations=["Section 61, Bharatiya Sakshya Adhiniyam, 2023"],
        legal_as_of_date=date(2026, 10, 16),
        commencement_source_id="IND-NOTIF-MHA-SO-849E-2024",
        commencement_date=date(2024, 7, 1),
        law_status_label=LawStatusLabel.IN_FORCE,
        provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
    )

    result = gate.validate_record(doc)
    assert not result.is_valid
    assert "exact_evidence_matching" in result.failed_checks
    assert any("omitting the legally material statutory proviso" in iss for iss in result.issues)


def test_adv_05_uncommenced_provision_described_as_currently_enforceable(gate_fixture):
    """Case 5: Uncommenced provision (DPDP s.11) falsely asserted as operative today."""
    gate, _ = gate_fixture
    doc = LegalQADocument(
        qa_id="QA-ADV-005",
        question="Can a citizen enforce their right under Section 11 of the DPDP Act today?",
        answer="Yes, Section 11 is currently in force and can be legally exercised today by any Data Principal.",
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
        commencement_source_id="IND-NOTIF-MEITY-GSR-843E-2025",
        commencement_date=date(2027, 5, 13),
        law_status_label=LawStatusLabel.IN_FORCE,  # False claim!
        provision_commencement_status=ProvisionCommencementStatus.COMMENCED,  # False claim!
    )

    result = gate.validate_record(doc)
    assert not result.is_valid
    assert "section_level_commencement" in result.failed_checks
    assert any("is labeled 'in_force', but its commencement date is 2027-05-13" in iss for iss in result.issues)


def test_adv_06_partial_commencement_incorrectly_labelled_fully_commenced(gate_fixture):
    """Case 6: Section 44 DPDP Act (partially commenced) incorrectly labeled fully commenced."""
    gate, _ = gate_fixture
    doc = LegalQADocument(
        qa_id="QA-ADV-006",
        question="Has Section 44 of the DPDP Act fully amended the IT Act as of 16 October 2026?",
        answer="Section 44 is fully in force.",
        supporting_source_ids=["IND-STAT-DPDP-2023"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-DPDP-2023",
                section_or_para_ref="Section 44(2)",
                verbatim_text="(2) The Information Technology Act, 2000 (21 of 2000) shall be amended in the following manner, namely:-\n\n(a) section 43A shall be omitted;",
            )
        ],
        legal_domain="Data Protection",
        statutory_citations=["Section 44, Digital Personal Data Protection Act, 2023"],
        legal_as_of_date=date(2026, 10, 16),
        commencement_source_id="IND-NOTIF-MEITY-GSR-843E-2025",
        commencement_date=date(2025, 11, 13),
        law_status_label=LawStatusLabel.IN_FORCE,  # Incorrect: s.44(2) is uncommenced until 13 May 2027!
        provision_commencement_status=ProvisionCommencementStatus.COMMENCED,  # Incorrect: it is partial!
    )

    result = gate.validate_record(doc)
    assert not result.is_valid
    assert "section_level_commencement" in result.failed_checks
    assert any("partially commenced under G.S.R. 843(E)" in iss for iss in result.issues)


def test_adv_07_quarantined_scaffold_referenced_directly_or_indirectly(gate_fixture):
    """Case 7: Quarantined scaffold referenced directly or indirectly."""
    gate, _ = gate_fixture

    # 7A: Direct reference to quarantined document ID
    doc_direct = LegalQADocument(
        qa_id="QA-ADV-007A",
        question="Can anticipatory bail be filed under BNSS Section 482?",
        answer="Under BNSS 482 bail can be sought.",
        supporting_source_ids=["IND-JUD-DEL-2024-BAIL"],  # Direct quarantined ID!
        evidence_passages=[
            EvidencePassage(
                source_id="IND-JUD-DEL-2024-BAIL",
                section_or_para_ref="Para 1",
                verbatim_text="IN THE HIGH COURT OF DELHI AT NEW DELHI",
            )
        ],
        legal_domain="Criminal Procedure",
        statutory_citations=["Section 482, Bharatiya Nagarik Suraksha Sanhita, 2023"],
        legal_as_of_date=date(2026, 10, 16),
        commencement_source_id="IND-NOTIF-MHA-SO-848E-2024",
        commencement_date=date(2024, 7, 1),
        law_status_label=LawStatusLabel.IN_FORCE,
        provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
    )
    res_direct = gate.validate_record(doc_direct)
    assert not res_direct.is_valid
    assert "quarantine_exclusion" in res_direct.failed_checks

    # 7B: Indirect reference (relying on synthetic precedent name in question/answer/citations)
    doc_indirect = LegalQADocument(
        qa_id="QA-ADV-007B",
        question="In State v. Rahul Kumar, how did the High Court interpret anticipatory bail?",
        answer="In State (NCT of Delhi) v. Rahul Kumar, bail was discussed under BNSS Section 482.",
        supporting_source_ids=["IND-STAT-BNSS-2023"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-BNSS-2023",
                section_or_para_ref="Section 482(1)",
                verbatim_text="When any person has reason to believe that he may be arrested on an accusation of having committed a non-bailable offence",
            )
        ],
        legal_domain="Criminal Procedure",
        statutory_citations=["Section 482, Bharatiya Nagarik Suraksha Sanhita, 2023"],
        case_citations=["State (NCT of Delhi) v. Rahul Kumar, Bail Appln 1234/2024"],
        legal_as_of_date=date(2026, 10, 16),
        commencement_source_id="IND-NOTIF-MHA-SO-848E-2024",
        commencement_date=date(2024, 7, 1),
        law_status_label=LawStatusLabel.IN_FORCE,
        provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
    )
    res_indirect = gate.validate_record(doc_indirect)
    assert not res_indirect.is_valid
    assert "quarantine_exclusion" in res_indirect.failed_checks
    assert any("indirect reference to quarantined synthetic scaffold" in iss for iss in res_indirect.issues)


def test_adv_08_duplicate_questions_with_superficially_different_wording(gate_fixture):
    """Case 8: Near-duplicate question with superficially rephrased words."""
    gate, _ = gate_fixture
    doc1 = LegalQADocument(
        qa_id="QA-ADV-008A",
        question="What is electronic evidence under BSA Section 61?",
        answer="Section 61 provides that electronic records are admissible.",
        supporting_source_ids=["IND-STAT-BSA-2023-SEC61"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-BSA-2023-SEC61",
                section_or_para_ref="Section 61",
                verbatim_text="Nothing in this Adhiniyam shall apply to deny the admissibility of an electronic or digital record",
            )
        ],
        legal_domain="Evidence Law",
        statutory_citations=["Section 61, Bharatiya Sakshya Adhiniyam, 2023"],
        legal_as_of_date=date(2026, 10, 16),
        commencement_source_id="IND-NOTIF-MHA-SO-849E-2024",
        commencement_date=date(2024, 7, 1),
        law_status_label=LawStatusLabel.IN_FORCE,
        provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
        legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
    )

    doc2 = LegalQADocument(
        qa_id="QA-ADV-008B",
        question="Under BSA Section 61, what is electronic evidence?",  # Superficial word reordering
        answer="Section 61 provides that electronic records are admissible.",
        supporting_source_ids=["IND-STAT-BSA-2023-SEC61"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-BSA-2023-SEC61",
                section_or_para_ref="Section 61",
                verbatim_text="Nothing in this Adhiniyam shall apply to deny the admissibility of an electronic or digital record",
            )
        ],
        legal_domain="Evidence Law",
        statutory_citations=["Section 61, Bharatiya Sakshya Adhiniyam, 2023"],
        legal_as_of_date=date(2026, 10, 16),
        commencement_source_id="IND-NOTIF-MHA-SO-849E-2024",
        commencement_date=date(2024, 7, 1),
        law_status_label=LawStatusLabel.IN_FORCE,
        provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
        legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
    )

    all_passed, results = gate.validate_batch([doc1, doc2])
    assert not all_passed
    assert results[0].is_valid is True
    assert results[1].is_valid is False
    assert "duplicate_detection" in results[1].failed_checks


def test_adv_09_missing_legal_as_of_date_or_commencement_metadata(gate_fixture):
    """Case 9: Missing legal-as-of date or commencement metadata."""
    gate, _ = gate_fixture

    # 9A: Missing legal_as_of_date
    doc_no_date = LegalQADocument(
        qa_id="QA-ADV-009A",
        question="What are consent requirements under Section 6?",
        answer="Consent must be free and specific.",
        supporting_source_ids=["IND-STAT-DPDP-2023"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-DPDP-2023",
                section_or_para_ref="Section 6(1)",
                verbatim_text="6. Consent.--(1) The consent given by the Data Principal shall be free",
            )
        ],
        legal_domain="Data Protection",
        statutory_citations=["Section 6(1), DPDP Act, 2023"],
        legal_as_of_date=None,  # Missing!
        commencement_source_id="IND-NOTIF-MEITY-GSR-843E-2025",
        commencement_date=date(2027, 5, 13),
        law_status_label=LawStatusLabel.ENACTED_NOT_YET_IN_FORCE,
        provision_commencement_status=ProvisionCommencementStatus.UNCOMMENCED,
    )
    res_no_date = gate.validate_record(doc_no_date)
    assert not res_no_date.is_valid
    assert "legal_as_of_date_consistency" in res_no_date.failed_checks

    # 9B: Missing commencement_date
    doc_no_comm = LegalQADocument(
        qa_id="QA-ADV-009B",
        question="What are consent requirements under Section 6?",
        answer="Consent must be free and specific.",
        supporting_source_ids=["IND-STAT-DPDP-2023"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-DPDP-2023",
                section_or_para_ref="Section 6(1)",
                verbatim_text="6. Consent.--(1) The consent given by the Data Principal shall be free",
            )
        ],
        legal_domain="Data Protection",
        statutory_citations=["Section 6(1), DPDP Act, 2023"],
        legal_as_of_date=date(2026, 10, 16),
        commencement_source_id="IND-NOTIF-MEITY-GSR-843E-2025",
        commencement_date=None,  # Missing!
        law_status_label=LawStatusLabel.ENACTED_NOT_YET_IN_FORCE,
        provision_commencement_status=ProvisionCommencementStatus.UNCOMMENCED,
    )
    res_no_comm = gate.validate_record(doc_no_comm)
    assert not res_no_comm.is_valid
    assert "legal_as_of_date_consistency" in res_no_comm.failed_checks


def test_adv_10_attempted_automated_transition_to_advocate_approved(gate_fixture):
    """Case 10: Automated system attempts to set status to LEGAL_EXPERT_APPROVED."""
    gate, _ = gate_fixture
    doc = LegalQADocument(
        qa_id="QA-ADV-010",
        question="What is electronic evidence under BSA Section 61?",
        answer="Section 61 provides for admissibility.",
        supporting_source_ids=["IND-STAT-BSA-2023-SEC61"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-BSA-2023-SEC61",
                section_or_para_ref="Section 61",
                verbatim_text="Nothing in this Adhiniyam shall apply to deny the admissibility of an electronic or digital record",
            )
        ],
        legal_domain="Evidence Law",
        statutory_citations=["Section 61, Bharatiya Sakshya Adhiniyam, 2023"],
        legal_as_of_date=date(2026, 10, 16),
        commencement_source_id="IND-NOTIF-MHA-SO-849E-2024",
        commencement_date=date(2024, 7, 1),
        law_status_label=LawStatusLabel.IN_FORCE,
        provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
        legal_review_status=LegalReviewStatus.LEGAL_EXPERT_APPROVED,  # Illegal self-approval!
    )

    result = gate.validate_record(doc)
    assert not result.is_valid
    assert "separate_human_review_status" in result.failed_checks
    assert any("Automated quality gate cannot self-approve" in iss for iss in result.issues)


def test_adv_11_repealed_statute_status_assigned_to_replacement_statute(gate_fixture):
    """Case 11: BNSS Section 531 provision mislabeled as repealed_with_savings."""
    gate, _ = gate_fixture
    doc = LegalQADocument(
        qa_id="QA-ADV-011",
        question="How does BNSS Section 531 govern pending cases?",
        answer="Section 531 is a savings clause.",
        supporting_source_ids=["IND-STAT-BNSS-2023"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-BNSS-2023",
                section_or_para_ref="Section 531(2)(a)",
                verbatim_text="531. Repeal and savings.-(1) The Code of Criminal Procedure, 1973 is hereby repealed.",
            )
        ],
        legal_domain="Criminal Procedure",
        statutory_citations=["Section 531, Bharatiya Nagarik Suraksha Sanhita, 2023"],
        legal_as_of_date=date(2026, 10, 16),
        commencement_source_id="IND-NOTIF-MHA-SO-848E-2024",
        commencement_date=date(2024, 7, 1),
        law_status_label=LawStatusLabel.REPEALED_WITH_SAVINGS,  # Error: conflating CrPC status with BNSS provision!
        provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
    )

    result = gate.validate_record(doc)
    assert not result.is_valid
    assert "section_level_commencement" in result.failed_checks
    assert any("Provision of BNSS 2023 cannot be labeled 'repealed' or 'repealed_with_savings'" in iss for iss in result.issues)


def test_adv_12_source_updated_after_legal_as_of_date_without_historical_version(gate_fixture):
    """Case 12: Source enacted after answer's legal-as-of date without a preserved historical version."""
    gate, _ = gate_fixture
    # Setting legal_as_of_date to 1 January 2023 (prior to BNSS enactment on 2023-12-25)
    doc = LegalQADocument(
        qa_id="QA-ADV-012",
        question="What was criminal procedure in January 2023 under BNSS?",
        answer="BNSS Section 482 governs anticipatory bail.",
        supporting_source_ids=["IND-STAT-BNSS-2023"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-BNSS-2023",
                section_or_para_ref="Section 482(1)",
                verbatim_text="When any person has reason to believe that he may be arrested on an accusation of having committed a non-bailable offence",
            )
        ],
        legal_domain="Criminal Procedure",
        statutory_citations=["Section 482, Bharatiya Nagarik Suraksha Sanhita, 2023"],
        legal_as_of_date=date(2023, 1, 1),  # Historical date before BNSS enactment!
        commencement_source_id="IND-NOTIF-MHA-SO-848E-2024",
        commencement_date=date(2024, 7, 1),
        law_status_label=LawStatusLabel.IN_FORCE,
        provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
    )

    result = gate.validate_record(doc)
    assert not result.is_valid
    assert "legal_as_of_date_consistency" in result.failed_checks
    assert any("is after the answer's legal-as-of date" in iss for iss in result.issues)
