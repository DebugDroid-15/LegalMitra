"""
Tests for LegalMitra Source-Grounded RAG Engine and Evaluator.
Verifies evidential bounding, citation extraction, unsupported-answer detection,
and evaluation scoring.
"""

from datetime import date
from pathlib import Path
import pytest

from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
from legalmitra.knowledge.models import SearchFilters
from legalmitra.llm.interface import BaseLLMProvider, LLMMessage, LLMResponse
from legalmitra.rag.engine import LegalRAGEngine
from legalmitra.rag.evaluator import RAGEvaluator
from legalmitra.schemas.evaluation import EvaluationQuestionDocument, EvaluationRubric
from legalmitra.schemas.legal_qa import EvidencePassage


class GroundedMockLLM(BaseLLMProvider):
    """Predictable mock provider for RAG tests."""
    def is_available(self) -> bool:
        return True

    def generate(self, messages, **kwargs) -> LLMResponse:
        user_msg = messages[-1].content
        if "maritime" in user_msg.lower() or "income tax" in user_msg.lower() or "No matching legal sources" in user_msg:
            return LLMResponse(
                content="The retrieved legal sources do not provide sufficient evidence to answer this question authoritatively under Indian law.",
                model_name="MockLLM-GroundingTest"
            )
        return LLMResponse(
            content=(
                "Under Section 61 of the Bharatiya Sakshya Adhiniyam, 2023, electronic or digital records "
                "shall not be denied admissibility solely on the ground of being electronic. "
                "Subject to Section 63, they have the same legal effect as other documents. "
                "[Bharatiya Sakshya Adhiniyam, 2023, Section 61]"
            ),
            model_name="MockLLM-GroundingTest"
        )


@pytest.fixture
def rag_engine():
    kb = LegalKnowledgeBase("data/legalmitra_kb.db")
    mock = GroundedMockLLM()
    engine = LegalRAGEngine(knowledge_base=kb, llm_provider=mock)
    return engine


def test_rag_answer_supported_query(rag_engine):
    resp = rag_engine.answer("What is the rule on admissibility of electronic records under Section 61 of BSA?")
    assert resp.is_grounded is True
    assert resp.evidence_sufficiency == "sufficient"
    assert len(resp.cited_evidence) >= 1
    assert "Section 61" in resp.answer
    assert any("Bharatiya Sakshya Adhiniyam" in b for b in resp.binding_authorities)
    assert "advocate" in resp.legal_disclaimer.lower()


def test_rag_answer_unsupported_query_reports_insufficient(rag_engine):
    # Query for something completely absent from corpus
    resp = rag_engine.answer("What are the salvage arbitration rules for maritime collisions in Mumbai harbor?")
    assert resp.evidence_sufficiency == "insufficient"
    assert "sufficient evidence" in resp.answer.lower() or "insufficient" in resp.evidence_sufficiency


def test_rag_detects_temporal_missing_facts(rag_engine):
    # Query mentioning electronic evidence without date
    resp = rag_engine.answer("How do I introduce electronic evidence in an ongoing criminal case?")
    assert resp.missing_facts_prompt is not None
    assert "1 July 2024" in resp.missing_facts_prompt or "Temporal" in resp.missing_facts_prompt


def test_rag_synthetic_scaffold_exclusion(rag_engine):
    # Default search excludes synthetic scaffold
    resp_clean = rag_engine.answer("anticipatory bail Rahul Kumar", filters=SearchFilters(include_synthetic=False))
    assert all(not ev.is_synthetic_scaffold for ev in resp_clean.cited_evidence)


def test_rag_evaluator_metrics(rag_engine):
    evaluator = RAGEvaluator(rag_engine)
    eval_item = EvaluationQuestionDocument(
        eval_id="EVAL-TEST-001",
        question="What is the rule under Section 61 of the Bharatiya Sakshya Adhiniyam, 2023?",
        expected_answer="Electronic records are admissible under Section 61 of BSA 2023.",
        target_statute_or_case="Bharatiya Sakshya Adhiniyam, 2023",
        golden_citations=["Section 61 BSA", "Bharatiya Sakshya Adhiniyam"],
        forbidden_terms_or_repealed_citations=["Section 65B Indian Evidence Act 1872 as current"],
        supporting_source_ids=["IND-STAT-BSA-2023-SEC61"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-BSA-2023-SEC61",
                section_or_para_ref="Section 61",
                verbatim_text="Nothing in this Adhiniyam shall apply to deny the admissibility of an electronic or digital record"
            )
        ],
        legal_domain="Law of Evidence",
    )

    res = evaluator.evaluate_item(eval_item, top_k=3)
    assert res.retrieval_success is True
    assert res.citation_accuracy > 0.0
    assert len(res.forbidden_terms_detected) == 0
    assert res.passed is True


def test_rag_evaluator_distinctive_tokens_regression(rag_engine):
    """
    Regression test: ensures generic legal words (section, explanation, evidence)
    do not trigger false-positive negative constraint violations when distinctive
    numerical/statutory tokens (e.g. 65B, 1872) are absent from the model answer.
    """
    evaluator = RAGEvaluator(rag_engine)
    eval_item = EvaluationQuestionDocument(
        eval_id="EVAL-TEST-REGRESSION-002",
        question="How is an electronic record defined under the Explanation to Section 61 BSA?",
        expected_answer="Electronic record includes records in electronic form under IT Act Section 2(1)(t).",
        target_statute_or_case="Bharatiya Sakshya Adhiniyam, 2023",
        golden_citations=["Section 61 Explanation BSA", "Section 2(1)(t)"],
        forbidden_terms_or_repealed_citations=["Section 65B Explanation Evidence Act 1872"],
        supporting_source_ids=["IND-STAT-BSA-2023-SEC61"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-BSA-2023-SEC61",
                section_or_para_ref="Section 61 Explanation",
                verbatim_text="Explanation.—For the purposes of this section, electronic or digital record includes records stored in an electronic form"
            )
        ],
        legal_domain="Law of Evidence",
    )

    res = evaluator.evaluate_item(eval_item, top_k=3)
    # The mock answer contains 'Section' and 'evidence', but does NOT contain '65B' or '1872'
    assert "Section 65B Explanation Evidence Act 1872" not in res.forbidden_terms_detected
    assert res.passed is True

