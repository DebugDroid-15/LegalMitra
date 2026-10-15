"""
LegalMitra Deduplication Engine
Detects exact and near-duplicate records across ingested statutes, judgments, and generated datasets.
"""

from typing import Dict, List, Optional, Set
from pydantic import BaseModel

from legalmitra.core.hashing import compute_content_fingerprint, compute_file_sha256, compute_text_sha256
from legalmitra.core.logging import get_logger

logger = get_logger("deduplication")


class DeduplicationEngine:
    """
    Tracks seen checksums, structural hashes, and content fingerprints.
    """

    def __init__(self):
        self.file_checksums: Set[str] = set()
        self.content_fingerprints: Dict[str, str] = {}  # fingerprint -> item_id
        self.item_ids: Set[str] = set()

    def is_file_duplicate(self, file_sha256: str) -> bool:
        return file_sha256.lower() in self.file_checksums

    def register_file(self, file_sha256: str) -> None:
        self.file_checksums.add(file_sha256.lower())

    def check_and_register_text(self, item_id: str, text: str) -> Optional[str]:
        """
        Computes normalized content fingerprint.
        If duplicate is detected, returns existing duplicate item_id.
        Otherwise registers text and returns None.
        """
        fingerprint = compute_content_fingerprint(text)
        if fingerprint in self.content_fingerprints:
            existing_id = self.content_fingerprints[fingerprint]
            logger.info(f"Duplicate content detected: '{item_id}' matches existing '{existing_id}'.")
            return existing_id

        self.content_fingerprints[fingerprint] = item_id
        self.item_ids.add(item_id)
        return None

    def deduplicate_items(self, items: List[BaseModel], text_field: str = "full_verbatim_text", id_field: str = "section_id") -> List[BaseModel]:
        """
        Filters out duplicate items from a list of Pydantic models.
        """
        unique_items = []
        for item in items:
            item_id = str(getattr(item, id_field, id(item)))
            text_val = str(getattr(item, text_field, ""))
            duplicate_id = self.check_and_register_text(item_id, text_val)
            if duplicate_id is None:
                unique_items.append(item)
            else:
                logger.warning(f"Dropping duplicate item {item_id} (duplicate of {duplicate_id})")
        return unique_items

