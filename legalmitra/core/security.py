"""
LegalMitra Security & Trust Boundary Utilities
Provides outbound URL validation, SSRF protection, sanitization, and cryptographic guards.
"""

from __future__ import annotations

import ipaddress
import re
from typing import Sequence, Tuple
from urllib.parse import urlparse

from legalmitra.core.logging import get_logger

logger = get_logger("security_core")


def validate_outbound_legal_url(
    url: str,
    allowed_schemes: Sequence[str] = ("http", "https")
) -> Tuple[bool, str]:
    """
    Validate outbound legal repository URLs against Server-Side Request Forgery (SSRF),
    loopback addresses, private networks, cloud metadata endpoints, and non-HTTP schemes.
    """
    if not url or not isinstance(url, str):
        return False, "URL cannot be empty"

    url_clean = url.strip()
    try:
        parsed = urlparse(url_clean)
    except Exception as e:
        return False, f"Malformed URL syntax: {e}"

    if parsed.scheme.lower() not in allowed_schemes:
        return False, f"Unsupported URL scheme: {parsed.scheme}"

    hostname = parsed.hostname
    if not hostname:
        return False, "Missing hostname in URL"

    hostname_lower = hostname.lower()

    # Blocked named hosts (cloud metadata, loopback hostnames, k8s internal)
    prohibited_hosts = {
        "localhost",
        "metadata.google.internal",
        "instance-data",
        "169.254.169.254",
        "metadata",
        "kubernetes.default",
        "kubernetes.default.svc",
    }
    if hostname_lower in prohibited_hosts:
        return False, f"Prohibited destination host: {hostname}"

    # Check IP addresses directly
    try:
        ip = ipaddress.ip_address(hostname_lower)
        if ip.is_loopback:
            return False, "Loopback IP addresses prohibited"
        if ip.is_private:
            return False, "Private network IP addresses prohibited"
        if ip.is_link_local:
            return False, "Link-local IP addresses prohibited"
        if ip.is_multicast:
            return False, "Multicast IP addresses prohibited"
        if ip.is_reserved:
            return False, "Reserved IP addresses prohibited"
    except ValueError:
        # Not an IP literal; domain name resolution is governed by OS DNS
        pass

    return True, "OK"


def sanitize_redact_sensitive_text(text: str) -> str:
    """
    Scrub common secret patterns, phone numbers, and private credentials
    from error logs and diagnostic strings.
    """
    if not text:
        return ""
    # Redact Authorization Bearer tokens
    cleaned = re.sub(r"(Bearer\s+)[A-Za-z0-9_\-\.]{12,}", r"\1[REDACTED_TOKEN]", text, flags=re.IGNORECASE)
    # Redact AWS / API keys
    cleaned = re.sub(r"(AKIA[0-9A-Z]{16})", r"[REDACTED_KEY]", cleaned)
    # Redact 10-digit Indian mobile numbers preceded by contact indicators
    cleaned = re.sub(r"(\b(?:\+?91[\-\s]?)?[6-9]\d{9}\b)", r"[REDACTED_PHONE]", cleaned)
    return cleaned

