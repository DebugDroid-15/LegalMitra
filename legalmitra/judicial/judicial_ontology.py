"""LegalMitra Judicial Knowledge Infrastructure — Judicial System Ontology.

Comprehensive machine-readable institutional ontology covering:
- Supreme Court of India
- 25 State/UT High Courts, benches, circuits, and historical predecessor courts
- District and Subordinate Judicial Hierarchy (States and UTs)
- Specialized and Administrative Tribunals (CAT, NCLT, NCLAT, NGT, ITAT, etc.)
- Military Justice System (Armed Forces Tribunal, Courts-Martial)
- Pre-Independence Historical Judicial Archives (Federal Court, Privy Council,
  Presidency Supreme Courts, Sadar Adalats)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class InstitutionTier(str, Enum):
    """Institutional hierarchy tier within the Indian judicial universe."""
    APEX = "APEX"                                # Supreme Court of India
    CONSTITUTIONAL_HIGH_COURT = "HIGH_COURT"   # 25 High Courts
    DISTRICT_SUBORDINATE = "DISTRICT_COURT"    # District & Sessions, CJM, Civil Judge, etc.
    SPECIALIZED_TRIBUNAL = "TRIBUNAL"          # NCLT, NGT, CAT, ITAT, etc.
    MILITARY_JUSTICE = "MILITARY_JUSTICE"      # Armed Forces Tribunal, Courts-Martial
    HISTORICAL_ARCHIVE = "HISTORICAL_ARCHIVE"  # Federal Court, Privy Council, Sadar Adalat


class JurisdictionType(str, Enum):
    """Type of jurisdiction exercised by an institution."""
    ORIGINAL = "ORIGINAL"
    APPELLATE = "APPELLATE"
    WRIT_CONSTITUTIONAL = "WRIT_CONSTITUTIONAL"
    ADVISORY = "ADVISORY"
    SUPERVISORY = "SUPERVISORY"
    REVISIONAL = "REVISIONAL"
    STATUTORY_TRIBUNAL = "STATUTORY_TRIBUNAL"
    MILITARY_SUMMARY = "MILITARY_SUMMARY"
    HISTORICAL_IMPERIAL = "HISTORICAL_IMPERIAL"


@dataclass
class CourtEntity:
    """Represents a court, bench, tribunal, or historical judicial institution."""
    court_id: str
    official_name: str
    tier: InstitutionTier
    jurisdiction_type: List[JurisdictionType]
    state_or_ut: Optional[str] = None
    seat_city: str = ""
    benches_and_circuits: List[str] = field(default_factory=list)
    predecessor_court_ids: List[str] = field(default_factory=list)
    successor_court_id: Optional[str] = None
    established_year: int = 1950
    dissolved_year: Optional[int] = None
    authoritative_reporter: Optional[str] = None
    neutral_citation_supported: bool = False
    is_active: bool = True
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "court_id": self.court_id,
            "official_name": self.official_name,
            "tier": self.tier.value,
            "jurisdiction_type": [j.value for j in self.jurisdiction_type],
            "state_or_ut": self.state_or_ut,
            "seat_city": self.seat_city,
            "benches_and_circuits": self.benches_and_circuits,
            "predecessor_court_ids": self.predecessor_court_ids,
            "successor_court_id": self.successor_court_id,
            "established_year": self.established_year,
            "dissolved_year": self.dissolved_year,
            "authoritative_reporter": self.authoritative_reporter,
            "neutral_citation_supported": self.neutral_citation_supported,
            "is_active": self.is_active,
            "notes": self.notes,
        }


class JudicialSystemOntology:
    """Core catalog and traversal graph for the Indian Judicial System."""

    def __init__(self) -> None:
        self._entities: Dict[str, CourtEntity] = {}
        self._populate_core_institutions()

    def register_entity(self, entity: CourtEntity) -> None:
        self._entities[entity.court_id] = entity

    def get_entity(self, court_id: str) -> Optional[CourtEntity]:
        return self._entities.get(court_id)

    def list_entities_by_tier(self, tier: InstitutionTier) -> List[CourtEntity]:
        return [e for e in self._entities.values() if e.tier == tier]

    def get_predecessor_chain(self, court_id: str) -> List[CourtEntity]:
        """Trace historical predecessors back in time."""
        chain: List[CourtEntity] = []
        curr = self.get_entity(court_id)
        if not curr:
            return chain

        for pred_id in curr.predecessor_court_ids:
            pred = self.get_entity(pred_id)
            if pred:
                chain.append(pred)
                chain.extend(self.get_predecessor_chain(pred_id))
        return chain

    def get_all_entities(self) -> List[CourtEntity]:
        return list(self._entities.values())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_entities": len(self._entities),
            "entities": {cid: ent.to_dict() for cid, ent in self._entities.items()},
        }

    def _populate_core_institutions(self) -> None:
        # 1. Apex Court
        self.register_entity(CourtEntity(
            court_id="IND-SC",
            official_name="Supreme Court of India",
            tier=InstitutionTier.APEX,
            jurisdiction_type=[
                JurisdictionType.ORIGINAL,
                JurisdictionType.APPELLATE,
                JurisdictionType.WRIT_CONSTITUTIONAL,
                JurisdictionType.ADVISORY,
                JurisdictionType.REVISIONAL,
            ],
            state_or_ut="National Capital Territory of Delhi",
            seat_city="New Delhi",
            benches_and_circuits=[],
            predecessor_court_ids=["HIST-FED-COURT", "HIST-PRIVY-COUNCIL"],
            established_year=1950,
            authoritative_reporter="Supreme Court Reports (SCR)",
            neutral_citation_supported=True,
            is_active=True,
            notes="Established on January 28, 1950 under Part V, Chapter IV of the Constitution.",
        ))

        # 2. Historical Apex Predecessors
        self.register_entity(CourtEntity(
            court_id="HIST-FED-COURT",
            official_name="Federal Court of India",
            tier=InstitutionTier.HISTORICAL_ARCHIVE,
            jurisdiction_type=[JurisdictionType.ORIGINAL, JurisdictionType.APPELLATE, JurisdictionType.ADVISORY],
            seat_city="New Delhi",
            successor_court_id="IND-SC",
            established_year=1937,
            dissolved_year=1950,
            authoritative_reporter="Federal Court Reports (FCR)",
            neutral_citation_supported=False,
            is_active=False,
            notes="Established under Government of India Act 1935. Functioned from 1937 until Supreme Court inauguration in 1950.",
        ))

        self.register_entity(CourtEntity(
            court_id="HIST-PRIVY-COUNCIL",
            official_name="Judicial Committee of the Privy Council (Indian Appeals)",
            tier=InstitutionTier.HISTORICAL_ARCHIVE,
            jurisdiction_type=[JurisdictionType.APPELLATE, JurisdictionType.HISTORICAL_IMPERIAL],
            seat_city="London",
            successor_court_id="IND-SC",
            established_year=1833,
            dissolved_year=1949,
            authoritative_reporter="Indian Appeals (L.R. I.A.) / Moore's Indian Appeals",
            neutral_citation_supported=False,
            is_active=False,
            notes="Highest court of appeal for British India until Abolition of Privy Council Jurisdiction Act 1949.",
        ))

        # 3. High Courts (25 High Courts)
        high_courts_spec = [
            ("IND-HC-ALL", "High Court of Judicature at Allahabad", "Uttar Pradesh", "Prayagraj", ["Lucknow Bench"], 1866, ["HIST-HC-AGRA"], "ILR Allahabad / Allahabad Law Journal"),
            ("IND-HC-AND", "High Court of Andhra Pradesh", "Andhra Pradesh", "Amaravati", [], 2019, ["HIST-HC-HYD"], "Andhra Pradesh Law Journal"),
            ("IND-HC-BOM", "High Court of Judicature at Bombay", "Maharashtra", "Mumbai", ["Nagpur", "Aurangabad", "Panaji (Goa)"], 1862, ["HIST-SC-BOMBAY", "HIST-SADAR-BOM"], "ILR Bombay / Bombay Law Reporter"),
            ("IND-HC-CAL", "High Court of Judicature at Fort William in Bengal (Calcutta High Court)", "West Bengal", "Kolkata", ["Circuit Bench at Jalpaiguri", "Circuit Bench at Port Blair (A&N Islands)"], 1862, ["HIST-SC-CALCUTTA", "HIST-SADAR-CAL"], "ILR Calcutta / Calcutta Weekly Notes"),
            ("IND-HC-CHH", "High Court of Chhattisgarh", "Chhattisgarh", "Bilaspur", [], 2000, ["HIST-HC-MP-JAB"], "Chhattisgarh Law Journal"),
            ("IND-HC-DEL", "High Court of Delhi", "NCT of Delhi", "New Delhi", [], 1966, ["HIST-HC-PUNJAB-CIRCUIT"], "Delhi Law Times / ILR Delhi"),
            ("IND-HC-GAU", "Gauhati High Court", "Assam", "Guwahati", ["Kohima (Nagaland)", "Aizawl (Mizoram)", "Itanagar (Arunachal Pradesh)"], 1948, [], "Gauhati Law Reports"),
            ("IND-HC-GUJ", "High Court of Gujarat", "Gujarat", "Ahmedabad", [], 1960, ["IND-HC-BOM"], "Gujarat Law Reporter"),
            ("IND-HC-HP", "High Court of Himachal Pradesh", "Himachal Pradesh", "Shimla", [], 1971, ["HIST-HC-DELHI-HP-BENCH"], "Himachal Law Reporter"),
            ("IND-HC-JK", "High Court of Jammu & Kashmir and Ladakh", "Jammu & Kashmir", "Srinagar & Jammu", [], 1928, [], "JK Law Reporter"),
            ("IND-HC-JHK", "High Court of Jharkhand", "Jharkhand", "Ranchi", [], 2000, ["IND-HC-PAT"], "Jharkhand Cases Digest"),
            ("IND-HC-KAR", "High Court of Karnataka", "Karnataka", "Bengaluru", ["Dharwad", "Kalaburagi"], 1884, ["HIST-CHIEF-COURT-MYSORE"], "Karnataka Law Journal / ILR Karnataka"),
            ("IND-HC-KER", "High Court of Kerala", "Kerala", "Kochi", [], 1956, ["HIST-HC-TRAVANCORE-COCHIN"], "Kerala Law Times / ILR Kerala"),
            ("IND-HC-MP", "High Court of Madhya Pradesh", "Madhya Pradesh", "Jabalpur", ["Gwalior", "Indore"], 1956, ["HIST-HC-NAGPUR"], "Madhya Pradesh Law Journal"),
            ("IND-HC-MAD", "High Court of Judicature at Madras", "Tamil Nadu", "Chennai", ["Madurai Bench"], 1862, ["HIST-SC-MADRAS", "HIST-SADAR-MADRAS"], "Madras Law Journal / ILR Madras"),
            ("IND-HC-MAN", "High Court of Manipur", "Manipur", "Imphal", [], 2013, ["IND-HC-GAU"], "Manipur Law Journal"),
            ("IND-HC-MEG", "High Court of Meghalaya", "Meghalaya", "Shillong", [], 2013, ["IND-HC-GAU"], "Meghalaya Law Reporter"),
            ("IND-HC-ORI", "Orissa High Court", "Odisha", "Cuttack", [], 1948, ["IND-HC-PAT"], "Orissa Law Reviews / ILR Cuttack"),
            ("IND-HC-PAT", "High Court of Judicature at Patna", "Bihar", "Patna", [], 1916, ["IND-HC-CAL"], "Patna Law Journal / ILR Patna"),
            ("IND-HC-PNH", "High Court of Punjab and Haryana", "Punjab & Haryana", "Chandigarh", [], 1947, ["HIST-CHIEF-COURT-PUNJAB", "HIST-HC-LAHORE"], "Punjab Law Reporter / ILR Punjab & Haryana"),
            ("IND-HC-RAJ", "High Court of Judicature for Rajasthan", "Rajasthan", "Jodhpur", ["Jaipur Bench"], 1949, [], "Rajasthan Law Weekly / ILR Rajasthan"),
            ("IND-HC-SIK", "High Court of Sikkim", "Sikkim", "Gangtok", [], 1975, [], "Sikkim Law Journal"),
            ("IND-HC-TEL", "High Court for the State of Telangana", "Telangana", "Hyderabad", [], 2019, ["HIST-HC-HYD"], "Telangana Law Journal"),
            ("IND-HC-TRI", "High Court of Tripura", "Tripura", "Agartala", [], 2013, ["IND-HC-GAU"], "Tripura Law Reports"),
            ("IND-HC-UTT", "High Court of Uttarakhand", "Uttarakhand", "Nainital", [], 2000, ["IND-HC-ALL"], "Uttarakhand Law Decisions"),
        ]

        for cid, name, state, seat, benches, est, preds, rep in high_courts_spec:
            self.register_entity(CourtEntity(
                court_id=cid,
                official_name=name,
                tier=InstitutionTier.CONSTITUTIONAL_HIGH_COURT,
                jurisdiction_type=[
                    JurisdictionType.ORIGINAL,
                    JurisdictionType.APPELLATE,
                    JurisdictionType.WRIT_CONSTITUTIONAL,
                    JurisdictionType.SUPERVISORY,
                    JurisdictionType.REVISIONAL,
                ],
                state_or_ut=state,
                seat_city=seat,
                benches_and_circuits=benches,
                predecessor_court_ids=preds,
                established_year=est,
                authoritative_reporter=rep,
                neutral_citation_supported=True,
                is_active=True,
            ))

        # 4. Specialized and Administrative Tribunals
        tribunals_spec = [
            ("IND-TR-CAT", "Central Administrative Tribunal", "National", "New Delhi", ["19 Benches across India"], 1985, "Administrative Tribunals Act 1985 / Service Matters"),
            ("IND-TR-NCLAT", "National Company Law Appellate Tribunal", "National", "New Delhi", ["Chennai Bench"], 2016, "Companies Act 2013, IBC 2016 Appeals"),
            ("IND-TR-NCLT", "National Company Law Tribunal", "National", "New Delhi", ["16 Benches across major cities"], 2016, "Insolvency, Bankruptcy & Corporate matters"),
            ("IND-TR-NGT", "National Green Tribunal", "National", "New Delhi", ["Bhopal", "Pune", "Kolkata", "Chennai"], 2010, "National Green Tribunal Act 2010 / Environmental matters"),
            ("IND-TR-ITAT", "Income Tax Appellate Tribunal", "National", "Mumbai / New Delhi", ["63 Benches across 27 stations"], 1941, "Income Tax Act 1961 matters"),
            ("IND-TR-CESTAT", "Customs, Excise and Service Tax Appellate Tribunal", "National", "New Delhi", ["Mumbai", "Kolkata", "Chennai", "Bengaluru", "Ahmedabad", "Allahabad", "Chandigarh", "Hyderabad"], 1982, "Customs, Central Excise, Service Tax"),
            ("IND-TR-TDSAT", "Telecom Disputes Settlement and Appellate Tribunal", "National", "New Delhi", [], 2000, "TRAI Act 1997 / Telecom & Broadcasting"),
            ("IND-TR-APTEL", "Appellate Tribunal for Electricity", "National", "New Delhi", [], 2005, "Electricity Act 2003 / Energy"),
            ("IND-TR-DRAT", "Debt Recovery Appellate Tribunal", "National", "New Delhi", ["Mumbai", "Kolkata", "Chennai", "Allahabad"], 1993, "RDDBFI Act 1993 & SARFAESI Act 2002"),
            ("IND-TR-DRT", "Debts Recovery Tribunal", "National", "Various", ["39 Tribunals nationwide"], 1993, "Recovery of debts due to banks and financial institutions"),
            ("IND-TR-NCDRC", "National Consumer Disputes Redressal Commission", "National", "New Delhi", [], 1988, "Consumer Protection Act 1986 / 2019"),
        ]

        for cid, name, state, seat, benches, est, notes in tribunals_spec:
            self.register_entity(CourtEntity(
                court_id=cid,
                official_name=name,
                tier=InstitutionTier.SPECIALIZED_TRIBUNAL,
                jurisdiction_type=[JurisdictionType.STATUTORY_TRIBUNAL, JurisdictionType.APPELLATE],
                state_or_ut=state,
                seat_city=seat,
                benches_and_circuits=benches,
                established_year=est,
                is_active=True,
                notes=notes,
            ))

        # 5. Military Justice
        self.register_entity(CourtEntity(
            court_id="IND-MIL-AFT",
            official_name="Armed Forces Tribunal",
            tier=InstitutionTier.MILITARY_JUSTICE,
            jurisdiction_type=[JurisdictionType.STATUTORY_TRIBUNAL, JurisdictionType.APPELLATE],
            state_or_ut="National",
            seat_city="New Delhi",
            benches_and_circuits=["Chandigarh", "Lucknow", "Kolkata", "Guwahati", "Chennai", "Kochi", "Mumbai", "Jabalpur", "Jaipur", "Srinagar (Circuit)"],
            established_year=2009,
            authoritative_reporter="AFT Reporter / Selected Decisions",
            is_active=True,
            notes="Established under Armed Forces Tribunal Act 2007. Adjudicates disputes regarding commission, appointments, enrollments, and conditions of service; appeals against courts-martial.",
        ))

        self.register_entity(CourtEntity(
            court_id="IND-MIL-CM",
            official_name="Courts-Martial System (Army, Navy, Air Force)",
            tier=InstitutionTier.MILITARY_JUSTICE,
            jurisdiction_type=[JurisdictionType.MILITARY_SUMMARY, JurisdictionType.ORIGINAL],
            state_or_ut="National",
            seat_city="Ad-hoc / Military Formations",
            benches_and_circuits=["General Court-Martial (GCM)", "District Court-Martial (DCM)", "Summary General Court-Martial (SGCM)", "Summary Court-Martial (SCM)"],
            established_year=1950,
            is_active=True,
            notes="Governed under Army Act 1950, Navy Act 1957, Air Force Act 1950. Subject to statutory appeals before the Armed Forces Tribunal.",
        ))

        # 6. District and Subordinate Judicial Framework (Generic Structure Archetype)
        self.register_entity(CourtEntity(
            court_id="IND-DIST-GENERIC",
            official_name="Subordinate Judiciary Hierarchy (District & Sessions Level)",
            tier=InstitutionTier.DISTRICT_SUBORDINATE,
            jurisdiction_type=[JurisdictionType.ORIGINAL, JurisdictionType.APPELLATE, JurisdictionType.REVISIONAL],
            state_or_ut="All States and Union Territories",
            seat_city="District Headquarters Nationwide",
            benches_and_circuits=[
                "Principal District & Sessions Judge",
                "Additional District & Sessions Judge",
                "Chief Judicial Magistrate (CJM) / Chief Metropolitan Magistrate (CMM)",
                "Civil Judge (Senior Division) / Subordinate Judge",
                "Judicial Magistrate 1st Class (JMFC) / Metropolitan Magistrate (MM)",
                "Civil Judge (Junior Division) / Munsif Court",
                "Small Causes Court",
                "Gram Nyayalaya",
            ],
            established_year=1950,
            is_active=True,
            notes="Governed by respective State Judicial Service Rules and High Court administrative superintendence (Art. 227). Case distribution handled via eCourts CIS.",
        ))

        # 7. Historical Pre-Independence Institutions
        self.register_entity(CourtEntity(
            court_id="HIST-SC-CALCUTTA",
            official_name="Supreme Court of Judicature at Fort William in Bengal",
            tier=InstitutionTier.HISTORICAL_ARCHIVE,
            jurisdiction_type=[JurisdictionType.HISTORICAL_IMPERIAL, JurisdictionType.ORIGINAL],
            seat_city="Calcutta",
            successor_court_id="IND-HC-CAL",
            established_year=1774,
            dissolved_year=1862,
            is_active=False,
            notes="Established under Regulating Act 1773. Replaced by Calcutta High Court under Indian High Courts Act 1861.",
        ))

        self.register_entity(CourtEntity(
            court_id="HIST-SC-MADRAS",
            official_name="Supreme Court of Judicature at Madras",
            tier=InstitutionTier.HISTORICAL_ARCHIVE,
            jurisdiction_type=[JurisdictionType.HISTORICAL_IMPERIAL, JurisdictionType.ORIGINAL],
            seat_city="Madras",
            successor_court_id="IND-HC-MAD",
            established_year=1801,
            dissolved_year=1862,
            is_active=False,
            notes="Replaced by Madras High Court under Indian High Courts Act 1861.",
        ))

        self.register_entity(CourtEntity(
            court_id="HIST-SC-BOMBAY",
            official_name="Supreme Court of Judicature at Bombay",
            tier=InstitutionTier.HISTORICAL_ARCHIVE,
            jurisdiction_type=[JurisdictionType.HISTORICAL_IMPERIAL, JurisdictionType.ORIGINAL],
            seat_city="Bombay",
            successor_court_id="IND-HC-BOM",
            established_year=1824,
            dissolved_year=1862,
            is_active=False,
            notes="Replaced by Bombay High Court under Indian High Courts Act 1861.",
        ))
