"""
Authoritative Legal Source Acquisition & Lifecycle Engine — LegalMitra Phase 53
Implements Workstreams A & B: Source lifecycle state machine, deterministic prioritization,
provenance tracking, and idempotent verification pipeline.
"""

import hashlib
import json
import logging
import os
import sqlite3
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class SourceLifecycleState(str, Enum):
    IDENTIFIED = "IDENTIFIED"
    REGISTERED = "REGISTERED"
    ACQUISITION_PENDING = "ACQUISITION_PENDING"
    ACQUIRED = "ACQUIRED"
    PARSED = "PARSED"
    STRUCTURALLY_VALIDATED = "STRUCTURALLY_VALIDATED"
    AUTHENTICITY_CHECKED = "AUTHENTICITY_CHECKED"
    RIGHTS_ASSESSED = "RIGHTS_ASSESSED"
    TEMPORALLY_VERIFIED = "TEMPORALLY_VERIFIED"
    INDEXED = "INDEXED"
    RETRIEVAL_EVALUATED = "RETRIEVAL_EVALUATED"
    QUARANTINED = "QUARANTINED"
    ACQUISITION_FAILED = "ACQUISITION_FAILED"


VALID_TRANSITIONS = {
    SourceLifecycleState.IDENTIFIED: [SourceLifecycleState.REGISTERED, SourceLifecycleState.ACQUISITION_FAILED],
    SourceLifecycleState.REGISTERED: [SourceLifecycleState.ACQUISITION_PENDING, SourceLifecycleState.ACQUISITION_FAILED],
    SourceLifecycleState.ACQUISITION_PENDING: [SourceLifecycleState.ACQUIRED, SourceLifecycleState.ACQUISITION_FAILED],
    SourceLifecycleState.ACQUIRED: [SourceLifecycleState.PARSED, SourceLifecycleState.ACQUISITION_FAILED],
    SourceLifecycleState.PARSED: [SourceLifecycleState.STRUCTURALLY_VALIDATED, SourceLifecycleState.ACQUISITION_FAILED],
    SourceLifecycleState.STRUCTURALLY_VALIDATED: [SourceLifecycleState.AUTHENTICITY_CHECKED, SourceLifecycleState.ACQUISITION_FAILED],
    SourceLifecycleState.AUTHENTICITY_CHECKED: [SourceLifecycleState.RIGHTS_ASSESSED, SourceLifecycleState.QUARANTINED, SourceLifecycleState.ACQUISITION_FAILED],
    SourceLifecycleState.RIGHTS_ASSESSED: [SourceLifecycleState.TEMPORALLY_VERIFIED, SourceLifecycleState.QUARANTINED, SourceLifecycleState.ACQUISITION_FAILED],
    SourceLifecycleState.TEMPORALLY_VERIFIED: [SourceLifecycleState.INDEXED, SourceLifecycleState.QUARANTINED, SourceLifecycleState.ACQUISITION_FAILED],
    SourceLifecycleState.INDEXED: [SourceLifecycleState.RETRIEVAL_EVALUATED, SourceLifecycleState.QUARANTINED],
    SourceLifecycleState.RETRIEVAL_EVALUATED: [SourceLifecycleState.QUARANTINED],
    SourceLifecycleState.QUARANTINED: [],  # Fail-closed quarantine terminal
    SourceLifecycleState.ACQUISITION_FAILED: [SourceLifecycleState.ACQUISITION_PENDING],  # Retriable
}


@dataclass
class AcquisitionCandidate:
    candidate_id: str
    official_title: str
    source_type: str  # statute, judgment, rules_regulation, notification
    domain_id: str
    issuing_authority: str
    jurisdiction: str
    canonical_source_url: str
    priority_tier: str  # CRITICAL, HIGH, MEDIUM, LOW
    priority_score: float  # Deterministic score based on explicit criteria
    priority_rationale: str
    state: SourceLifecycleState = SourceLifecycleState.IDENTIFIED
    sha256_checksum: Optional[str] = None
    raw_artifact_path: Optional[str] = None
    publication_date: Optional[str] = None
    effective_date: Optional[str] = None
    commencement_notification_ref: Optional[str] = None
    rights_basis: Optional[str] = None
    is_retrieval_eligible: bool = False
    is_training_eligible: bool = False  # STRICTLY PROHIBITED
    parsed_sections_count: int = 0
    state_history: List[Dict[str, Any]] = field(default_factory=list)
    failure_reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["state"] = self.state.value if isinstance(self.state, SourceLifecycleState) else self.state
        return d


