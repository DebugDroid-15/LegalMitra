"""
Phase 85: Multi-Source Sovereign Ingestion Pipeline Orchestrator
Aggregates streams from all four connectors (India Code, AI Kosh, Hugging Face, Kaggle/e-SCR),
persists raw documents to `data/01_raw/`, computes SHA-256 signatures,
and registers verified records into `registry/source_registry.jsonl`.
"""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from legalmitra.core.enums import LegalReviewStatus, ProcessingStatus
from legalmitra.ingestion.connectors.aikosh_connector import AIKoshConnector
from legalmitra.ingestion.connectors.base import BaseConnector, IngestionDocument
from legalmitra.ingestion.connectors.huggingface_connector import HuggingFaceConnector
from legalmitra.ingestion.connectors.indiacode_connector import IndiaCodeConnector
from legalmitra.ingestion.connectors.kaggle_escr_connector import KaggleESCRConnector
from legalmitra.ingestion.registry import SourceRegistryManager
from legalmitra.schemas.registry import SourceRegistryRecord

logger = logging.getLogger("multi_source_orchestrator")


@dataclass
class IngestionResult:
    total_fetched: int
    new_registered: int
    already_existing: int
    failed: int
    registered_ids: List[str]


class MultiSourceIngestionPipeline:
    """Orchestrates ingestion across all multi-source sovereign connectors."""

    def __init__(
        self,
        raw_storage_dir: Union[str, Path] = "data/01_raw",
        registry_file: Union[str, Path] = "registry/source_registry.jsonl",
        connectors: Optional[List[BaseConnector]] = None
    ):
        self.raw_storage_dir = Path(raw_storage_dir)
        self.raw_storage_dir.mkdir(parents=True, exist_ok=True)
        self.registry_manager = SourceRegistryManager(registry_file)
        self.connectors = connectors or [
            IndiaCodeConnector(),
            AIKoshConnector(),
            HuggingFaceConnector(),
            KaggleESCRConnector(),
        ]

    def run(self, limit_per_source: Optional[int] = None) -> IngestionResult:
        all_docs: List[IngestionDocument] = []
        for connector in self.connectors:
            try:
                docs = connector.fetch_documents(limit=limit_per_source)
                all_docs.extend(docs)
            except Exception as e:
                logger.error(f"Error fetching from connector {getattr(connector, 'origin', connector)}: {e}")

        total_fetched = len(all_docs)
        new_registered = 0
        already_existing = 0
        failed = 0
        registered_ids = []

        for doc in all_docs:
            try:
                # 1. Check if document already registered by ID
                existing = self.registry_manager.get(doc.document_id)
                if existing:
                    already_existing += 1
                    continue

                # 2. Write raw content to storage
                filename = f"{doc.document_id}{doc.file_format}"
                raw_path = self.raw_storage_dir / filename
                if isinstance(doc.content_raw, str):
                    raw_path.write_text(doc.content_raw, encoding="utf-8")
                else:
                    raw_path.write_bytes(doc.content_raw)

                # 3. Compute checksum & record size
                checksum = doc.compute_sha256()
                byte_size = doc.get_byte_size()

                # 4. Build registry record
                record = SourceRegistryRecord(
                    document_id=doc.document_id,
                    title=doc.title,
                    source_url=doc.source_url,
                    source_type=doc.source_type,
                    jurisdiction=doc.jurisdiction,
                    court=doc.court or "None (Statutory / Executive)",
                    document_date=doc.document_date,
                    effective_date=doc.effective_date,
                    version="1.0.0",
                    licence_or_terms=doc.license_or_terms,
                    checksum=checksum,
                    verification_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
                    processing_status=ProcessingStatus.NORMALIZED,
                    raw_file_path=str(raw_path),
                    file_format=doc.file_format,
                    byte_size=byte_size,
                    privacy_redaction_notes=doc.privacy_notes
                )

                # 5. Register in SourceRegistryManager
                self.registry_manager.register(record)
                new_registered += 1
                registered_ids.append(doc.document_id)
                logger.info(f"Registered document: {doc.document_id} ({doc.title})")

            except Exception as e:
                logger.error(f"Failed to ingest document {doc.document_id}: {e}")
                failed += 1

        return IngestionResult(
            total_fetched=total_fetched,
            new_registered=new_registered,
            already_existing=already_existing,
            failed=failed,
            registered_ids=registered_ids
        )
