"""Production-Grade REST API Server for LegalMitra (Phase 70).

Provides high-performance, asynchronous REST endpoints for:
1. Single-query 15-stage pipeline evaluation (`POST /api/v1/query`)
2. Multi-turn conversational legal chat (`POST /api/v1/chat`)
3. Statutory legal notice drafting (`POST /api/v1/draft`)
4. System health, FTS index parity & LoRA adapter status (`GET /api/v1/health`)
"""

from __future__ import annotations

import logging
import os
import time
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from legalmitra.drafting import (
    NoticeParty,
    NoticeType,
    StatutoryNoticeDraftingEngine,
    StatutoryNoticeExportEngine,
)
from legalmitra.models.local_adapter import (
    LocalLegalModelAdapter,
    ModelAdapterConfig,
    ModelExecutionMode,
)
from legalmitra.orchestration.decision_policy import LegalResponseState
from legalmitra.orchestration.pipeline import LegalQueryPipeline

logger = logging.getLogger(__name__)

app = FastAPI(
    title="LegalMitra Intelligence API",
    description="Deterministic 15-Stage Indian Legal Retrieval, Temporal Resolution & Neural IRAC Synthesis API.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared Pipeline Singletons
_default_pipeline: Optional[LegalQueryPipeline] = None
_mock_pipeline: Optional[LegalQueryPipeline] = None


def get_pipeline(model_mode: str = "deterministic") -> LegalQueryPipeline:
    """Retrieve or initialize pipeline instance according to requested model mode."""
    global _default_pipeline, _mock_pipeline

    if model_mode == "mock":
        if _mock_pipeline is None:
            mock_adapter = LocalLegalModelAdapter(ModelAdapterConfig(enable_mock_for_testing=True))
            _mock_pipeline = LegalQueryPipeline(model_adapter=mock_adapter)
        return _mock_pipeline
    elif model_mode == "neural":
        adapter = LocalLegalModelAdapter()
        return LegalQueryPipeline(model_adapter=adapter)
    else:
        if _default_pipeline is None:
            _default_pipeline = LegalQueryPipeline()
        return _default_pipeline


# --- Pydantic Data Models ---

class QueryRequest(BaseModel):
    query: str = Field(..., description="The substantive legal question to evaluate.")
    context_date: Optional[str] = Field(None, description="Point-in-time date (YYYY-MM-DD).")
    jurisdiction: Optional[str] = Field(None, description="Territorial jurisdiction code (e.g. IN, IN-DL, IN-MH).")
    model_mode: str = Field("deterministic", description="Synthesis mode: deterministic, neural, or mock.")
    language: Optional[str] = Field(None, description="Language mode: en, hi, or hinglish (defaults to auto-detect).")


class ClaimResponseItem(BaseModel):
    claim_id: str
    claim_text: str
    validation_verdict: str
    is_supported: bool
    authority_status: str
    statutory_version: Optional[str] = None
    validation_rationale: str


class QueryResponse(BaseModel):
    query: str
    detected_language: str
    response_state: str
    policy_rationale: str
    requires_clarification: bool
    clarifying_question: Optional[str] = None
    answer_text: str
    citations: List[str]
    governing_provisions: List[str]
    competing_authorities: List[str]
    claims: List[ClaimResponseItem]
    duration_ms: float
    timestamp: str


class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Unique dialogue session identifier.")
    message: str = Field(..., description="User message or follow-up question.")
    context_date: Optional[str] = Field(None, description="Optional override date.")
    jurisdiction: Optional[str] = Field(None, description="Optional override jurisdiction.")
    model_mode: str = Field("deterministic", description="deterministic, neural, or mock.")
    language: Optional[str] = Field(None, description="Language mode: en, hi, or hinglish (defaults to auto-detect).")


class ChatResponse(BaseModel):
    session_id: str
    turn_index: int
    user_message: str
    detected_language: str
    response_state: str
    answer_text: str
    clarification_requested: Optional[str] = None
    citations: List[str]
    persisted_date: Optional[str] = None
    persisted_jurisdiction: Optional[str] = None
    duration_ms: float


class NoticePartyModel(BaseModel):
    name: str
    address: str = "Address not specified"
    advocate_name: Optional[str] = None
    advocate_enrollment: Optional[str] = None


class NoticeDraftRequest(BaseModel):
    notice_type: str = Field(..., description="ni138, arb21, tpa106, ibc8, or general.")
    sender: NoticePartyModel
    recipient: NoticePartyModel
    facts: Dict[str, Any] = Field(default_factory=dict)
    as_of_date: Optional[str] = None


class NoticeDraftResponse(BaseModel):
    notice_type: str
    title: str
    statutory_governing_section: str
    mandatory_cure_period_days: int
    full_notice_markdown: str
    statutory_citations: List[str]
    created_at: str


class HealthResponse(BaseModel):
    status: str
    version: str
    fts_index_healthy: bool
    lora_adapter_available: bool
    active_sessions_count: int


# --- API Routes ---

@app.get("/api/v1/health", response_model=HealthResponse, tags=["System Health"])
def check_health():
    """Verify system health, FTS index parity, and LoRA adapter availability."""
    pipeline = get_pipeline("deterministic")
    adapter = LocalLegalModelAdapter()
    
    # Audit KB FTS health
    fts_healthy = True
    try:
        audit = pipeline.kb.audit_search_index()
        fts_healthy = audit.get("is_synchronized", True)
    except Exception:
        fts_healthy = False

    return HealthResponse(
        status="healthy",
        version="1.0.0",
        fts_index_healthy=fts_healthy,
        lora_adapter_available=adapter.is_available,
        active_sessions_count=len(pipeline.dialogue_manager.sessions),
    )


@app.post("/api/v1/query", response_model=QueryResponse, tags=["Legal Evaluation"])
def evaluate_legal_query(req: QueryRequest):
    """Execute complete 15-stage legal pipeline for a standalone legal inquiry."""
    pipeline = get_pipeline(req.model_mode)
    t0 = time.time()

    resp = pipeline.execute(
        query=req.query,
        context_date=req.context_date,
        jurisdiction=req.jurisdiction,
    )
    duration_ms = round((time.time() - t0) * 1000.0, 2)

    claims_out = []
    if resp.assembled_answer and resp.assembled_answer.claims:
        for c in resp.assembled_answer.claims:
            claims_out.append(ClaimResponseItem(
                claim_id=c.claim_id,
                claim_text=c.claim_text,
                validation_verdict=c.validation_verdict,
                is_supported=c.is_supported,
                authority_status=c.authority_status,
                statutory_version=c.statutory_version,
                validation_rationale=c.validation_rationale,
            ))

    lang = getattr(resp.parsed_query, "detected_language", "en") if resp.parsed_query else "en"
    return QueryResponse(
        query=resp.query,
        detected_language=lang,
        response_state=resp.response_state.value,
        policy_rationale=resp.policy_result.policy_rationale,
        requires_clarification=resp.policy_result.requires_clarifying_question,
        clarifying_question=resp.policy_result.clarifying_question,
        answer_text=resp.answer_text,
        citations=resp.citations,
        governing_provisions=resp.governing_provisions,
        competing_authorities=resp.competing_authorities,
        claims=claims_out,
        duration_ms=duration_ms,
        timestamp=resp.timestamp,
    )


@app.post("/api/v1/chat", response_model=ChatResponse, tags=["Conversational Chat"])
def execute_chat_turn(req: ChatRequest):
    """Execute multi-turn legal consultation with session memory and clarification resolving."""
    pipeline = get_pipeline(req.model_mode)
    t0 = time.time()

    resp = pipeline.execute(
        query=req.message,
        context_date=req.context_date,
        jurisdiction=req.jurisdiction,
        session_id=req.session_id,
    )
    duration_ms = round((time.time() - t0) * 1000.0, 2)

    sess = pipeline.dialogue_manager.get_or_create_session(req.session_id)
    turn_idx = len(sess.turns)

    lang = getattr(resp.parsed_query, "detected_language", "en") if resp.parsed_query else "en"
    return ChatResponse(
        session_id=req.session_id,
        turn_index=turn_idx,
        user_message=req.message,
        detected_language=lang,
        response_state=resp.response_state.value,
        answer_text=resp.answer_text,
        clarification_requested=resp.policy_result.clarifying_question,
        citations=resp.citations,
        persisted_date=sess.persisted_context_date,
        persisted_jurisdiction=sess.persisted_jurisdiction,
        duration_ms=duration_ms,
    )


@app.post("/api/v1/draft", response_model=NoticeDraftResponse, tags=["Document Drafting"])
def draft_statutory_notice(req: NoticeDraftRequest):
    """Generate legally compliant demand notice under Indian statutory mandates."""
    mapping = {
        "ni138": NoticeType.CHEQUE_BOUNCE_NI_ACT_138,
        "138": NoticeType.CHEQUE_BOUNCE_NI_ACT_138,
        "cheque": NoticeType.CHEQUE_BOUNCE_NI_ACT_138,
        "arb21": NoticeType.ARBITRATION_INVOCATION_SEC_21,
        "arbitration": NoticeType.ARBITRATION_INVOCATION_SEC_21,
        "tpa106": NoticeType.TENANCY_TERMINATION_TPA_106,
        "tenancy": NoticeType.TENANCY_TERMINATION_TPA_106,
        "ibc8": NoticeType.IBC_OPERATIONAL_CREDITOR_SEC_8,
        "ibc": NoticeType.IBC_OPERATIONAL_CREDITOR_SEC_8,
        "general": NoticeType.GENERAL_LEGAL_DEMAND,
    }

    ntype = mapping.get(req.notice_type.lower(), NoticeType.CHEQUE_BOUNCE_NI_ACT_138)
    s_party = NoticeParty(
        name=req.sender.name,
        address=req.sender.address,
        advocate_name=req.sender.advocate_name,
        advocate_enrollment=req.sender.advocate_enrollment,
    )
    r_party = NoticeParty(name=req.recipient.name, address=req.recipient.address)

    draft = StatutoryNoticeDraftingEngine.draft_notice(
        notice_type=ntype,
        sender=s_party,
        recipient=r_party,
        facts=req.facts,
        as_of_date=req.as_of_date,
    )

    return NoticeDraftResponse(
        notice_type=draft.notice_type.value,
        title=draft.title,
        statutory_governing_section=draft.statutory_governing_section,
        mandatory_cure_period_days=draft.mandatory_cure_period_days,
        full_notice_markdown=draft.full_notice_markdown,
        statutory_citations=draft.statutory_citations,
        created_at=draft.created_at,
    )



@app.post("/api/v1/draft/export/pdf", tags=["Document Drafting"])
def export_notice_as_pdf(req: NoticeDraftRequest):
    """Generates and streams a court-ready PDF notice."""
    mapping = {
        "ni138": NoticeType.CHEQUE_BOUNCE_NI_ACT_138,
        "138": NoticeType.CHEQUE_BOUNCE_NI_ACT_138,
        "cheque": NoticeType.CHEQUE_BOUNCE_NI_ACT_138,
        "arb21": NoticeType.ARBITRATION_INVOCATION_SEC_21,
        "arbitration": NoticeType.ARBITRATION_INVOCATION_SEC_21,
        "tpa106": NoticeType.TENANCY_TERMINATION_TPA_106,
        "tenancy": NoticeType.TENANCY_TERMINATION_TPA_106,
        "ibc8": NoticeType.IBC_OPERATIONAL_CREDITOR_SEC_8,
        "ibc": NoticeType.IBC_OPERATIONAL_CREDITOR_SEC_8,
        "general": NoticeType.GENERAL_LEGAL_DEMAND,
    }
    ntype = mapping.get(req.notice_type.lower(), NoticeType.CHEQUE_BOUNCE_NI_ACT_138)
    s_party = NoticeParty(
        name=req.sender.name,
        address=req.sender.address,
        advocate_name=req.sender.advocate_name,
        advocate_enrollment=req.sender.advocate_enrollment,
    )
    r_party = NoticeParty(name=req.recipient.name, address=req.recipient.address)

    draft = StatutoryNoticeDraftingEngine.draft_notice(
        notice_type=ntype,
        sender=s_party,
        recipient=r_party,
        facts=req.facts,
        as_of_date=req.as_of_date,
    )

    pdf_bytes = StatutoryNoticeExportEngine.export_to_pdf(draft)
    filename = f"legal_notice_{draft.notice_type.value}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.post("/api/v1/draft/export/docx", tags=["Document Drafting"])
def export_notice_as_docx(req: NoticeDraftRequest):
    """Generates and streams an editable court-ready DOCX notice."""
    mapping = {
        "ni138": NoticeType.CHEQUE_BOUNCE_NI_ACT_138,
        "138": NoticeType.CHEQUE_BOUNCE_NI_ACT_138,
        "cheque": NoticeType.CHEQUE_BOUNCE_NI_ACT_138,
        "arb21": NoticeType.ARBITRATION_INVOCATION_SEC_21,
        "arbitration": NoticeType.ARBITRATION_INVOCATION_SEC_21,
        "tpa106": NoticeType.TENANCY_TERMINATION_TPA_106,
        "tenancy": NoticeType.TENANCY_TERMINATION_TPA_106,
        "ibc8": NoticeType.IBC_OPERATIONAL_CREDITOR_SEC_8,
        "ibc": NoticeType.IBC_OPERATIONAL_CREDITOR_SEC_8,
        "general": NoticeType.GENERAL_LEGAL_DEMAND,
    }
    ntype = mapping.get(req.notice_type.lower(), NoticeType.CHEQUE_BOUNCE_NI_ACT_138)
    s_party = NoticeParty(
        name=req.sender.name,
        address=req.sender.address,
        advocate_name=req.sender.advocate_name,
        advocate_enrollment=req.sender.advocate_enrollment,
    )
    r_party = NoticeParty(name=req.recipient.name, address=req.recipient.address)

    draft = StatutoryNoticeDraftingEngine.draft_notice(
        notice_type=ntype,
        sender=s_party,
        recipient=r_party,
        facts=req.facts,
        as_of_date=req.as_of_date,
    )

    docx_bytes = StatutoryNoticeExportEngine.export_to_docx(draft)
    filename = f"legal_notice_{draft.notice_type.value}.docx"

    return Response(
        content=docx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
