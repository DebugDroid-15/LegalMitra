"""
Legal Coverage Gap Analyzer — LegalMitra Phase 52
Implements Workstream D: Corpus Coverage Gap Analysis across 17 Legal Domains
and prioritized acquisition backlog.
"""

import json
import logging
import os
import sqlite3
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Complete 17 Legal Domains Taxonomy for LegalMitra
DOMAINS_TAXONOMY: List[Dict[str, Any]] = [
    {
        "domain_id": "DOM-01-CRIMINAL",
        "name": "Criminal Law & Evidentiary Transition",
        "description": "BNS, BNSS, BSA, IPC, CrPC, IEA, POCSO, Special Criminal Acts",
        "priority_tier": "CRITICAL",
        "current_coverage_status": "HIGH",
        "primary_statutes": ["IND-STAT-BNS-2023", "IND-STAT-BNSS-2023", "IND-STAT-BSA-2023", "IND-ACT-2012-POCSO"],
        "gap_assessment": "Substantive offenses and procedural transition covered. High Court anticipatory bail interpretations under BNSS s.482 pending authentic expansion.",
    },
    {
        "domain_id": "DOM-02-CONSTITUTIONAL",
        "name": "Constitutional Law & Fundamental Rights",
        "description": "Constitution of India, Part III, Part IV, Writs (Art. 32/226), Basic Structure",
        "priority_tier": "CRITICAL",
        "current_coverage_status": "HIGH",
        "primary_statutes": ["IND-CONST-1950"],
        "gap_assessment": "Key articles (14, 19, 20, 21, 32, 226) and Constitution Benches mapped. Center-State legislative relations (Art. 245-254) need further chunking.",
    },
    {
        "domain_id": "DOM-03-DIGITAL-DATA",
        "name": "Information Technology & Digital Data Privacy",
        "description": "IT Act 2000, DPDP Act 2023, SPDI Rules 2011, Intermediary Guidelines 2021",
        "priority_tier": "HIGH",
        "current_coverage_status": "MODERATE",
        "primary_statutes": ["IND-STAT-IT-2000", "IND-STAT-DPDP-2023", "IND-RULE-IT-SPDI-2011", "IND-RULE-IT-INTERMEDIARY-2021"],
        "gap_assessment": "DPDP unnotified sections require temporal guardrails; Cert-In cybersecurity directions not yet ingested.",
    },
    {
        "domain_id": "DOM-04-COMMERCIAL-ARBITRATION",
        "name": "Commercial Law, Arbitration & Dispute Resolution",
        "description": "Arbitration & Conciliation Act 1996, Commercial Courts Act 2015, Mediation Act 2023",
        "priority_tier": "CRITICAL",
        "current_coverage_status": "HIGH",
        "primary_statutes": ["IND-STAT-ARB-1996", "IND-STAT-COMM-COURTS-2015"],
        "gap_assessment": "Arbitration Act well indexed (ss. 8, 9, 11, 34, 37). Mediation Act 2023 remains to be acquired.",
    },
    {
        "domain_id": "DOM-05-CONTRACTS-PROPERTY",
        "name": "Contracts, Specific Relief & Property Law",
        "description": "Indian Contract Act 1872, Specific Relief Act 1963, Transfer of Property Act 1882",
        "priority_tier": "HIGH",
        "current_coverage_status": "HIGH",
        "primary_statutes": ["IND-STAT-ICA-1872", "IND-STAT-SRA-1963", "IND-STAT-TPA-1882"],
        "gap_assessment": "Core sections indexed (ICA ss. 10, 56, 73; SRA ss. 10, 14A, 20; TPA ss. 53A, 54, 58). Easements Act not yet covered.",
    },
    {
        "domain_id": "DOM-06-CIVIL-PROCEDURE",
        "name": "Civil Procedure & Limitation",
        "description": "Code of Civil Procedure 1908, Limitation Act 1963",
        "priority_tier": "HIGH",
        "current_coverage_status": "HIGH",
        "primary_statutes": ["IND-STAT-CPC-1908", "IND-STAT-LIMIT-1963"],
        "gap_assessment": "CPC sections and key Orders (Order VII, Order XXXIX) covered. Detailed procedural rules for specialized High Court original side pending.",
    },
    {
        "domain_id": "DOM-07-CONSUMER-PROTECTION",
        "name": "Consumer Protection & E-Commerce",
        "description": "Consumer Protection Act 2019, CPA E-Commerce Rules 2020",
        "priority_tier": "HIGH",
        "current_coverage_status": "HIGH",
        "primary_statutes": ["IND-STAT-CPA-2019", "IND-RULE-CPA-ECOMMERCE-2020"],
        "gap_assessment": "Statute and e-commerce rules in force; NCDRC appellate precedents sparsely represented.",
    },
    {
        "domain_id": "DOM-08-BANKING-NEGOTIABLE",
        "name": "Banking & Negotiable Instruments",
        "description": "Negotiable Instruments Act 1881, SARFAESI Act 2002, RBI Act 1934",
        "priority_tier": "HIGH",
        "current_coverage_status": "MODERATE",
        "primary_statutes": ["IND-STAT-NI-1881"],
        "gap_assessment": "NI Act Section 138-142 covered with Rangappa precedent. SARFAESI Act and DRT regulations missing.",
    },
    {
        "domain_id": "DOM-09-INTELLECTUAL-PROPERTY",
        "name": "Intellectual Property Law (IPR)",
        "description": "Copyright Act 1957, Patents Act 1970, Trade Marks Act 1999, Designs Act 2000",
        "priority_tier": "HIGH",
        "current_coverage_status": "MODERATE",
        "primary_statutes": ["IND-STAT-CR-1957", "IND-STAT-PAT-1970", "IND-STAT-TM-1999"],
        "gap_assessment": "Key sections and leading Delhi High Court rulings mapped. Patents Act compulsory licensing and Section 3(d) chunks need expansion.",
    },
    {
        "domain_id": "DOM-10-LABOUR-EMPLOYMENT",
        "name": "Labour & Industrial Welfare Codes",
        "description": "Industrial Relations Code 2020, Code on Social Security 2020, Code on Wages 2019, OSH Code 2020",
        "priority_tier": "HIGH",
        "current_coverage_status": "MODERATE",
        "primary_statutes": ["IND-STAT-WAGES-2019", "IND-STAT-IRC-2020", "IND-STAT-SS-2020", "IND-STAT-OSH-2020"],
        "gap_assessment": "Enacted Labour Codes registered with unnotified commencement guardrails; historical Industrial Disputes Act 1947 savings mapped.",
    },
    {
        "domain_id": "DOM-11-CORPORATE-INSOLVENCY",
        "name": "Corporate Law & Insolvency (IBC)",
        "description": "Companies Act 2013, Insolvency and Bankruptcy Code 2016 (IBC)",
        "priority_tier": "CRITICAL",
        "current_coverage_status": "LOW",
        "primary_statutes": ["IND-STAT-COMP-2013", "IND-STAT-IBC-2016"],
        "gap_assessment": "High-priority gap. IBC CIRP regulations and Sections 7, 9, 10, 14, 31 require structured ingestion.",
    },
    {
        "domain_id": "DOM-12-TAXATION-DIRECT-INDIRECT",
        "name": "Direct & Indirect Taxation",
        "description": "Income Tax Act 1961, Central Goods and Services Tax Act 2017 (CGST)",
        "priority_tier": "MEDIUM",
        "current_coverage_status": "LOW",
        "primary_statutes": ["IND-STAT-ITA-1961", "IND-STAT-CGST-2017"],
        "gap_assessment": "High volume domain. GST council notifications and annual Finance Act amendments currently omitted to avoid hallucination.",
    },
    {
        "domain_id": "DOM-13-ENVIRONMENTAL-LAW",
        "name": "Environmental & Forest Conservation",
        "description": "Environment Protection Act 1986, National Green Tribunal Act 2010, Forest Conservation Act 1980",
        "priority_tier": "MEDIUM",
        "current_coverage_status": "LOW",
        "primary_statutes": ["IND-STAT-EPA-1986", "IND-STAT-NGT-2010"],
        "gap_assessment": "NGT principles (polluter pays, precautionary principle) not yet ingested in full.",
    },
    {
        "domain_id": "DOM-14-FAMILY-SUCCESSION",
        "name": "Family & Succession Law",
        "description": "Hindu Marriage Act 1955, Hindu Succession Act 1956, Special Marriage Act 1954, Guardians and Wards Act 1890",
        "priority_tier": "MEDIUM",
        "current_coverage_status": "LOW",
        "primary_statutes": ["IND-STAT-HMA-1955", "IND-STAT-HSA-1956"],
        "gap_assessment": "High-volume personal laws absent from current database; matrimonial relief queries must fail-closed or abstain.",
    },
    {
        "domain_id": "DOM-15-LOCAL-RENT-MUNICIPAL",
        "name": "State Rent Control & Police Legislation",
        "description": "Delhi Rent Control Act 1958, Delhi Police Act 1978, Maharashtra Rent Control Act 1999, Maharashtra Police Act 1951",
        "priority_tier": "MEDIUM",
        "current_coverage_status": "MODERATE",
        "primary_statutes": ["IND-DL-STAT-DRC-1958", "IND-DL-STAT-DPA-1978", "IND-MH-STAT-MRC-1999", "IND-MH-STAT-MPA-1951"],
        "gap_assessment": "State-specific pilot statutes ingested. Other states (e.g. Karnataka, Tamil Nadu, UP) not covered.",
    },
    {
        "domain_id": "DOM-16-MOTOR-ACCIDENTS-TRANSPORT",
        "name": "Motor Accidents & Transport Regulation",
        "description": "Motor Vehicles Act 1988 (as amended 2019), Central Motor Vehicles Rules 1989",
        "priority_tier": "HIGH",
        "current_coverage_status": "HIGH",
        "primary_statutes": ["IND-ACT-1988-MVA"],
        "gap_assessment": "MVA 1988 s.166 compensation principles and hit-and-run provisions ingested.",
    },
    {
        "domain_id": "DOM-17-INFORMATION-GOVERNANCE",
        "name": "Right to Information & Administrative Transparency",
        "description": "Right to Information Act 2005, Whistle Blowers Protection Act 2014",
        "priority_tier": "HIGH",
        "current_coverage_status": "HIGH",
        "primary_statutes": ["IND-ACT-2005-RTI"],
        "gap_assessment": "RTI Act sections 6, 7, 8 (exemptions) and 19 (appeals) fully indexed.",
    },
]


