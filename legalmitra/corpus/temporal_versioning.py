"""
LegalMitra Bitemporal Law & Criminal Code Transition Engine
Models bitemporal timelines (valid time vs system time), constitutional and statutory
versioning, and provision-level transition mappings between historic codes (IPC, CrPC, IEA)
and modern criminal codes (BNS, BNSS, BSA).
"""

from __future__ import annotations

import datetime
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class EquivalenceType(str, Enum):
    EQUIVALENT = "equivalent"                          # Direct 1:1 substantive correspondence
    SUCCESSOR_PROVISION = "successor_provision"        # Re-enacted with structural modification
    PARTIAL_OVERLAP = "partial_overlap"                # Subsumed partially or split across multiple sections
    REQUIRES_LEGAL_REVIEW = "requires_legal_review"    # Significant change in punishment, elements, or procedure


class TransitionRegime(str, Enum):
    HISTORIC_PRE_2024 = "historic_pre_2024"            # Governed by IPC 1860 / CrPC 1973 / IEA 1872
    MODERN_POST_2024 = "modern_post_2024"              # Governed by BNS 2023 / BNSS 2023 / BSA 2023
    TRANSITIONAL_SAVINGS = "transitional_savings"      # Pending investigation/trial under BNSS s. 531


@dataclass
class BitemporalRecord:
    """
    Bitemporal state tracking:
    - Valid Time: when the legal rule was in force in the real world
    - System Time: when this record was recorded/ingested in LegalMitra
    """
    valid_from: str                      # YYYY-MM-DD
    valid_to: Optional[str]              # YYYY-MM-DD or None if currently in force
    system_recorded_at: str              # ISO 8601 timestamp
    system_superseded_at: Optional[str] = None  # None if latest known state in system
    confidence_score: float = 1.0

    def is_valid_at(self, target_date_str: str) -> bool:
        """Checks if the rule was operative on target_date in the real world."""
        try:
            t_date = datetime.date.fromisoformat(target_date_str)
            v_from = datetime.date.fromisoformat(self.valid_from)
            if t_date < v_from:
                return False
            if self.valid_to:
                v_to = datetime.date.fromisoformat(self.valid_to)
                if t_date > v_to:
                    return False
            return True
        except ValueError:
            return False

    def is_current_in_system(self) -> bool:
        """True if this is the active, non-superseded record in LegalMitra's database."""
        return self.system_superseded_at is None


