"""Audit precedent conflict register and human-in-the-loop review integrity."""

import json
import sys

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

def audit_conflicts():
    print("=== Workstream D Precedent Conflict Register Audit ===")
    path = "data/21_judicial_infrastructure/precedent_conflict_register.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    meta = data.get("metadata", {})
    conflicts = data.get("conflicts", [])
    print(f"Total conflicts: {len(conflicts)}")
    print(f"Authorized reviewers: {meta.get('authorized_reviewers')}")

    for c in conflicts:
        cid = c["conflict_id"]
        cat = c["category"]
        stat = c["status"]
        p_score = c["priority_score"]
        sec = c["governing_statute_section"]
        rev = c["assigned_reviewer"]
        auth = c["reviewer_authorized"]

        case_a = c["case_a"]
        case_b = c["case_b"]

        anchor_a = case_a.get("passage_anchor", "")
        anchor_b = case_b.get("passage_anchor", "")

        has_anchors = bool(anchor_a.strip() and anchor_b.strip())

        print(f"\nConflict {cid}:")
        print(f"  Category: {cat}")
        print(f"  Status: {stat} | Priority: {p_score}")
        print(f"  Statute: {sec}")
        print(f"  Case A: {case_a['title']} ({case_a['court_id']}, bench={case_a['bench_count']})")
        print(f"    Anchor A: '{anchor_a}'")
        print(f"  Case B: {case_b['title']} ({case_b['court_id']}, bench={case_b['bench_count']})")
        print(f"    Anchor B: '{anchor_b}'")
        print(f"    Anchors verified non-empty: {has_anchors}")
        print(f"  Reviewer: {rev} (Authorized: {auth})")
        print(f"  Audit trail length: {len(c.get('audit_trail', []))}")

if __name__ == "__main__":
    audit_conflicts()
