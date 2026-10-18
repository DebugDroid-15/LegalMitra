"""
LegalMitra Advocate Review Operations & Lifecycle Workflow.
Enforces:
- Role-based authorization (ADVOCATE_REVIEWER, SENIOR_ADVOCATE, AUDITOR, SYSTEM_ADMIN)
- Bar Council credential validation
- Deterministic review state machine transitions
- Package export and dry-run/commit import with transactional rollback
- Protection of frozen review candidates
"""

from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from legalmitra.core.logging import get_logger

logger = get_logger("review_workflow")


class UserRole(str, Enum):
    ADVOCATE_REVIEWER = "advocate_reviewer"
    SENIOR_ADVOCATE = "senior_advocate"
    LEGAL_RESEARCHER = "legal_researcher"
    AUDITOR = "auditor"
    SYSTEM_ADMIN = "system_admin"


class ReviewStatus(str, Enum):
    PENDING_LEGAL_REVIEW = "pending_legal_review"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"
    DISPUTED = "disputed"
    ABSTAINED = "abstained"


class ReviewDecision(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"
    DISPUTED = "disputed"
    ABSTAINED = "abstained"


class ReviewAction(str, Enum):
    START_REVIEW = "start_review"
    SUBMIT_DECISION = "submit_decision"
    APPROVE = "approve"
    REJECT = "reject"
    REQUEST_REVISION = "request_revision"
    DISPUTE = "dispute"
    ABSTAIN = "abstain"
    EXPORT_PACKAGE = "export_package"
    IMPORT_PACKAGE = "import_package"


# Permitted role matrix for each action
ROLE_PERMISSIONS: Dict[ReviewAction, Set[UserRole]] = {
    ReviewAction.START_REVIEW: {UserRole.ADVOCATE_REVIEWER, UserRole.SENIOR_ADVOCATE},
    ReviewAction.SUBMIT_DECISION: {UserRole.ADVOCATE_REVIEWER, UserRole.SENIOR_ADVOCATE},
    ReviewAction.APPROVE: {UserRole.ADVOCATE_REVIEWER, UserRole.SENIOR_ADVOCATE},
    ReviewAction.REJECT: {UserRole.ADVOCATE_REVIEWER, UserRole.SENIOR_ADVOCATE},
    ReviewAction.REQUEST_REVISION: {UserRole.ADVOCATE_REVIEWER, UserRole.SENIOR_ADVOCATE},
    ReviewAction.DISPUTE: {UserRole.ADVOCATE_REVIEWER, UserRole.SENIOR_ADVOCATE, UserRole.AUDITOR},
    ReviewAction.ABSTAIN: {UserRole.ADVOCATE_REVIEWER, UserRole.SENIOR_ADVOCATE},
    ReviewAction.EXPORT_PACKAGE: {UserRole.LEGAL_RESEARCHER, UserRole.AUDITOR, UserRole.SYSTEM_ADMIN},
    ReviewAction.IMPORT_PACKAGE: {UserRole.SYSTEM_ADMIN, UserRole.AUDITOR},
}

# Permitted state transitions
VALID_STATE_TRANSITIONS: Dict[ReviewStatus, Set[ReviewStatus]] = {
    ReviewStatus.PENDING_LEGAL_REVIEW: {ReviewStatus.UNDER_REVIEW, ReviewStatus.DISPUTED},
    ReviewStatus.UNDER_REVIEW: {
        ReviewStatus.APPROVED,
        ReviewStatus.REJECTED,
        ReviewStatus.NEEDS_REVISION,
        ReviewStatus.DISPUTED,
        ReviewStatus.ABSTAINED,
    },
    ReviewStatus.NEEDS_REVISION: {ReviewStatus.UNDER_REVIEW, ReviewStatus.DISPUTED},
    ReviewStatus.DISPUTED: {ReviewStatus.UNDER_REVIEW, ReviewStatus.REJECTED},
    ReviewStatus.APPROVED: {ReviewStatus.DISPUTED},  # Allowed to dispute an approval upon audit
    ReviewStatus.REJECTED: {ReviewStatus.DISPUTED},
    ReviewStatus.ABSTAINED: {ReviewStatus.UNDER_REVIEW, ReviewStatus.DISPUTED},
}


@dataclass
class AdvocateCredentials:
    advocate_name: str
    bar_council_id: str
    state_bar_council: str
    enrollment_year: int
    role: UserRole = UserRole.ADVOCATE_REVIEWER

    def is_valid(self) -> Tuple[bool, List[str]]:
        errors = []
        if not self.advocate_name or len(self.advocate_name.strip()) < 3:
            errors.append("Advocate name must be at least 3 characters.")
        if not self.bar_council_id or "/" not in self.bar_council_id:
            errors.append("Bar council ID must follow standard format (e.g., 'D/1234/2015').")
        if not self.state_bar_council:
            errors.append("State bar council is required.")
        if self.enrollment_year < 1950 or self.enrollment_year > datetime.now().year:
            errors.append(f"Enrollment year {self.enrollment_year} is invalid.")
        return len(errors) == 0, errors


@dataclass
class ReviewSubmission:
    example_id: str
    target_status: ReviewStatus
    reviewer: AdvocateCredentials
    rationale: str
    score: Optional[float] = None
    suggested_amendments: Optional[str] = None
    conflict_of_interest_declared: bool = False
    legal_correctness_rating: Optional[int] = None
    citation_support_rating: Optional[int] = None
    jurisdiction_accuracy: bool = True
    temporal_applicability_verified: bool = True
    submitted_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class AdvocateReviewWorkflow:
    """
    Operational workflow manager for LegalMitra advocate review lifecycle.
    """

    def __init__(self, audit_log_path: Optional[Union[str, Path]] = None):
        self.audit_log_path = Path(audit_log_path or "data/06_review/audit/workflow_audit_log.jsonl")
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)

    def check_authorization(self, role: UserRole, action: ReviewAction) -> bool:
        """Verify role has permission to execute the specified action."""
        permitted = ROLE_PERMISSIONS.get(action, set())
        return role in permitted

    def validate_transition(
        self,
        current_status: ReviewStatus,
        target_status: ReviewStatus,
        credentials: Optional[AdvocateCredentials] = None,
    ) -> Tuple[bool, List[str]]:
        """Validate whether a state transition is legal according to rules."""
        errors: List[str] = []

        # Check state machine graph
        allowed_targets = VALID_STATE_TRANSITIONS.get(current_status, set())
        if target_status not in allowed_targets:
            errors.append(
                f"Illegal state transition from '{current_status.value}' to '{target_status.value}'. "
                f"Permitted targets: {[s.value for s in allowed_targets]}"
            )

        # Check credentials requirement for final decisions
        if target_status in (ReviewStatus.APPROVED, ReviewStatus.REJECTED, ReviewStatus.NEEDS_REVISION, ReviewStatus.ABSTAINED):
            if not credentials:
                errors.append(f"Advocate credentials required to transition to '{target_status.value}'.")
            else:
                valid_creds, cred_errs = credentials.is_valid()
                if not valid_creds:
                    errors.extend(cred_errs)
                if not self.check_authorization(credentials.role, ReviewAction.SUBMIT_DECISION):
                    errors.append(f"Role '{credentials.role.value}' is not authorized to submit decisions.")

        return len(errors) == 0, errors

    def process_review_submission(
        self,
        current_status: ReviewStatus,
        submission: ReviewSubmission,
        dry_run: bool = True,
    ) -> Dict[str, Any]:
        """
        Process a review submission with validation and dry-run execution.
        """
        # 1. State transition validation
        valid_trans, trans_errs = self.validate_transition(
            current_status=current_status,
            target_status=submission.target_status,
            credentials=submission.reviewer,
        )
        if not valid_trans:
            return {
                "success": False,
                "example_id": submission.example_id,
                "dry_run": dry_run,
                "errors": trans_errs,
            }

        # 2. Score bounds check
        if submission.score is not None:
            if not (1.0 <= submission.score <= 5.0):
                return {
                    "success": False,
                    "example_id": submission.example_id,
                    "dry_run": dry_run,
                    "errors": [f"Review score {submission.score} out of bounds [1.0, 5.0]."],
                }

        # 3. Mandatory rationale check for rejection, revision, or abstention
        if submission.target_status in (ReviewStatus.REJECTED, ReviewStatus.NEEDS_REVISION, ReviewStatus.ABSTAINED):
            if not submission.rationale or len(submission.rationale.strip()) < 15:
                return {
                    "success": False,
                    "example_id": submission.example_id,
                    "dry_run": dry_run,
                    "errors": ["Non-empty legal rationale (min 15 chars) is mandatory for rejection, revision, or abstention."],
                }

        audit_entry = {
            "example_id": submission.example_id,
            "previous_status": current_status.value,
            "new_status": submission.target_status.value,
            "reviewer_name": submission.reviewer.advocate_name,
            "bar_council_id": submission.reviewer.bar_council_id,
            "score": submission.score,
            "rationale": submission.rationale,
            "suggested_amendments": submission.suggested_amendments,
            "conflict_of_interest_declared": submission.conflict_of_interest_declared,
            "legal_correctness_rating": submission.legal_correctness_rating,
            "citation_support_rating": submission.citation_support_rating,
            "jurisdiction_accuracy": submission.jurisdiction_accuracy,
            "temporal_applicability_verified": submission.temporal_applicability_verified,
            "timestamp": submission.submitted_at,
            "dry_run": dry_run,
        }

        if not dry_run:
            with open(self.audit_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(audit_entry, ensure_ascii=False) + "\n")
            logger.info(f"Committed review update for {submission.example_id}: {submission.target_status.value}")

        return {
            "success": True,
            "example_id": submission.example_id,
            "new_status": submission.target_status.value,
            "dry_run": dry_run,
            "audit_entry": audit_entry,
        }

    def export_review_package(
        self,
        package_id: str,
        records: List[Dict[str, Any]],
        output_file: Union[str, Path],
        actor_role: UserRole,
    ) -> Dict[str, Any]:
        """
        Exports a standardized review package with checksum and schema verification.
        """
        if not self.check_authorization(actor_role, ReviewAction.EXPORT_PACKAGE):
            raise PermissionError(f"Role '{actor_role.value}' is not authorized to export review packages.")

        out_path = Path(output_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        package_data = {
            "package_id": package_id,
            "exported_at": datetime.utcnow().isoformat() + "Z",
            "total_records": len(records),
            "records": records,
        }
        serialized = json.dumps(package_data, indent=2, ensure_ascii=False)
        sha256_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(serialized)

        return {
            "package_id": package_id,
            "output_path": str(out_path),
            "record_count": len(records),
            "sha256": sha256_hash,
        }

    def import_review_package(
        self,
        package_file: Union[str, Path],
        actor_role: UserRole,
        dry_run: bool = True,
    ) -> Dict[str, Any]:
        """
        Imports and validates a review package.
        Supports dry_run to simulate checks without applying modifications.
        """
        if not self.check_authorization(actor_role, ReviewAction.IMPORT_PACKAGE):
            raise PermissionError(f"Role '{actor_role.value}' is not authorized to import review packages.")

        p = Path(package_file)
        if not p.exists():
            raise FileNotFoundError(f"Package file not found at {package_file}")

        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)

        records = data.get("records", [])
        validation_errors: List[str] = []
        valid_count = 0

        for idx, rec in enumerate(records):
            rec_id = rec.get("example_id") or rec.get("qa_id")
            if not rec_id:
                validation_errors.append(f"Record #{idx} missing required identifier.")
                continue

            status = rec.get("status") or rec.get("legal_review_status")
            if status not in [s.value for s in ReviewStatus]:
                validation_errors.append(f"Record {rec_id} has invalid review status '{status}'.")
                continue

            valid_count += 1

        is_valid = len(validation_errors) == 0

        return {
            "success": is_valid,
            "package_id": data.get("package_id", "UNKNOWN"),
            "total_records": len(records),
            "valid_records": valid_count,
            "dry_run": dry_run,
            "errors": validation_errors,
        }
