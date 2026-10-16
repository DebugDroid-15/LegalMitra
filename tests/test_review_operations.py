"""
Test suite for Phase 13 Advocate Review Operations and Boundary Protection.
Verifies:
1. Review-sheet schema validation.
2. Unknown example IDs rejection.
3. Duplicate and conflicting review decisions.
4. Missing comments on non-approval decisions.
5. Score bounds and date format validation.
6. Strict reviewer attribution validation.
7. Attempted overwrite protection on already-decided records.
8. Transactional rollback after invalid record (preserving candidate source data).
9. Correct training eligibility filtering (0 eligible when pending).
10. Quarantine exclusion (scaffold rejection).
11. Evaluation-partition leakage prevention (frozen pilot blocked from training).
12. Review package integrity verification & frozen pilot hash preservation.
"""

import csv
import json
from datetime import date
from pathlib import Path
import pytest

from legalmitra.core.enums import LawStatusLabel, LegalReviewStatus, ProvisionCommencementStatus, TemporalValidationStatus
from legalmitra.core.hashing import compute_file_sha256
from legalmitra.review.eligibility import DatasetEligibilityFilter
from legalmitra.review.import_review import ReviewImporter, ReviewImportError
from legalmitra.review.tracker import ReviewTracker
from legalmitra.schemas.legal_qa import EvidencePassage, LegalQADocument


@pytest.fixture
def mock_candidates_dataset(tmp_path):
    dataset_file = tmp_path / "test_candidates.jsonl"
    doc1 = LegalQADocument(
        qa_id="QA-TEST-OP-001",
        question="What is the legal requirement for notice under DPDP Section 5?",
        answer="Under Section 5, notice must precede consent.",
        supporting_source_ids=["IND-STAT-DPDP-2023"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-DPDP-2023",
                section_or_para_ref="Section 5(1)",
                verbatim_text="5. Notice.-(1) Every request made to a Data Principal under section 6",
            )
        ],
        statutory_citations=["Section 5(1), Digital Personal Data Protection Act, 2023"],
        legal_domain="Data Protection",
        legal_as_of_date=date(2026, 10, 16),
        commencement_source_id="IND-NOTIF-MEITY-GSR-843E-2025",
        commencement_date=date(2027, 5, 13),
        law_status_label=LawStatusLabel.ENACTED_NOT_YET_IN_FORCE,
        provision_commencement_status=ProvisionCommencementStatus.UNCOMMENCED,
        temporal_validation_status=TemporalValidationStatus.VERIFIED_FUTURE_COMMENCEMENT,
        legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
    )
    doc2 = LegalQADocument(
        qa_id="QA-TEST-OP-002",
        question="What is the admissibility of electronic records under BSA Section 61?",
        answer="Under Section 61, electronic records are admissible subject to Section 63.",
        supporting_source_ids=["IND-STAT-BSA-2023-SEC61"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-BSA-2023-SEC61",
                section_or_para_ref="Section 61",
                verbatim_text="Nothing in this Adhiniyam shall apply to deny the admissibility of an electronic or digital record in the evidence",
            )
        ],
        statutory_citations=["Section 61, Bharatiya Sakshya Adhiniyam, 2023"],
        legal_domain="Evidence Law",
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


def test_review_sheet_schema_validation_success(tmp_path, mock_candidates_dataset):
    importer = ReviewImporter(audit_dir=tmp_path / "audit")
    csv_file = tmp_path / "valid_review.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "record_id", "review_decision", "legal_accuracy_score_1_to_5",
            "temporal_accuracy_score_1_to_5", "grounding_accuracy_score_1_to_5",
            "reviewer_comments", "reviewer_name_initials", "review_date"
        ])
        writer.writeheader()
        writer.writerow({
            "record_id": "QA-TEST-OP-001",
            "review_decision": "APPROVED",
            "legal_accuracy_score_1_to_5": "5",
            "temporal_accuracy_score_1_to_5": "5",
            "grounding_accuracy_score_1_to_5": "5",
            "reviewer_comments": "Legally accurate.",
            "reviewer_name_initials": "Adv. AB",
            "review_date": "2026-10-16",
        })
        writer.writerow({
            "record_id": "QA-TEST-OP-002",
            "review_decision": "REVISION_REQUIRED",
            "legal_accuracy_score_1_to_5": "4",
            "temporal_accuracy_score_1_to_5": "4",
            "grounding_accuracy_score_1_to_5": "4",
            "reviewer_comments": "Explicitly cite Section 63(4) certificate proviso.",
            "reviewer_name_initials": "Adv. AB",
            "review_date": "2026-10-16",
        })

    report = importer.generate_validation_report(csv_file, mock_candidates_dataset)
    assert report.is_valid is True
    assert report.decisions_count == 2
    assert report.pending_count == 0
    assert len(report.errors) == 0


