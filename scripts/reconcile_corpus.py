"""
CLI Script to execute complete corpus, database, review package, and benchmark reconciliation.
Usage:
    python scripts/reconcile_corpus.py [--output data/22_central_legislation/phase61_reconciliation_report.json]
"""

import argparse
import json
import sys
from legalmitra.operations.reconciler import CorpusReconciler


def main():
    parser = argparse.ArgumentParser(description="LegalMitra Corpus Reconciliation Runner")
    parser.add_argument(
        "--output",
        default="data/22_central_legislation/phase63_reconciliation_report.json",
        help="Path to save reconciliation report JSON",
    )
    args = parser.parse_args()

    print("=== LegalMitra Corpus & Artifact Reconciliation Runner ===")
    reconciler = CorpusReconciler()
    report = reconciler.run_full_reconciliation()

    print(f"Audit ID:        {report.audit_id}")
    print(f"Overall Status:  {report.overall_status}")
    print(f"Sources:         {report.total_sources} (Authentic: {report.authentic_sources}, Quarantined: {report.quarantined_sources})")
    print(f"Chunks:          {report.total_chunks} (Authentic: {report.authentic_chunks}, Quarantined: {report.quarantined_chunks})")
    print(f"Orphaned Chunks: {report.orphaned_chunks}")
    print(f"Duplicate IDs:   {report.duplicate_chunk_ids}")
    print(f"Unchunked:       {report.unchunked_sources}")
    print(f"Review Records:  {report.review_package_records} (Pending: {report.review_package_pending_count})")
    print(f"Benchmark V14:   {report.benchmark_v14_total_cases} cases | Splits: {report.benchmark_v14_splits} | Clean: {report.benchmark_contamination_clean}")
    print(f"Quarantine OK:   {report.scaffold_quarantine_compliant}")

    if report.findings:
        print("\nFindings:")
        for f in report.findings:
            print(f"  + {f}")

    if report.errors:
        print("\nERRORS:", file=sys.stderr)
        for e in report.errors:
            print(f"  ! {e}", file=sys.stderr)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report.to_dict(), f, indent=2)
    print(f"\n[OK] Reconciliation report persisted to: {args.output}")

    if report.overall_status != "PASSED":
        sys.exit(1)


if __name__ == "__main__":
    main()
