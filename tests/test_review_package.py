"""
Test suite for Advocate Review Package in data/06_review/.
Verifies file existence, schema compliance, blank decision fields,
pending review status, and coverage of the 6 prioritized legal ambiguities.
"""

import csv
import json
from pathlib import Path
import pytest


def test_review_package_files_exist():
    review_dir = Path("data/06_review")
    assert review_dir.exists()

    guide_file = review_dir / "ADVOCATE_REVIEW_GUIDE.md"
    sheet_file = review_dir / "pilot_20_review_sheet.csv"
    bundle_file = review_dir / "pilot_20_source_bundle.json"
    issues_file = review_dir / "pilot_20_open_issues.md"

    assert guide_file.exists(), "ADVOCATE_REVIEW_GUIDE.md must exist"
    assert sheet_file.exists(), "pilot_20_review_sheet.csv must exist"
    assert bundle_file.exists(), "pilot_20_source_bundle.json must exist"
    assert issues_file.exists(), "pilot_20_open_issues.md must exist"


def test_review_sheet_structure_and_blank_decisions():
    sheet_file = Path("data/06_review/pilot_20_review_sheet.csv")
    with open(sheet_file, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 20, f"Expected 20 records in review sheet, found {len(rows)}"

    for row in rows:
        # Stable record ID
        assert row["record_id"].startswith("QA-PILOT-")
        assert len(row["question"]) > 10
        assert len(row["proposed_answer"]) > 10
        assert row["legal_as_of_date"] == "2026-10-16"
        assert row["commencement_notification"] != ""
        assert row["statutory_citations"] != ""
        assert row["source_urls"] != ""
        assert row["verbatim_evidence_passages"] != ""
        assert len(row["specific_advocate_question"]) > 15

        # Decision and score fields MUST be blank pending human review
        assert row["review_decision"] == "", "Decision must be blank pending advocate review"
        assert row["legal_accuracy_score_1_to_5"] == ""
        assert row["temporal_accuracy_score_1_to_5"] == ""
        assert row["grounding_accuracy_score_1_to_5"] == ""
        assert row["reviewer_comments"] == ""
        assert row["reviewer_name_initials"] == ""
        assert row["review_date"] == ""


def test_source_bundle_json_structure():
    bundle_file = Path("data/06_review/pilot_20_source_bundle.json")
    with open(bundle_file, "r", encoding="utf-8") as f:
        bundle = json.load(f)

    assert bundle["total_records"] == 20
    assert bundle["review_status_summary"]["pending_legal_review"] == 20
    assert bundle["review_status_summary"]["approved"] == 0
    assert bundle["review_status_summary"]["rejected"] == 0
    assert bundle["review_status_summary"]["revision_required"] == 0

    records = bundle["records"]
    assert len(records) == 20

    for rec in records:
        assert rec["review_status"] == "pending_legal_review"
        assert rec["decision"] is None
        assert len(rec["supporting_sources"]) >= 1
        assert len(rec["evidence_passages"]) >= 1
        for s in rec["supporting_sources"]:
            assert s["document_id"] != "IND-JUD-DEL-2024-BAIL"
            assert s["source_url"].startswith("http")


def test_open_issues_covers_all_six_priorities():
    issues_file = Path("data/06_review/pilot_20_open_issues.md")
    content = issues_file.read_text(encoding="utf-8")

    assert "Issue 1: BNSS Section 482(4)" in content
    assert "Issue 2: IT Act Section 43A" in content
    assert "Issue 3: DPDP Act Section 6(9)" in content
    assert "Issue 4: BNSS Section 531" in content
    assert "Issue 5: BSA Section 63" in content
    assert "Issue 6: Extrapolation Beyond Cited Statutory Text" in content

