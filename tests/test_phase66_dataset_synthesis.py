"""
Tests for Phase 66 External Data Ingestion & Instruction Dataset Synthesis.
Verifies:
  1. Integrity, counts, and schema of external KanoonGPT case extraction.
  2. Synthesized instruction dataset schemas (train, val, ShareGPT).
  3. Strict zero-leakage of test fixtures and scaffold quarantine enforcement.
  4. Kaggle fine-tuning notebook validity and configuration.
"""

import json
from pathlib import Path
import pytest

OUTPUT_DIR = Path("data/23_external_training")
KAN_CASES_PATH = OUTPUT_DIR / "kanoongpt_normalized_cases.jsonl"
TRAIN_DATASET_PATH = OUTPUT_DIR / "legal_instructions_train.jsonl"
VAL_DATASET_PATH = OUTPUT_DIR / "legal_instructions_val.jsonl"
SHAREGPT_PATH = OUTPUT_DIR / "legal_instructions_sharegpt.json"
NOTEBOOK_PATH = Path("kaggle/legalmitra_qlora_training.ipynb")


class TestPhase66DatasetSynthesisAndKagglePipeline:
    """Verifies all Phase 66 deliverables and datasets."""

    def test_kanoongpt_extracted_cases_integrity(self):
        """Verify that external KanoonGPT cases exist and have valid structure."""
        assert KAN_CASES_PATH.exists(), f"Missing {KAN_CASES_PATH}"

        with open(KAN_CASES_PATH, "r", encoding="utf-8") as f:
            cases = [json.loads(line) for line in f if line.strip()]

        assert len(cases) >= 100, f"Expected >= 100 cases, found {len(cases)}"

        sample = cases[0]
        required_keys = ["external_case_id", "title", "court", "decision_date", "ratio_summary", "text_excerpt"]
        for k in required_keys:
            assert k in sample, f"Missing key {k} in KanoonGPT sample"
            assert sample[k] is not None

        # Verify no synthetic test scaffold has leaked into external cases
        for c in cases:
            assert "IND-JUD-DEL-2024-BAIL" not in c["external_case_id"]

    def test_instruction_datasets_exist_and_partitioned(self):
        """Verify train and validation splits exist with proper proportions."""
        assert TRAIN_DATASET_PATH.exists()
        assert VAL_DATASET_PATH.exists()
        assert SHAREGPT_PATH.exists()

        with open(TRAIN_DATASET_PATH, "r", encoding="utf-8") as f:
            train_records = [json.loads(line) for line in f if line.strip()]

        with open(VAL_DATASET_PATH, "r", encoding="utf-8") as f:
            val_records = [json.loads(line) for line in f if line.strip()]

        assert len(train_records) >= 1500, f"Train set should have >= 1500 records, got {len(train_records)}"
        assert len(val_records) >= 150, f"Val set should have >= 150 records, got {len(val_records)}"

        # Verify schema
        for r in train_records[:50]:
            assert "instruction" in r and len(r["instruction"]) > 10
            assert "context" in r and len(r["context"]) > 10
            assert "response" in r and len(r["response"]) > 20
            assert "metadata" in r

    def test_zero_quarantined_scaffold_in_training_sets(self):
        """Verify that quarantined scaffold IND-JUD-DEL-2024-BAIL is NOT used as positive training example."""
        with open(TRAIN_DATASET_PATH, "r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                meta = data.get("metadata", {})
                # Positive examples must never use scaffold chunk
                if meta.get("source_type") in ("statute", "case_law"):
                    assert "IND-JUD-DEL-2024-BAIL" not in str(meta)
                    assert "IND-JUD-DEL-2024-BAIL" not in data.get("context", "")

    def test_sharegpt_format_validity(self):
        """Verify that ShareGPT JSON conforms to multi-turn conversation specification."""
        with open(SHAREGPT_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert isinstance(data, list)
        assert len(data) >= 1600

        sample = data[0]
        assert "conversations" in sample
        assert len(sample["conversations"]) == 2
        assert sample["conversations"][0]["from"] == "human"
        assert sample["conversations"][1]["from"] == "gpt"

    def test_kaggle_notebook_structure_and_cells(self):
        """Verify that the Kaggle QLoRA notebook is valid JSON and contains all required training steps."""
        assert NOTEBOOK_PATH.exists(), f"Missing {NOTEBOOK_PATH}"

        with open(NOTEBOOK_PATH, "r", encoding="utf-8") as f:
            nb = json.load(f)

        assert "cells" in nb
        assert len(nb["cells"]) >= 7

        code_cells = [c for c in nb["cells"] if c.get("cell_type") == "code"]
        assert len(code_cells) >= 6

        # Check for key ML libraries and functions
        all_code = "".join("".join(c.get("source", [])) for c in code_cells)
        assert "FastLanguageModel" in all_code
        assert "SFTTrainer" in all_code
        assert "save_pretrained" in all_code
        assert "Meta-Llama-3.1-8B" in all_code
