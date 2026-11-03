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
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
import json
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
from legalmitra.models.gguf_adapter import (
    LocalGGUFModelAdapter,
    GGUFAdapterConfig,
)
from legalmitra.orchestration.decision_policy import LegalResponseState
from legalmitra.orchestration.pipeline import LegalQueryPipeline
from legalmitra.caselaw.visualizer import AuthorityGraphVisualizer
from legalmitra.caselaw.brief_engine import JudgmentSummarizerEngine, CaseBrief
from legalmitra.drafting.contract_auditor import ContractRiskAuditorEngine, ContractAuditReport

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
_gguf_pipeline: Optional[LegalQueryPipeline] = None


def get_pipeline(model_mode: str = "deterministic") -> LegalQueryPipeline:
    """Retrieve or initialize pipeline instance according to requested model mode."""
    global _default_pipeline, _mock_pipeline, _gguf_pipeline

    if model_mode == "mock":
        if _mock_pipeline is None:
            mock_adapter = LocalLegalModelAdapter(ModelAdapterConfig(enable_mock_for_testing=True))
            _mock_pipeline = LegalQueryPipeline(model_adapter=mock_adapter)
        return _mock_pipeline
    elif model_mode == "gguf":
        if _gguf_pipeline is None:
            gguf_adapter = LocalGGUFModelAdapter()
            _gguf_pipeline = LegalQueryPipeline(model_adapter=gguf_adapter)
        return _gguf_pipeline
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
    model_mode: str = Field("deterministic", description="Synthesis mode: deterministic, gguf, neural, or mock.")
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
    model_mode: str = Field("deterministic", description="deterministic, gguf, neural, or mock.")
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
    gguf_model_available: bool
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

    gguf_adapter = LocalGGUFModelAdapter()
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        fts_index_healthy=fts_healthy,
        lora_adapter_available=adapter.is_available,
        gguf_model_available=gguf_adapter.is_available,
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


# --- Authority Knowledge Graph Endpoints (Phase 75) ---

@app.get("/api/v1/graph/subgraph", tags=["Knowledge Graph"])
def get_authority_subgraph(
    focus_node: Optional[str] = Query(None, description="Optional center node ID (e.g. SEC-BSA-63, CASE-KESAVANANDA)"),
    max_hops: int = Query(1, description="Neighborhood depth around focus node"),
):
    """Returns node and edge payloads for the National Judicial Knowledge Graph."""
    visualizer = AuthorityGraphVisualizer()
    return visualizer.get_subgraph_data(focus_node_id=focus_node, max_hops=max_hops)


@app.get("/api/v1/graph/html", tags=["Knowledge Graph"])
def get_authority_graph_html(
    focus_node: Optional[str] = Query(None, description="Optional center node ID"),
    height: str = Query("600px", description="Render height for HTML container"),
):
    """Returns an interactive standalone Vis.js HTML document rendering the authority network."""
    visualizer = AuthorityGraphVisualizer()
    html_content = visualizer.render_visjs_html(focus_node_id=focus_node, height=height)
    return Response(content=html_content, media_type="text/html")


# --- Case Brief & Judgment Summarizer Endpoints (Phase 77) ---

class JudgmentSummarizeRequest(BaseModel):
    judgment_text: str = Field(..., description="Raw text of the Supreme Court or High Court judgment/order.")


@app.post("/api/v1/brief/summarize", tags=["Judicial Case Briefs"])
def summarize_court_judgment(req: JudgmentSummarizeRequest):
    """Parses a court judgment to extract Coram, Ratio Decidendi, Disposition, and BNS transitions."""
    if not req.judgment_text.strip():
        raise HTTPException(status_code=400, detail="judgment_text cannot be empty.")
    
    brief = JudgmentSummarizerEngine.summarize_judgment(req.judgment_text)
    return {
        "court": brief.metadata.court_name,
        "title": brief.metadata.case_title,
        "coram": brief.metadata.bench_coram,
        "disposition": brief.disposition,
        "ratio_decidendi": brief.ratio_decidendi,
        "obiter_dicta": brief.obiter_dicta,
        "statutory_transitions": [
            {
                "cited_act": t.cited_act,
                "cited_section": t.cited_section,
                "modern_act": t.modern_act,
                "modern_section": t.modern_section,
                "status_note": t.status_note
            }
            for t in brief.statutory_transitions
        ],
        "key_precedents_relied": brief.key_precedents_relied,
        "full_brief_markdown": brief.full_brief_markdown,
        "created_at": brief.created_at,
    }


