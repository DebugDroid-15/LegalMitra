"""
Phase 90 Test Suite: Bhashini 22 Indic Languages Sovereign Pipeline
Validates 22 Scheduled Language registries, language identification, statutory citation
placeholding, and cross-lingual legal terminology synthesis.
"""

import pytest

from legalmitra.multilingual.bhashini_pipeline import (
    BhashiniIndicLegalBridge,
    IndicLanguageCode,
    SCHEDULED_LANGUAGES_REGISTRY,
)


class TestPhase90BhashiniMultilingual:

    def test_all_22_scheduled_languages_registered(self):
        # Must cover all 22 Eighth Schedule languages + English
        scheduled = [lang for lang, meta in SCHEDULED_LANGUAGES_REGISTRY.items() if meta.is_scheduled_language]
        assert len(scheduled) == 22

        # Verify key languages are present
        assert IndicLanguageCode.HINDI in scheduled
        assert IndicLanguageCode.BENGALI in scheduled
        assert IndicLanguageCode.TAMIL in scheduled
        assert IndicLanguageCode.TELUGU in scheduled
        assert IndicLanguageCode.MARATHI in scheduled
        assert IndicLanguageCode.GUJARATI in scheduled
        assert IndicLanguageCode.KANNADA in scheduled
        assert IndicLanguageCode.MALAYALAM in scheduled
        assert IndicLanguageCode.PUNJABI in scheduled
        assert IndicLanguageCode.ODIA in scheduled
        assert IndicLanguageCode.ASSAMESE in scheduled
        assert IndicLanguageCode.URDU in scheduled
        assert IndicLanguageCode.SANSKRIT in scheduled
        assert IndicLanguageCode.MAITHILI in scheduled
        assert IndicLanguageCode.SANTALI in scheduled
        assert IndicLanguageCode.KASHMIRI in scheduled
        assert IndicLanguageCode.NEPALI in scheduled
        assert IndicLanguageCode.KONKANI in scheduled
        assert IndicLanguageCode.SINDHI in scheduled
        assert IndicLanguageCode.DOGRI in scheduled
        assert IndicLanguageCode.MANIPURI in scheduled
        assert IndicLanguageCode.BODO in scheduled

    def test_language_detection_heuristics(self):
        bridge = BhashiniIndicLegalBridge()

        # Hindi (Devanagari)
        lang_hi = bridge.detect_language("पुलिस ने मेरी रिपोर्ट दर्ज करने से मना कर दिया")
        assert lang_hi == IndicLanguageCode.HINDI

        # Marathi (Devanagari with Marathi stopwords)
        lang_mr = bridge.detect_language("पोलीस ठाण्यात तक्रार नोंदवून घेतली नाही आहे")
        assert lang_mr == IndicLanguageCode.MARATHI

        # Bengali
        lang_bn = bridge.detect_language("পুলিশ আমার এফআইআর দায়ের করতে অস্বীকার করেছে")
        assert lang_bn == IndicLanguageCode.BENGALI

        # Tamil
        lang_ta = bridge.detect_language("காவல்துறை எனது வழக்கை பதிவு செய்ய மறுக்கிறது")
        assert lang_ta == IndicLanguageCode.TAMIL

        # Telugu
        lang_te = bridge.detect_language("పోలీసులు నా ఫిర్యాదును నమోదు చేయడానికి నిరాకరించారు")
        assert lang_te == IndicLanguageCode.TELUGU

        # English
        lang_en = bridge.detect_language("What are my legal rights upon police arrest?")
        assert lang_en == IndicLanguageCode.ENGLISH

    def test_citation_protection_and_restoration(self):
        bridge = BhashiniIndicLegalBridge()
        text = "Under Section 316 BNS (formerly Section 405 IPC) as ruled in (2014) 8 SCC 273, arrest must be justified."

        protected, citations = bridge.extract_and_protect_citations(text)
        assert len(citations) >= 2
        assert "__LEGAL_CIT_" in protected

        restored = bridge.restore_citations(protected, citations)
        # All extracted citations should be safely reinstated
        for cit in citations:
            assert cit in restored

    def test_translate_to_hindi_with_citation_preservation(self):
        bridge = BhashiniIndicLegalBridge()
        english_input = "Criminal Breach of Trust under Section 316 BNS requires entrustment. For Anticipatory Bail, see Section 482 BNSS."

        res = bridge.translate_legal_text(english_input, target_lang=IndicLanguageCode.HINDI)
        assert res.target_language == IndicLanguageCode.HINDI
        assert "Section 316 BNS" in res.translated_text
        assert "Section 482 BNSS" in res.translated_text
        assert "आपराधिक विश्वासघात" in res.translated_text
        assert "अग्रिम जमानत" in res.translated_text

    def test_translate_to_marathi_and_tamil(self):
        bridge = BhashiniIndicLegalBridge()
        english_input = "To file an Anticipatory Bail petition regarding Cheating, apply under Section 482 BNSS."

        res_mr = bridge.translate_legal_text(english_input, target_lang=IndicLanguageCode.MARATHI)
        assert "पूर्वजामीन" in res_mr.translated_text
        assert "Section 482 BNSS" in res_mr.translated_text

        res_ta = bridge.translate_legal_text(english_input, target_lang=IndicLanguageCode.TAMIL)
        assert "முன்ஜாமீன்" in res_ta.translated_text
        assert "Section 482 BNSS" in res_ta.translated_text
