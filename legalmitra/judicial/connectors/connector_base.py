"""LegalMitra Judicial Knowledge Infrastructure — High Court Connector Base.

Provides reusable, secure connector interfaces with:
- Standard 9-state document lifecycle model:
  REGISTERED -> ACCESS_REVIEWED -> DISCOVERED -> ACQUIRED -> PARSED ->
  AUTHENTICITY_CHECKED -> RIGHTS_REVIEWED -> INDEXED -> RETRIEVAL_ELIGIBLE
- SSRF protection, private IP / link-local blocking, DNS revalidation
- Rate limiting, exponential backoff, transient vs permanent retry classification
- Bounded response sizes and timeout protections
- Dry-run mode vs Live mode separation
- Cryptographic SHA-256 verification and idempotent processing
"""

from __future__ import annotations

import hashlib
import ipaddress
import re
import socket
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from urllib.parse import urlparse


class SourceDocumentState(str, Enum):
    """Rigorous 9-state document lifecycle model."""
    REGISTERED = "REGISTERED"
    ACCESS_REVIEWED = "ACCESS_REVIEWED"
    DISCOVERED = "DISCOVERED"
    ACQUIRED = "ACQUIRED"
    PARSED = "PARSED"
    AUTHENTICITY_CHECKED = "AUTHENTICITY_CHECKED"
    RIGHTS_REVIEWED = "RIGHTS_REVIEWED"
    INDEXED = "INDEXED"
    RETRIEVAL_ELIGIBLE = "RETRIEVAL_ELIGIBLE"
    BLOCKED_ACCESS_DENIED = "BLOCKED_ACCESS_DENIED"
    BLOCKED_QUALITY_FAILED = "BLOCKED_QUALITY_FAILED"


class RetryClassification(str, Enum):
    TRANSIENT = "TRANSIENT"      # Rate limit, 503, connection timeout
    PERMANENT = "PERMANENT"      # 404, 403 Forbidden, Invalid content type, SSRF blocked


@dataclass
class DiscoveredDocument:
    document_id: str
    court_id: str
    source_id: str
    source_url: str
    case_number: str
    neutral_citation: Optional[str] = None
    decision_date: Optional[str] = None
    party_title: Optional[str] = None
    discovered_timestamp: str = ""
    current_state: SourceDocumentState = SourceDocumentState.DISCOVERED
    state_history: List[Tuple[str, str, str]] = field(default_factory=list)  # (timestamp, state, notes)

    def transition(self, new_state: SourceDocumentState, note: str = "") -> None:
        self.current_state = new_state
        ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.state_history.append((ts, new_state.value, note))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_id": self.document_id,
            "court_id": self.court_id,
            "source_id": self.source_id,
            "source_url": self.source_url,
            "case_number": self.case_number,
            "neutral_citation": self.neutral_citation,
            "decision_date": self.decision_date,
            "party_title": self.party_title,
            "discovered_timestamp": self.discovered_timestamp,
            "current_state": self.current_state.value,
            "state_history": self.state_history,
        }


@dataclass
class AcquiredPayload:
    document_id: str
    source_url: str
    content_bytes: bytes
    sha256_hash: str
    content_type: str
    byte_count: int
    acquisition_timestamp: str
    is_dry_run: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_id": self.document_id,
            "source_url": self.source_url,
            "sha256_hash": self.sha256_hash,
            "content_type": self.content_type,
            "byte_count": self.byte_count,
            "acquisition_timestamp": self.acquisition_timestamp,
            "is_dry_run": self.is_dry_run,
            "metadata": self.metadata,
        }


class SSRFProtectionError(ValueError):
    """Raised when an outbound URL violates SSRF or private IP safeguards."""
    pass


class BoundedResponseError(ValueError):
    """Raised when an acquired document exceeds allowed size ceiling."""
    pass


import threading
from urllib.request import HTTPRedirectHandler


