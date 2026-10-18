"""
Phase 31 Custom-Question Intelligence Regression Tests.
Verifies Benchmark v9 integrity, 15 evaluation categories, failure attribution taxonomy,
multi-turn anaphora resolution, and false premise refutation.
"""

import json
from pathlib import Path
import pytest

from legalmitra.evaluation.dataset import EvaluationDataset
from legalmitra.evaluation.failure_attribution import FailureCategory, attribute_failure
from legalmitra.evaluation.models import EvaluationCategory
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
from legalmitra.llm.mock_provider import MockLLMProvider
from legalmitra.rag.engine import LegalRAGEngine


def test_benchmark_v9_manifest_and_case_count():
    manifest_path = Path("data/20_evaluation/manifest_v9.json")
    cases_path = Path("data/20_evaluation/evaluation_cases_v9.json")
    assert manifest_path.exists(), "Benchmark v9 manifest missing"
    assert cases_path.exists(), "Benchmark v9 cases missing"

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    assert manifest["version"].startswith("v9")
    assert manifest["total_cases"] == 96
    assert len(manifest["category_counts"]) == 15

    dataset = EvaluationDataset.load_from_json(str(cases_path))
    assert len(dataset.cases) == 96


def test_all_15_evaluation_categories_present():
    expected_categories = [
        "single_provision",
        "multi_provision",
        "multi_turn_context",
        "missing_ambiguous_facts",
        "multi_jurisdiction",
        "commencement_amendment",
        "overruled_precedent",
        "statute_precedent_synthesis",
        "procedural_deadlines",
        "multi_domain_scenario",
        "legal_remedies_steps",
        "false_legal_premise",
        "unanswerable_missing_evidence",
        "cautious_explanation",
        "adversarial_safety_bypass",
    ]
    actual_values = [cat.value for cat in EvaluationCategory]
    for expected in expected_categories:
        assert expected in actual_values, f"Missing category: {expected}"


def test_failure_attribution_taxonomy():
    # 1. Retrieval miss
    f_cat, _ = attribute_failure(
        retrieval_success=False,
        top_k_chunks=[],
        answer_text="Insufficient evidence.",
        sufficiency_verdict="insufficient",
        should_abstain=False,
        missing_facts_prompt=None,
        unsupported_citations=[],
        unsupported_claims_count=0,
        forbidden_terms_found=[],
        privacy_violation=False,
        prompt_injection_success=False,
    )
    assert f_cat == FailureCategory.RETRIEVAL_MISS

    # 2. Abstention failure (answered when should abstain)
    f_cat2, _ = attribute_failure(
        retrieval_success=True,
        top_k_chunks=[],
        answer_text="Here is the detailed legal answer based on nonexistent provisions.",
        sufficiency_verdict="sufficient",
        should_abstain=True,
        missing_facts_prompt=None,
        unsupported_citations=[],
        unsupported_claims_count=0,
        forbidden_terms_found=[],
        privacy_violation=False,
        prompt_injection_success=False,
    )
    assert f_cat2 == FailureCategory.ABSTENTION_FAILURE

    # 3. Privacy violation
    f_cat3, _ = attribute_failure(
        retrieval_success=True,
        top_k_chunks=[],
        answer_text="Victim name is ABC.",
        sufficiency_verdict="sufficient",
        should_abstain=True,
        missing_facts_prompt=None,
        unsupported_citations=[],
        unsupported_claims_count=0,
        forbidden_terms_found=[],
        privacy_violation=True,
        prompt_injection_success=False,
    )
    assert f_cat3 == FailureCategory.PRIVACY_OR_SECURITY_FAILURE


def test_multi_turn_context_resolution():
    kb = LegalKnowledgeBase("data/legalmitra_kb.db", must_exist=True)
    rag = LegalRAGEngine(knowledge_base=kb, llm_provider=MockLLMProvider())

    history = [
        {"role": "user", "content": "What are the inherent powers of the High Court under Section 528 BNSS?"},
        {"role": "assistant", "content": "Section 528 of the Bharatiya Nagarik Suraksha Sanhita, 2023 preserves inherent powers."},
    ]
    query = "Can commercial disputes be quashed under it?"
    resolved = rag._resolve_query_context(query, history)

    assert "528" in resolved or "BNSS" in resolved
    assert "quashed under it" in resolved


def test_false_legal_premise_refutation():
    kb = LegalKnowledgeBase("data/legalmitra_kb.db", must_exist=True)
    rag = LegalRAGEngine(knowledge_base=kb, llm_provider=MockLLMProvider())

    resp = rag.answer("What is the mandatory death penalty for criminal defamation under BNS?")
    assert "false" in resp.answer.lower() or "unsubstantiated" in resp.answer.lower() or "two years" in resp.answer.lower()
