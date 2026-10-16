"""
LegalMitra Docling Extractor
Uses IBM Docling to convert supported legal documents (PDF, DOCX, HTML)
into structured Markdown and structured page objects.
"""

from pathlib import Path
import traceback
from typing import Optional

from legalmitra.core.logging import get_logger
from legalmitra.extraction.base import BaseExtractor, ExtractedPage, ExtractionResult

logger = get_logger("docling_extractor")


class DoclingExtractor(BaseExtractor):
    """
    Primary extractor using Docling DocumentConverter.
    Preserves document structure, headings, tables, and page boundaries.
    """

    SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".pptx", ".html", ".htm", ".asciidoc", ".md"}

    def __init__(self, enable_ocr: bool = False, lazy_init: bool = True, max_num_pages: Optional[int] = None):
        self.enable_ocr = enable_ocr
        self.max_num_pages = max_num_pages
        self._converter = None
        self.lazy_init = lazy_init
        if not lazy_init:
            self._init_converter()

    def _init_converter(self):
        """Initializes the Docling DocumentConverter instance."""
        if self._converter is None:
            try:
                from docling.document_converter import DocumentConverter
                self._converter = DocumentConverter()
                logger.info("Initialized Docling DocumentConverter successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize Docling DocumentConverter: {e}")
                raise

    def supports_format(self, file_extension: str) -> bool:
        return file_extension.lower() in self.SUPPORTED_EXTENSIONS

    def extract(self, file_path: Path, document_id: str) -> ExtractionResult:
        path = Path(file_path).resolve()
        if not path.is_file():
            return ExtractionResult(
                document_id=document_id,
                source_file_path=str(path),
                success=False,
                extractor_name="DoclingExtractor",
                error_message=f"File not found: {path}",
            )

        ext = path.suffix.lower()
        if not self.supports_format(ext):
            return ExtractionResult(
                document_id=document_id,
                source_file_path=str(path),
                success=False,
                extractor_name="DoclingExtractor",
                error_message=f"File format '{ext}' is not supported by DoclingExtractor.",
            )

        try:
            self._init_converter()
            logger.info(f"Extracting structured text from {path.name} using Docling...")
            conv_kwargs = {}
            if self.max_num_pages:
                conv_kwargs["max_num_pages"] = self.max_num_pages
            conv_res = self._converter.convert(str(path), **conv_kwargs)
            doc = conv_res.document

            # Export markdown
            markdown_text = doc.export_to_markdown()

            # Extract page structure if available
            pages = []
            if hasattr(doc, "pages") and doc.pages:
                for page_no, page_obj in doc.pages.items():
                    pages.append(
                        ExtractedPage(
                            page_number=int(page_no),
                            text="",
                            tables=[]
                        )
                    )

            # Metadata
            metadata = {
                "name": getattr(doc, "name", path.name),
                "num_pages": len(pages),
                "format": ext,
            }

            return ExtractionResult(
                document_id=document_id,
                source_file_path=str(path),
                success=True,
                text=markdown_text,
                markdown=markdown_text,
                pages=pages,
                metadata=metadata,
                extractor_name="DoclingExtractor",
            )
        except Exception as e:
            tb = traceback.format_exc()
            error_msg = f"Docling conversion error on {path.name}: {str(e)}\n{tb}"
            logger.error(error_msg)
            return ExtractionResult(
                document_id=document_id,
                source_file_path=str(path),
                success=False,
                extractor_name="DoclingExtractor",
                error_message=error_msg,
            )

