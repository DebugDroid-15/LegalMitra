"""LegalMitra Judicial Knowledge Infrastructure — Judicial Corpus Indexer.

Manages acquired judicial documents, structural metadata, cryptographic hashes,
paragraph-level anchors, OCR quality metrics, and granular eligibility gates
(retrieval eligibility vs training eligibility).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set


@dataclass
class ParagraphAnchor:
    paragraph_number: int
    text_snippet: str
    token_count: int
    page_number: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "paragraph_number": self.paragraph_number,
            "text_snippet": self.text_snippet,
            "token_count": self.token_count,
            "page_number": self.page_number,
        }


@dataclass
class IndexedJudicialDocument:
    document_id: str
    canonical_case_id: str
    case_title: str
    source_id: str
    court_id: str
    document_type: str
    decision_date: str
    decision_year: int
    sha256_hash: str
    source_url: str
    language: str
    ocr_quality_score: float
    is_authenticity_verified: bool
    paragraph_anchors: List[ParagraphAnchor] = field(default_factory=list)
    cited_statutes: List[str] = field(default_factory=list)
    citation_aliases: List[str] = field(default_factory=list)
    is_retrieval_eligible: bool = True
    is_training_eligible: bool = False  # Strict pretraining gate
    quarantine_reason: Optional[str] = None
    historical_era: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_id": self.document_id,
            "canonical_case_id": self.canonical_case_id,
            "case_title": self.case_title,
            "source_id": self.source_id,
            "court_id": self.court_id,
            "document_type": self.document_type,
            "decision_date": self.decision_date,
            "decision_year": self.decision_year,
            "sha256_hash": self.sha256_hash,
            "source_url": self.source_url,
            "language": self.language,
            "ocr_quality_score": self.ocr_quality_score,
            "is_authenticity_verified": self.is_authenticity_verified,
            "paragraph_count": len(self.paragraph_anchors),
            "paragraph_anchors": [p.to_dict() for p in self.paragraph_anchors],
            "cited_statutes": self.cited_statutes,
            "citation_aliases": self.citation_aliases,
            "is_retrieval_eligible": self.is_retrieval_eligible,
            "is_training_eligible": self.is_training_eligible,
            "quarantine_reason": self.quarantine_reason,
            "historical_era": self.historical_era,
        }


class JudicialCorpusIndexer:
    """Manages the index of primary-source judicial texts and computes corpus metrics."""

    def __init__(self) -> None:
        self._documents: Dict[str, IndexedJudicialDocument] = {}

    def index_document(self, doc: IndexedJudicialDocument) -> None:
        self._documents[doc.document_id] = doc

    def get_document(self, doc_id: str) -> Optional[IndexedJudicialDocument]:
        return self._documents.get(doc_id)

    def list_all_documents(self) -> List[IndexedJudicialDocument]:
        return list(self._documents.values())

    def get_documents_by_court(self, court_id: str) -> List[IndexedJudicialDocument]:
        return [d for d in self._documents.values() if d.court_id == court_id]

    def compute_baseline_metrics(self) -> Dict[str, Any]:
        """Compute exhaustive Workstream C audit metrics across the judicial corpus."""
        total_docs = len(self._documents)
        unique_cases = len(set(d.canonical_case_id for d in self._documents.values()))
        auth_verified = sum(1 for d in self._documents.values() if d.is_authenticity_verified)
        with_hashes = sum(1 for d in self._documents.values() if d.sha256_hash and len(d.sha256_hash) == 64)
        with_anchors = sum(1 for d in self._documents.values() if len(d.paragraph_anchors) > 0)
        with_citations = sum(1 for d in self._documents.values() if len(d.citation_aliases) > 0)
        with_statutes = sum(1 for d in self._documents.values() if len(d.cited_statutes) > 0)
        historical_docs = sum(1 for d in self._documents.values() if d.decision_year < 1950)
        vernacular_docs = sum(1 for d in self._documents.values() if d.language != "en")
        retrieval_eligible = sum(1 for d in self._documents.values() if d.is_retrieval_eligible)
        training_eligible = sum(1 for d in self._documents.values() if d.is_training_eligible)
        quarantined = sum(1 for d in self._documents.values() if d.quarantine_reason is not None)

        # Breakdowns by Court
        court_breakdown: Dict[str, int] = {}
        for d in self._documents.values():
            court_breakdown[d.court_id] = court_breakdown.get(d.court_id, 0) + 1

        # Breakdowns by Language
        lang_breakdown: Dict[str, int] = {}
        for d in self._documents.values():
            lang_breakdown[d.language] = lang_breakdown.get(d.language, 0) + 1

        return {
            "total_acquired_documents": total_docs,
            "unique_case_identities": unique_cases,
            "authenticity_verified_documents": auth_verified,
            "documents_with_source_hashes": with_hashes,
            "documents_with_paragraph_anchors": with_anchors,
            "documents_with_verified_citations": with_citations,
            "documents_linked_to_statutes": with_statutes,
            "historical_pre_1950_documents": historical_docs,
            "regional_language_documents": vernacular_docs,
            "retrieval_eligible_documents": retrieval_eligible,
            "training_eligible_documents": training_eligible,  # Must be 0 under strict pretraining NO-GO
            "quarantined_documents": quarantined,
            "court_distribution": court_breakdown,
            "language_distribution": lang_breakdown,
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "baseline_metrics": self.compute_baseline_metrics(),
            "documents": {did: d.to_dict() for did, d in self._documents.items()},
        }
