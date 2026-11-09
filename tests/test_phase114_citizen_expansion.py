"""
Unit tests for Phase 114: Citizen Knowledge Base Expansion (Q28 to Q35).
"""

import pytest
from legalmitra.knowledge.citizen_intents import (
    CITIZEN_KNOWLEDGE_BASE,
    CitizenLegalGuidanceEngine,
)
from legalmitra.orchestration.pipeline import LegalQueryPipeline


class TestPhase114ExpandedCitizenScenarios:
    def test_total_scenarios_count_at_least_35(self):
        assert len(CITIZEN_KNOWLEDGE_BASE) >= 35

    def test_posh_workplace_sexual_harassment_matching(self):
        query = "My boss is sexually harassing me at the workplace and sending inappropriate messages. What can I do?"
        res = CitizenLegalGuidanceEngine.match_citizen_query(query)
        assert res is not None
        assert res.scenario_id == "Q28_POSH_WORKPLACE_HARASSMENT"
        assert "Internal Committee" in res.direct_answer or "POSH Act" in res.direct_answer
        assert any("75" in st for st in res.governing_statutes)

    def test_domestic_violence_protection_matching(self):
        query = "My husband and in-laws are beating me and threatening to throw me out of the house"
        res = CitizenLegalGuidanceEngine.match_citizen_query(query)
        assert res is not None
        assert res.scenario_id == "Q29_DOMESTIC_VIOLENCE_PROTECTION"
        assert "181" in res.helplines or "112 (Emergency Police)" in res.helplines
        assert any("85" in st for st in res.governing_statutes)

    def test_rera_builder_delay_possession(self):
        query = "The builder has delayed my flat possession by 2 years and refusing refund"
        res = CitizenLegalGuidanceEngine.match_citizen_query(query)
        assert res is not None
        assert res.scenario_id == "Q30_BUILDER_DELAY_RERA"
        assert "Section 18" in res.direct_answer or "Section 18" in res.legal_provisions_summary

    def test_online_defamation_trolling(self):
        query = "Someone is defaming me online on Instagram with false allegations to ruin my character"
        res = CitizenLegalGuidanceEngine.match_citizen_query(query)
        assert res is not None
        assert res.scenario_id == "Q31_ONLINE_DEFAMATION_TROLLING"
        assert any("356" in st for st in res.governing_statutes)

    def test_telegram_task_crypto_scam(self):
        query = "I was duped in a telegram part time job like task scam of 3 lakhs"
        res = CitizenLegalGuidanceEngine.match_citizen_query(query)
        assert res is not None
        assert res.scenario_id == "Q32_TELEGRAM_TASK_CRYPTO_SCAM"
        assert any("1930" in h for h in res.helplines)

    def test_ancestral_property_partition_daughters(self):
        query = "Can a married daughter claim equal share in father ancestral property partition?"
        res = CitizenLegalGuidanceEngine.match_citizen_query(query)
        assert res is not None
        assert res.scenario_id == "Q33_ANCESTRAL_PROPERTY_PARTITION"
        assert any("Hindu Succession Act" in st for st in res.governing_statutes)

    def test_medical_negligence(self):
        query = "Hospital and doctor committed gross medical negligence during laparoscopic surgery"
        res = CitizenLegalGuidanceEngine.match_citizen_query(query)
        assert res is not None
        assert res.scenario_id == "Q34_MEDICAL_NEGLIGENCE"
        assert "Consumer Protection Act" in res.governing_statutes[0]

    def test_anticipatory_bail_bnss_482(self):
        query = "I am apprehending arrest in a false criminal case, how to apply for anticipatory bail?"
        res = CitizenLegalGuidanceEngine.match_citizen_query(query)
        assert res is not None
        assert res.scenario_id == "Q35_ANTICIPATORY_BAIL"
        assert any("482" in st for st in res.governing_statutes)
