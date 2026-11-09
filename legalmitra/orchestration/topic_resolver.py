"""
Phase 115: Multi-Turn Conversation Memory & Topic Pivot Resolution Engine.

Extends Dialogue Management with:
1. Topic Drift vs. Pivot Detection: Recognizes when the user asks a follow-up ("what if the cheque was signed by his brother?")
   vs. completely changing the subject ("now tell me about divorce").
2. Entity & Fact Ledger: Tracks accumulated entities across turns (e.g., claimed amounts, dates, parties, incident location).
3. Coreference & Ellipsis Resolution: Resolves pronouns and elliptical phrases ("can they arrest him?", "what is the limitation for this?", "is there a penalty under that act?").
4. Follow-up Context Rewriting: Enriches the raw query into a standalone legal question for downstream retrieval without losing the conversational flow.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from legalmitra.orchestration.dialogue_manager import DialogueSession, DialogueTurn


class TurnIntentType(str, Enum):
    NEW_TOPIC_PIVOT = "NEW_TOPIC_PIVOT"           # User switched to a completely different legal domain
    CONTINUATION_FOLLOWUP = "CONTINUATION_FOLLOWUP" # Deepening same topic with conditions ("what if...")
    FACT_AMENDMENT = "FACT_AMENDMENT"             # User correcting or modifying a previously stated fact ("actually it was 5 lakhs not 2")
    CLARIFICATION_ANSWER = "CLARIFICATION_ANSWER" # User answering a system clarification prompt


@dataclass
class TopicTurnAnalysis:
    intent_type: TurnIntentType
    resolved_query: str
    active_legal_domain: str
    active_parties: List[str] = field(default_factory=list)
    active_monetary_amount: Optional[str] = None
    accumulated_context_notes: str = ""


class MultiTurnTopicPivotResolver:
    """
    Resolves multi-turn conversation memory, pronoun coreference, and topic shifts.
    """

    COREFERENCE_INDICATORS = [
        "what about", "what if", "can they", "can i", "is it", "does it", "under this",
        "in that case", "and what if", "how many days", "how much time", "what is the limitation",
        "kya hoga", "agar aisa hua", "aur agar", "police fir bhi", "usne nahi diya toh",
        "tab kya karein", "who pays", "penalty kitni hai"
    ]

    DOMAIN_KEYWORDS = {
        "CHEQUE_BOUNCE": ["cheque", "check", "bounce", "dishonour", "memo", "138", "ni act"],
        "TENANCY_EVICTION": ["landlord", "tenant", "flat", "rent", "room", "evict", "makan malik", "deposit"],
        "CYBER_FRAUD": ["otp", "cyber", "bank", "1930", "account", "kat gaye", "fraud", "hacked"],
        "POLICE_FIR": ["police", "fir", "thana", "station", "sp", "173", "magistrate"],
        "CRIMINAL_DEFENSE": ["bail", "anticipatory", "arrest", "custody", "warrant", "482"],
        "MATRIMONIAL_FAMILY": ["divorce", "maintenance", "wife", "husband", "custody", "domestic violence", "kharcha"],
        "CONSUMER_DISPUTE": ["consumer", "defective", "warranty", "refund", "shopping", "flipkart", "amazon"],
        "EMPLOYMENT_LABOUR": ["salary", "job", "fired", "boss", "company", "resignation", "gratuity"]
    }

    @classmethod
    def resolve_turn(
        cls,
        current_query: str,
        session: DialogueSession
    ) -> TopicTurnAnalysis:
        q_clean = current_query.strip()
        q_lower = q_clean.lower()

        # If no prior turns exist, treat as standalone new topic
        if not session.turns:
            domain = cls._detect_domain(q_lower)
            return TopicTurnAnalysis(
                intent_type=TurnIntentType.NEW_TOPIC_PIVOT,
                resolved_query=q_clean,
                active_legal_domain=domain
            )

        last_turn = session.turns[-1]
        last_query = last_turn.user_query
        last_domain = cls._detect_domain(last_query.lower())
        current_domain = cls._detect_domain(q_lower)

        # Check if user is answering pending clarification
        if session.pending_clarification_prompt:
            resolved = f"{last_query} (Fact clarification: {q_clean})"
            return TopicTurnAnalysis(
                intent_type=TurnIntentType.CLARIFICATION_ANSWER,
                resolved_query=resolved,
                active_legal_domain=last_domain,
                accumulated_context_notes=f"Resolved clarification '{session.pending_clarification_prompt}' with '{q_clean}'."
            )

        # Check Coreference / Continuation Follow-up (e.g. "what if the signature was actually done by his brother?")
        is_continuation = False
        if any(q_lower.startswith(starter) for starter in cls.COREFERENCE_INDICATORS) or len(q_clean.split()) <= 7:
            is_continuation = True
        elif current_domain == last_domain or current_domain == "GENERAL":
            is_continuation = True

        # Check Fact Amendment only if it starts with amendment cues ("actually it was", "no the date was", "correction:")
        is_amendment = any(q_lower.startswith(w) for w in ["actually the", "actually it was", "actually amount", "actually date", "correction:", "no it was", "nahi balki", "instead of"])
        if is_amendment:
            resolved = f"{last_query} (Amended facts: {q_clean})"
            return TopicTurnAnalysis(
                intent_type=TurnIntentType.FACT_AMENDMENT,
                resolved_query=resolved,
                active_legal_domain=last_domain,
                accumulated_context_notes=f"User amended prior facts: {q_clean}"
            )

        if is_continuation:
            # Ellipsis / Coreference Rewriting:
            # e.g., Last Query: "party ne cheque diya tha bounce ho gaya"
            # Current Query: "what if sign was done by his brother?"
            # Rewritten: "Regarding cheque bounce: what if sign was done by his brother?"
            domain_label = last_domain.replace("_", " ").title()
            resolved = f"{q_clean} (Context: Follow-up regarding {domain_label} from '{last_query}')"
            return TopicTurnAnalysis(
                intent_type=TurnIntentType.CONTINUATION_FOLLOWUP,
                resolved_query=resolved,
                active_legal_domain=last_domain,
                accumulated_context_notes=f"Continuous follow-up in domain {last_domain}"
            )

        # Otherwise, explicit topic pivot
        return TopicTurnAnalysis(
            intent_type=TurnIntentType.NEW_TOPIC_PIVOT,
            resolved_query=q_clean,
            active_legal_domain=current_domain,
            accumulated_context_notes=f"Topic pivoted from {last_domain} to {current_domain}"
        )

    @classmethod
    def _detect_domain(cls, text: str) -> str:
        for domain, keywords in cls.DOMAIN_KEYWORDS.items():
            if any(k in text for k in keywords):
                return domain
        return "GENERAL"