# --- Commercial Agreement & Contract Risk Auditor Endpoints (Phase 78) ---

class ContractAuditRequest(BaseModel):
    contract_text: str = Field(..., description="Full text of the commercial agreement, NDA, employment or lease contract.")
    contract_title: Optional[str] = Field("Commercial Agreement", description="Title or description of the contract.")


@app.post("/api/v1/contract/audit", tags=["Contract Risk Auditing"])
def audit_commercial_contract(req: ContractAuditRequest):
    """Audits commercial contract clauses against Section 27, Section 28, and Supreme Court precedent."""
    if not req.contract_text.strip():
        raise HTTPException(status_code=400, detail="contract_text cannot be empty.")
    
    report = ContractRiskAuditorEngine.audit_contract(req.contract_text, title=req.contract_title or "Commercial Agreement")
    return {
        "contract_title": report.contract_title,
        "composite_risk_score": report.composite_risk_score,
        "overall_compliance_verdict": report.overall_compliance_verdict,
        "critical_risks_count": report.critical_risks_count,
        "high_risks_count": report.high_risks_count,
        "medium_risks_count": report.medium_risks_count,
        "total_clauses_analyzed": report.total_clauses_analyzed,
        "findings": [
            {
                "clause_category": f.clause_category,
                "flagged_text": f.flagged_text,
                "severity": f.severity.value,
                "governing_statute": f.governing_statute,
                "statutory_violation": f.statutory_violation,
                "judicial_authority": f.judicial_authority,
                "risk_explanation": f.risk_explanation,
                "recommended_counter_clause": f.recommended_counter_clause
            }
            for f in report.findings
        ],
        "executive_summary_markdown": report.executive_summary_markdown,
        "created_at": report.created_at,
    }


# --- Real-Time Token Streaming Endpoints (Phase 79) ---

class StreamQueryRequest(BaseModel):
    query: str = Field(..., description="The legal query to stream answers for.")
    context_date: Optional[str] = Field(None, description="Point-in-time date.")
    jurisdiction: Optional[str] = Field(None, description="Territorial jurisdiction code.")
    mock_mode: bool = Field(False, description="Use fast mock generator for testing streaming client.")


@app.post("/api/v1/query/stream", tags=["Real-Time Token Streaming"])
def stream_legal_query(req: StreamQueryRequest):
    """Streams generated IRAC response token-by-token via Server-Sent Events (SSE)."""
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query text cannot be empty.")

    # 1. Indic Language Detection & Full-Duplex Translation Bridge
    from legalmitra.multilingual.duplex_bridge import BhashiniFullDuplexBridge
    from legalmitra.multilingual.bhashini_pipeline import IndicLanguageCode

    duplex = BhashiniFullDuplexBridge()
    effective_query, detected_lang = duplex.normalize_indic_to_english_query(req.query)

    # 2. Retrieve evidence from pipeline using normalized statutory concepts
    pipeline = get_pipeline("deterministic")
    resolved = pipeline.execute(query=effective_query, context_date=req.context_date, jurisdiction=req.jurisdiction)
    provisions = [{"act": prov, "section": "", "text": prov} for prov in resolved.governing_provisions]
    precedents = [{"case_title": cit, "citation": "", "ratio": cit} for cit in resolved.citations]

    # Initialize adapter
    adapter_cfg = GGUFAdapterConfig(enable_mock_for_testing=req.mock_mode)
    adapter = LocalGGUFModelAdapter(adapter_cfg)

    def event_generator():
        yield f"event: metadata\ndata: {json.dumps({'query': req.query, 'status': 'generating'})}\n\n"
        
        # Determine base answer text
        full_text = resolved.answer_text
        # Check if query specifically targets Criminal Breach of Trust or FIR
        q_lower = effective_query.lower()
        if (
            not full_text
            or len(full_text.strip()) < 20
            or "ABSTENTION" in full_text
        ):
            from legalmitra.training.aikosh_finetuner import AIKoshLegalFineTuner
            finetuner = AIKoshLegalFineTuner()
            full_text = finetuner.generate_response(effective_query)
        else:
            # Compact multi-line scattered spacing and ensure clean IRAC presentation
            import re
            full_text = re.sub(r'\n{3,}', '\n\n', full_text)
            # Remove repetitive mechanical standard headers if present
            full_text = full_text.replace("the governing legal standard is: ", "")

        # 3. If original query was in an Indic language, translate back while protecting statutory numbers
        if detected_lang != IndicLanguageCode.ENGLISH:
            trans_res = duplex.translate_legal_text(full_text, target_lang=detected_lang)
            full_text = trans_res.translated_text

        # Stream word-by-word with realistic human typing cadence
        words = full_text.split(" ")
        for i, word in enumerate(words):
            prefix = "" if i == 0 else " "
            token = prefix + word
            chunk_payload = json.dumps({"token": token})
            yield f"event: token\ndata: {chunk_payload}\n\n"
            time.sleep(0.012)
                
        yield f"event: done\ndata: {json.dumps({'status': 'completed'})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Digital India Bhashini ASR (Phase 93)
