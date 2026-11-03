"""
Unit tests for Phase 106: Commercial Contract Statutory Risk Auditor & Clause Redliner.
"""
import pytest
import os
from legalmitra.drafting.contract_redliner_engine import commercial_contract_auditor

def test_contract_audit_flags_noncompete_and_arbitrator():
    sample_contract = (
        "EMPLOYMENT AND VENDOR AGREEMENT\n"
        "1. Non-compete: Employee shall not engage in any competing business for 2 years post-termination.\n"
        "2. Dispute Resolution: The dispute shall be referred to a sole arbitrator appointed solely by company.\n"
        "3. Limitation: All legal proceedings must be initiated within 30 days.\n"
    )

    audit = commercial_contract_auditor.audit_contract_text(sample_contract, "Vendor Master Agreement")
    assert audit.composite_risk_score >= 50
    assert audit.critical_risks_count >= 2
    assert audit.high_risks_count >= 1
    assert any("Section 27" in c.statutory_reference for c in audit.analyzed_clauses)
    assert any("Perkins Eastman" in c.judicial_authority for c in audit.analyzed_clauses)

    # Test DOCX generation
    docx_path = commercial_contract_auditor.generate_docx_redline(audit)
    assert os.path.exists(docx_path)
    assert docx_path.endswith(".docx")
    assert os.path.getsize(docx_path) > 1000
