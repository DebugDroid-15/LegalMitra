"""
Tests for Phase 111: Indic Colloquial & Dialectal Semantic Normalizer Engine.
"""

import pytest
from legalmitra.multilingual.colloquial_normalizer import (
    IndicColloquialNormalizer,
    CanonicalLegalIntent,
)
from legalmitra.multilingual.duplex_bridge import BhashiniFullDuplexBridge


class TestPhase111ColloquialNormalizer:
    def test_cheque_bounce_hinglish(self):
        query = "party ne cheque diya tha bounce ho gaya sign mismatch bolke"
        res = IndicColloquialNormalizer.normalize_query(query)
        assert res.canonical_intent == CanonicalLegalIntent.CHEQUE_BOUNCE_DISHONOUR
        assert "138" in res.canonical_search_query
        assert "Negotiable Instruments Act" in res.canonical_search_query

    def test_tenant_eviction_slang(self):
        query = "my landlord locked my flat and threw my luggage out without any notice"
        res = IndicColloquialNormalizer.normalize_query(query)
        assert res.canonical_intent == CanonicalLegalIntent.ILLEGAL_TENANT_EVICTION
        assert "Transfer of Property Act" in res.canonical_search_query

    def test_cyber_fraud_otp_theft(self):
        query = "kisi ne call karke OTP le liya aur mere 50000 kat gaye account se ab kya karu"
        res = IndicColloquialNormalizer.normalize_query(query)
        assert res.canonical_intent == CanonicalLegalIntent.CYBER_OTP_FINANCIAL_FRAUD
        assert "1930" in res.canonical_search_query
        assert "66D" in res.canonical_search_query

    def test_fir_refusal_tanglish(self):
        query = "police station la complaint edukka maatengraanga enna panradhu"
        res = IndicColloquialNormalizer.normalize_query(query)
        assert res.canonical_intent == CanonicalLegalIntent.POLICE_FIR_REFUSAL
        assert "173(4)" in res.canonical_search_query
        assert "Superintendent of Police" in res.canonical_search_query

    def test_cheating_duping_hinglish(self):
        query = "ek aadmi ne dukaan ke naam par 2 lakh rupaye le liye aur bhaag gaya"
        res = IndicColloquialNormalizer.normalize_query(query)
        assert res.canonical_intent == CanonicalLegalIntent.CRIMINAL_CHEATING_DUPING
        assert "318" in res.canonical_search_query
        assert "cheating" in res.canonical_search_query.lower()

    def test_negative_keyword_guard_notice_in_tenancy_not_firing_employment(self):
        # Even with the word "notice", this should NOT be UNPAID_SALARY or employment termination
        query = "landlord threw my luggage without notice"
        res = IndicColloquialNormalizer.normalize_query(query)
        assert res.canonical_intent == CanonicalLegalIntent.ILLEGAL_TENANT_EVICTION
        assert res.canonical_intent != CanonicalLegalIntent.UNPAID_SALARY_WAGES

    def test_free_legal_aid_marathish(self):
        query = "paise nahi hai lawyer afford nahi kar sakta free legal aid milegi kya"
        res = IndicColloquialNormalizer.normalize_query(query)
        assert res.canonical_intent == CanonicalLegalIntent.FREE_LEGAL_AID
        assert "15100" in res.canonical_search_query

    def test_duplex_bridge_integration(self):
        bridge = BhashiniFullDuplexBridge()
        norm_query, lang = bridge.normalize_indic_to_english_query(
            "police station la complaint edukka maatengraanga enna panradhu"
        )
        assert "173(4)" in norm_query or "Superintendent of Police" in norm_query
