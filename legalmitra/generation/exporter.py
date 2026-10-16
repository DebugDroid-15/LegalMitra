"""
LegalMitra Generation Exporter
Exports generation results and reports in various formats.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

from legalmitra.core.logging import get_logger
from legalmitra.generation.schemas import GenerationSummary, GenerationResult, TaskType

logger = get_logger("generation_exporter")


class GenerationExporter:
    """Exports generation results, summaries, and reports."""
    
    def __init__(self, output_dir: str = "data/03_generated"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir = self.output_dir / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def export_summary(self, summary: GenerationSummary, filename: Optional[str] = None) -> Path:
        """Export generation summary as JSON."""
        if filename is None:
            filename = f"generation_summary_{summary.run_id}_{summary.started_at.strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = self.reports_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(summary.model_dump(), f, indent=2, default=str)
        
        logger.info(f"Exported generation summary to {filepath}")
        return filepath
    
    def export_markdown_report(self, summary: GenerationSummary, filename: Optional[str] = None) -> Path:
        """Export human-readable markdown generation report."""
        if filename is None:
            filename = f"generation_report_{summary.run_id}_{summary.started_at.strftime('%Y%m%d_%H%M%S')}.md"
        
        filepath = self.reports_dir / filename
        
        lines = [
            "# LegalMitra Generation Run Report",
            f"**Run ID**: {summary.run_id}",
            f"**Started**: {summary.started_at.isoformat()}",
            f"**Completed**: {summary.completed_at.isoformat() if summary.completed_at else 'In Progress'}",
            f"**Duration**: {summary.total_duration_seconds:.1f}s",
            "",
            "## Summary Metrics",
            f"- **Total Sources**: {summary.total_sources}",
            f"- **Sources Processed**: {summary.sources_processed}",
            f"- **Total Tasks**: {summary.total_tasks}",
            f"- **Tasks Completed**: {summary.tasks_completed}",
            f"- **Tasks Failed**: {summary.tasks_failed}",
            f"- **Examples Generated**: {summary.total_examples_generated}",
            f"- **Examples Validated**: {summary.total_examples_validated}",
            f"- **Examples Rejected**: {summary.total_examples_rejected}",
            f"- **Total Tokens**: {summary.total_tokens:,} (prompt: {summary.total_prompt_tokens:,}, completion: {summary.total_completion_tokens:,})",
            f"- **Estimated Cost**: ${summary.total_cost_estimate_usd:.4f}",
            "",
            "## Task Type Breakdown",
        ]
        
        for task_type, stats in summary.task_type_breakdown.items():
            lines.append(f"### {task_type}")
            lines.append(f"- Completed: {stats.get('completed', 0)}")
            lines.append(f"- Failed: {stats.get('failed', 0)}")
            lines.append(f"- Examples: {stats.get('examples', 0)}")
            lines.append("")
        
        lines.append("## Source Breakdown")
        for source_id, stats in summary.source_breakdown.items():
            lines.append(f"### {source_id}")
            lines.append(f"- Completed: {stats.get('completed', 0)}")
            lines.append(f"- Failed: {stats.get('failed', 0)}")
            lines.append(f"- Examples: {stats.get('examples', 0)}")
            lines.append("")
        
        if summary.errors:
            lines.append("## Errors")
            for error in summary.errors:
                lines.append(f"- {error}")
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
        logger.info(f"Exported markdown report to {filepath}")
        return filepath
    
    def export_results_jsonl(
        self,
        results: List[GenerationResult],
        filename: Optional[str] = None,
    ) -> Path:
        """Export individual task results as JSONL."""
        if filename is None:
            filename = f"generation_results_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.jsonl"
        
        filepath = self.reports_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            for result in results:
                f.write(json.dumps(result.model_dump(), default=str) + "\n")
        
        logger.info(f"Exported {len(results)} task results to {filepath}")
        return filepath
    
    def export_failed_tasks(
        self,
        results: List[GenerationResult],
        filename: Optional[str] = None,
    ) -> Path:
        """Export only failed tasks for review."""
        if filename is None:
            filename = f"generation_failures_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.jsonl"
        
        filepath = self.reports_dir / filename
        failed = [r for r in results if not r.success]
        
        with open(filepath, "w", encoding="utf-8") as f:
            for result in failed:
                f.write(json.dumps(result.model_dump(), default=str) + "\n")
        
        logger.info(f"Exported {len(failed)} failed tasks to {filepath}")
        return filepath
    
    def export_ungrounded_examples(
        self,
        results: List[GenerationResult],
        filename: Optional[str] = None,
    ) -> Path:
        """Export examples flagged as ungrounded for legal review."""
        if filename is None:
            filename = f"ungrounded_examples_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.jsonl"
        
        filepath = self.reports_dir / filename
        ungrounded = []
        
        for result in results:
            if result.success:
                for ex in result.examples_generated:
                    if ex.get("flagged_unsupported") or ex.get("legal_review_status") == "flagged_unsupported":
                        ex["_generation_task_id"] = result.task_id
                        ex["_generation_source_id"] = result.source_id
                        ex["_generation_task_type"] = result.task_type.value if hasattr(result.task_type, 'value') else str(result.task_type)
                        ungrounded.append(ex)
        
        with open(filepath, "w", encoding="utf-8") as f:
            for ex in ungrounded:
                f.write(json.dumps(ex, default=str) + "\n")
        
        logger.info(f"Exported {len(ungrounded)} ungrounded examples to {filepath}")
        return filepath
    
    def export_generation_quality_report(
        self,
        summary: GenerationSummary,
        results: List[GenerationResult],
        filename: Optional[str] = None,
    ) -> Path:
        """Export detailed quality metrics report distinguishing all categories."""
        if filename is None:
            filename = f"generation_quality_report_{summary.run_id}_{summary.started_at.strftime('%Y%m%d_%H%M%S')}.md"
        
        filepath = self.reports_dir / filename
        
        # Count categories
        total_generated = summary.total_examples_generated
        total_validated = summary.total_examples_validated
        total_rejected = summary.total_examples_rejected
        total_failed_tasks = summary.tasks_failed
        
        # Categorize by validation status
        structurally_valid = 0
        grounding_pass = 0
        grounding_fail = 0
        pending_review = 0
        flagged_unsupported = 0
        
        for result in results:
            if result.success:
                for ex in result.examples_generated:
                    structurally_valid += 1
                    if ex.get("flagged_unsupported"):
                        flagged_unsupported += 1
                        grounding_fail += 1
                    else:
                        grounding_pass += 1
                    
                    status = ex.get("legal_review_status", "unverified_automated")
                    if status == "pending_legal_review":
                        pending_review += 1
        
        lines = [
            "# LegalMitra Generation Quality Report",
            f"**Run ID**: {summary.run_id}",
            f"**Date**: {summary.started_at.strftime('%Y-%m-%d %H:%M:%S UTC')}",
            "",
            "## Generation Pipeline Metrics",
            "| Metric | Count |",
            "|---|---|",
            f"| Sources Discovered | {summary.total_sources} |",
            f"| Sources Successfully Processed | {summary.sources_processed} |",
            f"| Documents Normalized (pre-gen) | N/A (pre-existing) |",
            f"| Generation Tasks Created | {summary.total_tasks} |",
            f"| Tasks Completed | {summary.tasks_completed} |",
            f"| Tasks Failed | {summary.tasks_failed} |",
            f"| Examples Generated | {total_generated} |",
            f"| Examples Passing Structural Validation | {structurally_valid} |",
            f"| Examples Passing Grounding Checks | {grounding_pass} |",
            f"| Examples Failing Grounding Checks | {grounding_fail} |",
            f"| Examples Requiring Legal Review | {pending_review + flagged_unsupported} |",
            f"| Examples Approved by Legal Expert | 0 (requires manual review) |",
            f"| Examples Rejected by Legal Expert | 0 (requires manual review) |",
            f"| API Failures | {total_failed_tasks} |",
            f"| Extraction Failures (pre-gen) | N/A |",
            f"| Duplicate Records Detected | N/A (deduplicated at schema level) |",
            "",
            "## Per-Task-Type Quality",
            "| Task Type | Tasks | Generated | Validated | Grounding Pass | Grounding Fail | Flagged |",
            "|---|---|---|---|---|---|---|",
        ]
        
        for task_type, stats in summary.task_type_breakdown.items():
            lines.append(
                f"| {task_type} | {stats.get('completed', 0) + stats.get('failed', 0)} | "
                f"{stats.get('examples', 0)} | {stats.get('examples', 0)} | "
                f"TBD | TBD | TBD |"
            )
        
        lines.extend([
            "",
            "## Per-Source Quality",
            "| Source ID | Tasks | Generated |",
            "|---|---|---|",
        ])
        
        for source_id, stats in summary.source_breakdown.items():
            lines.append(f"| {source_id} | {stats.get('completed', 0) + stats.get('failed', 0)} | {stats.get('examples', 0)} |")
        
        lines.extend([
            "",
            "## Token Usage & Cost",
            f"- **Total Prompt Tokens**: {summary.total_prompt_tokens:,}",
            f"- **Total Completion Tokens**: {summary.total_completion_tokens:,}",
            f"- **Total Tokens**: {summary.total_tokens:,}",
            f"- **Estimated Cost**: ${summary.total_cost_estimate_usd:.4f}",
            "",
            "## Notes",
            "- All figures are from automated generation only",
            "- Legal expert review required before any record enters verified dataset",
            "- Grounding validation checks verbatim passage existence only, not legal correctness",
            "- `legal_expert_approved` status requires independent human review",
            "",
            "---",
            "*Report generated by LegalMitra Generation Engine*",
        ])
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
        logger.info(f"Exported quality report to {filepath}")
        return filepath


def create_generation_report(
    summary: GenerationSummary,
    results: List[GenerationResult],
    output_dir: str = "data/03_generated",
) -> Dict[str, Path]:
    """Create all standard generation reports."""
    exporter = GenerationExporter(output_dir)
    
    return {
        "summary_json": exporter.export_summary(summary),
        "markdown_report": exporter.export_markdown_report(summary),
        "results_jsonl": exporter.export_results_jsonl(results),
        "failures_jsonl": exporter.export_failed_tasks(results),
        "ungrounded_jsonl": exporter.export_ungrounded_examples(results),
        "quality_report": exporter.export_generation_quality_report(summary, results),
    }