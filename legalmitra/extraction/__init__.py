"""
LegalMitra Extraction Package
"""

from legalmitra.extraction.base import BaseExtractor, ExtractedPage, ExtractionResult
from legalmitra.extraction.dispatcher import ExtractionDispatcher
from legalmitra.extraction.docling_extractor import DoclingExtractor
from legalmitra.extraction.failure_reporter import ExtractionFailureReporter, FailureRecord
from legalmitra.extraction.text_extractor import TextExtractor

__all__ = [
    "BaseExtractor",
    "ExtractedPage",
    "ExtractionResult",
    "DoclingExtractor",
    "TextExtractor",
    "ExtractionDispatcher",
    "ExtractionFailureReporter",
    "FailureRecord",
]

