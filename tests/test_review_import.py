"""
Test suite for Advocate Review Import Workflow.
Verifies:
1. Valid import of APPROVED, REVISION_REQUIRED, and REJECTED decisions.
2. Enforcement of mandatory comments for REVISION_REQUIRED and REJECTED.
3. Strict rejection of unknown/invalid decisions.
4. Non-inference of approval from blank fields.
5. Preservation of original record snapshot in immutable audit ledger.
6. Atomic failure (no partial modifications on invalid import).
7. Separation of automated validation status from human legal review status.
"""

import csv
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
from legalmitra.review.import_review import ReviewImporter, ReviewImportError
from legalmitra.schemas.legal_qa import EvidencePassage, LegalQADocument


@pytest.fixture
def sample_dataset(tmp_path):
    dataset_file = tmp_path / "test_dataset.jsonl"
    doc1 = LegalQADocument(
        qa_id="QA-TEST-001",
        question="What is the scope of Section 11 of DPDP Act, 2023?",
        answer="Under Section 11, a Data Principal may request access.",
        supporting_source_ids=["IND-STAT-DPDP-2023"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-DPDP-2023",
                section_or_para_ref="Section 11(1)",
                verbatim_text="11. Right to access information about personal data",
            )
        ],
        legal_domain="Data Protection",
        statutory_citations=["Section 11, Digital Personal Data Protection Act, 2023"],
        legal_as_of_date=date(2026, 10, 16),
        commencement_source_id="IND-NOTIF-MEITY-GSR-843E-2025",
        commencement_date=date(2027, 5, 13),
        law_status_label=LawStatusLabel.ENACTED_NOT_YET_IN_FORCE,
        provision_commencement_status=ProvisionCommencementStatus.UNCOMMENCED,
        temporal_validation_status=TemporalValidationStatus.VERIFIED_FUTURE_COMMENCEMENT,
        legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
    )
    doc2 = LegalQADocument(
        qa_id="QA-TEST-002",
        question="What is electronic evidence under BSA Section 61?",
        answer="Section 61 provides for admissibility.",
        supporting_source_ids=["IND-STAT-BSA-2023-SEC61"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-BSA-2023-SEC61",
                section_or_para_ref="Section 61",
                verbatim_text="Nothing in this Adhiniyam shall apply to deny the admissibility",
            )
        ],
        legal_domain="Evidence Law",
        statutory_citations=["Section 61, Bharatiya Sakshya Adhiniyam, 2023"],
        legal_as_of_date=date(2026, 10, 16),
        commencement_source_id="IND-NOTIF-MHA-SO-849E-2024",
        commencement_date=date(2024, 7, 1),
        law_status_label=LawStatusLabel.IN_FORCE,
        provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
        temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
        legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
    )

    with open(dataset_file, "w", encoding="utf-8") as f:
        f.write(doc1.model_dump_json() + "\n")
        f.write(doc2.model_dump_json() + "\n")

    return dataset_file


def test_import_valid_advocate_reviews(tmp_path, sample_dataset):
    audit_dir = tmp_path / "audit"
    importer = ReviewImporter(audit_dir=audit_dir)

    csv_path = tmp_path / "reviews.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "record_id", "review_decision", "legal_accuracy_score_1_to_5",
            "temporal_accuracy_score_1_to_5", "grounding_accuracy_score_1_to_5",
            "reviewer_comments", "reviewer_name_initials", "review_date"
        ])
        writer.writeheader()
        writer.writerow({
            "record_id": "QA-TEST-001",
            "review_decision": "APPROVED",
            "legal_accuracy_score_1_to_5": "5",
            "temporal_accuracy_score_1_to_5": "5",
            "grounding_accuracy_score_1_to_5": "5",
            "reviewer_comments": "Statutorily precise and accurately notes uncommenced status under G.S.R. 843(E).",
            "reviewer_name_initials": "Adv. R.K. Sharma",
            "review_date": "2026-10-16",
        })
        writer.writerow({
            "record_id": "QA-TEST-002",
            "review_decision": "REVISION_REQUIRED",
            "legal_accuracy_score_1_to_5": "3",
            "temporal_accuracy_score_1_to_5": "4",
            "grounding_accuracy_score_1_to_5": "4",
            "reviewer_comments": "Please explicitly reference the proviso to Section 61 requiring Section 63(4) certificate.",
            "reviewer_name_initials": "Adv. R.K. Sharma",
            "review_date": "2026-10-16",
        })

    out_file = tmp_path / "updated_dataset.jsonl"
    updated_docs, summary = importer.import_reviews(csv_path, sample_dataset, output_path=out_file)

    assert summary.records_updated == 2
    assert summary.approved_count == 1
    assert summary.revision_required_count == 1
    assert summary.rejected_count == 0

    assert updated_docs[0].legal_review_status == LegalReviewStatus.LEGAL_EXPERT_APPROVED
    assert updated_docs[0].reviewer_name_initials == "Adv. R.K. Sharma"
    assert updated_docs[0].temporal_validation_status == TemporalValidationStatus.VERIFIED_FUTURE_COMMENCEMENT

    assert updated_docs[1].legal_review_status == LegalReviewStatus.REVISION_REQUIRED
    assert "Section 63(4)" in updated_docs[1].reviewer_comments

    # Audit log check
    audit_file = Path(summary.audit_log_path)
    assert audit_file.exists()
    lines = audit_file.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 2
    entry0 = json.loads(lines[0])
    assert entry0["decision"] == "APPROVED"
    assert entry0["original_record_snapshot"]["legal_review_status"] == "pending_legal_review"


