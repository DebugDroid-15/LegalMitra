import re
from typing import Any, Dict, List, Optional, Tuple

class IndicLegalTranslator:
    """
    Translates and normalizes Indic (Hindi, Hinglish) colloquial phrases into
    grounded statutory search terms and renders plain-language explanations in
    Hindi, Hinglish, or English.
    """

    INDIC_LEGAL_GLOSSARY: Dict[str, Dict[str, str]] = {
        "chori": {
            "canonical": "theft",
            "statute": "Section 303 Bharatiya Nyaya Sanhita, 2023 or Section 379 Indian Penal Code, 1860",
            "domain": "CRIMINAL",
            "search_keywords": "theft Section 303 BNS petty theft Section 379 IPC",
            "provisions": ["Section 303", "Section 379"],
            "acts": ["IND-STAT-BNS-2023", "IND-STAT-IPC-1860"],
            "plain_en": (
                "Regarding theft or stolen property:\n"
                "- 1. Under Section 303(2) of the Bharatiya Nyaya Sanhita, 2023 (BNS), if the value of stolen property is less than Rs 5,000 and it is a first-time conviction with return of property, the court can award community service instead of prison.\n"
                "- 2. If committed by a person under 18 years, the Juvenile Justice Act applies: juveniles are protected from regular jail and are handled by the Juvenile Justice Board."
            ),
            "plain_hi": (
                "चोरी या संपत्ति चोरी के मामले में कानूनी प्रावधान:\n"
                "- 1. भारतीय न्याय संहिता, 2023 (BNS) की धारा 303(2) के अनुसार, यदि चोरी की संपत्ति का मूल्य 5,000 रुपये से कम है और यह पहली बार का अपराध है, तो जेल के बजाय सामुदायिक सेवा (Community Service) का प्रावधान है।\n"
                "- 2. यदि आरोपी 18 वर्ष से कम उम्र का है (नाबालिग), तो किशोर न्याय अधिनियम (Juvenile Justice Act) लागू होता है। नाबालिगों को सामान्य जेल में नहीं भेजा जाता, बल्कि किशोर न्याय बोर्ड के माध्यम से सुधार प्रक्रिया होती है।"
            ),
            "plain_hinglish": (
                "Chori ya stolen property ke case mein kanooni niyam:\n"
                "- 1. Bharatiya Nyaya Sanhita, 2023 (BNS) ki Section 303(2) ke mutabiq, agar chori ki gayi cheez ki keemat 5,000 rupaye se kam hai aur pehli baar ka apradh hai, toh regular jail ki jagah Community Service (samajik seva) di ja sakti hai.\n"
                "- 2. Agar chori karne wala 18 saal se chota hai (minor), toh Juvenile Justice Act lagu hota hai. Aise bachhon ko normal jail mein nahi bheja jata, unka case Juvenile Justice Board handle karta hai."
            ),
        },
        "cheque bounce": {
            "canonical": "dishonour of cheque",
            "statute": "Section 138 Negotiable Instruments Act, 1881",
            "domain": "COMMERCIAL_ARBITRATION",
            "search_keywords": "cheque bounce Section 138 Negotiable Instruments Act demand notice 15 days",
            "provisions": ["Section 138", "Section 139", "Section 142"],
            "acts": ["IND-STAT-NI-1881"],
            "plain_en": (
                "Regarding cheque bounce due to insufficient funds:\n"
                "- 1. You must send a statutory demand notice within 30 days of receiving the bank memo.\n"
                "- 2. The other party gets a mandatory 15-day cure window to pay.\n"
                "- 3. If unpaid after 15 days, a criminal complaint under Section 138 NI Act can be filed in court within 30 days."
            ),
            "plain_hi": (
                "खाते में पैसे की कमी के कारण चेक बाउंस होने पर:\n"
                "- 1. बैंक से चेक अनादरित (बाउंस) पर्ची मिलने के 30 दिनों के भीतर कानूनी मांग नोटिस (Statutory Demand Notice) भेजना अनिवार्य है।\n"
                "- 2. सामने वाले पक्ष को भुगतान करने के लिए 15 दिनों का अनिवार्य समय मिलता है।\n"
                "- 3. यदि 15 दिनों में भुगतान नहीं होता है, तो अगले 30 दिनों के भीतर कोर्ट में धारा 138 परक्राम्य लिखत अधिनियम के तहत केस दर्ज किया जा सकता है।"
            ),
            "plain_hinglish": (
                "Account mein balance kam hone par cheque bounce hone par:\n"
                "- 1. Bank se memo milne ke 30 days ke andar legal Demand Notice bhejna zaroori hai.\n"
                "- 2. Saamne wale ko payment clear karne ke liye 15 mandatory days ka statutory time milta hai.\n"
                "- 3. Agar 15 din mein payment nahi hota, toh court mein Section 138 NI Act ke tehat criminal case file kiya ja sakta hai."
            ),
        },
        "kirayedar": {
            "canonical": "tenant eviction and tenancy termination",
            "statute": "Section 106 Transfer of Property Act, 1882 and State Rent Control Acts",
            "domain": "CONTRACT_PROPERTY",
            "search_keywords": "eviction tenant rent control Section 106 Transfer of Property notice to quit",
            "provisions": ["Section 106", "Section 108"],
            "acts": ["IND-STAT-TPA-1882"],
            "plain_en": (
                "Regarding rental property and tenant eviction:\n"
                "- 1. A landlord cannot forcefully eject a tenant or disconnect electricity/water without due legal process.\n"
                "- 2. A formal 15-day notice to quit under Section 106 TPA must be served before instituting eviction proceedings."
            ),
            "plain_hi": (
                "किरायेदार और मकान मालिक के विवाद व बेदखली के संबंध में:\n"
                "- 1. कोई भी मकान मालिक कानून को हाथ में लेकर किरायेदार को जबरन बेदखल नहीं कर सकता और न ही बिजली-पानी काट सकता है।\n"
                "- 2. संपत्ति अंतरण अधिनियम की धारा 106 के तहत कम से कम 15 दिनों का कानूनी नोटिस देना अनिवार्य है, जिसके बाद ही सक्षम अदालत में बेदखली याचिका दायर की जा सकती है।"
            ),
            "plain_hinglish": (
                "Makaan maalik aur kirayedar dispute ke case mein:\n"
                "- 1. Koi bhi landlord kirayedar ko zabardasti bahar nahi nikaal sakta aur na hi light/paani kaat sakta hai.\n"
                "- 2. Transfer of Property Act ki Section 106 ke tehat 15 days ka formal Notice to Quit bhejna zaroori hai, tabhi competent court mein eviction suit file ho sakta hai."
            ),
        },
        "jamanat": {
            "canonical": "bail and anticipatory bail",
            "statute": "Section 482 BNSS, 2023 or Section 438 CrPC, 1973",
            "domain": "CRIMINAL",
            "search_keywords": "anticipatory bail arrest Section 482 BNSS Section 438 CrPC bailable non-bailable",
            "provisions": ["Section 482", "Section 480"],
            "acts": ["IND-STAT-BNSS-2023", "IND-STAT-CRPC-1973"],
            "plain_en": (
                "Regarding bail and arrest:\n"
                "- 1. If you apprehend arrest in a false or non-bailable case, an application for Anticipatory Bail can be filed before the Sessions Court or High Court under Section 482 BNSS (or Section 438 CrPC).\n"
                "- 2. For bailable offences, bail is a matter of statutory right before the police station or Magistrate."
            ),
            "plain_hi": (
                "जमानत और गिरफ्तारी के संबंध में कानूनी अधिकार:\n"
                "- 1. यदि किसी गैर-जमानती मामले में गिरफ्तारी की आशंका है, तो सत्र न्यायालय (Sessions Court) या उच्च न्यायालय (High Court) में अग्रिम जमानत (Anticipatory Bail) दायर की जा सकती है।\n"
                "- 2. जमानती अपराधों (Bailable Offences) में जमानत पाना आरोपी का कानूनी अधिकार है जो थाने या मजिस्ट्रेट द्वारा दी जाती है।"
            ),
            "plain_hinglish": (
                "Bail aur arrest ke maamle mein legal rights:\n"
                "- 1. Agar arrest ka darr hai, toh Sessions Court ya High Court mein Anticipatory Bail (agrim jamanat) lagai ja sakti hai under Section 482 BNSS (ya Section 438 CrPC).\n"
                "- 2. Bailable offences mein bail ek statutory right hota hai jo police station ya magistrate court se aasani se mil jata hai."
            ),
        },
        "fir na likhna": {
            "canonical": "police refusal to register FIR",
            "statute": "Section 175(3) BNSS, 2023 or Section 156(3) CrPC, 1973",
            "domain": "CRIMINAL",
            "search_keywords": "FIR refusal register complaint Section 175 BNSS Section 156 CrPC Superintendent of Police",
            "provisions": ["Section 175", "Section 173"],
            "acts": ["IND-STAT-BNSS-2023", "IND-STAT-CRPC-1973"],
            "plain_en": (
                "If police refuse to register an FIR for a cognizable offence:\n"
                "- 1. You can send the written complaint by registered post to the Superintendent of Police (SP/DCP) under Section 175(3) BNSS.\n"
                "- 2. If still unregistered, an application under Section 175(3) BNSS / 156(3) CrPC can be filed directly before the Judicial Magistrate."
            ),
            "plain_hi": (
                "यदि पुलिस एफआईआर (FIR) दर्ज करने से मना कर दे:\n"
                "- 1. संज्ञेय अपराध में पुलिस द्वारा रिपोर्ट न लिखने पर आप अपनी लिखित शिकायत पुलिस अधीक्षक (SP / DCP) को स्पीड पोस्ट से भेज सकते हैं।\n"
                "- 2. यदि फिर भी कार्रवाई न हो, तो न्यायिक मजिस्ट्रेट के समक्ष धारा 175(3) BNSS (या 156(3) CrPC) के तहत सीधे आवेदन देकर एफआईआर दर्ज करने का आदेश प्राप्त किया जा सकता है।"
            ),
            "plain_hinglish": (
                "Agar police FIR darj na kare:\n"
                "- 1. Kisi cognizable offence mein police mana kare toh SP/DCP ko registered post se written complaint bheji ja sakti hai.\n"
                "- 2. Agar fir bhi action na ho, toh Judicial Magistrate ke paas Section 175(3) BNSS (ya 156(3) CrPC) ki petition daal kar police ko FIR darj karne ka direct order karwaya ja sakta hai."
            ),
        },
        "dhoka": {
            "canonical": "cheating and criminal breach of trust",
            "statute": "Section 318 Bharatiya Nyaya Sanhita, 2023 or Section 420 Indian Penal Code",
            "domain": "CRIMINAL",
            "search_keywords": "cheating fraud Section 318 BNS Section 420 IPC dishonest inducement",
            "provisions": ["Section 318", "Section 420"],
            "acts": ["IND-STAT-BNS-2023", "IND-STAT-IPC-1860"],
            "plain_en": (
                "Regarding fraud and cheating:\n"
                "- 1. For incidents after 1 July 2024, cheating is governed by Section 318 BNS; prior incidents fall under Section 420 IPC.\n"
                "- 2. Dishonest inducement from the very inception of the transaction must be established to constitute a criminal offence."
            ),
            "plain_hi": (
                "धोखाधड़ी और बेईमानी के मामलों में कानूनी स्थिति:\n"
                "- 1. 1 जुलाई 2024 के बाद की घटनाओं के लिए धारा 318 BNS लागू होती है, जबकि पुरानी घटनाओं के लिए धारा 420 IPC लागू होगी।\n"
                "- 2. आपराधिक धोखाधड़ी साबित करने के लिए यह दिखाना जरूरी है कि शुरुआत से ही बेईमानी की नीयत थी।"
            ),
            "plain_hinglish": (
                "Dhoka ya fraud ke case mein legal status:\n"
                "- 1. 1 July 2024 ke baad ki ghatnaon par Section 318 BNS lagu hota hai, jabki purani ghatnaon par Section 420 IPC lagu hota hai.\n"
                "- 2. Criminal cheating prove karne ke liye transaction ke start se hi dishonest intention hona zaroori hai."
            ),
        },
    }

    # Common colloquial patterns in Hindi / Hinglish mapped to keys
    PATTERN_MAP: List[Tuple[re.Pattern, str]] = [
        (re.compile(r"\b(chori|chura|churai|stolen|petty theft|minor theft|चोरी|चोर)\b", re.I), "chori"),
        (re.compile(r"\b(cheque|check|bounce|dishonour|चेक|बाउंस)\b", re.I), "cheque bounce"),
        (re.compile(r"\b(kirayedar|kirayedaar|makaan maalik|makan malik|evict|rent control|किरायेदार|किराया)\b", re.I), "kirayedar"),
        (re.compile(r"\b(jamanat|bail|anticipatory|giraftari|arrest|जमानत|गिरफ्तारी)\b", re.I), "jamanat"),
        (re.compile(r"\b(fir.*na|police.*mana|report.*na|fir.*nahi|thana|एफआईआर)\b", re.I), "fir na likhna"),
        (re.compile(r"\b(dhoka|dhokhadhadi|fraud|cheating|420|धोखा|धोखाधड़ी)\b", re.I), "dhoka"),
    ]

    @classmethod
    def detect_language(cls, query: str) -> str:
        """
        Detects if query is in Devanagari Hindi ('hi'), Hinglish ('hinglish'), or English ('en').
        """
        if re.search(r"[\u0900-\u097F]", query):
            return "hi"
        
        hinglish_words = {
            "kya", "kaise", "hota", "hoti", "hoga", "hogi", "karte", "karta",
            "chori", "kirayedar", "makaan", "jamanat", "kist", "paisa",
            "police", "dharpakad", "rok", "kanoon", "adalat", "thana", "muqadma",
            "kare", "karne", "gaya", "gayi", "gaye", "apradh", "dhoka", "dhokhadhadi",
            "wala", "wali", "meri", "mera", "mere", "par", "mein", "se", "ko", "hai", "hain"
        }
        tokens = set(re.findall(r"[a-zA-Z]+", query.lower()))
        matched = tokens.intersection(hinglish_words)
        if len(matched) >= 1:
            return "hinglish"
        return "en"

    @classmethod
    def analyze_indic_query(cls, query: str) -> Optional[Dict[str, Any]]:
        """
        Finds matching Indic legal entry for query expansion and synthesis.
        """
        q_lower = query.lower()
        for pattern, key in cls.PATTERN_MAP:
            if pattern.search(q_lower):
                entry = cls.INDIC_LEGAL_GLOSSARY[key].copy()
                entry["matched_key"] = key
                return entry
        return None

    @classmethod
    def get_plain_summary(cls, query: str, target_lang: Optional[str] = None) -> Optional[str]:
        """
        Retrieves the plain-language summary for the query in the requested language.
        """
        lang = target_lang or cls.detect_language(query)
        match = cls.analyze_indic_query(query)
        if not match:
            return None

        if lang == "hi":
            header = "### संक्षिप्त सरल कानूनी सारांश (Plain-Language Summary)"
            body = match["plain_hi"]
        elif lang == "hinglish":
            header = "### Aam Bhasha Mein Saral Summary (Plain-Language Summary)"
            body = match["plain_hinglish"]
        else:
            header = "### Plain-English Summary (For Quick Understanding)"
            body = match["plain_en"]

        return f"{header}\n{body}"
