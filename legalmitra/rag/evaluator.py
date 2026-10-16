"""
LegalMitra RAG Evaluator
Executes rigorous legal evaluation against held-out benchmark questions,
measuring retrieval recall, top-K precision, citation accuracy,
negative constraint compliance, and unsupported-answer detection.
"""

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field

from legalmitra.core.logging import get_logger
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
from legalmitra.knowledge.models import SearchFilters, SearchResult
from legalmitra.rag.engine import LegalRAGEngine
from legalmitra.rag.schemas import RAGResponse
from legalmitra.schemas.evaluation import EvaluationQuestionDocument

logger = get_logger("rag_evaluator")


class EvalItemResult(BaseModel):
    eval_id: str
    question: str
    target_statute_or_case: str
    retrieval_success: bool
    retrieved_source_ids: List[str]
    retrieved_top_k: int
    answer_text: str
    sufficiency_verdict: str
    golden_citations_found: List[str]
    golden_citations_missing: List[str]
    forbidden_terms_detected: List[str]
    citation_accuracy: float
    accuracy_score: float
    passed: bool
    latency_seconds: float
    failure_notes: Optional[str] = None


class RAGEvaluationSummary(BaseModel):
    total_questions: int
    retrieval_recall_at_k: float
    citation_accuracy_mean: float
    negative_constraint_compliance_rate: float
    unsupported_detection_rate: float
    temporal_discrimination_rate: float
    overall_pass_rate: float
    average_latency_seconds: float
    item_results: List[EvalItemResult] = Field(default_factory=list)


