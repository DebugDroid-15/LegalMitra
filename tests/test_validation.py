"""
Tests for LegalMitra Schema Validation.
"""

from datetime import date
import pytest

from legalmitra.core.enums import LegalReviewStatus, SourceType
from legalmitra.core.errors import SchemaValidationError
from legalmitra.schemas.registry import SourceRegistryRecord
from legalmitra.validation.pydantic_validator import SchemaValidator


def test_schema_validator_success():
    data = {
        "document_id": "IND-STAT-VALID-001",
        "title": "Valid Statute Title",
        "source_url": "https://indiacode.nic.in/valid",
        "source_type": SourceType.STATUTE.value,
        "document_date": "2023-12-25",
        "licence_or_terms": "GODL-India",
        "checksum": "f" * 64,
        "raw_file_path": "/tmp/valid.txt",
        "file_format": ".txt",
        "byte_size": 2048,
        "verification_status": LegalReviewStatus.UNVERIFIED_AUTOMATED.value,
    }

    is_valid, model, err = SchemaValidator.validate(SourceRegistryRecord, data)
    assert is_valid is True
    assert err is None
    assert isinstance(model, SourceRegistryRecord)


def test_schema_validator_failure():
    invalid_data = {
        "document_id": "BAD ID WITH SPACES",
        "checksum": "short",
    }
    is_valid, model, err = SchemaValidator.validate(SourceRegistryRecord, invalid_data)
    assert is_valid is False
    assert model is None
    assert err is not None


def test_schema_validator_validate_or_raise():
    invalid_data = {"document_id": "BAD"}
    with pytest.raises(SchemaValidationError):
        SchemaValidator.validate_or_raise(SourceRegistryRecord, invalid_data)

