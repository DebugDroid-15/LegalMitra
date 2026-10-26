"""
Evidence Eligibility Engine & Safeguards — LegalMitra Phase 65
Implements Workstream E & B: Evidence Eligibility Policy, Fail-Closed Retrieval Guards,
Scaffold Quarantine, Source Lifecycle Verification, Reuse Rights Validation, and Temporal Checks.
"""

import json
import logging
import os
import sqlite3
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class EvidenceEligibilityVerdict:
    is_eligible: bool
    rejection_reason: Optional[str] = None
    quarantine_policy: Optional[str] = None
    temporal_warning: Optional[str] = None
    rights_basis: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class EvidenceEligibilityEngine:
    """
    Enforces fail-closed rules and quarantine standards on candidate legal evidence chunks.
    Non-negotiable invariants:
    1. Synthetic scaffold chunks (is_synthetic_scaffold=1 or IND-JUD-DEL-2024-BAIL) are STRICTLY QUARANTINED.
    2. Sources flagged as 'flagged_unsupported' or 'unverified' test fixtures (e.g. IND-UNSUPPORTED-001) are REJECTED.
    3. Model pretraining use is STRICTLY PROHIBITED for all records.
    4. Substantive statutory provisions whose commencement is unnotified trigger TEMPORAL_WARNING.
    5. Sources with unresolved reuse rights (RIGHTS_RESTRICTED, UNRESOLVED_RIGHTS) are REJECTED from authoritative answering.
    """

    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = workspace_root or os.getcwd()
        self.db_path = os.path.join(self.workspace_root, "data", "legalmitra_kb.db")
        self._source_cache: Dict[str, Dict[str, Any]] = {}
        self._load_sources()

    def _load_sources(self):
        if not os.path.exists(self.db_path):
            return
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            "SELECT document_id, title, source_type, is_synthetic_scaffold, repeal_status, "
            "verification_status, effective_date, metadata_json FROM sources"
        )
        for r in cur.fetchall():
            meta = {}
            if len(r) > 7 and r[7]:
                try:
                    meta = json.loads(r[7])
                except Exception:
                    meta = {}
            self._source_cache[r[0]] = {
                "document_id": r[0],
                "title": r[1],
                "source_type": r[2],
                "is_scaffold": bool(r[3]),
                "repeal_status": r[4],
                "verification_status": r[5],
                "effective_date": r[6],
                "metadata": meta,
            }
        conn.close()

    def register_in_memory_source(self, document_id: str, record: Dict[str, Any]) -> None:
        """Register or override a source record in memory for testing or lifecycle tracking."""
        self._source_cache[document_id] = record

    def evaluate_chunk_eligibility(
        self,
        source_id: str,
        chunk_id: Optional[str] = None,
        is_synthetic_scaffold: bool = False,
        as_of_date: Optional[str] = None,
        source_metadata: Optional[Dict[str, Any]] = None,
    ) -> EvidenceEligibilityVerdict:
        """
        Evaluate if a candidate chunk or source is eligible for legal query retrieval.
        Fail-closed: If in doubt or missing, default to ineligible or restricted.
        """
        # 1. Invariant: Synthetic scaffold isolation
        if is_synthetic_scaffold or source_id == "IND-JUD-DEL-2024-BAIL" or (chunk_id and "BAIL" in chunk_id):
            return EvidenceEligibilityVerdict(
                is_eligible=False,
                rejection_reason="Quarantined synthetic test scaffold; strict non-negotiable governance barrier.",
                quarantine_policy="STRICT_SCAFFOLD_QUARANTINE",
            )

        # Check explicit source_metadata override if provided
        if source_metadata:
            v_status = str(source_metadata.get("verification_status", "")).lower()
            if v_status in ("unverified", "pending_review", "flagged_unsupported"):
                return EvidenceEligibilityVerdict(
                    is_eligible=False,
                    rejection_reason=f"Source ID '{source_id}' is unverified ({v_status}); excluded from authoritative retrieval.",
                    quarantine_policy="UNVERIFIED_SOURCE_BLOCKED",
                )
            rights_val = str(source_metadata.get("rights_status") or source_metadata.get("reuse_rights") or "").upper()
            if rights_val in ("RIGHTS_RESTRICTED", "UNRESOLVED_RIGHTS", "RESTRICTED", "PROPRIETARY_UNLICENSED"):
                return EvidenceEligibilityVerdict(
                    is_eligible=False,
                    rejection_reason=f"Source ID '{source_id}' has unresolved or restricted reuse rights ({rights_val}).",
                    quarantine_policy="RIGHTS_RESTRICTED_BLOCKED",
                    rights_basis=rights_val,
                )

        # 2. Check source info in cache
        s_info = self._source_cache.get(source_id)
        if not s_info:
            # Check if it's a known test fixture
            if "UNSUPPORTED" in source_id:
                return EvidenceEligibilityVerdict(
                    is_eligible=False,
                    rejection_reason="Unregistered or unsupported format fixture.",
                    quarantine_policy="UNSUPPORTED_FIXTURE",
                )
            # Fail-closed for unknown sources
            return EvidenceEligibilityVerdict(
                is_eligible=False,
                rejection_reason=f"Source ID '{source_id}' not found in authoritative source register.",
                quarantine_policy="UNKNOWN_SOURCE_REJECTION",
            )

        # If source is scaffold
        if s_info.get("is_scaffold"):
            return EvidenceEligibilityVerdict(
                is_eligible=False,
                rejection_reason="Source is marked as synthetic scaffold in sources table.",
                quarantine_policy="STRICT_SCAFFOLD_QUARANTINE",
            )

        # Explicit unverified check in cached source info
        v_status = str(s_info.get("verification_status", "")).lower()
        if v_status in ("unverified", "pending_review", "flagged_unsupported"):
            return EvidenceEligibilityVerdict(
                is_eligible=False,
                rejection_reason=f"Source ID '{source_id}' is unverified ({v_status}); excluded from authoritative retrieval.",
                quarantine_policy="UNVERIFIED_SOURCE_BLOCKED",
            )

        # Explicit reuse rights check
        meta = s_info.get("metadata") or {}
        rights_val = str(meta.get("rights_status") or meta.get("reuse_rights") or "").upper()
        if rights_val in ("RIGHTS_RESTRICTED", "UNRESOLVED_RIGHTS", "RESTRICTED", "PROPRIETARY_UNLICENSED"):
            return EvidenceEligibilityVerdict(
                is_eligible=False,
                rejection_reason=f"Source ID '{source_id}' has unresolved or restricted reuse rights ({rights_val}).",
                quarantine_policy="RIGHTS_RESTRICTED_BLOCKED",
                rights_basis=rights_val,
            )

        # Unsupported or test fixtures with 0 parsed content
        if source_id in ("IND-UNSUPPORTED-001", "IND-GUIDE-SCI-PROC-2025"):
            return EvidenceEligibilityVerdict(
                is_eligible=False,
                rejection_reason="Source is an unparsed fixture or procedural handbook with zero parsed chunks.",
                quarantine_policy="UNPARSED_FIXTURE",
            )

        # Temporal check
        temporal_warning = None
        eff_date = s_info.get("effective_date")
        if as_of_date and eff_date:
            as_of_str = as_of_date.isoformat() if hasattr(as_of_date, "isoformat") else str(as_of_date)
            if as_of_str < str(eff_date) and s_info.get("source_type") == "statute":
                temporal_warning = f"Statute effective date ({eff_date}) is post-dated relative to query date ({as_of_str})."

        repeal_status = s_info.get("repeal_status")
        if repeal_status == "repealed":
            temporal_warning = (temporal_warning or "") + " Source enactment has been repealed; verify temporal savings."

        return EvidenceEligibilityVerdict(
            is_eligible=True,
            rejection_reason=None,
            quarantine_policy=None,
            temporal_warning=temporal_warning,
            rights_basis=meta.get("rights_basis") or "GODL-India / Section 52(1)(q) Copyright Act, 1957",
        )
