"""
Tests for LegalMitra Dataset Partitioner.
Verifies strict partition by source document and case family with zero data leakage.
"""

import pytest

from legalmitra.core.enums import SplitType
from legalmitra.dataset.partitioner import DatasetPartitioner
from legalmitra.schemas.statute import StatuteSection


def test_partitioner_strict_source_grouping():
    partitioner = DatasetPartitioner(train_ratio=0.6, val_ratio=0.2, test_ratio=0.2, seed=42)

    # Create 10 sections belonging to 5 different sources (2 sections per source)
    items = []
    for s_idx in range(1, 6):
        source_id = f"IND-STAT-SOURCE-{s_idx}"
        for sec_num in [1, 2]:
            items.append(
                StatuteSection(
                    section_id=f"{source_id}-SEC-{sec_num}",
                    source_id=source_id,
                    act_title=f"Act {s_idx}",
                    section_number=str(sec_num),
                    section_title=f"Section {sec_num}",
                    full_verbatim_text=f"Content for {source_id} sec {sec_num}",
                )
            )

    splits = partitioner.partition_by_source(items, source_id_field="source_id")

    train_items = splits[SplitType.TRAIN]
    val_items = splits[SplitType.VALIDATION]
    test_items = splits[SplitType.TEST]

    train_sources = {item.source_id for item in train_items}
    val_sources = {item.source_id for item in val_items}
    test_sources = {item.source_id for item in test_items}

    # Verify that total items equal original items
    assert len(train_items) + len(val_items) + len(test_items) == len(items)

    # Crucial assertion: Zero source leakage across splits!
    assert len(train_sources.intersection(val_sources)) == 0
    assert len(train_sources.intersection(test_sources)) == 0
    assert len(val_sources.intersection(test_sources)) == 0


def test_partitioner_detects_leakage():
    with pytest.raises(ValueError, match="Data leakage detected"):
        DatasetPartitioner.verify_no_leakage(
            train_sources={"SRC-A", "SRC-B"},
            val_sources={"SRC-B", "SRC-C"},  # SRC-B is leaked!
            test_sources={"SRC-D"},
        )

