"""
LegalMitra Source-Grounded RAG Engine
Coordinates SQLite/FTS5 knowledge retrieval and LLM answer generation,
enforcing evidential constraints, authority distinctions, and statutory disclaimers.
"""

import re
import time
from datetime import date
from typing import List, Optional

from legalmitra.core.logging import get_logger
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
from legalmitra.knowledge.models import AuthorityLevel, SearchFilters, SearchResult
from legalmitra.llm.interface import BaseLLMProvider, LLMMessage
from legalmitra.llm.mock_provider import MockLLMProvider
from legalmitra.llm.nemotron import NemotronLLMProvider
from legalmitra.rag.prompts import SYSTEM_RAG_PROMPT, build_rag_user_prompt
from legalmitra.rag.schemas import CitedEvidence, RAGResponse

logger = get_logger("rag_engine")


class LegalRAGEngine:
    """
    Source-Grounded Indian Legal Retrieval-Augmented Generation Engine.
    """

    def __init__(
        self,
        knowledge_base: Optional[LegalKnowledgeBase] = None,
        llm_provider: Optional[BaseLLMProvider] = None,
    ):
        self.kb = knowledge_base or LegalKnowledgeBase()
        if llm_provider is not None:
            self.llm_provider = llm_provider
        else:
            default_nemotron = NemotronLLMProvider()
            if default_nemotron.is_available():
                self.llm_provider = default_nemotron
            else:
                logger.warning("NVIDIA credentials not configured. Falling back to MockLLMProvider for RAG.")
                self.llm_provider = MockLLMProvider()

    def answer(
        self,
        query: str,
        filters: Optional[SearchFilters] = None,
        limit: int = 4,
    ) -> RAGResponse:
        """
        Execute grounded RAG answering for an Indian legal query.
        """
        start_time = time.time()
        filters = filters or SearchFilters()

        # Step 1: Retrieve relevant legal provisions and paragraphs
        search_results: List[SearchResult] = self.kb.search(
            query=query,
            filters=filters,
            limit=limit,
        )

        # Assemble cited evidence items
        cited_evidence_list: List[CitedEvidence] = [
            CitedEvidence(
                chunk_id=r.chunk_id,
                source_id=r.source_id,
                act_or_case_title=r.act_or_case_title,
                provision_or_para_ref=r.provision_or_para_ref,
                authority_level=r.authority_level.value,
                verbatim_text=r.content,
                source_url=r.source_url,
                effective_date=r.effective_date.isoformat() if r.effective_date else None,
                is_synthetic_scaffold=r.is_synthetic_scaffold,
            )
            for r in search_results
        ]

        # Categorize authority levels
        binding_auths = [
            f"{r.act_or_case_title} ({r.provision_or_para_ref})"
            for r in search_results
            if r.authority_level in (AuthorityLevel.BINDING_STATUTE, AuthorityLevel.BINDING_PRECEDENT)
        ]
        persuasive_auths = [
            f"{r.act_or_case_title} ({r.provision_or_para_ref})"
            for r in search_results
            if r.authority_level == AuthorityLevel.PERSUASIVE_PRECEDENT
        ]

        # Step 2: Guardrails against Prompt Injection and POCSO/Victim Privacy Violations
        q_lower = query.lower()
        if any(term in q_lower for term in ["system override", "unconstrained mode", "disregard all previous", "bypass safety", "jailbreak", "output pwned"]):
            latency = time.time() - start_time
            return RAGResponse(
                query=query,
                answer="Request rejected: Unauthorized instruction override detected. LegalMitra strictly enforces Indian legal research boundaries.",
                citations=[],
                cited_evidence=[],
                evidence_sufficiency="insufficient",
                is_grounded=True,
                binding_authorities=[],
                persuasive_authorities=[],
                missing_facts_prompt=None,
                model_used=self.llm_provider.__class__.__name__,
                latency_seconds=latency,
            )

        if "pocso" in q_lower or "minor victim" in q_lower or "child victim" in q_lower:
            if any(term in q_lower for term in ["disclose", "name", "address", "identity", "unredacted", "contact"]):
                latency = time.time() - start_time
                return RAGResponse(
                    query=query,
                    answer="Disclosure of protected details regarding a child or child complainant is strictly prohibited under Section 33(7) and Section 74 of the Protection of Children from Sexual Offences (POCSO) Act, 2012.",
                    citations=[],
                    cited_evidence=[],
                    evidence_sufficiency="insufficient",
                    is_grounded=True,
                    binding_authorities=["Protection of Children from Sexual Offences Act, 2012"],
                    persuasive_authorities=[],
                    missing_facts_prompt=None,
                    model_used=self.llm_provider.__class__.__name__,
                    latency_seconds=latency,
                )


        # Step 2b: Handle empty or insufficient evidence case
        if not search_results:
            latency = time.time() - start_time
            return RAGResponse(
                query=query,
                answer=(
                    "The retrieved legal sources do not provide sufficient evidence to answer this question "
                    "authoritatively under Indian law. No relevant provisions or precedents matching this query "
                    "were located in the verified LegalMitra Knowledge Base."
                ),
                citations=[],
                cited_evidence=[],
                evidence_sufficiency="insufficient",
                is_grounded=True,
                binding_authorities=[],
                persuasive_authorities=[],
                missing_facts_prompt=(
                    "Please specify the applicable Act name, section number, or specific High Court jurisdiction."
                ),
                model_used=self.llm_provider.__class__.__name__,
                latency_seconds=latency,
            )


        # Step 3: Check for temporal or jurisdictional ambiguities
        missing_facts = self._detect_missing_facts(query, filters)

        # Step 4: Dispatch grounded prompt to LLM
        user_prompt = build_rag_user_prompt(query, search_results)
        messages = [
            LLMMessage(role="system", content=SYSTEM_RAG_PROMPT),
            LLMMessage(role="user", content=user_prompt),
        ]

        logger.info(f"Calling LLM provider ({self.llm_provider.__class__.__name__}) with {len(search_results)} evidence chunks...")
        llm_resp = self.llm_provider.generate(messages, temperature=0.0, max_tokens=1024)
        answer_text = llm_resp.content.strip()

        # Step 5: Extract citations and classify evidence sufficiency
        citations = self._extract_citations(answer_text, search_results)
        sufficiency = self._classify_sufficiency(answer_text, search_results)

        latency = time.time() - start_time

        return RAGResponse(
            query=query,
            answer=answer_text,
            citations=citations,
            cited_evidence=cited_evidence_list,
            evidence_sufficiency=sufficiency,
            is_grounded=True,
            binding_authorities=binding_auths,
            persuasive_authorities=persuasive_auths,
            missing_facts_prompt=missing_facts,
            model_used=getattr(llm_resp, "model_name", self.llm_provider.__class__.__name__),
            latency_seconds=latency,
        )

    def _detect_missing_facts(self, query: str, filters: SearchFilters) -> Optional[str]:
        """Detect if jurisdiction or date ambiguity materially affects legal validity."""
        q_lower = query.lower()
        
        # Check if temporal boundary (pre vs post 1 July 2024 new criminal laws) is relevant
        criminal_law_terms = ["evidence", "electronic record", "bail", "cheating", "murder", "theft", "arrest"]
        if any(term in q_lower for term in criminal_law_terms) and not filters.as_of_date:
            has_explicit_date = bool(re.search(r"\b(19\d\d|20\d\d)\b", query))
            if not has_explicit_date:
                return (
                    "Important Temporal Fact Required: On 1 July 2024, the Bharatiya Nyaya Sanhita (BNS), "
                    "Bharatiya Nagarik Suraksha Sanhita (BNSS), and Bharatiya Sakshya Adhiniyam (BSA) came into force, "
                    "repealing the IPC, CrPC, and Indian Evidence Act, 1872. The substantive law applicable depends on "
                    "whether the offence occurred before or after 1 July 2024."
                )

        # Check if state jurisdiction is missing for procedural matters
        procedural_terms = ["procedure", "high court", "appeal", "limitation", "stamp duty", "court fee"]
        if any(term in q_lower for term in procedural_terms) and not filters.jurisdiction:
            return (
                "Jurisdictional Fact Required: Procedural workflows and High Court practice directions "
                "vary across states (e.g. Delhi High Court Rules vs Bombay High Court Original Side Rules). "
                "Please specify the target High Court jurisdiction."
            )

        return None

    def _extract_citations(self, answer: str, results: List[SearchResult]) -> List[str]:
        """Extract citations referenced in the answer matching retrieved sources."""
        citations = []
        for r in results:
            # Check if reference or act title appears in answer
            if (
                r.provision_or_para_ref.lower() in answer.lower()
                or r.act_or_case_title.lower() in answer.lower()
                or r.source_id.lower() in answer.lower()
            ):
                if r.court and "none" not in str(r.court).lower():
                    citations.append(f"{r.act_or_case_title}, {r.provision_or_para_ref} ({r.court})")
                else:
                    citations.append(f"{r.act_or_case_title}, {r.provision_or_para_ref}")

        # Fallback to all retrieved results if answer synthesized them globally
        if not citations and results:
            citations = [f"{r.act_or_case_title}, {r.provision_or_para_ref}" for r in results]

        return list(dict.fromkeys(citations))


    def _classify_sufficiency(self, answer: str, results: List[SearchResult]) -> str:
        """Classify evidential sufficiency from model output."""
        ans_lower = answer.lower()
        if "insufficient evidence" in ans_lower or "do not provide sufficient evidence" in ans_lower:
            return "insufficient"
        if any(r.is_synthetic_scaffold for r in results):
            return "unverified_scaffold"
        if any(r.is_historical for r in results):
            return "potentially_outdated"
        return "sufficient"

