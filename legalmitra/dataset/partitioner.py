"""
LegalMitra Dataset Partitioner
Partitions legal records into Train / Validation / Test sets strictly grouped by
source document ID or case family to prevent data leakage.
"""

from collections import defaultdict
import random
from typing import Dict, List, Optional, Set, Tuple
from pydantic import BaseModel

from legalmitra.core.enums import SplitType
from legalmitra.core.logging import get_logger

logger = get_logger("dataset_partitioner")


class DatasetPartitioner:
    """
    Guarantees zero data leakage by grouping all items derived from a given source document
    or case family into exactly ONE split (Train, Validation, or Test).
    """

    def __init__(self, train_ratio: float = 0.7, val_ratio: float = 0.15, test_ratio: float = 0.15, seed: int = 42):
        assert abs((train_ratio + val_ratio + test_ratio) - 1.0) < 1e-5, "Split ratios must sum to 1.0"
        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.test_ratio = test_ratio
        self.seed = seed

    def partition_by_source(
        self,
        items: List[BaseModel],
        source_id_field: str = "source_id",
        case_family_field: Optional[str] = None,
    ) -> Dict[SplitType, List[BaseModel]]:
        """
        Groups items by source document or case family, then allocates entire groups
        to train, validation, or test.
        """
        rng = random.Random(self.seed)

        # Group items by key (source_id or case_family)
        groups: Dict[str, List[BaseModel]] = defaultdict(list)
        for item in items:
            key = None
            if case_family_field and hasattr(item, case_family_field):
                key = getattr(item, case_family_field)
            if not key and hasattr(item, source_id_field):
                key = getattr(item, source_id_field)
            if not key and hasattr(item, "supporting_source_ids"):
                supporting = getattr(item, "supporting_source_ids")
                key = supporting[0] if supporting else "unknown_source"
            if not key:
                key = "default_group"

            groups[str(key)].append(item)

        # Shuffle unique source keys
        unique_keys = list(groups.keys())
        rng.shuffle(unique_keys)

        total_keys = len(unique_keys)
        n_train = max(1, int(round(total_keys * self.train_ratio))) if total_keys >= 3 else 1
        n_val = max(1, int(round(total_keys * self.val_ratio))) if total_keys >= 3 else (1 if total_keys == 2 else 0)

        train_keys = set(unique_keys[:n_train])
        val_keys = set(unique_keys[n_train:n_train + n_val])
        test_keys = set(unique_keys[n_train + n_val:])

        # Handle edge cases with very few sources
        if not test_keys and total_keys >= 3:
            test_keys.add(unique_keys[-1])
            val_keys.discard(unique_keys[-1])

        splits: Dict[SplitType, List[BaseModel]] = {
            SplitType.TRAIN: [],
            SplitType.VALIDATION: [],
            SplitType.TEST: [],
        }

        for k in train_keys:
            splits[SplitType.TRAIN].extend(groups[k])
        for k in val_keys:
            splits[SplitType.VALIDATION].extend(groups[k])
        for k in test_keys:
            splits[SplitType.TEST].extend(groups[k])

        # Verify zero leakage
        self.verify_no_leakage(train_keys, val_keys, test_keys)

        logger.info(
            f"Partitioned {len(items)} items from {total_keys} sources: "
            f"Train={len(splits[SplitType.TRAIN])} items ({len(train_keys)} sources), "
            f"Val={len(splits[SplitType.VALIDATION])} items ({len(val_keys)} sources), "
            f"Test={len(splits[SplitType.TEST])} items ({len(test_keys)} sources)."
        )

        return splits

    @staticmethod
    def verify_no_leakage(train_sources: Set[str], val_sources: Set[str], test_sources: Set[str]) -> bool:
        train_val_overlap = train_sources.intersection(val_sources)
        train_test_overlap = train_sources.intersection(test_sources)
        val_test_overlap = val_sources.intersection(test_sources)

        if train_val_overlap or train_test_overlap or val_test_overlap:
            raise ValueError(
                f"Data leakage detected! Cross-contamination across splits: "
                f"Train/Val: {train_val_overlap}, Train/Test: {train_test_overlap}, Val/Test: {val_test_overlap}"
            )
        return True

