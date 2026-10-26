"""
LegalMitra Unified Observability & Failure Diagnosis (Phase 65)
Provides structured request/operation tracing across ingestion, retrieval,
validation, and recovery with standardized failure taxonomy and correlation IDs.
"""

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
import time
from typing import Any, Dict, List, Optional
import uuid

from legalmitra.core.logging import get_logger, redact_sensitive_text

logger = get_logger("observability")


class FailureCategory(str, Enum):
    """Actionable failure taxonomy distinguishing recovery, safety, and security states."""
    TRANSIENT_NETWORK = "TRANSIENT_NETWORK"
    PERMANENT_SOURCE_CORRUPT = "PERMANENT_SOURCE_CORRUPT"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    AUTHENTICITY_UNVERIFIED = "AUTHENTICITY_UNVERIFIED"
    AUTHORIZATION_DENIED = "AUTHORIZATION_DENIED"
    PROMPT_INJECTION_BLOCKED = "PROMPT_INJECTION_BLOCKED"
    SCAFFOLD_INTERCEPTED = "SCAFFOLD_INTERCEPTED"
    INDEX_CORRUPTION_DETECTED = "INDEX_CORRUPTION_DETECTED"
    STALE_VERSION_DETECTED = "STALE_VERSION_DETECTED"
    CONCURRENCY_LOCK_TIMEOUT = "CONCURRENCY_LOCK_TIMEOUT"


@dataclass
class DiagnosticEvent:
    """Timestamped event within an operational span."""
    event_name: str
    timestamp_utc: str
    payload: Dict[str, Any] = field(default_factory=dict)


class OperationContext:
    """
    Structured execution context propagating trace IDs and metrics across pipeline stages.
    Can be used as a context manager for automatic timing and error classification.
    """

    def __init__(
        self,
        operation_name: str,
        stage: str = "general",
        trace_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.operation_name = operation_name
        self.stage = stage
        self.trace_id = trace_id or f"TRC-{uuid.uuid4().hex[:12].upper()}"
        self.parent_id = parent_id
        self.metadata = metadata or {}
        self.start_time: float = 0.0
        self.end_time: Optional[float] = None
        self.duration_ms: float = 0.0
        self.status: str = "PENDING"
        self.failure_category: Optional[FailureCategory] = None
        self.error_message: Optional[str] = None
        self.events: List[DiagnosticEvent] = []

    def __enter__(self) -> "OperationContext":
        self.start_time = time.perf_counter()
        self.status = "IN_PROGRESS"
        logger.debug(
            f"[{self.trace_id}] Start operation '{self.operation_name}' stage='{self.stage}'"
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.end_time = time.perf_counter()
        self.duration_ms = (self.end_time - self.start_time) * 1000.0

        if exc_type is not None:
            self.status = "FAILED"
            raw_msg = str(exc_val)
            self.error_message = redact_sensitive_text(raw_msg)
            if not self.failure_category:
                self.failure_category = self._infer_failure_category(raw_msg)
            logger.error(
                f"[{self.trace_id}] Operation '{self.operation_name}' failed "
                f"[{self.failure_category}]: {self.error_message}"
            )
            # Propagate exception unless handled by caller
            return False

        if self.status == "IN_PROGRESS":
            self.status = "SUCCESS"
        logger.debug(
            f"[{self.trace_id}] Completed '{self.operation_name}' status={self.status} duration={self.duration_ms:.2f}ms"
        )
        return False

    def record_event(self, event_name: str, payload: Optional[Dict[str, Any]] = None) -> None:
        """Record an in-flight milestone or event."""
        event = DiagnosticEvent(
            event_name=event_name,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            payload=payload or {},
        )
        self.events.append(event)

    def mark_failed(self, category: FailureCategory, message: str) -> None:
        """Mark the operation as failed with an explicit category and sanitized message."""
        self.status = "FAILED"
        self.failure_category = category
        self.error_message = redact_sensitive_text(message)
        self.record_event("OPERATION_FAILED", {"category": category.value, "error": self.error_message})

    def mark_blocked(self, category: FailureCategory, reason: str) -> None:
        """Mark operation as blocked by security or governance safeguards."""
        self.status = "BLOCKED"
        self.failure_category = category
        self.error_message = redact_sensitive_text(reason)
        self.record_event("OPERATION_BLOCKED", {"category": category.value, "reason": self.error_message})

    def _infer_failure_category(self, message: str) -> FailureCategory:
        """Infer standardized category from exception message if not explicitly set."""
        lowered = message.lower()
        if "lock" in lowered or "busy" in lowered:
            return FailureCategory.CONCURRENCY_LOCK_TIMEOUT
        if "timeout" in lowered or "connection refused" in lowered or "network" in lowered:
            return FailureCategory.TRANSIENT_NETWORK
        if "scaffold" in lowered or "bail" in lowered:
            return FailureCategory.SCAFFOLD_INTERCEPTED
        if "injection" in lowered or "prompt" in lowered or "adversarial" in lowered:
            return FailureCategory.PROMPT_INJECTION_BLOCKED
        if "rights" in lowered or "license" in lowered or "unauthorized" in lowered:
            return FailureCategory.AUTHORIZATION_DENIED
        if "unverified" in lowered or "unsupported" in lowered:
            return FailureCategory.AUTHENTICITY_UNVERIFIED
        if "corrupt" in lowered or "checksum mismatch" in lowered or "damaged" in lowered:
            return FailureCategory.PERMANENT_SOURCE_CORRUPT
        if "fts" in lowered or "index" in lowered:
            return FailureCategory.INDEX_CORRUPTION_DETECTED
        if "stale" in lowered or "repealed" in lowered or "superseded" in lowered:
            return FailureCategory.STALE_VERSION_DETECTED
        return FailureCategory.VALIDATION_FAILED

    def to_dict(self) -> Dict[str, Any]:
        """Return machine-readable dictionary representation of the operation."""
        return {
            "trace_id": self.trace_id,
            "operation_name": self.operation_name,
            "stage": self.stage,
            "parent_id": self.parent_id,
            "status": self.status,
            "failure_category": self.failure_category.value if self.failure_category else None,
            "error_message": self.error_message,
            "duration_ms": round(self.duration_ms, 3),
            "metadata": self.metadata,
            "events_count": len(self.events),
            "events": [
                {
                    "event_name": e.event_name,
                    "timestamp_utc": e.timestamp_utc,
                    "payload": e.payload,
                }
                for e in self.events
            ],
        }

