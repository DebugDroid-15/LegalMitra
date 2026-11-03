"""
Tests for Phase 102: e-Courts & NJDG Live CNR Case Tracker & AI Order Explainer.
"""
import pytest
from legalmitra.integrations.ecourts_client import ecourts_client

def test_cnr_validation_valid():
    valid_cnr = "MHAU010012342023"
    res = ecourts_client.validate_cnr(valid_cnr)
    assert res.is_valid is True
    assert res.state_code == "MH"
    assert res.district_code == "AU"
    assert res.establishment_code == "01"
    assert res.case_number == "001234"
    assert res.filing_year == 2023

def test_cnr_validation_invalid_length():
    res = ecourts_client.validate_cnr("MH123")
    assert res.is_valid is False
    assert "Invalid length" in res.error

def test_cnr_track_case_success():
    cnr = "DLHC010045672022"
    result = ecourts_client.track_case(cnr)
    assert result["success"] is True
    case = result["case"]
    assert case["cnr"] == cnr
    assert "Delhi" in case["court_name"]
    assert len(case["hearing_history"]) > 0
    assert "plain_language_summary" in case
    assert "en" in case["plain_language_summary"]
    assert len(case["procedural_advice"]) > 0
