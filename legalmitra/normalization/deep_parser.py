"""
Phase 86: Deep Parsing & Statutory Structure Modeling Pipeline
Parses unstructured raw statutes, judgments, and gazettes ingested from multi-source connectors
into fully schema-compliant `StatuteDocument` and `JudgmentDocument` artifacts with
provisos, explanations, paragraph numbering, and citation extraction.
"""

from __future__ import annotations

import json
import logging
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from legalmitra.core.enums import CourtType, Jurisdiction, LegalReviewStatus, SourceType
from legalmitra.ingestion.registry import SourceRegistryManager
from legalmitra.normalization.clean_text import sanitize_legal_text
from legalmitra.schemas.judgment import JudgmentCitation, JudgmentDocument, JudgmentParagraph
from legalmitra.schemas.statute import (
    StatuteClause,
    StatuteDocument,
    StatuteExplanation,
    StatuteProviso,
    StatuteSection,
    StatuteSubClause,
    StatuteSubSection,
)

logger = logging.getLogger("deep_parsing_pipeline")


class DeepLegalParser:
    """
    Parses unstructured text of acts, judgments, and gazettes into structured models.
    """

    def parse_statute_sections(
        self,
        source_id: str,
        act_title: str,
        raw_text: str
    ) -> List[StatuteSection]:
        """Extracts structured sections, provisos, and explanations from raw statutory text."""
        sections: List[StatuteSection] = []
        clean_text = sanitize_legal_text(raw_text)

        # Regex pattern matching '### Sec 34 - ...' or 'Section 34.' or '34. Title'
        sec_pattern = re.compile(
            r'(?:###\s*(?:Section|Sec)\s*([0-9A-Z]+)\s*[-:]?\s*([^\n]+)|(?:Section|Sec)\s*([0-9A-Z]+)[.:]\s*([^\n]+))',
            re.IGNORECASE
        )

        matches = list(sec_pattern.finditer(clean_text))
        if not matches:
            # Fallback: create a general section for the document
            sec = StatuteSection(
                section_id=f"{source_id}-SEC-GEN",
                source_id=source_id,
                act_title=act_title,
                section_number="1",
                section_title=f"General Provisions of {act_title}",
                full_verbatim_text=clean_text[:4000]
            )
            return [sec]

        for i, match in enumerate(matches):
            sec_num = (match.group(1) or match.group(3) or "").strip()
            sec_title = (match.group(2) or match.group(4) or "").strip()
            start_pos = match.end()
            end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(clean_text)
            body = clean_text[start_pos:end_pos].strip()

            # Parse sub-elements: provisos & explanations
            provisos: List[StatuteProviso] = []
            explanations: List[StatuteExplanation] = []

            # Proviso match: "Provided that..."
            for prov_match in re.finditer(r'Provided(?:\s+further)?\s+that\s+([^.\n]+(?:\.[^.\n]+)*)', body, re.IGNORECASE):
                provisos.append(StatuteProviso(
                    proviso_index=len(provisos) + 1,
                    text=f"Provided that {prov_match.group(1).strip()}"
                ))

            # Explanation match: "Explanation 1. — ..." or "Explanation.—..."
            for exp_match in re.finditer(r'Explanation(?:\s*([0-9]+))?[.—\-]+\s*([^.\n]+(?:\.[^.\n]+)*)', body, re.IGNORECASE):
                exp_num = exp_match.group(1) or str(len(explanations) + 1)
                explanations.append(StatuteExplanation(
                    explanation_identifier=f"Explanation {exp_num}",
                    text=exp_match.group(2).strip()
                ))

            sec = StatuteSection(
                section_id=f"{source_id}-SEC-{sec_num}",
                source_id=source_id,
                act_title=act_title,
                section_number=sec_num,
                section_title=sec_title,
                full_verbatim_text=body if body else f"{sec_title} under {act_title}.",
                provisos=provisos,
                explanations=explanations
            )
            sections.append(sec)

        return sections

    def parse_judgment_document(
        self,
        doc_id: str,
        title: str,
        raw_text: str,
        court: CourtType,
        doc_date_str: str,
        source_url: str
    ) -> JudgmentDocument:
        """Parses case law into JudgmentDocument with numbered paragraphs and bench coram."""
        clean_text = sanitize_legal_text(raw_text)

        # 1. Parse bench coram: 'CORAM: A and B, JJ.'
        bench: List[str] = []
        coram_match = re.search(r'CORAM\s*:\s*([^\n]+)', clean_text, re.IGNORECASE)
        if coram_match:
            judges = [j.strip() for j in re.split(r'[,&]|\band\b', coram_match.group(1)) if j.strip()]
            for j in judges:
                cleaned_j = re.sub(r'JJ\.?|J\.?', '', j).strip()
                if len(cleaned_j) >= 3 and cleaned_j not in bench:
                    bench.append(cleaned_j)
        if not bench:
            bench = ["Hon'ble Bench of Supreme Court of India"]

        # 2. Extract citations: '(2014) 8 SCC 273', '1992 Supp (1) SCC 335'
        citations: List[JudgmentCitation] = []
        cit_pattern = re.compile(r'(\(?[0-9]{4}\)?(?:\s+Supp)?(?:\s*\([0-9]+\))?\s+[0-9]*\s*(?:SCC|SCR|AIR|INSC)\s+[0-9]+)', re.IGNORECASE)
        for cit in set(cit_pattern.findall(clean_text)):
            reporter = "SCC" if "SCC" in cit else "SCR" if "SCR" in cit else "AIR" if "AIR" in cit else "INSC"
            citations.append(JudgmentCitation(citation_text=cit.strip(), reporter=reporter))

        # 3. Parse numbered paragraphs or split by sections/ratio
        paragraphs: List[JudgmentParagraph] = []
        raw_paras = [p.strip() for p in clean_text.split("\n\n") if len(p.strip()) > 20]
        for idx, p in enumerate(raw_paras, start=1):
            paragraphs.append(JudgmentParagraph(
                paragraph_number=idx,
                verbatim_text=p
            ))

        # 4. Parse date
        try:
            j_date = date.fromisoformat(doc_date_str)
        except Exception:
            j_date = date(2024, 1, 1)

        return JudgmentDocument(
            judgment_id=doc_id,
            source_id=doc_id,
            case_title=title,
            court=court,
            jurisdiction=Jurisdiction.INDIA_CENTRAL,
            bench_coram=bench,
            judgment_date=j_date,
            paragraphs=paragraphs,
            citations=citations
        )


