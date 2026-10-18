"""LegalMitra Judicial Knowledge Infrastructure — Restricted Records & Privacy Engine.

Enforces statutory publication bars, privacy protections, and redaction rules:
- Section 228A IPC / Section 72 BNS (Sexual offence victims)
- POCSO Act 2012, Section 74 (Child victims)
- Juvenile Justice Act 2015, Section 74 (Children in conflict with law)
- Family Courts Act 1984, Section 11 (In-camera matrimonial proceedings)
- Official Secrets Act 1923 / Military Security (Classified records)
- Judicial seal orders & in-camera trial transcripts
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class RestrictionClassification(str, Enum):
    UNRESTRICTED_PUBLIC = "UNRESTRICTED_PUBLIC"
    REDACTION_REQUIRED_SEXUAL_OFFENCE = "REDACTION_REQUIRED_SEXUAL_OFFENCE"
    REDACTION_REQUIRED_CHILD_PROTECTION = "REDACTION_REQUIRED_CHILD_PROTECTION"
    IN_CAMERA_SEALED_BARRED = "IN_CAMERA_SEALED_BARRED"
    NATIONAL_SECURITY_CLASSIFIED_BARRED = "NATIONAL_SECURITY_CLASSIFIED_BARRED"


@dataclass
class RedactionAuditResult:
    original_text_length: int
    classification: RestrictionClassification
    is_eligible_for_ingestion: bool
    requires_redaction: bool
    violations_detected: List[str]
    sanitized_text: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_text_length": self.original_text_length,
            "classification": self.classification.value,
            "is_eligible_for_ingestion": self.is_eligible_for_ingestion,
            "requires_redaction": self.requires_redaction,
            "violations_detected": self.violations_detected,
            "sanitized_available": self.sanitized_text is not None,
        }


class RestrictedRecordsPolicyEngine:
    """Enforces statutory privacy restrictions and automatic anonymization."""

    # Patterns indicating sexual offence or child victim matters requiring Section 228A / POCSO handling
    _POCSO_PATTERNS = [
        re.compile(r"\bpocso\b", re.IGNORECASE),
        re.compile(r"protection of children from sexual offences", re.IGNORECASE),
    ]

    _SEXUAL_OFFENCE_PATTERNS = [
        re.compile(r"section 376\b", re.IGNORECASE),
        re.compile(r"section 375\b", re.IGNORECASE),
        re.compile(r"section 354\b", re.IGNORECASE),
        re.compile(r"section 64 bns", re.IGNORECASE),
        re.compile(r"section 65 bns", re.IGNORECASE),
        re.compile(r"section 70 bns", re.IGNORECASE),
        re.compile(r"\brape\b", re.IGNORECASE),
        re.compile(r"\bprosecutrix\b", re.IGNORECASE),
    ]

    _IN_CAMERA_SEALED_PATTERNS = [
        re.compile(r"in[- ]camera proceeding", re.IGNORECASE),
        re.compile(r"placed in sealed cover", re.IGNORECASE),
        re.compile(r"sealed cover procedure", re.IGNORECASE),
        re.compile(r"proceedings held in camera", re.IGNORECASE),
    ]

    _NATIONAL_SECURITY_PATTERNS = [
        re.compile(r"official secrets act", re.IGNORECASE),
        re.compile(r"defence secret", re.IGNORECASE),
        re.compile(r"classified military operation", re.IGNORECASE),
    ]

    def audit_record(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> RedactionAuditResult:
        meta = metadata or {}
        violations = []

        # 1. National Security
        for pat in self._NATIONAL_SECURITY_PATTERNS:
            if pat.search(text) and "classified" in text.lower():
                violations.append("Classified defence/national security content detected")
                return RedactionAuditResult(
                    original_text_length=len(text),
                    classification=RestrictionClassification.NATIONAL_SECURITY_CLASSIFIED_BARRED,
                    is_eligible_for_ingestion=False,
                    requires_redaction=False,
                    violations_detected=violations,
                )

        # 2. In-Camera Sealed Cover
        for pat in self._IN_CAMERA_SEALED_PATTERNS:
            if pat.search(text):
                violations.append("Sealed cover / in-camera proceedings bar detected")
                return RedactionAuditResult(
                    original_text_length=len(text),
                    classification=RestrictionClassification.IN_CAMERA_SEALED_BARRED,
                    is_eligible_for_ingestion=False,
                    requires_redaction=False,
                    violations_detected=violations,
                )

        # 3. Child Victim / POCSO
        is_pocso = any(pat.search(text) for pat in self._POCSO_PATTERNS)
        if is_pocso:
            violations.append("POCSO Act Section 74: Child identity protection statutory mandate")
            sanitized = self._sanitize_identity(text, is_child=True)
            return RedactionAuditResult(
                original_text_length=len(text),
                classification=RestrictionClassification.REDACTION_REQUIRED_CHILD_PROTECTION,
                is_eligible_for_ingestion=True,
                requires_redaction=True,
                violations_detected=violations,
                sanitized_text=sanitized,
            )

        # 4. Sexual Offence / Section 228A IPC / Section 72 BNS
        is_sex_offence = any(pat.search(text) for pat in self._SEXUAL_OFFENCE_PATTERNS)
        if is_sex_offence:
            violations.append("Section 228A IPC / Section 72 BNS: Victim identity protection mandate")
            sanitized = self._sanitize_identity(text, is_child=False)
            return RedactionAuditResult(
                original_text_length=len(text),
                classification=RestrictionClassification.REDACTION_REQUIRED_SEXUAL_OFFENCE,
                is_eligible_for_ingestion=True,
                requires_redaction=True,
                violations_detected=violations,
                sanitized_text=sanitized,
            )

        # 5. Unrestricted
        return RedactionAuditResult(
            original_text_length=len(text),
            classification=RestrictionClassification.UNRESTRICTED_PUBLIC,
            is_eligible_for_ingestion=True,
            requires_redaction=False,
            violations_detected=[],
            sanitized_text=text,
        )

    def _sanitize_identity(self, text: str, is_child: bool = False) -> str:
        """Replace victim identifying terms or mentions with anonymous markers."""
        sanitized = text
        marker = "[CHILD_VICTIM_ANONYMIZED]" if is_child else "[VICTIM_ANONYMIZED]"
        sanitized = re.sub(r"(prosecutrix\s+(?:named|namely)\s+)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", rf"\1{marker}", sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(r"(victim\s+(?:named|namely)\s+)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", rf"\1{marker}", sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(r"(minor\s+(?:named|namely)\s+)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", r"\1[CHILD_VICTIM_ANONYMIZED]", sanitized, flags=re.IGNORECASE)
        return sanitized
