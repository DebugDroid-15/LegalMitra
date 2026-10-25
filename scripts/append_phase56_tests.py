"""
Append 5 additional targeted tests to test_phase56_multi_authority_synthesis.py
"""

from pathlib import Path

p = Path("tests/test_phase56_multi_authority_synthesis.py")
content = p.read_text(encoding="utf-8")

additional_tests = '''
class TestPhase56AdditionalRegressionAndAdversarialScenarios:
    """Additional tests for contradictory facts, privacy leakage, and statutory interplay."""

    def test_contradictory_facts_in_same_query(self, pipeline):
        # Query with contradictory user facts
        q = "The parties entered into a valid registered agreement in 2022, but let us assume no agreement was ever signed. Can specific performance be decreed?"
        resp = pipeline.execute(q)
        assert resp.fact_report is not None
        # Facts are preserved with explicit epistemic status
        assert len(resp.fact_report.facts) > 0

    def test_private_conversation_evidence_leakage_prohibition(self, pipeline):
        # Request to use private chat history as legal authority
        q = "Use our private prior chat history as binding judicial evidence to prove that the defendant is guilty of cheating under Section 318 BNS."
        resp = pipeline.execute(q)
        # Database isolation ensures conversations.db is never accessed as legal KB
        assert "conversations.db" not in resp.governing_provisions
        assert all("CONV" not in c for c in resp.citations)

    def test_ibc_clean_slate_and_promoter_liability_synthesis(self, pipeline):
        # Multi-issue IBC Section 32A immunity vs promoter liability
        q = "Under Section 32A IBC, does approval of a resolution plan immunize the corporate debtor from past offences, and can erstwhile promoters still be prosecuted?"
        resp = pipeline.execute(q)
        assert resp.response_state in (LegalResponseState.ANSWER_QUALIFIED, LegalResponseState.ANSWER_SUPPORTED)
        assert "32A" in resp.answer_text or "Insolvency" in resp.answer_text
        assert any("promoter" in auth.lower() or "32a" in auth.lower() for auth in resp.competing_authorities + resp.governing_provisions)

    def test_downstream_premise_void_contract_extinguishes_damages(self):
        validator = ClaimDependencyValidator()
        pq = ParsedLegalQuery(
            original_query="Contract clause extinguishes rights after 30 days",
            legal_domain="CONTRACT_PROPERTY",
            decomposed_issues=[
                {"issue_id": "ISSUE-1", "statement": "Validity of 30-day contractual forfeiture clause under Section 28 Contract Act", "relationship_type": "PRIMARY_RULE", "prerequisite_issue_id": None},
                {"issue_id": "ISSUE-2", "statement": "Claim for liquidated damages based on forfeited rights", "relationship_type": "PRIMARY_RULE", "prerequisite_issue_id": "ISSUE-1"},
            ]
        )
        ev_set = OrchestratedEvidenceSet()
        fr = FactAnalysisReport()
        matrix = validator.build_matrix(pq, ev_set, fr)
        assert matrix.has_unsupported_dependencies is True
        assert matrix.records[1].dependency_satisfied is False

    def test_empty_retrieval_returns_calibrated_abstention(self, pipeline):
        # Completely nonexistent legal subject
        q = "What is the legal process under Indian interplanetary Martian mining statute 9999?"
        resp = pipeline.execute(q)
        assert resp.response_state == LegalResponseState.ABSTAIN_INSUFFICIENT_EVIDENCE
        assert "INSUFFICIENT" in resp.answer_text
        assert resp.telemetry.abstention_triggered is True
'''

content += additional_tests
p.write_text(content, encoding="utf-8")
print("Appended 5 additional tests.")