def test_review_sheet_unknown_example_id_rejected(tmp_path, mock_candidates_dataset):
    importer = ReviewImporter(audit_dir=tmp_path / "audit")
    csv_file = tmp_path / "unknown_id_review.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["record_id", "review_decision"])
        writer.writeheader()
        writer.writerow({"record_id": "QA-UNKNOWN-999", "review_decision": "APPROVED"})

    report = importer.generate_validation_report(csv_file, mock_candidates_dataset)
    assert report.is_valid is False
    assert any("does not exist in target dataset" in err for err in report.errors)


def test_review_sheet_duplicate_id_rejected(tmp_path, mock_candidates_dataset):
    importer = ReviewImporter(audit_dir=tmp_path / "audit")
    csv_file = tmp_path / "dup_id_review.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["record_id", "review_decision"])
        writer.writeheader()
        writer.writerow({"record_id": "QA-TEST-OP-001", "review_decision": "APPROVED"})
        writer.writerow({"record_id": "QA-TEST-OP-001", "review_decision": "REJECTED"})

    report = importer.generate_validation_report(csv_file, mock_candidates_dataset)
    assert report.is_valid is False
    assert any("Duplicate record_id 'QA-TEST-OP-001'" in err for err in report.errors)


def test_review_sheet_missing_comment_on_non_approval_rejected(tmp_path, mock_candidates_dataset):
    importer = ReviewImporter(audit_dir=tmp_path / "audit")
    for bad_decision in ("REVISION_REQUIRED", "REJECTED", "NEEDS_MORE_EVIDENCE", "DEFERRED"):
        csv_file = tmp_path / f"no_comment_{bad_decision}.csv"
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["record_id", "review_decision", "reviewer_comments"])
            writer.writeheader()
            writer.writerow({"record_id": "QA-TEST-OP-001", "review_decision": bad_decision, "reviewer_comments": ""})

        report = importer.generate_validation_report(csv_file, mock_candidates_dataset)
        assert report.is_valid is False
        assert any("Reviewer comment is mandatory" in err for err in report.errors)


def test_review_sheet_score_bounds_and_date_validation(tmp_path, mock_candidates_dataset):
    importer = ReviewImporter(audit_dir=tmp_path / "audit")
    csv_file = tmp_path / "bad_scores.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "record_id", "review_decision", "legal_accuracy_score_1_to_5", "review_date"
        ])
        writer.writeheader()
        writer.writerow({
            "record_id": "QA-TEST-OP-001",
            "review_decision": "APPROVED",
            "legal_accuracy_score_1_to_5": "6",  # Out of bounds (>5)
            "review_date": "16-10-2026",        # Bad format (not YYYY-MM-DD)
        })

    report = importer.generate_validation_report(csv_file, mock_candidates_dataset)
    assert report.is_valid is False
    assert any("must be between 1 and 5" in err for err in report.errors)
    assert any("Invalid date format" in err for err in report.errors)


def test_review_sheet_strict_attribution_enforcement(tmp_path, mock_candidates_dataset):
    importer = ReviewImporter(audit_dir=tmp_path / "audit")
    csv_file = tmp_path / "missing_attrib.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "record_id", "review_decision", "reviewer_name_initials", "review_date"
        ])
        writer.writeheader()
        writer.writerow({
            "record_id": "QA-TEST-OP-001",
            "review_decision": "APPROVED",
            "reviewer_name_initials": "",  # Missing
            "review_date": "",             # Missing
        })

    # Non-strict passes
    report_lax = importer.generate_validation_report(csv_file, mock_candidates_dataset, strict_attribution=False)
    assert report_lax.is_valid is True

    # Strict fails
    report_strict = importer.generate_validation_report(csv_file, mock_candidates_dataset, strict_attribution=True)
    assert report_strict.is_valid is False
    assert any("Reviewer initials or name is required" in err for err in report_strict.errors)


