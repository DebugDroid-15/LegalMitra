"""
Phase 94: Pillar 2 — Bhashini Document OCR (Legal FIR, Summons & Deed Parser)
Extracts printed & handwritten regional text from scanned FIR copies, police notices,
court summons, and land agreements across Devanagari, Tamil, Telugu, Bengali, etc.

Key Capabilities:
1. Multi-script OCR ingestion (PDF/PNG/JPEG/TIFF)
2. Indic & Arabic numeral normalization (०-९ -> 0-9)
3. Statutory citation extraction (e.g. कलम ३१८ -> Section 318 BNS, कलम १५४ -> Section 154 CrPC)
4. Direct crosswalk bridging from scanned documents into LegalMitra retrieval engine
"""

from __future__ import annotations

import base64
import logging
import os
import re
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from legalmitra.multilingual.bhashini_gateway import (
    BhashiniTaskType,
    BhashiniULCAGateway,
    ULCAInferenceRequest,
    ULCAInferenceResponse,
)

logger = logging.getLogger("bhashini_ocr")

# Indic Numeral translation maps to standardize section numbers
INDIC_NUMERAL_MAP = str.maketrans(
    "०१२३४५६७८९০১২৩৪৫৬৭৮৯੦੧੨੩੪੫੬੭੮੯૦૧૨૩૪૫૬૭૮૯୦୧୨୩୪୫୬୭୮୯௦౧౨౩౪౫౬౭౮౯౦౧౨౩౪౫౬౭౮౯౦౧౨౩౪౫౬౭౮౯൦൧൨൩൪൫൬൭൮൯",
    "012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789"
)


@dataclass
class ExtractedStatuteMention:
    raw_mention: str
    statute_code: str
    section_number: str
    normalized_canonical: str


@dataclass
class OCRExecutionResult:
    success: bool
    language: str
    extracted_text: str
    detected_statutes: List[ExtractedStatuteMention]
    document_type: str
    latency_ms: float
    provider: str
    error_message: Optional[str] = None


class BhashiniLegalOCREngine:
    """
    Sovereign Document OCR Engine tailored for Indian Police & Judicial documents.
    """

    STATUTE_PATTERNS = [
        # Devanagari Kalam (कलम / धारा)
        (r'(?:कलम|धारा|कलमे|sec|section)\s*([0-9]+(?:\([0-9a-zA-Z]+\))?)', 'BNS'),
        # English Section
        (r'(?:Section|Sec\.?|u/s)\s*([0-9]+(?:\([0-9a-zA-Z]+\))?)\s*(?:of\s+)?(BNS|BNSS|BSA|IPC|CrPC|NIA)', 'STATUTE')
    ]

    def __init__(self, gateway: Optional[BhashiniULCAGateway] = None):
        self.gateway = gateway or BhashiniULCAGateway()

    def normalize_numerals(self, text: str) -> str:
        """Standardizes regional Indic script numerals (Devanagari, Bengali, Tamil, etc.) into Latin 0-9."""
        return text.translate(INDIC_NUMERAL_MAP)

    def detect_document_classification(self, text: str) -> str:
        """Heuristic classifier for official Indian police and court documents."""
        lower = text.lower()
        if any(w in lower for w in ["प्रथम माहिती अहवाल", "प्रथम सूचना रिपोर्ट", "first information report", "fir no"]):
            return "FIRST_INFORMATION_REPORT (FIR)"
        if any(w in lower for w in ["समन्स", "समन", "summons", "warrant", "वॉरंट", "हजर राहणेबाबत"]):
            return "JUDICIAL_SUMMONS_OR_WARRANT"
        if any(w in lower for w in ["तक्रार अर्ज", "तक्रार", "शिकायत", "complaint", "आवेदन"]):
            return "POLICE_COMPLAINT_REPRESENTATION"
        if any(w in lower for w in ["भाडे करार", "किरायानामा", "rent agreement", "lease agreement"]):
            return "LEASE_OR_RENT_AGREEMENT"
        if any(w in lower for w in ["नोटीस", "notice", "कायदेशीर नोटीस", "legal notice"]):
            return "LEGAL_NOTICE"
        return "GENERAL_LEGAL_DOCUMENT"

    def extract_statutory_citations(self, text: str) -> List[ExtractedStatuteMention]:
        """Scans extracted text for explicit IPC/CrPC/BNS/BNSS penal provisions."""
        normalized_text = self.normalize_numerals(text)
        citations = []
        seen = set()

        # Contextual Statute Detection
        default_statute = "BNS"
        if "भा.ना.सु.सं." in text or "BNSS" in text or "नागरिक सुरक्षा" in text:
            default_statute = "BNSS"
        elif "भा.दं.वि." in text or "भा.द.वि." in text or "IPC" in text:
            default_statute = "IPC"
        elif "द.प्र.सं." in text or "CrPC" in text:
            default_statute = "CrPC"

        for pattern, statute_type in self.STATUTE_PATTERNS:
            for match in re.finditer(pattern, normalized_text, re.IGNORECASE):
                sec_num = match.group(1)
                statute = default_statute if statute_type != 'STATUTE' else match.group(2).upper()
                canonical = f"Section {sec_num} {statute}"
                if canonical not in seen:
                    seen.add(canonical)
                    citations.append(ExtractedStatuteMention(
                        raw_mention=match.group(0),
                        statute_code=statute,
                        section_number=sec_num,
                        normalized_canonical=canonical
                    ))
        return citations

    def analyze_document_bytes(
        self,
        doc_bytes: bytes,
        language: str = "mr"
    ) -> OCRExecutionResult:
        """
        Runs OCR on document bytes and performs statutory crosswalk extraction.
        """
        t0 = time.time()
        image_b64 = base64.b64encode(doc_bytes).decode("utf-8")

        req = ULCAInferenceRequest(
            task_type=BhashiniTaskType.OCR,
            source_language=language,
            image_base64=image_b64
        )

        resp: ULCAInferenceResponse = self.gateway.execute_task(req)
        latency_ms = round((time.time() - t0) * 1000, 2)

        if resp.success and resp.output_text:
            text = resp.output_text
            doc_type = self.detect_document_classification(text)
            statutes = self.extract_statutory_citations(text)
            return OCRExecutionResult(
                success=True,
                language=resp.source_language,
                extracted_text=text,
                detected_statutes=statutes,
                document_type=doc_type,
                latency_ms=latency_ms,
                provider=resp.provider
            )
        else:
            return OCRExecutionResult(
                success=False,
                language=language,
                extracted_text="",
                detected_statutes=[],
                document_type="UNKNOWN",
                latency_ms=latency_ms,
                provider=resp.provider,
                error_message=resp.error_message or "OCR extraction failed"
            )

    def analyze_base64(
        self,
        doc_base64: str,
        language: str = "mr"
    ) -> OCRExecutionResult:
        """Analyzes base64-encoded image or document uploaded from web frontend."""
        if "," in doc_base64:
            doc_base64 = doc_base64.split(",", 1)[1]
        try:
            raw_bytes = base64.b64decode(doc_base64)
            return self.analyze_document_bytes(raw_bytes, language=language)
        except Exception as e:
            return OCRExecutionResult(
                success=False,
                language=language,
                extracted_text="",
                detected_statutes=[],
                document_type="ERROR",
                latency_ms=0.0,
                provider="error",
                error_message=f"Failed to decode document base64: {str(e)}"
            )
