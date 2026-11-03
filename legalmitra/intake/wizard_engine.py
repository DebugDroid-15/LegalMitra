"""
Phase 100: Guided Conversational Citizen Intake Wizard
Enables grassroots citizens and non-lawyers to articulate their grievances through a
friendly 3-step conversational intake wizard:
1. What happened? (Plain language / Colloquial / Multi-dialect Indic text or voice)
2. When did it happen? (Evaluates IPC vs BNS / Limitation Act applicability)
3. Where did it happen? (Maps State jurisdiction, High Court territoriality, and Local Police / CDRC forum)

Automatically structures citizen inputs into an authoritative, taxonomically classified legal query
ready for instant execution by the 15-stage IRAC RAG engine.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("citizen_intake_wizard")


class BroadDomainCategory(str, Enum):
    CRIMINAL_POLICE = "criminal_police"
    FINANCIAL_CYBER = "financial_cyber"
    CONSUMER_COMMERCE = "consumer_commerce"
    PROPERTY_TENANCY = "property_tenancy"
    EMPLOYMENT_LABOUR = "employment_labour"
    FAMILY_MATRIMONIAL = "family_matrimonial"
    GENERAL_CIVIL = "general_civil"


@dataclass
class CitizenIntakeInput:
    incident_description: str
    incident_date_str: str
    state_or_city: str
    user_goal: Optional[str] = None
    language: str = "mr"


@dataclass
class StructuredLegalIntakeResult:
    success: bool
    broad_domain: str
    statutory_governance_framework: str
    temporal_applicability: str
    competent_forum: str
    suggested_statutes: List[str]
    synthesized_legal_query: str
    immediate_citizen_actions: List[str]
    recommended_notice_template: Optional[str] = None
    recommended_limitation_category: Optional[str] = None


class CitizenIntakeWizardEngine:
    """
    Translates raw citizen narratives into structured statutory queries.
    """

    # Domain keyword patterns
    DOMAIN_PATTERNS = [
        (BroadDomainCategory.CRIMINAL_POLICE, r'(?:पोलीस|police|fir|एफआयआर|तक्रार|मारहाण|धमकी|अटक|arrest|theft|चोरी|assault|fir नकार|refusal)'),
        (BroadDomainCategory.FINANCIAL_CYBER, r'(?:cyber|सायबर|ऑनलाइन|upi|cheque|चेक|बँक|bank|खाते|fraud|scam|420|पैसे|money transfer)'),
        (BroadDomainCategory.CONSUMER_COMMERCE, r'(?:consumer|ग्राहक|amazon|flipkart|खरेदी|defective|खराब|वारंटी|warranty|refund|पैसे परत|service)'),
        (BroadDomainCategory.PROPERTY_TENANCY, r'(?:घर|land|जमीन|भाडे|भाडेकरू|tenant|landlord|मालक|खरेदीखत|evict|ताबा|possession)'),
        (BroadDomainCategory.EMPLOYMENT_LABOUR, r'(?:कंपनी|company|नोकरी|job|पगार|salary|termination|काढून टाकले|pf|provident fund)'),
        (BroadDomainCategory.FAMILY_MATRIMONIAL, r'(?:पती|पत्नी|divorce|घटस्फोट|maintenance|पोटगी|custody|मुले|वारस|succession)')
    ]

    def classify_domain(self, text: str) -> BroadDomainCategory:
        """Determines the broad domain from citizen description."""
        for domain, pattern in self.DOMAIN_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return domain
        return BroadDomainCategory.GENERAL_CIVIL

    def evaluate_temporal_applicability(self, date_str: str) -> Tuple[str, str]:
        """
        Determines whether IPC or BNS applies based on the 1 July 2024 cutoff.
        """
        try:
            # Try YYYY-MM-DD or DD-MM-YYYY
            if "-" in date_str:
                parts = date_str.split("-")
                if len(parts[0]) == 4:
                    dt = datetime.strptime(date_str, "%Y-%m-%d").date()
                else:
                    dt = datetime.strptime(date_str, "%d-%m-%Y").date()
            else:
                dt = date.today()
        except Exception:
            dt = date.today()

        cutoff = date(2024, 7, 1)
        if dt < cutoff:
            framework = "Indian Penal Code, 1860 (IPC) & Code of Criminal Procedure, 1973 (CrPC)"
            reason = f"Incident occurred on {dt.strftime('%d-%m-%Y')} (prior to 1 July 2024). Substantive penal law remains IPC per Article 20(1) Constitution of India."
        else:
            framework = "Bharatiya Nyaya Sanhita, 2023 (BNS) & Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)"
            reason = f"Incident occurred on {dt.strftime('%d-%m-%Y')} (on/after 1 July 2024). Governed fully by New Criminal Codes (BNS, BNSS, BSA, 2023)."

        return framework, reason

    def resolve_intake(self, intake: CitizenIntakeInput) -> StructuredLegalIntakeResult:
        """
        Main pipeline executing the 3-step structured citizen intake.
        """
        domain = self.classify_domain(intake.incident_description)
        framework, temporal_reason = self.evaluate_temporal_applicability(intake.incident_date_str)
        loc = intake.state_or_city.strip() or "Concerned District / State"

        suggested_statutes = []
        immediate_actions = []
        notice_template = None
        limitation_cat = None

        if domain == BroadDomainCategory.CRIMINAL_POLICE:
            forum = f"Competent Judicial Magistrate Court & Office of SP/DCP, {loc}"
            if "BNS" in framework:
                suggested_statutes = ["Section 173(4) BNSS (FIR Refusal Representation)", "Section 175(3) BNSS (Magistrate Application)", "Section 47 BNSS (Arrest Rights)"]
            else:
                suggested_statutes = ["Section 154(3) CrPC (FIR Refusal Representation)", "Section 156(3) CrPC (Magistrate Application)"]
            immediate_actions = [
                "Preserve all written complaints submitted at the police station with official in-ward acknowledgment stamp.",
                "Send written representation to the Superintendent of Police (SP) / DCP under Section 173(4) BNSS via Registered Post.",
                "In emergency threats or immediate bodily harm, dial National Emergency Helpline 112."
            ]
            notice_template = "police_fir_refusal_sp"
            synthesized_query = f"Remedies under {framework} for police refusal to record FIR in {loc} regarding: {intake.incident_description}"

        elif domain == BroadDomainCategory.FINANCIAL_CYBER:
            forum = f"Cyber Crime Police Station, {loc} & National Cyber Crime Reporting Portal"
            suggested_statutes = ["Information Technology Act, 2000 (Section 66D)", "Section 318(4) BNS / Section 420 IPC (Cheating)", "Section 138 Negotiable Instruments Act"]
            immediate_actions = [
                "Immediately call National Cyber Crime Helpline 1930 to freeze fraudulent fund transaction within Golden Hour.",
                "Lodge formal complaint on cybercrime.gov.in and download the acknowledgment receipt.",
                "Submit formal dispute form to your bank along with transaction reference numbers (UTR)."
            ]
            notice_template = "cheque_dishonour_138"
            limitation_cat = "cheque_dishonour_138"
            synthesized_query = f"Legal remedies and helpline procedure for financial cyber fraud / cheating under {framework} in {loc}: {intake.incident_description}"

        elif domain == BroadDomainCategory.CONSUMER_COMMERCE:
            forum = f"District Consumer Disputes Redressal Commission (DCDRC), {loc} & e-Daakhil Portal"
            suggested_statutes = ["Section 35 Consumer Protection Act, 2019", "Section 2(11) Deficiency of Service", "Section 2(47) Unfair Trade Practice"]
            immediate_actions = [
                "Preserve purchase invoice, warranty card, and customer support email threads.",
                "Send formal 15-day pre-litigation legal notice under Consumer Protection Act demanding refund or replacement.",
                "File complaint online via consumerhelpline.gov.in (National Consumer Helpline 1915)."
            ]
            notice_template = "consumer_deficiency_notice"
            limitation_cat = "consumer_complaint"
            synthesized_query = f"Consumer protection procedure and statutory notice for deficiency of service under Consumer Protection Act 2019 in {loc}: {intake.incident_description}"

        elif domain == BroadDomainCategory.PROPERTY_TENANCY:
            forum = f"Competent Civil Court / Rent Authority, {loc}"
            suggested_statutes = ["Section 106 Transfer of Property Act, 1882", "Specific Relief Act, 1963 (Section 6)", "State Rent Control Act"]
            immediate_actions = [
                "Do not vacate without due process of law; forcible eviction without court order is illegal under Section 6 Specific Relief Act.",
                "Serve formal statutory 15-day lease termination notice under Section 106 Transfer of Property Act.",
                "Preserve registered rent agreement and rent bank transfer statements."
            ]
            notice_template = "tenant_eviction_notice"
            limitation_cat = "money_recovery_debt"
            synthesized_query = f"Tenant-landlord dispute procedure and eviction notice rules under Transfer of Property Act in {loc}: {intake.incident_description}"

        else:
            forum = f"District Court / Civil Judge Senior Division, {loc}"
            suggested_statutes = ["The Limitation Act, 1963", "Code of Civil Procedure, 1908", "Indian Contract Act, 1872"]
            immediate_actions = [
                "Collate all documentary proof, contracts, and communication records.",
                "Serve a formal statutory legal demand notice granting 15 days cure period."
            ]
            notice_template = "general_legal_demand"
            synthesized_query = f"Legal rights, civil procedure, and remedies in {loc} regarding: {intake.incident_description}"

        return StructuredLegalIntakeResult(
            success=True,
            broad_domain=domain.value.replace("_", " ").title(),
            statutory_governance_framework=framework,
            temporal_applicability=temporal_reason,
            competent_forum=forum,
            suggested_statutes=suggested_statutes,
            synthesized_legal_query=synthesized_query,
            immediate_citizen_actions=immediate_actions,
            recommended_notice_template=notice_template,
            recommended_limitation_category=limitation_cat
        )
