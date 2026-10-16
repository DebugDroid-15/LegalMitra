"""
Script: scripts/review_status_summary.py
Generates an executive summary of advocate review progress across:
- Package A: Frozen Pilot 20
- Package B: Batch 1 Candidate Expansion
- Model Fine-Tuning Eligibility Check (Enforcing 0 approved candidates = NO-GO)

Usage:
    python scripts/review_status_summary.py
"""

from pathlib import Path
import sys

from legalmitra.review.eligibility import DatasetEligibilityFilter
from legalmitra.review.tracker import ReviewTracker
from legalmitra.schemas.legal_qa import LegalQADocument
import json


def main():
    print("=== LegalMitra Advocate Review Status Summary ===\n")
    tracker = ReviewTracker()
    summary = tracker.get_summary()

    print(f"Total Tracked Records: {summary['total_records']}")
    print("\n--- Package Breakdown ---")
    for pkg, count in summary["packages"].items():
        print(f"  - {pkg}: {count} records")

    print("\n--- Status Distribution ---")
    for st, count in summary["status_distribution"].items():
        print(f"  - {st}: {count}")

    print("\n--- Dispatch & Operation Metrics ---")
    print(f"  - Sent to Advocates: {summary['dispatch_metrics']['sent_count']} / {summary['total_records']}")
    print(f"  - Responses Received: {summary['response_metrics']['received_count']} / {summary['total_records']}")
    print(f"  - Successfully Imported: {summary['import_metrics']['imported_count']} / {summary['total_records']}")

    # Training Eligibility Filter Check
    all_docs = []
    pilot_p = Path("data/03_generated/pilot_20_examples.jsonl")
    if pilot_p.exists():
        with open(pilot_p, "r", encoding="utf-8") as f:
            all_docs.extend([LegalQADocument(**json.loads(line)) for line in f if line.strip()])

    batch_p = Path("data/07_batches/batch_01_candidates/batch_01_examples.jsonl")
    if batch_p.exists():
        with open(batch_p, "r", encoding="utf-8") as f:
            all_docs.extend([LegalQADocument(**json.loads(line)) for line in f if line.strip()])

    eligibility_filter = DatasetEligibilityFilter()
    eligible_docs, elig_summary = eligibility_filter.filter_training_dataset(all_docs)

    print("\n--- Training & Fine-Tuning Dataset Eligibility ---")
    print(f"  - Total Evaluated Records: {elig_summary['total_evaluated']}")
    print(f"  - Eligible for Model Training: {elig_summary['eligible_for_training_count']}")
    print(f"  - Ineligible Count: {elig_summary['ineligible_count']}")
    print(f"  - Determination: {'AUTHORIZE PILOT EXPERIMENT' if elig_summary['eligible_for_training_count'] >= 150 else 'STRICT NO-GO FOR FINE-TUNING'}")

    # Outstanding Legal Ambiguities linked in tracker
    print("\n--- Outstanding Documented Legal Ambiguities ---")
    ambiguities = 0
    for eid, entry in tracker.entries.items():
        if entry.outstanding_issues:
            for issue in entry.outstanding_issues:
                print(f"  - [{eid}] {issue}")
                ambiguities += 1
    if ambiguities == 0:
        print("  - None recorded.")

    print("\n=== Review Status Report Complete ===")


if __name__ == "__main__":
    main()

