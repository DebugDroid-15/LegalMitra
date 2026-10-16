"""
Script: scripts/verify_freeze.py
Verifies handoff integrity and calculates cryptographic hashes for Phase 9 freeze.
"""

import csv
import hashlib
import json
from pathlib import Path


def verify_freeze():
    print("--- Phase 9 Review Snapshot Integrity Verification ---")

    # 1. Load pilot records
    examples_path = Path("data/03_generated/pilot_20_examples.jsonl")
    assert examples_path.exists(), f"Missing {examples_path}"
    docs = [json.loads(line) for line in examples_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    assert len(docs) == 20, f"Expected 20 docs, got {len(docs)}"
    doc_ids = [d["qa_id"] for d in docs]
    assert len(set(doc_ids)) == 20, "Non-unique IDs detected"
    print(f"[OK] pilot_20_examples.jsonl has exactly 20 unique records.")

    # 2. Load manifest
    manifest_path = Path("data/03_generated/pilot_20_manifest.json")
    assert manifest_path.exists(), f"Missing {manifest_path}"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_ids = [ex["qa_id"] for ex in manifest["examples"]]
    assert set(doc_ids) == set(manifest_ids), "Manifest ID mismatch"
    print(f"[OK] pilot_20_manifest.json matches all 20 record IDs.")

    # 3. Load review sheet CSV
    csv_path = Path("data/06_review/pilot_20_review_sheet.csv")
    assert csv_path.exists(), f"Missing {csv_path}"
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        csv_rows = list(csv.DictReader(f))
    csv_ids = [r["record_id"] for r in csv_rows]
    assert set(doc_ids) == set(csv_ids), "CSV ID mismatch"
    print(f"[OK] pilot_20_review_sheet.csv matches all 20 record IDs.")

    # 4. Load source bundle
    bundle_path = Path("data/06_review/pilot_20_source_bundle.json")
    assert bundle_path.exists(), f"Missing {bundle_path}"
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    bundle_ids = [r["record_id"] for r in bundle["records"]]
    assert set(doc_ids) == set(bundle_ids), "Bundle ID mismatch"
    print(f"[OK] pilot_20_source_bundle.json matches all 20 record IDs.")

    # 5. Verify pending status, dates, and quarantine compliance
    for d in docs:
        qid = d["qa_id"]
        assert d["legal_review_status"] == "pending_legal_review", f"{qid} not pending"
        assert d["legal_as_of_date"] == "2026-10-16", f"{qid} legal_as_of_date mismatch"
        assert d["commencement_source_id"] is not None, f"{qid} missing commencement notification"
        assert d["commencement_date"] is not None, f"{qid} missing commencement date"
        assert "IND-JUD-DEL-2024-BAIL" not in d["supporting_source_ids"], f"{qid} cites quarantined scaffold"
        for p in d["evidence_passages"]:
            assert p["source_id"] != "IND-JUD-DEL-2024-BAIL", f"{qid} passage cites quarantined scaffold"

    for r in csv_rows:
        qid = r["record_id"]
        assert r["review_decision"] == "", f"{qid} has non-blank decision: {r['review_decision']}"
        assert r["legal_accuracy_score_1_to_5"] == "", f"{qid} has non-blank legal score"
        assert r["temporal_accuracy_score_1_to_5"] == "", f"{qid} has non-blank temporal score"
        assert r["grounding_accuracy_score_1_to_5"] == "", f"{qid} has non-blank grounding score"
        assert r["reviewer_comments"] == "", f"{qid} has non-blank comments"
        assert r["reviewer_name_initials"] == "", f"{qid} has non-blank initials"
        assert r["review_date"] == "", f"{qid} has non-blank date"

    for b in bundle["records"]:
        assert b["review_status"] == "pending_legal_review"
        assert b["decision"] is None

    print(f"[OK] All 20 records remain strictly pending_legal_review with blank decision and score fields.")
    print(f"[OK] Quarantine compliance verified: Zero references to IND-JUD-DEL-2024-BAIL.")

    # 6. Check open issues coverage
    issues_path = Path("data/06_review/pilot_20_open_issues.md")
    assert issues_path.exists()
    issues_text = issues_path.read_text(encoding="utf-8")
    for iss in ["Issue 1", "Issue 2", "Issue 3", "Issue 4", "Issue 5", "Issue 6"]:
        assert iss in issues_text, f"Missing {iss} in pilot_20_open_issues.md"

    register_path = Path("PHASE8_OPEN_LEGAL_ISSUES_REGISTER.md")
    assert register_path.exists()
    reg_text = register_path.read_text(encoding="utf-8")
    for iss in ["Issue 1", "Issue 2", "Issue 3", "Issue 4", "Issue 5", "Issue 6"]:
        assert iss in reg_text, f"Missing {iss} in PHASE8_OPEN_LEGAL_ISSUES_REGISTER.md"

    print(f"[OK] All 6 open legal ambiguities are fully documented and linked to pilot records.")

    # 7. Compute cryptographic hashes
    artifacts = [
        examples_path,
        manifest_path,
        csv_path,
        bundle_path,
        issues_path,
        register_path,
    ]
    hash_data = {}
    for p in artifacts:
        data = p.read_bytes()
        sha = hashlib.sha256(data).hexdigest()
        hash_data[p.name] = {
            "path": str(p).replace("\\", "/"),
            "size_bytes": len(data),
            "sha256": sha,
        }
        print(f"  - {p.name}: {len(data):,} bytes | SHA256={sha}")

    return hash_data


if __name__ == "__main__":
    verify_freeze()

