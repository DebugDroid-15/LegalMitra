"""Phase 68 Test Suite: Multi-Turn Legal Dialogue Memory & Clarification Resolver."""

import pytest
from legalmitra.orchestration.decision_policy import LegalResponseState
from legalmitra.orchestration.dialogue_manager import LegalDialogueManager, DialogueSession, DialogueTurn
from legalmitra.orchestration.pipeline import LegalQueryPipeline
from legalmitra.models.local_adapter import LocalLegalModelAdapter, ModelAdapterConfig


class TestPhase68MultiTurnDialogueMemory:
    """Verifies dialogue memory tracking, coreference contextualization, clarification resolution, and REPL history."""

    def test_session_lifecycle_and_reset(self):
        """Test dialogue session creation, turn accumulation, and state resetting."""
        dm = LegalDialogueManager()
        sess = dm.get_or_create_session("sess_test_1")
        assert len(sess.turns) == 0

        dm.record_turn(
            session_id="sess_test_1",
            user_query="What is Section 9 Arbitration Act?",
            response_state=LegalResponseState.ANSWER_SUPPORTED,
            answer_text="Section 9 provides for interim measures.",
            citations=["Arbitration Act 1996 s.9"],
            governing_provisions=["Arbitration Act 1996 s.9"],
            context_date="2024-01-01",
            jurisdiction="IN"
        )
        assert len(sess.turns) == 1
        assert sess.persisted_context_date == "2024-01-01"
        assert sess.persisted_jurisdiction == "IN"

        sess.reset()
        assert len(sess.turns) == 0
        assert sess.persisted_context_date is None
        assert sess.persisted_jurisdiction is None

    def test_contextualize_query_with_prior_turn_coreference(self):
        """Test that short follow-up questions inherit context from prior query."""
        dm = LegalDialogueManager()
        dm.record_turn(
            session_id="sess_coref",
            user_query="Can an interim injunction be granted in infrastructure project contracts?",
            response_state=LegalResponseState.ANSWER_QUALIFIED,
            answer_text="Section 20A bars injunctions.",
            citations=[],
            governing_provisions=["Specific Relief Act s.20A"]
        )

        ctx = dm.contextualize_query(
            query="Can I appeal against it?",
            session_id="sess_coref"
        )
        assert "Can I appeal against it?" in ctx["enriched_query"]
        assert "Context from prior question" in ctx["enriched_query"]
        assert "infrastructure project contracts" in ctx["enriched_query"]

    def test_interactive_clarification_loop_resolution(self):
        """Test that answering a clarification request resolves the state cleanly."""
        pipeline = LegalQueryPipeline()
        sid = "clarif_session"

        # Turn 1: Omission of state on rent control triggers clarification
        resp1 = pipeline.execute(
            query="Can a landlord evict a tenant for personal bona fide requirement under rent control law?",
            context_date="2024-01-01",
            session_id=sid
        )
        assert resp1.response_state == LegalResponseState.CLARIFICATION_REQUIRED
        sess = pipeline.dialogue_manager.get_or_create_session(sid)
        assert sess.pending_clarification_prompt is not None

        # Turn 2: User provides state jurisdiction answer
        resp2 = pipeline.execute(
            query="The property is in Delhi under the Delhi Rent Control Act.",
            session_id=sid
        )
        assert resp2.response_state in (LegalResponseState.ANSWER_SUPPORTED, LegalResponseState.ANSWER_QUALIFIED)
        assert resp2.parsed_query.jurisdiction == "IN-DL"
        # Clarification prompt resolved and cleared
        assert sess.pending_clarification_prompt is None

    def test_date_and_jurisdiction_persistence_across_turns(self):
        """Test that date and jurisdiction persist across turns without user re-specifying them."""
        pipeline = LegalQueryPipeline()
        sid = "persist_session"

        # Turn 1: Explicit date and jurisdiction
        resp1 = pipeline.execute(
            query="What is the statutory procedure for search of digital records?",
            context_date="2024-09-15",
            jurisdiction="IN",
            session_id=sid
        )
        assert resp1.parsed_query.query_date == "2024-09-15"

        # Turn 2: Follow-up without specifying date or jurisdiction
        resp2 = pipeline.execute(
            query="Who has the power to seize electronic devices?",
            session_id=sid
        )
        # Should inherit date 2024-09-15
        assert resp2.parsed_query.query_date == "2024-09-15"
        assert resp2.parsed_query.jurisdiction == "IN"

    def test_multi_turn_history_formatting_for_prompt(self):
        """Test formatting recent dialogue turns for prompt injection."""
        dm = LegalDialogueManager()
        dm.record_turn("s1", "What is Section 138 NI Act?", LegalResponseState.ANSWER_SUPPORTED, "Cheque bounce offence.", [])
        dm.record_turn("s1", "What is the notice period?", LegalResponseState.ANSWER_SUPPORTED, "15 days statutory demand notice.", [])

        prompt_hist = dm.format_conversation_history_for_prompt("s1")
        assert "User: What is Section 138 NI Act?" in prompt_hist
        assert "Assistant: Cheque bounce offence." in prompt_hist
        assert "User: What is the notice period?" in prompt_hist
        assert "Assistant: 15 days statutory demand notice." in prompt_hist

    def test_pipeline_with_dialogue_and_mock_model_adapter(self):
        """Test multi-turn execution with both dialogue manager and model adapter active."""
        mock_adapter = LocalLegalModelAdapter(ModelAdapterConfig(enable_mock_for_testing=True))
        pipeline = LegalQueryPipeline(model_adapter=mock_adapter)
        sid = "combined_session"

        resp1 = pipeline.execute(
            query="Can an interim injunction be granted in infrastructure contracts under Section 20A?",
            context_date="2024-06-01",
            jurisdiction="IN",
            session_id=sid
        )
        assert resp1.response_state is not None
        assert len(resp1.assembled_answer.claims) > 0

        resp2 = pipeline.execute(
            query="What are the exceptions to this bar?",
            session_id=sid
        )
        assert resp2.response_state is not None
        assert "Direct Position" in resp2.answer_text

