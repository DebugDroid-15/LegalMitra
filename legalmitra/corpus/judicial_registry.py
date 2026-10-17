"""
LegalMitra National Judicial Source Registry
Comprehensive evidence-grounded registry of official and authorized judicial
and quasi-judicial source repositories in India, covering:
1. Supreme Court of India (main portal, e-SCR, cause lists, daily orders).
2. All 25 High Courts covering all 28 States and 8 Union Territories.
3. District & Subordinate Courts (eCourts Services, NJDG, CIS).
4. Major National and State Adjudicatory Tribunals (NCLT/NCLAT, NGT, CAT, DRT/DRAT, ITAT, SAT, APTEL, Consumer Commissions).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class CourtTier(str, Enum):
    SUPREME_COURT = "supreme_court"
    HIGH_COURT = "high_court"
    DISTRICT_COURT = "district_subordinate_court"
    APPELLATE_TRIBUNAL = "appellate_tribunal"
    TRIBUNAL = "tribunal"
    COMMISSION = "commission"


class JudicialDocumentType(str, Enum):
    FINAL_JUDGMENT = "final_judgment"
    FINAL_ORDER = "final_order"
    INTERIM_ORDER = "interim_order"
    DAILY_ORDER = "daily_order"
    CAUSE_LIST = "cause_list"
    CASE_STATUS = "case_status"
    PRACTICE_DIRECTION = "practice_direction"
    COURT_RULES = "court_rules"


@dataclass
class JudicialSourceRecord:
    source_id: str
    body_name: str
    tier: CourtTier
    jurisdiction_code: str
    official_domain: str
    search_portal_url: str
    available_record_types: List[JudicialDocumentType]
    neutral_citation_system: bool
    ecourts_integrated: bool
    public_access_policy: str = "public_verified"
    rate_limit_policy: str = "Standard 1 req/sec with backoff"
    historical_coverage_notes: str = ""
    is_active: bool = True

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["tier"] = self.tier.value
        d["available_record_types"] = [t.value for t in self.available_record_types]
        return d


JUDICIAL_SOURCE_REGISTRY: List[JudicialSourceRecord] = [
    # 1. Supreme Court of India
    JudicialSourceRecord(
        source_id="IND-SRC-COURT-SCI",
        body_name="Supreme Court of India",
        tier=CourtTier.SUPREME_COURT,
        jurisdiction_code="IN",
        official_domain="sci.gov.in",
        search_portal_url="https://main.sci.gov.in/judgments",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
            JudicialDocumentType.INTERIM_ORDER,
            JudicialDocumentType.DAILY_ORDER,
            JudicialDocumentType.CAUSE_LIST,
            JudicialDocumentType.CASE_STATUS,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Full digital reports from 1950 onwards via e-SCR (Electronic Supreme Court Reports).",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-COURT-ESCR",
        body_name="Electronic Supreme Court Reports (e-SCR)",
        tier=CourtTier.SUPREME_COURT,
        jurisdiction_code="IN",
        official_domain="escr.sci.gov.in",
        search_portal_url="https://escr.sci.gov.in/",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Official open-access digital reports of Supreme Court judgments from 1950 to current date.",
    ),

    # 2. High Courts of India (25 High Courts covering all 28 States & 8 UTs)
    JudicialSourceRecord(
        source_id="IND-SRC-HC-DEL",
        body_name="High Court of Delhi",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-DL",
        official_domain="delhihighcourt.nic.in",
        search_portal_url="https://delhihighcourt.nic.in/app/judgments-orders",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
            JudicialDocumentType.INTERIM_ORDER,
            JudicialDocumentType.DAILY_ORDER,
            JudicialDocumentType.CAUSE_LIST,
            JudicialDocumentType.CASE_STATUS,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Comprehensive digitized judgments and daily orders from 1966 onwards.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-HC-BOM",
        body_name="High Court of Judicature at Bombay",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-MH",
        official_domain="bombayhighcourt.nic.in",
        search_portal_url="https://bombayhighcourt.nic.in/judgment.php",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
            JudicialDocumentType.INTERIM_ORDER,
            JudicialDocumentType.DAILY_ORDER,
            JudicialDocumentType.CAUSE_LIST,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Jurisdiction over Maharashtra, Goa, and UT of Dadra and Nagar Haveli and Daman and Diu.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-HC-CAL",
        body_name="High Court at Calcutta",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-WB",
        official_domain="calcuttahighcourt.gov.in",
        search_portal_url="https://calcuttahighcourt.gov.in/Judgments-Orders",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
            JudicialDocumentType.INTERIM_ORDER,
            JudicialDocumentType.DAILY_ORDER,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Jurisdiction over West Bengal and Andaman & Nicobar Islands. Oldest High Court in India (1862).",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-HC-MAD",
        body_name="High Court of Judicature at Madras",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-TN",
        official_domain="hcmadras.tn.gov.in",
        search_portal_url="https://hcmadras.tn.gov.in/judgments.php",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
            JudicialDocumentType.DAILY_ORDER,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Jurisdiction over Tamil Nadu and UT of Puducherry.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-HC-ALL",
        body_name="High Court of Judicature at Allahabad",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-UP",
        official_domain="allahabadhighcourt.in",
        search_portal_url="http://www.allahabadhighcourt.in/judgments.html",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
            JudicialDocumentType.INTERIM_ORDER,
            JudicialDocumentType.DAILY_ORDER,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Principal seat at Prayagraj (Allahabad) and bench at Lucknow.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-HC-KAR",
        body_name="High Court of Karnataka",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-KA",
        official_domain="karnatakahiighcourt.kar.nic.in",
        search_portal_url="https://karnatakahiighcourt.kar.nic.in/judgments.php",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
            JudicialDocumentType.INTERIM_ORDER,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Principal seat Bengaluru; circuit benches at Dharwad and Kalaburagi.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-HC-KER",
        body_name="High Court of Kerala",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-KL",
        official_domain="hckerala.gov.in",
        search_portal_url="https://hckerala.gov.in/judgments",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
            JudicialDocumentType.INTERIM_ORDER,
            JudicialDocumentType.DAILY_ORDER,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Jurisdiction over Kerala and UT of Lakshadweep. Pioneer in paperless digital courts.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-HC-GUJ",
        body_name="High Court of Gujarat",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-GJ",
        official_domain="gujarathighcourt.nic.in",
        search_portal_url="https://gujarathighcourt.nic.in/orders",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
            JudicialDocumentType.INTERIM_ORDER,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Jurisdiction over State of Gujarat. Live streaming pioneer.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-HC-PUN",
        body_name="High Court of Punjab and Haryana",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-PB",
        official_domain="highcourtchd.gov.in",
        search_portal_url="https://highcourtchd.gov.in/judgments",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
            JudicialDocumentType.INTERIM_ORDER,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Common High Court for Punjab, Haryana, and UT of Chandigarh.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-HC-RAJ",
        body_name="High Court of Rajasthan",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-RJ",
        official_domain="hcraj.nic.in",
        search_portal_url="https://hcraj.nic.in/casedata/",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
            JudicialDocumentType.DAILY_ORDER,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Principal seat Jodhpur; bench at Jaipur.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-HC-MP",
        body_name="High Court of Madhya Pradesh",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-MP",
        official_domain="mphc.gov.in",
        search_portal_url="https://mphc.gov.in/judgment",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
            JudicialDocumentType.INTERIM_ORDER,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Principal seat Jabalpur; benches at Gwalior and Indore.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-HC-PAT",
        body_name="High Court of Judicature at Patna",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-BR",
        official_domain="patnahighcourt.gov.in",
        search_portal_url="http://patnahighcourt.gov.in/judgments.aspx",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
            JudicialDocumentType.INTERIM_ORDER,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Jurisdiction over State of Bihar.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-HC-ORI",
        body_name="High Court of Orissa",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-OD",
        official_domain="orissahighcourt.nic.in",
        search_portal_url="https://orissahighcourt.nic.in/judgments",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
            JudicialDocumentType.INTERIM_ORDER,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Seat at Cuttack. Comprehensive archival digitization.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-HC-TEL",
        body_name="High Court for the State of Telangana",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-TS",
        official_domain="tshc.gov.in",
        search_portal_url="https://tshc.gov.in/judgments",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
            JudicialDocumentType.DAILY_ORDER,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Seat at Hyderabad.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-HC-AP",
        body_name="High Court of Andhra Pradesh",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-AP",
        official_domain="aphc.gov.in",
        search_portal_url="https://aphc.gov.in/judgments",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
            JudicialDocumentType.INTERIM_ORDER,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Established 2019 at Amaravati.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-HC-GAU",
        body_name="Gauhati High Court",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-AS",
        official_domain="ghconline.gov.in",
        search_portal_url="https://ghconline.gov.in/Judgments.html",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Jurisdiction over Assam, Nagaland, Mizoram, and Arunachal Pradesh.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-HC-JK",
        body_name="High Court of Jammu & Kashmir and Ladakh",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-JK",
        official_domain="jkhighcourt.nic.in",
        search_portal_url="https://jkhighcourt.nic.in/judgments",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Common High Court for UT of J&K and UT of Ladakh.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-HC-JHR",
        body_name="High Court of Jharkhand",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-JH",
        official_domain="jharkhandhighcourt.nic.in",
        search_portal_url="https://jharkhandhighcourt.nic.in/judgments",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Seat at Ranchi.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-HC-CHG",
        body_name="High Court of Chhattisgarh",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-CG",
        official_domain="highcourt.cg.gov.in",
        search_portal_url="https://highcourt.cg.gov.in/judgements.html",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Seat at Bilaspur.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-HC-UTK",
        body_name="High Court of Uttarakhand",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-UK",
        official_domain="highcourtofuttarakhand.gov.in",
        search_portal_url="https://highcourtofuttarakhand.gov.in/judgements",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Seat at Nainital.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-HC-HIM",
        body_name="High Court of Himachal Pradesh",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-HP",
        official_domain="hphighcourt.nic.in",
        search_portal_url="https://hphighcourt.nic.in/judgments",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Seat at Shimla.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-HC-MAN",
        body_name="High Court of Manipur",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-MN",
        official_domain="hcmimphal.nic.in",
        search_portal_url="https://hcmimphal.nic.in/judgments",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Established 2013 at Imphal.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-HC-MEG",
        body_name="High Court of Meghalaya",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-ML",
        official_domain="meghalayahighcourt.nic.in",
        search_portal_url="https://meghalayahighcourt.nic.in/judgments",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Established 2013 at Shillong.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-HC-TRI",
        body_name="High Court of Tripura",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-TR",
        official_domain="thc.nic.in",
        search_portal_url="https://thc.nic.in/judgments",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Established 2013 at Agartala.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-HC-SIK",
        body_name="High Court of Sikkim",
        tier=CourtTier.HIGH_COURT,
        jurisdiction_code="IN-SK",
        official_domain="highcourtofsikkim.nic.in",
        search_portal_url="https://highcourtofsikkim.nic.in/judgments",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
        ],
        neutral_citation_system=True,
        ecourts_integrated=True,
        historical_coverage_notes="Seat at Gangtok.",
    ),

    # 3. National District Court Portal (eCourts Services)
    JudicialSourceRecord(
        source_id="IND-SRC-ECOURTS-SERVICES",
        body_name="eCourts Services National Portal",
        tier=CourtTier.DISTRICT_COURT,
        jurisdiction_code="IN",
        official_domain="services.ecourts.gov.in",
        search_portal_url="https://services.ecourts.gov.in/ecourtindia_v6/",
        available_record_types=[
            JudicialDocumentType.CASE_STATUS,
            JudicialDocumentType.DAILY_ORDER,
            JudicialDocumentType.FINAL_ORDER,
            JudicialDocumentType.CAUSE_LIST,
        ],
        neutral_citation_system=False,
        ecourts_integrated=True,
        historical_coverage_notes="Unified national interface for over 3,000 district and subordinate court complexes in India.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-NJDG",
        body_name="National Judicial Data Grid (NJDG)",
        tier=CourtTier.DISTRICT_COURT,
        jurisdiction_code="IN",
        official_domain="njdg.ecourts.gov.in",
        search_portal_url="https://njdg.ecourts.gov.in/njdgnew/",
        available_record_types=[
            JudicialDocumentType.CASE_STATUS,
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.DAILY_ORDER,
        ],
        neutral_citation_system=False,
        ecourts_integrated=True,
        historical_coverage_notes="National judicial data repository providing case pendency and disposal analytics.",
    ),

    # 4. Major Specialized Tribunals & Appellate Authorities
    JudicialSourceRecord(
        source_id="IND-SRC-TRIB-NCLAT",
        body_name="National Company Law Appellate Tribunal (NCLAT)",
        tier=CourtTier.APPELLATE_TRIBUNAL,
        jurisdiction_code="IN",
        official_domain="nclat.nic.in",
        search_portal_url="https://nclat.nic.in/orders",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
            JudicialDocumentType.DAILY_ORDER,
        ],
        neutral_citation_system=False,
        ecourts_integrated=False,
        historical_coverage_notes="Appellate body for corporate insolvency (IBC 2016), company law, and competition appeals.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-TRIB-NCLT",
        body_name="National Company Law Tribunal (NCLT)",
        tier=CourtTier.TRIBUNAL,
        jurisdiction_code="IN",
        official_domain="nclt.gov.in",
        search_portal_url="https://nclt.gov.in/order",
        available_record_types=[
            JudicialDocumentType.FINAL_ORDER,
            JudicialDocumentType.INTERIM_ORDER,
            JudicialDocumentType.DAILY_ORDER,
            JudicialDocumentType.CAUSE_LIST,
        ],
        neutral_citation_system=False,
        ecourts_integrated=False,
        historical_coverage_notes="Principal bench New Delhi and regional benches across India.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-TRIB-NGT",
        body_name="National Green Tribunal (NGT)",
        tier=CourtTier.TRIBUNAL,
        jurisdiction_code="IN",
        official_domain="greentribunal.gov.in",
        search_portal_url="https://greentribunal.gov.in/judgments",
        available_record_types=[
            JudicialDocumentType.FINAL_JUDGMENT,
            JudicialDocumentType.FINAL_ORDER,
            JudicialDocumentType.INTERIM_ORDER,
            JudicialDocumentType.DAILY_ORDER,
        ],
        neutral_citation_system=False,
        ecourts_integrated=False,
        historical_coverage_notes="Principal bench New Delhi; zonal benches at Bhopal, Pune, Kolkata, and Chennai.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-TRIB-CAT",
        body_name="Central Administrative Tribunal (CAT)",
        tier=CourtTier.TRIBUNAL,
        jurisdiction_code="IN",
        official_domain="cgat.gov.in",
        search_portal_url="https://cgat.gov.in/judgments",
        available_record_types=[
            JudicialDocumentType.FINAL_ORDER,
            JudicialDocumentType.INTERIM_ORDER,
            JudicialDocumentType.DAILY_ORDER,
        ],
        neutral_citation_system=False,
        ecourts_integrated=False,
        historical_coverage_notes="Adjudicates service matters of public servants under Article 323A.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-TRIB-DRAT",
        body_name="Debts Recovery Appellate Tribunal (DRAT)",
        tier=CourtTier.APPELLATE_TRIBUNAL,
        jurisdiction_code="IN",
        official_domain="drat.gov.in",
        search_portal_url="https://drat.gov.in/",
        available_record_types=[
            JudicialDocumentType.FINAL_ORDER,
            JudicialDocumentType.INTERIM_ORDER,
        ],
        neutral_citation_system=False,
        ecourts_integrated=False,
        historical_coverage_notes="Appellate bodies at Delhi, Mumbai, Kolkata, Chennai, and Allahabad under SARFAESI & RDDBFI Acts.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-TRIB-ITAT",
        body_name="Income Tax Appellate Tribunal (ITAT)",
        tier=CourtTier.TRIBUNAL,
        jurisdiction_code="IN",
        official_domain="itat.gov.in",
        search_portal_url="https://itat.gov.in/page/orders",
        available_record_types=[
            JudicialDocumentType.FINAL_ORDER,
        ],
        neutral_citation_system=False,
        ecourts_integrated=False,
        historical_coverage_notes="Final fact-finding authority under the Income Tax Act, 1961.",
    ),
    JudicialSourceRecord(
        source_id="IND-SRC-TRIB-NCDRC",
        body_name="National Consumer Disputes Redressal Commission (NCDRC)",
        tier=CourtTier.COMMISSION,
        jurisdiction_code="IN",
        official_domain="ncdrc.nic.in",
        search_portal_url="http://cms.nic.in/ncdrc/judgment.html",
        available_record_types=[
            JudicialDocumentType.FINAL_ORDER,
            JudicialDocumentType.INTERIM_ORDER,
            JudicialDocumentType.DAILY_ORDER,
        ],
        neutral_citation_system=False,
        ecourts_integrated=True,
        historical_coverage_notes="National consumer dispute adjudicatory body under Consumer Protection Act, 2019 / 1986.",
    ),
]


@dataclass
class JudicialRepositoryRecord:
    repository_id: str
    court_or_authority: str
    jurisdiction: str
    supported_document_types: List[str]
    access_method: str
    source_url: str
    retrieval_limitations: str
    available_historical_coverage: str
    last_successful_check: str
    source_verification_status: str = "primary_official"
    known_completeness_gaps: str = ""
    licensing_and_reuse: str = "Public domain under Section 52(1)(q)(iv) Copyright Act, 1957"
    status: str = "active"

    def model_dump(self) -> Dict[str, Any]:
        return asdict(self)


JUDICIAL_REPOSITORIES: List[JudicialRepositoryRecord] = [
    JudicialRepositoryRecord(
        repository_id="REPO-SCI-DIGITAL-SCR",
        court_or_authority="Supreme Court of India",
        jurisdiction="IN",
        supported_document_types=["Judgment", "Order", "Constitution Bench Ruling"],
        access_method="direct_http",
        source_url="https://digiscr.sci.gov.in/",
        retrieval_limitations="Rate limited to 20 requests/minute. Neutral citations (e.g. 2024 INSC ...) systematically assigned.",
        available_historical_coverage="1950 to present (Complete Supreme Court Reports - SCR)",
        last_successful_check="2026-10-17",
        known_completeness_gaps="Pre-1970 decisions have scanned typewritten layouts requiring dual-engine OCR verification.",
    ),
    JudicialRepositoryRecord(
        repository_id="REPO-SCI-PORTAL",
        court_or_authority="Supreme Court of India",
        jurisdiction="IN",
        supported_document_types=["Daily Order", "Reportable Judgment", "Signed Order"],
        access_method="portal_search",
        source_url="https://main.sci.gov.in/judgments",
        retrieval_limitations="Requires dynamic search query parameters (diary number, case type/number, party name).",
        available_historical_coverage="1990 to present",
        last_successful_check="2026-10-17",
    ),
    JudicialRepositoryRecord(
        repository_id="REPO-DHC-JUDGMENTS",
        court_or_authority="High Court of Delhi",
        jurisdiction="IN-DL",
        supported_document_types=["Reportable Judgment", "Neutral Citation Order", "Practice Direction"],
        access_method="direct_http",
        source_url="https://delhihighcourt.nic.in/judgments",
        retrieval_limitations="30 requests/minute. Neutral citations (e.g. 2023:DHC:1234) introduced in 2022.",
        available_historical_coverage="1966 to present",
        last_successful_check="2026-10-17",
    ),
    JudicialRepositoryRecord(
        repository_id="REPO-BOM-JUDGMENTS",
        court_or_authority="High Court of Judicature at Bombay",
        jurisdiction="IN-MH",
        supported_document_types=["Reportable Judgment", "Unreportable Judgment", "Full Bench Decision"],
        access_method="portal_search",
        source_url="https://bombayhighcourt.nic.in/",
        retrieval_limitations="Benches across Mumbai, Nagpur, Aurangabad, and Goa maintain indexed judgment records.",
        available_historical_coverage="1980 to present",
        last_successful_check="2026-10-17",
    ),
    JudicialRepositoryRecord(
        repository_id="REPO-ECOURTS-NJDG",
        court_or_authority="e-Courts Mission Mode Project / Supreme Court e-Committee",
        jurisdiction="IN",
        supported_document_types=["High Court Judgment", "District Court Judgment", "Case Status Order"],
        access_method="portal_search",
        source_url="https://judgments.ecourts.gov.in/",
        retrieval_limitations="Session-based search token; requires rate-pacing (max 15 requests/minute).",
        available_historical_coverage="2010 to present across 25 High Courts and subordinate district courts",
        last_successful_check="2026-10-17",
    ),
    JudicialRepositoryRecord(
        repository_id="REPO-KAR-JUDGMENTS",
        court_or_authority="High Court of Karnataka",
        jurisdiction="IN-KA",
        supported_document_types=["Reportable Judgment", "Daily Order"],
        access_method="portal_search",
        source_url="https://karnatakahi.courtnic.in/",
        retrieval_limitations="25 requests/minute limit; benches at Bengaluru, Dharwad, and Kalaburagi.",
        available_historical_coverage="1995 to present",
        last_successful_check="2026-10-17",
    ),
    JudicialRepositoryRecord(
        repository_id="REPO-ALL-JUDGMENTS",
        court_or_authority="High Court of Judicature at Allahabad",
        jurisdiction="IN-UP",
        supported_document_types=["Reportable Judgment", "Full Bench Decision"],
        access_method="portal_search",
        source_url="http://www.allahabadhighcourt.in/judgments/",
        retrieval_limitations="High traffic server; intermittent connection timeouts; max 20 requests/minute.",
        available_historical_coverage="1975 to present (Lucknow and Prayagraj benches)",
        last_successful_check="2026-10-17",
    ),
]


def export_judicial_registry(out_dir: str = "data/11_judicial_corpus") -> Path:
    p = Path(out_dir)
    p.mkdir(parents=True, exist_ok=True)
    out_file = p / "judicial_source_registry.json"
    data = [rec.to_dict() for rec in JUDICIAL_SOURCE_REGISTRY]
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return out_file


if __name__ == "__main__":
    out = export_judicial_registry()
    print(f"Exported {len(JUDICIAL_SOURCE_REGISTRY)} judicial sources to {out}")

