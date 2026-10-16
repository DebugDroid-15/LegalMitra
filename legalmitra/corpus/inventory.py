"""
LegalMitra National Indian Legal Corpus Inventory Engine
Manages machine-readable inventories of statutory sources, subordinate legislation,
and judicial precedents with comprehensive temporal and authenticity metadata.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class DocumentClass(str, Enum):
    CONSTITUTION = "Constitution"
    ACT = "Act"
    AMENDMENT = "Amendment"
    RULE = "Rule"
    REGULATION = "Regulation"
    NOTIFICATION = "Notification"
    JUDGMENT = "Judgment"
    ORDER = "Order"
    CIRCULAR = "Circular"
    PRACTICE_DIRECTION = "Practice Direction"
    FORM = "Form"
    OTHER = "Other"


class CorpusStatus(str, Enum):
    CURRENT = "current"
    HISTORICAL = "historical"
    UNVERIFIED = "unverified"
    INACCESSIBLE = "inaccessible"
    QUARANTINED = "quarantined"


@dataclass
class CorpusInventoryItem:
    document_id: str
    official_title: str
    aliases: List[str] = field(default_factory=list)
    issuing_authority: str = ""
    jurisdiction: str = "IN"  # IN, IN-DL, IN-MH, etc., or Court
    document_class: DocumentClass = DocumentClass.ACT
    legal_domain: str = ""
    topic_taxonomy: List[str] = field(default_factory=list)
    language: str = "en"
    source_url: str = ""
    retrieval_date: Optional[str] = None
    enactment_date: Optional[str] = None
    assent_date: Optional[str] = None
    publication_date: Optional[str] = None
    notification_date: Optional[str] = None
    commencement_date: Optional[str] = None
    effective_date: Optional[str] = None
    version: str = "1.0.0"
    amendment_history: List[str] = field(default_factory=list)
    repeal_metadata: Optional[str] = None
    authenticity_status: str = "official_government"
    licence_or_terms: str = "GODL-India / Public Domain"
    extraction_status: str = "pending"
    validation_status: str = "pending"
    corpus_status: CorpusStatus = CorpusStatus.CURRENT
    coverage_gap_notes: Optional[str] = None
    review_requirements: Optional[str] = None
    indexed_chunk_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["document_class"] = self.document_class.value
        d["corpus_status"] = self.corpus_status.value
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> CorpusInventoryItem:
        data = dict(data)
        if "document_class" in data and isinstance(data["document_class"], str):
            data["document_class"] = DocumentClass(data["document_class"])
        if "corpus_status" in data and isinstance(data["corpus_status"], str):
            data["corpus_status"] = CorpusStatus(data["corpus_status"])
        return cls(**data)


class CorpusInventoryManager:
    """Manages loading, searching, validating, and exporting corpus inventory."""

    def __init__(self, items: Optional[List[CorpusInventoryItem]] = None):
        self._items: Dict[str, CorpusInventoryItem] = {}
        if items:
            for item in items:
                self.add_item(item)

    def add_item(self, item: CorpusInventoryItem) -> None:
        self._items[item.document_id] = item

    def get_item(self, doc_id: str) -> Optional[CorpusInventoryItem]:
        return self._items.get(doc_id)

    def list_items(self) -> List[CorpusInventoryItem]:
        return list(self._items.values())

    def filter_by_domain(self, domain: str) -> List[CorpusInventoryItem]:
        return [i for i in self._items.values() if domain.lower() in i.legal_domain.lower()]

    def filter_by_status(self, status: CorpusStatus) -> List[CorpusInventoryItem]:
        return [i for i in self._items.values() if i.corpus_status == status]

    def filter_by_jurisdiction(self, jurisdiction: str) -> List[CorpusInventoryItem]:
        return [i for i in self._items.values() if i.jurisdiction == jurisdiction]

    def export_json(self, target_path: Path) -> None:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        raw_data = [item.to_dict() for item in self._items.values()]
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(raw_data, f, indent=2, ensure_ascii=False)

    def export_csv(self, target_path: Path) -> None:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        items = list(self._items.values())
        if not items:
            fieldnames = ["document_id", "official_title", "jurisdiction", "document_class", "corpus_status"]
        else:
            first_dict = items[0].to_dict()
            fieldnames = list(first_dict.keys())

        with open(target_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in items:
                d = item.to_dict()
                # Serialize list fields for CSV compatibility
                if isinstance(d.get("aliases"), list):
                    d["aliases"] = "; ".join(d["aliases"])
                if isinstance(d.get("topic_taxonomy"), list):
                    d["topic_taxonomy"] = "; ".join(d["topic_taxonomy"])
                if isinstance(d.get("amendment_history"), list):
                    d["amendment_history"] = "; ".join(d["amendment_history"])
                writer.writerow(d)

    @classmethod
    def load_json(cls, source_path: Path) -> CorpusInventoryManager:
        with open(source_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        items = [CorpusInventoryItem.from_dict(d) for d in raw_data]
        return cls(items)

