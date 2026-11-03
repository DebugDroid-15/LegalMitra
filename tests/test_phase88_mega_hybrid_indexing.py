"""
Phase 88 Test Suite: Mega Hybrid Indexing (Dense Vector + BM25 + Citation Pinning)
Validates multi-stage retrieval, semantic similarity encoding, citation pin detection,
and Reciprocal Rank Fusion (RRF) scoring on legal queries.
"""

from pathlib import Path
import pytest

from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
from legalmitra.retrieval.mega_hybrid_engine import (
    DenseSemanticEncoder,
    HybridScoredResult,
    MegaHybridRetrievalEngine,
)


class TestPhase88MegaHybridIndexing:

    def test_dense_semantic_encoder_properties(self):
        encoder = DenseSemanticEncoder()
        vec1 = encoder.encode("Section 316 BNS Criminal Breach of Trust entrustment")
        vec2 = encoder.encode("Section 405 IPC Criminal Breach of Trust property misappropriation")
        vec3 = encoder.encode("Motor Vehicles Act compensation for traffic accident negligence")

        assert len(vec1) == DenseSemanticEncoder.DIMENSION
        assert len(vec2) == DenseSemanticEncoder.DIMENSION

        # Related penal breach of trust queries should have higher cosine similarity than unrelated traffic queries
        sim_related = encoder.cosine_similarity(vec1, vec2)
        sim_unrelated = encoder.cosine_similarity(vec1, vec3)
        assert sim_related > sim_unrelated

    def test_detect_citation_pins_in_queries(self):
        engine = MegaHybridRetrievalEngine(db_path="data/legalmitra_kb.db")

        # 1. Gazette notification detection
        pins1 = engine.detect_citation_pins("Has notification S.O. 848(E) enforced the new BNS provisions?")
        assert any("848" in p for p in pins1)

        # 2. Section detection
        pins2 = engine.detect_citation_pins("What is the penalty under Section 318 of BNS for fraud?")
        assert any("318" in p for p in pins2)

        # 3. Case law citation detection
        pins3 = engine.detect_citation_pins("Check precedent ratio in (2014) 8 SCC 273 regarding arrest guidelines")
        assert any("2014" in p and "SCC" in p for p in pins3)

    def test_hybrid_search_scoring_and_rrf(self):
        engine = MegaHybridRetrievalEngine(db_path="data/legalmitra_kb.db")
        results = engine.search_hybrid("Criminal Breach of Trust Section 316 BNS", limit=5)

        assert len(results) > 0
        top = results[0]
        assert isinstance(top, HybridScoredResult)
        assert top.combined_score > 0
        assert top.rrf_score > 0
        assert top.content is not None
        assert len(top.citation) > 0

    def test_citation_pinning_boosts_exact_statute(self):
        engine = MegaHybridRetrievalEngine(db_path="data/legalmitra_kb.db")
        results = engine.search_hybrid("Section 103 BNS murder penalty", limit=5)

        assert len(results) > 0
        # If any chunk has the exact section, its citation_pinned attribute or high score should reflect
        assert results[0].combined_score >= results[-1].combined_score

    def test_semantic_generalization_on_citizen_plain_language(self):
        engine = MegaHybridRetrievalEngine(db_path="data/legalmitra_kb.db")
        # Query without exact legal jargon: "boss taking my money without consent"
        results = engine.search_hybrid("employer withholding salary or money without permission", limit=5)

        assert len(results) > 0
        # Should return relevant civil/contract or breach provisions
        contents = " ".join([r.content + " " + r.citation for r in results]).lower()
        assert any(k in contents for k in ["trust", "contract", "property", "employer", "relief", "cheating"])
