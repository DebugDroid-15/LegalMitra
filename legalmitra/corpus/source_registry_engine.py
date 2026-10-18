"""
LegalMitra National Legal Source Registry Engine (Phase 35).
Implements an auditable Finite State Machine (FSM) governing legal document lifecycle:
DISCOVERED -> REGISTERED -> ACQUIRED -> PARSED -> AUTHENTICITY_VERIFIED -> RIGHTS_REVIEWED -> TRAINING_ELIGIBLE.
Enforces strict transition validation, rights review, and prevents unauthorized pretraining data eligibility.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union


class SourceLifecycleState(str, Enum):
    """Finite State Machine states for legal data lifecycle."""
    # Active linear progression
    DISCOVERED = "DISCOVERED"
    REGISTERED = "REGISTERED"
    ACQUIRED = "ACQUIRED"
    PARSED = "PARSED"
    AUTHENTICITY_VERIFIED = "AUTHENTICITY_VERIFIED"
    RIGHTS_REVIEWED = "RIGHTS_REVIEWED"
    TRAINING_ELIGIBLE = "TRAINING_ELIGIBLE"

    # Terminal or exceptional states
    BLOCKED = "BLOCKED"
    QUARANTINED = "QUARANTINED"
    DUPLICATE = "DUPLICATE"
    PARSE_FAILED = "PARSE_FAILED"
    RIGHTS_UNRESOLVED = "RIGHTS_UNRESOLVED"


class IllegalStateTransitionError(ValueError):
    """Raised when an invalid or unauthorized lifecycle state transition is attempted."""
    pass


# Strict allowed transition mapping
ALLOWED_TRANSITIONS: Dict[SourceLifecycleState, Set[SourceLifecycleState]] = {
    SourceLifecycleState.DISCOVERED: {
        SourceLifecycleState.REGISTERED,
        SourceLifecycleState.BLOCKED,
        SourceLifecycleState.DUPLICATE,
        SourceLifecycleState.QUARANTINED,
    },
    SourceLifecycleState.REGISTERED: {
        SourceLifecycleState.ACQUIRED,
        SourceLifecycleState.BLOCKED,
        SourceLifecycleState.QUARANTINED,
    },
    SourceLifecycleState.ACQUIRED: {
        SourceLifecycleState.PARSED,
        SourceLifecycleState.PARSE_FAILED,
        SourceLifecycleState.QUARANTINED,
        SourceLifecycleState.BLOCKED,
    },
    SourceLifecycleState.PARSED: {
        SourceLifecycleState.AUTHENTICITY_VERIFIED,
        SourceLifecycleState.BLOCKED,
        SourceLifecycleState.QUARANTINED,
    },
    SourceLifecycleState.AUTHENTICITY_VERIFIED: {
        SourceLifecycleState.RIGHTS_REVIEWED,
        SourceLifecycleState.RIGHTS_UNRESOLVED,
        SourceLifecycleState.BLOCKED,
    },
    SourceLifecycleState.RIGHTS_REVIEWED: {
        SourceLifecycleState.TRAINING_ELIGIBLE,
        SourceLifecycleState.RIGHTS_UNRESOLVED,
        SourceLifecycleState.BLOCKED,
    },
    # Training-eligible can be revoked if issues discovered
    SourceLifecycleState.TRAINING_ELIGIBLE: {
        SourceLifecycleState.RIGHTS_UNRESOLVED,
        SourceLifecycleState.QUARANTINED,
        SourceLifecycleState.BLOCKED,
    },
    # Terminal / Recovery states
    SourceLifecycleState.PARSE_FAILED: {
        SourceLifecycleState.PARSED,  # Retry after parser upgrade
        SourceLifecycleState.BLOCKED,
        SourceLifecycleState.QUARANTINED,
    },
    SourceLifecycleState.RIGHTS_UNRESOLVED: {
        SourceLifecycleState.RIGHTS_REVIEWED,  # Resolved after legal assessment
        SourceLifecycleState.BLOCKED,
    },
    SourceLifecycleState.QUARANTINED: {
        SourceLifecycleState.BLOCKED,  # Quarantine is terminal unless explicitly unquarantined
    },
    SourceLifecycleState.BLOCKED: set(),
    SourceLifecycleState.DUPLICATE: set(),
}


@dataclass
class StateTransitionLog:
    timestamp: str
    from_state: str
    to_state: str
    reason: str
    actor: str = "system"


@dataclass
class SourceRegistryEntry:
    source_id: str
    official_title: str
    issuing_authority: str
    source_url: str
    source_type: str  # statute, judgment, rules_regulation, notification, manual
    jurisdiction: str  # IN, IN-DL, IN-MH, IN-WB, IN-TN, IN-KA, etc.
    language: str  # en, hi, mixed
    document_family: str
    document_identifier: str
    publication_date: Optional[str] = None
    acquisition_timestamp: Optional[str] = None
    commencement_date: Optional[str] = None
    effective_date: Optional[str] = None
    current_state: SourceLifecycleState = SourceLifecycleState.DISCOVERED
    content_hash: Optional[str] = None
    byte_size: int = 0
    duplicate_of: Optional[str] = None
    version: str = "1.0.0"
    rights_basis: Optional[str] = None
    pretraining_eligible: bool = False
    last_verified_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    error_message: Optional[str] = None
    history: List[Dict[str, Any]] = field(default_factory=list)
    derived_passages_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["current_state"] = self.current_state.value if isinstance(self.current_state, SourceLifecycleState) else str(self.current_state)
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SourceRegistryEntry:
        data_copy = dict(data)
        if isinstance(data_copy.get("current_state"), str):
            data_copy["current_state"] = SourceLifecycleState(data_copy["current_state"])
        return cls(**data_copy)


class UnifiedSourceRegistry:
    """
    Unified National Legal Source Registry.
    Tracks all discovered, acquired, and validated legal sources with an auditable FSM.
    """

    def __init__(self, registry_file: Union[str, Path] = "data/09_national_corpus/unified_source_registry.json"):
        self.registry_file = Path(registry_file)
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        self.records: Dict[str, SourceRegistryEntry] = {}
        self.load()

    def load(self) -> None:
        if self.registry_file.exists():
            try:
                with open(self.registry_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for rec in data.get("sources", []):
                        entry = SourceRegistryEntry.from_dict(rec)
                        self.records[entry.source_id] = entry
            except Exception as e:
                self.records = {}

    def save(self) -> None:
        data = {
            "registry_version": "v1.0.0",
            "last_updated": datetime.utcnow().isoformat(),
            "total_registered_sources": len(self.records),
            "training_eligible_count": sum(1 for r in self.records.values() if r.current_state == SourceLifecycleState.TRAINING_ELIGIBLE),
            "quarantined_count": sum(1 for r in self.records.values() if r.current_state == SourceLifecycleState.QUARANTINED),
            "sources": [r.to_dict() for r in self.records.values()],
        }
        temp_path = self.registry_file.with_suffix(".tmp")
        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            try:
                temp_path.replace(self.registry_file)
            except (PermissionError, OSError):
                with open(self.registry_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                if temp_path.exists():
                    try:
                        temp_path.unlink()
                    except Exception:
                        pass
        except Exception:
            with open(self.registry_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    def register_discovered_source(
        self,
        source_id: str,
        official_title: str,
        issuing_authority: str,
        source_url: str,
        source_type: str,
        jurisdiction: str,
        language: str,
        document_family: str,
        document_identifier: str,
        publication_date: Optional[str] = None,
        effective_date: Optional[str] = None,
        commencement_date: Optional[str] = None,
        auto_save: bool = True,
    ) -> SourceRegistryEntry:
        """Register a newly discovered primary legal source in DISCOVERED state."""
        if source_id in self.records:
            return self.records[source_id]

        now = datetime.utcnow().isoformat()
        entry = SourceRegistryEntry(
            source_id=source_id,
            official_title=official_title,
            issuing_authority=issuing_authority,
            source_url=source_url,
            source_type=source_type,
            jurisdiction=jurisdiction,
            language=language,
            document_family=document_family,
            document_identifier=document_identifier,
            publication_date=publication_date,
            effective_date=effective_date,
            commencement_date=commencement_date,
            current_state=SourceLifecycleState.DISCOVERED,
            history=[
                asdict(StateTransitionLog(
                    timestamp=now,
                    from_state="NONE",
                    to_state=SourceLifecycleState.DISCOVERED.value,
                    reason="Source candidate discovered via official portal audit",
                ))
            ],
        )
        self.records[source_id] = entry
        if auto_save:
            self.save()
        return entry

    def transition_state(
        self,
        source_id: str,
        target_state: SourceLifecycleState,
        reason: str,
        actor: str = "system",
        auto_save: bool = True,
        **metadata_updates,
    ) -> SourceRegistryEntry:
        """
        Safely transition a source to a new lifecycle state.
        Raises IllegalStateTransitionError if the transition is prohibited by FSM rules.
        """
        if source_id not in self.records:
            raise KeyError(f"Source {source_id} not found in registry")

        entry = self.records[source_id]
        current = entry.current_state

        allowed = ALLOWED_TRANSITIONS.get(current, set())
        if target_state not in allowed:
            raise IllegalStateTransitionError(
                f"Cannot transition source '{source_id}' from state '{current.value}' to '{target_state.value}'. "
                f"Permitted next states: {[s.value for s in allowed]}"
            )

        now = datetime.utcnow().isoformat()
        log = StateTransitionLog(
            timestamp=now,
            from_state=current.value,
            to_state=target_state.value,
            reason=reason,
            actor=actor,
        )
        entry.current_state = target_state
        entry.last_verified_at = now
        entry.history.append(asdict(log))

        # Update eligibility flag automatically based on state
        entry.pretraining_eligible = (target_state == SourceLifecycleState.TRAINING_ELIGIBLE)

        # Apply any metadata updates (content_hash, byte_size, etc.)
        for k, v in metadata_updates.items():
            if hasattr(entry, k):
                setattr(entry, k, v)

        if auto_save:
            self.save()
        return entry

    def get_training_eligible_sources(self) -> List[SourceRegistryEntry]:
        """Return strictly training-eligible sources."""
        return [
            r for r in self.records.values()
            if r.current_state == SourceLifecycleState.TRAINING_ELIGIBLE and r.pretraining_eligible
        ]

    def get_source(self, source_id: str) -> Optional[SourceRegistryEntry]:
        return self.records.get(source_id)

    def total_count(self) -> int:
        return len(self.records)
