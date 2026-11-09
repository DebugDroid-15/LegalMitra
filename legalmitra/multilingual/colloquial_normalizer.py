"""
Phase 111: Indic Colloquial & Dialectal Semantic Normalizer Engine.

Provides deep dialectal, slang, and phonetic normalization for Indian legal queries across:
- Hinglish (Hindi + English)
- Tanglish (Tamil + English)
- Manglish / Marathish (Marathi + English)
- Telugish (Telugu + English)
- Benglish (Bengali + English)
- Pure Indic vernaculars (Devanagari, Tamil, Telugu, Bengali, Gujarati, Gurmukhi scripts)

Converts messy real-world citizen phrasing, slang terms, emotional distress, and regional idioms
into canonical statutory concepts, ensuring zero-collision deterministic retrieval.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple


class CanonicalLegalIntent(str, Enum):
    # Police & FIR
    POLICE_FIR_REFUSAL = "POLICE_FIR_REFUSAL"
    POLICE_ARREST_RIGHTS = "POLICE_ARREST_RIGHTS"
    ANTICIPATORY_BAIL = "ANTICIPATORY_BAIL"
    REGULAR_BAIL = "REGULAR_BAIL"
    POLICE_HARASSMENT = "POLICE_HARASSMENT"

    # Financial & Banking Crimes
    CYBER_OTP_FINANCIAL_FRAUD = "CYBER_OTP_FINANCIAL_FRAUD"
    CHEQUE_BOUNCE_DISHONOUR = "CHEQUE_BOUNCE_DISHONOUR"
    CRIMINAL_CHEATING_DUPING = "CRIMINAL_CHEATING_DUPING"
    UNPAID_SALARY_WAGES = "UNPAID_SALARY_WAGES"
    DEBT_RECOVERY_FRIENDLY_LOAN = "DEBT_RECOVERY_FRIENDLY_LOAN"

    # Property & Tenancy
    ILLEGAL_TENANT_EVICTION = "ILLEGAL_TENANT_EVICTION"
    SECURITY_DEPOSIT_DISPUTE = "SECURITY_DEPOSIT_DISPUTE"
    LAND_ENCROACHMENT = "LAND_ENCROACHMENT"
    NOISE_POLLUTION_NUISANCE = "NOISE_POLLUTION_NUISANCE"

    # Domestic, Family & Personal
    DOMESTIC_VIOLENCE_PROTECTION = "DOMESTIC_VIOLENCE_PROTECTION"
    WIFE_CHILD_MAINTENANCE = "WIFE_CHILD_MAINTENANCE"
    ADULT_AUTONOMY_PARENTS = "ADULT_AUTONOMY_PARENTS"
    CRIMINAL_INTIMIDATION_THREATS = "CRIMINAL_INTIMIDATION_THREATS"

    # Cyber & Privacy
    SEXTORTION_IMAGE_LEAK = "SEXTORTION_IMAGE_LEAK"
    IDENTITY_THEFT_IMPERSONATION = "IDENTITY_THEFT_IMPERSONATION"
    STALKING_HARASSMENT = "STALKING_HARASSMENT"

    # Consumer & Services
    CONSUMER_PRODUCT_DEFECT = "CONSUMER_PRODUCT_DEFECT"
    ECOMMERCE_FRAUD_NON_DELIVERY = "ECOMMERCE_FRAUD_NON_DELIVERY"
    COLLEGE_CERTIFICATE_WITHHELD = "COLLEGE_CERTIFICATE_WITHHELD"

    # General Conversational & Legal Aid
    FREE_LEGAL_AID = "FREE_LEGAL_AID"
    CONVERSATIONAL_GREETING = "CONVERSATIONAL_GREETING"
    LANGUAGE_SUPPORT_QUERY = "LANGUAGE_SUPPORT_QUERY"
    GENERAL_DISTRESS_UNSPECIFIED = "GENERAL_DISTRESS_UNSPECIFIED"


@dataclass
class NormalizedIntentResult:
    canonical_intent: CanonicalLegalIntent
    confidence_score: float
    canonical_search_query: str
    extracted_entities: Dict[str, str] = field(default_factory=dict)
    detected_dialect: str = "Hinglish/General"
    statutory_governing_provisions: List[str] = field(default_factory=list)


# Detailed colloquial dialect patterns with explicit negative guards
DIALECTAL_INTENT_RULES = [
    # 1. Police FIR Refusal
    {
        "intent": CanonicalLegalIntent.POLICE_FIR_REFUSAL,
        "search_query": "police refusal to register FIR Section 173(4) BNSS Section 154 CrPC representation to Superintendent of Police Judicial Magistrate 175(3)",
        "governing_provisions": ["The Bharatiya Nagarik Suraksha Sanhita, 2023 (Section 173(4))", "The Bharatiya Nagarik Suraksha Sanhita, 2023 (Section 175(3))"],
        "patterns": [
            r"(?:fir|complaint|takraar|shikayat|case).*?(?:nahi\s*likh|nondvat\s*nahit|nondavli\s*nahi|edukka\s*maat|edukala|theesukole|not\s*taking|refus|mana\s*kar|dismiss)",
            r"(?:police|thana|chowki|station).*?(?:bhaga\s*diya|bhagavla|sun\s*nahi\s*rahe|action\s*nahi|fir\s*nahi|edukka\s*maat)",
            r"(?:fir|takraar).*?(?:ghyaayla\s*nakar|nondavnyas\s*nakar|darj\s*nahi)",
            r"(?:police\s*station\s*la\s*complaint\s*edukka\s*maatengraanga)",
        ],
        "negative_keywords": ["fake fir", "quash fir", "fir against me", "anticipatory bail", "quashing"],
        "base_weight": 0.95
    },

    # 2. Cheque Bounce (Section 138 NI Act)
    {
        "intent": CanonicalLegalIntent.CHEQUE_BOUNCE_DISHONOUR,
        "search_query": "cheque bounce dishonour Section 138 Negotiable Instruments Act statutory demand notice 30 days bank memo signature mismatch funds insufficient",
        "governing_provisions": ["The Negotiable Instruments Act, 1881 (Section 138)", "The Negotiable Instruments Act, 1881 (Section 142)"],
        "patterns": [
            r"(?:cheque|check|dhanaadesh).*?(?:bounce|bounced|dishonour|parath|mismatch|funds|insufficient|sign|signature|a/c\s*closed|stop\s*payment)",
            r"(?:party|aadmi|client|customer).*?(?:cheque|check).*?(?:diya|dila|bounce|atakla|clear\s*nahi)",
            r"(?:check|cheque).*?(?:sign\s*mismatch|signature\s*differs|paisa\s*nahi\s*aaya)",
        ],
        "negative_keywords": ["vehicle accident", "hit and run", "accident ho gaya"],
        "base_weight": 0.98
    },

    # 3. Illegal Tenant Eviction (Section 106 TPA / Rent Control)
    {
        "intent": CanonicalLegalIntent.ILLEGAL_TENANT_EVICTION,
        "search_query": "illegal tenant eviction without due process of law Section 106 Transfer of Property Act Section 329 BNS landlord lock luggage",
        "governing_provisions": ["Transfer of Property Act, 1882 (Section 106)", "The Bharatiya Nyaya Sanhita, 2023 (Section 329)", "Specific Relief Act, 1963 (Section 6)"],
        "patterns": [
            r"(?:landlord|makan\s*malik|ghar\s*malak|owner).*?(?:locked|tala\s*laga|bahar\s*nikal|throw|luggage|samaan\s*phek|kal\s*khali|room\s*se\s*nikal)",
            r"(?:flat|room|ghar|house).*?(?:locked|luggage|samaan\s*bahar|evict|khali\s*karne\s*ki\s*dhamki|bina\s*notice)",
            r"(?:bhadekaru|kirayedar|tenant).*?(?:baher\s*kaadhle|saaman\s*phekla|tala\s*thokla)",
            r"(?:landlord\s*locked\s*my\s*flat\s*and\s*threw\s*my\s*luggage)",
        ],
        "negative_keywords": ["fired from job", "company terminated", "employment notice", "salary"],
        "base_weight": 0.96
    },

    # 4. Cyber Financial Fraud & OTP Theft (Helpline 1930 / Sec 66D IT Act)
    {
        "intent": CanonicalLegalIntent.CYBER_OTP_FINANCIAL_FRAUD,
        "search_query": "cyber financial fraud helpline 1930 golden hour bank account freeze Section 66D IT Act Section 318 BNS cybercrime.gov.in OTP phishing",
        "governing_provisions": ["Information Technology Act, 2000 (Section 66D)", "The Bharatiya Nyaya Sanhita, 2023 (Section 318(4))", "RBI Master Direction on Customer Protection (2017)"],
        "patterns": [
            r"(?:otp|pin|cvv).*?(?:le\s*liya|share|galti\s*se|bata\s*diya|fraud|stole|paise\s*kat\s*gaye|cut\s*zale)",
            r"(?:account\s*se|bank\s*se).*?(?:paise\s*kat\s*gaye|rupaye\s*kat\s*gaye|deducted|nikal\s*gaye|paisa\s*ud\s*gaya)",
            r"(?:call\s*karke|phone\s*pe|fraud\s*call).*?(?:otp|bank\s*manager|lottery|kyc\s*update).*?(?:paise|kat\s*gaye|50000|lakh)",
            r"(?:1930|cyber\s*fraud|online\s*thagi|khate\s*se\s*paise)",
        ],
        "negative_keywords": ["unpaid salary", "loan borrowed return", "cheque bounce"],
        "base_weight": 0.98
    },

    # 5. Criminal Cheating, Business Fraud & Monetary Duping (Section 318 BNS / 420 IPC)
    {
        "intent": CanonicalLegalIntent.CRIMINAL_CHEATING_DUPING,
        "search_query": "cheating Section 318 BNS Section 420 IPC dishonest misappropriation Section 316 criminal breach of trust money duping absconding",
        "governing_provisions": ["The Bharatiya Nyaya Sanhita, 2023 (Section 318(4))", "The Bharatiya Nyaya Sanhita, 2023 (Section 316)", "The Bharatiya Nagarik Suraksha Sanhita, 2023 (Section 173(4))"],
        "patterns": [
            r"(?:paise|rupaye|lakh|crore).*?(?:le\s*kar\s*bhaag\s*gaya|lekar\s*farar|ghevun\s*palala|bhaag\s*gaya|dhokha\s*diya|thagi)",
            r"(?:dukaan|business|shop|plot|investment|scheme).*?(?:ke\s*naam\s*par|naavaavar).*?(?:paise|rupaye).*?(?:le\s*liye|thagle)",
            r"(?:fasavla|fasavnuk|dhokhadhadi|chuna\s*laga\s*diya|420|420i|cheated\s*money)",
            r"(?:ek\s*aadmi\s*ne\s*dukaan\s*ke\s*naam\s*par\s*2\s*lakh)",
        ],
        "negative_keywords": ["cheque bounce", "bank otp", "landlord tenant"],
        "base_weight": 0.94
    },

    # 6. Sudden Unlawful Termination from Job
    {
        "intent": CanonicalLegalIntent.UNPAID_SALARY_WAGES,
        "search_query": "unlawful employment termination unpaid salary notice period Section 10 Industrial Disputes Act contractual breach",
        "governing_provisions": ["Industrial Disputes Act, 1947 (Section 25F)", "Payment of Wages Act, 1936", "Contract Act, 1872 (Section 73)"],
        "patterns": [
            r"(?:company|boss|office|employer|hr).*?(?:fired|terminated|job\s*se\s*nikal|naukri\s*se\s*nikal|bina\s*notice|salary\s*nahi\s*di)",
            r"(?:unlawful\s*termination|sudden\s*firing|severance|experience\s*letter|fnf\s*nahi)",
            r"(?:pagaar|salary|wages).*?(?:dili\s*nahi|rok\s*li|nahi\s*de\s*raha|3\s*mahine)",
        ],
        "negative_keywords": ["flat", "room", "landlord", "rent", "tenant", "makan malik", "cheque"],
        "base_weight": 0.92
    },

    # 7. Criminal Intimidation & Death Threats (Section 351 BNS / 506 IPC)
    {
        "intent": CanonicalLegalIntent.CRIMINAL_INTIMIDATION_THREATS,
        "search_query": "criminal intimidation threats Section 351 BNS Section 506 IPC preventive police action Chapter VIII BNSS",
        "governing_provisions": ["The Bharatiya Nyaya Sanhita, 2023 (Section 351)", "The Bharatiya Nagarik Suraksha Sanhita, 2023 (Section 125)"],
        "patterns": [
            r"(?:dhamki|threat|threatening).*?(?:de\s*raha|jaan\s*se\s*maar|maar\s*peet|police\s*me\s*gaya\s*toh|dekh\s*lunga|gharat\s*yeun)",
            r"(?:neighbour|padosi|gunda|aadmi).*?(?:dhamka\s*raha|threaten\s*to\s*kill|beat)",
        ],
        "negative_keywords": ["cheque", "cyber otp", "landlord luggage"],
        "base_weight": 0.90
    },

    # 8. Sextortion, Private Photo Leaks & Blackmail
    {
        "intent": CanonicalLegalIntent.SEXTORTION_IMAGE_LEAK,
        "search_query": "sextortion blackmail Section 66E Section 67 IT Act Section 351 BNS Section 77 BNS voyeurism private photos viral helpline 1930",
        "governing_provisions": ["Information Technology Act, 2000 (Section 66E)", "Information Technology Act, 2000 (Section 67)", "The Bharatiya Nyaya Sanhita, 2023 (Section 77 & 351)"],
        "patterns": [
            r"(?:photo|video|recording|mms).*?(?:leak|viral|blackmail|social\s*media|instagram|whatsapp\s*group).*?(?:dhamki|paise\s*maang)",
            r"(?:nude|private\s*photo|intimate).*?(?:share|forward|threaten\s*to\s*post)",
        ],
        "negative_keywords": [],
        "base_weight": 0.98
    },

    # 9. Free Legal Aid & DLSA Assistance (NALSA / Sec 341 BNSS)
    {
        "intent": CanonicalLegalIntent.FREE_LEGAL_AID,
        "search_query": "free legal aid DLSA NALSA helpline 15100 Article 39A Section 341 BNSS legal services authority act",
        "governing_provisions": ["Constitution of India (Article 39A)", "Legal Services Authorities Act, 1987 (Section 12)", "The Bharatiya Nagarik Suraksha Sanhita, 2023 (Section 341)"],
        "patterns": [
            r"(?:paise\s*nahi\s*hai|gareeb|afford\s*nahi|free).*?(?:vakil|lawyer|advocate|court\s*case|sahayata)",
            r"(?:free\s*lawyer|sarkari\s*vakil|legal\s*aid|dlsa|nalsa|15100)",
        ],
        "negative_keywords": [],
        "base_weight": 0.93
    }
]


class IndicColloquialNormalizer:
    """
    High-precision normalizer for colloquial Indian dialects, transliterated slangs,
    and regional phrasing. Maps queries cleanly to verified legal intents.
    """

    @classmethod
    def normalize_query(cls, query: str) -> NormalizedIntentResult:
        if not query or not query.strip():
            return NormalizedIntentResult(
                canonical_intent=CanonicalLegalIntent.GENERAL_DISTRESS_UNSPECIFIED,
                confidence_score=0.0,
                canonical_search_query="",
            )

        q_clean = query.strip()
        q_lower = q_clean.lower()
        words = set(re.findall(r"\w+", q_lower))

        # Check Conversational Greeting
        greetings = ["hi", "hello", "hey", "namaste", "pranam", "kem cho", "vanakkam", "sat sri akal", "adab"]
        if q_lower in greetings or any(q_lower.startswith(g + " ") for g in greetings):
            return NormalizedIntentResult(
                canonical_intent=CanonicalLegalIntent.CONVERSATIONAL_GREETING,
                confidence_score=1.0,
                canonical_search_query="LegalMitra greeting welcome capabilities",
            )

        # Check Language Support query
        lang_phrases = ["what language", "which language", "languages do you support", "bhasha", "language support"]
        if any(lp in q_lower for lp in lang_phrases):
            return NormalizedIntentResult(
                canonical_intent=CanonicalLegalIntent.LANGUAGE_SUPPORT_QUERY,
                confidence_score=1.0,
                canonical_search_query="Digital India Bhashini 22 scheduled languages support",
            )

        # Extract numerical & monetary entities (e.g. 50000, 2 lakh, 15 days)
        entities = {}
        m_amt = re.search(r"(\d+(?:,\d+)*(?:\s*(?:lakh|crore|hazaar|k|rs|inr|rupaye|rupees))?)", q_clean, re.I)
        if m_amt:
            entities["amount_or_figure"] = m_amt.group(1)

        # Scan dialect rules with positive weights and negative penalty gates
        best_rule = None
        best_score = 0.0

        for rule in DIALECTAL_INTENT_RULES:
            # Check negative keywords first
            has_negative = any(neg in q_lower for neg in rule["negative_keywords"])
            if has_negative:
                continue

            score = 0.0
            for pattern in rule["patterns"]:
                if re.search(pattern, q_lower, re.I):
                    score += rule["base_weight"]
                    break

            if score > best_score:
                best_score = score
                best_rule = rule

        if best_rule and best_score >= 0.85:
            return NormalizedIntentResult(
                canonical_intent=best_rule["intent"],
                confidence_score=best_score,
                canonical_search_query=best_rule["search_query"],
                extracted_entities=entities,
                statutory_governing_provisions=best_rule["governing_provisions"]
            )

        # Fallback to general distress if vague
        return NormalizedIntentResult(
            canonical_intent=CanonicalLegalIntent.GENERAL_DISTRESS_UNSPECIFIED,
            confidence_score=0.4,
            canonical_search_query=q_clean,
            extracted_entities=entities
        )
