"""
Source Rights & Permitted Use Registry — LegalMitra Phase 52
Implements Workstream C: Source Rights, Copyright Law Compliance, and Retrieval Safeguards.
Strictly distinguishes internal evidence retrieval from foundation model pretraining (STRICT NO-GO).
"""

import json
import logging
import os
import sqlite3
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class SourceRightsRecord:
    document_id: str
    title: str
    source_type: str
    legal_basis: str  # e.g., "Copyright Act 1957 s.52(1)(q)(iv) / GODL-India"
    rights_status: str  # RIGHTS_VERIFIED, RIGHTS_RESTRICTED, RIGHTS_REVIEW_REQUIRED
    internal_retrieval_permitted: bool
    training_use_permitted: str  # "STRICTLY_PROHIBITED" (Non-negotiable architectural invariant)
    attribution_requirement: str
    retrieval_context_notes: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SourceRightsRegistry:
    manifest_version: str
    registry_id: str
    generated_at: str
    total_registered_records: int
    rights_verified_count: int
    rights_restricted_count: int
    training_prohibited_enforced: bool
    statutory_framework: Dict[str, str]
    records: List[SourceRightsRecord] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["records"] = [r.to_dict() if hasattr(r, "to_dict") else r for r in self.records]
        return d


class SourceRightsEngine:
    """
    Audits and registers permitted rights, licenses, and strict retrieval vs training boundaries.
    """

    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = workspace_root or os.getcwd()
        self.db_path = os.path.join(self.workspace_root, "data", "legalmitra_kb.db")
        self.manifest_dir = os.path.join(self.workspace_root, "data", "22_central_legislation")

    def audit_rights(self) -> SourceRightsRegistry:
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database missing at {self.db_path}")

        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            "SELECT document_id, title, source_type, is_synthetic_scaffold, metadata_json FROM sources"
        )
        rows = cur.fetchall()
        conn.close()

        records: List[SourceRightsRecord] = []

        for r in rows:
            doc_id = r[0]
            title = r[1]
            stype = r[2]
            is_scaffold = bool(r[3])

            if is_scaffold or doc_id == "IND-JUD-DEL-2024-BAIL":
                legal_basis = "Internal Synthetic Benchmark Scaffold (Non-Public)"
                rights_status = "RIGHTS_RESTRICTED"
                retrieval_ok = False
                attr = "LegalMitra Test Harness Only"
                notes = "Quarantined synthetic test scaffold. Never eligible for production retrieval or model training."
            elif doc_id in ("IND-UNSUPPORTED-001", "IND-GUIDE-SCI-PROC-2025"):
                legal_basis = "Official Administrative Publication / Unparsed Test Fixture"
                rights_status = "RIGHTS_REVIEW_REQUIRED"
                retrieval_ok = False
                attr = "Supreme Court of India / Diagnostic Fixture"
                notes = "Unprocessed fixture or practice handbook. Retrieval disabled until full ingestion."
            elif stype == "statute" or stype == "rules_regulation" or stype == "notification":
                legal_basis = "Section 52(1)(q)(i), (ii) Copyright Act, 1957 & GODL-India (Gazette of India)"
                rights_status = "RIGHTS_VERIFIED"
                retrieval_ok = True
                attr = "Government of India / Legislative Department / Official Gazette"
                notes = "Statutory text published under official authority. Permitted for internal legal query retrieval."
            elif stype == "judgment":
                legal_basis = "Section 52(1)(q)(iv) Copyright Act, 1957 (Judgments of Court/Tribunal)"
                rights_status = "RIGHTS_VERIFIED"
                retrieval_ok = True
                attr = "Supreme Court of India / Respective High Court"
                notes = "Judicial ruling reproduction permitted under s.52(1)(q)(iv). Permitted for internal legal query retrieval."
            else:
                legal_basis = "Government Open Data / Public Domain Legal Material"
                rights_status = "RIGHTS_VERIFIED"
                retrieval_ok = True
                attr = "Public Domain"
                notes = "Public legal authority."

            records.append(
                SourceRightsRecord(
                    document_id=doc_id,
                    title=title,
                    source_type=stype,
                    legal_basis=legal_basis,
                    rights_status=rights_status,
                    internal_retrieval_permitted=retrieval_ok,
                    training_use_permitted="STRICTLY_PROHIBITED",  # Non-negotiable
                    attribution_requirement=attr,
                    retrieval_context_notes=notes,
                )
            )

        verified_count = sum(1 for r in records if r.rights_status == "RIGHTS_VERIFIED")
        restricted_count = sum(1 for r in records if r.rights_status in ("RIGHTS_RESTRICTED", "RIGHTS_REVIEW_REQUIRED"))

        registry = SourceRightsRegistry(
            manifest_version="1.0.0",
            registry_id="SOURCE-RIGHTS-REGISTRY-PHASE52",
            generated_at=datetime.now(timezone.utc).isoformat(),
            total_registered_records=len(records),
            rights_verified_count=verified_count,
            rights_restricted_count=restricted_count,
            training_prohibited_enforced=True,
            statutory_framework={
                "copyright_act_1957": "Section 52(1)(q) exempts reproduction of parliamentary acts, gazette notifications, and court judgments",
                "godl_india": "Government Open Data License - India applies to Central Government official datasets",
                "internal_vs_training_boundary": "Internal knowledge-base indexing and zero-shot retrieval are permitted; foundation-model pretraining is STRICT NO-GO",
            },
            records=records,
        )
        return registry

    def generate_registry(self, output_path: Optional[str] = None) -> str:
        registry = self.audit_rights()
        target = output_path or os.path.join(self.manifest_dir, "source_rights_registry.json")
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            json.dump(registry.to_dict(), f, indent=2, ensure_ascii=False)
        logger.info(f"Generated Source Rights Registry at {target}")
        return target