def test_attempted_overwrite_protection(tmp_path, mock_candidates_dataset):
    importer = ReviewImporter(audit_dir=tmp_path / "audit")

    # First import an approval
    first_csv = tmp_path / "first_review.csv"
    with open(first_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["record_id", "review_decision", "reviewer_name_initials", "review_date"])
        writer.writeheader()
        writer.writerow({
            "record_id": "QA-TEST-OP-001",
            "review_decision": "APPROVED",
            "reviewer_name_initials": "Adv. X",
            "review_date": "2026-10-16",
        })

    importer.import_reviews(first_csv, mock_candidates_dataset)

    # Now attempt to overwrite QA-TEST-OP-001 with REJECTED
    second_csv = tmp_path / "second_review.csv"
    with open(second_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["record_id", "review_decision", "reviewer_comments"])
        writer.writeheader()
        writer.writerow({
            "record_id": "QA-TEST-OP-001",
            "review_decision": "REJECTED",
            "reviewer_comments": "Attempted overwrite test.",
        })

    # Default allow_overwrite=False MUST reject
    with pytest.raises(ReviewImportError) as exc_info:
        importer.import_reviews(second_csv, mock_candidates_dataset, allow_overwrite=False)
    assert "Cannot overwrite already decided status" in str(exc_info.value)

    # With allow_overwrite=True, import succeeds
    docs, summary = importer.import_reviews(second_csv, mock_candidates_dataset, allow_overwrite=True)
    assert docs[0].legal_review_status == LegalReviewStatus.LEGAL_EXPERT_REJECTED
    assert summary.rejected_count == 1


def test_transactional_rollback_preserves_candidate_file(tmp_path, mock_candidates_dataset):
    importer = ReviewImporter(audit_dir=tmp_path / "audit")
    original_hash = compute_file_sha256(mock_candidates_dataset)

    # CSV with 1 valid row and 1 invalid row (missing comment for rejection)
    mixed_csv = tmp_path / "mixed_review.csv"
    with open(mixed_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["record_id", "review_decision", "reviewer_comments"])
        writer.writeheader()
        writer.writerow({
            "record_id": "QA-TEST-OP-001",
            "review_decision": "APPROVED",
            "reviewer_comments": "Valid approval.",
        })
        writer.writerow({
            "record_id": "QA-TEST-OP-002",
            "review_decision": "REJECTED",
            "reviewer_comments": "",  # Missing mandatory comment!
        })

    with pytest.raises(ReviewImportError):
        importer.import_reviews(mixed_csv, mock_candidates_dataset)

    # Verify candidate dataset file is bitwise untouched
    after_hash = compute_file_sha256(mock_candidates_dataset)
    assert after_hash == original_hash, "Transactional rollback failed: candidate dataset was modified on error!"


