"""Conversational Empathy & Behavioral Edge-Case Engine (Phase 84).

Handles conversational dialogue triggers, emotional and urgent citizen inputs,
proactive clarification handling, and realistic guidance for common edge cases.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class ConversationalBehaviorResponse:
    behavior_id: str
    trigger_type: str
    response_text: str
    suggested_followups: list[str]


CONVERSATIONAL_BEHAVIORS = [
    # 1. Open-ended distress: "Mere saath galat hua hai, kya karu?" / "Something wrong happened to me"
    ConversationalBehaviorResponse(
        behavior_id="BEHAVIOR_DISTRESS_OPEN",
        trigger_type="DISTRESS_CLARIFICATION",
        response_text=(
            "### LegalMitra Guidance (Aapki Madad Ke Liye)\n\n"
            "Main aapki poori madad karunga. Sahi kanooni rasta (legal remedy) batane ke liye kripya thoda vistar se batayein:\n\n"
            "1. **Kya hua hai?** (Jaise: paise ka fraud, police complaint, landlord/kirayedaar ka vivad, parivarik samasya, ya naukri/salary ka issue?)\n"
            "2. **Yeh kab hua?** (Aaj, haal hi mein, ya purana maamla hai?)\n"
            "3. **Kya aapke paas koi dastavej (proof/receipt/message) hain?**\n\n"
            "Agar aap kisi tatkal khatre ya emergency mein hain, toh bina deri kiye **112** par call karein."
        ),
        suggested_followups=[
            "Police ya FIR se juda maamla hai",
            "Online fraud ya bank se paise kate hain",
            "Makaan maalik ya kiraye ka vivaad hai",
            "Company salary nahi de rahi hai"
        ]
    ),

    # 2. Urgent police arrest: "Police ne mujhe pakad liya hai" / "Police arrested me"
    ConversationalBehaviorResponse(
        behavior_id="BEHAVIOR_URGENT_ARREST",
        trigger_type="URGENT_RIGHTS",
        response_text=(
            "### Immediate Legal Rights Upon Detention / Arrest\n\n"
            "Agar police ne aapko ya aapke kisi parichit ko hirasat (detention) ya arrest kiya hai, toh ye aapke tatkal adhikaar hain:\n\n"
            "1. **Right to Know Grounds (Section 47 BNSS & Article 22(1)):** Police ko turant batana hoga ki kis jurm mein aur kyu arrest kiya gaya hai.\n"
            "2. **Right to Inform Family (Section 48 BNSS):** Police ki zimmedari hai ki aapke kisi ek parivar ke sadasya ya dost ko arrest aur police station ki jaankari turant de.\n"
            "3. **Right to a Lawyer (Section 41D / Article 22(1)):** Aapko poochtachh (interrogation) ke dauran apne advocate se milne ka adhikaar hai.\n"
            "4. **Production within 24 Hours (Section 57 BNSS & Article 22(2)):** Police kisi ko bhi bina Magistrate ke order ke 24 ghante se zyada custody mein nahi rakh sakti.\n"
            "5. **Free Legal Aid:** Agar advocate afford nahi kar sakte, toh Magistrate se **DLSA (Free Legal Aid)** advocate ki maang karein (Helpline: **15100**).\n\n"
            "Police ke sath physical jhadap na karein, shaant rahein aur kanooni niyam anusar advocate ki maang karein."
        ),
        suggested_followups=[
            "Bailable offence hai ya non-bailable?",
            "Agrim jamanat (Anticipatory Bail) kaise lein?",
            "DLSA se free lawyer kaise milega?"
        ]
    ),

    # 3. Wanting to file a case: "Mujhe case karna hai" / "I want to file a case"
    ConversationalBehaviorResponse(
        behavior_id="BEHAVIOR_FILE_CASE",
        trigger_type="INTENT_DISCOVERY",
        response_text=(
            "### Case File Karne Ke Sambandh Mein Jaankari\n\n"
            "Case darj karne ke liye sahi forum aur kanoon ka chunav zaroori hai. Kripya batayein:\n\n"
            "1. **Maamla kaisa hai?**\n"
            "   - **Criminal:** Dhokhadhadi, maarpeet, dhamki, chori (Isme Police FIR ya Magistrate Complaint hoti hai).\n"
            "   - **Civil / Recovery:** Udhaar paisa wapas lena, property/zameen ka vivaad, contract breach (Isme Civil Suit hota hai).\n"
            "   - **Consumer:** Kharab samaan, company ki laparwahi (Consumer Commission e-Daakhil par hota hai).\n"
            "   - **Family / Matrimonial:** Maintenance, gharelu hinsa, talak.\n"
            "2. **Aap kiske khilaf karwayi karna chahte hain aur incident kis shehar mein hua?**\n\n"
            "Aap apni samasya detail mein likhein, main aapko step-by-step guidance dunga."
        ),
        suggested_followups=[
            "Online cheating ka case karna hai",
            "Udhaar paisa wapas lene ka case",
            "Defective product ke liye consumer case"
        ]
    ),

    # 4. Wanting legal notice: "Mujhe ek legal notice likh do" / "Draft a legal notice"
    ConversationalBehaviorResponse(
        behavior_id="BEHAVIOR_DRAFT_NOTICE",
        trigger_type="DRAFTING_ASSISTANCE",
        response_text=(
            "### Statutory Legal Notice Drafting\n\n"
            "Main aapke liye formal legal notice draft kar sakta hoon. Structured legal notice taiyar karne ke liye kripya yeh zaroori details dein:\n\n"
            "1. **Notice Type:** Cheque Bounce (Section 138 NI Act), Makaan Khali Karane Ka Notice (Section 106 TPA), ya Unpaid Salary / Money Recovery Notice?\n"
            "2. **Bhejne Wale Ka Naam & Pata (Sender / Claimant)**\n"
            "3. **Jise Bhejna Hai Uska Naam & Pata (Recipient)**\n"
            "4. **Ghatna Ka Vivaran (Facts):** Amount, dates, cheque number ya contract ki date.\n"
            "5. **Demand:** Kitne din ka samay dena hai (Aam taur par 15 din ka statutory notice period hota hai).\n\n"
            "Aap upar top-right button **'Export Memo'** se Section 138 statutory draft turant download bhi kar sakte hain."
        ),
        suggested_followups=[
            "Section 138 Cheque bounce notice draft karo",
            "Unpaid salary recovery notice draft karo",
            "Tenant eviction notice draft karo"
        ]
    ),

    # 5. Outcome guarantee: "Kya main jeet jaunga?" / "Will I win the case?"
    ConversationalBehaviorResponse(
        behavior_id="BEHAVIOR_NO_GUARANTEE",
        trigger_type="OUTCOME_REALISM",
        response_text=(
            "### Kanooni Niyam: Outcome Guarantee Nahi Di Jaa Sakti\n\n"
            "Kanoon aur judicial ethics ke anusar, koi bhi advocate ya kanooni salahkar kisi bhi case ke nateeje (victory/winning) ki **100% guarantee nahi de sakta**.\n\n"
            "**Court ka faisla kin baaton par nirbhar karta hai:**\n"
            "1. **Documentary Evidence:** Aapke paas kitne thos dastavej (receipts, contracts, bank statements, messages) hain.\n"
            "2. **Statutory Compliance:** Kya kanooni samay-seema (Limitation period) ke bheetar kadam uthaya gaya hai.\n"
            "3. **Witness Credibility & Cross-Examination:** Court mein gavahon ki gawahi aur cross-examination ka prabhav.\n"
            "4. **Judicial Precedents:** Supreme Court aur High Court ke binding nirdesh.\n\n"
            "Aapka case kitna mazboot hai, yeh check karne ke liye apne sabhi dastavej kisi competent advocate se verify karwayein."
        ),
        suggested_followups=[
            "Apne case ke evidence kaise majboot karein?",
            "Limitation period kaise check karein?",
            "Free legal aid advocate se salaah kaise lein?"
        ]
    ),

    # 6. Demand for exact section: "Mujhe exact section batao" / "Tell me exact section"
    ConversationalBehaviorResponse(
        behavior_id="BEHAVIOR_EXACT_SECTION",
        trigger_type="STATUTE_MAPPING",
        response_text=(
            "### Exact Statutory Sections Under Indian Law\n\n"
            "Kanoon mein sahi section hamesha ghatna ke specific facts par nirbhar karta hai. Bharat ke pramukh kanooni sections:\n\n"
            "- **Criminal Dhokhadhadi / Cheating:** Section 318 BNS, 2023 (Pehle Section 420 IPC).\n"
            "- **Dhamki Dena / Intimidation:** Section 351 BNS, 2023 (Pehle Section 506 IPC).\n"
            "- **FIR Darj Karwana (SP Application):** Section 173(4) BNSS, 2023 (Pehle 154(3) CrPC).\n"
            "- **Magistrate FIR Order:** Section 175(3) BNSS, 2023 (Pehle 156(3) CrPC).\n"
            "- **Cheque Bounce:** Section 138 Negotiable Instruments Act, 1881.\n"
            "- **Defective Goods / Consumer:** Section 2(10) & Section 35 Consumer Protection Act, 2019.\n"
            "- **Maintenance (Patni/Bachhon Ka Kharcha):** Section 144 BNSS, 2023 (Pehle Section 125 CrPC).\n\n"
            "Aap apni ghatna batayein, main aapko specific governing section bataunga."
        ),
        suggested_followups=[
            "BNS aur IPC ke transitions dekhne hain",
            "BNSS aur CrPC ke badlav dekhne hain",
            "Meri specific samasya ka section batao"
        ]
    ),

    # 7. Mistake confession: "Maine galti kar di, ab kya hoga?" / "I made a mistake, what happens now?"
    ConversationalBehaviorResponse(
        behavior_id="BEHAVIOR_MISTAKE_GUIDANCE",
        trigger_type="NON_JUDGMENTAL_COUNSEL",
        response_text=(
            "### Legal Perspective & Damage Mitigation\n\n"
            "Ghabrayein nahi. Kanoon har vyakti ko apna paksh rakhne aur sahi kanooni bachaav (fair defense) ka poora adhikaar deta hai:\n\n"
            "1. **Bina Dastavej Dekhe Darr Na Banayein:** Pehle samjhein ki mamla civil nature ka hai ya criminal nature ka.\n"
            "2. **Right Against Self-Incrimination (Article 20(3)):** Bharat ke samvidhan ke mutabik kisi bhi vyakti ko apne hi khilaf gavahi dene ke liye majboor nahi kiya ja sakta.\n"
            "3. **Compounding & Settlement:** Kai mamle (jaise cheque bounce, choti takraar, civil disputes) aapsi samjhoute (compromise/compounding) se court mein ba-izzat khatam ho jate hain.\n"
            "4. **Kanooni Salah:** Kisi bhi police statement par hastakshar karne ya unauthorized transaction se pehle ek advocate se zaroor milein.\n\n"
            "Kya galti hui hai? Vistar se batayein taaki kanooni remedies samjhai ja sakein."
        ),
        suggested_followups=[
            "Kya yeh bailable offence hai?",
            "Compromise / Settlement kaise hota hai?",
            "Anticipatory bail kab lagani hoti hai?"
        ]
    ),

    # 8. No proof / evidence: "Mere paas koi proof nahi hai" / "I have no proof"
    ConversationalBehaviorResponse(
        behavior_id="BEHAVIOR_NO_PROOF_DISCOVERY",
        trigger_type="EVIDENCE_DISCOVERY",
        response_text=(
            "### Dastavej Na Hone Par Saboot Kaise Jutayein\n\n"
            "Aksar logon ko lagta hai ki unke paas saboot nahi hai, lekin kanoon kayi tarah ke secondary aur circumstantial evidence ko maanta hai:\n\n"
            "1. **Digital Evidence (Section 61–63 BSA, 2023):** WhatsApp chats, SMS, call detail records (CDR), UPI transaction logs, email threads sab court mein valid electronic evidence hain.\n"
            "2. **Oral Evidence & Gawah:** Ghatna ke samay maujood kisi bhi vyakti ki gawahi (eyewitness testimony) kanoon mein maanya hai.\n"
            "3. **Bank & Financial Trails:** Cash ke alawa bank passbook entry, ATM withdrawal slip, UPI transaction ID thos saboot maane jate hain.\n"
            "4. **CCTV Footage & Government Records:** Ghatna sthal ke aas-paas ki CCTV footage police ko preserve karne ki request karein.\n"
            "5. **RTI Act, 2005:** Agar sarkar ya authority se sambandhit mamla hai, toh RTI ke zariye certified documents nikale ja sakte hain.\n\n"
            "Aapka mamla kisse juda hai? Main batata hoon ki isme kaunse saboot kaam aayenge."
        ),
        suggested_followups=[
            "WhatsApp chat court mein kaise submit karein?",
            "Bank statement se saboot kaise banayein?",
            "CCTV footage preserve karne ka kanooni niyam"
        ]
    ),
    # 9. Conversational Greeting: "hello", "hi", "hey", "namaste"
    ConversationalBehaviorResponse(
        behavior_id="BEHAVIOR_GREETING",
        trigger_type="GREETING_ORIENTATION",
        response_text=(
            "### Namaste! Welcome to LegalMitra (भारतीय कानूनी मित्र)\n\n"
            "I am your dedicated AI Legal Companion for Indian Law. I help citizens, consumers, and advocates understand their legal rights and remedies in plain, simple words.\n\n"
            "**How I can help you today:**\n"
            "- **Police & Criminal Matters:** What to do if police refuse your FIR, arrest rights under BNSS, bail rules.\n"
            "- **Cybercrime & Online Fraud:** Urgent golden-hour steps for unauthorized bank debits (Helpline 1930).\n"
            "- **Consumer Disputes:** Defective products, e-commerce non-delivery, warranty refusal (Helpline 1915).\n"
            "- **Tenant & Property Issues:** Illegal landlord eviction, security deposit disputes, land encroachment.\n"
            "- **Employment & Salary:** Unpaid salaries, sudden termination without contractual notice.\n"
            "- **Women & Family Rights:** Maintenance under Sec 144 BNSS, domestic violence protection, free legal aid (15100).\n\n"
            "Please describe your problem or question in your own everyday words."
        ),
        suggested_followups=[
            "Police are refusing to register my FIR",
            "Someone stole money from my bank account",
            "Landlord asking me to vacate tomorrow",
            "Company not paying my salary"
        ]
    ),

    # 10. Capability Query: "what is this?", "who are you?", "what can you do?"
    ConversationalBehaviorResponse(
        behavior_id="BEHAVIOR_CAPABILITY",
        trigger_type="CAPABILITY_EXPLANATION",
        response_text=(
            "### About LegalMitra\n\n"
            "LegalMitra is a sovereign Indian legal guidance engine updated with the new 2024–2025 criminal enactments "
            "(Bharatiya Nyaya Sanhita, Bharatiya Nagarik Suraksha Sanhita, and Bharatiya Sakshya Adhiniyam) as well as consumer, labour, and constitutional statutes.\n\n"
            "**Key Capabilities:**\n"
            "1. **Plain-Words Legal Explanation:** We translate complex statutory sections into simple English and Hindi.\n"
            "2. **Actionable Step-by-Step Guidance:** Clear steps on where to go, what complaint to write, and who to contact.\n"
            "3. **Evidence & Helplines Checklist:** Official national helplines (112, 1930, 1915, 15100) and proof preservation checklists.\n"
            "4. **Verified Statutory Citations:** Accurate section numbers for legal proceedings.\n\n"
            "Type any question below to get started."
        ),
        suggested_followups=[
            "What to do in case of cyber fraud?",
            "Can police arrest without warrant?",
            "How to send a Section 138 cheque bounce notice?"
        ]
    )
]


class ConversationalEmpathyEngine:
    """Detects and resolves conversational, empathetic, and distressed citizen queries."""

    @classmethod
    def match_behavioral_query(cls, query: str) -> Optional[ConversationalBehaviorResponse]:
        if not query or not query.strip():
            return None

        q = query.lower().strip()
        import re
        words = set(re.findall(r"\w+", q))

        # 0. Greeting & Capability Detection
        greetings = ["hello", "hi", "hey", "namaste", "pranam", "good morning", "good evening", "good afternoon", "kya haal hai", "suno", "help"]
        if q in greetings or any(q == g or q.startswith(g + " ") for g in greetings):
            return next(b for b in CONVERSATIONAL_BEHAVIORS if b.behavior_id == "BEHAVIOR_GREETING")

        capability_phrases = ["what is this", "who are you", "what can you do", "what do you do", "tell me about yourself", "how does this work", "how do you work", "kya hai ye", "aap kaun ho"]
        if any(cp in q for cp in capability_phrases):
            return next(b for b in CONVERSATIONAL_BEHAVIORS if b.behavior_id == "BEHAVIOR_CAPABILITY")

        # 1. Open distress
        if any(p in q for p in ["mere saath galat", "mere sath galat", "kya karu", "something wrong happened", "kuch galat hua"]):
            return next(b for b in CONVERSATIONAL_BEHAVIORS if b.behavior_id == "BEHAVIOR_DISTRESS_OPEN")

        # 2. Urgent police arrest
        if any(p in q for p in ["police ne mujhe pakad", "police pakad", "police arrested me", "arrested by police", "police ne pakad"]):
            return next(b for b in CONVERSATIONAL_BEHAVIORS if b.behavior_id == "BEHAVIOR_URGENT_ARREST")

        # 3. Wanting to file case
        if any(p in q for p in ["mujhe case karna", "case karna hai", "case file karna", "i want to file a case", "file case against"]):
            return next(b for b in CONVERSATIONAL_BEHAVIORS if b.behavior_id == "BEHAVIOR_FILE_CASE")

        # 4. Wanting legal notice
        if any(p in q for p in ["legal notice likh", "notice draft", "notice likh do", "draft a legal notice", "write legal notice"]):
            return next(b for b in CONVERSATIONAL_BEHAVIORS if b.behavior_id == "BEHAVIOR_DRAFT_NOTICE")

        # 5. Outcome guarantee
        if any(p in q for p in ["kya main jeet", "kya mai jeet", "will i win", "jeetna pakka", "can i win the case"]):
            return next(b for b in CONVERSATIONAL_BEHAVIORS if b.behavior_id == "BEHAVIOR_NO_GUARANTEE")

        # 6. Demand for exact section
        if any(p in q for p in ["exact section batao", "kaun sa section", "tell me exact section", "which section applies"]):
            return next(b for b in CONVERSATIONAL_BEHAVIORS if b.behavior_id == "BEHAVIOR_EXACT_SECTION")

        # 7. Mistake confession
        if any(p in q for p in ["maine galti kar di", "meri galti", "i made a mistake", "ab kya hoga", "what will happen to me"]):
            return next(b for b in CONVERSATIONAL_BEHAVIORS if b.behavior_id == "BEHAVIOR_MISTAKE_GUIDANCE")

        # 8. No proof discovery
        if any(p in q for p in ["mere paas koi proof", "mere pass proof nahi", "i have no proof", "no evidence what to do"]):
            return next(b for b in CONVERSATIONAL_BEHAVIORS if b.behavior_id == "BEHAVIOR_NO_PROOF_DISCOVERY")

        return None

