"""
Unit tests for Phase 117: Multilingual Output Generation (22 Bhashini Languages).
"""

import pytest
from legalmitra.multilingual.bhashini_pipeline import IndicLanguageCode
from legalmitra.multilingual.regional_synthesizer import BhashiniRegionalOutputSynthesizer
from legalmitra.multilingual.duplex_bridge import BhashiniFullDuplexBridge


class TestPhase117MultilingualOutput:
    def test_hindi_headers_synthesis(self):
        text = (
            "### ⚖️ Direct Position (In Plain Words)\n"
            "This is the legal position under **Section 138**.\n\n"
            "### 📋 Practical Action Guide (What You Should Do)\n"
            "- Step 1: Send a notice."
        )
        res = BhashiniRegionalOutputSynthesizer.synthesize_regional_text(text, IndicLanguageCode.HINDI)
        assert "स्पष्ट कानूनी स्थिति" in res
        assert "व्यावहारिक कदम" in res
        assert "**Section 138**" in res

    def test_marathi_headers_synthesis(self):
        text = (
            "### ⚖️ Direct Position (In Plain Words)\n"
            "Court order.\n\n"
            "### 📋 Practical Action Guide (What You Should Do)\n"
            "- Step 1: File complaint."
        )
        res = BhashiniRegionalOutputSynthesizer.synthesize_regional_text(text, IndicLanguageCode.MARATHI)
        assert "स्पष्ट कायदेशीर भूमिका" in res
        assert "प्रत्यक्ष कृती मार्गदर्शक" in res

    def test_tamil_headers_synthesis(self):
        text = (
            "### ⚖️ Direct Position (In Plain Words)\n"
            "Legal advice.\n\n"
            "### 📋 Practical Action Guide (What You Should Do)\n"
            "- Step 1: Go to police."
        )
        res = BhashiniRegionalOutputSynthesizer.synthesize_regional_text(text, IndicLanguageCode.TAMIL)
        assert "தெளிவான சட்ட நிலைப்பாடு" in res
        assert "நடைமுறை வழிகாட்டுதல்" in res

    def test_telugu_bengali_gujarati_headers(self):
        for lang in [IndicLanguageCode.TELUGU, IndicLanguageCode.BENGALI, IndicLanguageCode.GUJARATI, IndicLanguageCode.KANNADA, IndicLanguageCode.PUNJABI]:
            text = "### ⚖️ Direct Position (In Plain Words)\nUnder Indian law."
            res = BhashiniRegionalOutputSynthesizer.synthesize_regional_text(text, lang)
            assert "Direct Position" not in res
            assert "Indian law" in res

    def test_duplex_bridge_statutory_token_preservation(self):
        bridge = BhashiniFullDuplexBridge()
        raw_text = "Under Section 173(4) of The Bharatiya Nagarik Suraksha Sanhita, 2023, you can write to SP."
        trans = bridge.translate_legal_text(raw_text, IndicLanguageCode.HINDI)
        # Verify section and act were preserved verbatim
        assert "Section 173(4)" in trans.translated_text
        assert "The Bharatiya Nagarik Suraksha Sanhita, 2023" in trans.translated_text
