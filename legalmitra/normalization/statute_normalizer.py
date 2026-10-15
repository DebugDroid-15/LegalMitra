"""
LegalMitra Statute Normalizer
Parses extracted legal text into structured StatuteDocument and StatuteSection models,
preserving section numbering, headings, subsections, provisos, and explanations.
"""

import re
from typing import List, Optional

from legalmitra.core.enums import LegalReviewStatus
from legalmitra.core.logging import get_logger
from legalmitra.extraction.base import ExtractionResult
from legalmitra.normalization.clean_text import sanitize_legal_text
from legalmitra.schemas.registry import SourceRegistryRecord
from legalmitra.schemas.statute import (
    StatuteClause,
    StatuteDocument,
    StatuteExplanation,
    StatuteIllustration,
    StatuteProviso,
    StatuteSection,
    StatuteSubSection,
)

logger = get_logger("statute_normalizer")


class StatuteNormalizer:
    """
    Normalizes statutory text adhering to Indian legislative drafting conventions.
    """

    # Matches Section header patterns:
    # "Section 61. Admissibility of electronic records"
    # "61. Admissibility of electronic records.—"
    # "Section 437A. Bail to require accused to appear before next appellate Court"
    SECTION_HEADER_PATTERN = re.compile(
        r"(?:^|\n)(?:#+\s*)?(?:Section\s+)?(\d+[A-Z]?)\.\s*([^\n—\.\-]+)?(?:[—\.\-]+|\n|$)",
        re.MULTILINE
    )

    SUBSECTION_PATTERN = re.compile(r"(?:^|\n)\s*\(([0-9]+)\)\s*", re.MULTILINE)
    CLAUSE_PATTERN = re.compile(r"(?:^|\n)\s*\(([a-z]+)\)\s*", re.MULTILINE)
    PROVISO_PATTERN = re.compile(r"(Provided (?:further )?that[^\n]+(?:\n(?!\s*(?:Provided|Explanation|Illustration|\([0-9]+\)|Section|\d+\.))[^\n]+)*)", re.IGNORECASE)
    EXPLANATION_PATTERN = re.compile(r"(Explanation(?:\s*\d+)?\s*[\.—\-][^\n]+(?:\n(?!\s*(?:Provided|Explanation|Illustration|\([0-9]+\)|Section|\d+\.))[^\n]+)*)", re.IGNORECASE)
    ILLUSTRATION_PATTERN = re.compile(r"(Illustration(?:\s*\([a-z]\))?\s*[\.—\-][^\n]+(?:\n(?!\s*(?:Provided|Explanation|Illustration|\([0-9]+\)|Section|\d+\.))[^\n]+)*)", re.IGNORECASE)

    def normalize(self, extraction: ExtractionResult, registry_record: SourceRegistryRecord) -> StatuteDocument:
        raw_text = sanitize_legal_text(extraction.text or extraction.markdown)

        # Parse sections
        sections = self._parse_sections(raw_text, registry_record)

        # Build StatuteDocument
        statute_doc = StatuteDocument(
            source_id=registry_record.document_id,
            act_title=registry_record.title,
            jurisdiction=registry_record.jurisdiction,
            enactment_date=registry_record.document_date,
            effective_date=registry_record.effective_date,
            sections=sections,
            legal_review_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
        )

        logger.info(f"Normalized statute {registry_record.document_id}: parsed {len(sections)} sections.")
        return statute_doc

    def _parse_sections(self, text: str, record: SourceRegistryRecord) -> List[StatuteSection]:
        matches = list(self.SECTION_HEADER_PATTERN.finditer(text))
        if not matches:
            # Fallback: treat whole text as a single section or general provision
            return [
                StatuteSection(
                    section_id=f"{record.document_id}-SEC-FULL",
                    source_id=record.document_id,
                    act_title=record.title,
                    section_number="General",
                    section_title=record.title,
                    full_verbatim_text=text.strip(),
                    subsections=self._extract_subsections(text),
                    provisos=self._extract_provisos(text),
                    explanations=self._extract_explanations(text),
                    illustrations=self._extract_illustrations(text),
                    legal_review_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
                )
            ]

        sections: List[StatuteSection] = []
        for i, match in enumerate(matches):
            sec_num = match.group(1).strip()
            sec_title = (match.group(2) or "").strip() or f"Section {sec_num}"

            start_idx = match.start()
            end_idx = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            sec_body = text[start_idx:end_idx].strip()

            subsections = self._extract_subsections(sec_body)
            provisos = self._extract_provisos(sec_body)
            explanations = self._extract_explanations(sec_body)
            illustrations = self._extract_illustrations(sec_body)

            sec_id = f"{record.document_id}-SEC-{sec_num}"

            section = StatuteSection(
                section_id=sec_id,
                source_id=record.document_id,
                act_title=record.title,
                section_number=sec_num,
                section_title=sec_title,
                full_verbatim_text=sec_body,
                subsections=subsections,
                provisos=provisos,
                explanations=explanations,
                illustrations=illustrations,
                legal_review_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
            )
            sections.append(section)

        return sections

    def _extract_subsections(self, text: str) -> List[StatuteSubSection]:
        matches = list(self.SUBSECTION_PATTERN.finditer(text))
        if not matches:
            return []

        subsections: List[StatuteSubSection] = []
        for i, match in enumerate(matches):
            num = match.group(1).strip()
            start = match.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            body = text[start:end].strip()

            # Check for clauses (a), (b) inside subsection
            clause_matches = list(self.CLAUSE_PATTERN.finditer(body))
            clauses = []
            for j, c_match in enumerate(clause_matches):
                c_num = c_match.group(1).strip()
                c_start = c_match.start()
                c_end = clause_matches[j + 1].start() if j + 1 < len(clause_matches) else len(body)
                clauses.append(StatuteClause(clause_number=f"({c_num})", text=body[c_start:c_end].strip()))

            subsections.append(
                StatuteSubSection(
                    sub_section_number=f"({num})",
                    text=body,
                    clauses=clauses,
                )
            )
        return subsections

    def _extract_provisos(self, text: str) -> List[StatuteProviso]:
        provisos = []
        for idx, match in enumerate(self.PROVISO_PATTERN.finditer(text), start=1):
            p_text = match.group(1).strip()
            if p_text:
                provisos.append(StatuteProviso(proviso_index=idx, text=p_text))
        return provisos

    def _extract_explanations(self, text: str) -> List[StatuteExplanation]:
        explanations = []
        for match in self.EXPLANATION_PATTERN.finditer(text):
            e_text = match.group(1).strip()
            if e_text:
                ident = "Explanation"
                if "Explanation 1" in e_text or "Explanation I" in e_text:
                    ident = "Explanation 1"
                elif "Explanation 2" in e_text or "Explanation II" in e_text:
                    ident = "Explanation 2"
                explanations.append(StatuteExplanation(explanation_identifier=ident, text=e_text))
        return explanations

    def _extract_illustrations(self, text: str) -> List[StatuteIllustration]:
        illustrations = []
        for match in self.ILLUSTRATION_PATTERN.finditer(text):
            i_text = match.group(1).strip()
            if i_text:
                illustrations.append(StatuteIllustration(illustration_identifier="Illustration", text=i_text))
        return illustrations

