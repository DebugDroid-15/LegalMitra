"""
LegalMitra Data Engineering Pipeline Orchestrator
Coordinates document ingestion, structured extraction (Docling/Text), legal normalization,
strict schema validation, failure tracking, and resumable state management.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from pydantic import BaseModel

from legalmitra.core.enums import Jurisdiction, ProcessingStatus
from legalmitra.core.logging import get_logger
from legalmitra.extraction.dispatcher import ExtractionDispatcher
from legalmitra.extraction.failure_reporter import ExtractionFailureReporter
from legalmitra.ingestion.ingestor import DocumentIngestor
from legalmitra.ingestion.registry import SourceRegistryManager
from legalmitra.normalization.normalizer import DocumentNormalizer
from legalmitra.schemas.registry import SourceRegistryRecord

logger = get_logger("pipeline_orchestrator")


class LegalDataPipeline:
    """
    End-to-end reproducible pipeline for legal documents under Indian jurisdiction.
    """

    def __init__(
        self,
        registry_file: Union[str, Path] = "registry/source_registry.jsonl",
        raw_dir: Union[str, Path] = "data/01_raw",
        normalized_dir: Union[str, Path] = "data/02_normalized",
    ):
        self.registry = SourceRegistryManager(registry_file)
        self.ingestor = DocumentIngestor(self.registry, raw_dir)
        self.dispatcher = ExtractionDispatcher(self.registry)
        self.normalizer = DocumentNormalizer(normalized_dir, self.registry)
        self.failure_reporter = ExtractionFailureReporter()

    def process_file(
        self,
        file_path: Union[str, Path],
        doc_metadata: Dict[str, Any],
        force_reprocess: bool = False,
    ) -> Tuple[SourceRegistryRecord, Optional[BaseModel]]:
        """
        Processes a single document through Ingestion -> Extraction -> Normalization.
        Maintains resumable status and catches failures without crashing pipeline.
        """
        source_path = Path(file_path).resolve()
        doc_id = doc_metadata["document_id"]

        logger.info(f"Pipeline started for: {doc_id} ({source_path.name})")

        # 1. Ingestion / Registration
        record = self.registry.get(doc_id)
        if not record or force_reprocess:
            record = self.ingestor.ingest_document(
                file_path=source_path,
                document_id=doc_id,
                title=doc_metadata["title"],
                source_url=doc_metadata["source_url"],
                source_type=doc_metadata["source_type"],
                document_date=doc_metadata["document_date"],
                licence_or_terms=doc_metadata["licence_or_terms"],
                jurisdiction=doc_metadata.get("jurisdiction") or Jurisdiction.INDIA_CENTRAL,
                court=doc_metadata.get("court"),
                effective_date=doc_metadata.get("effective_date"),
                version=doc_metadata.get("version", "1.0.0"),
                privacy_redaction_notes=doc_metadata.get("privacy_redaction_notes"),
                force_replace=force_reprocess,
            )

        # Check resumability
        if not force_reprocess and record.processing_status == ProcessingStatus.NORMALIZED:
            logger.info(f"Document {doc_id} is already normalized. Skipping extraction.")
            # Load cached normalized output
            norm_file = self.normalizer.output_dir / f"{doc_id}.json"
            if norm_file.exists():
                return record, None

        # 2. Extraction
        extraction_res = self.dispatcher.extract(record.raw_file_path, doc_id)
        self.failure_reporter.record_result(extraction_res)

        if not extraction_res.success:
            logger.warning(f"Extraction failed for {doc_id}: {extraction_res.error_message}")
            latest_rec = self.registry.get(doc_id) or record
            return latest_rec, None

        # 3. Normalization & Schema Validation
        try:
            normalized_doc = self.normalizer.normalize(extraction_res, record)
            latest_rec = self.registry.get(doc_id) or record
            return latest_rec, normalized_doc
        except Exception as e:
            logger.error(f"Normalization failed for {doc_id}: {e}")
            latest_rec = self.registry.get(doc_id) or record
            return latest_rec, None

    def process_batch(
        self,
        batch_items: List[Tuple[Union[str, Path], Dict[str, Any]]],
        force_reprocess: bool = False,
    ) -> List[Tuple[SourceRegistryRecord, Optional[BaseModel]]]:
        """
        Processes a collection of files sequentially, recording metrics and failures.
        """
        results = []
        for file_path, meta in batch_items:
            res = self.process_file(file_path, meta, force_reprocess=force_reprocess)
            results.append(res)
        return results

    def get_failure_report(self) -> str:
        """Returns diagnostic Markdown failure report."""
        return self.failure_reporter.generate_markdown_report()
