"""
LegalMitra Secure Acquisition Engine (Phase 35).
Implements hardened, SSRF-safe legal document acquisition with:
- Pre-request URL and DNS validation
- Safe redirect tracking (every hop validated against loopback, private IP, and cloud metadata)
- Content-type verification and maximum payload size enforcement (50 MB)
- Timeout controls and bounded exponential backoff
- Cryptographic SHA-256 verification and atomic temporary-file writes
- Quarantine of malformed or truncated responses
"""

from __future__ import annotations

import hashlib
import ipaddress
import os
import socket
import tempfile
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union
from urllib.parse import urljoin, urlparse

from legalmitra.core.logging import get_logger
from legalmitra.core.security import validate_outbound_legal_url

logger = get_logger("secure_acquisition")


class AcquisitionErrorType(str, Enum):
    NONE = "NONE"
    SSRF_BLOCKED = "SSRF_BLOCKED"
    REDIRECT_SSRF_BLOCKED = "REDIRECT_SSRF_BLOCKED"
    INVALID_SCHEME = "INVALID_SCHEME"
    DNS_RESOLUTION_FAILED = "DNS_RESOLUTION_FAILED"
    PRIVATE_IP_BLOCKED = "PRIVATE_IP_BLOCKED"
    TIMEOUT = "TIMEOUT"
    SIZE_EXCEEDED = "SIZE_EXCEEDED"
    UNSUPPORTED_CONTENT_TYPE = "UNSUPPORTED_CONTENT_TYPE"
    HTTP_ERROR = "HTTP_ERROR"
    EMPTY_OR_TRUNCATED = "EMPTY_OR_TRUNCATED"
    QUARANTINED = "QUARANTINED"
    NETWORK_FAILURE = "NETWORK_FAILURE"


@dataclass
class AcquisitionResult:
    source_url: str
    success: bool
    status_code: Optional[int] = None
    content_hash: Optional[str] = None
    byte_size: int = 0
    content_type: Optional[str] = None
    destination_ip: Optional[str] = None
    redirect_history: List[str] = field(default_factory=list)
    local_path: Optional[str] = None
    error_type: AcquisitionErrorType = AcquisitionErrorType.NONE
    error_message: Optional[str] = None
    acquired_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    retries_used: int = 0
    is_duplicate: bool = False


