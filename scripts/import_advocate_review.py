"""
Script: scripts/import_advocate_review.py
CLI tool to import advocate review decisions from a CSV review sheet into a dataset.
Usage:
    python scripts/import_advocate_review.py --csv data/06_review/pilot_20_review_sheet.csv --dataset data/03_generated/pilot_20_examples.jsonl --dry-run
"""

import argparse
from pathlib import Path
import sys

from legalmitra.review.import_review import ReviewImporter, ReviewImportError


def main():
    parser = argparse.ArgumentParser(description="Import human advocate review decisions into LegalMitra datasets.")
    parser.add_argument("--csv", required=True, help="Path to filled review CSV sheet.")
    parser.add_argument("--dataset", required=True, help="Path to dataset JSONL to update.")
    parser.add_argument("--output", default=None, help="Optional output path (defaults to in-place update).")
    parser.add_argument("--audit-dir", default="data/06_review/audit", help="Directory for immutable audit logs.")
    parser.add_argument("--dry-run", action="store_true", help="Validate review sheet without applying changes.")
    parser.add_argument("--allow-overwrite", action="store_true", help="Allow overwriting already decided records.")
    parser.add_argument("--strict-attribution", action="store_true", help="Strictly require reviewer initials and date.")

    args = parser.parse_args()

    csv_path = Path(args.csv)
    dataset_path = Path(args.dataset)

    if not csv_path.exists():
        print(f"Error: CSV file not found: {csv_path}", file=sys.stderr)
        sys.exit(1)

    if not dataset_path.exists():
        print(f"Error: Dataset file not found: {dataset_path}", file=sys.stderr)
        sys.exit(1)

    importer = ReviewImporter(audit_dir=args.audit_dir)

    try:
        if args.dry_run:
            print(f"Validating review sheet '{csv_path}' against '{dataset_path}' (dry run)...")
            from legalmitra.schemas.legal_qa import LegalQADocument
            import json
            records = {}
            with open(dataset_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        d = LegalQADocument(**json.loads(line))
                        records[d.qa_id] = d

            is_valid, errors, rows = importer.validate_review_sheet(
                csv_path, records, allow_overwrite=args.allow_overwrite, strict_attribution=args.strict_attribution
            )
            if not is_valid:
                print(f"VALIDATION FAILED with {len(errors)} error(s):", file=sys.stderr)
                for err in errors:
                    print(f" - {err}", file=sys.stderr)
                sys.exit(1)
            else:
                decisions_count = len([r for r in rows if r["decision"] is not None])
                pending_count = len([r for r in rows if r["decision"] is None])
                print(f"VALIDATION PASSED: {len(rows)} rows checked ({decisions_count} decisions, {pending_count} pending).")
                sys.exit(0)
        else:
            print(f"Importing advocate reviews from '{csv_path}' into '{dataset_path}'...")
            docs, summary = importer.import_reviews(
                csv_path,
                dataset_path,
                output_path=args.output,
                allow_overwrite=args.allow_overwrite,
                strict_attribution=args.strict_attribution,
            )
            print("Import completed successfully!")
            print(f"- Total rows: {summary.total_csv_rows}")
            print(f"- Records updated: {summary.records_updated}")
            print(f"- Approved: {summary.approved_count}")
            print(f"- Revision required: {summary.revision_required_count}")
            print(f"- Rejected: {summary.rejected_count}")
            print(f"- Pending remaining: {summary.pending_count}")
            print(f"- Submitted CSV SHA-256: {summary.submitted_csv_sha256}")
            print(f"- Audit log written to: {summary.audit_log_path}")

            # Update ReviewTracker if records were updated
            if summary.records_updated > 0:
                try:
                    from legalmitra.review.tracker import ReviewTracker
                    tracker = ReviewTracker()
                    updated_ids = [d.qa_id for d in docs if d.legal_review_status.value != "pending_legal_review"]
                    status_map = {d.qa_id: d.legal_review_status.value for d in docs}
                    tracker.update_imported(updated_ids, summary.audit_log_path, new_status_map=status_map)
                    print(f"- Review tracker updated with {len(updated_ids)} imported records.")
                except Exception as ex:
                    print(f"Warning: Failed to update review tracker: {ex}")

            sys.exit(0)

    except ReviewImportError as e:
        print(f"Review import error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

