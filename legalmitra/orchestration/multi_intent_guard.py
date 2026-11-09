"""
Phase 112: Multi-Intent Disambiguation & Fact Extraction Guard Engine.

Provides deep structural parsing of compound, multi-issue legal queries:
1. Deconstructs compound queries (e.g., "my landlord threw my luggage out and also kept my deposit of 50000").
2. Extracts grounded factual entities (amounts, dates, places, party relationships, payment modes).
3. Evaluates Triage & Urgency (Golden-hour cyber fraud, violence/arrest emergency vs. civil disputes).
4. Emits a structured multi-intent payload with separate legal paths for each spotted issue.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


class UrgencyTier(str, Enum):
    IMMEDIATE_EMERGENCY = "IMMEDIATE_EMERGENCY"  # Violence, impending physical harm, physical arrest -> 112
    GOLDEN_HOUR_FINANCIAL = "GOLDEN_HOUR_FINANCIAL"  # Cyber/OTP/UPI fraud within hours -> 1930 / bank freeze
    URGENT_CIVIL_DEADLINE = "URGENT_CIVIL_DEADLINE"  # 15-day cheque notice, 30-day limitation, court summons
    STANDARD_GRIEVANCE = "STANDARD_GRIEVANCE"  # Consumer defect, long-standing civil dispute, general query


@dataclass
class ExtractedFactEntities:
    """Entities grounded directly in user statements."""
    monetary_amounts: List[str] = field(default_factory=list)
    dates_or_durations: List[str] = field(default_factory=list)
    parties_involved: List[str] = field(default_factory=list)
    locations_or_forums: List[str] = field(default_factory=list)
    instruments_or_channels: List[str] = field(default_factory=list)  # e.g. "cheque", "UPI", "WhatsApp", "registered post"
    key_actions: List[str] = field(default_factory=list)  # e.g. "locked door", "refused complaint"


@dataclass
class SubIssueIntent:
    """Individual legal problem spotted within a compound query."""
    issue_index: int
    issue_title: str
    primary_category: str
    governing_statutes: List[str]
    immediate_action: str
    statutory_limitation_or_timeline: Optional[str] = None
    urgency_tier: UrgencyTier = UrgencyTier.STANDARD_GRIEVANCE


@dataclass
class MultiIntentDisambiguationResult:
    """Comprehensive multi-issue deconstruction."""
    original_query: str
    is_compound_query: bool
    primary_urgency: UrgencyTier
    extracted_facts: ExtractedFactEntities
    sub_issues: List[SubIssueIntent]
    recommended_synthesis_structure: str


class MultiIntentDisambiguationGuard:
    """
    Evaluates complex citizen inquiries that contain multiple distinct legal dilemmas,
    preventing one issue from completely overshadowing or ignoring another.
    """

    @classmethod
    def analyze_query(cls, query: str) -> MultiIntentDisambiguationResult:
        if not query or not query.strip():
            return MultiIntentDisambiguationResult(
                original_query=query,
                is_compound_query=False,
                primary_urgency=UrgencyTier.STANDARD_GRIEVANCE,
                extracted_facts=ExtractedFactEntities(),
                sub_issues=[],
                recommended_synthesis_structure="SINGLE_ISSUE",
            )

        q_clean = query.strip()
        q_lower = q_clean.lower()

        # 1. Extract Factual Entities
        extracted_facts = cls._extract_facts(q_clean, q_lower)

        # 2. Identify all candidate sub-issues present
        sub_issues = cls._spot_all_sub_issues(q_lower, extracted_facts)

        is_compound = len(sub_issues) > 1

        # 3. Determine Highest Urgency Tier
        primary_urgency = UrgencyTier.STANDARD_GRIEVANCE
        if any(si.urgency_tier == UrgencyTier.IMMEDIATE_EMERGENCY for si in sub_issues):
            primary_urgency = UrgencyTier.IMMEDIATE_EMERGENCY
        elif any(si.urgency_tier == UrgencyTier.GOLDEN_HOUR_FINANCIAL for si in sub_issues):
            primary_urgency = UrgencyTier.GOLDEN_HOUR_FINANCIAL
        elif any(si.urgency_tier == UrgencyTier.URGENT_CIVIL_DEADLINE for si in sub_issues):
            primary_urgency = UrgencyTier.URGENT_CIVIL_DEADLINE

        synthesis_structure = "COMPOUND_MULTI_ISSUE" if is_compound else "SINGLE_ISSUE"

        return MultiIntentDisambiguationResult(
            original_query=q_clean,
            is_compound_query=is_compound,
            primary_urgency=primary_urgency,
            extracted_facts=extracted_facts,
            sub_issues=sub_issues,
            recommended_synthesis_structure=synthesis_structure,
        )

    @classmethod
    def _extract_facts(cls, q_raw: str, q_lower: str) -> ExtractedFactEntities:
        entities = ExtractedFactEntities()

        # Amounts (e.g. 50000, 50,000, 2 lakh, 15000 rs, 10 cr)
        amt_matches = re.findall(
            r"\b(?:\u20b9|rs\.?|inr)?\s*(\d+(?:,\d+)*(?:\.\d+)?\s*(?:lakh|crore|hazaar|k|rupaye|rupees)?)\b",
            q_raw,
            re.IGNORECASE,
        )
        for amt in amt_matches:
            amt_str = amt.strip()
            if amt_str and amt_str not in entities.monetary_amounts and any(char.isdigit() for char in amt_str):
                entities.monetary_amounts.append(amt_str)

        # Dates / Durations (e.g. "yesterday", "tomorrow", "3 months", "15 days", "aaj", "kal")
        dur_patterns = [
            r"\b(\d+\s*(?:days?|din|months?|mahine|weeks?|hafte|years?|saal))\b",
            r"\b(yesterday|today|tomorrow|aaj|kal|parso|last\s*night)\b",
        ]
        for pat in dur_patterns:
            matches = re.findall(pat, q_lower)
            for m in matches:
                if m not in entities.dates_or_durations:
                    entities.dates_or_durations.append(m)

        # Parties involved
        party_keywords = {
            "landlord": "Landlord / Makaan Maalik",
            "makan malik": "Landlord / Makaan Maalik",
            "owner": "Property Owner",
            "tenant": "Tenant / Kirayedaar",
            "kirayedaar": "Tenant / Kirayedaar",
            "bhadekaru": "Tenant / Kirayedaar",
            "police": "Police Officer / Station Staff",
            "sho": "Station House Officer (SHO)",
            "boss": "Employer / Company Boss",
            "company": "Employer / Organization",
            "husband": "Spouse (Husband)",
            "wife": "Spouse (Wife)",
            "pati": "Spouse (Husband)",
            "patni": "Spouse (Wife)",
            "padosi": "Neighbour",
            "neighbour": "Neighbour",
            "bank": "Bank / Financial Institution",
        }
        for kw, canonical_role in party_keywords.items():
            if kw in q_lower and canonical_role not in entities.parties_involved:
                entities.parties_involved.append(canonical_role)

        # Channels / Instruments
        instruments = {
            "cheque": "Cheque (Negotiable Instrument)",
            "check": "Cheque (Negotiable Instrument)",
            "otp": "SMS OTP (One Time Password)",
            "upi": "UPI / Net Banking Trail",
            "whatsapp": "WhatsApp Chat / Electronic Record",
            "speed post": "Speed Post / Postal Service",
            "registered post": "Registered Post with Acknowledgment",
        }
        for inst_kw, label in instruments.items():
            if inst_kw in q_lower and label not in entities.instruments_or_channels:
                entities.instruments_or_channels.append(label)

        return entities

    @classmethod
    def _spot_all_sub_issues(
        cls, q_lower: str, facts: ExtractedFactEntities
    ) -> List[SubIssueIntent]:
        sub_issues: List[SubIssueIntent] = []
        issue_idx = 1

        # 1. Illegal Tenant Eviction Check
        if any(w in q_lower for w in ["landlord", "flat", "rent", "room", "makan malik", "house"]) and any(
            w in q_lower for w in ["locked", "lock", "throw", "luggage", "samaan", "evict", "bahar", "nikal"]
        ):
            sub_issues.append(
                SubIssueIntent(
                    issue_index=issue_idx,
                    issue_title="Unlawful Dispossession & Illegal Tenant Eviction",
                    primary_category="Property & Tenancy Rights",
                    governing_statutes=[
                        "Transfer of Property Act, 1882 (Section 106)",
                        "Specific Relief Act, 1963 (Section 6)",
                        "The Bharatiya Nyaya Sanhita, 2023 (Section 329)",
                    ],
                    immediate_action="File an urgent police complaint for criminal trespass and house-breaking under Section 329 BNS, and seek an interim injunction before Civil Court under Section 6 Specific Relief Act.",
                    statutory_limitation_or_timeline="Mandatory 15-day statutory notice required before lease termination; recovery of possession under Sec 6 Specific Relief Act within 6 months of dispossession.",
                    urgency_tier=UrgencyTier.URGENT_CIVIL_DEADLINE,
                )
            )
            issue_idx += 1

        # 2. Security Deposit / Money Retention Dispute
        if (
            any(w in q_lower for w in ["deposit", "security", "advance", "amanat", "paise wapas"])
            or ("deposit" in q_lower and facts.monetary_amounts)
        ):
            sub_issues.append(
                SubIssueIntent(
                    issue_index=issue_idx,
                    issue_title="Withholding / Wrongful Deductions of Rental Security Deposit",
                    primary_category="Civil Recovery & Contractual Debt",
                    governing_statutes=[
                        "Indian Contract Act, 1872 (Section 73)",
                        "Code of Civil Procedure, 1908 (Order XXXVII)",
                        "Consumer Protection Act, 2019 (if serviced apartment/corporate accommodation)",
                    ],
                    immediate_action="Serve a formal Legal Notice for refund of security deposit within 15 days; if unpaid, initiate a Summary Recovery Suit under Order XXXVII CPC.",
                    statutory_limitation_or_timeline="3 years from the date of vacating the premises (Limitation Act, 1963).",
                    urgency_tier=UrgencyTier.STANDARD_GRIEVANCE,
                )
            )
            issue_idx += 1

        # 3. Cyber Financial Fraud / OTP Theft
        if any(w in q_lower for w in ["otp", "cyber", "khate se", "account se"]) and any(
            w in q_lower for w in ["kat gaye", "stole", "fraud", "deducted", "ud gaya", "nikal gaye"]
        ):
            sub_issues.append(
                SubIssueIntent(
                    issue_index=issue_idx,
                    issue_title="Cyber Financial Fraud & Unauthorized Bank Debit",
                    primary_category="Cybercrime & Banking Fraud",
                    governing_statutes=[
                        "Information Technology Act, 2000 (Section 66D)",
                        "The Bharatiya Nyaya Sanhita, 2023 (Section 318(4))",
                        "RBI Circular on Customer Liability (2017)",
                    ],
                    immediate_action="Dial 1930 immediately to freeze the recipient bank account, notify bank within 3 days for zero/limited liability, and report on cybercrime.gov.in.",
                    statutory_limitation_or_timeline="Golden hour (first 2-4 hours) for freezing; 3 working days for notifying bank for zero customer liability.",
                    urgency_tier=UrgencyTier.GOLDEN_HOUR_FINANCIAL,
                )
            )
            issue_idx += 1

        # 4. Cheque Bounce / Dishonour
        if any(w in q_lower for w in ["cheque", "check"]) and any(
            w in q_lower for w in ["bounce", "dishonour", "mismatch", "sign", "funds", "cleared"]
        ):
            sub_issues.append(
                SubIssueIntent(
                    issue_index=issue_idx,
                    issue_title="Dishonour of Cheque under Negotiable Instruments Act",
                    primary_category="Banking & Criminal Liability",
                    governing_statutes=[
                        "The Negotiable Instruments Act, 1881 (Section 138)",
                        "The Negotiable Instruments Act, 1881 (Section 142)",
                    ],
                    immediate_action="Obtain bank dishonour memo and send a formal Statutory Demand Notice to the drawer within 30 days giving 15 days to pay.",
                    statutory_limitation_or_timeline="Notice within 30 days of bank memo; Court complaint within 30 days after expiry of 15-day cure period.",
                    urgency_tier=UrgencyTier.URGENT_CIVIL_DEADLINE,
                )
            )
            issue_idx += 1

        # 5. Police Refusal to File FIR
        if any(w in q_lower for w in ["fir", "complaint", "takraar"]) and any(
            w in q_lower for w in ["refus", "nahi likh", "mana", "edukka maat", "not taking", "dismiss"]
        ):
            sub_issues.append(
                SubIssueIntent(
                    issue_index=issue_idx,
                    issue_title="Police Refusal to Register Cognizable Complaint (FIR)",
                    primary_category="Criminal Procedure & Police Accountability",
                    governing_statutes=[
                        "The Bharatiya Nagarik Suraksha Sanhita, 2023 (Section 173(4))",
                        "The Bharatiya Nagarik Suraksha Sanhita, 2023 (Section 175(3))",
                    ],
                    immediate_action="Send written complaint via registered post to Superintendent of Police (SP) under Sec 173(4) BNSS; if ignored, file application before Judicial Magistrate under Sec 175(3) BNSS.",
                    statutory_limitation_or_timeline="Prompt dispatch recommended; preserve postal tracking receipts.",
                    urgency_tier=UrgencyTier.URGENT_CIVIL_DEADLINE,
                )
            )
            issue_idx += 1

        # 6. Physical Violence / Immediate Arrest / Bodily Threat Emergency
        if any(w in q_lower for w in ["arrested", "custody", "hirasat", "police pakad", "maar peet", "killing", "attack"]):
            sub_issues.append(
                SubIssueIntent(
                    issue_index=issue_idx,
                    issue_title="Immediate Threat to Personal Liberty / Physical Safety",
                    primary_category="Constitutional Habeas Corpus & Arrest Rights",
                    governing_statutes=[
                        "Constitution of India (Article 21 & 22)",
                        "The Bharatiya Nagarik Suraksha Sanhita, 2023 (Section 47 & 48)",
                    ],
                    immediate_action="Dial 112 immediately. Under Section 47 & 48 BNSS, demand grounds of arrest, intimation to family, and access to an advocate.",
                    statutory_limitation_or_timeline="Production before Judicial Magistrate within mandatory 24 hours of arrest (Sec 57 BNSS).",
                    urgency_tier=UrgencyTier.IMMEDIATE_EMERGENCY,
                )
            )
            issue_idx += 1

        # 7. Cheating & Money Duping (Section 318 BNS)
        if any(w in q_lower for w in ["paise", "money", "rupaye", "lakh"]) and any(
            w in q_lower for w in ["bhaag", "farar", "cheated", "dhokha", "dukaan ke naam"]
        ):
            if not any(si.primary_category == "Cybercrime & Banking Fraud" for si in sub_issues):
                sub_issues.append(
                    SubIssueIntent(
                        issue_index=issue_idx,
                        issue_title="Criminal Cheating & Dishonest Inducement of Property",
                        primary_category="Criminal Fraud & Misappropriation",
                        governing_statutes=[
                            "The Bharatiya Nyaya Sanhita, 2023 (Section 318(4))",
                            "The Bharatiya Nyaya Sanhita, 2023 (Section 316)",
                        ],
                        immediate_action="Lodge an FIR under Section 318(4) BNS for cheating with bank statements and chat proofs; invoke Sec 173(4) BNSS if police hesitate.",
                        statutory_limitation_or_timeline="3 years from the commission/discovery of offence under Section 514 BNSS.",
                        urgency_tier=UrgencyTier.STANDARD_GRIEVANCE,
                    )
                )
                issue_idx += 1

        return sub_issues
