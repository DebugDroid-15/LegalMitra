"""
LegalMitra Source Registry Schema
Defines the Pydantic schema for tracking legally sourced documents with full provenance,
licensing, cryptographic checksums, and explicit verification status.
"""

from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
import re

from legalmitra.core.enums import CourtType, Jurisdiction, LegalReviewStatus, ProcessingStatus, SourceType


class SourceRegistryRecord(BaseModel):
    """
    Metadata record for every ingested legal source document.
    Ensures strict provenance, authenticity, and legal review tracking.
    """
    document_id: str = Field(
        ...,
        description="Unique identifier (e.g. IND-STAT-BSA-2023-SEC61, IND-JUD-SC-2017-PUTTASWAMY)",
        min_length=3,
        max_length=128
    )
    title: str = Field(
        ...,
        description="Official title of the statute, notification, or judgment",
        min_length=3,
        max_length=512
    )
    source_url: str = Field(
        ...,
        description="Canonical URL of the official repository (e.g., India Code, e-Courts, Supreme Court portal)"
    )
    source_type: SourceType = Field(
        ...,
        description="Type of legal document (statute, judgment, notification, etc.)"
    )
    jurisdiction: Jurisdiction = Field(
        default=Jurisdiction.INDIA_CENTRAL,
        description="Legal jurisdiction (e.g. IN for Union, IN-DL for Delhi)"
    )
    court: Optional[CourtType] = Field(
        default=CourtType.NONE,
        description="Court that delivered the judgment, or NONE for statutes"
    )
    document_date: date = Field(
        ...,
        description="Date of enactment, notification, or judgment delivery (YYYY-MM-DD)"
    )
    effective_date: Optional[date] = Field(
        default=None,
        description="Date when statute/amendment came into legal force, where applicable"
    )
    retrieval_timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="ISO 8601 UTC timestamp of document ingestion"
    )
    version: str = Field(
        default="1.0.0",
        description="Version or amendment iteration of the source document"
    )
    licence_or_terms: str = Field(
        ...,
        description="Licence or access terms (e.g., 'GODL-India (Government Open Data License)', 'Public Domain / Official Gazette')",
        min_length=3
    )
    checksum: str = Field(
        ...,
        description="Cryptographic SHA-256 hex digest of the raw document file",
        min_length=64,
        max_length=64
    )
    verification_status: LegalReviewStatus = Field(
        default=LegalReviewStatus.UNVERIFIED_AUTOMATED,
        description="Explicit status of legal review. Automated check never equals legal correctness."
    )
    processing_status: ProcessingStatus = Field(
        default=ProcessingStatus.REGISTERED,
        description="Pipeline processing state (registered, extracted, normalized, validated, failed)"
    )
    raw_file_path: str = Field(
        ...,
        description="Relative or absolute path to the stored raw file"
    )
    file_format: str = Field(
        ...,
        description="MIME type or file extension (e.g., '.pdf', '.docx', '.html', '.txt')"
    )
    byte_size: int = Field(
        ...,
        ge=0,
        description="File size in bytes"
    )
    privacy_redaction_notes: Optional[str] = Field(
        default=None,
        description="Notes on compliance with statutory redaction rules (e.g. POCSO s.33(7), JJ Act s.74)"
    )
    error_log: Optional[str] = Field(
        default=None,
        description="Recorded errors if extraction or normalization failed"
    )

    @field_validator("checksum")
    @classmethod
    def validate_checksum(cls, v: str) -> str:
        if not re.fullmatch(r"[0-9a-fA-F]{64}", v):
            raise ValueError("Checksum must be a valid 64-character SHA-256 hexadecimal string")
        return v.lower()

    @field_validator("document_id")
    @classmethod
    def validate_document_id(cls, v: str) -> str:
        if not re.fullmatch(r"^[A-Za-z0-9_\-\.]+$", v):
            raise ValueError("document_id must contain only alphanumeric characters, underscores, hyphens, and periods")
        return v

