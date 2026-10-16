"""
LegalMitra Review Tracker
Provides an auditable, persistent tracking registry for tracking the lifecycle
of legal review packages (Package A: Frozen Pilot 20, Package B: Batch 1 Candidates).

Tracks dispatch, response receipt, schema validation, import status, and outstanding issues
without inventing advocate identities, delivery dates, or artificial approvals.
"""

from dataclasses import asdict, dataclass, field
from datetime import datetime
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from legalmitra.core.logging import get_logger
from legalmitra.schemas.legal_qa import LegalQADocument

logger = get_logger("review_tracker")


@dataclass
class ReviewTrackerEntry:
    """Represents the tracking record for a single legal QA example."""
    example_id: str
    dataset_version: str
    batch_id: str
    package_identifier: str
    legal_domain: str
    statutory_citations: List[str]
    review_status: str = "pending_legal_review"
    sent_to_advocate: bool = False
    sent_date: Optional[str] = None
    advocate_recipient_tag: Optional[str] = None
    response_received: bool = False
    response_date: Optional[str] = None
    validation_passed: bool = False
    validation_report_ref: Optional[str] = None
    imported: bool = False
    import_audit_reference: Optional[str] = None
    outstanding_issues: List[str] = field(default_factory=list)


class ReviewTracker:
    """
    Manages the persistent tracking registry across all review packages.
    Operates strictly outside the frozen pilot dataset directory.
    """

    DEFAULT_REGISTER_PATH = Path("data/07_batches/review/review_tracking_register.json")

    def __init__(self, register_path: Optional[Union[str, Path]] = None):
        self.register_path = Path(register_path or self.DEFAULT_REGISTER_PATH)
        self.entries: Dict[str, ReviewTrackerEntry] = {}
        if self.register_path.exists():
            self.load()

    def load(self) -> None:
        """Loads tracker entries from disk."""
        try:
            with open(self.register_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data.get("entries", []):
                    entry = ReviewTrackerEntry(**item)
                    self.entries[entry.example_id] = entry
            logger.info(f"Loaded {len(self.entries)} tracking records from {self.register_path}")
        except Exception as e:
            logger.error(f"Failed to load review tracker from {self.register_path}: {e}")
            raise

    def save(self) -> None:
        """Persists tracker entries to disk."""
        self.register_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": "1.0.0",
            "last_updated_utc": datetime.utcnow().isoformat() + "Z",
            "total_tracked_records": len(self.entries),
            "summary": self.get_summary(),
            "entries": [asdict(entry) for entry in sorted(self.entries.values(), key=lambda x: x.example_id)],
        }
        with open(self.register_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(self.entries)} tracking records to {self.register_path}")

    def initialize_from_datasets(
        self,
        pilot_path: Union[str, Path] = "data/03_generated/pilot_20_examples.jsonl",
        batch_01_path: Union[str, Path] = "data/07_batches/batch_01_candidates/batch_01_examples.jsonl",
        open_issues_path: Optional[Union[str, Path]] = "data/06_review/pilot_20_open_issues.md",
    ) -> int:
        """
        Initializes or refreshes the tracking register with entries from the frozen pilot
        and Batch 1 candidates, preserving any existing dispatch/import history.
        """
        pilot_path = Path(pilot_path)
        batch_01_path = Path(batch_01_path)

        count_added = 0

        # Load Pilot 20
        if pilot_path.exists():
            with open(pilot_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        doc = LegalQADocument(**json.loads(line))
                        if doc.qa_id not in self.entries:
                            # Map known open issues for specific pilot records
                            issues = []
                            if doc.qa_id == "QA-PILOT-DPDP-009":
                                issues.append("DPDP Section 44(2) 18-month computation vs IT Act s.43A omission")
                            elif doc.qa_id == "QA-PILOT-CROSS-010":
                                issues.append("BNSS Section 531(2)(a) CrPC 1973 repeal and savings distinction")
                            elif "DPDP" in doc.qa_id:
                                issues.append("DPDP Act 2023 uncommenced text vs in-force notice requirement")
                            elif "BSA" in doc.qa_id or "CROSS-001" in doc.qa_id or "CROSS-002" in doc.qa_id:
                                issues.append("BSA Section 61 admissibility subject to Section 63 certificate")

                            self.entries[doc.qa_id] = ReviewTrackerEntry(
                                example_id=doc.qa_id,
                                dataset_version="pilot_20_frozen_v1.2",
                                batch_id="PILOT-20",
                                package_identifier="PACKAGE_A_PILOT_20",
                                legal_domain=doc.legal_domain,
                                statutory_citations=doc.statutory_citations,
                                review_status=doc.legal_review_status.value,
                                sent_to_advocate=False,
                                response_received=False,
                                validation_passed=False,
                                imported=False,
                                outstanding_issues=issues,
                            )
                            count_added += 1

        # Load Batch 1 Candidates
        if batch_01_path.exists():
            with open(batch_01_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        doc = LegalQADocument(**json.loads(line))
                        if doc.qa_id not in self.entries:
                            self.entries[doc.qa_id] = ReviewTrackerEntry(
                                example_id=doc.qa_id,
                                dataset_version="batch_01_candidates_v1.0",
                                batch_id="BATCH-01",
                                package_identifier="PACKAGE_B_BATCH_01",
                                legal_domain=doc.legal_domain,
                                statutory_citations=doc.statutory_citations,
                                review_status=doc.legal_review_status.value,
                                sent_to_advocate=False,
                                response_received=False,
                                validation_passed=False,
                                imported=False,
                                outstanding_issues=[],
                            )
                            count_added += 1

        self.save()
        return count_added

    def update_dispatch(
        self,
        example_ids: List[str],
        sent_date: str,
        recipient_tag: Optional[str] = None,
    ) -> int:
        """Records that specific review packages were dispatched to an advocate."""
        updated = 0
        for eid in example_ids:
            if eid in self.entries:
                self.entries[eid].sent_to_advocate = True
                self.entries[eid].sent_date = sent_date
                if recipient_tag:
                    self.entries[eid].advocate_recipient_tag = recipient_tag
                updated += 1
        self.save()
        return updated

    def update_receipt(
        self,
        example_ids: List[str],
        response_date: str,
        validation_passed: bool,
        validation_report_ref: Optional[str] = None,
    ) -> int:
        """Records receipt and preliminary validation of returned reviews."""
        updated = 0
        for eid in example_ids:
            if eid in self.entries:
                self.entries[eid].response_received = True
                self.entries[eid].response_date = response_date
                self.entries[eid].validation_passed = validation_passed
                if validation_report_ref:
                    self.entries[eid].validation_report_ref = validation_report_ref
                updated += 1
        self.save()
        return updated

    def update_imported(
        self,
        example_ids: List[str],
        audit_reference: str,
        new_status_map: Optional[Dict[str, str]] = None,
    ) -> int:
        """Records successful import and links the immutable audit log reference."""
        updated = 0
        for eid in example_ids:
            if eid in self.entries:
                self.entries[eid].imported = True
                self.entries[eid].import_audit_reference = audit_reference
                if new_status_map and eid in new_status_map:
                    self.entries[eid].review_status = new_status_map[eid]
                updated += 1
        self.save()
        return updated

    def get_summary(self) -> Dict[str, Any]:
        """Calculates aggregate metrics across all tracked packages."""
        total = len(self.entries)
        by_package: Dict[str, int] = {}
        by_status: Dict[str, int] = {}
        sent_count = 0
        received_count = 0
        imported_count = 0

        for entry in self.entries.values():
            pkg = entry.package_identifier
            by_package[pkg] = by_package.get(pkg, 0) + 1

            st = entry.review_status
            by_status[st] = by_status.get(st, 0) + 1

            if entry.sent_to_advocate:
                sent_count += 1
            if entry.response_received:
                received_count += 1
            if entry.imported:
                imported_count += 1

        return {
            "total_records": total,
            "packages": by_package,
            "status_distribution": by_status,
            "dispatch_metrics": {
                "sent_count": sent_count,
                "unsent_count": total - sent_count,
            },
            "response_metrics": {
                "received_count": received_count,
                "pending_receipt_count": total - received_count,
            },
            "import_metrics": {
                "imported_count": imported_count,
                "unimported_count": total - imported_count,
            },
        }

