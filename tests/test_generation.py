"""
Tests for LegalMitra Generation Module
"""

import pytest
from legalmitra.generation.prompts import TaskType, get_prompt, GENERATION_PROMPTS
from legalmitra.generation.schemas import (
    GenerationConfig,
    GenerationTask,
    GenerationResult,
    GenerationStatus,
    task_type_to_schema,
    get_output_filename,
)
from legalmitra.generation.validator import GenerationValidator, extract_json_from_response
from legalmitra.generation.orchestrator import run_generation_pipeline
from legalmitra.generation.exporter import GenerationExporter
from legalmitra.schemas.legal_qa import LegalQADocument
from legalmitra.schemas.case_analysis import CaseAnalysisDocument
from legalmitra.schemas.procedural_guide import ProceduralGuidanceDocument
from legalmitra.schemas.drafting_example import DraftingExampleDocument
from legalmitra.ingestion.registry import SourceRegistryManager


class TestGenerationPrompts:
    """Test prompt system."""
    
    def test_all_task_types_have_prompts(self):
        for task_type in TaskType:
            assert task_type in GENERATION_PROMPTS
            prompt = GENERATION_PROMPTS[task_type]
            assert len(prompt) > 100
            assert "Indian law" in prompt or "Indian legal" in prompt
    
    def test_get_prompt(self):
        prompt = get_prompt(TaskType.STATUTORY_QA)
        assert "statutory question-answer" in prompt.lower()
    
    def test_build_user_prompt(self):
        from legalmitra.generation.prompts import build_user_prompt
        prompt = build_user_prompt(TaskType.STATUTORY_QA, "test text", "TEST-ID")
        assert "TEST-ID" in prompt
        assert "statutory_qa" in prompt


class TestGenerationSchemas:
    """Test generation schemas."""
    
    def test_generation_config_defaults(self):
        config = GenerationConfig()
        assert config.max_examples_per_source_per_task == 5
        assert config.max_concurrent_requests == 3
        assert TaskType.STATUTORY_QA in config.task_types
    
    def test_generation_config_pilot_mode(self):
        config = GenerationConfig(pilot_mode=True, pilot_max_sources=5)
        assert config.pilot_mode is True
        assert config.pilot_max_sources == 5
    
    def test_generation_task(self):
        task = GenerationTask(
            task_id="test-1",
            source_id="TEST-SRC",
            task_type=TaskType.STATUTORY_QA,
        )
        assert task.status == GenerationStatus.PENDING
        assert task.max_attempts == 3  # default max_retries + 1 (default max_retries=2)
    
    def test_task_type_to_schema(self):
        assert task_type_to_schema(TaskType.STATUTORY_QA) == LegalQADocument
        assert task_type_to_schema(TaskType.JUDGMENT_ANALYSIS) == CaseAnalysisDocument
        assert task_type_to_schema(TaskType.PROCEDURAL_GUIDANCE) == ProceduralGuidanceDocument
        assert task_type_to_schema(TaskType.DRAFTING) == DraftingExampleDocument
    
    def test_get_output_filename(self):
        assert get_output_filename(TaskType.STATUTORY_QA) == "legal_qa.jsonl"
        assert get_output_filename(TaskType.JUDGMENT_ANALYSIS) == "case_analysis.jsonl"
        assert get_output_filename(TaskType.PROCEDURAL_GUIDANCE) == "procedural_guide.jsonl"
        assert get_output_filename(TaskType.DRAFTING) == "drafting_examples.jsonl"


class TestGenerationValidator:
    """Test generation validator."""
    
    def test_extract_json_from_response_bare_array(self):
        response = '[{"qa_id": "test", "question": "q", "answer": "a"}]'
        result = extract_json_from_response(response)
        assert result == response
    
    def test_extract_json_from_response_markdown(self):
        response = '```json\n[{"qa_id": "test"}]\n```'
        result = extract_json_from_response(response)
        assert result == '[{"qa_id": "test"}]'
    
    def test_extract_json_from_response_nested_arrays(self):
        response = '[{"evidence_passages": [{"text": "nested"}]}]'
        result = extract_json_from_response(response)
        assert '"evidence_passages"' in result
        assert '"nested"' in result
    
    def test_validate_generation_output_schema_error(self):
        registry = SourceRegistryManager("registry/source_registry.jsonl")
        validator = GenerationValidator(registry)
        
        # Missing required field
        bad_json = '[{"question": "q", "answer": "a"}]'  # missing qa_id
        docs, errors = validator.validate_generation_output(
            bad_json, TaskType.STATUTORY_QA, {"TEST": "text"}, {"TEST": registry.get("TEST") or None}
        )
        assert len(errors) > 0
        assert len(docs) == 0


class TestGenerationOrchestrator:
    """Test generation orchestrator (dry-run mode)."""
    
    def test_run_generation_dry_run(self):
        config = GenerationConfig(
            dry_run=True,
            pilot_mode=True,
            pilot_max_sources=2,
            pilot_max_examples=5,
            max_retries=1,
            checkpoint_interval=1,
        )
        
        # Use sources that exist in registry
        summary = run_generation_pipeline(
            config=config,
            source_ids=["IND-STAT-BSA-2023-SEC61", "IND-JUD-SC-2017-PUTTASWAMY"],
        )
        
        assert summary.tasks_completed > 0
        assert summary.total_examples_generated > 0
        assert summary.total_duration_seconds >= 0


class TestGenerationExporter:
    """Test generation exporter."""
    
    def test_export_summary(self, tmp_path):
        from legalmitra.generation.schemas import GenerationSummary
        from datetime import datetime
        
        summary = GenerationSummary(
            run_id="test123",
            started_at=datetime.utcnow(),
            total_sources=2,
            total_tasks=4,
            tasks_completed=4,
            tasks_failed=0,
            total_examples_generated=10,
            total_examples_validated=10,
            total_examples_rejected=0,
        )
        
        exporter = GenerationExporter(str(tmp_path))
        path = exporter.export_summary(summary)
        
        assert path.exists()
        import json
        with open(path) as f:
            data = json.load(f)
        assert data["run_id"] == "test123"
    
    def test_export_markdown_report(self, tmp_path):
        from legalmitra.generation.schemas import GenerationSummary
        from datetime import datetime
        
        summary = GenerationSummary(
            run_id="test123",
            started_at=datetime.utcnow(),
            total_sources=2,
            total_tasks=4,
            tasks_completed=4,
            tasks_failed=0,
            total_examples_generated=10,
            total_examples_validated=10,
        )
        
        exporter = GenerationExporter(str(tmp_path))
        path = exporter.export_markdown_report(summary)
        
        assert path.exists()
        content = path.read_text()
        assert "test123" in content
        assert "10" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])