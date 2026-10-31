"""Multi-turn legal dialogue state and context management for LegalMitra.

Maintains factual context across conversation turns, tracks jurisdiction and date
continuity, and handles interactive clarification resolution when the legal policy
requires additional decisive facts.
"""

from __future__ import annotations

import copy
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from legalmitra.orchestration.decision_policy import LegalResponseState
from legalmitra.orchestration.query_understanding import ParsedLegalQuery

logger = logging.getLogger(__name__)


@dataclass
class DialogueTurn:
    """Represents a single query-response turn in a multi-turn conversation."""
    turn_index: int
    user_query: str
    response_state: LegalResponseState
    answer_text: str
    citations: List[str] = field(default_factory=list)
    governing_provisions: List[str] = field(default_factory=list)
    context_date: Optional[str] = None
    jurisdiction: Optional[str] = None
    clarification_requested: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class DialogueSession:
    """Stores the cumulative multi-turn state of an ongoing legal inquiry."""
    session_id: str
    turns: List[DialogueTurn] = field(default_factory=list)
    persisted_context_date: Optional[str] = None
    persisted_jurisdiction: Optional[str] = None
    accumulated_facts: Dict[str, Any] = field(default_factory=dict)
    pending_clarification_prompt: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def reset(self) -> None:
        """Clear conversation history and state."""
        self.turns.clear()
        self.persisted_context_date = None
        self.persisted_jurisdiction = None
        self.accumulated_facts.clear()
        self.pending_clarification_prompt = None


class LegalDialogueManager:
    """Orchestrates multi-turn dialogue memory, state propagation, and clarification loops."""

    def __init__(self, default_session_id: str = "default_session") -> None:
        self.sessions: Dict[str, DialogueSession] = {}
        self.default_session_id = default_session_id

    def get_or_create_session(self, session_id: Optional[str] = None) -> DialogueSession:
        """Retrieve existing session or instantiate a new dialogue session."""
        sid = session_id or self.default_session_id
        if sid not in self.sessions:
            self.sessions[sid] = DialogueSession(session_id=sid)
        return self.sessions[sid]

    def contextualize_query(
        self,
        query: str,
        session_id: Optional[str] = None,
        context_date: Optional[str] = None,
        jurisdiction: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Merge prior session context into the incoming query.
        Handles clarification resolution, date propagation, and jurisdiction continuity.
        """
        session = self.get_or_create_session(session_id)
        effective_date = context_date or session.persisted_context_date
        effective_jurisdiction = jurisdiction or session.persisted_jurisdiction

        # If there is a pending clarification, user query is likely the answer to it
        is_clarification_response = False
        clarification_context = ""
        if session.pending_clarification_prompt:
            is_clarification_response = True
            clarification_context = (
                f"Prior Query Clarification Needed: '{session.pending_clarification_prompt}'. "
                f"User Clarifying Response: '{query.strip()}'. "
            )

        # Context synthesis: If this is a follow-up query, append prior topic context
        enriched_query = query.strip()
        if session.turns and not is_clarification_response:
            last_turn = session.turns[-1]
            # Coreference hint if user asks brief follow-up ("what about...", "can I...", "under that law")
            short_followup_starters = ("what about", "can i", "is it", "does it", "under this", "in that case", "and what if")
            lower_q = query.strip().lower()
            if any(lower_q.startswith(starter) for starter in short_followup_starters) or len(query.split()) <= 6:
                enriched_query = f"{query.strip()} (Context from prior question: '{last_turn.user_query}')"

        return {
            "enriched_query": enriched_query,
            "effective_date": effective_date,
            "effective_jurisdiction": effective_jurisdiction,
            "is_clarification_response": is_clarification_response,
            "clarification_context": clarification_context,
            "session": session,
        }

    def record_turn(
        self,
        session_id: str,
        user_query: str,
        response_state: LegalResponseState,
        answer_text: str,
        citations: Optional[List[str]] = None,
        governing_provisions: Optional[List[str]] = None,
        context_date: Optional[str] = None,
        jurisdiction: Optional[str] = None,
        clarifying_question: Optional[str] = None
    ) -> DialogueTurn:
        """Record turn outcome and update session state."""
        session = self.get_or_create_session(session_id)
        turn_index = len(session.turns) + 1

        turn = DialogueTurn(
            turn_index=turn_index,
            user_query=user_query,
            response_state=response_state,
            answer_text=answer_text,
            citations=citations or [],
            governing_provisions=governing_provisions or [],
            context_date=context_date,
            jurisdiction=jurisdiction,
            clarification_requested=clarifying_question,
        )
        session.turns.append(turn)

        # Persist date and jurisdiction if provided
        if context_date:
            session.persisted_context_date = context_date
        if jurisdiction:
            session.persisted_jurisdiction = jurisdiction

        # Update pending clarification status
        if response_state == LegalResponseState.CLARIFICATION_REQUIRED and clarifying_question:
            session.pending_clarification_prompt = clarifying_question
        else:
            session.pending_clarification_prompt = None

        return turn

    def format_conversation_history_for_prompt(
        self,
        session_id: Optional[str] = None,
        max_turns: int = 3
    ) -> str:
        """Format recent dialogue turns for injection into the neural model prompt."""
        session = self.get_or_create_session(session_id)
        if not session.turns:
            return ""

        recent_turns = session.turns[-max_turns:]
        lines = []
        for t in recent_turns:
            # Compact summary of prior turn
            lines.append(f"User: {t.user_query}")
            short_ans = t.answer_text.split("\n\n")[0] if "\n\n" in t.answer_text else t.answer_text[:160]
            lines.append(f"Assistant: {short_ans.strip()}")

        return "\n".join(lines)
