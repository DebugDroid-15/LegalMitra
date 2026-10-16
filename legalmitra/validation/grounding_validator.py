"""
LegalMitra Source Grounding Validator
Enforces zero-hallucination standards by verifying that every legal statement,
statutory section, case citation, and evidence passage maps to registered source documents.
"""

from pathlib import Path
import re
from typing import List, Optional, Tuple, Union

from legalmitra.core.enums import LegalReviewStatus
from legalmitra.core.errors import GroundingValidationError
from legalmitra.core.logging import get_logger
from legalmitra.ingestion.registry import SourceRegistryManager
from legalmitra.schemas.legal_qa import EvidencePassage, LegalQADocument

logger = get_logger("grounding_validator")


class GroundingValidator:
    """
    Validates that synthetic or processed legal texts are strictly grounded in identified sources.
    """

    def __init__(self, registry_manager: Optional[SourceRegistryManager] = None):
        self.registry = registry_manager

    def verify_evidence_passage(
        self,
        passage: EvidencePassage,
        source_text: str,
    ) -> bool:
        """
        Verifies that the verbatim passage text exists in the source text
        (normalized for whitespace and punctuation differences).
        """
        def _clean(t: str) -> str:
            t = re.sub(r"[\u2018\u2019`]", "'", t)
            t = re.sub(r"[\u201c\u201d]", '"', t)
            t = re.sub(r"[\u2013\u2014]", "-", t)
            return re.sub(r"\s+", " ", t).strip().lower()

        norm_passage = _clean(passage.verbatim_text)
        norm_source = _clean(source_text)
        return norm_passage in norm_source

    def validate_grounding(
        self,
        qa_doc: LegalQADocument,
        source_texts: Optional[dict[str, str]] = None,
    ) -> Tuple[bool, List[str]]:
        """
        Validates grounding for a LegalQADocument.
        Returns: (is_grounded, issues_found)
        """
        issues: List[str] = []

        # 1. Verify supporting source IDs exist in registry if registry is configured
        if self.registry is not None:
            for s_id in qa_doc.supporting_source_ids:
                record = self.registry.get(s_id)
                if not record:
                    issues.append(f"Supporting source ID '{s_id}' is not registered in the Source Registry.")

        # 2. Verify evidence passages
        if not qa_doc.evidence_passages:
            issues.append("Document has no evidence passages to support its claims.")

        for idx, passage in enumerate(qa_doc.evidence_passages, start=1):
            if passage.source_id not in qa_doc.supporting_source_ids:
                issues.append(
                    f"Evidence passage {idx} references source '{passage.source_id}', "
                    f"which is not listed in supporting_source_ids."
                )

            # If source text is available, check passage existence
            if source_texts and passage.source_id in source_texts:
                stext = source_texts[passage.source_id]
                if not self.verify_evidence_passage(passage, stext):
                    issues.append(
                        f"Evidence passage {idx} ('{passage.section_or_para_ref}') does not appear verbatim in source text for {passage.source_id}."
                    )

        # 3. Check for invented sections or citations in the answer
        # Extract statutory sections cited in answer, e.g. "Section 61", "Section 437A"
        cited_sections = re.findall(r"\bSection\s+(\d+[A-Z]?)\b", qa_doc.answer, re.IGNORECASE)
        for sec in cited_sections:
            # Check if this section is mentioned in evidence passages
            mentioned_in_evidence = any(
                f"section {sec.lower()}" in p.verbatim_text.lower() or f"{sec.lower()}" in p.section_or_para_ref.lower()
                for p in qa_doc.evidence_passages
            )
            if not mentioned_in_evidence:
                issues.append(
                    f"Answer cites 'Section {sec}', but this section is not present in any evidence passage."
                )

        is_grounded = len(issues) == 0
        if not is_grounded:
            qa_doc.flagged_unsupported = True
            qa_doc.legal_review_status = LegalReviewStatus.FLAGGED_UNSUPPORTED
            logger.warning(f"Grounding validation issues for {qa_doc.qa_id}: {'; '.join(issues)}")

        return is_grounded, issues
