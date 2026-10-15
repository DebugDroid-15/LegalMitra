"""
LegalMitra Core Module
"""

from legalmitra.core.enums import (
    CourtType,
    Jurisdiction,
    LegalReviewStatus,
    ProcessingStatus,
    SourceType,
    SplitType,
)
from legalmitra.core.errors import (
    DuplicateDocumentError,
    ExtractionError,
    GroundingValidationError,
    LegalMitraError,
    NormalizationError,
    SchemaValidationError,
    SourceRegistryError,
    UnsupportedDocumentError,
)
from legalmitra.core.hashing import (
    compute_content_fingerprint,
    compute_file_sha256,
    compute_text_sha256,
)
from legalmitra.core.logging import get_logger

__all__ = [
    "SourceType",
    "Jurisdiction",
    "CourtType",
    "LegalReviewStatus",
    "ProcessingStatus",
    "SplitType",
    "LegalMitraError",
    "SourceRegistryError",
    "DuplicateDocumentError",
    "ExtractionError",
    "UnsupportedDocumentError",
    "NormalizationError",
    "SchemaValidationError",
    "GroundingValidationError",
    "compute_file_sha256",
    "compute_text_sha256",
    "compute_content_fingerprint",
    "get_logger",
]

