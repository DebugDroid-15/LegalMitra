"""Audit eCourts CIS ingestion protocol, CNR validation, and privacy gating."""

import json
import sys
from legalmitra.judicial.ecourts_protocol import (
    ECourtsProtocolValidator,
    ECourtsWorkflowStage,
)

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

def audit_ecourts():
    print("=== Workstream E eCourts CIS Protocol Audit ===")
    validator = ECourtsProtocolValidator()

    # 1. Manifest inspection
    manifest_path = "data/21_judicial_infrastructure/ecourts_sample_manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    records = data.get("records", [])
    print(f"Total manifest records: {len(records)}")
    
    for r in records:
        cnr = r["cnr_number"]
        decomp = validator.validate_cnr(cnr)
        print(f"\nRecord {r['record_id']} (CNR: {cnr}):")
        print(f"  Valid format: {decomp.is_valid} (State={decomp.state_code}, Dist={decomp.district_code}, Case={decomp.case_number}, Year={decomp.filing_year})")
        print(f"  Stage: {r['stage']}")
        print(f"  Retrieval eligible: {r['is_retrieval_eligible']}")
        print(f"  Training eligible: {r['is_training_eligible']} (Must be False!)")
        print(f"  Privacy classification: {r['privacy_classification']}")
        assert r['is_training_eligible'] is False, "Pretraining gate violation!"

    # 2. CNR Edge Cases
    print("\n--- Testing CNR Edge Cases ---")
    test_cases = [
        ("DLTH010012342023", True, "Valid Delhi Tis Hazari CNR"),
        ("MHCC020056782022", True, "Valid Mumbai City Civil CNR"),
        ("DLTH01001234202", False, "Invalid length (15 chars)"),
        ("DLTH0100123420239", False, "Invalid length (17 chars)"),
        ("12TH010012342023", False, "Invalid numeric state code"),
        ("DL12010012342023", False, "Invalid numeric district code"),
        ("DLTH010012341930", False, "Year out of range (1930)"),
        ("DLTH010012342045", False, "Year out of range (2045)"),
    ]
    for cnr_input, exp_valid, label in test_cases:
        res = validator.validate_cnr(cnr_input)
        matches = (res.is_valid == exp_valid)
        print(f"  [{'PASS' if matches else 'FAIL'}] {cnr_input} ({label}) -> is_valid={res.is_valid}")
        assert matches, f"Validation mismatch for {cnr_input}"

if __name__ == "__main__":
    audit_ecourts()
