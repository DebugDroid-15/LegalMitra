"""
LegalMitra Document Normalizer Orchestrator
Coordinates normalization across statutes, judgments, and legal notifications,
persisting structured outputs to data/02_normalized/.
"""

import json
from pathlib import Path
from typing import Optional, Union

from pydantic import BaseModel

from legalmitra.core.enums import ProcessingStatus, SourceType
from legalmitra.core.errors import NormalizationError
from legalmitra.core.logging import get_logger
from legalmitra.extraction.base import ExtractionResult
from legalmitra.ingestion.registry import SourceRegistryManager
from legalmitra.normalization.judgment_normalizer import JudgmentNormalizer
from legalmitra.normalization.statute_normalizer import StatuteNormalizer
from legalmitra.schemas.registry import SourceRegistryRecord

logger = get_logger("document_normalizer")


class DocumentNormalizer:
    """
    High-level normalization coordinator.
    Transforms raw extractions into schema-validated models and saves normalized JSON artifacts.
    """

    def __init__(
        self,
        normalized_output_dir: Union[str, Path],
        registry_manager: Optional[SourceRegistryManager] = None,
    ):
        self.output_dir = Path(normalized_output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.registry = registry_manager
        self.statute_normalizer = StatuteNormalizer()
        self.judgment_normalizer = JudgmentNormalizer()

    def normalize(
        self,
        extraction: ExtractionResult,
        registry_record: SourceRegistryRecord,
    ) -> BaseModel:
        if not extraction.success:
            raise NormalizationError(
                f"Cannot normalize document {registry_record.document_id}: extraction was unsuccessful."
            )

        logger.info(f"Normalizing document {registry_record.document_id} (type: {registry_record.source_type})...")

        try:
            if registry_record.source_type in (SourceType.STATUTE, SourceType.RULES_REGULATION, SourceType.GAZETTE):
                model = self.statute_normalizer.normalize(extraction, registry_record)
            elif registry_record.source_type == SourceType.JUDGMENT:
                model = self.judgment_normalizer.normalize(extraction, registry_record)
            else:
                # Default to statute structure for legal provisions
                model = self.statute_normalizer.normalize(extraction, registry_record)

            # Persist normalized JSON
            output_file = self.output_dir / f"{registry_record.document_id}.json"
            with output_file.open("w", encoding="utf-8") as f:
                f.write(model.model_dump_json(indent=2))

            logger.info(f"Saved normalized model to {output_file}")

            # Update registry
            if self.registry:
                self.registry.update_status(
                    document_id=registry_record.document_id,
                    processing_status=ProcessingStatus.NORMALIZED,
                )

            return model

        except Exception as e:
            logger.error(f"Normalization failed for {registry_record.document_id}: {e}")
            if self.registry:
                self.registry.update_status(
                    document_id=registry_record.document_id,
                    processing_status=ProcessingStatus.FAILED,
                    error_log=f"Normalization failed: {str(e)}",
                )
            raise NormalizationError(f"Failed to normalize {registry_record.document_id}: {e}") from e