class SecureAcquisitionEngine:
    """
    Hardened acquisition client preventing SSRF, payload inflation, and corrupt downloads.
    """

    ALLOWED_SCHEMES: Set[str] = {"http", "https"}
    ALLOWED_CONTENT_TYPES: Set[str] = {
        "text/html",
        "text/plain",
        "application/pdf",
        "application/json",
        "application/xml",
        "text/xml",
    }
    MAX_RESPONSE_BYTES: int = 50 * 1024 * 1024  # 50 MB safety cap
    MIN_CONTENT_BYTES: int = 40  # Under 40 bytes considered empty/truncated error page
    DEFAULT_TIMEOUT_SEC: float = 30.0
    MAX_REDIRECTS: int = 5

    def __init__(
        self,
        storage_dir: Union[str, Path] = "data/09_national_corpus/raw_sources",
        quarantine_dir: Union[str, Path] = "data/09_national_corpus/quarantine",
        rate_limit_delay_sec: float = 0.5,
    ):
        self.storage_dir = Path(storage_dir)
        self.quarantine_dir = Path(quarantine_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.quarantine_dir.mkdir(parents=True, exist_ok=True)
        self.rate_limit_delay_sec = rate_limit_delay_sec
        self.last_domain_access: Dict[str, float] = {}
        self.known_hashes: Set[str] = self._index_existing_hashes()

    def _index_existing_hashes(self) -> Set[str]:
        hashes = set()
        if self.storage_dir.exists():
            for p in self.storage_dir.glob("*.*"):
                if p.is_file():
                    # If filename has hash or file exists, record
                    hashes.add(p.stem)
        return hashes

    def validate_url_and_ip(self, url: str) -> Tuple[bool, Optional[str], AcquisitionErrorType, str]:
        """
        Validate URL syntax, prohibited domains, and resolve DNS to confirm
        it does not map to loopback, private RFC1918, link-local, or cloud metadata IP.
        """
        # Step 1: Syntactic and hostname validation via core security module
        is_valid, msg = validate_outbound_legal_url(url, allowed_schemes=tuple(self.ALLOWED_SCHEMES))
        if not is_valid:
            if "Unsupported URL scheme" in msg:
                return False, None, AcquisitionErrorType.INVALID_SCHEME, msg
            return False, None, AcquisitionErrorType.SSRF_BLOCKED, msg

        # Step 2: DNS Resolution and IP Destination Check
        parsed = urlparse(url)
        hostname = parsed.hostname
        if not hostname:
            return False, None, AcquisitionErrorType.SSRF_BLOCKED, "Missing hostname"

        try:
            # Resolve all IPv4 addresses
            addr_info = socket.getaddrinfo(hostname, None, socket.AF_INET, socket.SOCK_STREAM)
            resolved_ips = {item[4][0] for item in addr_info}
        except socket.gaierror as e:
            return False, None, AcquisitionErrorType.DNS_RESOLUTION_FAILED, f"DNS resolution failed: {e}"

        for ip_str in resolved_ips:
            try:
                ip_obj = ipaddress.ip_address(ip_str)
                if (
                    ip_obj.is_loopback
                    or ip_obj.is_private
                    or ip_obj.is_link_local
                    or ip_obj.is_multicast
                    or ip_obj.is_reserved
                    or ip_str == "169.254.169.254"
                ):
                    return (
                        False,
                        ip_str,
                        AcquisitionErrorType.PRIVATE_IP_BLOCKED,
                        f"Resolved IP {ip_str} falls into prohibited address space",
                    )
            except ValueError:
                return False, ip_str, AcquisitionErrorType.DNS_RESOLUTION_FAILED, f"Invalid resolved IP: {ip_str}"

        destination_ip = next(iter(resolved_ips)) if resolved_ips else None
        return True, destination_ip, AcquisitionErrorType.NONE, "OK"

    def _apply_rate_limit(self, domain: str) -> None:
        last_time = self.last_domain_access.get(domain, 0.0)
        elapsed = time.time() - last_time
        if elapsed < self.rate_limit_delay_sec:
            time.sleep(self.rate_limit_delay_sec - elapsed)
        self.last_domain_access[domain] = time.time()

    def acquire_document(
        self,
        url: str,
        expected_content_type: Optional[str] = None,
        max_retries: int = 3,
        source_id: Optional[str] = None,
    ) -> AcquisitionResult:
        """
        Safely acquire a legal document.
        Validates URL, follows redirects safely, checks size limits, hashes content,
        and saves atomically.
        """
        current_url = url
        redirect_chain: List[str] = []
        retries = 0

        # Step 1: Initial URL and IP validation
        is_ok, dest_ip, err_type, err_msg = self.validate_url_and_ip(current_url)
        if not is_ok:
            logger.warning(f"Acquisition blocked for {url}: {err_msg} ({err_type.value})")
            return AcquisitionResult(
                source_url=url,
                success=False,
                error_type=err_type,
                error_message=err_msg,
            )

        # Domain rate limiting
        domain = urlparse(url).netloc
        self._apply_rate_limit(domain)

        # In local/offline or test mode, handle local file/fixtures or network safely
        # Note: If target URL starts with test:// or file:// fixture, handle safely
        parsed = urlparse(url)
        if parsed.scheme == "file":
            return self._acquire_local_file(parsed.path, url, source_id)

        # Simulate or perform controlled acquisition with socket/requests
        # Using urllib.request with custom redirect handler that checks each hop
        import urllib.request
        import urllib.error

        class SafeRedirectHandler(urllib.request.HTTPRedirectHandler):
            def __init__(self, engine: SecureAcquisitionEngine):
                super().__init__()
                self.engine = engine
                self.redirect_count = 0

            def redirect_request(self, req, fp, code, msg, headers, newurl):
                self.redirect_count += 1
                if self.redirect_count > SecureAcquisitionEngine.MAX_REDIRECTS:
                    raise urllib.error.HTTPError(
                        req.full_url, code, "Maximum redirect limit exceeded", headers, fp
                    )
                # Absolute redirect resolution
                resolved_url = urljoin(req.full_url, newurl)
                # Validate redirect target against SSRF!
                is_safe, _, redirect_err, err_detail = self.engine.validate_url_and_ip(resolved_url)
                if not is_safe:
                    raise urllib.error.HTTPError(
                        resolved_url, 403, f"SSRF redirect blocked: {err_detail}", headers, fp
                    )
                redirect_chain.append(resolved_url)
                return super().redirect_request(req, fp, code, msg, headers, newurl)

        opener = urllib.request.build_opener(SafeRedirectHandler(self))
        headers = {
            "User-Agent": "LegalMitra-CorpusEngine/1.0 (+https://github.com/DebugDroid-15/LegalMitra)",
            "Accept": "text/html,application/pdf,application/json,text/plain",
        }

        while retries <= max_retries:
            try:
                req = urllib.request.Request(current_url, headers=headers)
                with opener.open(req, timeout=self.DEFAULT_TIMEOUT_SEC) as response:
                    status_code = response.getcode()
                    content_type = response.info().get_content_type()

                    # Validate Content-Type
                    if content_type not in self.ALLOWED_CONTENT_TYPES:
                        return AcquisitionResult(
                            source_url=url,
                            success=False,
                            status_code=status_code,
                            content_type=content_type,
                            destination_ip=dest_ip,
                            redirect_history=redirect_chain,
                            error_type=AcquisitionErrorType.UNSUPPORTED_CONTENT_TYPE,
                            error_message=f"Unsupported content type: {content_type}",
                            retries_used=retries,
                        )

                    # Stream download with size cap
                    hasher = hashlib.sha256()
                    total_bytes = 0
                    temp_fd, temp_path_str = tempfile.mkstemp(prefix="lm_acq_", dir=str(self.storage_dir))
                    temp_path = Path(temp_path_str)

                    with os.fdopen(temp_fd, "wb") as f_out:
                        while True:
                            chunk = response.read(65536)
                            if not chunk:
                                break
                            total_bytes += len(chunk)
                            if total_bytes > self.MAX_RESPONSE_BYTES:
                                f_out.close()
                                if temp_path.exists():
                                    temp_path.unlink()
                                return AcquisitionResult(
                                    source_url=url,
                                    success=False,
                                    status_code=status_code,
                                    destination_ip=dest_ip,
                                    error_type=AcquisitionErrorType.SIZE_EXCEEDED,
                                    error_message=f"Response exceeded size limit {self.MAX_RESPONSE_BYTES} bytes",
                                    retries_used=retries,
                                )
                            hasher.update(chunk)
                            f_out.write(chunk)

                    # Check for empty or truncated content
                    if total_bytes < self.MIN_CONTENT_BYTES:
                        # Move to quarantine
                        quarantine_target = self.quarantine_dir / f"truncated_{int(time.time())}_{temp_path.name}"
                        temp_path.replace(quarantine_target)
                        return AcquisitionResult(
                            source_url=url,
                            success=False,
                            status_code=status_code,
                            destination_ip=dest_ip,
                            byte_size=total_bytes,
                            error_type=AcquisitionErrorType.EMPTY_OR_TRUNCATED,
                            error_message=f"Response too small ({total_bytes} bytes). Moved to quarantine: {quarantine_target.name}",
                            retries_used=retries,
                        )

                    content_hash = hasher.hexdigest()
                    ext = ".pdf" if "pdf" in content_type else ".html" if "html" in content_type else ".txt"
                    filename = f"{source_id or 'doc'}_{content_hash[:16]}{ext}"
                    final_path = self.storage_dir / filename

                    # Deduplication check
                    is_dup = content_hash in self.known_hashes or final_path.exists()
                    if not is_dup:
                        temp_path.replace(final_path)
                        self.known_hashes.add(content_hash)
                    else:
                        temp_path.unlink()

                    return AcquisitionResult(
                        source_url=url,
                        success=True,
                        status_code=status_code,
                        content_hash=content_hash,
                        byte_size=total_bytes,
                        content_type=content_type,
                        destination_ip=dest_ip,
                        redirect_history=redirect_chain,
                        local_path=str(final_path),
                        retries_used=retries,
                        is_duplicate=is_dup,
                    )

            except urllib.error.HTTPError as e:
                if "SSRF redirect blocked" in str(e):
                    return AcquisitionResult(
                        source_url=url,
                        success=False,
                        status_code=e.code,
                        redirect_history=redirect_chain,
                        error_type=AcquisitionErrorType.REDIRECT_SSRF_BLOCKED,
                        error_message=str(e),
                    )
                retries += 1
                if retries > max_retries or (400 <= e.code < 500 and e.code != 429):
                    return AcquisitionResult(
                        source_url=url,
                        success=False,
                        status_code=e.code,
                        destination_ip=dest_ip,
                        redirect_history=redirect_chain,
                        error_type=AcquisitionErrorType.HTTP_ERROR,
                        error_message=f"HTTP Error {e.code}: {e.reason}",
                        retries_used=retries,
                    )
                time.sleep(min(8.0, 0.5 * (2 ** retries)))

            except (socket.timeout, urllib.error.URLError) as e:
                retries += 1
                if retries > max_retries:
                    err_cls = AcquisitionErrorType.TIMEOUT if isinstance(e, socket.timeout) else AcquisitionErrorType.NETWORK_FAILURE
                    return AcquisitionResult(
                        source_url=url,
                        success=False,
                        destination_ip=dest_ip,
                        redirect_history=redirect_chain,
                        error_type=err_cls,
                        error_message=f"Network error: {e}",
                        retries_used=retries,
                    )
                time.sleep(min(8.0, 0.5 * (2 ** retries)))

        return AcquisitionResult(
            source_url=url,
            success=False,
            error_type=AcquisitionErrorType.NETWORK_FAILURE,
            error_message="Retries exhausted",
            retries_used=retries,
        )

    def _acquire_local_file(self, file_path_str: str, original_url: str, source_id: Optional[str]) -> AcquisitionResult:
        file_path = Path(file_path_str.lstrip("/"))
        if not file_path.exists():
            return AcquisitionResult(
                source_url=original_url,
                success=False,
                error_type=AcquisitionErrorType.HTTP_ERROR,
                error_message=f"Local file fixture does not exist: {file_path}",
            )
        data = file_path.read_bytes()
        byte_size = len(data)
        if byte_size < self.MIN_CONTENT_BYTES:
            return AcquisitionResult(
                source_url=original_url,
                success=False,
                byte_size=byte_size,
                error_type=AcquisitionErrorType.EMPTY_OR_TRUNCATED,
                error_message=f"Local file too small: {byte_size} bytes",
            )
        h = hashlib.sha256(data).hexdigest()
        ext = file_path.suffix or ".txt"
        dest = self.storage_dir / f"{source_id or 'doc'}_{h[:16]}{ext}"
        if not dest.exists():
            dest.write_bytes(data)
            self.known_hashes.add(h)
        return AcquisitionResult(
            source_url=original_url,
            success=True,
            status_code=200,
            content_hash=h,
            byte_size=byte_size,
            content_type="text/plain" if ext == ".txt" else "application/pdf" if ext == ".pdf" else "text/html",
            local_path=str(dest),
            is_duplicate=h in self.known_hashes,
        )

