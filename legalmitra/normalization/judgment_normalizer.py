"""
LegalMitra Judgment Normalizer
Parses extracted Indian court judgment text into structured JudgmentDocument models,
preserving numbered paragraph structure, bench composition, citations, and ratio decidendi.
"""

import re
from typing import List, Tuple

from legalmitra.core.enums import LegalReviewStatus
from legalmitra.core.logging import get_logger
from legalmitra.extraction.base import ExtractionResult
from legalmitra.normalization.clean_text import extract_paragraphs, sanitize_legal_text
from legalmitra.schemas.judgment import (
    CaseHolding,
    JudgmentCitation,
    JudgmentDocument,
    JudgmentParagraph,
)
from legalmitra.schemas.registry import SourceRegistryRecord

logger = get_logger("judgment_normalizer")


class JudgmentNormalizer:
    """
    Normalizes Indian court judgment text with paragraph fidelity.
    """

    CITATION_PATTERN = re.compile(
        r"(\((?:19|20)\d{2}\)\s+\d+\s+(?:SCC|SCR)\s+\d+|AIR\s+(?:19|20)\d{2}\s+SC\s+\d+|(?:20\d{2})\s+INSC\s+\d+)",
        re.IGNORECASE
    )

    PARA_NUMBER_PATTERN = re.compile(
        r"^(?:\[?(\d+)\]?\.?|\bpara(?:graph)?\s+(\d+)\.?:?)\s*(.*)",
        re.DOTALL | re.IGNORECASE
    )

    def normalize(self, extraction: ExtractionResult, registry_record: SourceRegistryRecord) -> JudgmentDocument:
        raw_text = sanitize_legal_text(extraction.text or extraction.markdown)

        bench_coram = self._extract_coram(raw_text)
        citations = self._extract_citations(raw_text)
        paragraphs = self._extract_paragraphs(raw_text)
        ratio = self._extract_ratio(raw_text)

        doc = JudgmentDocument(
            judgment_id=registry_record.document_id,
            source_id=registry_record.document_id,
            case_title=registry_record.title,
            court=registry_record.court,
            jurisdiction=registry_record.jurisdiction,
            bench_coram=bench_coram or ["Hon'ble Bench"],
            judgment_date=registry_record.document_date,
            citations=citations,
            paragraphs=paragraphs,
            ratio_decidendi=ratio,
            legal_review_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
        )

        logger.info(
            f"Normalized judgment {registry_record.document_id}: "
            f"{len(paragraphs)} paragraphs, {len(citations)} citations."
        )
        return doc

    def _extract_coram(self, text: str) -> List[str]:
        coram_match = re.search(
            r"(?:CORAM|BENCH|BEFORE)\s*:\s*([^\n]+(?:\n(?!\s*(?:JUDGMENT|ORDER|Writ|Civil))[^\n]+)*)",
            text,
            re.IGNORECASE
        )
        if coram_match:
            raw_coram = coram_match.group(1).replace("\n", " ").strip()
            judges = [j.strip() for j in re.split(r"[,;]|(?:\band\b)", raw_coram) if j.strip()]
            return judges
        return []

    def _extract_citations(self, text: str) -> List[JudgmentCitation]:
        found = set()
        citations = []
        for match in self.CITATION_PATTERN.finditer(text):
            cit = match.group(1).strip()
            if cit not in found:
                found.add(cit)
                reporter = "SCC" if "SCC" in cit else ("AIR" if "AIR" in cit else "OTHER")
                citations.append(JudgmentCitation(citation_text=cit, reporter=reporter))
        return citations

    def _extract_paragraphs(self, text: str) -> List[JudgmentParagraph]:
        raw_blocks = extract_paragraphs(text)
        paragraphs: List[JudgmentParagraph] = []

        auto_para_no = 1
        for block in raw_blocks:
            match = self.PARA_NUMBER_PATTERN.match(block)
            if match:
                explicit_num = match.group(1) or match.group(2)
                para_no = int(explicit_num) if explicit_num else auto_para_no
                para_text = match.group(3).strip() if match.group(3) else block
                paragraphs.append(
                    JudgmentParagraph(
                        paragraph_number=para_no,
                        verbatim_text=para_text,
                    )
                )
                auto_para_no = para_no + 1
            else:
                paragraphs.append(
                    JudgmentParagraph(
                        paragraph_number=auto_para_no,
                        verbatim_text=block,
                    )
                )
                auto_para_no += 1

        return paragraphs

    def _extract_ratio(self, text: str) -> str:
        # Search for ratio decidendi or holding markers
        ratio_match = re.search(
            r"(?:HELD|RATIO DECIDENDI|CONCLUSION|DISPOSITION)\s*[:—\-]\s*([^\n]+(?:\n(?!\s*\n)[^\n]+)*)",
            text,
            re.IGNORECASE
        )
        if ratio_match:
            return ratio_match.group(1).strip()
        return "Ratio decidendi to be synthesized and verified by legal counsel."

