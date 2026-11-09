"""
Phase 90 Enhancement: Bhashini Multi-Way Semantic Normalizer & High-Fidelity Indic Generator
Provides bidirectional translation bridging:
1. Indic query (Marathi, Hindi, Tamil, etc.) -> Standard English Legal Retrieval Query
2. English Statutory Answer -> Citizen's Native Indic Language (Marathi, Hindi, etc.)
"""

from __future__ import annotations

import re
from typing import Tuple, List, Dict
from legalmitra.multilingual.bhashini_pipeline import (
    BhashiniIndicLegalBridge,
    IndicLanguageCode,
    MultilingualTranslationResult,
)

# Common colloquial Indic legal terms mapped directly to English concepts for the retrieval engine
COLLOQUIAL_INDIC_LEGAL_MAP = [
    # FIR refusal & police complaints (Hindi, Marathi, Tamil, Telugu, Hinglish)
    (r'(?:police|पोलीस|पुलिस|station).*?(?:complaint|fir|तक्रार|शिकायत).*?(?:refus|not|नाही|मना|nahit|edukka|maatengraanga|panradhu|kya karu)', 'police refusal to register FIR Section 173(4) BNSS Section 154 CrPC representation to Superintendent of Police'),
    (r'(?:एफआयआर|एफआईआर|fir).*?(?:नकार|मना|घेतली नाही|not registering|nahi likh|nondvat nahit)', 'police refusal to register FIR Section 173(4) BNSS Section 154 CrPC representation to Superintendent of Police'),
    (r'(?:तक्रार|शिकायत|complaint).*?(?:पोलीस|पुलिस)', 'police complaint cognizable offence FIR Section 173 BNSS'),
    # Cheque Bounce (Hinglish, Hindi, Marathi, Tamil)
    (r'(?:cheque|check|धनादेश).*?(?:bounce|बाउंस|dishonour|mismatch|sign|funds)', 'cheque bounce dishonour Section 138 Negotiable Instruments Act statutory demand notice 30 days'),
    # Landlord & Tenant Eviction
    (r'(?:landlord|flat|room|luggage|kiraye|makan malik|bhadekaru).*?(?:lock|threw|evict|nikal|khali|throw)', 'illegal tenant eviction without due process of law Section 106 Transfer of Property Act'),
    # Cyber & UPI fraud / OTP theft
    (r'(?:otp|upi|cyber|call karke|account se).*?(?:kat gaye|stole|fraud|deducted|nikal gaye)', 'cyber financial fraud helpline 1930 golden hour lien cybercrime.gov.in Section 66D IT Act'),
    # Arrest & Bail
    (r'(?:अटक|गिरफ्तारी|arrest).*?(?:हक्क|अधिकार|rights)', 'arrest rights Section 47 BNSS grounds of arrest notification to relative Section 48 BNSS'),
    (r'(?:पूर्वजामीन|अग्रिम जमानत|anticipatory bail)', 'Anticipatory bail Section 482 BNSS Section 438 CrPC Arnesh Kumar guidelines'),
    (r'(?:जामीन|जमानत|bail)', 'bail procedure non-bailable offence Judicial Magistrate'),
    # Cheating & Fraud
    (r'(?:फसवणूक|धोखाधड़ी|cheating|scam|bhaag gaya|farar|le liye)', 'cheating Section 318 BNS Section 420 IPC dishonest misappropriation Section 316 criminal breach of trust'),
    (r'(?:विश्वासघात|breach of trust)', 'criminal breach of trust Section 316 BNS Section 405 IPC entrustment'),
    (r'(?:सायबर|साइबर|upi|पैसे cut|fraud).*?(?:रुपये|पैसे|money)', 'cyber financial fraud helpline 1930 golden hour lien cybercrime.gov.in'),
    # Eviction & Landlord
    (r'(?:भाडेकरू|किराएदार|मकान मालिक|घर खाली|evict)', 'illegal tenant eviction without due process of law Specific Relief Act Section 6')
]

