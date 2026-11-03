"""
Unit tests for Phase 104: Pinpoint Gazette Source Peek & Citation Inspector.
"""
import pytest
from legalmitra.corpus.gazette_inspector import gazette_inspector

def test_gazette_inspect_bns_318():
    res = gazette_inspector.inspect_section("BNS", "318")
    assert "Act No. 45 of 2023" in res.statute_code
    assert "250894" in res.gazette_notification_no
    assert "1st July, 2024" in res.commencement_date
    assert "SHA256:" in res.digital_signature_hash
    assert res.is_in_force is True

def test_gazette_inspect_bnss_173():
    res = gazette_inspector.inspect_section("BNSS", "173")
    assert "Act No. 46 of 2023" in res.statute_code
    assert "electronic communication" in res.verbatim_text
    assert res.is_in_force is True
