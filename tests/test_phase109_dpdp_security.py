"""
Unit tests for Phase 109: Enterprise Security, RBAC & DPDP Compliance.
"""
import pytest
from legalmitra.security.dpdp_engine import dpdp_compliance_engine, UserRole

def test_dpdp_pii_scrubbing_aadhaar_pan_phone():
    sample = (
        "Complainant Rajesh Kumar, Aadhaar: 5412 8901 2345, PAN: ABCDE1234F, "
        "Phone: +91 9876543210, Email: rajesh.k@example.com reported cheating."
    )
    result = dpdp_compliance_engine.scrub_pii(sample)
    
    assert "[REDACTED_AADHAAR]" in result.sanitized_text
    assert "[REDACTED_PAN]" in result.sanitized_text
    assert "[REDACTED_PHONE]" in result.sanitized_text
    assert "[REDACTED_EMAIL]" in result.sanitized_text
    assert result.redacted_items_count == 4
    assert "AADHAAR_NUMBER" in result.redaction_types_found
    assert result.dpdp_compliance_tag == "SEC_8_DPDP_COMPLIANT_ZERO_RETENTION"

def test_dpdp_consent_generation():
    consent = dpdp_compliance_engine.generate_consent_record("USR-1002")
    assert consent.consent_id.startswith("DPDP-")
    assert consent.consent_valid is True
    assert "Session Only" in consent.data_retention_period

def test_rbac_authorization_matrix():
    assert dpdp_compliance_engine.authorize_action(UserRole.LITIGANT, "ask_query") is True
    assert dpdp_compliance_engine.authorize_action(UserRole.LITIGANT, "audit_contract") is False
    assert dpdp_compliance_engine.authorize_action(UserRole.SENIOR_PARTNER, "audit_contract") is True
    assert dpdp_compliance_engine.authorize_action(UserRole.SYSTEM_ADMIN, "any_privileged_task") is True
