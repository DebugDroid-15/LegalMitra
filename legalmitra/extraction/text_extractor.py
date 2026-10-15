"""
LegalMitra Text Extractor
Extracts verbatim text from legal text files (.txt, .md, .law) preserving exact statutory layout.
"""

from pathlib import Path
import re
from typing import List

from legalmitra.core.logging import get_logger
from legalmitra.extraction.base import BaseExtractor, ExtractedPage, ExtractionResult

logger = get_logger("text_extractor")


class TextExtractor(BaseExtractor):
    """
    Extracts text files while detecting explicit page markers (e.g. [Page X] or --- PAGE X ---).
    """

    SUPPORTED_EXTENSIONS = {".txt", ".md", ".law", ".text"}

    def supports_format(self, file_extension: str) -> bool:
        return file_extension.lower() in self.SUPPORTED_EXTENSIONS

    def extract(self, file_path: Path, document_id: str) -> ExtractionResult:
        path = Path(file_path).resolve()
        if not path.is_file():
            return ExtractionResult(
                document_id=document_id,
                source_file_path=str(path),
                success=False,
                extractor_name="TextExtractor",
                error_message=f"File not found: {path}",
            )

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            try:
                content = path.read_text(encoding="latin-1")
            except Exception as e:
                return ExtractionResult(
                    document_id=document_id,
                    source_file_path=str(path),
                    success=False,
                    extractor_name="TextExtractor",
                    error_message=f"Failed to decode text file: {e}",
                )

        # Detect page breaks if present: e.g. [Page 1] or --- Page 2 --- or \f (form feed)
        page_pattern = re.compile(r"(?:\[Page\s+(\d+)\]|---\s*PAGE\s+(\d+)\s*---|\f)", re.IGNORECASE)
        splits = page_pattern.split(content)

        pages: List[ExtractedPage] = []
        if len(splits) > 1:
            current_page_no = 1
            i = 0
            while i < len(splits):
                segment = splits[i]
                if segment is None:
                    i += 1
                    continue
                if segment.isdigit():
                    current_page_no = int(segment)
                elif segment.strip():
                    pages.append(
                        ExtractedPage(
                            page_number=current_page_no,
                            text=segment.strip(),
                        )
                    )
                    current_page_no += 1
                i += 1
        else:
            pages.append(ExtractedPage(page_number=1, text=content.strip()))

        return ExtractionResult(
            document_id=document_id,
            source_file_path=str(path),
            success=True,
            text=content,
            markdown=content,
            pages=pages,
            metadata={"num_pages": len(pages), "format": path.suffix.lower()},
            extractor_name="TextExtractor",
        )

