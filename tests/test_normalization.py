"""
Tests for LegalMitra Statutory and Judgment Normalizers.
"""

from datetime import date
from pathlib import Path
import pytest

from legalmitra.core.enums import CourtType, Jurisdiction, LegalReviewStatus, SourceType
from legalmitra.extraction.text_extractor import TextExtractor
from legalmitra.normalization.judgment_normalizer import JudgmentNormalizer
from legalmitra.normalization.normalizer import DocumentNormalizer
from legalmitra.normalization.statute_normalizer import StatuteNormalizer
from legalmitra.schemas.registry import SourceRegistryRecord


def test_statute_normalizer_bsa_s61():
    normalizer = StatuteNormalizer()
    extractor = TextExtractor()

    sample_path = Path("corpus/sample_statute_bsa_s61.txt")
    extraction = extractor.extract(sample_path, "TEST-BSA-S61")

    record = SourceRegistryRecord(
        document_id="IND-STAT-BSA-2023-SEC61",
        title="Bharatiya Sakshya Adhiniyam, 2023 - Section 61",
        source_url="https://indiacode.nic.in/handle/123456789/20000",
        source_type=SourceType.STATUTE,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        document_date=date(2023, 12, 25),
        effective_date=date(2024, 7, 1),
        licence_or_terms="GODL-India",
        checksum="0" * 64,
        raw_file_path=str(sample_path),
        file_format=".txt",
        byte_size=500,
    )

    doc = normalizer.normalize(extraction, record)
    assert doc.act_title == record.title
    assert len(doc.sections) >= 1

    sec = doc.sections[0]
    assert sec.section_number == "61"
    assert "Admissibility of electronic records" in sec.section_title
    assert "Nothing in this Adhiniyam shall apply to deny the admissibility" in sec.full_verbatim_text
    assert len(sec.provisos) >= 1
    assert "section 63" in sec.provisos[0].text
    assert len(sec.explanations) >= 1
    assert "Information Technology Act, 2000" in sec.explanations[0].text


def test_judgment_normalizer_puttaswamy():
    normalizer = JudgmentNormalizer()
    extractor = TextExtractor()

    sample_path = Path("corpus/sample_judgment_sc_privacy.txt")
    extraction = extractor.extract(sample_path, "TEST-PUTTASWAMY")

    record = SourceRegistryRecord(
        document_id="IND-SC-2017-PUTTASWAMY",
        title="Justice K.S. Puttaswamy (Retd.) v. Union of India",
        source_url="https://main.sci.gov.in/judgments",
        source_type=SourceType.JUDGMENT,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        court=CourtType.SUPREME_COURT,
        document_date=date(2017, 8, 24),
        licence_or_terms="Public Domain / Court Records",
        checksum="1" * 64,
        raw_file_path=str(sample_path),
        file_format=".txt",
        byte_size=1200,
    )

    doc = normalizer.normalize(extraction, record)
    assert doc.court == CourtType.SUPREME_COURT
    assert len(doc.bench_coram) >= 2
    assert any("Khehar" in j for j in doc.bench_coram)
    assert any("Chandrachud" in j for j in doc.bench_coram)
    assert len(doc.citations) >= 1
    assert any("SCC" in c.citation_text for c in doc.citations)
    assert len(doc.paragraphs) >= 4
    assert doc.paragraphs[0].paragraph_number == 1
    assert "right to privacy" in doc.ratio_decidendi.lower()


def test_document_normalizer_persists_json(temp_env_dir):
    extractor = TextExtractor()
    sample_path = Path("corpus/sample_statute_bsa_s61.txt")
    extraction = extractor.extract(sample_path, "TEST-BSA-S61")

    record = SourceRegistryRecord(
        document_id="IND-STAT-BSA-2023-SEC61",
        title="Bharatiya Sakshya Adhiniyam, 2023",
        source_url="https://indiacode.nic.in/handle/123456789/20000",
        source_type=SourceType.STATUTE,
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        document_date=date(2023, 12, 25),
        licence_or_terms="GODL-India",
        checksum="2" * 64,
        raw_file_path=str(sample_path),
        file_format=".txt",
        byte_size=500,
    )

    doc_norm = DocumentNormalizer(temp_env_dir["norm_dir"])
    model = doc_norm.normalize(extraction, record)

    output_json = temp_env_dir["norm_dir"] / f"{record.document_id}.json"
    assert output_json.exists()
    assert output_json.stat().st_size > 0

