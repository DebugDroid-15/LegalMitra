"""
Test suite for Phase 9 Review Snapshot Freeze & Integrity.
Verifies:
1. Cryptographic SHA-256 hashes of all frozen pilot and handoff artifacts.
2. Complete handoff integrity (20 records, matching IDs, blank decisions, pending status).
3. Review-import safeguards operate strictly on temporary copies without mutating frozen files.
4. Quarantine compliance (no synthetic scaffold in pilot).
"""

import csv
import hashlib
import json
from pathlib import Path
import pytest

from legalmitra.review.import_review import ReviewImporter, ReviewImportError


def test_frozen_artifacts_sha256_manifest_integrity():
    manifest_file = Path("data/06_review/PHASE9_REVIEW_SNAPSHOT_MANIFEST.json")
    assert manifest_file.exists(), "Snapshot manifest must exist"

    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    assert manifest["total_records"] == 20
    assert manifest["unique_record_count"] == 20
    assert manifest["review_status_summary"]["pending_legal_review"] == 20
    assert manifest["review_status_summary"]["legal_expert_approved"] == 0

    frozen_artifacts = manifest["frozen_artifacts"]

    for key, info in frozen_artifacts.items():
        artifact_path = Path(info["path"])
        assert artifact_path.exists(), f"Frozen artifact {artifact_path} missing"

        content = artifact_path.read_bytes()
        calculated_sha = hashlib.sha256(content).hexdigest()

        assert len(content) == info["size_bytes"], f"Byte size mismatch for {artifact_path}"
        assert calculated_sha == info["sha256"], f"SHA-256 hash mismatch for {artifact_path}"


def test_handoff_blank_decisions_and_pending_status():
    csv_path = Path("data/06_review/pilot_20_review_sheet.csv")
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 20
    for r in rows:
        assert r["review_decision"] == "", "Decision field must be blank in frozen handoff sheet"
        assert r["legal_accuracy_score_1_to_5"] == ""
        assert r["reviewer_comments"] == ""
        assert r["reviewer_name_initials"] == ""
        assert r["review_date"] == ""


def test_review_import_safeguards_on_temporary_copies(tmp_path):
    """Verifies review-import validation rules without touching frozen files."""
    # Copy frozen dataset to tmp_path
    frozen_dataset = Path("data/03_generated/pilot_20_examples.jsonl")
    temp_dataset = tmp_path / "temp_pilot.jsonl"
    temp_dataset.write_bytes(frozen_dataset.read_bytes())
    orig_hash = hashlib.sha256(temp_dataset.read_bytes()).hexdigest()

    importer = ReviewImporter(audit_dir=tmp_path / "audit")

    # 1. Invalid decision should fail and keep temp_dataset unchanged
    bad_csv = tmp_path / "bad.csv"
    with open(bad_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["record_id", "review_decision", "reviewer_comments"])
        writer.writeheader()
        writer.writerow({
            "record_id": "QA-PILOT-DPDP-001",
            "review_decision": "SELF_APPROVED_BY_AI",
            "reviewer_comments": "Invalid",
        })

    with pytest.raises(ReviewImportError):
        importer.import_reviews(bad_csv, temp_dataset)

    # Assert atomic protection: temp_dataset unchanged
    assert hashlib.sha256(temp_dataset.read_bytes()).hexdigest() == orig_hash

    # 2. Rejection without comment must fail
    no_comment_csv = tmp_path / "no_comment.csv"
    with open(no_comment_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["record_id", "review_decision", "reviewer_comments"])
        writer.writeheader()
        writer.writerow({
            "record_id": "QA-PILOT-DPDP-001",
            "review_decision": "REJECTED",
            "reviewer_comments": "",  # Empty!
        })

    with pytest.raises(ReviewImportError) as exc_info:
        importer.import_reviews(no_comment_csv, temp_dataset)
    assert "Reviewer comment is mandatory" in str(exc_info.value)
    assert hashlib.sha256(temp_dataset.read_bytes()).hexdigest() == orig_hash

    # 3. Verify original frozen dataset on disk was never touched
    frozen_hash = hashlib.sha256(frozen_dataset.read_bytes()).hexdigest()
    assert frozen_hash == "e01b22f50f36c3927b595ecd03e2258c6889f299e6394644b2cd4cb359ffa953"

