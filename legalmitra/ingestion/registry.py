"""
LegalMitra Source Registry Manager
Provides persistent, thread-safe, and resumable registry management for Indian legal sources.
Stored as JSONL with validation against SourceRegistryRecord schema.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Union
import threading

from legalmitra.core.enums import LegalReviewStatus, ProcessingStatus, SourceType
from legalmitra.core.errors import DuplicateDocumentError, SourceRegistryError
from legalmitra.core.logging import get_logger
from legalmitra.schemas.registry import SourceRegistryRecord

logger = get_logger("registry_manager")


class SourceRegistryManager:
    """
    Manages reading, writing, querying, deduplicating, and updating source records.
    Backed by a JSONL file for append-only auditability and reproducibility.
    """

    def __init__(self, registry_file: Union[str, Path]):
        self.registry_file = Path(registry_file)
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._records: Dict[str, SourceRegistryRecord] = {}
        self._checksum_index: Dict[str, str] = {}  # checksum -> document_id
        self._load()

    def _load(self) -> None:
        """Loads records from the JSONL file."""
        if not self.registry_file.exists():
            logger.info(f"Registry file not found. Initialized empty registry at {self.registry_file}")
            return

        with self.registry_file.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                clean_line = line.strip()
                if not clean_line:
                    continue
                try:
                    data = json.loads(clean_line)
                    record = SourceRegistryRecord.model_validate(data)
                    self._records[record.document_id] = record
                    self._checksum_index[record.checksum] = record.document_id
                except Exception as e:
                    logger.error(f"Corrupted registry entry at line {line_no} in {self.registry_file}: {e}")
                    raise SourceRegistryError(f"Registry corrupted at line {line_no}: {e}") from e

        logger.info(f"Loaded {len(self._records)} source records from {self.registry_file}")

    def _save_all(self) -> None:
        """Atomically saves all records to the JSONL file."""
        temp_file = self.registry_file.with_suffix(".tmp")
        with temp_file.open("w", encoding="utf-8") as f:
            for record in self._records.values():
                f.write(record.model_dump_json() + "\n")
        temp_file.replace(self.registry_file)

    def register(self, record: SourceRegistryRecord, allow_duplicate_checksum: bool = False) -> SourceRegistryRecord:
        """
        Registers a new source document.
        Detects duplicate document_id and duplicate checksum.
        """
        with self._lock:
            if record.document_id in self._records:
                raise DuplicateDocumentError(
                    f"Document with ID '{record.document_id}' already registered."
                )

            if not allow_duplicate_checksum and record.checksum in self._checksum_index:
                existing_id = self._checksum_index[record.checksum]
                raise DuplicateDocumentError(
                    f"Document with identical checksum ({record.checksum}) already exists under ID '{existing_id}'."
                )

            self._records[record.document_id] = record
            self._checksum_index[record.checksum] = record.document_id

            # Append to file
            with self.registry_file.open("a", encoding="utf-8") as f:
                f.write(record.model_dump_json() + "\n")

            logger.info(f"Registered document {record.document_id} ('{record.title}')")
            return record

    def get(self, document_id: str) -> Optional[SourceRegistryRecord]:
        """Retrieves a source record by its document_id."""
        return self._records.get(document_id)

    def get_by_checksum(self, checksum: str) -> Optional[SourceRegistryRecord]:
        """Retrieves a source record by file checksum."""
        doc_id = self._checksum_index.get(checksum.lower())
        return self._records.get(doc_id) if doc_id else None

    def list_all(self) -> List[SourceRegistryRecord]:
        """Returns all registered records."""
        return list(self._records.values())

    def filter(
        self,
        source_type: Optional[SourceType] = None,
        processing_status: Optional[ProcessingStatus] = None,
        verification_status: Optional[LegalReviewStatus] = None,
    ) -> List[SourceRegistryRecord]:
        """Filters records by criteria (useful for resumable batch workflows)."""
        results = []
        for r in self._records.values():
            if source_type and r.source_type != source_type:
                continue
            if processing_status and r.processing_status != processing_status:
                continue
            if verification_status and r.verification_status != verification_status:
                continue
            results.append(r)
        return results

    def update_status(
        self,
        document_id: str,
        processing_status: Optional[ProcessingStatus] = None,
        verification_status: Optional[LegalReviewStatus] = None,
        error_log: Optional[str] = None,
    ) -> SourceRegistryRecord:
        """
        Updates processing and/or legal review status of a registered document.
        Maintains resumable pipeline state.
        """
        with self._lock:
            record = self._records.get(document_id)
            if not record:
                raise SourceRegistryError(f"Cannot update status: document '{document_id}' not found.")

            update_dict = record.model_dump()
            if processing_status is not None:
                update_dict["processing_status"] = processing_status.value
            if verification_status is not None:
                update_dict["verification_status"] = verification_status.value
            if error_log is not None:
                update_dict["error_log"] = error_log

            updated_record = SourceRegistryRecord.model_validate(update_dict)
            self._records[document_id] = updated_record
            self._save_all()

            logger.info(
                f"Updated document {document_id}: processing={updated_record.processing_status.value}, "
                f"verification={updated_record.verification_status.value}"
            )
            return updated_record

    def __len__(self) -> int:
        return len(self._records)

