"""
Unit tests for Phase 112: Multi-Intent Disambiguation & Fact Extraction Guard Engine.
"""

import pytest
from legalmitra.orchestration.multi_intent_guard import (
    MultiIntentDisambiguationGuard,
    UrgencyTier,
)
from legalmitra.orchestration.pipeline import LegalQueryPipeline


class TestPhase112MultiIntentGuard:
    def test_compound_eviction_and_deposit_withholding(self):
        query = "my landlord locked my flat and threw my luggage, and is also refusing to return my security deposit of 50000"
        res = MultiIntentDisambiguationGuard.analyze_query(query)
        assert res.is_compound_query is True
        assert len(res.sub_issues) >= 2

        # Verify eviction issue exists
        titles = [si.issue_title for si in res.sub_issues]
        assert any("Eviction" in t for t in titles)
        assert any("Security Deposit" in t for t in titles)

        # Verify factual extraction of ₹50,000
        assert any("50000" in amt for amt in res.extracted_facts.monetary_amounts)
        assert "Landlord / Makaan Maalik" in res.extracted_facts.parties_involved

    def test_single_issue_not_marked_compound(self):
        query = "party ne cheque diya tha bounce ho gaya sign mismatch bolke"
        res = MultiIntentDisambiguationGuard.analyze_query(query)
        assert res.is_compound_query is False
        assert len(res.sub_issues) == 1
        assert "Dishonour of Cheque" in res.sub_issues[0].issue_title
        assert res.sub_issues[0].urgency_tier == UrgencyTier.URGENT_CIVIL_DEADLINE

    def test_cyber_fraud_urgency_tier(self):
        query = "kisi ne call karke OTP le liya aur mere 50000 kat gaye account se ab kya karu"
        res = MultiIntentDisambiguationGuard.analyze_query(query)
        assert res.primary_urgency == UrgencyTier.GOLDEN_HOUR_FINANCIAL
        assert any("50000" in amt for amt in res.extracted_facts.monetary_amounts)

    def test_violence_and_fir_refusal_compound(self):
        query = "neighbour attacked me with physical violence and police in thana is refusing to take my FIR"
        res = MultiIntentDisambiguationGuard.analyze_query(query)
        assert res.is_compound_query is True
        assert res.primary_urgency == UrgencyTier.IMMEDIATE_EMERGENCY
        titles = [si.issue_title for si in res.sub_issues]
        assert any("Physical Safety" in t for t in titles)
        assert any("Refusal to Register" in t for t in titles)

    def test_answer_assembler_e2e_compound_query(self):
        pipeline = LegalQueryPipeline()
        query = "my landlord locked my flat and threw my luggage, and is also refusing to return my deposit of 50000"
        resp = pipeline.execute(query=query)
        assert resp is not None
        assert "Multi-Issue Legal Determination" in resp.answer_text
        assert "Issue 1" in resp.answer_text
        assert "Issue 2" in resp.answer_text
        assert "Specific Relief Act" in resp.answer_text
        assert "Security Deposit" in resp.answer_text
