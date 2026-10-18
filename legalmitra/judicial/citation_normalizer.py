"""LegalMitra Judicial Knowledge Infrastructure — Indian Citation Normalizer.

Standardizes, parses, and normalizes Indian judicial citations across:
- Official Neutral Citations (Supreme Court e.g. 2023 INSC 101, High Courts e.g. 2023:DHC:1234)
- Supreme Court Reports (SCR)
- All India Reporter (AIR)
- Supreme Court Cases (SCC)
- Indian Law Reports (ILR)
- State High Court Reporters (DLT, BomCR, MLJ, etc.)
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class ReporterFamily(str, Enum):
    NEUTRAL_SUPREME_COURT = "NEUTRAL_INSC"
    NEUTRAL_HIGH_COURT = "NEUTRAL_HC"
    SUPREME_COURT_REPORTS = "SCR"
    ALL_INDIA_REPORTER = "AIR"
    SUPREME_COURT_CASES = "SCC"
    INDIAN_LAW_REPORTS = "ILR"
    HIGH_COURT_REGIONAL = "HC_REGIONAL"
    UNKNOWN = "UNKNOWN"


@dataclass
class ParsedCitation:
    raw_text: str
    canonical_form: str
    reporter_family: ReporterFamily
    year: int
    court_code: str
    volume: Optional[int] = None
    page_or_number: int = 0
    is_neutral: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "raw_text": self.raw_text,
            "canonical_form": self.canonical_form,
            "reporter_family": self.reporter_family.value,
            "year": self.year,
            "court_code": self.court_code,
            "volume": self.volume,
            "page_or_number": self.page_or_number,
            "is_neutral": self.is_neutral,
        }


class CitationNormalizer:
    """Parses and canonicalizes citations across Indian judicial reporting formats."""

    # Patterns
    # 1. Neutral INSC: e.g. 2023 INSC 101 or 2023 INSC 1234
    _RE_INSC = re.compile(r"\b(19\d{2}|20\d{2})\s+INSC\s+(\d+)\b", re.IGNORECASE)

    # 2. Neutral High Court: e.g. 2023:DHC:1234 or 2024:BHC-OS:456
    _RE_HC_NEUTRAL = re.compile(r"\b(19\d{2}|20\d{2}):([A-Z\-]+):(\d+)\b", re.IGNORECASE)

    # 3. SCC: e.g. (2017) 10 SCC 1 or 2017 (10) SCC 1 or (1973) 4 SCC 225
    _RE_SCC = re.compile(r"\(?(19\d{2}|20\d{2})\)?\s*\(?(\d+)\)?\s+SCC\s+(\d+)", re.IGNORECASE)

    # 4. AIR: e.g. AIR 1973 SC 1461 or AIR 1967 Del 12 or AIR 1950 SC 27
    _RE_AIR = re.compile(r"\bAIR\s+(19\d{2}|20\d{2})\s+([A-Z]+)\s+(\d+)\b", re.IGNORECASE)

    # 5. SCR: e.g. [1973] 4 SCR 225 or (1973) 4 S.C.R. 225 or 1973 (4) SCR 225
    _RE_SCR = re.compile(r"[\[\(]?(19\d{2}|20\d{2})[\]\)]?\s*\(?(\d+)\)?\s+S\.?C\.?R\.?\s+(\d+)", re.IGNORECASE)

    # 6. ILR: e.g. ILR (1975) 1 Del 450 or ILR 1960 Bom 120
    _RE_ILR = re.compile(r"\bILR\s*\(?(19\d{2}|20\d{2})\)?\s*\(?(\d+)?\)?\s*([A-Za-z]+)\s+(\d+)\b", re.IGNORECASE)

    def parse_citation(self, text: str) -> Optional[ParsedCitation]:
        text_clean = text.strip()

        # Check INSC
        m = self._RE_INSC.search(text_clean)
        if m:
            yr = int(m.group(1))
            num = int(m.group(2))
            return ParsedCitation(
                raw_text=text_clean,
                canonical_form=f"{yr} INSC {num}",
                reporter_family=ReporterFamily.NEUTRAL_SUPREME_COURT,
                year=yr,
                court_code="SC",
                volume=None,
                page_or_number=num,
                is_neutral=True,
            )

        # Check HC Neutral
        m = self._RE_HC_NEUTRAL.search(text_clean)
        if m:
            yr = int(m.group(1))
            court_tag = m.group(2).upper()
            num = int(m.group(3))
            return ParsedCitation(
                raw_text=text_clean,
                canonical_form=f"{yr}:{court_tag}:{num}",
                reporter_family=ReporterFamily.NEUTRAL_HIGH_COURT,
                year=yr,
                court_code=court_tag,
                volume=None,
                page_or_number=num,
                is_neutral=True,
            )

        # Check SCC
        m = self._RE_SCC.search(text_clean)
        if m:
            yr = int(m.group(1))
            vol = int(m.group(2))
            pg = int(m.group(3))
            return ParsedCitation(
                raw_text=text_clean,
                canonical_form=f"({yr}) {vol} SCC {pg}",
                reporter_family=ReporterFamily.SUPREME_COURT_CASES,
                year=yr,
                court_code="SC",
                volume=vol,
                page_or_number=pg,
                is_neutral=False,
            )

        # Check AIR
        m = self._RE_AIR.search(text_clean)
        if m:
            yr = int(m.group(1))
            court_raw = m.group(2).upper()
            pg = int(m.group(3))
            return ParsedCitation(
                raw_text=text_clean,
                canonical_form=f"AIR {yr} {court_raw} {pg}",
                reporter_family=ReporterFamily.ALL_INDIA_REPORTER,
                year=yr,
                court_code=court_raw,
                volume=None,
                page_or_number=pg,
                is_neutral=False,
            )

        # Check SCR
        m = self._RE_SCR.search(text_clean)
        if m:
            yr = int(m.group(1))
            vol = int(m.group(2))
            pg = int(m.group(3))
            return ParsedCitation(
                raw_text=text_clean,
                canonical_form=f"[{yr}] {vol} SCR {pg}",
                reporter_family=ReporterFamily.SUPREME_COURT_REPORTS,
                year=yr,
                court_code="SC",
                volume=vol,
                page_or_number=pg,
                is_neutral=False,
            )

        # Check ILR
        m = self._RE_ILR.search(text_clean)
        if m:
            yr = int(m.group(1))
            vol_str = m.group(2)
            vol = int(vol_str) if vol_str else 1
            court_raw = m.group(3).capitalize()
            pg = int(m.group(4))
            return ParsedCitation(
                raw_text=text_clean,
                canonical_form=f"ILR ({yr}) {vol} {court_raw} {pg}",
                reporter_family=ReporterFamily.INDIAN_LAW_REPORTS,
                year=yr,
                court_code=court_raw,
                volume=vol,
                page_or_number=pg,
                is_neutral=False,
            )

        return None

    def extract_citations(self, text: str) -> List[ParsedCitation]:
        """Extract all recognized citations from a body of text."""
        citations: List[ParsedCitation] = []
        seen = set()

        # Find all patterns
        for pattern in [self._RE_INSC, self._RE_HC_NEUTRAL, self._RE_SCC, self._RE_AIR, self._RE_SCR, self._RE_ILR]:
            for match in pattern.finditer(text):
                parsed = self.parse_citation(match.group(0))
                if parsed and parsed.canonical_form not in seen:
                    citations.append(parsed)
                    seen.add(parsed.canonical_form)

        return citations
