"""
LegalMitra Corpus Ingestion Pipeline
Provides reproducible, resumable, and idempotent ingestion of Acts, amendments,
delegated legislation, and court precedents into the LegalMitra Knowledge Base.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from legalmitra.core.enums import CourtType, Jurisdiction, LegalReviewStatus, SourceType
from legalmitra.core.logging import get_logger
from legalmitra.corpus.inventory import CorpusInventoryItem, CorpusInventoryManager, CorpusStatus, DocumentClass
from legalmitra.ingestion.registry import SourceRegistryManager
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
from legalmitra.schemas.judgment import JudgmentDocument
from legalmitra.schemas.registry import SourceRegistryRecord
from legalmitra.schemas.statute import StatuteDocument, StatuteSection

logger = get_logger("corpus_ingestor")


@dataclass
class IngestionBatchResult:
    batch_name: str
    total_sources: int = 0
    successfully_indexed: int = 0
    skipped_existing: int = 0
    quarantined: int = 0
    failed: int = 0
    indexed_chunk_count: int = 0
    errors: List[Dict[str, str]] = field(default_factory=list)
    processed_doc_ids: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "batch_name": self.batch_name,
            "total_sources": self.total_sources,
            "successfully_indexed": self.successfully_indexed,
            "skipped_existing": self.skipped_existing,
            "quarantined": self.quarantined,
            "failed": self.failed,
            "indexed_chunk_count": self.indexed_chunk_count,
            "errors": self.errors,
            "processed_doc_ids": self.processed_doc_ids,
        }


class CorpusIngestionPipeline:
    """
    Orchestrates idempotent document parsing, validation, and knowledge base indexing.
    """

    def __init__(
        self,
        knowledge_base: Optional[LegalKnowledgeBase] = None,
        registry_manager: Optional[SourceRegistryManager] = None,
        inventory_manager: Optional[CorpusInventoryManager] = None,
    ):
        self.kb = knowledge_base or LegalKnowledgeBase(db_path="data/legalmitra_kb.db")
        self.registry = registry_manager or SourceRegistryManager(registry_file="registry/source_registry.jsonl")
        self.inventory = inventory_manager

    def ingest_statute_document(
        self,
        statute_doc: StatuteDocument,
        registry_record: SourceRegistryRecord,
        force_reindex: bool = False,
    ) -> int:
        """
        Indexes a statute document and its individual provisions into the Knowledge Base.
        Returns the number of indexed chunks.
        """
        doc_id = registry_record.document_id

        # Idempotency check: check if already in KB
        if not force_reindex and self.kb._source_exists(doc_id):
            logger.info(f"Document {doc_id} already exists in knowledge base. Skipping indexing.")
            return 0

        # Execute indexing into KB
        chunk_count = self.kb.index_statute_document(statute_doc, registry_record)
        logger.info(f"Successfully indexed statute {doc_id} ({chunk_count} chunks).")

        # Update inventory if available
        if self.inventory:
            item = self.inventory.get_item(doc_id)
            if item:
                item.extraction_status = "completed"
                item.validation_status = "validated"
                item.indexed_chunk_count = chunk_count

        return chunk_count

    def ingest_judgment_document(
        self,
        judgment_doc: JudgmentDocument,
        registry_record: SourceRegistryRecord,
        force_reindex: bool = False,
    ) -> int:
        """
        Indexes a judicial decision and its holding/ratio paragraphs into the Knowledge Base.
        Returns the number of indexed chunks.
        """
        doc_id = registry_record.document_id

        if not force_reindex and self.kb._source_exists(doc_id):
            logger.info(f"Judgment {doc_id} already exists in knowledge base. Skipping indexing.")
            return 0

        chunk_count = self.kb.index_judgment_document(judgment_doc, registry_record)
        logger.info(f"Successfully indexed judgment {doc_id} ({chunk_count} chunks).")

        if self.inventory:
            item = self.inventory.get_item(doc_id)
            if item:
                item.extraction_status = "completed"
                item.validation_status = "validated"
                item.indexed_chunk_count = chunk_count

        return chunk_count

    def ingest_normalized_file(
        self,
        normalized_file_path: Union[str, Path],
        force_reindex: bool = False,
    ) -> int:
        """
        Loads a pre-normalized JSON file from data/02_normalized and indexes it into the KB.
        """
        path = Path(normalized_file_path)
        if not path.is_file():
            raise FileNotFoundError(f"Normalized file not found: {path}")

        doc_id = path.stem
        registry_record = self.registry.get(doc_id)
        if not registry_record:
            raise ValueError(f"No registry record found for normalized document ID: {doc_id}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if registry_record.source_type == SourceType.JUDGMENT:
            doc = JudgmentDocument.model_validate(data)
            return self.ingest_judgment_document(doc, registry_record, force_reindex=force_reindex)
        else:
            doc = StatuteDocument.model_validate(data)
            return self.ingest_statute_document(doc, registry_record, force_reindex=force_reindex)

    def execute_batch(
        self,
        batch_name: str,
        file_paths: List[Union[str, Path]],
        force_reindex: bool = False,
    ) -> IngestionBatchResult:
        """
        Executes a controlled, resumable ingestion batch across multiple normalized files.
        """
        res = IngestionBatchResult(batch_name=batch_name, total_sources=len(file_paths))

        for p in file_paths:
            path = Path(p)
            doc_id = path.stem
            try:
                record = self.registry.get(doc_id)
                if record and record.verification_status == LegalReviewStatus.FLAGGED_UNSUPPORTED:
                    logger.warning(f"Quarantining flagged document: {doc_id}")
                    res.quarantined += 1
                    res.processed_doc_ids.append(doc_id)
                    continue

                chunk_count = self.ingest_normalized_file(path, force_reindex=force_reindex)
                if chunk_count > 0:
                    res.successfully_indexed += 1
                    res.indexed_chunk_count += chunk_count
                else:
                    res.skipped_existing += 1
                res.processed_doc_ids.append(doc_id)

            except Exception as e:
                logger.error(f"Failed to ingest {doc_id}: {str(e)}")
                res.failed += 1
                res.errors.append({"document_id": doc_id, "error": str(e)})

        return res
