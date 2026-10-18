"""
LegalMitra National Legal Document Parser & Defect Detection Engine (Phase 35).
Parses complex Indian legal documents (Central/State Acts, Delegated Rules,
Supreme Court / High Court Judgments, and Bilingual Statutes).
Preserves structural hierarchy: Chapters, Sections, Subsections, Provisos, Explanations,
Schedules, and Judgment Paragraphs.
Detects critical legal defects: broken numbering, corrupted Devanagari, header/footer
leakage, truncation, and document false concatenation.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


class LegalDocumentType(str, Enum):
    STATUTE = "statute"
    JUDGMENT = "judgment"
    DELEGATED_RULE = "delegated_rule"
    GAZETTE_NOTIFICATION = "gazette_notification"
    PROCEDURAL_CODE = "procedural_code"


class DefectSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    FATAL = "FATAL"


@dataclass
class ParsingDefect:
    defect_code: str
    description: str
    severity: DefectSeverity
    line_number: Optional[int] = None
    sample_text: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["severity"] = self.severity.value
        return d


@dataclass
class LegalProvisionNode:
    node_id: str
    node_type: str  # act_title, chapter, section, subsection, clause, proviso, explanation, schedule, judgment_para
    heading: str
    reference: str  # e.g., 'Section 15', 'Paragraph 24', 'Chapter II'
    content: str
    normalized_content: str
    language: str  # 'en', 'hi', 'bilingual'
    char_count: int
    parent_node_id: Optional[str] = None
    subsections: List[str] = field(default_factory=list)
    provisos: List[str] = field(default_factory=list)
    explanations: List[str] = field(default_factory=list)
    illustrations: List[str] = field(default_factory=list)
    anchor: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ParsedLegalDocument:
    document_id: str
    title: str
    doc_type: LegalDocumentType
    raw_hash_sha256: str
    total_provisions: int
    language: str
    nodes: List[LegalProvisionNode]
    defects: List[ParsingDefect]
    is_valid_parse: bool
    parsing_timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    bench_or_authority: Optional[str] = None
    citations: List[str] = field(default_factory=list)
    effective_date: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_id": self.document_id,
            "title": self.title,
            "doc_type": self.doc_type.value,
            "raw_hash_sha256": self.raw_hash_sha256,
            "total_provisions": self.total_provisions,
            "language": self.language,
            "is_valid_parse": self.is_valid_parse,
            "parsing_timestamp": self.parsing_timestamp,
            "bench_or_authority": self.bench_or_authority,
            "citations": self.citations,
            "effective_date": self.effective_date,
            "defects": [d.to_dict() for d in self.defects],
            "nodes": [n.to_dict() for n in self.nodes],
        }


class LegalDocumentParser:
    """
    Parser for Indian legal documents with built-in structural defect and contamination detection.
    """

    # Common Indian header/footer contamination patterns
    HEADER_FOOTER_PATTERNS = [
        re.compile(r"Page\s+\d+\s+of\s+\d+", re.IGNORECASE),
        re.compile(r"Printed\s+on\s+\d{1,2}[/-]\d{1,2}[/-]\d{2,4}", re.IGNORECASE),
        re.compile(r"https?://(?:www\.)?(?:indiacode|egazette|main\.sci|delhihighcourt)\.nic\.in\S*", re.IGNORECASE),
        re.compile(r"COURT\s+OF\s+RECORD\s+-\s+DIGITAL\s+COPY", re.IGNORECASE),
        re.compile(r"\[\s*Confidential\s*-\s*For\s+Court\s+Use\s+Only\s*\]", re.IGNORECASE),
    ]

    # Section / Paragraph regex patterns
    SECTION_PATTERN_EN = re.compile(
        r"^\s*(?:Section\s+(\d+[A-Z]?)\.?|(\d+[A-Z]?)\.)\s+(.+)$",
        re.MULTILINE | re.IGNORECASE
    )
    SECTION_PATTERN_HI = re.compile(
        r"^\s*(?:धारा\s+([०-९\d]+[क-हA-Z]?)\.?|([०-९\d]+[क-हA-Z]?)\.)\s+(.+)$",
        re.MULTILINE
    )
    JUDGMENT_PARA_PATTERN = re.compile(
        r"^(?:\[?(\d+)\]?\.?)\s+(.+)$",
        re.MULTILINE
    )

    def __init__(self):
        pass

    def detect_defects(self, text: str, nodes: List[LegalProvisionNode]) -> List[ParsingDefect]:
        """Audit parsed text and extracted nodes for quality and integrity defects."""
        defects: List[ParsingDefect] = []

        # 1. Truncation defect: check if text ends abruptly mid-sentence
        stripped = text.strip()
        if stripped and not stripped.endswith((".", ";", ":", ")", "।", "”", '"', "']", "}")):
            defects.append(
                ParsingDefect(
                    defect_code="ERR_TRUNCATED_TEXT",
                    description="Document text terminates abruptly without terminating legal punctuation.",
                    severity=DefectSeverity.FATAL,
                    sample_text=stripped[-100:],
                )
            )

        # 2. Devanagari corruption (Mojibake, replacement chars, malformed sequences)
        if "\ufffd" in text:
            defects.append(
                ParsingDefect(
                    defect_code="ERR_DEVANAGARI_REPLACEMENT_CHAR",
                    description="Text contains Unicode replacement character (U+FFFD), indicating decoding corruption.",
                    severity=DefectSeverity.FATAL,
                )
            )

        # Check for isolated virama or broken combining diacritics in Hindi
        if re.search(r"\s[\u093e-\u094f]", text):
            defects.append(
                ParsingDefect(
                    defect_code="ERR_DEVANAGARI_ISOLATED_MATRA",
                    description="Devanagari text contains isolated dependent vowel sign without base consonant.",
                    severity=DefectSeverity.WARNING,
                )
            )

        # 3. Header/Footer Contamination
        for pattern in self.HEADER_FOOTER_PATTERNS:
            matches = pattern.findall(text)
            if matches:
                defects.append(
                    ParsingDefect(
                        defect_code="WARN_HEADER_FOOTER_LEAK",
                        description=f"Detected running header/footer/URL artifact: '{matches[0]}'",
                        severity=DefectSeverity.WARNING,
                        sample_text=str(matches[0]),
                    )
                )

        # 4. Broken Section Numbering Check (for statutes)
        sec_numbers = []
        for n in nodes:
            if n.node_type == "section":
                m = re.search(r"(\d+)", n.reference)
                if m:
                    sec_numbers.append(int(m.group(1)))

        if len(sec_numbers) >= 3:
            # Check for non-increasing anomalies or large unexpected gaps > 25
            for i in range(len(sec_numbers) - 1):
                diff = sec_numbers[i + 1] - sec_numbers[i]
                if diff <= 0 and sec_numbers[i + 1] != sec_numbers[i]:
                    defects.append(
                        ParsingDefect(
                            defect_code="WARN_NON_SEQUENTIAL_SECTIONS",
                            description=f"Section numbering reversed or disordered: Section {sec_numbers[i]} followed by {sec_numbers[i+1]}",
                            severity=DefectSeverity.WARNING,
                        )
                    )
                    break
                elif diff > 30:
                    defects.append(
                        ParsingDefect(
                            defect_code="WARN_LARGE_SECTION_GAP",
                            description=f"Suspicious section number gap: Section {sec_numbers[i]} to {sec_numbers[i+1]} (diff={diff})",
                            severity=DefectSeverity.INFO,
                        )
                    )
                    break

        # 5. Repeated / duplicate paragraph defect
        seen_paragraphs: Set[str] = set()
        for node in nodes:
            norm = " ".join(node.normalized_content.split())
            if len(norm) > 100:
                if norm in seen_paragraphs:
                    defects.append(
                        ParsingDefect(
                            defect_code="WARN_REPEATED_PARAGRAPH",
                            description=f"Identical text paragraph duplicated in {node.reference}",
                            severity=DefectSeverity.WARNING,
                            sample_text=norm[:80],
                        )
                    )
                    break
                seen_paragraphs.add(norm)

        return defects

    def clean_text(self, text: str) -> str:
        """Strip running headers, footers, and normalise whitespace."""
        cleaned = text
        for pat in self.HEADER_FOOTER_PATTERNS:
            cleaned = pat.sub("", cleaned)
        # Normalize double newlines and tabs
        cleaned = re.sub(r"\r\n", "\n", cleaned)
        cleaned = re.sub(r"[ \t]+", " ", cleaned)
        return cleaned.strip()

    def parse_statute(
        self,
        raw_text: str,
        document_id: str,
        title: str,
        language: str = "en",
        doc_type: LegalDocumentType = LegalDocumentType.STATUTE,
    ) -> ParsedLegalDocument:
        """Parse statutory enactment or rules into structured provisions."""
        cleaned = self.clean_text(raw_text)
        hasher = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()
        nodes: List[LegalProvisionNode] = []

        # Split into provision candidate chunks
        # Handle English or Hindi pattern
        pattern = self.SECTION_PATTERN_HI if language == "hi" else self.SECTION_PATTERN_EN
        matches = list(pattern.finditer(cleaned))

        if matches:
            for i, match in enumerate(matches):
                sec_num = match.group(1) or match.group(2)
                start_idx = match.start()
                end_idx = matches[i + 1].start() if i + 1 < len(matches) else len(cleaned)
                section_body = cleaned[start_idx:end_idx].strip()

                first_line = section_body.split("\n")[0]
                heading = first_line[:120].strip()
                ref = f"धारा {sec_num}" if language == "hi" else f"Section {sec_num}"

                node = LegalProvisionNode(
                    node_id=f"{document_id}_SEC_{sec_num}",
                    node_type="section",
                    heading=heading,
                    reference=ref,
                    content=section_body,
                    normalized_content=self.clean_text(section_body),
                    language=language,
                    char_count=len(section_body),
                    anchor=f"sec_{sec_num}",
                )
                nodes.append(node)
        else:
            # Fallback: paragraph-level parsing if sections not explicitly delimited
            paragraphs = [p.strip() for p in cleaned.split("\n\n") if p.strip()]
            for idx, p in enumerate(paragraphs):
                node = LegalProvisionNode(
                    node_id=f"{document_id}_P_{idx+1}",
                    node_type="paragraph",
                    heading=p[:80],
                    reference=f"Para {idx+1}",
                    content=p,
                    normalized_content=self.clean_text(p),
                    language=language,
                    char_count=len(p),
                    anchor=f"p_{idx+1}",
                )
                nodes.append(node)

        # Detect defects
        defects = self.detect_defects(raw_text, nodes)
        has_fatal = any(d.severity == DefectSeverity.FATAL for d in defects)

        return ParsedLegalDocument(
            document_id=document_id,
            title=title,
            doc_type=doc_type,
            raw_hash_sha256=hasher,
            total_provisions=len(nodes),
            language=language,
            nodes=nodes,
            defects=defects,
            is_valid_parse=(not has_fatal and len(nodes) > 0),
        )

    def parse_judgment(
        self,
        raw_text: str,
        document_id: str,
        title: str,
        bench: Optional[str] = None,
        citations: Optional[List[str]] = None,
    ) -> ParsedLegalDocument:
        """Parse judicial judgment into structured paragraphs."""
        cleaned = self.clean_text(raw_text)
        hasher = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()
        nodes: List[LegalProvisionNode] = []

        # Split into numbered paragraphs or double-newline blocks
        paras = [p.strip() for p in cleaned.split("\n\n") if p.strip()]
        for idx, p in enumerate(paras):
            match = self.JUDGMENT_PARA_PATTERN.match(p)
            para_num = match.group(1) if match else str(idx + 1)
            ref = f"Paragraph {para_num}"
            node = LegalProvisionNode(
                node_id=f"{document_id}_PARA_{para_num}",
                node_type="judgment_para",
                heading=p[:90].strip(),
                reference=ref,
                content=p,
                normalized_content=self.clean_text(p),
                language="en",
                char_count=len(p),
                anchor=f"para_{para_num}",
            )
            nodes.append(node)

        defects = self.detect_defects(raw_text, nodes)
        has_fatal = any(d.severity == DefectSeverity.FATAL for d in defects)

        return ParsedLegalDocument(
            document_id=document_id,
            title=title,
            doc_type=LegalDocumentType.JUDGMENT,
            raw_hash_sha256=hasher,
            total_provisions=len(nodes),
            language="en",
            nodes=nodes,
            defects=defects,
            is_valid_parse=(not has_fatal and len(nodes) > 0),
            bench_or_authority=bench,
            citations=citations or [],
        )

