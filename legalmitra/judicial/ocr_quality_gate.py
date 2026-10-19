"""LegalMitra Judicial Knowledge Infrastructure — OCR Quality Gate & Uncertainty Reporting.

Implements a fail-closed quality assessment layer evaluating Devanagari OCR outputs before
ingestion into legal knowledge bases or retrieval-augmented generation pipelines.

Enforces four explicit operational states:
- OCR_ACCEPTABLE_FOR_RETRIEVAL: Provenance complete, glyph integrity preserved, legal tokens intact.
- OCR_REQUIRES_REVIEW: Minor glyph noise, ambiguous negations, or suspicious ligatures requiring advocate audit.
- OCR_REJECTED: Excessive truncation, replacement characters, corrupted statutory sections, or restricted records.
- SOURCE_PROVENANCE_INCOMPLETE: Missing source URLs, cryptographic hashes, or court attribution.

Preserves the invariant: Low OCR confidence must never silently be interpreted as low legal importance.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from legalmitra.judicial.devanagari_ocr import DevanagariOCREngine, DevanagariOCRResult


class OCRQualityState(str, Enum):
    """Operational status classifications for OCR ingestion and retrieval gates."""
    OCR_ACCEPTABLE_FOR_RETRIEVAL = "OCR_ACCEPTABLE_FOR_RETRIEVAL"
    OCR_REQUIRES_REVIEW = "OCR_REQUIRES_REVIEW"
    OCR_REJECTED = "OCR_REJECTED"
    SOURCE_PROVENANCE_INCOMPLETE = "SOURCE_PROVENANCE_INCOMPLETE"


@dataclass
class OCRQualityAssessment:
    """Detailed quality gate assessment report for a single OCR document or page."""
    state: OCRQualityState
    is_retrieval_eligible: bool
    rejection_reasons: List[str] = field(default_factory=list)
    review_flags: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    provenance_details: Dict[str, Any] = field(default_factory=dict)
    heuristic_confidence: Optional[float] = None  # Explicitly labeled as heuristic, not calibrated probability

    def to_dict(self) -> Dict[str, Any]:
        return {
            "state": self.state.value,
            "is_retrieval_eligible": self.is_retrieval_eligible,
            "rejection_reasons": self.rejection_reasons,
            "review_flags": self.review_flags,
            "metrics": self.metrics,
            "provenance_details": self.provenance_details,
            "heuristic_confidence": round(self.heuristic_confidence, 4) if self.heuristic_confidence is not None else None,
        }


class OCRQualityGate:
    """Fail-closed operational validator for scanned legal texts."""

    MIN_CHAR_COUNT = 50
    MAX_REPLACEMENT_CHARS_FOR_REVIEW = 3
    MAX_RAW_TO_NORM_CER = 0.15

    # Core statutory negation markers in Indian vernacular drafting
    _NEGATION_TERMS = ["नहीं", "न", "अभाव", "बिना", "वर्जित", "अस्वीकृत", "अमान्य"]

    # Statutory section patterns
    _SECTION_PATTERNS = [
        re.compile(r"धारा\s*(\d+[A-Za-z]*)"),
        re.compile(r"अनुच्छेद\s*(\d+[A-Za-z]*)"),
        re.compile(r"(?:Section|Sec\.)\s*(\d+[A-Za-z]*)", re.IGNORECASE),
        re.compile(r"(?:Article|Art\.)\s*(\d+[A-Za-z]*)", re.IGNORECASE),
    ]

    def __init__(self, engine: Optional[DevanagariOCREngine] = None) -> None:
        self.engine = engine or DevanagariOCREngine()

    def evaluate_page(
        self,
        raw_text: str,
        normalized_text: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> OCRQualityAssessment:
        """Execute fail-closed quality evaluation on raw and normalized OCR texts."""
        metadata = metadata or {}
        rejection_reasons: List[str] = []
        review_flags: List[str] = []

        # 1. Normalize if not pre-computed
        if normalized_text is None:
            norm_res = self.engine.normalize(raw_text)
            normalized_text = norm_res.normalized_text
            anomalies = norm_res.detected_anomalies
            ligature_warnings = norm_res.detected_ligature_warnings
            has_repl = norm_res.has_replacement_characters
            legal_tokens = norm_res.legal_tokens_detected
        else:
            norm_res = self.engine.normalize(raw_text)
            anomalies = norm_res.detected_anomalies
            ligature_warnings = norm_res.detected_ligature_warnings
            has_repl = norm_res.has_replacement_characters
            legal_tokens = norm_res.legal_tokens_detected

        # 2. Check Provenance Completeness
        provenance_ok = True
        prov_missing = []
        for req_field in ["page_id", "court_or_source", "source_url"]:
            if not metadata.get(req_field):
                prov_missing.append(req_field)
                provenance_ok = False

        has_hash = bool(
            metadata.get("reference_text_hash")
            or metadata.get("raw_ocr_text_hash")
            or metadata.get("sha256_hash")
        )
        if not has_hash:
            prov_missing.append("cryptographic_hash")
            provenance_ok = False

        if not provenance_ok:
            rejection_reasons.append(
                f"Missing mandatory provenance fields: {', '.join(prov_missing)}"
            )

        # 3. Check Statutory Protection / Privacy Barriers (POCSO, In-Camera, Sealed Records)
        if (
            metadata.get("is_restricted")
            or metadata.get("is_sealed")
            or metadata.get("is_quarantined")
            or "POCSO" in str(metadata.get("privacy_assessment", ""))
            or "IN_CAMERA" in str(metadata.get("privacy_assessment", ""))
        ):
            rejection_reasons.append(
                "Document marked as restricted or subject to statutory non-disclosure bar (POCSO/In-Camera/Quarantined)"
            )

        # 4. Text Completeness & Truncation Check
        stripped_raw = raw_text.strip()
        raw_char_count = len(stripped_raw)
        raw_word_count = len(stripped_raw.split())

        if raw_char_count < self.MIN_CHAR_COUNT:
            rejection_reasons.append(
                f"OCR text truncated or below minimum character threshold ({raw_char_count} < {self.MIN_CHAR_COUNT})"
            )

        # 5. Replacement Character (\ufffd) Lossy Decoding Check
        repl_count = raw_text.count("\ufffd")
        if repl_count > self.MAX_REPLACEMENT_CHARS_FOR_REVIEW:
            rejection_reasons.append(
                f"Severe lossy decoding: {repl_count} Unicode replacement characters detected"
            )
        elif repl_count > 0:
            review_flags.append(
                f"Minor lossy decoding: {repl_count} Unicode replacement characters detected"
            )

        # 6. Illegal Control Characters Check
        control_chars = [ch for ch in raw_text if ord(ch) < 32 and ch not in ("\n", "\r", "\t")]
        if control_chars:
            review_flags.append(f"Found {len(control_chars)} illegal control characters in OCR stream")

        # 7. Ligature & Halant Virama Check
        if ligature_warnings:
            review_flags.extend(ligature_warnings)

        # 8. Negation & Exception Term Analysis
        negations_found = [term for term in self._NEGATION_TERMS if term in normalized_text]
        # Check for isolated / broken negations (e.g. dangling 'न' surrounded by garbage)
        broken_negation = re.findall(r"(?:^|\s)न(?:\s|$)(?!\s*[\u0900-\u097F])", normalized_text)
        if broken_negation:
            review_flags.append("Suspicious isolated negation particle 'न' detected without verbal context")

        # 9. Statutory Section Extraction
        sections_found: List[str] = []
        for pat in self._SECTION_PATTERNS:
            sections_found.extend(pat.findall(normalized_text))

        # Check for corrupted section indicators (e.g. 'धारा' followed immediately by non-digit or symbol)
        corrupted_section = re.findall(r"धारा\s*[\?\!\@\#\$\%\^\&\*]", normalized_text)
        if corrupted_section:
            review_flags.append("Corrupted statutory section syntax detected (e.g. 'धारा ?')")

        # 10. Raw vs Normalized Distortion Check
        edit_dist_cer = DevanagariOCREngine.compute_cer(raw_text, normalized_text)
        if edit_dist_cer > self.MAX_RAW_TO_NORM_CER:
            review_flags.append(
                f"Excessive normalization divergence: CER between raw and normalized is {edit_dist_cer*100:.1f}%"
            )

        # 11. Heuristic Confidence Computation (Explicitly documented as non-probabilistic)
        heuristic_score = 1.0
        if repl_count > 0:
            heuristic_score -= 0.15 * repl_count
        if ligature_warnings:
            heuristic_score -= 0.10 * len(ligature_warnings)
        if edit_dist_cer > 0.05:
            heuristic_score -= 0.10
        if raw_char_count < 100:
            heuristic_score -= 0.20
        heuristic_confidence = max(0.0, min(1.0, heuristic_score))

        # 12. Final State Determination (Fail-Closed)
        if not provenance_ok:
            state = OCRQualityState.SOURCE_PROVENANCE_INCOMPLETE
            eligible = False
        elif rejection_reasons:
            state = OCRQualityState.OCR_REJECTED
            eligible = False
        elif review_flags:
            state = OCRQualityState.OCR_REQUIRES_REVIEW
            eligible = False  # Fail-closed: Requires advocate signoff before retrieval indexing
        else:
            state = OCRQualityState.OCR_ACCEPTABLE_FOR_RETRIEVAL
            eligible = True

        metrics = {
            "raw_char_count": raw_char_count,
            "raw_word_count": raw_word_count,
            "normalized_char_count": len(normalized_text),
            "normalized_word_count": len(normalized_text.split()),
            "replacement_char_count": repl_count,
            "illegal_control_char_count": len(control_chars),
            "orphaned_halant_count": len(ligature_warnings),
            "legal_tokens_detected": legal_tokens,
            "negations_detected": negations_found,
            "sections_detected": sections_found,
            "raw_to_normalized_cer": round(edit_dist_cer, 4),
        }

        provenance_details = {
            "page_id": metadata.get("page_id", "UNKNOWN"),
            "court_or_source": metadata.get("court_or_source", "UNKNOWN"),
            "source_url": metadata.get("source_url", "UNKNOWN"),
            "verification_status": metadata.get("reference_verification_status", "UNVERIFIED"),
            "scan_resolution_dpi": metadata.get("scan_resolution_dpi"),
        }

        return OCRQualityAssessment(
            state=state,
            is_retrieval_eligible=eligible,
            rejection_reasons=rejection_reasons,
            review_flags=review_flags,
            metrics=metrics,
            provenance_details=provenance_details,
            heuristic_confidence=heuristic_confidence,
        )
