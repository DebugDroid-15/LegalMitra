"""
LegalMitra Structural Legal Document Diffing Engine (Phase 19)
Compares versions of statutes, provisions, schedules, and definitions.
Distinguishes textual modifications from substantive legal shifts (penalties, remedies, time limits).
"""

from __future__ import annotations

import difflib
from dataclasses import asdict, dataclass, field
from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class LegalModificationType(str, Enum):
    INSERTION = "insertion"
    DELETION = "deletion"
    SUBSTITUTION = "substitution"
    RENUMBERING = "renumbering"
    PENALTY_ENHANCEMENT = "penalty_enhancement"
    PENALTY_REDUCTION = "penalty_reduction"
    LIMITATION_ALTERATION = "limitation_alteration"
    EDITORIAL_OR_TYPO = "editorial_or_typo"
    COMMENCEMENT_MODIFICATION = "commencement_modification"
    NO_SUBSTANTIVE_CHANGE = "no_substantive_change"


@dataclass
class ProvisionDiffResult:
    provision_id: str
    section_number: str
    previous_version_label: str
    new_version_label: str
    modification_type: LegalModificationType
    unified_diff: str
    substantive_summary: str
    amending_instrument_id: Optional[str] = None
    effective_date: Optional[str] = None
    requires_advocate_review: bool = False

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["modification_type"] = self.modification_type.value
        return d


class LegalDiffEngine:
    """
    Compares two statutory provisions and classifies the structural change.
    """

    PENAL_KEYWORDS = ["imprisonment", "fine", "penalty", "punished", "rigorous", "cognizable"]
    TIME_KEYWORDS = ["days", "months", "years", "limitation", "period", "within"]

    @classmethod
    def diff_provisions(
        cls,
        provision_id: str,
        section_number: str,
        old_text: str,
        new_text: str,
        prev_label: str,
        new_label: str,
        amending_instrument: Optional[str] = None,
        effective_date: Optional[str] = None
    ) -> ProvisionDiffResult:
        old_lines = old_text.strip().splitlines(keepends=True)
        new_lines = new_text.strip().splitlines(keepends=True)
        
        diff = "".join(difflib.unified_diff(
            old_lines, new_lines,
            fromfile=f"{section_number} ({prev_label})",
            tofile=f"{section_number} ({new_label})"
        ))

        if not diff.strip():
            return ProvisionDiffResult(
                provision_id=provision_id,
                section_number=section_number,
                previous_version_label=prev_label,
                new_version_label=new_label,
                modification_type=LegalModificationType.NO_SUBSTANTIVE_CHANGE,
                unified_diff="",
                substantive_summary="Texts are identical; zero legal modification.",
                amending_instrument_id=amending_instrument,
                effective_date=effective_date,
                requires_advocate_review=False
            )

        # Detect substantive markers
        old_lower = old_text.lower()
        new_lower = new_text.lower()

        # Check penalties
        has_penal_old = any(k in old_lower for k in cls.PENAL_KEYWORDS)
        has_penal_new = any(k in new_lower for k in cls.PENAL_KEYWORDS)

        # Check limitation/time
        has_time_old = any(k in old_lower for k in cls.TIME_KEYWORDS)
        has_time_new = any(k in new_lower for k in cls.TIME_KEYWORDS)

        if not old_text.strip() and new_text.strip():
            mod_type = LegalModificationType.INSERTION
            summary = f"New provision {section_number} inserted."
            review = False
        elif old_text.strip() and not new_text.strip():
            mod_type = LegalModificationType.DELETION
            summary = f"Provision {section_number} repealed or omitted."
            review = True
        elif has_penal_new and ("seven years" in new_lower or "ten years" in new_lower or "life" in new_lower):
            mod_type = LegalModificationType.PENALTY_ENHANCEMENT
            summary = f"Substantive penal enhancement detected in {section_number}."
            review = True
        elif has_time_old != has_time_new:
            mod_type = LegalModificationType.LIMITATION_ALTERATION
            summary = f"Procedural limitation period altered in {section_number}."
            review = True
        else:
            mod_type = LegalModificationType.SUBSTITUTION
            summary = f"Substantive text substituted in {section_number}."
            review = True

        return ProvisionDiffResult(
            provision_id=provision_id,
            section_number=section_number,
            previous_version_label=prev_label,
            new_version_label=new_label,
            modification_type=mod_type,
            unified_diff=diff,
            substantive_summary=summary,
            amending_instrument_id=amending_instrument,
            effective_date=effective_date,
            requires_advocate_review=review
        )

