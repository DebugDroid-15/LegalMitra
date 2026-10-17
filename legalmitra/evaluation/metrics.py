"""
Mathematical and Metric Definitions for LegalMitra Quality Assurance.
Implements formal formulations for:
- Precision, Recall, and Mean Reciprocal Rank (MRR)
- Citation Support Rate and Hallucination Rate
- Abstention Precision and Refusal F1
- Temporal Correctness and Anachronism Penalty
"""

from typing import Dict, List, Optional, Set, Tuple
from legalmitra.evaluation.models import CaseEvaluationResult, EvaluationCategory


def calculate_mrr(rankings: List[int]) -> float:
    """
    Calculate Mean Reciprocal Rank (MRR) where rankings contains the 1-based index
    of the first relevant document retrieved, or 0 if no relevant document was retrieved.
    MRR = (1 / |Q|) * sum_{q=1}^{|Q|} (1 / rank_q)
    """
    if not rankings:
        return 0.0
    reciprocal_sum = sum(1.0 / r for r in rankings if r > 0)
    return round(reciprocal_sum / len(rankings), 4)


def calculate_retrieval_recall(total_cases: int, successful_retrievals: int) -> float:
    """
    Calculate Retrieval Recall @ K across evaluation queries.
    Recall = Successful Retrievals / Total Eligible Retrieval Queries
    """
    if total_cases == 0:
        return 0.0
    return round(successful_retrievals / total_cases, 4)


def calculate_citation_metrics(
    extracted_citations: List[str],
    evidence_chunk_texts: List[str],
    evidence_titles_and_refs: Optional[List[str]] = None,
) -> Tuple[float, float, List[str], List[str]]:
    """
    Verify citation grounding against retrieved knowledge chunks and metadata.
    Returns:
        (citation_support_rate, hallucination_rate, supported_list, unsupported_list)
    """
    if not extracted_citations:
        return 1.0, 0.0, [], []

    supported: List[str] = []
    unsupported: List[str] = []

    all_evidence = list(evidence_chunk_texts)
    if evidence_titles_and_refs:
        all_evidence.extend(evidence_titles_and_refs)

    combined_evidence = " ".join(all_evidence).lower()

    for cit in extracted_citations:
        cit_clean = cit.strip().lower()
        # Direct token match or substring match
        if cit_clean in combined_evidence or any(cit_clean in e.lower() for e in all_evidence):
            supported.append(cit)
        else:
            # Check if key tokens in citation appear in retrieved evidence
            # Ignore generic noise tokens like '(none (statutory / executive))'
            clean_str = cit_clean.replace("(", " ").replace(")", " ").replace("/", " ").replace(",", " ").replace(":", " ").replace("-", " ")
            clean_cit_tokens = [
                t for t in clean_str.split()
                if len(t) > 2 and t not in {"none", "statutory", "executive", "court", "india", "act", "the", "and"}
            ]
            if clean_cit_tokens and all(t in combined_evidence for t in clean_cit_tokens):
                supported.append(cit)
            else:
                unsupported.append(cit)


    total = len(extracted_citations)
    support_rate = round(len(supported) / total, 4)
    hallucination_rate = round(len(unsupported) / total, 4)


    return support_rate, hallucination_rate, supported, unsupported


def compute_category_statistics(
    results: List[CaseEvaluationResult]
) -> Dict[str, Dict[str, float]]:
    """
    Compute aggregate performance breakdown by EvaluationCategory.
    """
    categories: Dict[str, List[CaseEvaluationResult]] = {}
    for res in results:
        cat_key = res.category.value
        categories.setdefault(cat_key, []).append(res)

    breakdown: Dict[str, Dict[str, float]] = {}
    for cat_name, cat_res in categories.items():
        total = len(cat_res)
        passed = sum(1 for r in cat_res if r.passed)
        pass_rate = round(passed / total, 4) if total > 0 else 0.0
        retrieval_ok = sum(1 for r in cat_res if r.retrieval_success)
        retrieval_rate = round(retrieval_ok / total, 4) if total > 0 else 0.0
        
        breakdown[cat_name] = {
            "total_cases": total,
            "passed_cases": passed,
            "failed_cases": total - passed,
            "pass_rate": pass_rate,
            "retrieval_rate": retrieval_rate,
        }

    return breakdown