def test_dataset_eligibility_filtering():
    """Verify that only approved, non-holdout, non-quarantined records are training-eligible."""
    filter_engine = DatasetEligibilityFilter()

    # 1. Pending record -> Ineligible
    doc_pending = LegalQADocument(
        qa_id="QA-EXP-001",
        question="What is the title and extent of the Information Technology Act, 2000?",
        answer="Under Section 1, this Act may be called the Information Technology Act, 2000.",
        supporting_source_ids=["IND-STAT-IT-2000"],
        evidence_passages=[EvidencePassage(source_id="IND-STAT-IT-2000", section_or_para_ref="s.1", verbatim_text="text")],
        statutory_citations=["Section 1, Information Technology Act, 2000"],
        legal_domain="Cyber Law",
        legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
    )
    is_elig, reasons = filter_engine.evaluate_record_eligibility(doc_pending)
    assert is_elig is False
    assert any("only 'legal_expert_approved' records are eligible" in r for r in reasons)

    # 2. Approved record from Holdout Evaluation Partition (Pilot 20) -> Ineligible (Leakage Protection)
    doc_pilot_approved = LegalQADocument(
        qa_id="QA-PILOT-DPDP-001",
        question="What is the right of a Data Principal under Section 11 of DPDP Act, 2023?",
        answer="Under Section 11, a Data Principal has the right to access personal data.",
        supporting_source_ids=["IND-STAT-DPDP-2023"],
        evidence_passages=[EvidencePassage(source_id="IND-STAT-DPDP-2023", section_or_para_ref="s.11", verbatim_text="text")],
        statutory_citations=["Section 11, Digital Personal Data Protection Act, 2023"],
        legal_domain="Data Protection",
        legal_review_status=LegalReviewStatus.LEGAL_EXPERT_APPROVED,
        reviewer_name_initials="Adv. Test",
        review_date=date(2026, 10, 16),
    )
    is_elig_pilot, reasons_pilot = filter_engine.evaluate_record_eligibility(doc_pilot_approved)
    assert is_elig_pilot is False
    assert any("permanent blind holdout evaluation partition" in r for r in reasons_pilot)

    # 3. Approved record citing Quarantined Scaffold -> Ineligible
    doc_quarantine_approved = LegalQADocument(
        qa_id="QA-EXP-002",
        question="What are the anticipatory bail principles under BNSS Section 482?",
        answer="Under Section 482, the High Court or Sessions Court may grant anticipatory bail.",
        supporting_source_ids=["IND-JUD-DEL-2024-BAIL"],
        evidence_passages=[EvidencePassage(source_id="IND-JUD-DEL-2024-BAIL", section_or_para_ref="para 1", verbatim_text="text")],
        statutory_citations=["Section 482, Bharatiya Nagarik Suraksha Sanhita, 2023"],
        legal_domain="Criminal Procedure",
        legal_review_status=LegalReviewStatus.LEGAL_EXPERT_APPROVED,
        reviewer_name_initials="Adv. Test",
        review_date=date(2026, 10, 16),
    )
    is_elig_quar, reasons_quar = filter_engine.evaluate_record_eligibility(doc_quarantine_approved)
    assert is_elig_quar is False
    assert any("relies on quarantined source ID" in r for r in reasons_quar)

    # 4. Approved expansion candidate with valid attribution -> Eligible!
    doc_valid_approved = LegalQADocument(
        qa_id="QA-BATCH1-001",
        question="What are the lawful grounds for processing personal data under DPDP Act Section 4?",
        answer="Under Section 4, personal data may only be processed for lawful purpose with consent or legitimate use.",
        supporting_source_ids=["IND-STAT-DPDP-2023"],
        evidence_passages=[EvidencePassage(source_id="IND-STAT-DPDP-2023", section_or_para_ref="s.4", verbatim_text="text")],
        statutory_citations=["Section 4, Digital Personal Data Protection Act, 2023"],
        legal_domain="Data Protection",
        legal_review_status=LegalReviewStatus.LEGAL_EXPERT_APPROVED,
        reviewer_name_initials="Adv. Verified",
        review_date=date(2026, 10, 16),
    )
    is_elig_ok, reasons_ok = filter_engine.evaluate_record_eligibility(doc_valid_approved)
    assert is_elig_ok is True
    assert len(reasons_ok) == 0


def test_review_package_verification_scripts():
    """Verify verify_review_packages.py functions directly."""
    from scripts.verify_review_packages import verify_package_a, verify_package_b, verify_review_tracker
    assert verify_package_a() is True
    assert verify_package_b() is True
    assert verify_review_tracker() is True


def test_review_tracker_operations(tmp_path):
    """Test ReviewTracker lifecycle dispatch, receipt, and status updates."""
    tracker_file = tmp_path / "tracker.json"
    tracker = ReviewTracker(register_path=tracker_file)

    # Initialize from actual datasets
    count = tracker.initialize_from_datasets()
    assert count == 40
    assert len(tracker.entries) == 40

    # Dispatch simulation
    sample_ids = ["QA-BATCH1-001", "QA-BATCH1-002"]
    updated_dispatch = tracker.update_dispatch(sample_ids, "2026-10-16", recipient_tag="ADVOCATE_PANEL_A")
    assert updated_dispatch == 2
    assert tracker.entries["QA-BATCH1-001"].sent_to_advocate is True
    assert tracker.entries["QA-BATCH1-001"].advocate_recipient_tag == "ADVOCATE_PANEL_A"

    # Receipt simulation
    updated_receipt = tracker.update_receipt(sample_ids, "2026-10-17", validation_passed=True, validation_report_ref="VAL-REPORT-001")
    assert updated_receipt == 2
    assert tracker.entries["QA-BATCH1-001"].response_received is True
    assert tracker.entries["QA-BATCH1-001"].validation_passed is True

    # Import simulation
    status_map = {"QA-BATCH1-001": "legal_expert_approved", "QA-BATCH1-002": "revision_required"}
    updated_imported = tracker.update_imported(sample_ids, "AUDIT-LOG-001", new_status_map=status_map)
    assert updated_imported == 2
    assert tracker.entries["QA-BATCH1-001"].imported is True
    assert tracker.entries["QA-BATCH1-001"].review_status == "legal_expert_approved"
    assert tracker.entries["QA-BATCH1-002"].review_status == "revision_required"
