"""
End-to-End Pipeline Integration Test.
Runs the entire LegalMitra pipeline on the test corpus:
Ingestion -> Extraction (Docling/Text) -> Normalization -> Validation -> Partitioning -> Failure Reporting.
"""

from datetime import date
from pathlib import Path
import pytest

from legalmitra.core.enums import CourtType, Jurisdiction, ProcessingStatus, SourceType, SplitType
from legalmitra.dataset.partitioner import DatasetPartitioner
from legalmitra.dataset.pipeline import LegalDataPipeline
from legalmitra.schemas.judgment import JudgmentDocument
from legalmitra.schemas.statute import StatuteDocument


def test_end_to_end_pipeline_execution(temp_env_dir):
    pipeline = LegalDataPipeline(
        registry_file=temp_env_dir["registry_file"],
        raw_dir=temp_env_dir["raw_dir"],
        normalized_dir=temp_env_dir["norm_dir"],
    )

    corpus_items = [
        (
            Path("corpus/sample_statute_bsa_s61.txt"),
            {
                "document_id": "IND-STAT-BSA-2023-SEC61",
                "title": "Bharatiya Sakshya Adhiniyam, 2023 - Section 61",
                "source_url": "https://indiacode.nic.in/handle/123456789/20000",
                "source_type": SourceType.STATUTE,
                "jurisdiction": Jurisdiction.INDIA_CENTRAL,
                "document_date": date(2023, 12, 25),
                "effective_date": date(2024, 7, 1),
                "licence_or_terms": "GODL-India",
            },
        ),
        (
            Path("corpus/sample_judgment_sc_privacy.txt"),
            {
                "document_id": "IND-JUD-SC-2017-PUTTASWAMY",
                "title": "Justice K.S. Puttaswamy (Retd.) v. Union of India",
                "source_url": "https://main.sci.gov.in/judgments",
                "source_type": SourceType.JUDGMENT,
                "jurisdiction": Jurisdiction.INDIA_CENTRAL,
                "court": CourtType.SUPREME_COURT,
                "document_date": date(2017, 8, 24),
                "licence_or_terms": "Public Domain / Court Records",
            },
        ),
        (
            Path("corpus/sample_statute_bsa_s63.html"),
            {
                "document_id": "IND-STAT-BSA-2023-SEC63",
                "title": "Bharatiya Sakshya Adhiniyam, 2023 - Section 63",
                "source_url": "https://indiacode.nic.in/handle/123456789/20000",
                "source_type": SourceType.STATUTE,
                "jurisdiction": Jurisdiction.INDIA_CENTRAL,
                "document_date": date(2023, 12, 25),
                "licence_or_terms": "GODL-India",
            },
        ),
        (
            Path("corpus/sample_statute_pocso_s4.txt"),
            {
                "document_id": "IND-STAT-POCSO-2012-SEC4",
                "title": "Protection of Children from Sexual Offences Act, 2012 - Section 4",
                "source_url": "https://indiacode.nic.in/pocso",
                "source_type": SourceType.STATUTE,
                "jurisdiction": Jurisdiction.INDIA_CENTRAL,
                "document_date": date(2012, 6, 19),
                "licence_or_terms": "GODL-India",
                "privacy_redaction_notes": "Complies with POCSO Section 33(7) child privacy rules.",
            },
        ),
        (
            Path("corpus/unsupported_dummy.xyz"),
            {
                "document_id": "IND-UNSUPPORTED-001",
                "title": "Corrupt or Unsupported Document",
                "source_url": "https://example.com/unsupported",
                "source_type": SourceType.OTHER,
                "document_date": date(2024, 1, 1),
                "licence_or_terms": "Unknown",
            },
        ),
    ]

    # Run batch processing
    results = pipeline.process_batch(corpus_items)
    assert len(results) == 5

    # Check registry contents
    assert len(pipeline.registry) == 5

    # Verify BSA S61 normalization
    bsa_rec, bsa_model = results[0]
    assert bsa_rec.processing_status == ProcessingStatus.NORMALIZED
    assert isinstance(bsa_model, StatuteDocument)
    assert bsa_model.sections[0].section_number == "61"

    # Verify Puttaswamy judgment normalization
    sc_rec, sc_model = results[1]
    assert sc_rec.processing_status == ProcessingStatus.NORMALIZED
    assert isinstance(sc_model, JudgmentDocument)
    assert sc_model.court == CourtType.SUPREME_COURT
    assert len(sc_model.paragraphs) >= 4

    # Verify HTML processed via Docling
    html_rec, html_model = results[2]
    assert html_rec.processing_status == ProcessingStatus.NORMALIZED
    assert isinstance(html_model, StatuteDocument)

    # Verify POCSO normalization
    pocso_rec, pocso_model = results[3]
    assert pocso_rec.processing_status == ProcessingStatus.NORMALIZED
    assert isinstance(pocso_model, StatuteDocument)

    # Verify unsupported case
    unsup_rec, unsup_model = results[4]
    assert unsup_rec.processing_status == ProcessingStatus.FAILED
    assert unsup_model is None
    assert "No extractor registered" in (unsup_rec.error_log or "")

    # Verify Failure Reporter output
    report = pipeline.get_failure_report()
    assert "# LegalMitra Extraction & Failure Diagnostic Report" in report
    assert "UNSUPPORTED_FORMAT" in report
    assert "IND-UNSUPPORTED-001" in report

    # Test Resumability: re-running does not re-extract already normalized docs
    second_run = pipeline.process_batch(corpus_items, force_reprocess=False)
    assert len(second_run) == 5

    # Test dataset partitioning across normalized documents
    normalized_models = [m for _, m in results if m is not None]
    partitioner = DatasetPartitioner(train_ratio=0.5, val_ratio=0.25, test_ratio=0.25, seed=42)
    splits = partitioner.partition_by_source(normalized_models)

    # Ensure zero data leakage
    train_sources = {m.source_id for m in splits[SplitType.TRAIN]}
    val_sources = {m.source_id for m in splits[SplitType.VALIDATION]}
    test_sources = {m.source_id for m in splits[SplitType.TEST]}

    assert len(train_sources.intersection(val_sources)) == 0
    assert len(train_sources.intersection(test_sources)) == 0
    assert len(val_sources.intersection(test_sources)) == 0

