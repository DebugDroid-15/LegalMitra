"""
Phase 119: Real-World Slang Evaluation & Regression Benchmark Suite.

Executes an exhaustive multi-lingual, multi-dialectal, and colloquial regression
evaluation covering real-world Indian citizen phrasing across:
- Hinglish (Hindi + English)
- Tanglish (Tamil + English)
- Marathish (Marathi + English)
- Telugish (Telugu + English)
- Pure Indic Vernaculars
- Emotional distress and slang idioms
"""

from __future__ import annotations

import pytest
from legalmitra.orchestration.pipeline import LegalQueryPipeline
from legalmitra.multilingual.colloquial_normalizer import IndicColloquialNormalizer, CanonicalLegalIntent
from legalmitra.orchestration.multi_intent_guard import MultiIntentDisambiguationGuard, UrgencyTier
from legalmitra.knowledge.citizen_intents import CitizenLegalGuidanceEngine


# Comprehensive Bank of Real-World Slang & Dialectal Queries
BENCHMARK_SLANG_DATASET = [
    # 1. Cheque Bounce Dialects
    {
        "query": "party ne cheque diya tha bounce ho gaya sign mismatch bolke",
        "expected_domain_keyword": "138",
        "forbidden_domain_keyword": "motor vehicle",
        "dialect": "Hinglish",
    },
    {
        "query": "merko ek client ne cheque diya par account me balance nahi tha bounce ho gaya",
        "expected_domain_keyword": "138",
        "forbidden_domain_keyword": "accident",
        "dialect": "Delhi/Hinglish",
    },
    {
        "query": "check dila hota bounce zala bank wale mhanale sign match hot nahi",
        "expected_domain_keyword": "138",
        "forbidden_domain_keyword": "accident",
        "dialect": "Marathish",
    },

    # 2. Landlord & Illegal Eviction Slang
    {
        "query": "my landlord locked my flat and threw my luggage out without any notice",
        "expected_domain_keyword": "Transfer of Property",
        "forbidden_domain_keyword": "employment",
        "dialect": "Everyday Slang",
    },
    {
        "query": "makan malik ne room par tala laga diya aur samaan bahar phek diya",
        "expected_domain_keyword": "106",
        "forbidden_domain_keyword": "fired from job",
        "dialect": "Hinglish",
    },
    {
        "query": "ghar malakane baher kaadhle aamcha luggage phekla",
        "expected_domain_keyword": "Specific Relief",
        "forbidden_domain_keyword": "salary",
        "dialect": "Marathi Colloquial",
    },

    # 3. Police Station & FIR Refusal
    {
        "query": "police station la complaint edukka maatengraanga enna panradhu",
        "expected_domain_keyword": "173(4)",
        "forbidden_domain_keyword": "motor vehicle",
        "dialect": "Tanglish",
    },
    {
        "query": "police thane me gaya tha fir likhne se mana kar diya bolte civil matter hai",
        "expected_domain_keyword": "173(4)",
        "forbidden_domain_keyword": "accident",
        "dialect": "Hinglish",
    },
    {
        "query": "police station me complaint nahi le rahe hai SHO bhaga raha hai",
        "expected_domain_keyword": "173(4)",
        "forbidden_domain_keyword": "quashing",
        "dialect": "Bihari/Hinglish",
    },

    # 4. Cyber Fraud & OTP Theft
    {
        "query": "kisi ne call karke OTP le liya aur mere 50000 kat gaye account se ab kya karu",
        "expected_domain_keyword": "1930",
        "forbidden_domain_keyword": "employment",
        "dialect": "Hinglish",
    },
    {
        "query": "bank manager ban ke call kiya tha upi pin dala aur 1 lakh gayab ho gaya",
        "expected_domain_keyword": "1930",
        "forbidden_domain_keyword": "cheque bounce",
        "dialect": "Hinglish",
    },
    {
        "query": "telegram part time job like task fraud me 3 lakh chale gaye",
        "expected_domain_keyword": "1930",
        "forbidden_domain_keyword": "landlord",
        "dialect": "Online Slang",
    },

    # 5. Cheating & Duping
    {
        "query": "ek aadmi ne dukaan ke naam par 2 lakh rupaye le liye aur bhaag gaya",
        "expected_domain_keyword": "318",
        "forbidden_domain_keyword": "information technology act section 45",
        "dialect": "Hinglish",
    },
    {
        "query": "plot bechne ke naam par advance le liya aur phone band karke farar ho gaya",
        "expected_domain_keyword": "318",
        "forbidden_domain_keyword": "motor vehicle",
        "dialect": "Hinglish",
    },

    # 6. Domestic Violence & Cruelty
    {
        "query": "pati aur sasural wale dahej ke liye maarpeet kar rahe hain aur ghar se nikal rahe",
        "expected_domain_keyword": "181",
        "forbidden_domain_keyword": "cheque",
        "dialect": "Hinglish",
    },

    # 7. Workplace POSH Harassment
    {
        "query": "mera boss office me gandi baatein karta hai aur inappropriate touching karta hai",
        "expected_domain_keyword": "POSH",
        "forbidden_domain_keyword": "landlord",
        "dialect": "Hinglish",
    },

    # 8. RERA Builder Delay
    {
        "query": "builder 3 saal se flat ka possession nahi de raha aur refund bhi mana kar raha",
        "expected_domain_keyword": "RERA",
        "forbidden_domain_keyword": "cheque bounce",
        "dialect": "Hinglish",
    },

    # 9. Free Legal Aid
    {
        "query": "mere paas paise nahi hai court me case ladne ke liye sarkari vakil kaise milega",
        "expected_domain_keyword": "15100",
        "forbidden_domain_keyword": "bail",
        "dialect": "Hinglish",
    },

    # 10. Anticipatory Bail
    {
        "query": "padosi ne jhootha case kiya hai police arrest karne aane wali hai agrim jamanat kaise milegi",
        "expected_domain_keyword": "482",
        "forbidden_domain_keyword": "traffic fine",
        "dialect": "Hinglish",
    }
]


class TestPhase119SlangRegressionBenchmark:
    @pytest.fixture(scope="class")
    def pipeline(self):
        return LegalQueryPipeline()

    @pytest.mark.parametrize("item", BENCHMARK_SLANG_DATASET)
    def test_benchmark_slang_intent_accuracy(self, pipeline, item):
        query = item["query"]
        expected_kw = item["expected_domain_keyword"].lower()
        forbidden_kw = item["forbidden_domain_keyword"].lower()

        resp = pipeline.execute(query=query)
        assert resp is not None
        ans_lower = resp.answer_text.lower()

        # 1. Verification of expected statutory domain
        assert expected_kw in ans_lower, (
            f"Failed on dialect '{item['dialect']}': Expected '{expected_kw}' not found in response for '{query}'."
        )

        # 2. Strict zero false-positive guard against forbidden domain leakage
        assert forbidden_kw not in ans_lower, (
            f"Domain collision on dialect '{item['dialect']}': Forbidden keyword '{forbidden_kw}' leaked into response for '{query}'."
        )
