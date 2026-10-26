"""
LegalMitra Structured Logging with Production Security Redaction (Phase 65)
Provides high-performance structured logging with automated redactors for
PII, API keys, Bearer tokens, passwords, JWTs, and database credentials.
"""

import logging
import re
import sys
from typing import Any, Dict, List, Optional, Pattern, Tuple, Union


class SensitiveDataRedactor:
    """
    Production-grade regex sanitizer that redacts credentials, secrets,
    and personally identifiable information (PII) before log emission.
    """

    REDACTION_PATTERNS: List[Tuple[Pattern, str]] = [
        # Bearer tokens
        (re.compile(r"(?i)\b(bearer\s+)([a-zA-Z0-9_\-\.]{10,})\b"), r"\1[REDACTED_TOKEN]"),
        # API Keys, secrets, tokens
        (
            re.compile(
                r"(?i)\b((?:api[_-]?key|access[_-]?token|secret[_-]?key|client[_-]?secret|private[_-]?key)\s*[:=]\s*['\"]?)([a-zA-Z0-9_\-\.]{8,})(['\"]?)",
            ),
            r"\1[REDACTED_SECRET]\3",
        ),
        # Passwords
        (
            re.compile(
                r"(?i)\b((?:password|passwd|pwd)\s*[:=]\s*['\"]?)([^'\"\s]{4,})(['\"]?)",
            ),
            r"\1[REDACTED_PASSWORD]\3",
        ),
        # Database URIs with credentials
        (
            re.compile(
                r"(?i)\b((?:postgresql|postgres|mysql|sqlite|mongodb)://[^:]+:)([^@\s]+)(@)",
            ),
            r"\1[REDACTED_CREDENTIALS]\3",
        ),
        # JWT tokens
        (
            re.compile(r"\beyJ[a-zA-Z0-9_\-]+\.eyJ[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+\b"),
            "[REDACTED_JWT]",
        ),
        # Email addresses
        (
            re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,24}\b"),
            "[REDACTED_EMAIL]",
        ),
        # Indian 10-digit mobile numbers
        (
            re.compile(r"\b(?:\+91[\-\s]?)?[6-9]\d{9}\b"),
            "[REDACTED_PHONE]",
        ),
        # 12-digit Aadhaar numbers
        (
            re.compile(r"\b\d{4}\s\d{4}\s\d{4}\b"),
            "[REDACTED_AADHAAR]",
        ),
    ]

    @classmethod
    def redact(cls, text: str) -> str:
        """Apply all redaction rules to input text."""
        if not text:
            return text
        sanitized = str(text)
        for pattern, replacement in cls.REDACTION_PATTERNS:
            sanitized = pattern.sub(replacement, sanitized)
        return sanitized


def redact_sensitive_text(text: str) -> str:
    """Public utility to redact sensitive credentials and PII."""
    return SensitiveDataRedactor.redact(text)


class RedactingFilter(logging.Filter):
    """
    Logging filter that redacts sensitive information from log records.
    Intercepts record message, args, and formatted representations.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = SensitiveDataRedactor.redact(record.msg)
        if record.args:
            if isinstance(record.args, dict):
                record.args = {
                    k: SensitiveDataRedactor.redact(str(v)) if isinstance(v, str) else v
                    for k, v in record.args.items()
                }
            elif isinstance(record.args, (list, tuple)):
                record.args = tuple(
                    SensitiveDataRedactor.redact(str(a)) if isinstance(a, str) else a
                    for a in record.args
                )
        return True


def get_logger(name: str = "legalmitra", level: Optional[int] = None) -> logging.Logger:
    """
    Returns a configured logger instance with structured formatting and automated redaction.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s:%(funcName)s:%(lineno)d] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        handler.addFilter(RedactingFilter())
        logger.addHandler(handler)
        logger.setLevel(level or logging.INFO)
    elif level is not None:
        logger.setLevel(level)

    for h in logger.handlers:
        if not any(isinstance(f, RedactingFilter) for f in h.filters):
            h.addFilter(RedactingFilter())

    return logger
