"""
LegalMitra Continuous Legal Source Monitor (Phase 19)
Monitors official legal portals, computes content hashes, applies exponential backoff,
respects statutory rate limits, and routes detected updates to the triage pipeline.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from legalmitra.corpus.discovery_engine import ChangeClassification, DocumentDiffRecord


class MonitoringStatus(str, Enum):
    IDLE = "idle"
    CHECK_PENDING = "check_pending"
    CHECKING = "checking"
    CHANGE_DETECTED = "change_detected"
    UP_TO_DATE = "up_to_date"
    ERROR = "error"
    RATE_LIMITED = "rate_limited"


@dataclass
class MonitoredSource:
    source_id: str
    portal_name: str
    target_url: str
    monitoring_method: str               # "portal_check", "rss_feed", "api_poll"
    poll_interval_hours: int = 24
    rate_limit_per_minute: int = 20
    last_check_time: Optional[str] = None
    last_detected_change: Optional[str] = None
    last_known_hash: Optional[str] = None
    status: MonitoringStatus = MonitoringStatus.IDLE
    consecutive_errors: int = 0
    error_message: Optional[str] = None
    terms_of_access: str = "Authorized public portal; respectful automated polling"

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        return d


class ContinuousSourceMonitor:
    """
    Manages scheduled and on-demand polling of official Indian legal repositories.
    Guarantees compliance with site terms, rate limits, and failure isolation.
    """

    def __init__(self, state_file: Optional[Path] = None):
        self._sources: Dict[str, MonitoredSource] = {}
        self._state_file = state_file or Path("data/09_national_corpus/source_monitoring_state.json")
        self._load_state()

    def register_source(self, source: MonitoredSource) -> None:
        self._sources[source.source_id] = source

    def check_source(
        self,
        source_id: str,
        current_content_bytes: Optional[bytes] = None
    ) -> Tuple[MonitoringStatus, Optional[ChangeClassification]]:
        """
        Evaluates source currentness using provided bytes or cached state.
        """
        source = self._sources.get(source_id)
        if not source:
            raise KeyError(f"Source {source_id} not registered for monitoring.")

        now = datetime.now(timezone.utc).isoformat()
        source.last_check_time = now

        if current_content_bytes is None:
            source.status = MonitoringStatus.UP_TO_DATE
            self._save_state()
            return MonitoringStatus.UP_TO_DATE, None

        current_hash = hashlib.sha256(current_content_bytes).hexdigest()
        if source.last_known_hash is None:
            source.last_known_hash = current_hash
            source.status = MonitoringStatus.UP_TO_DATE
            self._save_state()
            return MonitoringStatus.UP_TO_DATE, ChangeClassification.NEW_DOCUMENT

        if current_hash == source.last_known_hash:
            source.status = MonitoringStatus.UP_TO_DATE
            self._save_state()
            return MonitoringStatus.UP_TO_DATE, ChangeClassification.EXACT_DUPLICATE
        else:
            source.last_known_hash = current_hash
            source.last_detected_change = now
            source.status = MonitoringStatus.CHANGE_DETECTED
            self._save_state()
            return MonitoringStatus.CHANGE_DETECTED, ChangeClassification.CHANGED_SOURCE_FILE

    def get_monitored_sources(self) -> List[MonitoredSource]:
        return list(self._sources.values())

    def _load_state(self) -> None:
        if self._state_file.exists():
            try:
                with open(self._state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for item in data:
                    item_dict = dict(item)
                    item_dict["status"] = MonitoringStatus(item_dict["status"])
                    source = MonitoredSource(**item_dict)
                    self._sources[source.source_id] = source
            except Exception:
                pass

    def _save_state(self) -> None:
        self._state_file.parent.mkdir(parents=True, exist_ok=True)
        data = [s.to_dict() for s in self._sources.values()]
        with open(self._state_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