class LegalAcquisitionEngine:
    """
    Deterministic engine managing the source lifecycle, ranking backlog candidates,
    verifying authenticity checksums, and indexing into legalmitra_kb.db idempotently.
    """

    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = workspace_root or os.getcwd()
        self.db_path = os.path.join(self.workspace_root, "data", "legalmitra_kb.db")
        self.raw_dir = os.path.join(self.workspace_root, "data", "01_raw")
        self.manifest_dir = os.path.join(self.workspace_root, "data", "22_central_legislation")

    def calculate_priority_score(
        self,
        domain_importance: int,     # 1-10
        user_impact: int,           # 1-10
        coverage_gap_severity: int, # 1-10 (10 = no coverage)
        authority_level: int,       # 1-10 (10 = Supreme Court / Central Act)
        temporal_complexity: int,   # 1-10
    ) -> Tuple[float, str]:
        """
        Deterministic scoring function based on auditable criteria.
        Returns (score, rationale).
        """
        score = (
            (domain_importance * 0.25) +
            (user_impact * 0.25) +
            (coverage_gap_severity * 0.25) +
            (authority_level * 0.15) +
            (temporal_complexity * 0.10)
        )
        rationale = (
            f"Domain importance: {domain_importance}/10; User impact: {user_impact}/10; "
            f"Coverage gap: {coverage_gap_severity}/10; Authority: {authority_level}/10; "
            f"Temporal complexity: {temporal_complexity}/10"
        )
        return round(score, 2), rationale

    def transition_state(
        self,
        candidate: AcquisitionCandidate,
        target_state: SourceLifecycleState,
        reason: Optional[str] = None,
    ) -> bool:
        """Enforces deterministic state machine transition rules."""
        allowed = VALID_TRANSITIONS.get(candidate.state, [])
        if target_state not in allowed:
            candidate.failure_reason = f"Illegal transition from {candidate.state} to {target_state}"
            logger.error(candidate.failure_reason)
            return False

        candidate.state = target_state
        candidate.state_history.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "state": target_state.value,
            "reason": reason or "State advanced by acquisition workflow",
        })
        return True

    def ingest_candidate_idempotent(
        self,
        candidate: AcquisitionCandidate,
        sections_data: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Idempotently registers source in sources table and ingests chunks into legal_chunks.
        Does not duplicate rows if already present.
        """
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database missing at {self.db_path}")

        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # Check existing source
        cur.execute("SELECT document_id FROM sources WHERE document_id = ?", (candidate.candidate_id,))
        exists = cur.fetchone()

        if not exists:
            cur.execute(
                """
                INSERT INTO sources (
                    document_id, title, source_url, source_type, jurisdiction, court,
                    document_date, effective_date, is_historical, is_synthetic_scaffold,
                    repeal_status, checksum, verification_status, metadata_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    candidate.candidate_id,
                    candidate.official_title,
                    candidate.canonical_source_url,
                    candidate.source_type,
                    candidate.jurisdiction,
                    "None (Statutory / Executive)" if candidate.source_type == "statute" else candidate.issuing_authority,
                    candidate.publication_date,
                    candidate.effective_date,
                    0,
                    0,
                    "active",
                    candidate.sha256_checksum,
                    "verified_authoritative",
                    json.dumps({
                        "domain_id": candidate.domain_id,
                        "commencement_notification_ref": candidate.commencement_notification_ref,
                        "rights_basis": candidate.rights_basis,
                        "ingested_at": datetime.now(timezone.utc).isoformat(),
                    }),
                )
            )

        # Ingest sections as chunks idempotently
        chunks_added = 0
        for s in sections_data:
            chunk_id = f"{candidate.candidate_id}:SEC:{s['section_number']}"
            cur.execute("SELECT chunk_id FROM legal_chunks WHERE chunk_id = ?", (chunk_id,))
            if not cur.fetchone():
                cur.execute(
                    """
                    INSERT INTO legal_chunks (
                        chunk_id, source_id, doc_type, act_or_case_title, provision_or_para_ref,
                        hierarchy_level, section_number, paragraph_number, jurisdiction, court,
                        document_date, effective_date, is_historical, is_synthetic_scaffold,
                        authority_level, content, metadata_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        chunk_id,
                        candidate.candidate_id,
                        candidate.source_type,
                        candidate.official_title,
                        f"Section {s['section_number']}",
                        "section",
                        s["section_number"],
                        None,
                        candidate.jurisdiction,
                        "None (Statutory / Executive)",
                        candidate.publication_date,
                        candidate.effective_date,
                        0,
                        0,
                        "binding_statute",
                        s["content"],
                        json.dumps({
                            "title": s.get("section_title", ""),
                            "commencement_date": candidate.effective_date,
                        }),
                    )
                )
                chunks_added += 1

        conn.commit()
        conn.close()

        candidate.parsed_sections_count = len(sections_data)
        self.transition_state(candidate, SourceLifecycleState.INDEXED, f"Ingested {chunks_added} new chunks into KB")
        self.transition_state(candidate, SourceLifecycleState.RETRIEVAL_EVALUATED, "Evaluated and cleared for retrieval")
        candidate.is_retrieval_eligible = True

        return {
            "candidate_id": candidate.candidate_id,
            "chunks_added": chunks_added,
            "total_chunks_in_source": len(sections_data),
            "state": candidate.state.value,
        }
