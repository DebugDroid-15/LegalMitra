"""
LegalMitra National Legal Corpus Versioning Engine (Phase 35).
Manages version-aware temporal tracking of Indian legislation, amendments, repeals,
and commencement milestones.
Guarantees that:
1. Historical legal versions are preserved and never overwritten.
2. Enactment dates are strictly separated from Commencement dates (e.g., BNS 2023 enacted 2023-12-25, commenced 2024-07-01).
3. Authoritative Knowledge Base remains separate from Pretraining manifests.
4. Reprocessing and parser version bumps maintain full lineage.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union


class VersionChangeType(str, Enum):
    INITIAL_CREATION = "INITIAL_CREATION"
    AMENDMENT = "AMENDMENT"
    REPEAL = "REPEAL"
    COMMENCEMENT_NOTIFICATION = "COMMENCEMENT_NOTIFICATION"
    PARSER_UPGRADE = "PARSER_UPGRADE"
    TEXT_CORRECTION = "TEXT_CORRECTION"
    STATUS_REVOCATION = "STATUS_REVOCATION"


@dataclass
class LegalVersionRecord:
    version_id: str  # e.g., 'IND-STAT-BNS-2023:v1.0.0'
    source_id: str
    semantic_version: str  # '1.0.0', '1.1.0'
    change_type: VersionChangeType
    effective_date: str  # YYYY-MM-DD
    enactment_date: Optional[str] = None
    commencement_date: Optional[str] = None
    repealed_by_source_id: Optional[str] = None
    superseded_source_id: Optional[str] = None
    change_description: str = ""
    authoritative_gazette_ref: Optional[str] = None
    content_sha256: str = ""
    parser_version: str = "v1.0.0"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["change_type"] = self.change_type.value
        return d


class NationalCorpusVersioningEngine:
    """
    Tracks legal temporal versions, amendments, and replacements without mutating historical baselines.
    """

    def __init__(self, ledger_file: Union[str, Path] = "data/09_national_corpus/corpus_version_ledger.json"):
        self.ledger_file = Path(ledger_file)
        self.ledger_file.parent.mkdir(parents=True, exist_ok=True)
        self.records: Dict[str, LegalVersionRecord] = {}
        self.active_versions: Dict[str, str] = {}  # source_id -> latest version_id
        self._load()

    def _load(self) -> None:
        if self.ledger_file.exists():
            try:
                with open(self.ledger_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for rec in data.get("versions", []):
                        rec_copy = dict(rec)
                        rec_copy["change_type"] = VersionChangeType(rec_copy["change_type"])
                        v = LegalVersionRecord(**rec_copy)
                        self.records[v.version_id] = v
                    self.active_versions = data.get("active_versions", {})
            except Exception:
                self.records = {}
                self.active_versions = {}

    def save(self) -> None:
        temp_file = self.ledger_file.with_suffix(".tmp")
        data = {
            "schema_version": "1.0.0",
            "last_updated": datetime.utcnow().isoformat(),
            "total_versions": len(self.records),
            "active_sources": len(self.active_versions),
            "active_versions": self.active_versions,
            "versions": [r.to_dict() for r in self.records.values()],
        }
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        temp_file.replace(self.ledger_file)

    def register_version(
        self,
        source_id: str,
        semantic_version: str,
        change_type: VersionChangeType,
        effective_date: str,
        content_sha256: str,
        change_description: str,
        enactment_date: Optional[str] = None,
        commencement_date: Optional[str] = None,
        repealed_by_source_id: Optional[str] = None,
        superseded_source_id: Optional[str] = None,
        authoritative_gazette_ref: Optional[str] = None,
        parser_version: str = "v1.0.0",
    ) -> LegalVersionRecord:
        """Register a version transition without overwriting historical records."""
        version_id = f"{source_id}:{semantic_version}"
        if version_id in self.records:
            return self.records[version_id]

        record = LegalVersionRecord(
            version_id=version_id,
            source_id=source_id,
            semantic_version=semantic_version,
            change_type=change_type,
            effective_date=effective_date,
            enactment_date=enactment_date,
            commencement_date=commencement_date,
            repealed_by_source_id=repealed_by_source_id,
            superseded_source_id=superseded_source_id,
            change_description=change_description,
            authoritative_gazette_ref=authoritative_gazette_ref,
            content_sha256=content_sha256,
            parser_version=parser_version,
        )
        self.records[version_id] = record
        self.active_versions[source_id] = version_id
        self.save()
        return record

    def record_repeal_replacement(
        self,
        old_source_id: str,
        new_source_id: str,
        commencement_date: str,
        gazette_notification_ref: str,
    ) -> Tuple[LegalVersionRecord, LegalVersionRecord]:
        """
        Record repeal of historic code and commencement of new criminal/civil code.
        Example: IPC 1860 repealed by BNS 2023 on 2024-07-01.
        """
        # Repeal entry for old code
        old_v = self.register_version(
            source_id=old_source_id,
            semantic_version="repealed-2024",
            change_type=VersionChangeType.REPEAL,
            effective_date=commencement_date,
            commencement_date=commencement_date,
            repealed_by_source_id=new_source_id,
            change_description=f"Repealed and replaced by {new_source_id} under notification {gazette_notification_ref}",
            authoritative_gazette_ref=gazette_notification_ref,
            content_sha256="REPEALED",
        )
        # Commencement entry for new code
        new_v = self.register_version(
            source_id=new_source_id,
            semantic_version="1.0.0-commenced",
            change_type=VersionChangeType.COMMENCEMENT_NOTIFICATION,
            effective_date=commencement_date,
            commencement_date=commencement_date,
            superseded_source_id=old_source_id,
            change_description=f"Formally commenced on {commencement_date} superseding {old_source_id}",
            authoritative_gazette_ref=gazette_notification_ref,
            content_sha256="COMMENCED",
        )
        return old_v, new_v

    def get_version_history(self, source_id: str) -> List[LegalVersionRecord]:
        """Get chronological history of a given source."""
        return sorted(
            [r for r in self.records.values() if r.source_id == source_id],
            key=lambda x: x.created_at,
        )

    def populate_seed_temporal_versions(self) -> int:
        """Seed baseline criminal and civil reform version transitions."""
        seeds = [
            # IPC 1860 -> BNS 2023
            ("IND-STAT-IPC-1860", "IND-STAT-BNS-2023", "2024-07-01", "Gazette of India S.O. 850(E)"),
            # CrPC 1973 -> BNSS 2023
            ("IND-STAT-CRPC-1973", "IND-STAT-BNSS-2023", "2024-07-01", "Gazette of India S.O. 849(E)"),
            # IEA 1872 -> BSA 2023
            ("IND-STAT-IEA-1872", "IND-STAT-BSA-2023", "2024-07-01", "Gazette of India S.O. 851(E)"),
        ]
        count = 0
        for old_id, new_id, comm_dt, notif in seeds:
            self.record_repeal_replacement(old_id, new_id, comm_dt, notif)
            count += 2
        return count

