"""
LegalMitra FastAPI Application Entry Point
Exposes source-grounded Indian legal intelligence API endpoints, conversation persistence,
security controls, session isolation, and serves the Stitch Constitutional Modernism frontend.
"""

import os
import secrets
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from legalmitra.core.logging import get_logger
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
from legalmitra.knowledge.models import SearchFilters
from legalmitra.rag.engine import LegalRAGEngine
from legalmitra.web.schemas import (
    ChatRequest,
    ChatResponse,
    FeedbackRequest,
    FeedbackResponse,
    HealthStatus,
    SourceEvidenceItem,
)
from legalmitra.web.store import ConversationStore

logger = get_logger("web_api")

app = FastAPI(
    title="LegalMitra AI Chatbot API",
    description="Source-Grounded Indian Legal Intelligence System",
    version="1.1.0",
)

# CORS configuration: strict allowed origins
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "ALLOWED_ORIGINS",
        "http://localhost:8000,http://127.0.0.1:8000,http://localhost:3000"
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Session-ID"],
)

# Initialize backend services
KB_PATH = Path(os.environ.get("LEGALMITRA_KB_PATH", "data/legalmitra_kb.db"))
if not KB_PATH.exists():
    logger.critical(f"Configured Legal Knowledge Base does not exist at {KB_PATH}!")
    raise RuntimeError(f"Critical configuration error: Knowledge base missing at {KB_PATH}")

kb = LegalKnowledgeBase(db_path=KB_PATH)
rag_engine = LegalRAGEngine(knowledge_base=kb)
conv_store = ConversationStore(db_path=os.environ.get("LEGALMITRA_CONV_PATH", "data/conversations.db"))

# Base directories
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# Rate Limiting & Request Throttling Cache (In-Memory sliding window)
RATE_LIMIT_MAX_REQUESTS = int(os.environ.get("RATE_LIMIT_PER_MINUTE", "30"))
_rate_limit_cache: Dict[str, List[float]] = {}


def check_rate_limit(client_id: str) -> bool:
    """Enforce request rate limiting per minute per client."""
    now = time.time()
    timestamps = _rate_limit_cache.get(client_id, [])
    # prune entries older than 60s
    timestamps = [t for t in timestamps if now - t < 60.0]
    if len(timestamps) >= RATE_LIMIT_MAX_REQUESTS:
        _rate_limit_cache[client_id] = timestamps
        return False
    timestamps.append(now)
    _rate_limit_cache[client_id] = timestamps
    return True


# Session Management Dependency
SESSION_COOKIE_NAME = "legalmitra_session"
IS_PRODUCTION = os.environ.get("LEGALMITRA_ENV", "development").lower() == "production"


def get_current_session(request: Request, response: Response) -> str:
    """
    Extract or generate a secure, isolated session identifier.
    Guarantees privacy by preventing cross-client conversation enumeration.
    """
    session_id = request.cookies.get(SESSION_COOKIE_NAME)
    if not session_id:
        # Check header fallback for headless/mobile API clients
        session_id = request.headers.get("X-Session-ID")
    
    if not session_id or len(session_id) < 16:
        session_id = secrets.token_urlsafe(24)
        response.set_cookie(
            key=SESSION_COOKIE_NAME,
            value=session_id,
            httponly=True,
            samesite="lax",
            secure=IS_PRODUCTION,
            max_age=86400 * 30,  # 30 days
        )
    return session_id


# Security & Request Size Middleware
MAX_REQUEST_BODY_BYTES = 64 * 1024  # 64 KB limit for JSON payloads


@app.middleware("http")
async def security_and_limit_middleware(request: Request, call_next):
    # Request body size enforcement
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > MAX_REQUEST_BODY_BYTES:
        return JSONResponse(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            content={"detail": "Request payload exceeds maximum allowed size of 64KB."}
        )

    response = await call_next(request)
    
    # Injected Security Headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data: https://lh3.googleusercontent.com https://contribution.usercontent.google.com; "
        "connect-src 'self';"
    )
    return response


# --- Health & Readiness Endpoints ---

@app.get("/api/v1/health", response_model=HealthStatus)
def health_check():
    """Liveness probe: verifies process health and basic knowledge base availability."""
    try:
        cursor = kb.conn.cursor()
        cursor.execute("SELECT count(*) FROM legal_chunks")
        chunk_count = cursor.fetchone()[0]
        cursor.execute("SELECT count(DISTINCT source_id) FROM legal_chunks")
        source_count = cursor.fetchone()[0]
    except Exception as e:
        logger.error(f"Error querying KB stats: {e}")
        chunk_count = 0
        source_count = 0

    return HealthStatus(
        status="healthy" if chunk_count > 0 else "degraded",
        app_name="LegalMitra AI Chatbot",
        version="1.1.0",
        knowledge_base_chunks=chunk_count,
        active_sources=source_count,
        model_provider=rag_engine.llm_provider.__class__.__name__,
    )


@app.get("/api/v1/ready")
def readiness_check():
    """Readiness probe: validates database connectivity and RAG availability."""
    chunks = kb.count_chunks()
    if chunks == 0:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Knowledge base contains zero indexed chunks. Service not ready."
        )
    return {
        "status": "ready",
        "kb_status": "connected",
        "chunks_indexed": chunks,
        "llm_provider": rag_engine.llm_provider.__class__.__name__,
    }


# --- Legal Chat Endpoints ---