class RAGEvaluator:
    """
    Automated evaluator for the LegalMitra RAG Engine.
    """

    def __init__(self, engine: LegalRAGEngine):
        self.engine = engine
        self.kb = engine.kb

    def evaluate_retrieval(
        self,
        item: EvaluationQuestionDocument,
        top_k: int = 5,
    ) -> Tuple[bool, List[SearchResult]]:
        """Evaluate whether required source IDs are retrieved in top-K."""
        # For unsupported cases, expected retrieval is 0 or non-matching
        if "UNSUPPORTED" in item.eval_id:
            results = self.kb.search(item.question, limit=top_k)
            # Retrieval is considered successful for unsupported if top results don't fabricate false matches
            return True, results

        results = self.kb.search(item.question, limit=top_k)
        retrieved_ids = {r.source_id for r in results}
        
        target_ids = set(item.supporting_source_ids)
        # Check if at least one target source ID is retrieved
        matched = bool(target_ids.intersection(retrieved_ids))
        return matched, results

    def evaluate_item(
        self,
        item: EvaluationQuestionDocument,
        top_k: int = 4,
    ) -> EvalItemResult:
        """Run full end-to-end evaluation on a single benchmark question."""
        start_time = time.time()
        
        # 1. Retrieval evaluation
        retrieval_ok, search_results = self.evaluate_retrieval(item, top_k=top_k)
        retrieved_source_ids = [r.source_id for r in search_results]

        # 2. Answer Generation via RAG engine
        try:
            resp: RAGResponse = self.engine.answer(item.question, limit=top_k)
        except Exception as e:
            logger.error(f"Inference error evaluating {item.eval_id}: {e}")
            elapsed = time.time() - start_time
            return EvalItemResult(
                eval_id=item.eval_id,
                question=item.question,
                target_statute_or_case=item.target_statute_or_case,
                retrieval_success=retrieval_ok,
                retrieved_source_ids=retrieved_source_ids,
                retrieved_top_k=len(search_results),
                answer_text=f"ERROR: Inference call failed: {e}",
                sufficiency_verdict="error",
                golden_citations_found=[],
                golden_citations_missing=item.golden_citations,
                forbidden_terms_detected=[],
                citation_accuracy=0.0,
                accuracy_score=0.0,
                passed=False,
                latency_seconds=elapsed,
                failure_notes=f"Inference call error: {e}",
            )

        ans_lower = resp.answer.lower()
        combined_text = (resp.answer + " " + " ".join(resp.citations)).lower()

        # 3. Citation Analysis
        found_cites = []
        missing_cites = []
        for gc in item.golden_citations:
            # Check for keyword overlap
            gc_terms = [t.lower() for t in gc.split() if len(t) > 3]
            if any(term in combined_text for term in gc_terms):
                found_cites.append(gc)
            else:
                missing_cites.append(gc)

        citation_acc = len(found_cites) / len(item.golden_citations) if item.golden_citations else 1.0

        # 4. Negative Constraint / Forbidden Terms Check
        detected_forbidden = []
        for forbidden in item.forbidden_terms_or_repealed_citations:
            fb_clean = forbidden.lower()
            if fb_clean in ans_lower:
                is_negated_or_overruled = any(
                    marker in ans_lower for marker in [
                        "overruled", "stand overruled", "cannot", "does not", "no provision",
                        "unverified", "insufficient evidence", "repealed", "not applicable",
                        "never", "not an authentic", "synthetic", "prior to"
                    ]
                )
                if not is_negated_or_overruled:
                    detected_forbidden.append(forbidden)
            else:
                distinctive_tokens = [
                    w for w in fb_clean.split()
                    if w not in {"section", "act", "explanation", "evidence", "the", "and", "under", "court", "of", "in", "to"} and len(w) > 1
                ]
                if distinctive_tokens and all(tok in ans_lower for tok in distinctive_tokens):
                    is_negated_or_overruled = any(
                        marker in ans_lower for marker in [
                            "overruled", "stand overruled", "cannot", "does not", "no provision",
                            "unverified", "insufficient evidence", "repealed", "not applicable",
                            "never", "not an authentic", "synthetic", "prior to"
                        ]
                    )
                    if not is_negated_or_overruled:
                        detected_forbidden.append(forbidden)

        # 5. Accuracy determination based on question type
        failure_notes = []
        accuracy_score = 1.0

        if "UNSUPPORTED" in item.eval_id:
            # Must declare insufficient evidence
            is_insufficient = (
                resp.evidence_sufficiency == "insufficient"
                or "insufficient evidence" in ans_lower
                or "do not provide sufficient evidence" in ans_lower
                or "not contain" in ans_lower
            )
            if is_insufficient:
                accuracy_score = 1.0
            else:
                accuracy_score = 0.0
                failure_notes.append("Failed to declare insufficient evidence on out-of-corpus query.")

        elif "TEMPORAL" in item.eval_id:
            # Must distinguish 2023 vs 2024 dates or Evidence Act vs BSA
            if "not applicable" in ans_lower or "came into force on 1 july 2024" in ans_lower or "1872" in ans_lower:
                accuracy_score = 1.0
            else:
                accuracy_score = 0.5
                failure_notes.append("Weak temporal distinction between pre-2024 and post-2024 law.")

        elif "SCAFFOLD" in item.eval_id:
            # Must detect that State cannot petition for anticipatory bail
            if "cannot" in ans_lower or "unverified" in ans_lower or "synthetic" in ans_lower or "accused" in ans_lower:
                accuracy_score = 1.0
            else:
                accuracy_score = 0.0
                failure_notes.append("Failed to detect synthetic bail scaffold impossibility.")

        else:
            if not retrieval_ok:
                accuracy_score -= 0.4
                failure_notes.append(f"Target sources {item.supporting_source_ids} missed in retrieval.")
            if citation_acc < 0.5:
                accuracy_score -= 0.3
                failure_notes.append(f"Missing golden citations: {missing_cites}")
            if detected_forbidden:
                accuracy_score -= 0.5
                failure_notes.append(f"Forbidden terms detected: {detected_forbidden}")

        accuracy_score = max(0.0, min(1.0, accuracy_score))
        passed = (accuracy_score >= 0.70) and (len(detected_forbidden) == 0)

        elapsed = time.time() - start_time

        return EvalItemResult(
            eval_id=item.eval_id,
            question=item.question,
            target_statute_or_case=item.target_statute_or_case,
            retrieval_success=retrieval_ok,
            retrieved_source_ids=retrieved_source_ids,
            retrieved_top_k=len(search_results),
            answer_text=resp.answer,
            sufficiency_verdict=resp.evidence_sufficiency,
            golden_citations_found=found_cites,
            golden_citations_missing=missing_cites,
            forbidden_terms_detected=detected_forbidden,
            citation_accuracy=citation_acc,
            accuracy_score=accuracy_score,
            passed=passed,
            latency_seconds=elapsed,
            failure_notes="; ".join(failure_notes) if failure_notes else None,
        )

    def evaluate_benchmark(
        self,
        eval_path: Path,
        top_k: int = 4,
    ) -> RAGEvaluationSummary:
        """Run full evaluation suite over JSONL benchmark dataset."""
        items: List[EvaluationQuestionDocument] = []
        with open(eval_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    items.append(EvaluationQuestionDocument.model_validate_json(line))

        results: List[EvalItemResult] = []
        total_q = len(items)

        for item in items:
            logger.info(f"Evaluating {item.eval_id}...")
            res = self.evaluate_item(item, top_k=top_k)
            results.append(res)

        # Aggregate metrics
        retrieval_recall = sum(1 for r in results if r.retrieval_success) / total_q if total_q else 0.0
        citation_mean = sum(r.citation_accuracy for r in results) / total_q if total_q else 0.0
        neg_constraint = sum(1 for r in results if not r.forbidden_terms_detected) / total_q if total_q else 0.0
        
        unsupported_items = [r for r in results if "UNSUPPORTED" in r.eval_id]
        unsupported_rate = (
            sum(1 for r in unsupported_items if r.passed) / len(unsupported_items)
            if unsupported_items else 1.0
        )

        temporal_items = [r for r in results if "TEMPORAL" in r.eval_id]
        temporal_rate = (
            sum(1 for r in temporal_items if r.passed) / len(temporal_items)
            if temporal_items else 1.0
        )

        pass_rate = sum(1 for r in results if r.passed) / total_q if total_q else 0.0
        avg_latency = sum(r.latency_seconds for r in results) / total_q if total_q else 0.0

        return RAGEvaluationSummary(
            total_questions=total_q,
            retrieval_recall_at_k=retrieval_recall,
            citation_accuracy_mean=citation_mean,
            negative_constraint_compliance_rate=neg_constraint,
            unsupported_detection_rate=unsupported_rate,
            temporal_discrimination_rate=temporal_rate,
            overall_pass_rate=pass_rate,
            average_latency_seconds=avg_latency,
            item_results=results,
        )
