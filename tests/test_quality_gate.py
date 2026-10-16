"""
Test suite for DataQualityGate.
Verifies pre-generation and pre-release gates:
1. Source authenticity
2. Section-level commencement
3. Exact evidence-span matching
4. Citation completeness
5. Quarantine exclusion
6. Duplicate detection
7. Legal-as-of date consistency
8. Separate human review status
"""

import json
from pathlib import Path
from datetime import date
import pytest

from legalmitra.core.enums import (
    LawStatusLabel,
    LegalReviewStatus,
    ProvisionCommencementStatus,
)
from legalmitra.generation.orchestrator import GenerationOrchestrator
from legalmitra.generation.schemas import GenerationConfig
from legalmitra.ingestion.registry import SourceRegistryManager
from legalmitra.schemas.legal_qa import EvidencePassage, LegalQADocument
from legalmitra.validation.quality_gate import DataQualityGate


@pytest.fixture
def source_context():
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
    return gate


def test_pilot_20_all_pass_quality_gate(source_context):
    gate = source_context
    examples_file = Path("data/03_generated/pilot_20_examples.jsonl")
    assert examples_file.exists()

    docs = []
    with open(examples_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                docs.append(LegalQADocument(**json.loads(line)))

    assert len(docs) == 20
    all_passed, results = gate.validate_batch(docs)

    for idx, r in enumerate(results, 1):
        assert r.is_valid, f"Pilot record {idx} ({r.qa_id}) failed quality gate checks: {r.issues}"
        assert len(r.passed_checks) == 8
        assert len(r.failed_checks) == 0

    assert all_passed is True


def test_quality_gate_rejects_quarantined_scaffold(source_context):
    gate = source_context
    doc = LegalQADocument(
        qa_id="QA-TEST-QUARANTINE-001",
        question="Can anticipatory bail be filed by the State under Section 482 of BNSS?",
        answer="In State v. Rahul Kumar, anticipatory bail was examined.",
        supporting_source_ids=["IND-JUD-DEL-2024-BAIL"],  # Quarantined!
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

    result = gate.validate_record(doc)
    assert not result.is_valid
    assert "quarantine_exclusion" in result.failed_checks
    assert any("quarantined" in iss.lower() for iss in result.issues)


def test_quality_gate_rejects_automated_self_approval(source_context):
    gate = source_context
    doc = LegalQADocument(
        qa_id="QA-TEST-SELF-APPROVE-001",
        question="What is the definition of data under the Information Technology Act, 2000?",
        answer="Section 2(1)(o) defines data.",
        supporting_source_ids=["IND-STAT-IT-2000"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-IT-2000",
                section_or_para_ref="Section 2(1)(o)",
                verbatim_text="data means a representation of information",
            )
        ],
        legal_domain="Cyber Law",
        statutory_citations=["Section 2(1)(o), Information Technology Act, 2000"],
        legal_as_of_date=date(2026, 10, 16),
        commencement_source_id="IND-NOTIF-MEITY-2000",
        commencement_date=date(2000, 10, 17),
        law_status_label=LawStatusLabel.IN_FORCE,
        provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
        legal_review_status=LegalReviewStatus.LEGAL_EXPERT_APPROVED,  # Illegal self-approval!
    )

    result = gate.validate_record(doc)
    assert not result.is_valid
    assert "separate_human_review_status" in result.failed_checks
    assert any("cannot self-approve" in iss.lower() for iss in result.issues)


def test_quality_gate_rejects_duplicate_records(source_context):
    gate = source_context
    doc1 = LegalQADocument(
        qa_id="QA-TEST-DUP-001",
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
        qa_id="QA-TEST-DUP-002",
        question="  what IS electronic evidence under BSA Section 61?  ",  # Duplicate question
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
        legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
    )

    all_passed, results = gate.validate_batch([doc1, doc2])
    assert not all_passed
    assert results[0].is_valid is True
    assert results[1].is_valid is False
    assert "duplicate_detection" in results[1].failed_checks


def test_quality_gate_rejects_bnss_conflation(source_context):
    gate = source_context
    doc = LegalQADocument(
        qa_id="QA-TEST-CONFLATE-001",
        question="How does BNSS Section 531 deal with prior criminal proceedings?",
        answer="Section 531 repeals the CrPC with savings.",
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
        law_status_label=LawStatusLabel.REPEALED_WITH_SAVINGS,  # BNSS provision mistakenly labeled repealed!
        provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
    )

    result = gate.validate_record(doc)
    assert not result.is_valid
    assert "section_level_commencement" in result.failed_checks
    assert any("Provision of BNSS 2023 cannot be labeled 'repealed'" in iss for iss in result.issues)

