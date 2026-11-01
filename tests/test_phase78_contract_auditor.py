"""Tests for Phase 78: Commercial Contract & Agreement Risk Auditor Engine."""

import pytest
from legalmitra.drafting.contract_auditor import (
    ContractRiskAuditorEngine,
    ContractAuditReport,
    RiskSeverity,
)

SAMPLE_RISKY_EMPLOYMENT_AGREEMENT = """
MASTER EMPLOYMENT & CONSULTANCY AGREEMENT

1. Non-Compete Covenant:
The Employee agrees that following termination of employment for any reason, the Employee shall not engage in any competing business for a period of 2 years within India.

2. Limitation of Action:
Any dispute or claim by the Employee arising under this agreement must be filed within 90 days of the cause of action, failing which all claims shall be permanently extinguished.

3. Dispute Resolution & Arbitration:
All disputes shall be referred to a sole arbitrator who shall be appointed unilaterally by the Managing Director of the Company. The venue of arbitration shall be Mumbai.

4. Indemnity:
The Consultant shall indemnify the Client from and against any and all losses, damages, liabilities, costs, and expenses without any limitation whatsoever.
"""

SAMPLE_CLEAN_COMMERCIAL_CONTRACT = """
STANDARD SERVICES AGREEMENT

1. Confidentiality:
Both parties agree to protect Proprietary Information during the term of this agreement and for three years thereafter.

2. Dispute Resolution:
The parties agree that all disputes shall be resolved by mutual consultation. If unresolved, the dispute shall be referred to a sole arbitrator appointed by mutual consent of both parties. The Seat and Venue of arbitration shall be New Delhi.

3. Limitation of Liability:
Neither party shall be liable for indirect damages. The aggregate liability of either party shall be capped at the total amount paid under this agreement.
"""


class TestPhase78ContractAuditor:
    """Test suite certifying Contract Risk Auditor Engine."""

    def test_audit_void_non_compete_section_27(self):
        """Verify detection of post-termination non-compete void under Section 27."""
        report = ContractRiskAuditorEngine.audit_contract(SAMPLE_RISKY_EMPLOYMENT_AGREEMENT, "Executive Employment Agreement")
        
        nc_findings = [f for f in report.findings if f.clause_category == "Non-Compete & Restraint of Trade"]
        assert len(nc_findings) == 1
        assert nc_findings[0].severity == RiskSeverity.CRITICAL
        assert "Section 27" in nc_findings[0].governing_statute
        assert "Zaheer Khan" in nc_findings[0].judicial_authority

    def test_audit_void_limitation_curtailment_section_28(self):
        """Verify detection of clause curtailing 3-year limitation period under Section 28."""
        report = ContractRiskAuditorEngine.audit_contract(SAMPLE_RISKY_EMPLOYMENT_AGREEMENT)
        
        lim_findings = [f for f in report.findings if "Limitation" in f.clause_category]
        assert len(lim_findings) == 1
        assert lim_findings[0].severity == RiskSeverity.CRITICAL
        assert "Section 28" in lim_findings[0].governing_statute

    def test_audit_unilateral_arbitrator_perkins_eastman(self):
        """Verify detection of unilateral sole arbitrator nomination under Perkins Eastman ratio."""
        report = ContractRiskAuditorEngine.audit_contract(SAMPLE_RISKY_EMPLOYMENT_AGREEMENT)
        
        arb_findings = [f for f in report.findings if f.clause_category == "Arbitration Appointment Neutrality"]
        assert len(arb_findings) == 1
        assert arb_findings[0].severity == RiskSeverity.HIGH
        assert "Section 12(5)" in arb_findings[0].governing_statute
        assert "Perkins Eastman" in arb_findings[0].judicial_authority

    def test_audit_seat_vs_venue_ambiguity(self):
        """Verify detection of venue without seat designation (BALCO ratio)."""
        report = ContractRiskAuditorEngine.audit_contract(SAMPLE_RISKY_EMPLOYMENT_AGREEMENT)
        
        venue_findings = [f for f in report.findings if f.clause_category == "Dispute Resolution Jurisdiction"]
        assert len(venue_findings) == 1
        assert venue_findings[0].severity == RiskSeverity.MEDIUM
        assert "BALCO" in venue_findings[0].judicial_authority

    def test_audit_uncapped_indemnity(self):
        """Verify detection of uncapped, asymmetric indemnity."""
        report = ContractRiskAuditorEngine.audit_contract(SAMPLE_RISKY_EMPLOYMENT_AGREEMENT)
        
        indem_findings = [f for f in report.findings if "Indemnity" in f.clause_category]
        assert len(indem_findings) == 1
        assert indem_findings[0].severity == RiskSeverity.HIGH

    def test_composite_risk_score_and_verdict(self):
        """Verify composite risk scoring and non-compliant verdict for high-risk contract."""
        report = ContractRiskAuditorEngine.audit_contract(SAMPLE_RISKY_EMPLOYMENT_AGREEMENT)
        assert report.composite_risk_score >= 80
        assert "NON-COMPLIANT" in report.overall_compliance_verdict
        assert report.critical_risks_count >= 2

    def test_clean_contract_audit_results(self):
        """Verify that a balanced, compliant contract receives 0 risk score and compliant verdict."""
        report = ContractRiskAuditorEngine.audit_contract(SAMPLE_CLEAN_COMMERCIAL_CONTRACT, "Standard Services")
        assert report.critical_risks_count == 0
        assert report.high_risks_count == 0
        assert report.composite_risk_score == 0
        assert "COMPLIANT" in report.overall_compliance_verdict
        assert "No critical statutory violations detected" in report.executive_summary_markdown