@dataclass
class DomainCoverageReport:
    domain_id: str
    name: str
    priority_tier: str
    current_coverage_status: str
    active_sources_in_db: int
    active_chunks_in_db: int
    gap_assessment: str
    recommended_acquisitions: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CoverageGapAnalysis:
    manifest_version: str
    analysis_id: str
    generated_at: str
    total_domains_audited: int
    domains_by_coverage: Dict[str, int]
    prioritized_acquisition_backlog: List[Dict[str, Any]]
    domain_reports: List[DomainCoverageReport] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["domain_reports"] = [r.to_dict() if hasattr(r, "to_dict") else r for r in self.domain_reports]
        return d


class CoverageGapAnalyzer:
    """
    Evaluates repository legal coverage across 17 legal domains against
    the database chunks and manifests, producing an actionable acquisition backlog.
    """

    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = workspace_root or os.getcwd()
        self.db_path = os.path.join(self.workspace_root, "data", "legalmitra_kb.db")
        self.manifest_dir = os.path.join(self.workspace_root, "data", "22_central_legislation")

    def analyze_coverage(self) -> CoverageGapAnalysis:
        conn = sqlite3.connect(self.db_path) if os.path.exists(self.db_path) else None
        cur = conn.cursor() if conn else None

        # Build map of document_id -> chunk count
        chunk_counts: Dict[str, int] = {}
        if cur:
            cur.execute("SELECT source_id, count(*) FROM legal_chunks WHERE is_synthetic_scaffold = 0 GROUP BY source_id")
            for sid, count in cur.fetchall():
                chunk_counts[sid] = count
            conn.close()

        reports: List[DomainCoverageReport] = []
        coverage_counts = {"HIGH": 0, "MODERATE": 0, "LOW": 0}

        for dom in DOMAINS_TAXONOMY:
            did = dom["domain_id"]
            statutes = dom["primary_statutes"]
            active_srcs = 0
            active_chnks = 0
            for s in statutes:
                if s in chunk_counts:
                    active_srcs += 1
                    active_chnks += chunk_counts[s]

            status = dom["current_coverage_status"]
            coverage_counts[status] = coverage_counts.get(status, 0) + 1

            # Determine recommendations
            recs = []
            if status == "LOW":
                recs.append(f"Acquire primary text of {statutes[0] if statutes else 'core statutes'} from India Code")
                recs.append("Build Gazette-verified temporal versioning map")
            elif status == "MODERATE":
                recs.append("Ingest subordinate rules and High Court precedents")
            else:
                recs.append("Maintain temporal amendment monitor")

            reports.append(
                DomainCoverageReport(
                    domain_id=did,
                    name=dom["name"],
                    priority_tier=dom["priority_tier"],
                    current_coverage_status=status,
                    active_sources_in_db=active_srcs,
                    active_chunks_in_db=active_chnks,
                    gap_assessment=dom["gap_assessment"],
                    recommended_acquisitions=recs,
                )
            )

        # Prioritized backlog
        backlog = [
            {
                "rank": 1,
                "domain_id": "DOM-11-CORPORATE-INSOLVENCY",
                "title": "Insolvency and Bankruptcy Code, 2016 (IBC)",
                "priority": "CRITICAL",
                "rationale": "High-volume corporate disputes; Section 7/9 admission standards and Section 14 moratorium rules frequently litigated.",
            },
            {
                "rank": 2,
                "domain_id": "DOM-14-FAMILY-SUCCESSION",
                "title": "Hindu Succession Act, 1956 (Coparcenary & Gender Parity)",
                "priority": "HIGH",
                "rationale": "Critical personal law questions regarding Vineeta Sharma (2020) coparcenary rights require authentic source texts.",
            },
            {
                "rank": 3,
                "domain_id": "DOM-09-INTELLECTUAL-PROPERTY",
                "title": "Patents Act, 1970 (Section 3(d) & Pharmaceutical Inventions)",
                "priority": "HIGH",
                "rationale": "Technical jurisprudence on patentability standards under Section 3(d) requires authentic statutory chunks.",
            },
            {
                "rank": 4,
                "domain_id": "DOM-12-TAXATION-DIRECT-INDIRECT",
                "title": "Central Goods and Services Tax Act, 2017 (Input Tax Credit)",
                "priority": "MEDIUM",
                "rationale": "High-complexity fiscal statute; requires strict fail-closed guards to prevent hallucination of transitional credit rules.",
            },
            {
                "rank": 5,
                "domain_id": "DOM-13-ENVIRONMENTAL-LAW",
                "title": "National Green Tribunal Act, 2010 (Section 14 & 15 Limitation)",
                "priority": "MEDIUM",
                "rationale": "Environmental statutory jurisdiction and absolute liability doctrines.",
            },
        ]

        analysis = CoverageGapAnalysis(
            manifest_version="1.0.0",
            analysis_id="COVERAGE-GAP-ANALYSIS-PHASE52",
            generated_at=datetime.now(timezone.utc).isoformat(),
            total_domains_audited=len(reports),
            domains_by_coverage=coverage_counts,
            prioritized_acquisition_backlog=backlog,
            domain_reports=reports,
        )
        return analysis

    def generate_analysis(self, output_path: Optional[str] = None) -> str:
        analysis = self.analyze_coverage()
        target = output_path or os.path.join(self.manifest_dir, "coverage_gap_analysis.json")
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            json.dump(analysis.to_dict(), f, indent=2, ensure_ascii=False)
        logger.info(f"Generated Coverage Gap Analysis at {target}")
        return target
