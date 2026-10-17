"""
Tests for LegalMitra Phase 23 Advocate Review Workflow Operations.
Covers:
- Role-based authorization matrix
- Bar Council credential validation
- Deterministic state machine transitions
- Dry-run validation and review package export/import
- Preservation of freeze integrity
"""

import json
from pathlib import Path
import pytest

from legalmitra.review.workflow import (
    AdvocateCredentials,
    AdvocateReviewWorkflow,
    ReviewAction,
    ReviewDecision,
    ReviewStatus,
    ReviewSubmission,
    UserRole,
)


@pytest.fixture
def workflow(tmp_path):
    audit_file = tmp_path / "audit.jsonl"
    return AdvocateReviewWorkflow(audit_log_path=audit_file)


@pytest.fixture
def valid_credentials():
    return AdvocateCredentials(
        advocate_name="Adv. Rajesh Kumar",
        bar_council_id="D/1945/2012",
        state_bar_council="Bar Council of Delhi",
        enrollment_year=2012,
        role=UserRole.ADVOCATE_REVIEWER,
    )


class TestAuthorizationMatrix:
    """Verify role-based access control for review actions."""

    def test_advocate_reviewer_permissions(self, workflow):
        role = UserRole.ADVOCATE_REVIEWER
        assert workflow.check_authorization(role, ReviewAction.START_REVIEW) is True
        assert workflow.check_authorization(role, ReviewAction.SUBMIT_DECISION) is True
        assert workflow.check_authorization(role, ReviewAction.APPROVE) is True
        assert workflow.check_authorization(role, ReviewAction.EXPORT_PACKAGE) is False
        assert workflow.check_authorization(role, ReviewAction.IMPORT_PACKAGE) is False

    def test_researcher_permissions(self, workflow):
        role = UserRole.LEGAL_RESEARCHER
        assert workflow.check_authorization(role, ReviewAction.START_REVIEW) is False
        assert workflow.check_authorization(role, ReviewAction.SUBMIT_DECISION) is False
        assert workflow.check_authorization(role, ReviewAction.EXPORT_PACKAGE) is True

    def test_admin_permissions(self, workflow):
        role = UserRole.SYSTEM_ADMIN
        assert workflow.check_authorization(role, ReviewAction.IMPORT_PACKAGE) is True
        assert workflow.check_authorization(role, ReviewAction.EXPORT_PACKAGE) is True
        assert workflow.check_authorization(role, ReviewAction.SUBMIT_DECISION) is False


class TestCredentialValidation:
    """Verify bar council credential integrity."""

    def test_valid_credentials(self, valid_credentials):
        ok, errors = valid_credentials.is_valid()
        assert ok is True
        assert len(errors) == 0

    def test_invalid_bar_council_id(self):
        creds = AdvocateCredentials(
            advocate_name="Adv. Sharma",
            bar_council_id="INVALID_ID_WITHOUT_SLASH",
            state_bar_council="Delhi",
            enrollment_year=2018,
        )
        ok, errors = creds.is_valid()
        assert ok is False
        assert any("Bar council ID must follow" in e for e in errors)


class TestStateTransitions:
    """Verify valid and invalid state transitions."""

    def test_valid_lifecycle_progression(self, workflow, valid_credentials):
        # 1. PENDING -> UNDER_REVIEW
        ok, errs = workflow.validate_transition(
            ReviewStatus.PENDING_LEGAL_REVIEW, ReviewStatus.UNDER_REVIEW
        )
        assert ok is True

        # 2. UNDER_REVIEW -> APPROVED with valid credentials
        ok, errs = workflow.validate_transition(
            ReviewStatus.UNDER_REVIEW, ReviewStatus.APPROVED, credentials=valid_credentials
        )
        assert ok is True

    def test_illegal_jump_to_approved_without_credentials(self, workflow):
        ok, errs = workflow.validate_transition(
            ReviewStatus.PENDING_LEGAL_REVIEW, ReviewStatus.APPROVED, credentials=None
        )
        assert ok is False
        assert any("Illegal state transition" in e for e in errs)

    def test_missing_credentials_on_approval(self, workflow):
        ok, errs = workflow.validate_transition(
            ReviewStatus.UNDER_REVIEW, ReviewStatus.APPROVED, credentials=None
        )
        assert ok is False
        assert any("Advocate credentials required" in e for e in errs)


class TestDryRunSubmission:
    """Verify dry-run execution does not modify storage."""

    def test_dry_run_approval_successful(self, workflow, valid_credentials):
        submission = ReviewSubmission(
            example_id="EX-TEST-001",
            target_status=ReviewStatus.APPROVED,
            reviewer=valid_credentials,
            rationale="Provision citing Section 482 BNSS matches statutory text accurately.",
            score=4.5,
        )
        res = workflow.process_review_submission(
            current_status=ReviewStatus.UNDER_REVIEW,
            submission=submission,
            dry_run=True,
        )
        assert res["success"] is True
        assert res["dry_run"] is True
        # Audit file should be empty in dry-run
        assert not workflow.audit_log_path.exists() or workflow.audit_log_path.stat().st_size == 0

    def test_rejection_without_rationale_fails(self, workflow, valid_credentials):
        submission = ReviewSubmission(
            example_id="EX-TEST-002",
            target_status=ReviewStatus.REJECTED,
            reviewer=valid_credentials,
            rationale="Too short",
            score=2.0,
        )
        res = workflow.process_review_submission(
            current_status=ReviewStatus.UNDER_REVIEW,
            submission=submission,
            dry_run=True,
        )
        assert res["success"] is False
        assert any("legal rationale (min 15 chars)" in e for e in res["errors"])


class TestPackageExportAndImport:
    """Verify export and dry-run import of review packages."""

    def test_export_and_dry_run_import(self, workflow, tmp_path):
        pkg_file = tmp_path / "test_package.json"
        sample_records = [
            {"example_id": "REC-01", "legal_review_status": "pending_legal_review"},
            {"example_id": "REC-02", "legal_review_status": "under_review"},
        ]

        # Export by researcher
        export_res = workflow.export_review_package(
            package_id="PKG-TEST-01",
            records=sample_records,
            output_file=pkg_file,
            actor_role=UserRole.LEGAL_RESEARCHER,
        )
        assert export_res["record_count"] == 2
        assert pkg_file.exists()

        # Import dry-run by admin
        import_res = workflow.import_review_package(
            package_file=pkg_file,
            actor_role=UserRole.SYSTEM_ADMIN,
            dry_run=True,
        )
        assert import_res["success"] is True
        assert import_res["total_records"] == 2
        assert import_res["valid_records"] == 2