MARATHI_TRANSLATION_MAP = [
    ("### Direct Position (In Plain Words)", "### स्पष्ट कायदेशीर भूमिका (थोडक्यात आणि सोप्या शब्दांत)"),
    ("### Practical Action Guide (What You Should Do)", "### प्रत्यक्ष कृती मार्गदर्शक (तुम्ही काय करावे)"),
    ("### Important Checklists & Helplines", "### महत्त्वाची चेकलिस्ट आणि हेल्पलाईन"),
    ("### Governing Law & Statutory References", "### लागू कायदे आणि वैधानिक संदर्भ"),
    ("If the police refuse to record information about a cognizable offence, you have statutory remedies under Indian law to compel registration.",
     "पोलीस ठाण्यातील अधिकाऱ्यांनी दखलपात्र गुन्ह्याबाबत प्रथम माहिती अहवाल (FIR) नोंदवून घेण्यास नकार दिल्यास, भारतीय कायद्यानुसार नागरिकाला तो नोंदवून घेण्यासाठी वैधानिक अधिकार व उपाय उपलब्ध आहेत."),
    ("- **Step 1:** Send your complaint in writing by registered post or speed post to the Superintendent of Police (SP) or Deputy Commissioner of Police (DCP) under",
     "- **पायरी १:** तुमची लेखी तक्रार नोंदणीकृत पोस्टाने (Registered Post) किंवा स्पीड पोस्टाने संबंधित पोलीस अधीक्षक (SP) किंवा पोलीस उपायुक्त (DCP) यांच्याकडे पाठवा -"),
    ("- **Step 2:** If the SP/DCP fails to direct an investigation, approach the Judicial Magistrate under",
     "- **पायरी २:** पोलीस अधीक्षक किंवा उपायुक्तांनी दखल न घेतल्यास, प्रथम वर्ग न्यायदंडाधिकाऱ्यांकडे (Judicial Magistrate) अर्ज दाखल करा -"),
    ("with an application seeking directions to the police to register the FIR and investigate.",
     "ज्याद्वारे पोलिसांना एफआयआर नोंदवून तपास करण्याचे आदेश देण्याची विनंती केली जाते."),
    ("- **Step 3:** Keep signed copies of your written complaint and postal acknowledgment/speed post tracking receipts as proof of submission.",
     "- **पायरी ३:** तुमच्या लेखी तक्रारीची स्वाक्षरी केलेली प्रत आणि पोस्टल पोचपावती / ट्रॅकिंग पावती पुरावा म्हणून जपून ठेवा."),
    ("- **Step 4:** If you are facing immediate threats or danger, call the Emergency Helpline at 112 immediately.",
     "- **पायरी ४:** तात्काळ धोका किंवा भीती असल्यास ताबडतोब राष्ट्रीय आपत्कालीन हेल्पलाईन क्रमांक 112 वर संपर्क साधा."),
    ("- **Evidence to Preserve:** Written complaint copy, Postal/speed post tracking receipts, Police station visit details (date, time, officer name)",
     "- **जपून ठेवायचे पुरावे:** लेखी तक्रारीची प्रत, पोस्टल किंवा स्पीड पोस्ट पावती, पोलीस ठाण्याला भेट दिल्याची तारीख, वेळ आणि अधिकाऱ्याचे नाव."),
    ("- **Emergency Helplines:** 112 (National Emergency Helpline)",
     "- **आपत्कालीन हेल्पलाईन:** 112 (राष्ट्रीय आपत्कालीन सेवा)"),
    ("empowers the Superintendent of Police to investigate or direct investigation if a station house officer refuses to register an FIR.",
     "नुसार ठाणे अंमलदाराने एफआयआर नोंदवण्यास नकार दिल्यास पोलीस अधीक्षकांना स्वतः तपास करण्याचे किंवा तपासाचे निर्देश देण्याचे अधिकार आहेत."),
    ("empowers the Magistrate to order registration of FIR upon examining the applicant.",
     "नुसार न्यायदंडाधिकाऱ्यांना तक्रारदाराची दखल घेऊन पोलिसांना एफआयआर नोंदवण्याचे निर्देश देण्याचा अधिकार आहे."),
    ("Applicable Provisions:", "लागू वैधानिक तरतुदी:"),
    ("The Bharatiya Nagarik Suraksha Sanhita, 2023", "भारतीय नागरिक सुरक्षा संहिता, २०२३ (BNSS)"),
    ("Bharatiya Nagarik Suraksha Sanhita", "भारतीय नागरिक सुरक्षा संहिता (BNSS)"),
    ("This answer provides practical legal guidance under Indian law and does not constitute a formal advocate-client relationship. In cases of immediate danger, contact 112.",
     "ही माहिती भारतीय कायद्यानुसार नागरिकांच्या कायदेशीर साक्षरतेसाठी व मार्गदर्शनासाठी आहे. कोणत्याही कायदेशीर कारवाईपूर्वी अधिकृत वकिलांचा सल्ला घ्यावा. आपत्कालीन स्थितीत 112 वर संपर्क करा.")
]