@app.post("/api/v1/chat", response_model=ChatResponse)
def submit_chat(
    req: ChatRequest,
    request: Request,
    response: Response,
    session_id: str = Depends(get_current_session)
):
    """
    Submit a legal inquiry to the LegalMitra source-grounded RAG engine.
    Enforces rate limits, evidential retrieval, and session-isolated conversation persistence.
    """
    # Rate limit check
    client_ip = request.client.host if (request.client and request.client.host) else "testclient"
    rate_key = f"{session_id}:{client_ip}"
    if not check_rate_limit(rate_key):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please wait a moment before submitting your next legal question."
        )

    clean_query = req.query.strip()
    if not clean_query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    # Manage conversation session with ownership check
    conv_id = req.conversation_id
    if conv_id:
        owner = conv_store.get_conversation_owner(conv_id)
        if owner and owner != session_id:
            logger.warning(f"Session {session_id} attempted cross-session write to {conv_id}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access to conversation denied.")
    else:
        conv_id = conv_store.create_conversation(session_id=session_id, title=clean_query[:50])

    # Record incoming user message
    conv_store.add_message(conversation_id=conv_id, role="user", content=clean_query)

    # Fetch prior messages in this conversation for multi-turn context
    prior_messages = conv_store.get_messages(conv_id, session_id=session_id) or []
    # Build history excluding the user message just added
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in prior_messages[:-1]
    ]

    # Build search filters
    filters = SearchFilters(
        act_title=req.act_filter,
        court=req.court_filter,
    )

    try:
        # Execute Source-Grounded RAG with conversation history
        rag_resp = rag_engine.answer_with_history(
            query=clean_query,
            history=history,
            filters=filters,
            limit=req.limit,
        )

        evidence_items = [
            SourceEvidenceItem(
                chunk_id=ev.chunk_id,
                source_id=ev.source_id,
                act_or_case_title=ev.act_or_case_title,
                provision_or_para_ref=ev.provision_or_para_ref,
                authority_level=ev.authority_level,
                verbatim_text=ev.verbatim_text,
                source_url=ev.source_url,
                effective_date=ev.effective_date,
                is_synthetic_scaffold=ev.is_synthetic_scaffold,
            )
            for ev in rag_resp.cited_evidence
        ]

        # Record assistant answer in conversation store
        conv_store.add_message(
            conversation_id=conv_id,
            role="assistant",
            content=rag_resp.answer,
            citations=rag_resp.citations,
            evidence=[e.model_dump() for e in evidence_items],
            model_used=rag_resp.model_used,
            latency_seconds=rag_resp.latency_seconds,
        )

        return ChatResponse(
            conversation_id=conv_id,
            query=clean_query,
            answer=rag_resp.answer,
            citations=rag_resp.citations,
            evidence=evidence_items,
            evidence_sufficiency=rag_resp.evidence_sufficiency,
            binding_authorities=rag_resp.binding_authorities,
            persuasive_authorities=rag_resp.persuasive_authorities,
            missing_facts_prompt=rag_resp.missing_facts_prompt,
            legal_disclaimer=rag_resp.legal_disclaimer,
            model_used=rag_resp.model_used,
            latency_seconds=round(rag_resp.latency_seconds, 2),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    except Exception as exc:
        logger.error(f"Inference error handling query: {exc}", exc_info=True)
        # Safe error response without exposing internal traces or credentials
        raise HTTPException(
            status_code=500,
            detail="The legal intelligence engine encountered an internal inference error. Please verify the query and try again."
        )


@app.get("/api/v1/conversations")
def list_conversations(
    limit: int = 20,
    session_id: str = Depends(get_current_session)
):
    """Retrieve recent conversation sessions strictly owned by the caller's session."""
    return conv_store.list_conversations(session_id=session_id, limit=limit)


@app.get("/api/v1/conversations/{conv_id}/messages")
def get_conversation_messages(
    conv_id: str,
    session_id: str = Depends(get_current_session)
):
    """Retrieve all messages for a specific conversation with strict ownership validation."""
    messages = conv_store.get_messages(conversation_id=conv_id, session_id=session_id)
    if messages is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied."
        )
    return messages


@app.delete("/api/v1/conversations/{conv_id}")
def delete_conversation(
    conv_id: str,
    session_id: str = Depends(get_current_session)
):
    """Delete a conversation thread permanently if owned by current session."""
    success = conv_store.delete_conversation(conversation_id=conv_id, session_id=session_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied."
        )
    return {"status": "deleted", "conversation_id": conv_id}


@app.post("/api/v1/feedback", response_model=FeedbackResponse)
def submit_feedback(
    fb: FeedbackRequest,
    session_id: str = Depends(get_current_session)
):
    """Record user evaluation feedback on legal answer accuracy."""
    fid = conv_store.record_feedback(
        conversation_id=fb.conversation_id,
        session_id=session_id,
        query=fb.query,
        is_helpful=fb.is_helpful,
        feedback_text=fb.feedback_text,
    )
    return FeedbackResponse(status="recorded", message=f"Feedback ID {fid} stored.")


# --- Frontend HTML Page Delivery ---

@app.get("/")
def serve_landing_page():
    """Serves the complete Constitutional Modernism Landing Page."""
    landing_file = TEMPLATES_DIR / "landing_page.html"
    if not landing_file.exists():
        raise HTTPException(status_code=404, detail="Landing page not found.")
    return FileResponse(str(landing_file), media_type="text/html")


@app.get("/chat")
def serve_chat_app():
    """Serves the complete Constitutional Modernism AI Chat Application."""
    chat_file = TEMPLATES_DIR / "chat.html"
    if not chat_file.exists():
        raise HTTPException(status_code=404, detail="Chat interface not found.")
    return FileResponse(str(chat_file), media_type="text/html")
