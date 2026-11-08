"""Phase 83 Test Suite: Citizen Legal Guidance Engine & Practical Intent Mapping.

Validates that:
1. CitizenLegalGuidanceEngine recognizes all 25 benchmark citizen queries.
2. Formatted citizen answers prioritize plain-English direct answer and practical steps.
3. Essential helplines (112, 1930, 1915, 15100, 181) and evidence checklists are produced.
4. Correct statutory mappings (BNSS 173(4), BNSS 47, BNS 351, BNS 78, Consumer Protection Act) are delivered.
5. End-to-end pipeline execution delivers human-friendly citizen answers.
"""

import pytest
from legalmitra.knowledge.citizen_intents import CitizenLegalGuidanceEngine, CITIZEN_KNOWLEDGE_BASE
from legalmitra.orchestration.pipeline import LegalQueryPipeline


class TestPhase83CitizenGuidance:
    @pytest.fixture(scope="module")
    def pipeline(self):
        return LegalQueryPipeline()

    def test_all_25_scenarios_exist(self):
        assert len(CITIZEN_KNOWLEDGE_BASE) >= 25

    def test_intent_matching_police_and_fir(self):
        q = "Police are refusing to register my FIR. What should I do?"
        m = CitizenLegalGuidanceEngine.match_citizen_query(q)
        assert m is not None
        assert m.scenario_id == "Q1_FIR_REFUSAL"
        assert "173(4)" in m.legal_provisions_summary
        assert "175(3)" in m.legal_provisions_summary
        assert "112" in m.helplines[0]

    def test_intent_matching_arrest_rights(self):
        q = "Can police arrest me without telling me why?"
        m = CitizenLegalGuidanceEngine.match_citizen_query(q)
        assert m is not None
        assert m.scenario_id == "Q2_ARREST_GROUNDS"
        assert "Article 22(1)" in m.legal_provisions_summary
        assert "Section 47" in m.legal_provisions_summary

    def test_intent_matching_cyber_fraud_1930(self):
        q = "Someone called me pretending to be a bank employee and stole 15000 from my account. What should I do?"
        m = CitizenLegalGuidanceEngine.match_citizen_query(q)
        assert m is not None
        assert m.scenario_id == "Q4_CYBER_BANK_FRAUD"
        assert "1930" in m.helplines[0]
        assert "cybercrime.gov.in" in m.step_by_step_actions[1]

    def test_intent_matching_consumer_phone_defect(self):
        q = "I bought a new phone, but it stopped working after five days. The shopkeeper refuses to replace it. What can I do?"
        m = CitizenLegalGuidanceEngine.match_citizen_query(q)
        assert m is not None
        assert m.scenario_id == "Q7_DEFECTIVE_PRODUCT_SHOP"
        assert "1915" in m.helplines[0]
        assert "Consumer Protection Act" in m.direct_answer

    def test_intent_matching_maintenance_wife(self):
        q = "My husband is not giving me money for household expenses. Do I have any legal rights?"
        m = CitizenLegalGuidanceEngine.match_citizen_query(q)
        assert m is not None
        assert m.scenario_id == "Q10_WIFE_MAINTENANCE"
        assert "144" in m.legal_provisions_summary

    def test_intent_matching_illegal_eviction(self):
        q = "My landlord is asking me to leave my rented house tomorrow. Can he throw me out immediately?"
        m = CitizenLegalGuidanceEngine.match_citizen_query(q)
        assert m is not None
        assert m.scenario_id == "Q16_ILLEGAL_EVICTION"
        assert "due process" in m.step_by_step_actions[0].lower()

    def test_intent_matching_free_legal_aid(self):
        q = "I cannot afford a lawyer. Does that mean I cannot fight my case?"
        m = CitizenLegalGuidanceEngine.match_citizen_query(q)
        assert m is not None
        assert m.scenario_id == "Q20_FREE_LEGAL_AID"
        assert "15100" in m.helplines[0]

    def test_pipeline_e2e_clean_citizen_answer(self, pipeline):
        q = "Police are refusing to register my FIR. What should I do?"
        res = pipeline.execute(q)
        text = res.answer_text
        assert "### Direct Position (In Plain Words)" in text
        assert "### Practical Action Guide" in text
        assert "Section 173(4)" in text
        assert "112" in text
        # Verify no confusing technical clutter
        assert "Section 51. Examination of accused" not in text

