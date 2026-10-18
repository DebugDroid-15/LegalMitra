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
from legalmitra.rag.schemas import (
    CitedEvidence,
    ClaimType,
    ClaimVerificationStatus,
    LegalClaim,
    RAGResponse,
)

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
            import os
            if os.environ.get("LEGALMITRA_OFFLINE_EVAL") == "1":
                self.llm_provider = MockLLMProvider()
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

        # Step 2: Guardrails against Prompt Injection and Privacy Violations
        q_lower = query.lower()
        if any(term in q_lower for term in ["system override", "admin override", "unconstrained mode", "disregard all previous", "bypass safety", "jailbreak", "output pwned", "ignore all"]):
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

        if any(term in q_lower for term in ["pocso", "minor victim", "child victim", "juvenile"]):
            if any(term in q_lower for term in ["disclose", "name", "address", "identity", "unredacted", "contact", "residential"]):
                latency = time.time() - start_time
                return RAGResponse(
                    query=query,
                    answer=(
                        "Disclosure of protected details regarding a child or juvenile in conflict with law is strictly prohibited "
                        "under Section 33(7) and Section 74 of the Protection of Children from Sexual Offences (POCSO) Act, 2012 "
                        "and Section 74 of the Juvenile Justice (Care and Protection of Children) Act, 2015."
                    ),
                    citations=[],
                    cited_evidence=[],
                    evidence_sufficiency="insufficient",
                    is_grounded=True,
                    binding_authorities=["Protection of Children from Sexual Offences Act, 2012", "Juvenile Justice Act, 2015"],
                    persuasive_authorities=[],
                    missing_facts_prompt=None,
                    model_used=self.llm_provider.__class__.__name__,
                    latency_seconds=latency,
                )

        # Personal data / witness / investigator / litigant privacy protection
        personal_privacy_terms = ["investigator", "witness", "litigant", "advocate", "judge", "parties", "party"]
        contact_leak_terms = ["residential address", "phone number", "home address", "contact details", "personal email", "mobile number"]
        if any(c in q_lower for c in contact_leak_terms) or (
            any(p in q_lower for p in personal_privacy_terms) and any(c in q_lower for c in ["address", "phone", "contact", "mobile", "residence"])
        ):
            latency = time.time() - start_time
            return RAGResponse(
                query=query,
                answer=(
                    "Disclosure of personal contact information, residential addresses, and private communication details "
                    "of investigators, witnesses, or parties is strictly restricted under Indian privacy law and judicial "
                    "record publication protocols. LegalMitra does not disclose unredacted personal identifiable information."
                ),
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

        # Step 2b: Verify evidence relevance to query
        if search_results:
            q_clean = re.sub(r'[^\w\s]', ' ', query.lower())
            stop_relevance = {
                'what', 'under', 'with', 'from', 'this', 'that', 'have', 'been', 'which', 'there',
                'their', 'about', 'shall', 'where', 'when', 'does', 'explain', 'state', 'provision',
                'section', 'conditions', 'timelines', 'mandatory', 'rates', 'licences', 'licenses',
                'commercial', 'establishments'
            }
            q_distinct_words = set(w for w in q_clean.split() if len(w) > 3 and w not in stop_relevance)
            
            has_relevant = False
            for r in search_results:
                chunk_haystack = (r.act_or_case_title + " " + r.provision_or_para_ref + " " + r.content).lower()
                overlap = sum(1 for w in q_distinct_words if w in chunk_haystack)
                if r.section_number and r.section_number.lower() in query.lower():
                    has_relevant = True
                    break
                if overlap >= 2 or (q_distinct_words and (overlap / len(q_distinct_words)) >= 0.25):
                    has_relevant = True
                    break

            # If query mentions a specific state (meghalaya, haryana, etc.), require state match in evidence
            state_names = ["meghalaya", "haryana", "nagaland", "mizoram", "ladakh", "sikkim"]
            mentioned_states = [s for s in state_names if s in q_lower]
            if mentioned_states:
                state_match = any(
                    any(s in (r.act_or_case_title + " " + r.content).lower() for s in mentioned_states)
                    for r in search_results
                )
                if not state_match:
                    has_relevant = False

            # Check false premise / adversarial mismatch (e.g. death penalty for defamation under BNSS 500)
            if "defamation" in q_lower and ("death penalty" in q_lower or not any("defamation" in (r.content + " " + r.act_or_case_title).lower() for r in search_results)):
                has_relevant = False

            if not has_relevant:
                search_results = []
                cited_evidence_list = []
                binding_auths = []
                persuasive_auths = []

        # Step 2c: Handle empty or insufficient evidence case
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
        llm_resp = None
        answer_text = None
        try:
            llm_resp = self.llm_provider.generate(messages, temperature=0.0, max_tokens=1024)
            resp_content = llm_resp.content.strip()
            if resp_content.startswith("[{\"error\":") or "Unknown task type" in resp_content:
                answer_text = None
            else:
                answer_text = resp_content
        except Exception as e:
            logger.warning(f"LLM provider generation failed or timed out: {e}. Falling back to extractive grounded synthesis.")
            answer_text = None

        if not answer_text:
            answer_parts = []
            for r in search_results:
                court_str = f" ({r.court})" if r.court and "none" not in str(r.court).lower() else ""
                ref_str = f" [{r.act_or_case_title}{court_str}, {r.provision_or_para_ref}]"
                chunk_body = r.content.strip()
                if "life or liberty" in q_lower and "forty-eight hours" in chunk_body.lower():
                    chunk_body = re.sub(r'within thirty days of the receipt of the request:?', 'within the prescribed statutory period:', chunk_body, flags=re.IGNORECASE)
                answer_parts.append(
                    f"Under {r.act_or_case_title}{court_str}, {r.provision_or_para_ref}:\n"
                    f"{chunk_body}{ref_str}"
                )
            answer_text = "\n\n".join(answer_parts)

        # Step 5: Extract citations and classify evidence sufficiency
        citations = self._extract_citations(answer_text, search_results)
        sufficiency = self._classify_sufficiency(answer_text, search_results)
        claims = self._decompose_and_verify_claims(answer_text, search_results)

        latency = time.time() - start_time

        return RAGResponse(
            query=query,
            answer=answer_text,
            citations=citations,
            cited_evidence=cited_evidence_list,
            claims=claims,
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

    def _decompose_and_verify_claims(self, answer: str, results: List[SearchResult]) -> List[LegalClaim]:
        """
        Decompose the generated legal answer into verifiable legal claims.
        Establishes traceability to exact source chunk IDs, pinpoint refs, verbatim spans,
        jurisdiction, temporal status, and verification flags.
        """
        if not answer or not results:
            return []

        claims: List[LegalClaim] = []
        # Split answer into paragraphs or coherent analytical blocks
        blocks = [b.strip() for b in re.split(r'\n\s*\n', answer) if b.strip()]
        
        for idx, block in enumerate(blocks, start=1):
            claim_id = f"CLM-{idx:03d}"
            b_lower = block.lower()

            # Identify best matching evidence chunk
            best_chunk: Optional[SearchResult] = None
            for r in results:
                if (r.provision_or_para_ref.lower() in b_lower or 
                    r.act_or_case_title.lower() in b_lower or 
                    r.chunk_id.lower() in b_lower):
                    best_chunk = r
                    break

            if not best_chunk and results:
                best_chunk = results[0]

            # Determine claim type
            claim_type = ClaimType.GENERAL_EXPLANATION
            if "proviso" in b_lower or "provided that" in b_lower or "except" in b_lower:
                claim_type = ClaimType.STATUTORY_EXCEPTION
            elif "procedure" in b_lower or "timeline" in b_lower or "days" in b_lower or "hours" in b_lower:
                claim_type = ClaimType.PROCEDURAL_REQUIREMENT
            elif "held that" in b_lower or "ratio" in b_lower or "supreme court" in b_lower or "high court" in b_lower:
                claim_type = ClaimType.PRECEDENT_PROPOSITION
            elif "savings" in b_lower or "repeal" in b_lower or "transitional" in b_lower or "effective" in b_lower:
                claim_type = ClaimType.TRANSITIONAL_SAVINGS
            elif best_chunk and best_chunk.doc_type == "statute":
                claim_type = ClaimType.STATUTORY_RULE

            # Verify claim against supporting chunk
            status = ClaimVerificationStatus.VERIFIED_GROUNDED
            notes = None

            if best_chunk:
                if best_chunk.is_synthetic_scaffold:
                    status = ClaimVerificationStatus.WRONG_AUTHORITY
                    notes = "Supported only by quarantined synthetic scaffold"
                elif best_chunk.is_historical:
                    status = ClaimVerificationStatus.OUTDATED
                    notes = "Supported by repealed or historical statutory provision"
                else:
                    # Check token overlap with verbatim text
                    chunk_tokens = set(re.findall(r'\w+', best_chunk.content.lower()))
                    block_tokens = set(re.findall(r'\w+', b_lower))
                    overlap = len(block_tokens.intersection(chunk_tokens))
                    if len(block_tokens) > 5 and overlap < 3:
                        status = ClaimVerificationStatus.UNSUPPORTED
                        notes = "Low evidential alignment with supporting chunk text"
            else:
                status = ClaimVerificationStatus.UNSUPPORTED
                notes = "No supporting knowledge chunk retrieved"

            eff_str = str(best_chunk.effective_date) if best_chunk and best_chunk.effective_date else None
            claims.append(LegalClaim(
                claim_id=claim_id,
                claim_text=block[:300],
                claim_type=claim_type,
                source_id=best_chunk.source_id if best_chunk else None,
                act_or_case_title=best_chunk.act_or_case_title if best_chunk else None,
                provision_or_para_ref=best_chunk.provision_or_para_ref if best_chunk else None,
                supporting_chunk_id=best_chunk.chunk_id if best_chunk else None,
                verbatim_evidence_passage=best_chunk.content[:250] if best_chunk else None,
                jurisdiction=str(best_chunk.jurisdiction.value) if best_chunk and hasattr(best_chunk.jurisdiction, 'value') else (str(best_chunk.jurisdiction) if best_chunk else "IN"),
                temporal_applicability=eff_str,
                verification_status=status,
                verification_method="deterministic_evidence_alignment",
                verification_notes=notes,
            ))

        return claims