# ---------------------------------------------------------------------------
class VoiceTranscribeRequest(BaseModel):
    audio_base64: str = Field(..., description="Base64-encoded audio.")
    language: str = Field("mr", description="Indic language code.")


@app.post("/api/v1/voice/transcribe", tags=["Digital India Bhashini Gateway"])
def transcribe_voice_query(req: VoiceTranscribeRequest):
    """Transcribes citizen voice query into native Indic legal text via Bhashini ASR."""
    if not req.audio_base64.strip():
        raise HTTPException(status_code=400, detail="audio_base64 payload cannot be empty.")
    from legalmitra.multilingual.asr_engine import BhashiniASREngine
    asr = BhashiniASREngine()
    result = asr.transcribe_base64(req.audio_base64, language=req.language)
    if not result.success:
        raise HTTPException(status_code=500, detail=result.error_message)
    return {
        "success": True,
        "language": result.language,
        "transcription": result.transcription,
        "confidence_score": result.confidence_score,
        "duration_seconds": result.duration_seconds,
        "latency_ms": result.latency_ms,
        "provider": result.provider
    }


# ---------------------------------------------------------------------------
# Digital India Bhashini Document OCR (Phase 94)
# ---------------------------------------------------------------------------
class DocumentOCRRequest(BaseModel):
    document_base64: str = Field(..., description="Base64-encoded PDF or image scan of FIR, notice, or agreement.")
    language: str = Field("mr", description="Indic language code (e.g. mr, hi, ta, te, en).")


@app.post("/api/v1/document/ocr-analyze", tags=["Digital India Bhashini Gateway"])
def analyze_document_scan(req: DocumentOCRRequest):
    """Extracts text from scanned FIRs, complaints, or notices and detects statutory penal provisions."""
    if not req.document_base64.strip():
        raise HTTPException(status_code=400, detail="document_base64 cannot be empty.")
    from legalmitra.multilingual.ocr_engine import BhashiniLegalOCREngine
    ocr = BhashiniLegalOCREngine()
    result = ocr.analyze_base64(req.document_base64, language=req.language)
    if not result.success:
        raise HTTPException(status_code=500, detail=result.error_message)
    return {
        "success": True,
        "document_type": result.document_type,
        "language": result.language,
        "extracted_text": result.extracted_text,
        "detected_statutes": [
            {
                "raw_mention": s.raw_mention,
                "statute_code": s.statute_code,
                "section_number": s.section_number,
                "normalized_canonical": s.normalized_canonical
            }
            for s in result.detected_statutes
        ],
        "latency_ms": result.latency_ms,
        "provider": result.provider
    }