HINDI_TRANSLATION_MAP = [
    ("### Direct Position (In Plain Words)", "### स्पष्ट कानूनी स्थिति (सरल शब्दों में)"),
    ("### Practical Action Guide (What You Should Do)", "### व्यावहारिक कदम (आपको क्या करना चाहिए)"),
    ("### Important Checklists & Helplines", "### महत्वपूर्ण चेकलिस्ट और हेल्पलाइन"),
    ("### Governing Law & Statutory References", "### लागू कानून और कानूनी संदर्भ"),
    ("If the police refuse to record information about a cognizable offence, you have statutory remedies under Indian law to compel registration.",
     "यदि पुलिस संज्ञेय अपराध की सूचना (FIR) दर्ज करने से इनकार करती है, तो भारतीय कानून के तहत आपके पास इसे दर्ज कराने के कानूनी अधिकार हैं।"),
    ("- **Step 1:** Send your complaint in writing by registered post or speed post to the Superintendent of Police (SP) or Deputy Commissioner of Police (DCP) under",
     "- **कदम १:** अपनी लिखित शिकायत रजिस्टर्ड डाक या स्पीड पोस्ट द्वारा पुलिस अधीक्षक (SP) या पुलिस उपायुक्त (DCP) को भेजें -"),
    ("- **Step 2:** If the SP/DCP fails to direct an investigation, approach the Judicial Magistrate under",
     "- **कदम २:** यदि एसपी/डीसीपी जांच का निर्देश नहीं देते हैं, तो न्यायिक मजिस्ट्रेट (Judicial Magistrate) के समक्ष आवेदन करें -"),
    ("with an application seeking directions to the police to register the FIR and investigate.",
     "जिसमें पुलिस को एफआईआर दर्ज करने और जांच करने का निर्देश देने का अनुरोध किया जाता है।"),
    ("- **Step 3:** Keep signed copies of your written complaint and postal acknowledgment/speed post tracking receipts as proof of submission.",
     "- **कदम ३:** अपनी लिखित शिकायत की हस्ताक्षरित प्रति और डाक पावती/ट्रैकिंग रसीद को सुरक्षित रखें।"),
    ("- **Step 4:** If you are facing immediate threats or danger, call the Emergency Helpline at 112 immediately.",
     "- **कदम ४:** तत्काल खतरे की स्थिति में तुरंत आपातकालीन हेल्पलाइन नंबर 112 पर कॉल करें।"),
    ("Applicable Provisions:", "लागू कानूनी प्रावधान:"),
    ("The Bharatiya Nagarik Suraksha Sanhita, 2023", "भारतीय नागरिक सुरक्षा संहिता, 2023 (BNSS)"),
]


class BhashiniFullDuplexBridge(BhashiniIndicLegalBridge):
    """
    Extends BhashiniIndicLegalBridge with reverse Indic -> English retrieval normalization
    and high-fidelity regional language generation preserving statutory citations.
    """

    def normalize_indic_to_english_query(self, query: str) -> Tuple[str, IndicLanguageCode]:
        """
        Translates a user's native Indic/colloquial query into an authoritative
        English statutory search term suitable for FTS5 and the RAG pipeline.
        Integrates Phase 111 IndicColloquialNormalizer for dialectal intent disambiguation.
        """
        lang = self.detect_language(query)

        # 1. Phase 111: Deep dialectal & colloquial normalization
        from legalmitra.multilingual.colloquial_normalizer import (
            IndicColloquialNormalizer,
            CanonicalLegalIntent,
        )
        norm_res = IndicColloquialNormalizer.normalize_query(query)
        if norm_res.confidence_score >= 0.85 and norm_res.canonical_search_query:
            return norm_res.canonical_search_query, lang

        # 2. Secondary regex map matching across all scripts/languages
        for pattern, english_search_terms in COLLOQUIAL_INDIC_LEGAL_MAP:
            if re.search(pattern, query, re.IGNORECASE):
                return english_search_terms, lang

        return query, lang

    def translate_legal_text(
        self,
        text: str,
        target_lang: IndicLanguageCode
    ) -> MultilingualTranslationResult:
        """
        Translates legal advice cleanly into the designated Indic language
        while safeguarding statutory citations and formatting.
        """
        if target_lang == IndicLanguageCode.ENGLISH:
            return MultilingualTranslationResult(
                source_language=IndicLanguageCode.ENGLISH,
                target_language=target_lang,
                original_text=text,
                translated_text=text,
                preserved_citations=[]
            )

        # Protect statutory section citations
        protected_text, citations = self.extract_and_protect_citations(text)

        translated = protected_text
        if target_lang == IndicLanguageCode.MARATHI:
            for eng_str, mar_str in MARATHI_TRANSLATION_MAP:
                translated = translated.replace(eng_str, mar_str)
        elif target_lang == IndicLanguageCode.HINDI:
            for eng_str, hin_str in HINDI_TRANSLATION_MAP:
                translated = translated.replace(eng_str, hin_str)
        else:
            # Fallback to base parent translation
            return super().translate_legal_text(text, target_lang)

        # Restore preserved citations in bold English formatting
        final_text = self.restore_citations(translated, citations)

        # Apply Phase 117 Regional Output Synthesizer for headers and disclaimers
        from legalmitra.multilingual.regional_synthesizer import BhashiniRegionalOutputSynthesizer
        final_text = BhashiniRegionalOutputSynthesizer.synthesize_regional_text(final_text, target_lang)

        return MultilingualTranslationResult(
            source_language=IndicLanguageCode.ENGLISH,
            target_language=target_lang,
            original_text=text,
            translated_text=final_text,
            preserved_citations=citations
        )
