"""
LegalMitra Document Ingestor
Ingests legally sourced documents into raw storage, computes SHA-256 provenance hashes,
and creates tracked entries in the Source Registry.
"""

import shutil
from datetime import date
from pathlib import Path
from typing import Optional, Union

from legalmitra.core.enums import CourtType, Jurisdiction, LegalReviewStatus, ProcessingStatus, SourceType
from legalmitra.core.errors import DuplicateDocumentError, UnsupportedDocumentError
from legalmitra.core.hashing import compute_file_sha256
from legalmitra.core.logging import get_logger
from legalmitra.ingestion.registry import SourceRegistryManager
from legalmitra.schemas.registry import SourceRegistryRecord

logger = get_logger("document_ingestor")


class DocumentIngestor:
    """
    Ingests source legal documents into raw data storage and source registry.
    """

    def __init__(self, registry_manager: SourceRegistryManager, raw_storage_dir: Union[str, Path]):
        self.registry = registry_manager
        self.raw_storage_dir = Path(raw_storage_dir)
        self.raw_storage_dir.mkdir(parents=True, exist_ok=True)

    def ingest_document(
        self,
        file_path: Union[str, Path],
        document_id: str,
        title: str,
        source_url: str,
        source_type: SourceType,
        document_date: date,
        licence_or_terms: str,
        jurisdiction: Jurisdiction = Jurisdiction.INDIA_CENTRAL,
        court: Optional[CourtType] = None,
        effective_date: Optional[date] = None,
        version: str = "1.0.0",
        privacy_redaction_notes: Optional[str] = None,
        force_replace: bool = False,
    ) -> SourceRegistryRecord:
        """
        Ingests a source file into data/01_raw, hashes its content, and registers it.
        """
        source_path = Path(file_path).resolve()
        if not source_path.is_file():
            raise FileNotFoundError(f"Source file does not exist: {source_path}")

        file_extension = source_path.suffix.lower()
        if not file_extension:
            raise UnsupportedDocumentError(f"File {source_path.name} lacks a valid extension.")

        checksum = compute_file_sha256(source_path)
        byte_size = source_path.stat().st_size

        # Check deduplication
        existing = self.registry.get_by_checksum(checksum)
        if existing and not force_replace:
            if existing.document_id == document_id:
                logger.info(f"Document '{document_id}' already registered with checksum {checksum}.")
                return existing
            raise DuplicateDocumentError(
                f"File content matches registered document '{existing.document_id}' with checksum {checksum}."
            )

        # Destination path in data/01_raw
        dest_filename = f"{document_id}{file_extension}"
        dest_path = (self.raw_storage_dir / dest_filename).resolve()

        if source_path != dest_path:
            shutil.copy2(source_path, dest_path)

        record = SourceRegistryRecord(
            document_id=document_id,
            title=title,
            source_url=source_url,
            source_type=source_type,
            jurisdiction=jurisdiction or Jurisdiction.INDIA_CENTRAL,
            court=court or (CourtType.NONE if source_type == SourceType.STATUTE else CourtType.SUPREME_COURT),
            document_date=document_date,
            effective_date=effective_date,
            version=version,
            licence_or_terms=licence_or_terms,
            checksum=checksum,
            verification_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
            processing_status=ProcessingStatus.REGISTERED,
            raw_file_path=str(dest_path),
            file_format=file_extension,
            byte_size=byte_size,
            privacy_redaction_notes=privacy_redaction_notes,
        )

        return self.registry.register(record, allow_duplicate_checksum=force_replace)
