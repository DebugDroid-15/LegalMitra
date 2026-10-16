"""
Script: scripts/verify_review_packages.py
Comprehensive integrity verification of both Advocate Review Packages:
1. Package A: Frozen Pilot 20 (Bitwise SHA-256 hash preservation)
2. Package B: Batch 1 Candidate Expansion (Candidate count, schema, blank review sheet)
3. Review Tracking Register: Consistency across all 40 tracked examples
Usage:
    python scripts/verify_review_packages.py
"""

import json
from pathlib import Path
import sys

from legalmitra.core.hashing import compute_file_sha256
from legalmitra.review.tracker import ReviewTracker
from legalmitra.schemas.legal_qa import LegalQADocument


def verify_package_a() -> bool:
    print("--- Verifying Package A (Frozen Pilot 20 Snapshot) ---")
    manifest_path = Path("data/06_review/PHASE9_REVIEW_SNAPSHOT_MANIFEST.json")
    if not manifest_path.exists():
        print(f"[FAIL] Manifest not found at {manifest_path}", file=sys.stderr)
        return False

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    all_matched = True
    for key, item in manifest["frozen_artifacts"].items():
        p = Path(item["path"])
        if not p.exists():
            print(f"[FAIL] Frozen artifact {p} does not exist!", file=sys.stderr)
            all_matched = False
            continue
        actual_hash = compute_file_sha256(p)
        expected_hash = item["sha256"]
        if actual_hash != expected_hash:
            print(f"[FAIL] SHA256 mismatch for {p}: expected {expected_hash}, got {actual_hash}", file=sys.stderr)
            all_matched = False
        else:
            print(f"  [OK] {key} ({p.name}) matches SHA256={actual_hash[:16]}...")

    # Check 20 records strictly pending
    pilot_file = Path("data/03_generated/pilot_20_examples.jsonl")
    with open(pilot_file, "r", encoding="utf-8") as f:
        docs = [LegalQADocument(**json.loads(line)) for line in f if line.strip()]
    if len(docs) != 20:
        print(f"[FAIL] Expected 20 pilot records, found {len(docs)}", file=sys.stderr)
        return False
    for d in docs:
        if d.legal_review_status.value != "pending_legal_review":
            print(f"[FAIL] Pilot record {d.qa_id} has status {d.legal_review_status}", file=sys.stderr)
            return False

    print("[OK] Package A is 100% byte-for-byte verified and pending review.\n")
    return all_matched


def verify_package_b() -> bool:
    print("--- Verifying Package B (Batch 1 Candidate Expansion) ---")
    manifest_path = Path("data/07_batches/review/batch_01_handoff_manifest.json")
    if not manifest_path.exists():
        print(f"[FAIL] Batch 1 handoff manifest not found at {manifest_path}", file=sys.stderr)
        return False

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    all_matched = True
    for key, item in manifest["artifacts"].items():
        p = Path(item["path"])
        if not p.exists():
            print(f"[FAIL] Batch 1 artifact {p} does not exist!", file=sys.stderr)
            all_matched = False
            continue
        actual_hash = compute_file_sha256(p)
        expected_hash = item["sha256"]
        if actual_hash != expected_hash:
            print(f"[FAIL] SHA256 mismatch for {p}: expected {expected_hash}, got {actual_hash}", file=sys.stderr)
            all_matched = False
        else:
            print(f"  [OK] {key} ({p.name}) matches SHA256={actual_hash[:16]}...")

    # Check 20 candidates strictly pending
    batch_file = Path("data/07_batches/batch_01_candidates/batch_01_examples.jsonl")
    with open(batch_file, "r", encoding="utf-8") as f:
        docs = [LegalQADocument(**json.loads(line)) for line in f if line.strip()]
    if len(docs) != 20:
        print(f"[FAIL] Expected 20 Batch 1 candidates, found {len(docs)}", file=sys.stderr)
        return False
    for d in docs:
        if d.legal_review_status.value != "pending_legal_review":
            print(f"[FAIL] Candidate {d.qa_id} has status {d.legal_review_status}", file=sys.stderr)
            return False

    print("[OK] Package B is 100% verified and pending review.\n")
    return all_matched


def verify_review_tracker() -> bool:
    print("--- Verifying Review Tracking Register ---")
    tracker = ReviewTracker()
    summary = tracker.get_summary()
    total = summary["total_records"]
    if total != 40:
        print(f"[FAIL] Expected 40 tracked records in review tracker, found {total}", file=sys.stderr)
        return False

    pkg_a = summary["packages"].get("PACKAGE_A_PILOT_20", 0)
    pkg_b = summary["packages"].get("PACKAGE_B_BATCH_01", 0)
    if pkg_a != 20 or pkg_b != 20:
        print(f"[FAIL] Tracker package count mismatch: Package A={pkg_a}, Package B={pkg_b}", file=sys.stderr)
        return False

    pending_count = summary["status_distribution"].get("pending_legal_review", 0)
    if pending_count != 40:
        print(f"[FAIL] Expected all 40 records to have pending_legal_review, got {pending_count}", file=sys.stderr)
        return False

    print(f"[OK] Review tracking register verified: 40 total records (20 Package A, 20 Package B), all pending review.\n")
    return True


def main():
    print("=== LegalMitra Advocate Review Package Integrity Verification ===\n")
    ok_a = verify_package_a()
    ok_b = verify_package_b()
    ok_tr = verify_review_tracker()

    if ok_a and ok_b and ok_tr:
        print("=== ALL REVIEW PACKAGES & TRACKING REGISTERS VERIFIED SUCCESSFUL ===")
        sys.exit(0)
    else:
        print("=== VERIFICATION FAILED ===", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

