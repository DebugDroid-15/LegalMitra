"""
Tests for LegalMitra Document Extraction, Fallback, and Failure Reporting.
"""

from pathlib import Path
import pytest

from legalmitra.extraction.base import ExtractionResult
from legalmitra.extraction.dispatcher import ExtractionDispatcher
from legalmitra.extraction.docling_extractor import DoclingExtractor
from legalmitra.extraction.failure_reporter import ExtractionFailureReporter
from legalmitra.extraction.text_extractor import TextExtractor


def test_text_extractor_success():
    extractor = TextExtractor()
    sample_file = Path("corpus/sample_statute_bsa_s61.txt")
    assert sample_file.exists()

    result = extractor.extract(sample_file, "TEST-BSA-001")
    assert result.success is True
    assert "Section 61" in result.text or "61." in result.text
    assert result.total_pages >= 1


def test_docling_extractor_html():
    extractor = DoclingExtractor(lazy_init=True)
    html_file = Path("corpus/sample_statute_bsa_s63.html")
    assert html_file.exists()

    result = extractor.extract(html_file, "TEST-HTML-001")
    assert result.success is True
    assert "Section 63" in result.text or "63." in result.text


def test_dispatcher_routing():
    dispatcher = ExtractionDispatcher()

    # Routes .txt to TextExtractor
    ext_txt = dispatcher.get_extractor_for(".txt")
    assert isinstance(ext_txt, TextExtractor)

    # Routes .html to DoclingExtractor
    ext_html = dispatcher.get_extractor_for(".html")
    assert isinstance(ext_html, DoclingExtractor)


def test_dispatcher_unsupported_format():
    dispatcher = ExtractionDispatcher()
    unsupported_file = Path("corpus/unsupported_dummy.xyz")
    assert unsupported_file.exists()

    result = dispatcher.extract(unsupported_file, "UNSUPPORTED-001")
    assert result.success is False
    assert "No extractor registered" in result.error_message


def test_failure_reporter_summary():
    reporter = ExtractionFailureReporter()

    # Record success
    res_success = ExtractionResult(
        document_id="DOC-OK-001",
        source_file_path="doc.pdf",
        success=True,
    )
    reporter.record_result(res_success)

    # Record failure
    res_fail = ExtractionResult(
        document_id="DOC-FAIL-001",
        source_file_path="unknown.xyz",
        success=False,
        error_message="No extractor registered for file extension: '.xyz'",
    )
    reporter.record_result(res_fail)

    assert reporter.total_attempts == 2
    assert reporter.successful_extractions == 1
    assert len(reporter.failures) == 1
    assert reporter.failures[0].failure_category == "UNSUPPORTED_FORMAT"

    md_report = reporter.generate_markdown_report()
    assert "# LegalMitra Extraction & Failure Diagnostic Report" in md_report
    assert "UNSUPPORTED_FORMAT" in md_report
    assert "DOC-FAIL-001" in md_report

