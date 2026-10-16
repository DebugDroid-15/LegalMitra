"""
LegalMitra RAG Schemas
Defines request and response contracts for the source-grounded Indian Legal RAG engine.
"""

from datetime import date
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CitedEvidence(BaseModel):
    """Specific piece of evidence retrieved from the Knowledge Base."""
    chunk_id: str
    source_id: str
    act_or_case_title: str
    provision_or_para_ref: str
    authority_level: str
    verbatim_text: str
    source_url: str
    effective_date: Optional[str] = None
    is_synthetic_scaffold: bool = False


class RAGResponse(BaseModel):
    """
    Complete response produced by the LegalMitra RAG engine.
    Strictly source-grounded with provenance, authority ranking, and disclaimers.
    """
    query: str
    answer: str
    citations: List[str] = Field(default_factory=list)
    cited_evidence: List[CitedEvidence] = Field(default_factory=list)
    evidence_sufficiency: str = Field(
        default="sufficient",
        description="'sufficient', 'insufficient', 'contradictory', or 'potentially_outdated'"
    )
    is_grounded: bool = True
    binding_authorities: List[str] = Field(
        default_factory=list,
        description="Statutes in force or Supreme Court decisions under Article 141"
    )
    persuasive_authorities: List[str] = Field(
        default_factory=list,
        description="High Court precedents outside jurisdiction or tribunal rulings"
    )
    missing_facts_prompt: Optional[str] = Field(
        default=None,
        description="Prompt to user requesting missing jurisdiction or date when materially decisive"
    )
    legal_disclaimer: str = Field(
        default="This response is an automated synthesis of Indian legal sources and does not constitute formal legal advice or create an advocate-client relationship. Substantive rights and procedural timelines should be verified with an advocate enrolled under the Advocates Act, 1961."
    )
    model_used: str
    latency_seconds: float = 0.0

