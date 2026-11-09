"""
Unit tests for Phase 115: Multi-Turn Conversation Memory & Topic Pivot Resolution.
"""

import pytest
from legalmitra.orchestration.dialogue_manager import DialogueSession, LegalDialogueManager, DialogueTurn
from legalmitra.orchestration.decision_policy import LegalResponseState
from legalmitra.orchestration.topic_resolver import MultiTurnTopicPivotResolver, TurnIntentType
from legalmitra.orchestration.pipeline import LegalQueryPipeline


class TestPhase115MultiTurnMemory:
    def test_continuation_followup_coreference(self):
        session = DialogueSession(session_id="test_session_1")
        # Turn 1
        turn1 = DialogueTurn(
            turn_index=1,
            user_query="party ne cheque diya tha bounce ho gaya sign mismatch bolke",
            response_state=LegalResponseState.ANSWER_SUPPORTED,
            answer_text="Under Section 138 NI Act..."
        )
        session.turns.append(turn1)

        # Turn 2: Follow-up question with pronoun/ellipsis
        turn2_query = "what if the signature was actually done by his brother?"
        analysis = MultiTurnTopicPivotResolver.resolve_turn(turn2_query, session)

        assert analysis.intent_type == TurnIntentType.CONTINUATION_FOLLOWUP
        assert analysis.active_legal_domain == "CHEQUE_BOUNCE"
        assert "Cheque Bounce" in analysis.resolved_query
        assert "sign mismatch bolke" in analysis.resolved_query

    def test_explicit_topic_pivot(self):
        session = DialogueSession(session_id="test_session_2")
        turn1 = DialogueTurn(
            turn_index=1,
            user_query="party ne cheque diya tha bounce ho gaya sign mismatch bolke",
            response_state=LegalResponseState.ANSWER_SUPPORTED,
            answer_text="Section 138 NI Act..."
        )
        session.turns.append(turn1)

        # Turn 2: Completely new domain (Divorce/Maintenance)
        turn2_query = "my wife wants a divorce and demanding 20 lakhs maintenance"
        analysis = MultiTurnTopicPivotResolver.resolve_turn(turn2_query, session)

        assert analysis.intent_type == TurnIntentType.NEW_TOPIC_PIVOT
        assert analysis.active_legal_domain == "MATRIMONIAL_FAMILY"
        # Should NOT pollute with cheque bounce query
        assert "cheque" not in analysis.resolved_query.lower()

    def test_fact_amendment_handling(self):
        session = DialogueSession(session_id="test_session_3")
        turn1 = DialogueTurn(
            turn_index=1,
            user_query="cyber fraud me 20000 kat gaye account se",
            response_state=LegalResponseState.ANSWER_SUPPORTED,
            answer_text="Call 1930..."
        )
        session.turns.append(turn1)

        turn2_query = "actually the amount was 2 lakhs not 20000"
        analysis = MultiTurnTopicPivotResolver.resolve_turn(turn2_query, session)

        assert analysis.intent_type == TurnIntentType.FACT_AMENDMENT
        assert analysis.active_legal_domain == "CYBER_FRAUD"
        assert "Amended facts" in analysis.resolved_query

    def test_pipeline_dialogue_manager_integration(self):
        pipeline = LegalQueryPipeline()
        sid = "dialogue_integration_test"
        
        # Turn 1
        resp1 = pipeline.execute(query="someone gave me a cheque that bounced", session_id=sid)
        assert resp1 is not None
        assert "138" in resp1.answer_text

        # Turn 2: Follow-up
        resp2 = pipeline.execute(query="how many days do I have to send notice?", session_id=sid)
        assert resp2 is not None
        assert "30" in resp2.answer_text or "15" in resp2.answer_text
