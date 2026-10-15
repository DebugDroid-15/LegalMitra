"""
LegalMitra Extraction Failure Reporter
Audits, categorizes, and produces diagnostic reports for extraction failures and unsupported cases.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import json

from legalmitra.extraction.base import ExtractionResult


@dataclass
class FailureRecord:
    document_id: str
    file_path: str
    file_extension: str
    failure_category: str
    error_message: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    suggested_remediation: str = ""


class ExtractionFailureReporter:
    """
    Collects extraction attempts, identifies failure modes, and renders diagnostic reports.
    """

    def __init__(self):
        self.total_attempts: int = 0
        self.successful_extractions: int = 0
        self.failures: List[FailureRecord] = []

    def record_result(self, result: ExtractionResult) -> None:
        self.total_attempts += 1
        if result.success:
            self.successful_extractions += 1
            return

        file_ext = Path(result.source_file_path).suffix.lower()
        error_msg = result.error_message or "Unknown extraction failure"

        # Categorize failure mode
        if "not supported" in error_msg.lower() or "no extractor registered" in error_msg.lower():
            category = "UNSUPPORTED_FORMAT"
            remediation = f"Convert file from '{file_ext}' to standard PDF, DOCX, HTML, or TXT before ingestion."
        elif "decode" in error_msg.lower() or "codec" in error_msg.lower():
            category = "ENCODING_DECODING_FAILURE"
            remediation = "Re-encode source text file into UTF-8 without byte-order marks."
        elif "ocr" in error_msg.lower() or "scanned" in error_msg.lower():
            category = "SCANNED_PDF_REQUIRES_OCR"
            remediation = "Enable OCR model weights in Docling pipeline or pre-process with rapidocr."
        elif "not found" in error_msg.lower():
            category = "FILE_NOT_FOUND"
            remediation = "Verify source document was correctly copied into raw repository."
        else:
            category = "ENGINE_CONVERSION_ERROR"
            remediation = "Inspect Docling parser logs; file may contain malformed PDF structure or corrupted tables."

        self.failures.append(
            FailureRecord(
                document_id=result.document_id,
                file_path=result.source_file_path,
                file_extension=file_ext,
                failure_category=category,
                error_message=error_msg,
                suggested_remediation=remediation,
            )
        )

    def generate_markdown_report(self) -> str:
        """Generates a human-readable markdown diagnostic report."""
        failure_count = len(self.failures)
        success_rate = (self.successful_extractions / self.total_attempts * 100.0) if self.total_attempts > 0 else 0.0

        lines = [
            "# LegalMitra Extraction & Failure Diagnostic Report",
            f"**Generated at**: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}",
            "",
            "## Summary Metrics",
            f"- **Total Documents Processed**: {self.total_attempts}",
            f"- **Successful Extractions**: {self.successful_extractions}",
            f"- **Failed / Unsupported Extractions**: {failure_count}",
            f"- **Success Rate**: {success_rate:.1f}%",
            "",
        ]

        if not self.failures:
            lines.append("### Status: All documents extracted cleanly without failure.\n")
            return "\n".join(lines)

        lines.extend([
            "## Extraction Failures and Unsupported Cases",
            "| Document ID | Format | Failure Category | Suggested Remediation |",
            "|---|---|---|---|",
        ])

        for f in self.failures:
            doc_link = f"`{f.document_id}`"
            lines.append(
                f"| {doc_link} | `{f.file_extension}` | **{f.failure_category}** | {f.suggested_remediation} |"
            )

        lines.append("\n### Detailed Failure Logs\n")
        for idx, f in enumerate(self.failures, start=1):
            lines.extend([
                f"#### Case {idx}: {f.document_id}",
                f"- **File Path**: `{f.file_path}`",
                f"- **Failure Mode**: `{f.failure_category}`",
                f"- **Error Diagnostic**: ```\n{f.error_message}\n```",
                f"- **Actionable Remediation**: {f.suggested_remediation}",
                "",
            ])

        return "\n".join(lines)

    def to_dict(self) -> Dict:
        return {
            "total_attempts": self.total_attempts,
            "successful_extractions": self.successful_extractions,
            "failed_extractions": len(self.failures),
            "failures": [
                {
                    "document_id": f.document_id,
                    "file_path": f.file_path,
                    "file_extension": f.file_extension,
                    "failure_category": f.failure_category,
                    "error_message": f.error_message,
                    "timestamp": f.timestamp,
                    "suggested_remediation": f.suggested_remediation,
                }
                for f in self.failures
            ],
        }

