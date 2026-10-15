"""
LegalMitra Hashing Utilities
Provides cryptographic and semantic content hashes for deduplication and provenance tracking.
"""

import hashlib
import re
from pathlib import Path
from typing import Union


def compute_file_sha256(file_path: Union[str, Path], chunk_size: int = 65536) -> str:
    """
    Computes standard SHA-256 hex digest for a file.
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    hasher = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()


def compute_text_sha256(text: str) -> str:
    """
    Computes SHA-256 hex digest for an arbitrary string.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def compute_content_fingerprint(text: str) -> str:
    """
    Computes a normalized content fingerprint to detect near-duplicate legal provisions
    despite minor spacing or case differences.
    """
    normalized = re.sub(r"\s+", " ", text).strip().lower()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

