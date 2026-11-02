"""
Phase 85 Multi-Source Connectors: Base Definitions and Protocol
Defines standardized interfaces and schemas for Sovereign Ingestion Connectors:
- India Code (Central & State Acts)
- AI Kosh (IndiaAI Knowledge Hub & Gazettes)
- Hugging Face Open Legal Datasets (InLegalEval, ILQA, EkStep)
- Kaggle & e-SCR (Supreme Court & Consumer Judgments)
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, Union

from legalmitra.core.enums import LegalReviewStatus, ProcessingStatus, SourceType
from legalmitra.schemas.registry import SourceRegistryRecord


class IngestionOrigin(str, Enum):
    INDIA_CODE = "india_code"
    AI_KOSH = "ai_kosh"
    HUGGING_FACE = "hugging_face"
    KAGGLE_ESCR = "kaggle_escr"


@dataclass
class IngestionDocument:
    document_id: str
    title: str
    source_url: str
    source_type: SourceType
    jurisdiction: str
    document_date: str
    origin: IngestionOrigin
    content_raw: Union[str, bytes]
    file_format: str = ".txt"
    effective_date: Optional[str] = None
    court: Optional[str] = "None (Statutory / Executive)"
    license_or_terms: str = "Government of India Open Data License (GODL-India)"
    metadata: Dict[str, Any] = field(default_factory=dict)
    privacy_notes: Optional[str] = None

    def compute_sha256(self) -> str:
        if isinstance(self.content_raw, str):
            b = self.content_raw.encode("utf-8")
        else:
            b = self.content_raw
        return hashlib.sha256(b).hexdigest()

    def get_byte_size(self) -> int:
        if isinstance(self.content_raw, str):
            return len(self.content_raw.encode("utf-8"))
        return len(self.content_raw)


class BaseConnector(Protocol):
    """Protocol for all multi-source connectors in Phase 85."""
    origin: IngestionOrigin

    def fetch_documents(self, limit: Optional[int] = None) -> List[IngestionDocument]:
        """Fetch documents from the underlying source."""
        ...
