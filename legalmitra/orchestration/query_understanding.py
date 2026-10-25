"""
LegalMitra Query Understanding & Issue Spotting Engine (Phase 50)
Parses natural-language legal questions into structured representations of:
- Legal domain & sub-domains
- Candidate legal issues and dependencies
- Temporal events, dates, and versioning boundaries
- User-supplied facts vs unverified assertions vs assumptions
- Stated parties and legal roles
- Territorial jurisdiction
- Candidate Acts, provisions, delegated rules, and precedents
- Ambiguous statutory definitions
- Material missing facts and clarification necessities
"""

import re
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass
class ParsedLegalQuery:
    """Structured representation of a user's legal inquiry."""
    original_query: str
    legal_domain: str
    sub_domains: List[str] = field(default_factory=list)
    candidate_issues: List[str] = field(default_factory=list)
    events_and_dates: List[Dict[str, Any]] = field(default_factory=list)
    query_date: Optional[str] = None
    user_supplied_facts: List[str] = field(default_factory=list)
    alleged_facts_unverified: List[str] = field(default_factory=list)
    implicit_assumptions: List[str] = field(default_factory=list)
    parties_and_roles: List[Dict[str, str]] = field(default_factory=list)
    jurisdiction: Optional[str] = None
    applicable_acts: List[str] = field(default_factory=list)
    candidate_provisions: List[str] = field(default_factory=list)
    delegated_instruments: List[str] = field(default_factory=list)
    candidate_precedents: List[str] = field(default_factory=list)
    ambiguous_terms: List[str] = field(default_factory=list)
    missing_facts: List[str] = field(default_factory=list)
    clarification_necessary: bool = False
    clarification_prompt: Optional[str] = None
    source_coverage_requirements: List[str] = field(default_factory=list)
    is_adversarial_injection: bool = False
    adversarial_notes: Optional[str] = None
    procedural_posture: Optional[str] = None
    material_unknowns: List[Dict[str, str]] = field(default_factory=list)
    issue_dependencies: List[Dict[str, Any]] = field(default_factory=list)
    decomposed_issues: List[Dict[str, Any]] = field(default_factory=list)
    statutory_exceptions_identified: List[str] = field(default_factory=list)