def test_import_blank_decision_retains_pending(tmp_path, sample_dataset):
    audit_dir = tmp_path / "audit"
    importer = ReviewImporter(audit_dir=audit_dir)

    csv_path = tmp_path / "reviews_blank.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["record_id", "review_decision", "reviewer_comments"])
        writer.writeheader()
        writer.writerow({
            "record_id": "QA-TEST-001",
            "review_decision": "",  # Blank: MUST NOT infer approval!
            "reviewer_comments": "",
        })
        writer.writerow({
            "record_id": "QA-TEST-002",
            "review_decision": "REJECTED",
            "reviewer_comments": "Incorrect legal characterization.",
        })

    out_file = tmp_path / "updated_dataset.jsonl"
    updated_docs, summary = importer.import_reviews(csv_path, sample_dataset, output_path=out_file)

    assert summary.records_updated == 1
    assert summary.pending_count == 1
    assert summary.rejected_count == 1
    assert updated_docs[0].legal_review_status == LegalReviewStatus.PENDING_LEGAL_REVIEW
    assert updated_docs[1].legal_review_status == LegalReviewStatus.LEGAL_EXPERT_REJECTED


def test_import_rejects_missing_comment_for_rejection(tmp_path, sample_dataset):
    audit_dir = tmp_path / "audit"
    importer = ReviewImporter(audit_dir=audit_dir)

    csv_path = tmp_path / "reviews_no_comment.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["record_id", "review_decision", "reviewer_comments"])
        writer.writeheader()
        writer.writerow({
            "record_id": "QA-TEST-001",
            "review_decision": "REJECTED",
            "reviewer_comments": "",  # Missing mandatory comment!
        })

    with pytest.raises(ReviewImportError) as exc_info:
        importer.import_reviews(csv_path, sample_dataset)

    assert "Reviewer comment is mandatory for 'REJECTED' decisions" in str(exc_info.value)


def test_import_atomic_rejection_on_unknown_record(tmp_path, sample_dataset):
    audit_dir = tmp_path / "audit"
    importer = ReviewImporter(audit_dir=audit_dir)

    csv_path = tmp_path / "reviews_bad_record.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["record_id", "review_decision", "reviewer_comments"])
        writer.writeheader()
        writer.writerow({
            "record_id": "QA-TEST-001",
            "review_decision": "APPROVED",
            "reviewer_comments": "Good",
        })
        writer.writerow({
            "record_id": "QA-NONEXISTENT-999",  # Unknown record!
            "review_decision": "APPROVED",
            "reviewer_comments": "Good",
        })

    # Dataset file must not be modified if any row fails validation
    orig_content = sample_dataset.read_text(encoding="utf-8")
    with pytest.raises(ReviewImportError) as exc_info:
        importer.import_reviews(csv_path, sample_dataset)

    assert "does not exist in target dataset" in str(exc_info.value)
    assert sample_dataset.read_text(encoding="utf-8") == orig_content, "Atomic failure violated"


def test_import_rejects_invalid_decision_enum(tmp_path, sample_dataset):
    audit_dir = tmp_path / "audit"
    importer = ReviewImporter(audit_dir=audit_dir)

    csv_path = tmp_path / "reviews_invalid_enum.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["record_id", "review_decision", "reviewer_comments"])
        writer.writeheader()
        writer.writerow({
            "record_id": "QA-TEST-001",
            "review_decision": "ACCEPTED_BY_ALGORITHM",  # Invalid!
            "reviewer_comments": "None",
        })

    with pytest.raises(ReviewImportError) as exc_info:
        importer.import_reviews(csv_path, sample_dataset)

    assert "Invalid review_decision 'ACCEPTED_BY_ALGORITHM'" in str(exc_info.value)

