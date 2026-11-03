"""
Phase 89 Test Suite: AI Kosh Legal LLM Fine-Tuning & Multi-Task Instruction Dataset
Validates generation of multi-task instruction pairs, DPO preference formatting,
LoRA checkpoint optimization, and non-advisory guardrail enforcement.
"""

from pathlib import Path
import tempfile
import pytest

from legalmitra.training.aikosh_finetuner import (
    AIKoshLegalFineTuner,
    LoRAConfig,
    TrainingMetrics,
)
from legalmitra.training.instruction_generator import (
    AIKoshDatasetGenerator,
    LegalTaskType,
    MultiTaskInstructionPair,
)


class TestPhase89AIKoshFineTuning:

    def test_generate_core_instruction_dataset(self):
        generator = AIKoshDatasetGenerator()
        dataset = generator.generate_core_dataset()

        assert len(dataset) >= 5
        task_types = {item.task_type for item in dataset}
        assert LegalTaskType.STATUTE_SIMPLIFICATION in task_types
        assert LegalTaskType.PROCEDURAL_ROADMAP in task_types
        assert LegalTaskType.TRI_CODE_CROSSWALK in task_types
        assert LegalTaskType.RATIO_EXTRACTION in task_types
        assert LegalTaskType.NON_ADVISORY_GUARDRAIL in task_types

    def test_dpo_preference_pairs_quality(self):
        generator = AIKoshDatasetGenerator()
        dataset = generator.generate_core_dataset()

        for item in dataset:
            # Chosen response should be longer, detailed and include statutory citations
            assert len(item.chosen_response) > len(item.rejected_response)
            assert len(item.chosen_response) > 50
            # Chosen response must not make false 100% guarantee promises
            assert "100% full refund" not in item.chosen_response
            # Rejected responses must be flagged
            assert len(item.rejected_response) > 0

    def test_dataset_jsonl_export(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "test_instructions.jsonl"
            generator = AIKoshDatasetGenerator()
            count = generator.export_dataset_jsonl(out_file)

            assert count >= 5
            assert out_file.exists()
            assert out_file.stat().st_size > 500

    def test_finetuner_lora_and_metrics(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            lora = LoRAConfig(r=8, lora_alpha=16)
            finetuner = AIKoshLegalFineTuner(
                output_dir=tmp_dir,
                lora_config=lora
            )
            dataset = finetuner.dataset_generator.generate_core_dataset()
            metrics = finetuner.train_epoch_step(dataset)

            assert isinstance(metrics, TrainingMetrics)
            assert metrics.train_loss < 0.8
            assert metrics.perplexity > 1.0
            assert metrics.citation_grounding_accuracy >= 80.0

            # Verify adapter_config.json was saved
            config_file = Path(tmp_dir) / "adapter_config.json"
            assert config_file.exists()

    def test_finetuner_response_generation_grounding(self):
        finetuner = AIKoshLegalFineTuner()
        
        # Test 1: Criminal Breach of Trust
        ans1 = finetuner.generate_response("Explain Section 316 BNS Criminal Breach of Trust")
        assert "Section 316 BNS" in ans1
        assert "Section 405 IPC" in ans1

        # Test 2: FIR Refusal Procedure
        ans2 = finetuner.generate_response("police station refuses to register my FIR")
        assert "Section 173(4) BNSS" in ans2
        assert "Section 175(3) BNSS" in ans2

        # Test 3: Emergency Helpline Guardrail
        ans3 = finetuner.generate_response("scammed 50000 rupees on UPI guarantee money back")
        assert "1930" in ans3
        assert "cybercrime.gov.in" in ans3
        assert "No legal intelligence system or advocate can guarantee" in ans3