class LegalQueryAnalyzer:
    """
    Deterministic analyzer that converts unstructured legal questions
    into verifiable structured query representations without hallucinating facts.
    """

    # Domain keyword patterns
    DOMAIN_PATTERNS = {
        "CONSTITUTIONAL": [
            r"\b(constitution|article\s*\d+|basic structure|fundamental right|writ|habeas corpus|mandamus|certiorari|amendment\s*act|article 368|article 21|article 14|article 19|ninth schedule|president'?s rule|article 356)\b"
        ],
        "CRIMINAL": [
            r"\b(fir|bns|bnss|bsa|ipc|crpc|evidence act|bail|anticipatory bail|arrest|quash|police|cognizable|non-bailable|magistrate|cheating|theft|murder|defamation|section 482|section 438|section 528|section 173)\b"
        ],
        "COMMERCIAL_ARBITRATION": [
            r"\b(arbitrat|arbitral|award|section 34|section 29a|section 9|section 11|commercial court|commercial dispute|written statement|120 days|interim measures)\b"
        ],
        "CORPORATE_INSOLVENCY": [
            r"\b(ibc|insolvency|bankruptcy|cirp|section 29a|section 32a|clean slate|resolution plan|resolution applicant|nclt|nclat|csr|section 135|corporate social responsibility)\b"
        ],
        "INTELLECTUAL_PROPERTY": [
            r"\b(copyright|patent|trade\s*mark|trademark|infringement|section 3\(d\)|section 52|fair dealing|section 57|moral rights|compulsory licence|madrid protocol|therapeutic efficacy)\b"
        ],
        "LABOUR_EMPLOYMENT": [
            r"\b(workman|employee|retrenchment|industrial dispute|labour code|code on wages|industrial relations code|factories act|section 25f|section 25-o|overtime|strike|lockout)\b"
        ],
        "CONTRACT_PROPERTY": [
            r"\b(contract|agreement|specific relief|section 28|limitation clause|forfeiture|section 53a|part performance|transfer of property|unregistered agreement|rent control|eviction|tenant|landlord)\b"
        ],
        "MOTOR_ACCIDENT": [
            r"\b(motor vehicle|mva|accident|compensation|no fault liability|section 163a|section 164|structured formula|mact)\b"
        ],
        "DATA_PROTECTION": [
            r"\b(dpdp|data protection|personal data|data fiduciary|data principal|privacy|surveillance|it act|section 66a|intermediary)\b"
        ],
    }

    # Cross-statute ambiguous terms
    AMBIGUOUS_TERMS = [
        "workman", "employee", "goods", "wages", "commercial dispute",
        "industry", "factory", "public servant"
    ]

    # Jurisdiction mapping
    JURISDICTION_MAP = {
        "delhi": "IN-DL",
        "bombay": "IN-MH",
        "maharashtra": "IN-MH",
        "madras": "IN-TN",
        "tamil nadu": "IN-TN",
        "calcutta": "IN-WB",
        "west bengal": "IN-WB",
        "karnataka": "IN-KA",
        "allahabad": "IN-UP",
        "uttar pradesh": "IN-UP",
        "punjab": "IN-PB",
        "haryana": "IN-HR",
        "gujarat": "IN-GJ",
        "kerala": "IN-KL",
        "supreme court": "IN-SC",
    }

    def parse_query(self, query: str, context_date: Optional[str] = None) -> ParsedLegalQuery:
        """
        Parses a user's natural-language legal query into a rich structured representation.
        """
        clean_q = query.strip()
        q_lower = clean_q.lower()

        # 0. Check for adversarial injection attempts
        is_adversarial = False
        adv_notes = None
        adv_triggers = [
            "ignore all", "ignore previous", "disregard", "pretend you are",
            "bypass evidence", "override safeguards", "unconstrained", "jailbreak"
        ]
        if any(t in q_lower for t in adv_triggers) and any(kw in q_lower for kw in [
            "law", "statute", "statutory", "instruction", "provisos", "exceptions", "lawyer", "rules", "confirming", "legal", "clause is"
        ]):
            is_adversarial = True
            adv_notes = "Adversarial prompt injection attempt detected: directive to ignore statutory rules."

        # 1. Identify Legal Domain
        matched_domains = []
        for domain, patterns in self.DOMAIN_PATTERNS.items():
            if any(re.search(pat, q_lower) for pat in patterns):
                matched_domains.append(domain)
        primary_domain = matched_domains[0] if matched_domains else "GENERAL_CIVIL"
        sub_domains = matched_domains[1:] if len(matched_domains) > 1 else []

        # 2. Extract Dates and Temporal Context
        events_and_dates = []
        # Match explicit dates: DD/MM/YYYY, YYYY-MM-DD, or Month YYYY, or bare YYYY
        iso_dates = re.findall(r"\b(\d{4}-\d{2}-\d{2})\b", clean_q)
        for d in iso_dates:
            events_and_dates.append({"raw": d, "parsed": d, "type": "explicit_iso_date"})

        dmy_dates = re.findall(r"\b(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})\b", clean_q)
        for d in dmy_dates:
            events_and_dates.append({"raw": d, "parsed": d, "type": "explicit_dmy_date"})

        year_matches = re.findall(r"\b(19\d{2}|20\d{2})\b", clean_q)
        for y in year_matches:
            if not any(y in d["raw"] for d in events_and_dates):
                events_and_dates.append({"raw": y, "parsed": f"{y}-01-01", "type": "year_reference"})

        # Query date resolution
        query_date = context_date
        if not query_date and events_and_dates:
            query_date = events_and_dates[0]["parsed"]

        # 3. Extract Jurisdiction
        detected_jurisdiction = None
        for name, code in self.JURISDICTION_MAP.items():
            if name in q_lower:
                detected_jurisdiction = code
                break

        # 4. Extract Applicable Acts & Provisions
        acts = []
        provisions = []
        delegated_instruments = []
        precedents = []

        if any(term in q_lower for term in ["bnss", "nagarik suraksha"]) or ("crpc" in q_lower and any(t in q_lower for t in ["repeal", "savings", "1 july 2024", "abated", "531"])):
            acts.append("IND-STAT-BNSS-2023")
            if any(t in q_lower for t in ["repeal", "savings", "abated", "pending", "1 july 2024"]):
                provisions.append("Section 531")
        if any(term in q_lower for term in ["bns", "nyaya sanhita"]):
            acts.append("IND-STAT-BNS-2023")
        if any(term in q_lower for term in ["bsa", "sakshya"]):
            acts.append("IND-STAT-BSA-2023")
        if any(term in q_lower for term in ["ipc", "penal code"]):
            acts.append("IND-STAT-IPC-1860")
        if any(term in q_lower for term in ["crpc", "criminal procedure code"]):
            acts.append("IND-STAT-CRPC-1973")
        if any(term in q_lower for term in ["contract act", "section 28"]):
            acts.append("IND-STAT-ICA-1872")
        if any(term in q_lower for term in ["arbitration", "section 34", "section 29a"]):
            acts.append("IND-STAT-ARBITRATION-1996")
        if any(term in q_lower for term in ["specific relief"]):
            acts.append("IND-STAT-SRA-1963")
        if any(term in q_lower for term in ["transfer of property", "section 53a"]):
            acts.append("IND-STAT-TPA-1882")
        if any(term in q_lower for term in ["it act", "information technology", "section 66a", "66a"]):
            acts.append("IND-STAT-IT-2000")
            if "66a" in q_lower:
                provisions.append("Section 66A")
        if any(term in q_lower for term in ["copyright"]):
            acts.append("IND-STAT-COPYRIGHT-1957")
            if any(term in q_lower for term in ["rule", "rules", "registration"]):
                delegated_instruments.append("IND-RULE-COPYRIGHT-2013")
        if any(term in q_lower for term in ["patent"]):
            acts.append("IND-STAT-PATENTS-1970")
            if any(term in q_lower for term in ["rule", "rules", "form 27"]):
                delegated_instruments.append("IND-RULE-PATENTS-2003")
        if any(term in q_lower for term in ["trade mark", "trademark"]):
            acts.append("IND-STAT-TRADEMARKS-1999")
            if any(term in q_lower for term in ["rule", "rules"]):
                delegated_instruments.append("IND-RULE-TRADEMARKS-2017")
        if any(term in q_lower for term in ["csr", "corporate social responsibility"]):
            acts.append("IND-STAT-COMPANIES-2013")
            delegated_instruments.append("IND-RULE-CSR-2014")
        if any(term in q_lower for term in ["industrial dispute", "retrenchment", "ida", "industrial disputes act"]):
            acts.append("IND-STAT-IDA-1947")
        if any(term in q_lower for term in ["code on wages"]):
            acts.append("IND-STAT-WAGES-2019")
        if any(term in q_lower for term in ["industrial relations code"]):
            acts.append("IND-STAT-IRCODE-2020")
        if any(term in q_lower for term in ["constitution", "article 368", "article 21", "basic structure"]):
            acts.append("IND-CONST-1950")
        if any(term in q_lower for term in ["factories act", "factory", "overtime"]):
            acts.append("IND-STAT-FACTORIES-1948")
        if any(term in q_lower for term in ["gratuity", "payment of gratuity"]):
            acts.append("IND-STAT-GRATUITY-1972")
            provisions.append("Section 4")
        if any(term in q_lower for term in ["anticipatory bail", "bail"]):
            if context_date and context_date >= "2024-07-01":
                acts.append("IND-STAT-BNSS-2023")
                provisions.append("Section 482")
            else:
                acts.append("IND-STAT-CRPC-1973")
                provisions.append("Section 438")
        if any(term in q_lower for term in ["delhi rent control", "drc act", "rent control", "rent controller"]):
            acts.append("IND-STAT-DRC-1958")
            provisions.append("Section 3")
        if any(term in q_lower for term in ["osh code", "occupational safety"]):
            acts.append("IND-STAT-OSHCODE-2020")
            provisions.append("Section 25")
        if any(term in q_lower for term in ["ni act", "negotiable instruments", "cheque bounce", "138", "139"]):
            acts.append("IND-STAT-NI-1881")
            provisions.append("Section 138")
            provisions.append("Section 139")
        if any(term in q_lower for term in ["commercial court", "commercial courts act", "pre-institution mediation"]):
            acts.append("IND-STAT-COMMERCIAL_COURTS-2015")
            provisions.append("Section 12A")
        if any(term in q_lower for term in ["hindu succession", "coparcen", "daughter coparcener", "ancestral property"]):
            acts.append("IND-STAT-HSA-1956")
            provisions.append("Section 6")
        if any(term in q_lower for term in ["specific relief", "infrastructure project", "section 20a"]) and "IND-STAT-SRA-1963" not in acts:
            acts.append("IND-STAT-SRA-1963")
            if "20a" in q_lower or "infrastructure" in q_lower:
                provisions.append("Section 20A")
            if "10" in q_lower:
                provisions.append("Section 10")
        if any(term in q_lower for term in ["ibc", "insolvency and bankruptcy", "clean slate", "resolution plan"]) and "IND-STAT-IBC-2016" not in acts:
            acts.append("IND-STAT-IBC-2016")
            if "32a" in q_lower or "clean slate" in q_lower:
                provisions.append("Section 32A")

        # Extract explicit section references
        sec_matches = re.findall(r"\b(?:section|sec\.?|s\.)\s*(\d+[A-Za-z]?(?:\(\d+\))?)\b", clean_q, re.IGNORECASE)
        for s in sec_matches:
            provisions.append(s.strip())

        # Extract explicit article references
        art_matches = re.findall(r"\b(?:article|art\.?)\s*(\d+[A-Za-z]?(?:\(\d+\))?)\b", clean_q, re.IGNORECASE)
        for a in art_matches:
            provisions.append(f"Article {a.strip()}")

        # Extract candidate precedents
        known_precedents = [
            ("kesavananda", "CASE-SC-CONST-KESAVANANDA-1973"),
            ("minerva mills", "CASE-SC-CONST-MINERVA-1980"),
            ("maneka gandhi", "CASE-SC-CONST-MANEKA-GANDHI-1978"),
            ("ir coelho", "CASE-SC-CONST-COELHO-2007"),
            ("i.r. coelho", "CASE-SC-CONST-COELHO-2007"),
            ("puttaswamy", "CASE-SC-CONST-PUTTASWAMY-2017"),
            ("sr bommai", "CASE-SC-CONST-BOMMAI-1994"),
            ("s.r. bommai", "CASE-SC-CONST-BOMMAI-1994"),
            ("delhi laws", "CASE-SC-CONST-DELHI-LAWS-1951"),
            ("champakam", "CASE-SC-CONST-CHAMPAKAM-1951"),
            ("vulcan insurance", "CASE-VULCAN"),
            ("vodafone", "CASE-SC-VODAFONE-2012"),
            ("excel wear", "CASE-SC-EXCEL-WEAR-1978"),
            ("arnesh kumar", "CASE-ARNESH-KUMAR"),
            ("nn global", "CASE-NN-GLOBAL"),
            ("st. stephen", "CASE-HC-DEL-ST-STEPHENS-2022"),
            ("st stephen", "CASE-HC-DEL-ST-STEPHENS-2022"),
            ("cadila", "CASE-CADILA-2001"),
            ("novartis", "CASE-NOVARTIS-2013"),
            ("subhash kashinath", "CASE-SC-SUBHASH-KASHINATH-2018"),
            ("subhash", "CASE-SC-SUBHASH-KASHINATH-2018"),
            ("ramesh chandra", "CASE-SC-RAMESH-CHANDRA-REF-2019"),
            ("ramesh verma", "CASE-SC-RAMESH-VERMA-2017"),
            ("rohan builders", "CASE-HC-BOM-ARBITRATION-2021"),
            ("harkirat", "CASE-HC-BOM-ARBITRATION-2021"),
            ("sibbia", "CASE-SIBBIA"),
            ("gurbaksh", "CASE-SIBBIA"),
            ("sushila aggarwal", "CASE-SUSHILA-AGGARWAL"),
            ("lalita kumari", "CASE-LALITA-KUMARI"),
            ("adm jabalpur", "CASE-SC-ADM-JABALPUR-1976"),
        ]
        for name, pid in known_precedents:
            if name in q_lower:
                precedents.append(pid)

        # 5. Extract Ambiguous Legal Terms
        ambiguous_terms = [t for t in self.AMBIGUOUS_TERMS if t in q_lower]

        # 6. Extract User-Supplied Facts vs Unverified Assertions
        user_facts = []
        alleged_facts = []
        implicit_assumptions = []

        sentences = [s.strip() for s in re.split(r"[.?!;]", clean_q) if s.strip()]
        for s in sentences:
            s_low = s.lower()
            if any(term in s_low for term in ["alleged", "claimed", "states that", "claims that", "accused of"]):
                alleged_facts.append(s)
            elif any(term in s_low for term in ["if", "assuming", "suppose", "let us assume"]):
                implicit_assumptions.append(s)
            elif any(term in s_low for term in ["entered into", "signed", "employed as", "rent is", "accident occurred", "dated", "filed on"]):
                user_facts.append(s)

        # 7. Extract Parties and Roles
        parties = []
        if "tenant" in q_lower:
            parties.append({"role": "tenant", "entity": "user/respondent"})
        if "landlord" in q_lower:
            parties.append({"role": "landlord", "entity": "adverse party"})
        if "employer" in q_lower:
            parties.append({"role": "employer", "entity": "management"})
        if "workman" in q_lower or "worker" in q_lower or "employee" in q_lower:
            parties.append({"role": "employee", "entity": "claimant"})
        if "accused" in q_lower or "arrest" in q_lower or "bail" in q_lower:
            parties.append({"role": "accused/applicant", "entity": "applicant"})

        # 8. Identify Candidate Legal Issues
        issues = []
        if primary_domain == "CRIMINAL":
            if "bail" in q_lower or "anticipatory" in q_lower:
                issues.append("Jurisdiction and statutory conditions for grant of anticipatory bail")
            if "quash" in q_lower:
                issues.append("Maintainability and legal grounds for quashing criminal proceedings under inherent powers")
            if "electronic" in q_lower or "whatsapp" in q_lower or "printout" in q_lower:
                issues.append("Admissibility and certification requirements for electronic records")
            if "cheating" in q_lower:
                issues.append("Substantive criminal liability and penal sanctions for cheating across the 1 July 2024 boundary")

        elif primary_domain == "COMMERCIAL_ARBITRATION":
            if "29a" in q_lower or "mandate" in q_lower or "time limit" in q_lower:
                issues.append("Power of court to extend arbitral tribunal mandate and territorial divergence of High Courts")
            if "34" in q_lower or "set aside" in q_lower:
                issues.append("Grounds for setting aside arbitral award and non-interference by non-judicial authorities")

        elif primary_domain == "CONTRACT_PROPERTY":
            if "28" in q_lower or "forfeiture" in q_lower or "extinguish" in q_lower:
                issues.append("Validity of contractual limitation / forfeiture clause under Section 28 post-1997 amendment")
            if "53a" in q_lower or "part performance" in q_lower:
                issues.append("Availability of Section 53A part-performance protection under an unregistered agreement post-2001")
            if "rent control" in q_lower or "tenant" in q_lower:
                issues.append("Exemption threshold under Rent Control Act and applicability of general Transfer of Property Act")

        elif primary_domain == "INTELLECTUAL_PROPERTY":
            if "copyright" in q_lower and ("moral" in q_lower or "57" in q_lower):
                issues.append("Perpetual duration of author's moral rights post-2012 Copyright amendment")
            if "patent" in q_lower and ("3(d)" in q_lower or "therapeutic" in q_lower):
                issues.append("Therapeutic efficacy threshold for patentability of incremental chemical/pharmaceutical substances")
            if "trade mark" in q_lower or "trademark" in q_lower:
                issues.append("Deceptive similarity standards in medicinal trademarks and Madrid protocol international registration")

        elif primary_domain == "LABOUR_EMPLOYMENT":
            if "retrenchment" in q_lower or "25f" in q_lower:
                issues.append("Conditions precedent to retrenchment of workmen under Industrial Disputes Act Section 25F")
            if "code on wages" in q_lower or "labour code" in q_lower:
                issues.append("Commencement status of Labour Codes and continued operation of predecessor statutes")

        elif primary_domain == "CONSTITUTIONAL":
            if "basic structure" in q_lower or "article 368" in q_lower:
                issues.append("Limits on Parliament's constituent amending power under Article 368 per Kesavananda Bharati")
            if "privacy" in q_lower or "article 21" in q_lower:
                issues.append("Fundamental right to privacy and proportionality standard under Article 21 per Puttaswamy")

        # Procedural Posture Extraction (Phase 56)
        posture = "GENERAL_LEGAL_INQUIRY"
        if any(t in q_lower for t in ["statutory demand notice", "notice under section 138", "demand notice", "legal notice"]):
            posture = "STATUTORY_PRE_SUIT_NOTICE"
        elif any(t in q_lower for t in ["pre-institution mediation", "section 12a", "mediation non-starter"]):
            posture = "COMMERCIAL_PRE_INSTITUTION_MEDIATION"
        elif any(t in q_lower for t in ["fir", "investigation", "arrest", "police custody", "remand"]):
            posture = "INVESTIGATION_STAGE"
        elif any(t in q_lower for t in ["anticipatory bail", "regular bail", "bail application"]):
            posture = "BAIL_APPLICATION"
        elif any(t in q_lower for t in ["quashing", "section 482", "section 528"]):
            posture = "QUASHING_PETITION"
        elif any(t in q_lower for t in ["mandate extension", "extension of mandate", "section 29a"]):
            posture = "ARBITRAL_MANDATE_EXTENSION"
        elif any(t in q_lower for t in ["setting aside award", "section 34", "challenge award"]):
            posture = "AWARD_CHALLENGE"
        elif any(t in q_lower for t in ["suit for specific performance", "injunction", "civil suit"]):
            posture = "ORIGINAL_CIVIL_SUIT"
        elif any(t in q_lower for t in ["retrenchment", "industrial tribunal", "conciliation"]):
            posture = "LABOUR_TRIBUNAL_PROCEEDING"
        elif any(t in q_lower for t in ["appeal", "revision", "special leave petition", "slp"]):
            posture = "APPELLATE_PROCEEDING"

        # Multi-Issue Decomposition & Rule Dependency Identification (Phase 56)
        decomposed_issues = []
        issue_dependencies = []
        statutory_exceptions = []
        material_unknowns = []

        # Compound Pattern 1: Specific Relief Act Sec 10 + Sec 20A Infrastructure Bar
        if ("specific relief" in q_lower or "specific performance" in q_lower or "contract" in q_lower) and ("infrastructure" in q_lower or "20a" in q_lower):
            decomposed_issues.append({
                "issue_id": "ISSUE-1",
                "statement": "Entitlement to specific performance of contract under Section 10 of Specific Relief Act, 1963",
                "governing_statute": "IND-STAT-SRA-1963 Section 10",
                "relationship_type": "PRIMARY_RULE",
                "prerequisite_issue_id": None,
            })
            decomposed_issues.append({
                "issue_id": "ISSUE-2",
                "statement": "Statutory bar on granting injunctions in infrastructure projects under Section 20A and Schedule of Specific Relief Act",
                "governing_statute": "IND-STAT-SRA-1963 Section 20A",
                "relationship_type": "STATUTORY_EXCEPTION",
                "prerequisite_issue_id": "ISSUE-1",
            })
            issue_dependencies.append({
                "dependent_issue_id": "ISSUE-2",
                "governing_issue_id": "ISSUE-1",
                "dependency_type": "STATUTORY_EXCEPTION_BAR",
                "description": "Section 20A operates as a statutory bar overriding general injunctive relief if project falls under infrastructure schedule."
            })
            statutory_exceptions.append("Section 20A(1) SRA: No injunction shall be granted in infrastructure project suits where it causes impediment or delay.")

        # Compound Pattern 2: Hindu Succession Act Sec 6 Coparcenary + Pre-2004 Partition Proviso
        elif ("hindu succession" in q_lower or "coparcen" in q_lower or "daughter" in q_lower) and ("partition" in q_lower or "proviso" in q_lower or "2004" in q_lower or "ancestral" in q_lower):
            decomposed_issues.append({
                "issue_id": "ISSUE-1",
                "statement": "Right of daughter as coparcener by birth under Section 6(1) of Hindu Succession Act as amended in 2005",
                "governing_statute": "IND-STAT-HSA-1956 Section 6(1)",
                "relationship_type": "PRIMARY_RULE",
                "prerequisite_issue_id": None,
            })
            decomposed_issues.append({
                "issue_id": "ISSUE-2",
                "statement": "Statutory exemption preserving registered partitions executed prior to 20 December 2004 under Section 6(1) proviso",
                "governing_statute": "IND-STAT-HSA-1956 Section 6(1) Proviso",
                "relationship_type": "STATUTORY_EXCEPTION",
                "prerequisite_issue_id": "ISSUE-1",
            })
            issue_dependencies.append({
                "dependent_issue_id": "ISSUE-2",
                "governing_issue_id": "ISSUE-1",
                "dependency_type": "STATUTORY_SAVINGS_PROVISO",
                "description": "Section 6(1) proviso saves partitions and dispositions executed before 20 December 2004 from being reopened."
            })
            statutory_exceptions.append("Section 6(1) Proviso HSA: Nothing contained in sub-section (1) shall affect or invalidate any disposition or alienation, including any partition, which took place before 20 December 2004.")
            material_unknowns.append({
                "unknown_fact": "Date and registration status of family partition",
                "governing_provision": "Section 6(1) Proviso, Hindu Succession Act, 1956",
                "legal_consequence": "If partition was registered before 20 Dec 2004, it is protected; if executed thereafter, daughter is entitled to reopen coparcenary share.",
            })

        # Compound Pattern 3: Cheque Bounce NI Act Sec 138 Notice + Sec 142 Limitation
        elif any(t in q_lower for t in ["cheque bounce", "section 138", "dishonour", "138 of ni act"]):
            decomposed_issues.append({
                "issue_id": "ISSUE-1",
                "statement": "Service of 15-day statutory demand notice within 30 days of dishonour memo under Section 138 proviso (b)",
                "governing_statute": "IND-STAT-NI-1881 Section 138",
                "relationship_type": "PROCEDURAL_PREREQUISITE",
                "prerequisite_issue_id": None,
            })
            decomposed_issues.append({
                "issue_id": "ISSUE-2",
                "statement": "Limitation period of 1 month for institution of criminal complaint under Section 142(1)(b) of Negotiable Instruments Act",
                "governing_statute": "IND-STAT-NI-1881 Section 142(1)(b)",
                "relationship_type": "PRIMARY_RULE",
                "prerequisite_issue_id": "ISSUE-1",
            })
            issue_dependencies.append({
                "dependent_issue_id": "ISSUE-2",
                "governing_issue_id": "ISSUE-1",
                "dependency_type": "PROCEDURAL_PREREQUISITE",
                "description": "Cause of action under Section 142 arises only upon failure of drawer to pay within 15 days of statutory notice under Section 138(c)."
            })
            statutory_exceptions.append("Section 142(1)(b) Proviso NI Act: Court may take cognizance of complaint after 1-month limitation period if complainant satisfies court of sufficient cause.")

        # Compound Pattern 4: Retrenchment under IDA Sec 25F + Uncommenced Labour Code
        elif ("retrenchment" in q_lower or "25f" in q_lower) and any(t in q_lower for t in ["labour code", "code on wages", "industrial relations code"]) and not any(t in q_lower for t in ["definition", "2(s)", "managerial exclusion", "override"]):
            decomposed_issues.append({
                "issue_id": "ISSUE-1",
                "statement": "Substantive validity and conditions precedent for retrenchment of workmen under Section 25F Industrial Disputes Act, 1947",
                "governing_statute": "IND-STAT-IDA-1947 Section 25F",
                "relationship_type": "PRIMARY_RULE",
                "prerequisite_issue_id": None,
            })
            decomposed_issues.append({
                "issue_id": "ISSUE-2",
                "statement": "Inapplicability of uncommenced Industrial Relations Code, 2020 pending Central Government Gazette commencement notification",
                "governing_statute": "IND-STAT-IRCODE-2020 Section 1(3)",
                "relationship_type": "UNCOMMENCED_REGIME",
                "prerequisite_issue_id": None,
            })
            issue_dependencies.append({
                "dependent_issue_id": "ISSUE-2",
                "governing_issue_id": "ISSUE-1",
                "dependency_type": "TEMPORAL_COEXISTENCE",
                "description": "Predecessor Act (IDA 1947) remains operative substantive law; uncommenced Code cannot be enforced."
            })

        # Compound Pattern 5: Commercial Courts Act Sec 12A Mediation + Urgent Interim Relief
        elif ("commercial court" in q_lower or "12a" in q_lower or "pre-institution mediation" in q_lower) and ("urgent" in q_lower or "interim" in q_lower or "suit" in q_lower):
            decomposed_issues.append({
                "issue_id": "ISSUE-1",
                "statement": "Mandatory nature of pre-institution mediation under Section 12A Commercial Courts Act, 2015",
                "governing_statute": "IND-STAT-COMMERCIAL_COURTS-2015 Section 12A",
                "relationship_type": "PRIMARY_RULE",
                "prerequisite_issue_id": None,
            })
            decomposed_issues.append({
                "issue_id": "ISSUE-2",
                "statement": "Statutory exemption from pre-institution mediation where urgent interim relief is contemplated",
                "governing_statute": "IND-STAT-COMMERCIAL_COURTS-2015 Section 12A(1)",
                "relationship_type": "STATUTORY_EXCEPTION",
                "prerequisite_issue_id": "ISSUE-1",
            })
            issue_dependencies.append({
                "dependent_issue_id": "ISSUE-2",
                "governing_issue_id": "ISSUE-1",
                "dependency_type": "STATUTORY_EXCEPTION",
                "description": "Section 12A(1) exempts suits that contemplate urgent interim relief from mandatory pre-institution mediation."
            })
            statutory_exceptions.append("Section 12A(1) Commercial Courts Act: Suit which does not contemplate any urgent interim relief shall not be instituted unless plaintiff exhausts pre-institution mediation.")

        # Compound Pattern 6: IBC Sec 32A Clean Slate + Promoter Liability Proviso
        elif ("ibc" in q_lower or "clean slate" in q_lower or "resolution plan" in q_lower) and ("promoter" in q_lower or "director" in q_lower or "offence" in q_lower or "32a" in q_lower):
            decomposed_issues.append({
                "issue_id": "ISSUE-1",
                "statement": "Cessation of liability of corporate debtor for prior offences upon approval of resolution plan under Section 32A(1) IBC",
                "governing_statute": "IND-STAT-IBC-2016 Section 32A(1)",
                "relationship_type": "PRIMARY_RULE",
                "prerequisite_issue_id": None,
            })
            decomposed_issues.append({
                "issue_id": "ISSUE-2",
                "statement": "Continuation of liability and prosecution of erstwhile promoters/directors under Section 32A(1) proviso",
                "governing_statute": "IND-STAT-IBC-2016 Section 32A(1) Proviso",
                "relationship_type": "STATUTORY_EXCEPTION",
                "prerequisite_issue_id": "ISSUE-1",
            })
            issue_dependencies.append({
                "dependent_issue_id": "ISSUE-2",
                "governing_issue_id": "ISSUE-1",
                "dependency_type": "STATUTORY_EXCEPTION",
                "description": "Section 32A(1) proviso explicitly preserves criminal liability of designated partner, promoter, or key managerial personnel."
            })
            statutory_exceptions.append("Section 32A(1) Proviso IBC: Every person who was a designated partner or officer in default shall continue to be liable to be prosecuted and punished.")

        # If decomposed issues identified, update candidate_issues
        if decomposed_issues:
            issues = [d["statement"] for d in decomposed_issues]

        if not issues:
            issues.append(f"Substantive and procedural rights governing '{clean_q[:60]}...' under Indian law")

        # 9. Missing Facts & Clarification Policy
        missing_facts = []
        clarification_necessary = False
        clarification_prompt = None

        # Check if missing transaction date is materially decisive
        temporal_sensitive_terms = [
            "cheating", "electronic record", "forfeiture clause", "unregistered agreement",
            "copyright fair dealing", "patent application", "mva compensation", "accident date",
            "labour code", "wages", "420", "318", "misrepresentation"
        ]
        if any(term in q_lower for term in temporal_sensitive_terms) and not query_date:
            missing_facts.append("Transaction or incident date (decisive across legislative amendment/commencement boundaries)")

        # Check if missing jurisdiction is materially decisive
        jurisdiction_sensitive_terms = [
            "arbitration mandate extension", "section 29a", "rent control", "court fees",
            "quashing petition", "high court rules", "article 226", "writ petition", "writ against"
        ]
        if any(term in q_lower for term in jurisdiction_sensitive_terms) and not detected_jurisdiction:
            missing_facts.append("State or High Court territorial jurisdiction (decisive due to inter-High Court conflicts or state amendments)")

        # Check if document registration is missing for property transactions
        if "part performance" in q_lower or "agreement to sell" in q_lower or "possession" in q_lower:
            if not any(term in q_lower for term in ["registered", "unregistered"]):
                missing_facts.append("Whether the agreement to sell was registered under the Registration Act")

        if missing_facts:
            # Clarification necessary if answering definitively would risk asserting overruled/inapplicable law
            if any(term in q_lower for term in [
                "is my clause valid", "can i evict", "can a landlord evict", "evict",
                "is my petition maintainable", "what is the compensation", "offense of cheating",
                "cheating?", "cheating", "file a writ", "writ petition", "does section 420", "420 ipc or"
            ]):
                clarification_necessary = True
                clarification_prompt = (
                    "To determine the governing legal position accurately, please clarify: "
                    + "; ".join(missing_facts) + "."
                )

        return ParsedLegalQuery(
            original_query=clean_q,
            legal_domain=primary_domain,
            sub_domains=sub_domains,
            candidate_issues=issues,
            events_and_dates=events_and_dates,
            query_date=query_date,
            user_supplied_facts=user_facts,
            alleged_facts_unverified=alleged_facts,
            implicit_assumptions=implicit_assumptions,
            parties_and_roles=parties,
            jurisdiction=detected_jurisdiction,
            applicable_acts=acts,
            candidate_provisions=provisions,
            delegated_instruments=delegated_instruments,
            candidate_precedents=precedents,
            ambiguous_terms=ambiguous_terms,
            missing_facts=missing_facts,
            clarification_necessary=clarification_necessary,
            clarification_prompt=clarification_prompt,
            source_coverage_requirements=acts + [f"Rule: {r}" for r in delegated_instruments],
            is_adversarial_injection=is_adversarial,
            adversarial_notes=adv_notes,
            procedural_posture=posture,
            material_unknowns=material_unknowns,
            issue_dependencies=issue_dependencies,
            decomposed_issues=decomposed_issues,
            statutory_exceptions_identified=statutory_exceptions,
        )
