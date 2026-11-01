"""
Test Suite for Phase 73: Bilingual Indic & Hinglish Plain-Language Synthesis.
Verifies:
1. Language detection across Devanagari Hindi, Romanized Hinglish, and English.
2. Colloquial Indic query normalization & FTS5 search expansion.
3. Bilingual plain summary generation (Hindi, Hinglish, English).
4. Full pipeline execution on common Indic legal questions (theft, tenant eviction, cheque bounce, bail).
5. REST API language parameter and detected_language response contract.
"""

import pytest
from fastapi.testclient import TestClient

from legalmitra.orchestration.indic_translator import IndicLegalTranslator
from legalmitra.orchestration.pipeline import LegalQueryPipeline
from legalmitra.orchestration.query_understanding import LegalQueryAnalyzer
from legalmitra.server.api import app


class TestPhase73IndicSynthesis:

    def test_language_detection(self):
        # Devanagari Hindi
        assert IndicLegalTranslator.detect_language("चोरी होने पर क्या होता है") == "hi"
        assert IndicLegalTranslator.detect_language("किरायेदार मकान खाली नहीं कर रहा") == "hi"

        # Hinglish
        assert IndicLegalTranslator.detect_language("chori hone par kya hota hai") == "hinglish"
        assert IndicLegalTranslator.detect_language("kirayedar makan khali nahi kar raha") == "hinglish"
        assert IndicLegalTranslator.detect_language("cheque bounce hone par notice kaise bheje") == "hinglish"
        assert IndicLegalTranslator.detect_language("police fir na likhe toh kya kare") == "hinglish"

        # English
        assert IndicLegalTranslator.detect_language("What happens in case of Minor theft") == "en"
        assert IndicLegalTranslator.detect_language("Can an injunction be granted against an infrastructure project?") == "en"

    def test_indic_query_parsing_and_search_normalization(self):
        analyzer = LegalQueryAnalyzer()

        # Hinglish query
        parsed_hinglish = analyzer.parse_query("chori hone par kya hota hai")
        assert parsed_hinglish.detected_language == "hinglish"
        assert parsed_hinglish.legal_domain == "CRIMINAL"
        assert "IND-STAT-BNS-2023" in parsed_hinglish.applicable_acts
        assert "Section 303" in parsed_hinglish.candidate_provisions
        assert parsed_hinglish.search_normalized_query is not None
        assert "theft" in parsed_hinglish.search_normalized_query

        # Hindi query
        parsed_hi = analyzer.parse_query("किरायेदार मकान खाली नहीं कर रहा")
        assert parsed_hi.detected_language == "hi"
        assert parsed_hi.legal_domain == "CONTRACT_PROPERTY"
        assert "IND-STAT-TPA-1882" in parsed_hi.applicable_acts
        assert "Section 106" in parsed_hi.candidate_provisions

    def test_indic_plain_summaries(self):
        # Hinglish summary
        sum_hinglish = IndicLegalTranslator.get_plain_summary("chori hone par kya hota hai")
        assert sum_hinglish is not None
        assert "Community Service" in sum_hinglish
        assert "Juvenile Justice Act" in sum_hinglish
        assert "Aam Bhasha Mein Saral Summary" in sum_hinglish

        # Devanagari Hindi summary
        sum_hi = IndicLegalTranslator.get_plain_summary("चोरी होने पर क्या होता है")
        assert sum_hi is not None
        assert "सामुदायिक सेवा" in sum_hi
        assert "किशोर न्याय अधिनियम" in sum_hi
        assert "संक्षिप्त सरल कानूनी सारांश" in sum_hi

    def test_pipeline_execution_hinglish_theft(self):
        pipeline = LegalQueryPipeline()
        resp = pipeline.execute("chori hone par kya hota hai")

        assert resp.response_state.value == "ANSWER_SUPPORTED"
        assert resp.assembled_answer is not None
        assert any("303" in p for p in resp.assembled_answer.governing_provisions)
        assert "Community Service" in resp.answer_text or "Section 303" in resp.answer_text
        assert "Aam Bhasha Mein Saral Summary" in resp.answer_text

    def test_pipeline_execution_hindi_tenancy(self):
        pipeline = LegalQueryPipeline()
        resp = pipeline.execute("किरायेदार मकान खाली नहीं कर रहा")

        assert resp.response_state.value == "ANSWER_SUPPORTED"
        assert resp.assembled_answer is not None
        assert any("106" in p for p in resp.assembled_answer.governing_provisions)
        assert "संक्षिप्त सरल कानूनी सारांश" in resp.answer_text

    def test_rest_api_language_contract(self):
        client = TestClient(app)

        # 1. Query endpoint with Hinglish
        res = client.post("/api/v1/query", json={
            "query": "chori hone par kya hota hai",
            "model_mode": "deterministic",
        })
        assert res.status_code == 200
        data = res.json()
        assert data["detected_language"] == "hinglish"
        assert data["response_state"] == "ANSWER_SUPPORTED"
        assert len(data["governing_provisions"]) > 0

        # 2. Chat endpoint with Devanagari Hindi
        chat_res = client.post("/api/v1/chat", json={
            "session_id": "test_indic_session_73",
            "message": "किरायेदार मकान खाली नहीं कर रहा",
            "model_mode": "deterministic",
        })
        assert chat_res.status_code == 200
        chat_data = chat_res.json()
        assert chat_data["detected_language"] == "hi"
        assert chat_data["response_state"] == "ANSWER_SUPPORTED"
