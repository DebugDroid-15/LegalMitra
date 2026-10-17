"""
Phase 23 National Legal Evaluation Suite Runner
Executes LegalEvaluationRunner across all 26 cases in data/13_evaluation/evaluation_cases_v2.json.
Outputs:
- data/13_evaluation/evaluation_results_v2.json
"""

import json
from pathlib import Path
from legalmitra.evaluation.dataset import EvaluationDataset
from legalmitra.evaluation.runner import LegalEvaluationRunner


def run_phase23_eval():
    dataset_path = "data/13_evaluation/evaluation_cases_v2.json"
    output_path = Path("data/13_evaluation/evaluation_results_v2.json")

    print(f"Loading benchmark suite v2 from {dataset_path}...")
    dataset = EvaluationDataset.load_from_json(dataset_path)
    print(f"Loaded {len(dataset.cases)} evaluation cases.")

    runner = LegalEvaluationRunner()
    print("Executing evaluation suite across all cases...")
    report = runner.evaluate_suite(dataset.cases)

    report_dict = report.model_dump(mode="json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report_dict, f, indent=2, ensure_ascii=False)

    print(f"\n=== Evaluation Suite v2 Completed ===")
    print(f"Total Cases: {report.total_cases}")
    print(f"Passed Cases: {report.passed_cases}")
    print(f"Failed Cases: {report.failed_cases}")
    print(f"Overall Pass Rate: {report.overall_pass_rate * 100:.2f}%")
    print(f"Retrieval Recall @ K: {report.retrieval_recall_at_k * 100:.2f}%")
    print(f"Mean Reciprocal Rank (MRR): {report.mean_reciprocal_rank:.4f}")
    print(f"Citation Support Rate: {report.citation_support_rate * 100:.2f}%")
    print(f"Hallucination Rate: {report.hallucination_rate * 100:.2f}%")
    print(f"Abstention Precision: {report.abstention_precision * 100:.2f}%")
    print(f"Temporal Correctness Rate: {report.temporal_correctness_rate * 100:.2f}%")
    print(f"Adversarial Robustness Rate: {report.adversarial_robustness_rate * 100:.2f}%")
    print(f"Privacy Compliance Rate: {report.privacy_compliance_rate * 100:.2f}%")
    print(f"Blocking Defects: {report.blocking_defects_count}")
    print(f"Release Gate Verdict: {report.release_gate_status}")
    print(f"Saved complete report to {output_path}")

    return report


if __name__ == "__main__":
    run_phase23_eval()

