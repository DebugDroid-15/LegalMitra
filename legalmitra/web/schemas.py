"""
LegalMitra Web API Schemas
Typed contracts for legal chat requests, responses, and conversation management.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Client request to submit a legal question."""
    query: str = Field(..., min_length=3, max_length=2000, description="Legal question or query")
    conversation_id: Optional[str] = Field(default=None, description="Existing conversation session ID")
    act_filter: Optional[str] = Field(default=None, description="Optional Act title to restrict search")
    section_filter: Optional[str] = Field(default=None, description="Optional Section reference")
    court_filter: Optional[str] = Field(default=None, description="Optional Court jurisdiction")
    limit: int = Field(default=4, ge=1, le=10, description="Maximum number of evidence chunks to retrieve")


class SourceEvidenceItem(BaseModel):
    """Specific verified legal source citation."""
    chunk_id: str
    source_id: str
    act_or_case_title: str
    provision_or_para_ref: str
    authority_level: str
    verbatim_text: str
    source_url: str
    effective_date: Optional[str] = None
    is_synthetic_scaffold: bool = False


class ChatResponse(BaseModel):
    """Server response containing answer, citations, and constitutional telemetry."""
    conversation_id: str
    query: str
    answer: str
    citations: List[str] = Field(default_factory=list)
    evidence: List[SourceEvidenceItem] = Field(default_factory=list)
    evidence_sufficiency: str = Field(default="sufficient")
    binding_authorities: List[str] = Field(default_factory=list)
    persuasive_authorities: List[str] = Field(default_factory=list)
    missing_facts_prompt: Optional[str] = None
    legal_disclaimer: str
    model_used: str
    latency_seconds: float
    timestamp: str


class FeedbackRequest(BaseModel):
    """User evaluation feedback on answer accuracy or precision."""
    conversation_id: str
    query: str
    is_helpful: bool
    feedback_text: Optional[str] = None


class FeedbackResponse(BaseModel):
    """Acknowledgment of recorded feedback."""
    status: str
    message: str


class HealthStatus(BaseModel):
    """System health check and knowledge-base status."""
    status: str
    app_name: str
    version: str
    knowledge_base_chunks: int
    active_sources: int
    model_provider: str

