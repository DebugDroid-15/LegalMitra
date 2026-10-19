"""Audit independent judicial benchmark v3 cases, categories, and authority."""

import json
import sys

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

def audit_benchmark():
    print("=== Workstream F Independent Judicial Benchmark V3 Audit ===")
    path = "data/21_judicial_infrastructure/independent_judicial_benchmark_v3.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    benchmark_id = data.get("benchmark_id")
    version = data.get("benchmark_version")
    total_cases = data.get("total_test_cases")
    cases = data.get("cases", [])
    categories = data.get("categories_covered", [])

    print(f"Benchmark ID: {benchmark_id} (Version {version})")
    print(f"Reported total cases: {total_cases}, Actual cases list length: {len(cases)}")
    print(f"Categories covered: {len(categories)}")

    # Check for duplicate IDs or prompts
    seen_ids = set()
    dup_ids = set()
    seen_prompts = set()
    dup_prompts = set()

    cat_counts = {}

    for c in cases:
        cid = c.get("id")
        prompt = c.get("prompt")
        cat = c.get("category")

        if cid in seen_ids:
            dup_ids.add(cid)
        seen_ids.add(cid)

        if prompt in seen_prompts:
            dup_prompts.add(prompt)
        seen_prompts.add(prompt)

        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    print(f"\nUnique IDs: {len(seen_ids)}, Duplicate IDs: {len(dup_ids)}")
    print(f"Unique Prompts: {len(seen_prompts)}, Duplicate Prompts: {len(dup_prompts)}")

    print("\n--- Category Breakdown ---")
    for cat, count in sorted(cat_counts.items()):
        print(f"  {cat}: {count} cases")

    print("\n--- Phase 40 Cases (CASE-36 to CASE-48) ---")
    phase40_ids = [f"CASE-{i}" for i in range(36, 49)]
    for cid in phase40_ids:
        case_match = next((c for c in cases if c.get("id") == cid), None)
        if case_match:
            print(f"  [{case_match['id']}] ({case_match['category']}): {case_match['prompt'][:70]}...")
            print(f"    Authority: {case_match.get('statutory_authority')}")
        else:
            print(f"  [{cid}] MISSING!")

if __name__ == "__main__":
    audit_benchmark()
