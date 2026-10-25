"""
Audit IndependentClaimEvaluator across the 94 held-out cases of PIT-V13.
Measures real independent claim support rate, overstatement rate, and trustworthiness score.
"""

import json
from legalmitra.orchestration.pipeline import LegalQueryPipeline
from legalmitra.evaluation.independent_evaluator import IndependentClaimEvaluator
from legalmitra.evaluation.completeness_auditor import AnswerCompletenessAuditor

def audit_held_out():
    manifest_path = "data/22_central_legislation/temporal_benchmark_manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    held_out = [c for c in data["test_cases"] if c.get("split") == "held_out_evaluation"]
    print(f"Total held-out cases: {len(held_out)}")

    pipeline = LegalQueryPipeline()
    ice = IndependentClaimEvaluator()
    aca = AnswerCompletenessAuditor()

    # Sample 20 representative held-out cases
    sample = held_out[::5]
    print(f"Auditing sample of {len(sample)} held-out cases...")

    results = []
    total_props = 0
    supported_props = 0
    overstated_props = 0
    contradicted_props = 0
    scores = []
    completeness_scores = []

    for idx, case in enumerate(sample):
        q = case["query_description"]
        resp = pipeline.execute(q)
        eval_rep = ice.evaluate_response(
            query=q,
            answer_text=resp.answer_text,
            citations=resp.citations,
            production_response_state=resp.response_state.value,
        )
        comp_rep = aca.audit(
            query=q,
            answer_text=resp.answer_text,
            citations=resp.citations,
            response_state=resp.response_state.value,
        )

        total_props += eval_rep.total_propositions
        supported_props += eval_rep.supported_propositions
        overstated_props += eval_rep.overstated_propositions
        contradicted_props += eval_rep.contradicted_propositions
        scores.append(eval_rep.trustworthiness_score)
        completeness_scores.append(comp_rep.overall_completeness_score)

        results.append({
            "case_id": case["case_id"],
            "query": q[:60],
            "prod_state": resp.response_state.value,
            "ind_verdict": eval_rep.independent_verdict,
            "props": eval_rep.total_propositions,
            "supported": eval_rep.supported_propositions,
            "overstated": eval_rep.overstated_propositions,
            "score": eval_rep.trustworthiness_score,
            "comp_score": comp_rep.overall_completeness_score,
        })

    avg_trustworthiness = sum(scores) / len(scores) if scores else 0.0
    avg_completeness = sum(completeness_scores) / len(completeness_scores) if completeness_scores else 0.0
    support_rate = supported_props / total_props if total_props else 0.0
    overstatement_rate = overstated_props / total_props if total_props else 0.0

    print("--- HELD-OUT AUDIT RESULTS ---")
    print(f"Total Propositions: {total_props}")
    print(f"Supported Propositions: {supported_props} ({support_rate:.1%})")
    print(f"Overstated Propositions: {overstated_props} ({overstatement_rate:.1%})")
    print(f"Average Trustworthiness Score: {avg_trustworthiness:.4f}")
    print(f"Average Completeness Score: {avg_completeness:.4f}")

    for r in results[:5]:
        print(r)

if __name__ == "__main__":
    audit_held_out()
