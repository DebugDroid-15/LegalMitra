"""
Test suite for Phase 12 Advocate Review Pipeline and Controlled Dataset Expansion.
Verifies:
1. Extended review status enums (NEEDS_MORE_EVIDENCE, DEFERRED).
2. ReviewImporter atomic rollback and decision validation.
3. Batch 0 validation integrity.
4. Batch 1 candidate dataset integrity, quality gates, and blank review sheet.
5. Absolute preservation of the frozen Phase 9 pilot snapshot.
"""

import csv
import json
from pathlib import Path
import pytest

from legalmitra.core.enums import LegalReviewStatus
from legalmitra.core.hashing import compute_file_sha256
from legalmitra.review.import_review import ReviewImporter, ReviewImportError
from legalmitra.schemas.legal_qa import LegalQADocument


def test_phase12_review_status_enums():
    """Verify new enums are present in LegalReviewStatus."""
    assert LegalReviewStatus.NEEDS_MORE_EVIDENCE.value == "needs_more_evidence"
    assert LegalReviewStatus.DEFERRED.value == "deferred"
    assert LegalReviewStatus.PENDING_LEGAL_REVIEW.value == "pending_legal_review"
    assert LegalReviewStatus.LEGAL_EXPERT_APPROVED.value == "legal_expert_approved"
    assert LegalReviewStatus.LEGAL_EXPERT_REJECTED.value == "legal_expert_rejected"


def test_phase12_review_importer_atomic_rollback(tmp_path):
    """Test that invalid decision in CSV triggers atomic rollback without mutating dataset."""
    from legalmitra.schemas.legal_qa import EvidencePassage
    sample_doc = LegalQADocument(
        qa_id="QA-TEST-001",
        question="Test question?",
        answer="Test answer under Section 1.",
        supporting_source_ids=["IND-STAT-IT-2000"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-IT-2000",
                section_or_para_ref="Section 1",
                verbatim_text="Short title, extent and commencement.-",
            )
        ],
        statutory_citations=["Section 1, Information Technology Act, 2000"],
        legal_domain="Cyber Law",
        legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
    )
    test_jsonl = tmp_path / "candidates.jsonl"
    with open(test_jsonl, "w", encoding="utf-8") as f:
        f.write(sample_doc.model_dump_json() + "\n")

    # CSV with invalid decision
    bad_csv = tmp_path / "reviews.csv"
    with open(bad_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["record_id", "review_decision", "reviewer_comments"])
        writer.writeheader()
        writer.writerow({
            "record_id": "QA-TEST-001",
            "review_decision": "UNAUTHORIZED_DECISION",
            "reviewer_comments": "Testing rollback",
        })

    importer = ReviewImporter(audit_dir=tmp_path / "audit")
    with pytest.raises(ReviewImportError):
        importer.import_reviews(bad_csv, test_jsonl)

    # Verify JSONL remained unchanged
    with open(test_jsonl, "r", encoding="utf-8") as f:
        doc = LegalQADocument(**json.loads(f.readline()))
        assert doc.legal_review_status == LegalReviewStatus.PENDING_LEGAL_REVIEW


def test_phase12_batch_00_integrity():
    """Verify Batch 0 validation batch files exist and are strictly pending review."""
    batch_file = Path("data/07_batches/batch_00_validation/batch_00_examples.jsonl")
    assert batch_file.exists(), "Batch 0 examples file must exist"

    docs = []
    with open(batch_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                docs.append(LegalQADocument(**json.loads(line)))

    assert len(docs) == 3
    for doc in docs:
        assert doc.legal_review_status == LegalReviewStatus.PENDING_LEGAL_REVIEW


def test_phase12_batch_01_candidate_dataset():
    """Verify Batch 1 candidates exist, have exact count of 20, and pass schema rules."""
    batch_file = Path("data/07_batches/batch_01_candidates/batch_01_examples.jsonl")
    manifest_file = Path("data/07_batches/batch_01_candidates/batch_01_manifest.json")
    review_sheet = Path("data/07_batches/review/batch_01_review_sheet.csv")

    assert batch_file.exists(), "Batch 1 candidates file must exist"
    assert manifest_file.exists(), "Batch 1 manifest file must exist"
    assert review_sheet.exists(), "Batch 1 review sheet must exist"

    # Check manifest SHA-256
    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    assert manifest["total_records"] == 20
    assert manifest["sha256"] == compute_file_sha256(batch_file)
    assert manifest["quarantine_compliance"]["IND-JUD-DEL-2024-BAIL_excluded"] is True

    # Check candidates
    docs = []
    with open(batch_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                docs.append(LegalQADocument(**json.loads(line)))

    assert len(docs) == 20
    for doc in docs:
        assert doc.legal_review_status == LegalReviewStatus.PENDING_LEGAL_REVIEW
        assert len(doc.statutory_citations) > 0
        assert len(doc.evidence_passages) > 0
        # Check quarantine
        assert "IND-JUD-DEL-2024-BAIL" not in doc.supporting_source_ids
        for passage in doc.evidence_passages:
            assert passage.source_id != "IND-JUD-DEL-2024-BAIL"
        combined = f"{doc.question} {doc.answer}".lower()
        assert "rahul kumar" not in combined

    # Check review sheet blank fields
    with open(review_sheet, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 20
    for row in rows:
        assert row["review_decision"] == "", "Decision must be blank initially"
        assert row["legal_accuracy_score_1_to_5"] == ""
        assert row["reviewer_name_initials"] == ""


def test_phase12_freeze_preservation():
    """Verify that Phase 9 review snapshot remains 100% identical to SHA-256 manifest."""
    manifest_path = Path("data/06_review/PHASE9_REVIEW_SNAPSHOT_MANIFEST.json")
    assert manifest_path.exists()

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    for item in manifest["frozen_artifacts"].values():
        filepath = Path(item["path"])
        assert filepath.exists(), f"Frozen artifact {filepath} missing"
        computed_hash = compute_file_sha256(filepath)
        assert computed_hash == item["sha256"], f"SHA256 mismatch for {filepath}"
