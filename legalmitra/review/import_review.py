"""
LegalMitra Advocate Review Importer
Imports human advocate decisions from the review sheet CSV into the dataset.
Enforces strict audit standards:
1. Accepts only APPROVED, REVISION_REQUIRED, or REJECTED.
2. Preserves reviewer identity and review date only where provided.
3. Requires non-empty reviewer comment for revision or rejection.
4. Preserves the original generated record snapshot in an immutable audit ledger.
5. Never infers approval from a blank field, passing test, or source match.
6. Keeps automated validation status completely separate from legal-review status.
7. Enforces atomic validation: Rejects malformed imports without partially modifying the dataset.
"""

from dataclasses import asdict, dataclass, field
from datetime import date, datetime
import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from legalmitra.core.enums import LegalReviewStatus
from legalmitra.core.hashing import compute_file_sha256
from legalmitra.core.logging import get_logger
from legalmitra.schemas.legal_qa import LegalQADocument

logger = get_logger("review_importer")


class ReviewImportError(Exception):
    """Raised when advocate review import validation fails."""
    pass


@dataclass
class ReviewAuditEntry:
    """Immutable audit record tracking a reviewer decision."""
    timestamp: str
    record_id: str
    previous_review_status: str
    new_review_status: str
    decision: str
    reviewer_name_initials: Optional[str]
    review_date: Optional[str]
    reviewer_comments: Optional[str]
    scores: Dict[str, Optional[int]]
    original_record_snapshot: Dict[str, Any]
    submitted_csv_sha256: Optional[str] = None


@dataclass
class ReviewImportSummary:
    """Summary metrics of a review import operation."""
    total_csv_rows: int
    records_updated: int
    approved_count: int
    revision_required_count: int
    rejected_count: int
    pending_count: int
    audit_log_path: str
    imported_at: str
    submitted_csv_sha256: Optional[str] = None


@dataclass
class ReviewValidationReport:
    """Structured report returned from pre-import review sheet validation."""
    is_valid: bool
    total_rows: int
    decisions_count: int
    pending_count: int
    errors: List[str]
    accepted_record_ids: List[str]
    pending_record_ids: List[str]
    rejected_record_ids: List[str]
    submitted_csv_sha256: str
    generated_at: str
    summary_markdown: str


