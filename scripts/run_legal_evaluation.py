"""
LegalMitra CLI tool to run independent legal evaluation suite against verified corpus.
"""

import argparse
import json
import sys
from pathlib import Path

from legalmitra.core.logging import get_logger
from legalmitra.evaluation.dataset import EvaluationDataset
from legalmitra.evaluation.runner import LegalEvaluationRunner
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase

logger = get_logger("run_legal_evaluation")


def main():
    parser = argparse.ArgumentParser(description="LegalMitra Independent Legal Quality Evaluator")
    parser.add_argument("--dataset", default="data/12_evaluation/evaluation_cases_v1.json", help="Path to evaluation dataset JSON")
    parser.add_argument("--output", default="data/12_evaluation/evaluation_results.json", help="Path to output summary results JSON")
    parser.add_argument("--category", default=None, help="Filter by specific category")
    args = parser.parse_args()

    print(f"Loading evaluation dataset from {args.dataset}...")
    dataset = EvaluationDataset.load_from_json(args.dataset)
    cases = dataset.cases

    if args.category:
        cases = [c for c in cases if c.category.value == args.category]
        print(f"Filtered to {len(cases)} cases matching category '{args.category}'")

    print(f"Initializing LegalEvaluationRunner...")
    kb = LegalKnowledgeBase()
    runner = LegalEvaluationRunner(kb=kb)

    print(f"Executing evaluation across {len(cases)} benchmark cases...")
    report = runner.evaluate_suite(cases)

    print("\n" + "=" * 60)
    print("LEGALMITRA EVALUATION RESULTS SUMMARY")
    print("=" * 60)
    print(f"Total Cases Evaluated:       {report.total_cases}")
    print(f"Passed Cases:                {report.passed_cases}")
    print(f"Failed Cases:                {report.failed_cases}")
    print(f"Overall Pass Rate:           {report.overall_pass_rate * 100:.2f}%")
    print(f"Retrieval Recall @ K:        {report.retrieval_recall_at_k * 100:.2f}%")
    print(f"Mean Reciprocal Rank (MRR):  {report.mean_reciprocal_rank:.4f}")
    print(f"Citation Support Rate:       {report.citation_support_rate * 100:.2f}%")
    print(f"Hallucination Rate:          {report.hallucination_rate * 100:.2f}%")
    print(f"Abstention Precision:        {report.abstention_precision * 100:.2f}%")
    print(f"Temporal Correctness Rate:   {report.temporal_correctness_rate * 100:.2f}%")
    print(f"Adversarial Robustness Rate: {report.adversarial_robustness_rate * 100:.2f}%")
    print(f"Privacy Compliance Rate:     {report.privacy_compliance_rate * 100:.2f}%")
    print(f"Release Gate Verdict:        {report.release_gate_status}")
    print("=" * 60)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(report.model_dump(mode="json"), indent=2, ensure_ascii=False))
    print(f"Saved evaluation report to {args.output}")

    if report.release_gate_status == "NO-GO":
        print("WARNING: Release gate is NO-GO.")


if __name__ == "__main__":
    main()

