"""
Script: scripts/validate_review_submission.py
CLI tool to validate a submitted advocate review sheet without applying any changes.
Produces a clear, auditable validation report detailing accepted, pending, and rejected records.

Usage:
    python scripts/validate_review_submission.py --csv data/07_batches/review/batch_01_review_sheet.csv --dataset data/07_batches/batch_01_candidates/batch_01_examples.jsonl
"""

import argparse
from pathlib import Path
import sys

from legalmitra.review.import_review import ReviewImporter, ReviewImportError


def main():
    parser = argparse.ArgumentParser(description="Validate advocate review sheet CSV before import.")
    parser.add_argument("--csv", required=True, help="Path to the filled advocate review sheet CSV.")
    parser.add_argument("--dataset", required=True, help="Path to the target dataset JSONL.")
    parser.add_argument("--allow-overwrite", action="store_true", help="Allow overwriting already decided records.")
    parser.add_argument("--strict-attribution", action="store_true", help="Strictly require reviewer initials and date.")
    parser.add_argument("--report-out", default=None, help="Optional output path to write the markdown report.")

    args = parser.parse_args()

    csv_path = Path(args.csv)
    dataset_path = Path(args.dataset)

    if not csv_path.exists():
        print(f"Error: CSV file not found: {csv_path}", file=sys.stderr)
        sys.exit(1)

    if not dataset_path.exists():
        print(f"Error: Dataset file not found: {dataset_path}", file=sys.stderr)
        sys.exit(1)

    importer = ReviewImporter()

    try:
        report = importer.generate_validation_report(
            csv_path,
            dataset_path,
            allow_overwrite=args.allow_overwrite,
            strict_attribution=args.strict_attribution,
        )

        print(report.summary_markdown)

        if args.report_out:
            out_p = Path(args.report_out)
            out_p.parent.mkdir(parents=True, exist_ok=True)
            with open(out_p, "w", encoding="utf-8") as f:
                f.write(report.summary_markdown)
            print(f"\n[OK] Validation report written to {out_p}")

        if report.is_valid:
            print("\n[RESULT] Validation PASSED. Sheet is eligible for import.")
            sys.exit(0)
        else:
            print("\n[RESULT] Validation FAILED. Sheet contains errors that must be resolved.")
            sys.exit(1)

    except ReviewImportError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