@dataclass
class SectionVersion:
    version_id: str
    statute_id: str
    section_number: str
    version_label: str                   # e.g., "Original 1950", "Post-44th Amendment 1978"
    amendment_instrument_id: Optional[str]
    bitemporal: BitemporalRecord
    text: str
    marginal_note: str = ""
    subsections: List[str] = field(default_factory=list)
    provisos: List[str] = field(default_factory=list)
    explanations: List[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        res = asdict(self)
        res["bitemporal"] = asdict(self.bitemporal)
        return res


@dataclass
class CriminalTransitionMapping:
    """
    Explicit provision-level bridge between pre-July 2024 and post-July 2024 criminal codes.
    """
    mapping_id: str
    old_code: str                        # "IPC", "CrPC", "IEA"
    old_section: str                     # e.g., "Section 302", "Section 420"
    old_title: str
    new_code: str                        # "BNS", "BNSS", "BSA"
    new_section: str                     # e.g., "Section 103", "Section 318(4)"
    new_title: str
    equivalence_type: EquivalenceType
    statutory_changes_summary: str
    savings_provision_ref: str           # e.g., "BNSS Section 531(2)(a)", "BNS Section 358"
    key_differences: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CriminalCodeTransitionRegistry:
    """
    Registry providing high-fidelity, bidirectional lookup between Old Codes and New Codes.
    """

    TRANSITION_CUTOFF_DATE = "2024-07-01"

    def __init__(self) -> None:
        self._mappings: Dict[str, CriminalTransitionMapping] = {}
        self._old_to_new_index: Dict[Tuple[str, str], List[CriminalTransitionMapping]] = {}
        self._new_to_old_index: Dict[Tuple[str, str], List[CriminalTransitionMapping]] = {}
        self._load_core_mappings()

    def register_mapping(self, mapping: CriminalTransitionMapping) -> None:
        self._mappings[mapping.mapping_id] = mapping
        
        old_key = (mapping.old_code.upper(), mapping.old_section.strip())
        self._old_to_new_index.setdefault(old_key, []).append(mapping)
        
        new_key = (mapping.new_code.upper(), mapping.new_section.strip())
        self._new_to_old_index.setdefault(new_key, []).append(mapping)

    def lookup_old_to_new(self, old_code: str, old_section: str) -> List[CriminalTransitionMapping]:
        key = (old_code.upper(), old_section.strip())
        return self._old_to_new_index.get(key, [])

    def lookup_new_to_old(self, new_code: str, new_section: str) -> List[CriminalTransitionMapping]:
        key = (new_code.upper(), new_section.strip())
        return self._new_to_old_index.get(key, [])

    def determine_governing_regime(self, incident_date_str: str) -> Tuple[TransitionRegime, str]:
        """
        Determines whether IPC/CrPC or BNS/BNSS applies based on the date of alleged offence.
        Under Article 20(1) (Ex-post facto laws), substantive criminal law in force on the date
        of commission strictly governs liability and punishment.
        """
        try:
            inc_date = datetime.date.fromisoformat(incident_date_str)
            cutoff = datetime.date.fromisoformat(self.TRANSITION_CUTOFF_DATE)
            if inc_date < cutoff:
                return (
                    TransitionRegime.HISTORIC_PRE_2024,
                    f"Incident date {incident_date_str} precedes 1 July 2024. Substantive offences governed by "
                    f"Indian Penal Code, 1860; investigation/trial governed by CrPC 1973 under BNSS Section 531 savings."
                )
            else:
                return (
                    TransitionRegime.MODERN_POST_2024,
                    f"Incident date {incident_date_str} is on or after 1 July 2024. Substantive offences governed by "
                    f"Bharatiya Nyaya Sanhita, 2023; procedure governed by Bharatiya Nagarik Suraksha Sanhita, 2023."
                )
        except ValueError:
            return (
                TransitionRegime.TRANSITIONAL_SAVINGS,
                f"Invalid date format '{incident_date_str}'. Defaulting to transitional evaluation."
            )

    def _load_core_mappings(self) -> None:
        """Loads canonical criminal transition provisions between IPC/CrPC/IEA and BNS/BNSS/BSA."""
        core_records = [
            # IPC -> BNS
            CriminalTransitionMapping(
                mapping_id="TRANS-IPC-BNS-302-103",
                old_code="IPC",
                old_section="Section 302",
                old_title="Punishment for murder",
                new_code="BNS",
                new_section="Section 103",
                new_title="Punishment for murder",
                equivalence_type=EquivalenceType.EQUIVALENT,
                statutory_changes_summary="Section 103(1) re-enacts Section 302 IPC. Section 103(2) introduces specific provision for mob lynching / murder by group of 5 or more on specified grounds.",
                savings_provision_ref="BNS Section 358(1) & BNSS Section 531(2)(a)",
                key_differences=["Sub-section (2) introduces mandatory minimum punishment for hate mob lynching."]
            ),
            CriminalTransitionMapping(
                mapping_id="TRANS-IPC-BNS-304A-106",
                old_code="IPC",
                old_section="Section 304A",
                old_title="Causing death by negligence",
                new_code="BNS",
                new_section="Section 106",
                new_title="Causing death by negligence",
                equivalence_type=EquivalenceType.SUCCESSOR_PROVISION,
                statutory_changes_summary="Section 106(1) covers death by rash or negligent act (up to 5 years imprisonment). Section 106(2) provides up to 10 years for hit-and-run failure to report (kept in abeyance pending stakeholder consultation).",
                savings_provision_ref="BNS Section 358",
                key_differences=["Hit-and-run clause Section 106(2) distinguishes registered medical practitioners and drivers."]
            ),
            CriminalTransitionMapping(
                mapping_id="TRANS-IPC-BNS-420-318",
                old_code="IPC",
                old_section="Section 420",
                old_title="Cheating and dishonestly inducing delivery of property",
                new_code="BNS",
                new_section="Section 318(4)",
                new_title="Cheating",
                equivalence_type=EquivalenceType.SUCCESSOR_PROVISION,
                statutory_changes_summary="Consolidates cheating provisions under Section 318. Sub-section (4) corresponds directly to old Section 420 IPC with imprisonment up to seven years and fine.",
                savings_provision_ref="BNS Section 358",
                key_differences=["Consolidated structure under a single section with defined sub-clauses."]
            ),
            CriminalTransitionMapping(
                mapping_id="TRANS-IPC-BNS-378-303",
                old_code="IPC",
                old_section="Section 378",
                old_title="Theft",
                new_code="BNS",
                new_section="Section 303",
                new_title="Theft",
                equivalence_type=EquivalenceType.SUCCESSOR_PROVISION,
                statutory_changes_summary="Definition of theft consolidated in Section 303(1); punishment in Section 303(2). First-time petty theft under Rs. 5,000 may attract community service under proviso.",
                savings_provision_ref="BNS Section 358",
                key_differences=["Proviso introducing community service for first-time petty theft under Rs 5,000 upon restoration."]
            ),
            CriminalTransitionMapping(
                mapping_id="TRANS-IPC-BNS-498A-85",
                old_code="IPC",
                old_section="Section 498A",
                old_title="Husband or relative of husband of a woman subjecting her to cruelty",
                new_code="BNS",
                new_section="Section 85",
                new_title="Husband or relative of husband of a woman subjecting her to cruelty",
                equivalence_type=EquivalenceType.EQUIVALENT,
                statutory_changes_summary="Section 85 replicates Section 498A IPC verbatim in substantive elements and penal scope (imprisonment up to 3 years and fine).",
                savings_provision_ref="BNS Section 358",
                key_differences=["Repositioned from Chapter XXA IPC into Chapter V BNS (Offences against Women and Children)."]
            ),
            # CrPC -> BNSS
            CriminalTransitionMapping(
                mapping_id="TRANS-CRPC-BNSS-154-173",
                old_code="CrPC",
                old_section="Section 154",
                old_title="Information in cognizable cases (FIR)",
                new_code="BNSS",
                new_section="Section 173",
                new_title="Information in cognizable cases (Zero FIR & e-FIR)",
                equivalence_type=EquivalenceType.SUCCESSOR_PROVISION,
                statutory_changes_summary="Formalizes Zero FIR (irrespective of jurisdiction) and e-FIR with signature requirement within three days under Section 173(1). Preliminary enquiry permitted for offences punishable between 3 to 7 years.",
                savings_provision_ref="BNSS Section 531(2)(a)",
                key_differences=["Express recognition of electronic FIR and preliminary inquiry mechanism within 14 days."]
            ),
            CriminalTransitionMapping(
                mapping_id="TRANS-CRPC-BNSS-437-480",
                old_code="CrPC",
                old_section="Section 437",
                old_title="When bail may be taken in case of non-bailable offence",
                new_code="BNSS",
                new_section="Section 480",
                new_title="When bail may be taken in case of non-bailable offence",
                equivalence_type=EquivalenceType.EQUIVALENT,
                statutory_changes_summary="Substantive provisions governing regular bail before Magistrate for non-bailable offences retained under Section 480 BNSS.",
                savings_provision_ref="BNSS Section 531(2)(a)",
                key_differences=["Renumbered under Chapter XXXV of BNSS."]
            ),
            CriminalTransitionMapping(
                mapping_id="TRANS-CRPC-BNSS-438-482",
                old_code="CrPC",
                old_section="Section 438",
                old_title="Direction for grant of bail to person apprehending arrest (Anticipatory Bail)",
                new_code="BNSS",
                new_section="Section 482",
                new_title="Direction for grant of bail to person apprehending arrest",
                equivalence_type=EquivalenceType.EQUIVALENT,
                statutory_changes_summary="Anticipatory bail powers of Court of Session and High Court re-enacted under Section 482 BNSS.",
                savings_provision_ref="BNSS Section 531(2)(a)",
                key_differences=["State amendments to Section 438 CrPC (e.g., UP, West Bengal) subject to interpretation under Section 531."]
            ),
            CriminalTransitionMapping(
                mapping_id="TRANS-CRPC-BNSS-439-483",
                old_code="CrPC",
                old_section="Section 439",
                old_title="Special powers of High Court or Court of Session regarding bail",
                new_code="BNSS",
                new_section="Section 483",
                new_title="Special powers of High Court or Court of Session regarding bail",
                equivalence_type=EquivalenceType.EQUIVALENT,
                statutory_changes_summary="Powers of High Court and Sessions Court to release on bail or cancel bail retained under Section 483 BNSS.",
                savings_provision_ref="BNSS Section 531(2)(a)",
                key_differences=["Direct equivalent."]
            ),
            CriminalTransitionMapping(
                mapping_id="TRANS-CRPC-BNSS-436A-479",
                old_code="CrPC",
                old_section="Section 436A",
                old_title="Maximum period for which an undertrial prisoner can be detained",
                new_code="BNSS",
                new_section="Section 479",
                new_title="Maximum period for which an undertrial prisoner can be detained",
                equivalence_type=EquivalenceType.SUCCESSOR_PROVISION,
                statutory_changes_summary="Expands undertrial relief: first-time offenders who have never been previously convicted are eligible for release on bail upon completing one-third of maximum sentence.",
                savings_provision_ref="BNSS Section 531(2)(a)",
                key_differences=["Introduces one-third detention threshold for first-time offenders; mandatory application by Jail Superintendent."]
            ),
            # IEA -> BSA
            CriminalTransitionMapping(
                mapping_id="TRANS-IEA-BSA-65B-63",
                old_code="IEA",
                old_section="Section 65B",
                old_title="Admissibility of electronic records",
                new_code="BSA",
                new_section="Section 63",
                new_title="Admissibility of electronic records",
                equivalence_type=EquivalenceType.SUCCESSOR_PROVISION,
                statutory_changes_summary="Electronic records placed on par with primary documentary evidence under Section 57/63 BSA; updated certification requirements incorporating hash algorithms and modern digital forensics.",
                savings_provision_ref="BSA Section 170",
                key_differences=["Expands electronic evidence scope, includes server logs, cloud data, semiconductor memory."]
            ),
        ]
        for rec in core_records:
            self.register_mapping(rec)

    def get_all_mappings(self) -> List[CriminalTransitionMapping]:
        return list(self._mappings.values())

