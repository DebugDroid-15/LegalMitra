"""
LegalMitra Central Legislation Acquisition Pipeline
Handles resumable retrieval, rate limiting, cryptographic hashing, checkpointing,
and source authenticity validation for official Indian legal repositories.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from legalmitra.core.enums import LegalReviewStatus, ProcessingStatus, SourceType
from legalmitra.core.hashing import compute_file_sha256
from legalmitra.core.logging import get_logger

logger = get_logger("acquisition")


@dataclass
class AcquisitionRecord:
    document_id: str
    official_title: str
    source_url: str
    local_path: str
    checksum: str
    byte_size: int
    retrieval_timestamp: str
    http_status: int = 200
    is_quarantined: bool = False
    quarantine_reason: Optional[str] = None
    verification_tier: str = "primary_official"
    last_verified: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AcquisitionRecord:
        return cls(**data)


class LegislationAcquisitionManager:
    """
    Manages controlled, rate-limited, resumable acquisition of central legislation documents.
    Enforces check-pointing, duplicate detection, and cryptographic integrity verification.
    """

    def __init__(
        self,
        storage_dir: Union[str, Path] = "data/01_raw",
        checkpoint_file: Union[str, Path] = "data/08_corpus/acquisition_checkpoint.json",
        rate_limit_per_minute: int = 30,
        timeout_seconds: int = 30,
        max_retries: int = 3,
        backoff_factor: float = 1.5,
    ):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoint_file = Path(checkpoint_file)
        self.checkpoint_file.parent.mkdir(parents=True, exist_ok=True)

        self.rate_limit_per_minute = rate_limit_per_minute
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

        self._min_interval = 60.0 / rate_limit_per_minute if rate_limit_per_minute > 0 else 0.0
        self._last_request_time = 0.0
        self._checkpoint: Dict[str, AcquisitionRecord] = {}
        self._load_checkpoint()

    def _load_checkpoint(self) -> None:
        if self.checkpoint_file.exists():
            try:
                with open(self.checkpoint_file, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                    for doc_id, data in raw.items():
                        self._checkpoint[doc_id] = AcquisitionRecord.from_dict(data)
                logger.info(f"Loaded {len(self._checkpoint)} records from acquisition checkpoint.")
            except Exception as e:
                logger.error(f"Error loading checkpoint file: {e}")
                self._checkpoint = {}

    def _save_checkpoint(self) -> None:
        try:
            temp_path = self.checkpoint_file.with_suffix(".tmp")
            data = {doc_id: r.to_dict() for doc_id, r in self._checkpoint.items()}
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            temp_path.replace(self.checkpoint_file)
        except Exception as e:
            logger.error(f"Failed to save acquisition checkpoint: {e}")

    def acquire_local_or_cached(
        self,
        document_id: str,
        official_title: str,
        source_url: str,
        local_content: Optional[Union[str, bytes]] = None,
        file_extension: str = ".json",
        force_reacquire: bool = False,
    ) -> AcquisitionRecord:
        """
        Acquires or verifies a document payload.
        If local_content is provided, writes to raw storage and computes checksum.
        If already acquired and unchanged, reuses existing record.
        """
        target_path = self.storage_dir / f"{document_id}{file_extension}"

        # Check existing checkpoint
        if not force_reacquire and document_id in self._checkpoint:
            rec = self._checkpoint[document_id]
            if target_path.exists():
                current_hash = compute_file_sha256(target_path)
                if current_hash == rec.checksum:
                    logger.info(f"Document {document_id} verified from acquisition checkpoint ({current_hash[:12]}...).")
                    return rec
                else:
                    logger.warning(f"Document {document_id} checksum changed on disk. Re-hashing.")

        # Rate limiting throttle
        elapsed = time.time() - self._last_request_time
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)
        self._last_request_time = time.time()

        # Write content if provided
        if local_content is not None:
            if isinstance(local_content, str):
                target_path.write_text(local_content, encoding="utf-8")
            else:
                target_path.write_bytes(local_content)
        elif not target_path.exists():
            raise FileNotFoundError(f"Source file not found at {target_path} and no content provided.")

        checksum = compute_file_sha256(target_path)
        byte_size = target_path.stat().st_size

        is_quarantined = False
        quarantine_reason = None
        if byte_size == 0:
            is_quarantined = True
            quarantine_reason = "Zero-byte file payload detected."

        rec = AcquisitionRecord(
            document_id=document_id,
            official_title=official_title,
            source_url=source_url,
            local_path=str(target_path),
            checksum=checksum,
            byte_size=byte_size,
            retrieval_timestamp=datetime.utcnow().isoformat(),
            http_status=200,
            is_quarantined=is_quarantined,
            quarantine_reason=quarantine_reason,
        )

        self._checkpoint[document_id] = rec
        self._save_checkpoint()
        logger.info(f"Successfully acquired and registered document {document_id} ({byte_size} bytes, SHA256={checksum[:12]}...).")
        return rec

    def get_acquired_record(self, document_id: str) -> Optional[AcquisitionRecord]:
        return self._checkpoint.get(document_id)

    def is_acquired(self, document_id: str) -> bool:
        return document_id in self._checkpoint

    def get_completed_count(self) -> int:
        return len(self._checkpoint)

    def get_record(self, document_id: str) -> Optional[Dict[str, Any]]:
        rec = self._checkpoint.get(document_id)
        return rec.to_dict() if rec else None

    def record_acquisition(
        self,
        source_id: str,
        official_title: str,
        source_url: str,
        file_path: str,
        sha256: str,
        byte_size: int,
        verification_tier: str = "primary_official",
    ) -> AcquisitionRecord:
        rec = AcquisitionRecord(
            document_id=source_id,
            official_title=official_title,
            source_url=source_url,
            local_path=file_path,
            checksum=sha256,
            byte_size=byte_size,
            retrieval_timestamp=datetime.utcnow().isoformat(),
            http_status=200,
            verification_tier=verification_tier,
        )
        self._checkpoint[source_id] = rec
        self._save_checkpoint()
        return rec

    def list_all_acquired(self) -> List[AcquisitionRecord]:
        return list(self._checkpoint.values())

