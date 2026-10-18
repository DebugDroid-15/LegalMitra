"""
Custom-Question Failure Audit Runner for LegalMitra Phase 31.
Executes Benchmark v9 against the system, traces each execution step,
applies failure attribution taxonomy, and exports structured traces and failure statistics.
"""

import json
from pathlib import Path
import time
from typing import Any, Dict, List

from legalmitra.evaluation.dataset import EvaluationDataset
from legalmitra.evaluation.failure_attribution import (
    EvaluationTrace,
    FailureCategory,
    attribute_failure,
)
from legalmitra.evaluation.runner import LegalEvaluationRunner
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
from legalmitra.knowledge.models import SearchFilters
from legalmitra.llm.mock_provider import MockLLMProvider
from legalmitra.rag.engine import LegalRAGEngine


def run_custom_question_audit(dataset_path: str = "data/20_evaluation/evaluation_cases_v9.json") -> Dict[str, Any]:
    dataset = EvaluationDataset.load_from_json(dataset_path)
    kb = LegalKnowledgeBase("data/legalmitra_kb.db", must_exist=True)
    rag = LegalRAGEngine(knowledge_base=kb, llm_provider=MockLLMProvider())
    runner = LegalEvaluationRunner(kb=kb, rag_engine=rag)

    traces: List[EvaluationTrace] = []
    failure_counts: Dict[str, int] = {cat.value: 0 for cat in FailureCategory}
    passed_count = 0
    total_count = len(dataset.cases)

    print(f"=== Running Custom-Question Audit on {total_count} cases ===")

    for case in dataset.cases:
        t0 = time.time()
        # Build search filters
        filters = SearchFilters(
            jurisdiction=case.jurisdiction,
            court=case.court,
            as_of_date=case.as_of_date,
        )

        # Retrieval
        retrieved_chunks = kb.search(query=case.question, filters=filters, limit=5)
        retrieved_ids = [c.chunk_id for c in retrieved_chunks]
        provenance = [
            {"source_id": c.source_id, "title": c.act_or_case_title, "ref": c.provision_or_para_ref, "url": c.source_url}
            for c in retrieved_chunks
        ]
        scores = [round(c.score, 2) for c in retrieved_chunks]

        # Check retrieval success
        retrieval_success = False
        if case.should_abstain and case.category in [
            "missing_evidence",
            "unanswerable_missing_evidence",
            "false_legal_premise",
            "adversarial_safety_bypass",
            "prompt_injection",
        ]:
            retrieval_success = True
        else:
            for chunk in retrieved_chunks:
                if case.target_act_or_case.lower() in chunk.act_or_case_title.lower():
                    retrieval_success = True
                    break
                for ref in case.target_sections_or_paras:
                    if ref.lower() in chunk.provision_or_para_ref.lower():
                        retrieval_success = True
                        break

        # Pass conversation history to RAG engine if present
        conv_hist = getattr(case, "conversation_history", [])
        if hasattr(rag, "answer_with_history"):
            rag_resp = rag.answer_with_history(query=case.question, history=conv_hist, filters=filters, limit=5)
        else:
            rag_resp = rag.answer(query=case.question, filters=filters, limit=5)

        eval_res = runner.evaluate_case(case)
        passed = eval_res.passed
        if passed:
            passed_count += 1

        # Check multi-turn miss
        is_turn_miss = bool(conv_hist and not eval_res.retrieval_success)

        # Extract failure attribution
        forbidden_found = [f for f in case.forbidden_terms if f.lower() in rag_resp.answer.lower()]
        priv_violation = eval_res.adversarial_audit.privacy_violation_detected
        inj_success = eval_res.adversarial_audit.injected_override_detected

        primary_fail, secondary_fails = attribute_failure(
            retrieval_success=eval_res.retrieval_success,
            top_k_chunks=retrieved_chunks,
            answer_text=rag_resp.answer,
            sufficiency_verdict=rag_resp.evidence_sufficiency,
            should_abstain=case.should_abstain,
            missing_facts_prompt=rag_resp.missing_facts_prompt,
            unsupported_citations=eval_res.citation_audit.citations_unverified,
            unsupported_claims_count=eval_res.claim_audit.unsupported_claims if eval_res.claim_audit else 0,
            forbidden_terms_found=forbidden_found,
            privacy_violation=priv_violation,
            prompt_injection_success=inj_success,
            is_multi_turn_miss=is_turn_miss,
        )

        if not passed and primary_fail:
            failure_counts[primary_fail.value] += 1
        for sf in secondary_fails:
            if not passed:
                failure_counts[sf.value] += 1

        trace = EvaluationTrace(
            eval_id=case.eval_id,
            turn_id=f"turn_{len(conv_hist) + 1}",
            original_query=case.question,
            normalized_query=case.question.strip(),
            detected_legal_issues=[case.target_act_or_case],
            detected_missing_facts=rag_resp.missing_facts_prompt,
            selected_jurisdiction=case.jurisdiction,
            effective_date=case.as_of_date,
            retrieved_chunk_ids=retrieved_ids,
            retrieved_sources_provenance=provenance,
            retrieval_scores=scores,
            constructed_prompt_redacted=f"[PROMPT with {len(retrieved_chunks)} evidence chunks for: {case.question[:60]}...]",
            provider_model_id=rag_resp.model_used,
            generated_response=rag_resp.answer,
            extracted_claims=[{"text": c.claim_text, "status": c.verification_status.value} for c in rag_resp.claims],
            citation_to_claim_relationships=[],
            verification_decisions={"passed": passed, "reasons": eval_res.failure_reasons},
            abstention_outcome=rag_resp.evidence_sufficiency,
            latency_seconds=round(time.time() - t0, 4),
            primary_failure_cause=primary_fail if not passed else None,
            secondary_failure_causes=secondary_fails if not passed else [],
            passed=passed,
            audit_notes="; ".join(eval_res.failure_reasons) if eval_res.failure_reasons else "All criteria passed",
        )
        traces.append(trace)

    pass_rate = round(passed_count / total_count, 4)
    print(f"\nAudit Finished: {passed_count}/{total_count} Passed ({pass_rate * 100:.2f}%)")
    print("Failure Distribution:")
    for k, v in failure_counts.items():
        if v > 0:
            print(f"  - {k}: {v}")

    # Export traces
    out_dir = Path("data/20_evaluation")
    trace_file = out_dir / "evaluation_traces_v9.json"
    with open(trace_file, "w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in traces], f, indent=2)

    summary = {
        "total_cases": total_count,
        "passed_cases": passed_count,
        "failed_cases": total_count - passed_count,
        "pass_rate": pass_rate,
        "failure_counts": failure_counts,
        "trace_file": str(trace_file),
    }

    results_file = out_dir / "evaluation_results_v9.json"
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    kb.close()
    return summary


if __name__ == "__main__":
    run_custom_question_audit()