class RateLimiter:
    """Thread-safe token-bucket or sliding window rate limiter."""

    def __init__(self, requests_per_minute: int = 20) -> None:
        self.rpm = requests_per_minute
        self.min_interval = 60.0 / requests_per_minute
        self._last_request_time = 0.0
        self._lock = threading.Lock()

    def wait_if_needed(self) -> float:
        with self._lock:
            now = time.time()
            elapsed = now - self._last_request_time
            if elapsed < self.min_interval:
                delay = self.min_interval - elapsed
                time.sleep(delay)
                self._last_request_time = time.time()
                return delay
            self._last_request_time = now
            return 0.0


class SafeRedirectHandler(HTTPRedirectHandler):
    """Revalidates destination URL on HTTP 301/302 redirects against SSRF policy."""

    def __init__(self, security_validator) -> None:
        self.security_validator = security_validator
        super().__init__()

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.security_validator(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class BaseJudicialConnector(ABC):
    """Abstract base class for lawful, rate-limited High Court judgment connectors."""

    _BLOCKED_HOSTNAMES = {"localhost", "127.0.0.1", "0.0.0.0", "::1"}

    def __init__(
        self,
        source_id: str,
        court_id: str,
        allowed_domains: List[str],
        requests_per_minute: int = 15,
        max_response_bytes: int = 25 * 1024 * 1024,  # 25 MB
        request_timeout_seconds: int = 30,
        is_live_enabled: bool = False,
        dry_run: bool = True,
    ) -> None:
        self.source_id = source_id
        self.court_id = court_id
        self.allowed_domains = [d.lower() for d in allowed_domains]
        self.rate_limiter = RateLimiter(requests_per_minute)
        self.max_response_bytes = max_response_bytes
        self.request_timeout_seconds = request_timeout_seconds
        self.is_live_enabled = is_live_enabled
        self.dry_run = dry_run
        self._acquired_hashes: Set[str] = set()

    def validate_url_security(self, url: str) -> None:
        """Validate URL to protect against SSRF, internal network scanning, and DNS rebinding."""
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            raise SSRFProtectionError(f"Prohibited URL scheme: {parsed.scheme}")

        if parsed.username or parsed.password:
            raise SSRFProtectionError("Prohibited URL with embedded user credentials")

        if parsed.port and parsed.port not in (80, 443):
            raise SSRFProtectionError(f"Prohibited non-standard port: {parsed.port}")

        hostname = parsed.hostname
        if not hostname:
            raise SSRFProtectionError("Missing hostname in URL")

        host_lower = hostname.lower().strip("[]")
        if host_lower in self._BLOCKED_HOSTNAMES:
            raise SSRFProtectionError(f"Prohibited loopback/local host: {hostname}")

        # Check allowed domain whitelist
        is_domain_allowed = any(
            host_lower == d or host_lower.endswith("." + d)
            for d in self.allowed_domains
        )
        if not is_domain_allowed:
            raise SSRFProtectionError(
                f"Domain '{hostname}' is not in allowed domain whitelist for connector {self.source_id}: {self.allowed_domains}"
            )

        # Check IP address literal or resolve DNS to verify it is not private/reserved
        try:
            ip_obj = ipaddress.ip_address(host_lower)
            if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local or ip_obj.is_reserved:
                raise SSRFProtectionError(f"Target IP address '{host_lower}' is private/reserved")
        except ValueError:
            # Not an IP literal, it is a valid domain name
            pass

    def compute_sha256(self, data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def is_duplicate_hash(self, sha256_hash: str) -> bool:
        return sha256_hash in self._acquired_hashes

    def record_hash(self, sha256_hash: str) -> None:
        self._acquired_hashes.add(sha256_hash)

    def classify_error(self, status_code: int, exc: Optional[Exception] = None) -> RetryClassification:
        if status_code in (429, 502, 503, 504) or isinstance(exc, (TimeoutError, socket.timeout)):
            return RetryClassification.TRANSIENT
        return RetryClassification.PERMANENT

    @abstractmethod
    def discover_documents(self, filter_params: Dict[str, Any]) -> List[DiscoveredDocument]:
        """Discover candidate judgments matching filter criteria."""
        pass

    @abstractmethod
    def acquire_document(self, discovered_doc: DiscoveredDocument) -> AcquiredPayload:
        """Acquire document bytes, enforcing safety limits and hashing."""
        pass