class DeepParsingPipeline:
    """
    Orchestrates parsing of raw documents from `data/01_raw/` into `data/02_normalized/`.
    """

    def __init__(
        self,
        raw_dir: Union[str, Path] = "data/01_raw",
        normalized_dir: Union[str, Path] = "data/02_normalized",
        registry_file: Union[str, Path] = "registry/source_registry.jsonl"
    ):
        self.raw_dir = Path(raw_dir)
        self.normalized_dir = Path(normalized_dir)
        self.normalized_dir.mkdir(parents=True, exist_ok=True)
        self.registry_manager = SourceRegistryManager(registry_file)
        self.parser = DeepLegalParser()

    def run(self) -> Dict[str, Any]:
        records = self.registry_manager.list_all()
        normalized_count = 0
        skipped_count = 0
        errors = []

        for record in records:
            norm_path = self.normalized_dir / f"{record.document_id}.json"
            if norm_path.exists():
                skipped_count += 1
                continue

            raw_path = Path(record.raw_file_path)
            if not raw_path.exists():
                # check inside raw_dir
                raw_path = self.raw_dir / f"{record.document_id}{record.file_format}"
                if not raw_path.exists():
                    logger.warning(f"Raw file missing for {record.document_id}")
                    continue

            try:
                raw_text = raw_path.read_text(encoding="utf-8")
            except Exception as e:
                logger.error(f"Cannot read raw file {raw_path}: {e}")
                errors.append(f"{record.document_id}: {e}")
                continue

            try:
                # 1. Statutes & Gazettes
                if record.source_type in [SourceType.STATUTE, SourceType.GAZETTE, SourceType.OTHER]:
                    sections = self.parser.parse_statute_sections(
                        source_id=record.document_id,
                        act_title=record.title,
                        raw_text=raw_text
                    )
                    try:
                        enact_date = date.fromisoformat(record.document_date)
                    except Exception:
                        enact_date = date(2024, 1, 1)

                    eff_date = None
                    if record.effective_date:
                        try:
                            eff_date = date.fromisoformat(record.effective_date)
                        except Exception:
                            pass

                    stat_doc = StatuteDocument(
                        source_id=record.document_id,
                        act_title=record.title,
                        act_number=record.document_id,
                        jurisdiction=Jurisdiction.INDIA_CENTRAL,
                        enactment_date=enact_date,
                        effective_date=eff_date,
                        preamble=f"Authentic statutory enactments and notifications under {record.title}",
                        sections=sections
                    )
                    norm_path.write_text(stat_doc.model_dump_json(indent=2), encoding="utf-8")
                    normalized_count += 1

                # 2. Judgments
                elif record.source_type == SourceType.JUDGMENT:
                    judg_doc = self.parser.parse_judgment_document(
                        doc_id=record.document_id,
                        title=record.title,
                        raw_text=raw_text,
                        court=record.court,
                        doc_date_str=record.document_date,
                        source_url=record.source_url
                    )
                    norm_path.write_text(judg_doc.model_dump_json(indent=2), encoding="utf-8")
                    normalized_count += 1

            except Exception as e:
                logger.error(f"Failed to normalize {record.document_id}: {e}")
                errors.append(f"{record.document_id}: {e}")

        return {
            "total_records": len(records),
            "normalized_count": normalized_count,
            "skipped_existing": skipped_count,
            "errors": errors
        }
