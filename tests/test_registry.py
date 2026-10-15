"""
Tests for LegalMitra Source Registry Manager and Document Ingestor.
"""

from datetime import date
from pathlib import Path
import pytest

from legalmitra.core.enums import CourtType, Jurisdiction, LegalReviewStatus, ProcessingStatus, SourceType
from legalmitra.core.errors import DuplicateDocumentError
from legalmitra.ingestion.ingestor import DocumentIngestor
from legalmitra.ingestion.registry import SourceRegistryManager
from legalmitra.schemas.registry import SourceRegistryRecord


def test_registry_empty_init(temp_env_dir):
    mgr = SourceRegistryManager(temp_env_dir["registry_file"])
    assert len(mgr) == 0
    assert mgr.list_all() == []


def test_registry_register_and_get(temp_env_dir, sample_registry_record):
    mgr = SourceRegistryManager(temp_env_dir["registry_file"])
    mgr.register(sample_registry_record)
    assert len(mgr) == 1

    fetched = mgr.get(sample_registry_record.document_id)
    assert fetched is not None
    assert fetched.document_id == sample_registry_record.document_id
    assert fetched.checksum == sample_registry_record.checksum


def test_registry_deduplication_by_id(temp_env_dir, sample_registry_record):
    mgr = SourceRegistryManager(temp_env_dir["registry_file"])
    mgr.register(sample_registry_record)

    # Attempt duplicate ID registration
    with pytest.raises(DuplicateDocumentError):
        mgr.register(sample_registry_record)


def test_registry_deduplication_by_checksum(temp_env_dir, sample_registry_record):
    mgr = SourceRegistryManager(temp_env_dir["registry_file"])
    mgr.register(sample_registry_record)

    # Attempt registration with different ID but same checksum
    dup_record = sample_registry_record.model_copy(update={"document_id": "ANOTHER-DOC-ID"})
    with pytest.raises(DuplicateDocumentError):
        mgr.register(dup_record)


def test_registry_status_update(temp_env_dir, sample_registry_record):
    mgr = SourceRegistryManager(temp_env_dir["registry_file"])
    mgr.register(sample_registry_record)

    updated = mgr.update_status(
        document_id=sample_registry_record.document_id,
        processing_status=ProcessingStatus.EXTRACTED,
        verification_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
    )
    assert updated.processing_status == ProcessingStatus.EXTRACTED
    assert updated.verification_status == LegalReviewStatus.PENDING_LEGAL_REVIEW

    # Re-instantiate manager to verify persistence
    reloaded_mgr = SourceRegistryManager(temp_env_dir["registry_file"])
    reloaded = reloaded_mgr.get(sample_registry_record.document_id)
    assert reloaded.processing_status == ProcessingStatus.EXTRACTED
    assert reloaded.verification_status == LegalReviewStatus.PENDING_LEGAL_REVIEW


def test_document_ingestor_flow(temp_env_dir):
    mgr = SourceRegistryManager(temp_env_dir["registry_file"])
    ingestor = DocumentIngestor(mgr, temp_env_dir["raw_dir"])

    # Create dummy source file
    src_file = temp_env_dir["root"] / "input_statute.txt"
    src_file.write_text("Section 1. Short title, extent and commencement.", encoding="utf-8")

    record = ingestor.ingest_document(
        file_path=src_file,
        document_id="IND-STAT-TEST-INGEST",
        title="Test Ingestion Statute",
        source_url="https://indiacode.nic.in/test",
        source_type=SourceType.STATUTE,
        document_date=date(2023, 1, 1),
        licence_or_terms="GODL-India",
    )

    assert record.document_id == "IND-STAT-TEST-INGEST"
    assert Path(record.raw_file_path).exists()
    assert record.byte_size > 0
    assert len(mgr) == 1

