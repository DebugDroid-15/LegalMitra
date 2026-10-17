"""
LegalMitra National Corpus Discovery Engine (Phase 19)
Discovers official legal documents, monitors change events across official portals,
computes cryptographic content hashes, detects duplicate candidates, and classifies updates.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from legalmitra.corpus.legal_universe import DocumentFamily, IngestionLifecycleState, LegalAuthorityLevel


class ChangeClassification(str, Enum):
    NEW_DOCUMENT = "new_document"
    EXACT_DUPLICATE = "exact_duplicate"
    UPDATED_METADATA = "updated_metadata"
    CHANGED_SOURCE_FILE = "changed_source_file"
    CHANGED_EXTRACTED_TEXT = "changed_extracted_text"
    NEW_LEGAL_VERSION = "new_legal_version"
    CORRECTED_OCR = "corrected_ocr"
    SUPERSEDED_DOCUMENT = "superseded_document"
    UNRESOLVED_CHANGE = "unresolved_change"


@dataclass
class DiscoveryCandidate:
    candidate_id: str
    source_url: str
    official_title: str
    document_family: DocumentFamily
    authority_level: LegalAuthorityLevel
    jurisdiction: str
    issuing_authority: str
    discovered_at: str
    raw_content_bytes: Optional[bytes] = None
    checksum_sha256: Optional[str] = None
    http_etag: Optional[str] = None
    http_last_modified: Optional[str] = None
    lifecycle_state: IngestionLifecycleState = IngestionLifecycleState.DISCOVERED
    metadata: Dict[str, Any] = field(default_factory=dict)

    def compute_hash(self) -> str:
        if self.raw_content_bytes:
            self.checksum_sha256 = hashlib.sha256(self.raw_content_bytes).hexdigest()
        return self.checksum_sha256 or ""

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d.pop("raw_content_bytes", None)
        d["document_family"] = self.document_family.value
        d["authority_level"] = self.authority_level.value
        d["lifecycle_state"] = self.lifecycle_state.value
        return d


@dataclass
class DocumentDiffRecord:
    diff_id: str
    document_id: str
    previous_hash: Optional[str]
    new_hash: str
    classification: ChangeClassification
    detected_at: str
    change_summary: str
    source_instrument_ref: Optional[str] = None
    requires_human_review: bool = False

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["classification"] = self.classification.value
        return d


class NationalSourceDiscoveryEngine:
    """
    Automated source discovery and change detection engine.
    Scans authoritative endpoints, computes SHA-256 hashes, and triages changes.
    """

    def __init__(self, known_inventory_path: Optional[Path] = None):
        self._candidates: Dict[str, DiscoveryCandidate] = {}
        self._diff_history: List[DocumentDiffRecord] = []
        self._known_hashes: Dict[str, str] = {}  # sha256 -> document_id
        self._known_docs: Dict[str, str] = {}    # document_id -> sha256

        if known_inventory_path and known_inventory_path.exists():
            self._load_known_inventory(known_inventory_path)

    def _load_known_inventory(self, path: Path) -> None:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for item in data:
                doc_id = item.get("record_id")
                sha = item.get("checksum_sha256")
                if doc_id:
                    if sha:
                        self._known_hashes[sha] = doc_id
                        self._known_docs[doc_id] = sha
        except Exception:
            pass

    def register_candidate(self, candidate: DiscoveryCandidate) -> Tuple[DiscoveryCandidate, ChangeClassification]:
        """
        Registers a newly discovered legal document and determines change classification.
        """
        c_hash = candidate.compute_hash()
        doc_id = candidate.candidate_id

        # Check exact duplicate by hash
        if c_hash and c_hash in self._known_hashes:
            existing_doc_id = self._known_hashes[c_hash]
            candidate.lifecycle_state = IngestionLifecycleState.LOCATED
            classification = ChangeClassification.EXACT_DUPLICATE
            diff = DocumentDiffRecord(
                diff_id=f"DIFF-{len(self._diff_history)+1:04d}",
                document_id=doc_id,
                previous_hash=c_hash,
                new_hash=c_hash,
                classification=classification,
                detected_at=datetime.now(timezone.utc).isoformat(),
                change_summary=f"Exact duplicate of already known document {existing_doc_id}"
            )
            self._diff_history.append(diff)
            self._candidates[doc_id] = candidate
            return candidate, classification

        # Check updated version of known document
        if doc_id in self._known_docs:
            prev_hash = self._known_docs[doc_id]
            if prev_hash != c_hash:
                classification = ChangeClassification.CHANGED_SOURCE_FILE
                candidate.lifecycle_state = IngestionLifecycleState.AWAITING_ACQUISITION
                diff = DocumentDiffRecord(
                    diff_id=f"DIFF-{len(self._diff_history)+1:04d}",
                    document_id=doc_id,
                    previous_hash=prev_hash,
                    new_hash=c_hash,
                    classification=classification,
                    detected_at=datetime.now(timezone.utc).isoformat(),
                    change_summary=f"Content updated for {doc_id}; SHA-256 changed from {prev_hash[:8]} to {c_hash[:8]}",
                    requires_human_review=True
                )
                self._diff_history.append(diff)
                self._known_docs[doc_id] = c_hash
                if c_hash:
                    self._known_hashes[c_hash] = doc_id
                self._candidates[doc_id] = candidate
                return candidate, classification

        # Brand new document
        classification = ChangeClassification.NEW_DOCUMENT
        candidate.lifecycle_state = IngestionLifecycleState.LOCATED
        diff = DocumentDiffRecord(
            diff_id=f"DIFF-{len(self._diff_history)+1:04d}",
            document_id=doc_id,
            previous_hash=None,
            new_hash=c_hash or "PENDING_DOWNLOAD",
            classification=classification,
            detected_at=datetime.now(timezone.utc).isoformat(),
            change_summary=f"Discovered new authentic instrument: {candidate.official_title}"
        )
        self._diff_history.append(diff)
        if c_hash:
            self._known_hashes[c_hash] = doc_id
            self._known_docs[doc_id] = c_hash
        self._candidates[doc_id] = candidate
        return candidate, classification

    def get_candidate(self, candidate_id: str) -> Optional[DiscoveryCandidate]:
        return self._candidates.get(candidate_id)

    def get_diff_history(self) -> List[DocumentDiffRecord]:
        return list(self._diff_history)

    def export_candidates_manifest(self, output_path: Path) -> None:
        data = [c.to_dict() for c in self._candidates.values()]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

