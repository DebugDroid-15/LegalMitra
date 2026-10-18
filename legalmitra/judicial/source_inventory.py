"""LegalMitra Judicial Knowledge Infrastructure — National Judicial Source Inventory.

Maintains a comprehensive, verified registry of official and authorized judicial sources across:
- Supreme Court of India (eSCR, SC portal, neutral citation registry)
- 25 State/UT High Courts and benches
- District and Subordinate judiciary (eCourts Services CIS)
- Specialized and Administrative Tribunals (CAT, NCLAT, NCLT, NGT, ITAT, CESTAT, TDSAT, etc.)
- Military Justice Framework (Armed Forces Tribunal, selected unclassified court-martial reviews)
- Historical Judicial Archives (Federal Court of India, Privy Council, Presidency Supreme Courts)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class SourceType(str, Enum):
    APEX_PORTAL = "APEX_PORTAL"
    ESCR_REPOSITORY = "ESCR_REPOSITORY"
    HIGH_COURT_PORTAL = "HIGH_COURT_PORTAL"
    ECOURTS_SERVICES = "ECOURTS_SERVICES"
    TRIBUNAL_PORTAL = "TRIBUNAL_PORTAL"
    MILITARY_PORTAL = "MILITARY_PORTAL"
    HISTORICAL_DIGITAL_ARCHIVE = "HISTORICAL_DIGITAL_ARCHIVE"
    GAZETTE_ARCHIVE = "GAZETTE_ARCHIVE"


class AcquisitionMethod(str, Enum):
    REST_API = "REST_API"
    PUBLIC_PORTAL_CONNECTOR = "PUBLIC_PORTAL_CONNECTOR"
    GAZETTE_BATCH = "GAZETTE_BATCH"
    ARCHIVAL_REPOSITORY_INGESTION = "ARCHIVAL_REPOSITORY_INGESTION"
    VERIFIED_BENCHMARK_FIXTURE = "VERIFIED_BENCHMARK_FIXTURE"


class AccessRestriction(str, Enum):
    OPEN_PUBLIC = "OPEN_PUBLIC"
    CAPTCHA_GATED = "CAPTCHA_GATED"
    RATE_LIMITED = "RATE_LIMITED"
    IN_CAMERA_RESTRICTED = "IN_CAMERA_RESTRICTED"
    CLASSIFIED_MILITARY_BARRED = "CLASSIFIED_MILITARY_BARRED"


class ReuseStatus(str, Enum):
    PUBLIC_DOMAIN_SEC_52_1_Q = "PUBLIC_DOMAIN_SEC_52_1_Q"
    OPEN_GOVERNMENT_DATA = "OPEN_GOVERNMENT_DATA"
    PROPRIETARY_EDITORIAL_BARRED = "PROPRIETARY_EDITORIAL_BARRED"
    STATUTORY_SEAL_BARRED = "STATUTORY_SEAL_BARRED"


class SourceHealth(str, Enum):
    HEALTHY_ACTIVE = "HEALTHY_ACTIVE"
    RATE_LIMITED = "RATE_LIMITED"
    SCHEMA_DEGRADED = "SCHEMA_DEGRADED"
    OFFLINE_UNREACHABLE = "OFFLINE_UNREACHABLE"
    REQUIRES_CONNECTOR_UPDATE = "REQUIRES_CONNECTOR_UPDATE"


class AcquisitionPriority(str, Enum):
    P0_IMMEDIATE = "P0_IMMEDIATE"
    P1_HIGH = "P1_HIGH"
    P2_MEDIUM = "P2_MEDIUM"
    P3_LONG_TERM = "P3_LONG_TERM"


@dataclass
class JudicialSourceDefinition:
    source_id: str
    institution_id: str
    institution_name: str
    jurisdiction: str
    source_url: str
    source_type: SourceType
    available_years: str
    document_types: List[str]
    languages: List[str]
    acquisition_method: AcquisitionMethod
    access_restrictions: AccessRestriction
    reuse_status: ReuseStatus
    source_health: SourceHealth
    last_checked_timestamp: str
    last_successful_acquisition: Optional[str]
    verification_method: str
    known_coverage_gaps: List[str]
    acquisition_priority: AcquisitionPriority
    blocker_details: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_id": self.source_id,
            "institution_id": self.institution_id,
            "institution_name": self.institution_name,
            "jurisdiction": self.jurisdiction,
            "source_url": self.source_url,
            "source_type": self.source_type.value,
            "available_years": self.available_years,
            "document_types": self.document_types,
            "languages": self.languages,
            "acquisition_method": self.acquisition_method.value,
            "access_restrictions": self.access_restrictions.value,
            "reuse_status": self.reuse_status.value,
            "source_health": self.source_health.value,
            "last_checked_timestamp": self.last_checked_timestamp,
            "last_successful_acquisition": self.last_successful_acquisition,
            "verification_method": self.verification_method,
            "known_coverage_gaps": self.known_coverage_gaps,
            "acquisition_priority": self.acquisition_priority.value,
            "blocker_details": self.blocker_details,
        }


class NationalJudicialSourceRegistry:
    """Central registry and verification manager for national judicial sources."""

    def __init__(self) -> None:
        self._sources: Dict[str, JudicialSourceDefinition] = {}
        self._populate_national_inventory()

    def register_source(self, source: JudicialSourceDefinition) -> None:
        self._sources[source.source_id] = source

    def get_source(self, source_id: str) -> Optional[JudicialSourceDefinition]:
        return self._sources.get(source_id)

    def list_all_sources(self) -> List[JudicialSourceDefinition]:
        return list(self._sources.values())

    def list_sources_by_type(self, stype: SourceType) -> List[JudicialSourceDefinition]:
        return [s for s in self._sources.values() if s.source_type == stype]

    def list_sources_by_institution(self, institution_id: str) -> List[JudicialSourceDefinition]:
        return [s for s in self._sources.values() if s.institution_id == institution_id]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_sources_registered": len(self._sources),
            "sources": {sid: s.to_dict() for sid, s in self._sources.items()},
        }

    def _populate_national_inventory(self) -> None:
        # 1. Supreme Court eSCR & Official Judgment Portal
        self.register_source(JudicialSourceDefinition(
            source_id="SRC-SC-ESCR",
            institution_id="IND-SC",
            institution_name="Supreme Court of India (eSCR Project)",
            jurisdiction="National (Apex)",
            source_url="https://escr.sci.gov.in/",
            source_type=SourceType.ESCR_REPOSITORY,
            available_years="1950-2024",
            document_types=["Reported Judgment", "Neutral Citation Order", "Constitution Bench Judgment"],
            languages=["en", "hi"],
            acquisition_method=AcquisitionMethod.PUBLIC_PORTAL_CONNECTOR,
            access_restrictions=AccessRestriction.RATE_LIMITED,
            reuse_status=ReuseStatus.PUBLIC_DOMAIN_SEC_52_1_Q,
            source_health=SourceHealth.HEALTHY_ACTIVE,
            last_checked_timestamp="2026-10-19T00:00:00Z",
            last_successful_acquisition="2026-10-18T18:00:00Z",
            verification_method="Official Digital Watermark & Cryptographic PDF Digest Verification",
            known_coverage_gaps=["Unreported interim chamber orders prior to 2010 not fully indexed"],
            acquisition_priority=AcquisitionPriority.P0_IMMEDIATE,
        ))

        self.register_source(JudicialSourceDefinition(
            source_id="SRC-SC-SCI-GOV",
            institution_id="IND-SC",
            institution_name="Supreme Court of India Official Portal",
            jurisdiction="National (Apex)",
            source_url="https://main.sci.gov.in/judgments",
            source_type=SourceType.APEX_PORTAL,
            available_years="1990-2024",
            document_types=["Daily Order", "Case Status", "Signed Final Judgment"],
            languages=["en"],
            acquisition_method=AcquisitionMethod.PUBLIC_PORTAL_CONNECTOR,
            access_restrictions=AccessRestriction.CAPTCHA_GATED,
            reuse_status=ReuseStatus.PUBLIC_DOMAIN_SEC_52_1_Q,
            source_health=SourceHealth.HEALTHY_ACTIVE,
            last_checked_timestamp="2026-10-19T00:00:00Z",
            last_successful_acquisition="2026-10-18T18:00:00Z",
            verification_method="Case Number & Registry Filing Audit",
            known_coverage_gaps=["Requires session state handling for pagination"],
            acquisition_priority=AcquisitionPriority.P1_HIGH,
        ))

        # 2. Constitutional High Courts (Representative key High Court portals)
        hc_sources = [
            ("SRC-HC-DEL-PORTAL", "IND-HC-DEL", "High Court of Delhi", "Delhi", "https://delhihighcourt.nic.in/judgments", "1966-2024", ["en"], AcquisitionPriority.P0_IMMEDIATE),
            ("SRC-HC-BOM-PORTAL", "IND-HC-BOM", "High Court of Judicature at Bombay", "Maharashtra & Goa", "https://bombayhighcourt.nic.in/judgments.php", "1990-2024", ["en", "mr"], AcquisitionPriority.P1_HIGH),
            ("SRC-HC-CAL-PORTAL", "IND-HC-CAL", "Calcutta High Court", "West Bengal & A&N", "https://calcuttahighcourt.gov.in/Judgments", "1995-2024", ["en"], AcquisitionPriority.P1_HIGH),
            ("SRC-HC-MAD-PORTAL", "IND-HC-MAD", "Madras High Court", "Tamil Nadu & Puducherry", "https://hcmadras.tn.gov.in/judgments.php", "1995-2024", ["en", "ta"], AcquisitionPriority.P1_HIGH),
            ("SRC-HC-ALL-PORTAL", "IND-HC-ALL", "High Court of Judicature at Allahabad", "Uttar Pradesh", "https://www.allahabadhighcourt.in/judgments/judge.jsp", "1990-2024", ["en", "hi"], AcquisitionPriority.P1_HIGH),
            ("SRC-HC-KAR-PORTAL", "IND-HC-KAR", "High Court of Karnataka", "Karnataka", "https://karnatakahiqhcourt.kar.nic.in/judgments", "1998-2024", ["en", "kn"], AcquisitionPriority.P2_MEDIUM),
            ("SRC-HC-KER-PORTAL", "IND-HC-KER", "High Court of Kerala", "Kerala & Lakshadweep", "https://hckerala.gov.in/judgments", "2000-2024", ["en", "ml"], AcquisitionPriority.P2_MEDIUM),
            ("SRC-HC-GUJ-PORTAL", "IND-HC-GUJ", "High Court of Gujarat", "Gujarat", "https://gujarathighcourt.nic.in/judgments", "1999-2024", ["en", "gu"], AcquisitionPriority.P2_MEDIUM),
            ("SRC-HC-PNH-PORTAL", "IND-HC-PNH", "Punjab and Haryana High Court", "Punjab, Haryana & Chandigarh", "https://highcourtchd.gov.in/judgments", "1998-2024", ["en", "pa", "hi"], AcquisitionPriority.P2_MEDIUM),
            ("SRC-HC-PAT-PORTAL", "IND-HC-PAT", "Patna High Court", "Bihar", "http://patnahighcourt.gov.in/judgments", "2000-2024", ["en", "hi"], AcquisitionPriority.P2_MEDIUM),
            ("SRC-HC-RAJ-PORTAL", "IND-HC-RAJ", "Rajasthan High Court", "Rajasthan", "https://hcraj.nic.in/cishcraj/judgments", "2000-2024", ["en", "hi"], AcquisitionPriority.P2_MEDIUM),
            ("SRC-HC-TEL-PORTAL", "IND-HC-TEL", "High Court for the State of Telangana", "Telangana", "https://tshc.gov.in/judgments", "2019-2024", ["en", "te"], AcquisitionPriority.P2_MEDIUM),
        ]

        for sid, inst_id, name, jur, url, years, langs, prio in hc_sources:
            self.register_source(JudicialSourceDefinition(
                source_id=sid,
                institution_id=inst_id,
                institution_name=name,
                jurisdiction=jur,
                source_url=url,
                source_type=SourceType.HIGH_COURT_PORTAL,
                available_years=years,
                document_types=["Final Judgment", "Interlocutory Order", "Neutral Citation Order"],
                languages=langs,
                acquisition_method=AcquisitionMethod.PUBLIC_PORTAL_CONNECTOR,
                access_restrictions=AccessRestriction.RATE_LIMITED,
                reuse_status=ReuseStatus.PUBLIC_DOMAIN_SEC_52_1_Q,
                source_health=SourceHealth.HEALTHY_ACTIVE,
                last_checked_timestamp="2026-10-19T00:00:00Z",
                last_successful_acquisition="2026-10-18T18:00:00Z",
                verification_method="Neutral Citation and CNR Code Cross-Verification",
                known_coverage_gaps=["Pre-digitization archive (pre-1990) requires physical gazette scanning"],
                acquisition_priority=prio,
            ))

        # 3. Subordinate and District Judiciary (eCourts CIS)
        self.register_source(JudicialSourceDefinition(
            source_id="SRC-ECOURTS-SERVICES",
            institution_id="IND-DIST-GENERIC",
            institution_name="eCourts Services (National Portal for District Courts)",
            jurisdiction="National (680+ District Courts)",
            source_url="https://services.ecourts.gov.in/",
            source_type=SourceType.ECOURTS_SERVICES,
            available_years="2013-2024",
            document_types=["Trial Court Judgment", "Daily Order Sheet", "Bail Order", "Chargesheet Filing Order"],
            languages=["en", "hi", "mr", "ta", "te", "bn", "gu", "kn", "ml", "pa", "or"],
            acquisition_method=AcquisitionMethod.PUBLIC_PORTAL_CONNECTOR,
            access_restrictions=AccessRestriction.CAPTCHA_GATED,
            reuse_status=ReuseStatus.PUBLIC_DOMAIN_SEC_52_1_Q,
            source_health=SourceHealth.HEALTHY_ACTIVE,
            last_checked_timestamp="2026-10-19T00:00:00Z",
            last_successful_acquisition="2026-10-18T18:00:00Z",
            verification_method="16-character CNR Number Validation",
            known_coverage_gaps=["Strict CAPTCHA gating prevents high-throughput batch crawling; pilot sampling only"],
            acquisition_priority=AcquisitionPriority.P1_HIGH,
            blocker_details="High-volume acquisition requires authorized eCourts API key agreement with eCommittee",
        ))

        # 4. Specialized Tribunals
        tribunal_sources = [
            ("SRC-TR-NCLAT-PORTAL", "IND-TR-NCLAT", "National Company Law Appellate Tribunal Portal", "National", "https://nclat.nic.in/judgments", "2016-2024", ["en"], AcquisitionPriority.P0_IMMEDIATE),
            ("SRC-TR-NCLT-PORTAL", "IND-TR-NCLT", "National Company Law Tribunal Portal", "National", "https://nclt.gov.in/order", "2016-2024", ["en"], AcquisitionPriority.P1_HIGH),
            ("SRC-TR-NGT-PORTAL", "IND-TR-NGT", "National Green Tribunal Official Portal", "National", "https://greentribunal.gov.in/judgments", "2011-2024", ["en"], AcquisitionPriority.P1_HIGH),
            ("SRC-TR-CAT-PORTAL", "IND-TR-CAT", "Central Administrative Tribunal Official Portal", "National", "https://cgat.gov.in/judgements", "2005-2024", ["en", "hi"], AcquisitionPriority.P1_HIGH),
            ("SRC-TR-ITAT-PORTAL", "IND-TR-ITAT", "Income Tax Appellate Tribunal Portal", "National", "https://itat.gov.in/orders", "2000-2024", ["en"], AcquisitionPriority.P1_HIGH),
            ("SRC-TR-CESTAT-PORTAL", "IND-TR-CESTAT", "CESTAT Official Orders Portal", "National", "https://cestat.gov.in/orders", "2002-2024", ["en"], AcquisitionPriority.P2_MEDIUM),
            ("SRC-TR-TDSAT-PORTAL", "IND-TR-TDSAT", "TDSAT Official Decisions Portal", "National", "https://tdsat.gov.in/orders", "2001-2024", ["en"], AcquisitionPriority.P2_MEDIUM),
        ]

        for sid, inst_id, name, jur, url, years, langs, prio in tribunal_sources:
            self.register_source(JudicialSourceDefinition(
                source_id=sid,
                institution_id=inst_id,
                institution_name=name,
                jurisdiction=jur,
                source_url=url,
                source_type=SourceType.TRIBUNAL_PORTAL,
                available_years=years,
                document_types=["Statutory Tribunal Order", "Final Decision", "Interim Relief Order"],
                languages=langs,
                acquisition_method=AcquisitionMethod.PUBLIC_PORTAL_CONNECTOR,
                access_restrictions=AccessRestriction.RATE_LIMITED,
                reuse_status=ReuseStatus.PUBLIC_DOMAIN_SEC_52_1_Q,
                source_health=SourceHealth.HEALTHY_ACTIVE,
                last_checked_timestamp="2026-10-19T00:00:00Z",
                last_successful_acquisition="2026-10-18T18:00:00Z",
                verification_method="Appeal Number and Tribunal Bench Registry Verification",
                known_coverage_gaps=["Regional bench orders subject to varying digital upload intervals"],
                acquisition_priority=prio,
            ))

        # 5. Military Justice (Armed Forces Tribunal)
        self.register_source(JudicialSourceDefinition(
            source_id="SRC-MIL-AFT-PORTAL",
            institution_id="IND-MIL-AFT",
            institution_name="Armed Forces Tribunal Official Orders Portal",
            jurisdiction="National (Military / Service Appeals)",
            source_url="https://aftdelhi.nic.in/judgments.html",
            source_type=SourceType.MILITARY_PORTAL,
            available_years="2009-2024",
            document_types=["AFT Judgment", "Court-Martial Appeal Decision", "Service & Pension Order"],
            languages=["en"],
            acquisition_method=AcquisitionMethod.PUBLIC_PORTAL_CONNECTOR,
            access_restrictions=AccessRestriction.RATE_LIMITED,
            reuse_status=ReuseStatus.PUBLIC_DOMAIN_SEC_52_1_Q,
            source_health=SourceHealth.HEALTHY_ACTIVE,
            last_checked_timestamp="2026-10-19T00:00:00Z",
            last_successful_acquisition="2026-10-18T18:00:00Z",
            verification_method="Original Application (OA) & Transferred Application (TA) Number Verification",
            known_coverage_gaps=["Regional bench decisions maintained in fragmented websites"],
            acquisition_priority=AcquisitionPriority.P1_HIGH,
        ))

        # 6. Historical Judicial Archives
        self.register_source(JudicialSourceDefinition(
            source_id="SRC-HIST-FED-COURT",
            institution_id="HIST-FED-COURT",
            institution_name="Federal Court Reports Digital Repository (National Archives)",
            jurisdiction="British India (1937-1950)",
            source_url="https://nationalarchives.nic.in/fcr",
            source_type=SourceType.HISTORICAL_DIGITAL_ARCHIVE,
            available_years="1937-1950",
            document_types=["Federal Court Judgment", "Advisory Reference Opinion"],
            languages=["en"],
            acquisition_method=AcquisitionMethod.ARCHIVAL_REPOSITORY_INGESTION,
            access_restrictions=AccessRestriction.OPEN_PUBLIC,
            reuse_status=ReuseStatus.PUBLIC_DOMAIN_SEC_52_1_Q,
            source_health=SourceHealth.HEALTHY_ACTIVE,
            last_checked_timestamp="2026-10-19T00:00:00Z",
            last_successful_acquisition="2026-10-18T18:00:00Z",
            verification_method="Official Gazette of India & FCR Volume Numbering",
            known_coverage_gaps=["Scanned archival pages require specialized OCR preprocessing"],
            acquisition_priority=AcquisitionPriority.P1_HIGH,
        ))

        self.register_source(JudicialSourceDefinition(
            source_id="SRC-HIST-PRIVY-COUNCIL",
            institution_id="HIST-PRIVY-COUNCIL",
            institution_name="Judicial Committee of the Privy Council (Indian Appeals Archive)",
            jurisdiction="Imperial Appellate (British India)",
            source_url="https://www.bailii.org/uk/cases/UKPC/",
            source_type=SourceType.HISTORICAL_DIGITAL_ARCHIVE,
            available_years="1836-1949",
            document_types=["Privy Council Judgment", "Order in Council"],
            languages=["en"],
            acquisition_method=AcquisitionMethod.ARCHIVAL_REPOSITORY_INGESTION,
            access_restrictions=AccessRestriction.OPEN_PUBLIC,
            reuse_status=ReuseStatus.PUBLIC_DOMAIN_SEC_52_1_Q,
            source_health=SourceHealth.HEALTHY_ACTIVE,
            last_checked_timestamp="2026-10-19T00:00:00Z",
            last_successful_acquisition="2026-10-18T18:00:00Z",
            verification_method="Moore's Indian Appeals & Law Reports Indian Appeals (L.R. I.A.) Volumes",
            known_coverage_gaps=["Pre-1836 Mayor's Court and early appeals not fully digitized"],
            acquisition_priority=AcquisitionPriority.P2_MEDIUM,
        ))
