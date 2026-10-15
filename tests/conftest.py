"""
Pytest configuration and shared fixtures for LegalMitra test suite.
"""

from datetime import date
from pathlib import Path
import pytest
import shutil
import tempfile

from legalmitra.core.enums import CourtType, Jurisdiction, LegalReviewStatus, SourceType
from legalmitra.ingestion.registry import SourceRegistryManager
from legalmitra.schemas.registry import SourceRegistryRecord


@pytest.fixture
def temp_env_dir():
    """Provides an isolated temporary directory tree for testing pipeline runs."""
    temp_dir = Path(tempfile.mkdtemp(prefix="legalmitra_test_"))
    raw_dir = temp_dir / "01_raw"
    norm_dir = temp_dir / "02_normalized"
    reg_file = temp_dir / "registry" / "source_registry.jsonl"

    raw_dir.mkdir(parents=True)
    norm_dir.mkdir(parents=True)
    reg_file.parent.mkdir(parents=True)

    yield {
        "root": temp_dir,
        "raw_dir": raw_dir,
        "norm_dir": norm_dir,
        "registry_file": reg_file,
    }

    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_registry_record(temp_env_dir):
    """Provides a sample SourceRegistryRecord for testing."""
    return SourceRegistryRecord(
        document_id="IND-STAT-BSA-2023-SEC61",
        title="Bharatiya Sakshya Adhiniyam, 2023 - Section 61",
        source_url="https://www.indiacode.nic.in/handle/123456789/20000",
        source_type=SourceType.STATUTE,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        court=CourtType.NONE,
        document_date=date(2023, 12, 25),
        effective_date=date(2024, 7, 1),
        licence_or_terms="Government of India Open Data License (GODL-India)",
        checksum="a" * 64,
        verification_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
        raw_file_path=str(temp_env_dir["raw_dir"] / "IND-STAT-BSA-2023-SEC61.txt"),
        file_format=".txt",
        byte_size=1024,
    )

