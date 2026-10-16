"""
LegalMitra Extraction Dispatcher
Routes documents to Docling or text extractors, logs failures, and maintains registry states.
"""

from pathlib import Path
from typing import Dict, Optional, Union

from legalmitra.core.enums import ProcessingStatus
from legalmitra.core.errors import ExtractionError, UnsupportedDocumentError
from legalmitra.core.logging import get_logger
from legalmitra.extraction.base import BaseExtractor, ExtractionResult
from legalmitra.extraction.docling_extractor import DoclingExtractor
from legalmitra.extraction.text_extractor import TextExtractor
from legalmitra.ingestion.registry import SourceRegistryManager

logger = get_logger("extraction_dispatcher")


class ExtractionDispatcher:
    """
    Coordinates extraction across available backends with fallback, error handling,
    and registry synchronization.
    """

    def __init__(self, registry_manager: Optional[SourceRegistryManager] = None, max_num_pages: int = 30):
        self.registry = registry_manager
        self.docling_extractor = DoclingExtractor(lazy_init=True, max_num_pages=max_num_pages)
        self.text_extractor = TextExtractor()
        self.extractors: Dict[str, BaseExtractor] = {}

    def get_extractor_for(self, file_extension: str) -> BaseExtractor:
        ext = file_extension.lower()
        if self.docling_extractor.supports_format(ext):
            return self.docling_extractor
        if self.text_extractor.supports_format(ext):
            return self.text_extractor
        raise UnsupportedDocumentError(f"No extractor registered for file extension: '{file_extension}'")

    def extract(self, file_path: Union[str, Path], document_id: str) -> ExtractionResult:
        path = Path(file_path).resolve()
        ext = path.suffix.lower()

        try:
            extractor = self.get_extractor_for(ext)
            result = extractor.extract(path, document_id)
        except UnsupportedDocumentError as e:
            error_msg = str(e)
            logger.warning(f"Unsupported document {document_id} ({path.name}): {error_msg}")
            result = ExtractionResult(
                document_id=document_id,
                source_file_path=str(path),
                success=False,
                extractor_name="None",
                error_message=error_msg,
            )
        except Exception as e:
            error_msg = f"Unexpected failure extracting {document_id}: {e}"
            logger.error(error_msg)
            result = ExtractionResult(
                document_id=document_id,
                source_file_path=str(path),
                success=False,
                extractor_name="Unknown",
                error_message=error_msg,
            )

        # Update registry if available
        if self.registry:
            rec = self.registry.get(document_id)
            if rec:
                new_status = ProcessingStatus.EXTRACTED if result.success else ProcessingStatus.FAILED
                self.registry.update_status(
                    document_id=document_id,
                    processing_status=new_status,
                    error_log=result.error_message if not result.success else None,
                )

        return result

