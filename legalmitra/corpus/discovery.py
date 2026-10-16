"""
LegalMitra Official Legal Source Discovery & Repository Registry Engine
Catalogs official government repositories, court websites, gazette portals,
access methods, rate limits, reuse rights, and verification reliability.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class AccessMethod(str, Enum):
    REST_API = "rest_api"
    BULK_DOWNLOAD = "bulk_download"
    DIRECT_HTTP = "direct_http"
    PORTAL_PULL = "portal_pull"
    MANUAL_OFFICIAL = "manual_official"


class VerificationTier(str, Enum):
    PRIMARY_OFFICIAL = "primary_official"        # Supreme Court, India Code, e-Gazette
    REGULATORY_OFFICIAL = "regulatory_official"  # RBI, SEBI, CCI, MeitY, MCA
    STATE_OFFICIAL = "state_official"            # State Gazettes, High Courts
    ACADEMIC_PUBLIC = "academic_public"          # Law Commission Reports, Public Archives


@dataclass
class SourceRepository:
    repository_id: str
    name: str
    authority: str
    base_url: str
    scope: str
    document_types: List[str]
    access_method: AccessMethod
    update_frequency: str
    rate_limit_per_minute: int
    licence_or_terms: str
    verification_tier: VerificationTier
    known_limitations: str
    last_checked_date: str = "2026-10-16"
    status: str = "active"

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["access_method"] = self.access_method.value
        d["verification_tier"] = self.verification_tier.value
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SourceRepository:
        d = dict(data)
        d["access_method"] = AccessMethod(d["access_method"])
        d["verification_tier"] = VerificationTier(d["verification_tier"])
        return cls(**d)


class SourceDiscoveryManager:
    """Manages the catalog of official Indian legal repositories."""

    def __init__(self, repos: Optional[List[SourceRepository]] = None):
        self._repos: Dict[str, SourceRepository] = {}
        if repos:
            for repo in repos:
                self.add_repo(repo)

    def add_repo(self, repo: SourceRepository) -> None:
        self._repos[repo.repository_id] = repo

    def get_repo(self, repo_id: str) -> Optional[SourceRepository]:
        return self._repos.get(repo_id)

    def list_repos(self) -> List[SourceRepository]:
        return list(self._repos.values())

    def filter_by_tier(self, tier: VerificationTier) -> List[SourceRepository]:
        return [r for r in self._repos.values() if r.verification_tier == tier]

    def export_json(self, target_path: Path) -> None:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": "1.0.0",
            "total_repositories": len(self._repos),
            "repositories": [r.to_dict() for r in self._repos.values()],
        }
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    @classmethod
    def load_json(cls, source_path: Path) -> SourceDiscoveryManager:
        with open(source_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        repos = [SourceRepository.from_dict(d) for d in payload.get("repositories", [])]
        return cls(repos)


def build_default_source_catalog() -> SourceDiscoveryManager:
    """Builds the comprehensive official source catalog for Indian law."""
    mgr = SourceDiscoveryManager()

    # 1. India Code (Legislative Department, Ministry of Law and Justice)
    mgr.add_repo(SourceRepository(
        repository_id="REPO-INDIA-CODE",
        name="India Code: Digital Repository of All Central and State Acts",
        authority="Legislative Department, Ministry of Law and Justice, Government of India",
        base_url="https://www.indiacode.nic.in/",
        scope="All Central Acts in force, State Acts, and historical consolidated legislation",
        document_types=["Act", "Amendment", "Repealed Act", "Schedule"],
        access_method=AccessMethod.DIRECT_HTTP,
        update_frequency="Weekly",
        rate_limit_per_minute=30,
        licence_or_terms="Government of India Open Data License (GODL-India) / Copyright Act s.52(1)(q)",
        verification_tier=VerificationTier.PRIMARY_OFFICIAL,
        known_limitations="Consolidated acts may experience lag of 1-3 months following major amendments; PDF layout varies."
    ))

    # 2. The e-Gazette of India (Directorate of Printing)
    mgr.add_repo(SourceRepository(
        repository_id="REPO-EGAZETTE",
        name="e-Gazette of India (The Gazette of India)",
        authority="Directorate of Printing, Ministry of Housing and Urban Affairs",
        base_url="https://egazette.gov.in/",
        scope="Official Extraordinary and Ordinary Gazettes: Enactment Assents, Notifications, Rules, and Commencement S.O. Orders",
        document_types=["Notification", "Rule", "Regulation", "Commencement Order", "Bill Assent"],
        access_method=AccessMethod.PORTAL_PULL,
        update_frequency="Daily",
        rate_limit_per_minute=20,
        licence_or_terms="Government of India Official Publication / Public Notice",
        verification_tier=VerificationTier.PRIMARY_OFFICIAL,
        known_limitations="Search index relies on publication date and issue number; scanned PDFs require robust OCR."
    ))

    # 3. Supreme Court of India - Judgments Portal
    mgr.add_repo(SourceRepository(
        repository_id="REPO-SCI-JUDGMENTS",
        name="Supreme Court of India Official Judgments & Orders",
        authority="Supreme Court of India",
        base_url="https://main.sci.gov.in/judgments",
        scope="All reportable and non-reportable judgments, orders, and Constitution Bench decisions",
        document_types=["Judgment", "Order", "Constitution Bench Ruling"],
        access_method=AccessMethod.DIRECT_HTTP,
        update_frequency="Daily upon pronouncement",
        rate_limit_per_minute=20,
        licence_or_terms="Public Domain / Section 52(1)(q)(iv) Copyright Act, 1957",
        verification_tier=VerificationTier.PRIMARY_OFFICIAL,
        known_limitations="Historical judgments pre-1990 have varied optical scan clarity; neutral citations (e.g. 2024 INSC ...) introduced systematically only from 2023."
    ))

    # 4. Supreme Court of India - Practice & Procedure Rules
    mgr.add_repo(SourceRepository(
        repository_id="REPO-SCI-RULES",
        name="Supreme Court Rules & Registry Practice Manuals",
        authority="Supreme Court of India",
        base_url="https://www.sci.gov.in/practice-procedure/",
        scope="Supreme Court Rules 2013, Practice Directions, Circulars, and Office Procedure Handbooks",
        document_types=["Practice Direction", "Rule", "Circular"],
        access_method=AccessMethod.DIRECT_HTTP,
        update_frequency="Monthly / As notified",
        rate_limit_per_minute=30,
        licence_or_terms="Public Domain / Supreme Court Official Publication",
        verification_tier=VerificationTier.PRIMARY_OFFICIAL,
        known_limitations="Large monolithic PDF handbooks (200-300+ pages) exceed default single-pass chunking limits."
    ))

    # 5. Ministry of Electronics and Information Technology (MeitY)
    mgr.add_repo(SourceRepository(
        repository_id="REPO-MEITY",
        name="MeitY Cyber Laws, Data Protection & IT Rules Repository",
        authority="Ministry of Electronics and Information Technology (MeitY)",
        base_url="https://www.meity.gov.in/content/cyber-laws-and-data-protection",
        scope="IT Act 2000, IT Rules 2021, Intermediary Guidelines, DPDP Act rules and notifications",
        document_types=["Act", "Rule", "Notification", "Draft Guidelines"],
        access_method=AccessMethod.DIRECT_HTTP,
        update_frequency="As published",
        rate_limit_per_minute=40,
        licence_or_terms="Government of India Open Data License (GODL-India)",
        verification_tier=VerificationTier.REGULATORY_OFFICIAL,
        known_limitations="Rules and amendment draft notifications are frequently posted in press releases before final gazetting."
    ))

    # 6. Ministry of Corporate Affairs (MCA)
    mgr.add_repo(SourceRepository(
        repository_id="REPO-MCA",
        name="MCA Companies Act, Rules & Circulars Repository",
        authority="Ministry of Corporate Affairs, Government of India",
        base_url="https://www.mca.gov.in/content/mca/global/en/acts-rules.html",
        scope="Companies Act 2013, Companies Rules, General Circulars, Decriminalization Notifications, LLP Act",
        document_types=["Act", "Rule", "Circular", "Form"],
        access_method=AccessMethod.DIRECT_HTTP,
        update_frequency="Weekly",
        rate_limit_per_minute=30,
        licence_or_terms="Government of India Open Data License (GODL-India)",
        verification_tier=VerificationTier.REGULATORY_OFFICIAL,
        known_limitations="MCA portal enforces strict bot mitigation; automated scraping requires controlled pacing and user-agent headers."
    ))

    # 7. Ministry of Home Affairs (MHA)
    mgr.add_repo(SourceRepository(
        repository_id="REPO-MHA",
        name="MHA Criminal Law Reforms & Notification Portal",
        authority="Ministry of Home Affairs, Government of India",
        base_url="https://www.mha.gov.in/",
        scope="Bharatiya Nyaya Sanhita (BNS), BNSS, BSA commencement notifications, SOPs, and police guidelines",
        document_types=["Act", "Notification", "SOP", "Commencement Order"],
        access_method=AccessMethod.DIRECT_HTTP,
        update_frequency="Monthly / As notified",
        rate_limit_per_minute=30,
        licence_or_terms="Government of India Open Data License (GODL-India)",
        verification_tier=VerificationTier.REGULATORY_OFFICIAL,
        known_limitations="Commencement S.O. notifications are published across gazettes and MHA releases."
    ))

    # 8. Law Commission of India Reports
    mgr.add_repo(SourceRepository(
        repository_id="REPO-LAW-COMMISSION",
        name="Law Commission of India Official Reports",
        authority="Law Commission of India, Ministry of Law and Justice",
        base_url="https://lawcommissionofindia.nic.in/reports/",
        scope="Reports 1 through 289 detailing legislative intent, historical background of enactments, and proposed legal reforms",
        document_types=["Report", "Draft Bill"],
        access_method=AccessMethod.DIRECT_HTTP,
        update_frequency="Quarterly / As tabled in Parliament",
        rate_limit_per_minute=25,
        licence_or_terms="Government of India Open Data License (GODL-India)",
        verification_tier=VerificationTier.ACADEMIC_PUBLIC,
        known_limitations="Advisory documents; recommendations do not constitute operative law until enacted by Parliament."
    ))

    # 9. National Green Tribunal (NGT)
    mgr.add_repo(SourceRepository(
        repository_id="REPO-NGT",
        name="National Green Tribunal Judgments & Orders Portal",
        authority="National Green Tribunal (Principal Bench, New Delhi)",
        base_url="https://greentribunal.gov.in/",
        scope="Environmental orders, EIA reviews, pollution directions, and statutory compliance orders",
        document_types=["Judgment", "Order"],
        access_method=AccessMethod.DIRECT_HTTP,
        update_frequency="Daily upon pronouncement",
        rate_limit_per_minute=25,
        licence_or_terms="Public Domain / Section 52(1)(q) Copyright Act, 1957",
        verification_tier=VerificationTier.REGULATORY_OFFICIAL,
        known_limitations="Zonal benches (Western, Eastern, Southern, Central) maintain separate daily cause lists."
    ))

    # 10. High Court of Delhi Official Judgments Portal
    mgr.add_repo(SourceRepository(
        repository_id="REPO-DHC",
        name="Delhi High Court Judgments & Orders Repository",
        authority="High Court of Delhi",
        base_url="https://delhihighcourt.nic.in/",
        scope="Reportable and signed judgments and orders of the High Court of Delhi",
        document_types=["Judgment", "Order", "Practice Direction"],
        access_method=AccessMethod.DIRECT_HTTP,
        update_frequency="Daily",
        rate_limit_per_minute=30,
        licence_or_terms="Public Domain / Section 52(1)(q) Copyright Act, 1957",
        verification_tier=VerificationTier.STATE_OFFICIAL,
        known_limitations="State-level jurisdiction (IN-DL); binding within NCT of Delhi, persuasive for other High Courts."
    ))

    return mgr

