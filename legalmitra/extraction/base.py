"""
LegalMitra Extraction Base
Defines the abstract interface and data structures for document extractors.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ExtractedPage:
    """Represents text and structural elements from a single document page."""
    page_number: int
    text: str
    tables: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ExtractionResult:
    """Standardized output of the document extraction pipeline."""
    document_id: str
    source_file_path: str
    success: bool
    text: str = ""
    markdown: str = ""
    pages: List[ExtractedPage] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    extractor_name: str = "BaseExtractor"
    error_message: Optional[str] = None

    @property
    def total_pages(self) -> int:
        return len(self.pages)


class BaseExtractor(ABC):
    """Abstract interface for all document extraction backends."""

    @abstractmethod
    def extract(self, file_path: Path, document_id: str) -> ExtractionResult:
        """
        Extracts structured text from a document.
        Must return ExtractionResult and never crash unhandled.
        """
        pass

    @abstractmethod
    def supports_format(self, file_extension: str) -> bool:
        """Returns True if the extractor can handle the given file extension."""
        pass