# ---------------------------------------------------------------------------
# Digital India Bhashini IndicTrans2 NMT (Phase 95)
# ---------------------------------------------------------------------------
class IndicTranslationRequest(BaseModel):
    text: str = Field(..., description="English or Indic statutory legal text to translate.")
    target_language: str = Field("mr", description="Target 22 scheduled language code or dialect (e.g. mr, hi, ta, te, bn, gu, kn, bho).")


@app.post("/api/v1/nmt/translate", tags=["Digital India Bhashini Gateway"])
def translate_statutory_text(req: IndicTranslationRequest):
    """Translates legal response across 22 Indic languages and dialects while strictly preserving statutory citations."""
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="text cannot be empty.")
    from legalmitra.multilingual.indictrans2_engine import SovereignIndicTrans2Engine
    nmt = SovereignIndicTrans2Engine()
    result = nmt.translate_with_sovereign_fidelity(req.text, target_language=req.target_language)
    return {
        "success": True,
        "source_language": result.source_language.value,
        "target_language": result.target_language.value,
        "translated_text": result.translated_text,
        "preserved_citations_count": len(result.preserved_citations),
        "preserved_citations": result.preserved_citations,
        "is_sovereign_grounded": result.is_sovereign_grounded
    }


# ---------------------------------------------------------------------------
# Digital India Bhashini TTS (Phase 96)
# ---------------------------------------------------------------------------
class VoiceSynthesizeRequest(BaseModel):
    text: str = Field(..., description="Legal explanation text to synthesize into spoken audio.")
    language: str = Field("mr", description="Indic language code (e.g. mr, hi, ta, te, bn, gu, kn, en).")
    gender: str = Field("female", description="Voice gender: female or male.")


@app.post("/api/v1/voice/synthesize", tags=["Digital India Bhashini Gateway"])
def synthesize_voice_advice(req: VoiceSynthesizeRequest):
    """Synthesizes legal guidance into native Indic voice audio for non-literate citizens."""
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="text cannot be empty.")
    from legalmitra.multilingual.tts_engine import BhashiniLegalTTSEngine
    tts = BhashiniLegalTTSEngine()
    result = tts.synthesize_speech(req.text, language=req.language, gender=req.gender)
    if not result.success:
        raise HTTPException(status_code=500, detail=result.error_message)
    return {
        "success": True,
        "language": result.language,
        "audio_base64": result.audio_base64,
        "audio_format": result.audio_format,
        "duration_seconds": result.duration_seconds,
        "latency_ms": result.latency_ms,
        "provider": result.provider
    }


# Digital India Bhashini Gateway (Phase 92)
# ---------------------------------------------------------------------------
@app.get('/api/v1/bhashini/status', tags=['Digital India Bhashini Gateway'])
def get_bhashini_gateway_status():
    """Returns connectivity and supported model status for Digital India Bhashini Gateway."""
    from legalmitra.multilingual.bhashini_gateway import BhashiniULCAGateway
    gw = BhashiniULCAGateway()
    return {
        'status': 'healthy',
        'environment': gw.config.active_environment,
        'cloud_enabled': gw.is_cloud_enabled(),
        'offline_fallback_enabled': gw.config.enable_offline_fallback,
        'supported_tasks': ['asr', 'translation', 'tts', 'ocr'],
        'supported_scheduled_languages': 22,
        'default_provider': 'MeitY Bhashini ULCA / Hybrid IndicTrans2'
    }


# ---------------------------------------------------------------------------
# Stitch UI Web Application Routes (Phase 80)
# ---------------------------------------------------------------------------
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIR, "assets")), name="assets")

    @app.get("/", tags=["Stitch Web UI"], include_in_schema=False)
    def serve_stitch_landing():
        """Serves the Stitch Design Landing Page."""
        index_path = os.path.join(FRONTEND_DIR, "index.html")
        return FileResponse(index_path)

    @app.get("/chat", tags=["Stitch Web UI"], include_in_schema=False)
    def serve_stitch_chat():
        """Serves the Stitch Design Interactive Legal Consultation UI."""
        chat_path = os.path.join(FRONTEND_DIR, "chat.html")
        return FileResponse(chat_path)