class ReviewImporter:
    """
    Validates and applies human advocate decisions from review sheets to LegalQADocument datasets.
    """

    ALLOWED_DECISIONS: Set[str] = {
        "APPROVED",
        "APPROVED_WITH_CORRECTIONS",
        "REVISION_REQUIRED",
        "REJECTED",
        "NEEDS_MORE_EVIDENCE",
        "DEFERRED",
    }

    def __init__(self, audit_dir: Union[str, Path] = "data/06_review/audit"):
        self.audit_dir = Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)

    def validate_review_sheet(
        self,
        csv_path: Union[str, Path],
        existing_records: Dict[str, LegalQADocument],
        allow_overwrite: bool = False,
        strict_attribution: bool = False,
    ) -> Tuple[bool, List[str], List[Dict[str, Any]]]:
        """
        Validates the entire review sheet CSV before making any modifications (Atomic Guarantee).
        Returns: (is_valid, error_messages, valid_row_data)
        """
        csv_path = Path(csv_path)
        if not csv_path.exists():
            return False, [f"Review CSV file not found: {csv_path}"], []

        errors: List[str] = []
        valid_rows: List[Dict[str, Any]] = []

        try:
            with open(csv_path, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        except Exception as e:
            return False, [f"Failed to parse CSV file '{csv_path}': {e}"], []

        if not rows:
            return False, ["Review sheet CSV is completely empty."], []

        required_columns = {"record_id", "review_decision"}
        missing_cols = required_columns - set(reader.fieldnames or [])
        if missing_cols:
            return False, [f"Review sheet CSV missing required columns: {sorted(missing_cols)}"], []

        seen_records: Set[str] = set()

        for line_num, row in enumerate(rows, start=2):
            record_id = (row.get("record_id") or "").strip()
            if not record_id:
                errors.append(f"Row {line_num}: Empty record_id.")
                continue

            if record_id in seen_records:
                errors.append(f"Row {line_num}: Duplicate record_id '{record_id}' in review sheet.")
                continue
            seen_records.add(record_id)

            if record_id not in existing_records:
                errors.append(f"Row {line_num}: record_id '{record_id}' does not exist in target dataset.")
                continue

            target_doc = existing_records[record_id]
            raw_decision = (row.get("review_decision") or "").strip()

            # Rule 5: Never infer approval from a blank field
            if not raw_decision:
                # Retains pending status
                valid_rows.append({
                    "record_id": record_id,
                    "decision": None,
                    "row": row,
                })
                continue

            norm_decision = raw_decision.upper().replace("-", "_").replace(" ", "_")
            if norm_decision == "APPROVED_WITH_CORRECTIONS":
                norm_decision = "REVISION_REQUIRED"

            if norm_decision not in self.ALLOWED_DECISIONS:
                errors.append(
                    f"Row {line_num} ({record_id}): Invalid review_decision '{raw_decision}'. "
                    f"Must be one of {sorted(self.ALLOWED_DECISIONS)}."
                )
                continue

            # Detect attempted overwrite of an already decided record
            if target_doc.legal_review_status != LegalReviewStatus.PENDING_LEGAL_REVIEW and not allow_overwrite:
                errors.append(
                    f"Row {line_num} ({record_id}): Cannot overwrite already decided status '{target_doc.legal_review_status.value}' "
                    f"with new decision '{norm_decision}' without allow_overwrite=True."
                )

            # Rule 3: Require reviewer comments for all non-approval decisions
            comments = (row.get("reviewer_comments") or "").strip()
            if norm_decision in ("REVISION_REQUIRED", "REJECTED", "NEEDS_MORE_EVIDENCE", "DEFERRED") and not comments:
                errors.append(
                    f"Row {line_num} ({record_id}): Reviewer comment is mandatory for '{norm_decision}' decisions."
                )

            # Validate reviewer attribution
            reviewer_initials = (row.get("reviewer_name_initials") or "").strip() or None
            raw_date = (row.get("review_date") or "").strip()
            parsed_date = None
            if raw_date:
                try:
                    parsed_date = date.fromisoformat(raw_date)
                except ValueError:
                    errors.append(f"Row {line_num} ({record_id}): Invalid date format '{raw_date}'. Must be YYYY-MM-DD.")

            if strict_attribution:
                if not reviewer_initials:
                    errors.append(f"Row {line_num} ({record_id}): Reviewer initials or name is required for decision '{norm_decision}'.")
                if not parsed_date:
                    errors.append(f"Row {line_num} ({record_id}): Valid review date (YYYY-MM-DD) is required for decision '{norm_decision}'.")

            # Validate scores if provided
            scores = {}
            for score_col in ("legal_accuracy_score_1_to_5", "temporal_accuracy_score_1_to_5", "grounding_accuracy_score_1_to_5"):
                val_str = (row.get(score_col) or "").strip()
                if val_str:
                    try:
                        val_int = int(val_str)
                        if val_int < 1 or val_int > 5:
                            errors.append(f"Row {line_num} ({record_id}): Score '{score_col}' must be between 1 and 5, got {val_int}.")
                        scores[score_col] = val_int
                    except ValueError:
                        errors.append(f"Row {line_num} ({record_id}): Score '{score_col}' is not an integer: '{val_str}'.")
                else:
                    scores[score_col] = None

            valid_rows.append({
                "record_id": record_id,
                "decision": norm_decision,
                "comments": comments if comments else None,
                "reviewer_name_initials": reviewer_initials,
                "review_date": parsed_date,
                "scores": scores,
                "row": row,
            })

        is_valid = len(errors) == 0
        return is_valid, errors, valid_rows

    def generate_validation_report(
        self,
        csv_path: Union[str, Path],
        dataset_path: Union[str, Path],
        allow_overwrite: bool = False,
        strict_attribution: bool = False,
    ) -> ReviewValidationReport:
        """
        Performs standalone validation on a review sheet CSV without mutating any records,
        returning a structured ReviewValidationReport.
        """
        csv_path = Path(csv_path)
        dataset_path = Path(dataset_path)

        if not dataset_path.exists():
            raise ReviewImportError(f"Target dataset file not found: {dataset_path}")

        records_map = {}
        with open(dataset_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    doc = LegalQADocument(**json.loads(line))
                    records_map[doc.qa_id] = doc

        is_valid, errors, valid_rows = self.validate_review_sheet(
            csv_path, records_map, allow_overwrite=allow_overwrite, strict_attribution=strict_attribution
        )

        accepted_ids = [r["record_id"] for r in valid_rows if r["decision"] is not None]
        pending_ids = [r["record_id"] for r in valid_rows if r["decision"] is None]
        rejected_ids = list(set([err.split("(")[1].split(")")[0] for err in errors if "(" in err and ")" in err]))

        csv_hash = compute_file_sha256(csv_path) if csv_path.exists() else "NOT_FOUND"
        now_str = datetime.utcnow().isoformat() + "Z"

        report_md = f"""# LegalMitra Advocate Review Sheet Validation Report

**Review Sheet:** `{csv_path}`  
**SHA-256 Hash:** `{csv_hash}`  
**Dataset Target:** `{dataset_path}`  
**Validation Time:** `{now_str}`  
**Overall Validation Status:** **{'PASSED' if is_valid else 'FAILED'}**

## Summary Metrics
- **Total Rows Evaluated:** {len(valid_rows) if is_valid else 'N/A'}
- **Decisions Provided:** {len(accepted_ids)}
- **Pending / Blank Rows:** {len(pending_ids)}
- **Validation Errors:** {len(errors)}

## Decision Breakdown
"""
        if is_valid:
            dec_counts: Dict[str, int] = {}
            for r in valid_rows:
                d = r["decision"] or "PENDING"
                dec_counts[d] = dec_counts.get(d, 0) + 1
            for d, c in sorted(dec_counts.items()):
                report_md += f"- **{d}:** {c}\n"
        else:
            report_md += "Validation failed. Detailed errors below:\n"
            for err in errors:
                report_md += f"- ❌ {err}\n"

        return ReviewValidationReport(
            is_valid=is_valid,
            total_rows=len(valid_rows) if is_valid else 0,
            decisions_count=len(accepted_ids),
            pending_count=len(pending_ids),
            errors=errors,
            accepted_record_ids=accepted_ids,
            pending_record_ids=pending_ids,
            rejected_record_ids=rejected_ids,
            submitted_csv_sha256=csv_hash,
            generated_at=now_str,
            summary_markdown=report_md,
        )

    def import_reviews(
        self,
        csv_path: Union[str, Path],
        dataset_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
        allow_overwrite: bool = False,
        strict_attribution: bool = False,
    ) -> Tuple[List[LegalQADocument], ReviewImportSummary]:
        """
        Executes atomic import of advocate reviews into dataset.
        Raises ReviewImportError if any row fails validation, without modifying the dataset.
        """
        csv_path = Path(csv_path)
        dataset_path = Path(dataset_path)

        if not dataset_path.exists():
            raise ReviewImportError(f"Target dataset file not found: {dataset_path}")

        csv_hash = compute_file_sha256(csv_path)

        # Load existing dataset
        existing_docs: List[LegalQADocument] = []
        with open(dataset_path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                if line.strip():
                    try:
                        doc = LegalQADocument(**json.loads(line))
                        existing_docs.append(doc)
                    except Exception as e:
                        raise ReviewImportError(f"Dataset parsing error at line {line_no}: {e}")

        records_map = {doc.qa_id: doc for doc in existing_docs}

        # Step 1: Pre-validation of entire review sheet (Atomic Guarantee)
        is_valid, errors, row_data = self.validate_review_sheet(
            csv_path, records_map, allow_overwrite=allow_overwrite, strict_attribution=strict_attribution
        )
        if not is_valid:
            error_details = "\n - " + "\n - ".join(errors[:10])
            if len(errors) > 10:
                error_details += f"\n ... and {len(errors) - 10} more errors"
            raise ReviewImportError(
                f"Review import rejected. Failed validation with {len(errors)} error(s):{error_details}"
            )

        # Step 2: Apply decisions and generate audit trail
        audit_entries: List[ReviewAuditEntry] = []
        approved_count = 0
        revision_required_count = 0
        rejected_count = 0
        pending_count = 0
        updated_count = 0

        timestamp_str = datetime.utcnow().isoformat() + "Z"

        for item in row_data:
            rec_id = item["record_id"]
            decision = item["decision"]
            doc = records_map[rec_id]

            if decision is None:
                # Blank field: Preserves PENDING_LEGAL_REVIEW
                pending_count += 1
                continue

            previous_status = doc.legal_review_status.value
            snapshot = doc.model_dump(mode="json")

            if decision == "APPROVED":
                doc.legal_review_status = LegalReviewStatus.LEGAL_EXPERT_APPROVED
                approved_count += 1
            elif decision == "REVISION_REQUIRED":
                doc.legal_review_status = LegalReviewStatus.REVISION_REQUIRED
                revision_required_count += 1
            elif decision == "REJECTED":
                doc.legal_review_status = LegalReviewStatus.LEGAL_EXPERT_REJECTED
                rejected_count += 1
            elif decision == "NEEDS_MORE_EVIDENCE":
                doc.legal_review_status = LegalReviewStatus.NEEDS_MORE_EVIDENCE
            elif decision == "DEFERRED":
                doc.legal_review_status = LegalReviewStatus.DEFERRED

            doc.reviewer_comments = item["comments"]
            doc.reviewer_name_initials = item["reviewer_name_initials"]
            doc.review_date = item["review_date"]
            updated_count += 1

            audit_entry = ReviewAuditEntry(
                timestamp=timestamp_str,
                record_id=rec_id,
                previous_review_status=previous_status,
                new_review_status=doc.legal_review_status.value,
                decision=decision,
                reviewer_name_initials=item["reviewer_name_initials"],
                review_date=item["review_date"].isoformat() if item["review_date"] else None,
                reviewer_comments=item["comments"],
                scores=item["scores"],
                original_record_snapshot=snapshot,
                submitted_csv_sha256=csv_hash,
            )
            audit_entries.append(audit_entry)

        # Step 3: Write immutable audit ledger
        audit_file = self.audit_dir / f"review_audit_log_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.jsonl"
        with open(audit_file, "w", encoding="utf-8") as f:
            for entry in audit_entries:
                f.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")

        # Step 4: Write updated dataset if output path specified
        dest_path = Path(output_path) if output_path else dataset_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, "w", encoding="utf-8") as f:
            for doc in existing_docs:
                f.write(doc.model_dump_json() + "\n")

        summary = ReviewImportSummary(
            total_csv_rows=len(row_data),
            records_updated=updated_count,
            approved_count=approved_count,
            revision_required_count=revision_required_count,
            rejected_count=rejected_count,
            pending_count=pending_count,
            audit_log_path=str(audit_file),
            imported_at=timestamp_str,
            submitted_csv_sha256=csv_hash,
        )

        logger.info(
            f"Successfully imported advocate reviews: {updated_count} records updated "
            f"({approved_count} approved, {revision_required_count} revision required, {rejected_count} rejected, "
            f"{pending_count} pending). Audit log at: {audit_file}"
        )

        return existing_docs, summary

