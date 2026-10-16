# LEGALMITRA: OPERATIONS RUNBOOK

**Document Version:** 1.1.0  
**Target Environment:** Local & Staging  
**Application:** LegalMitra AI Chatbot  

---

## 1. Service Architecture & Entry Points

- **Application Module**: `legalmitra.web.app:app`
- **Command-line Runner**: `run_server.py`
- **Default Bind Address**: `127.0.0.1:8000`
- **Primary Routes**:
  - `GET /` — Landing Page (Constitutional Modernism)
  - `GET /chat` — AI Chat Application
  - `GET /api/v1/health` — Liveness & Knowledge Base Chunk Probe
  - `GET /api/v1/ready` — Readiness Probe for Traffic Routing
  - `POST /api/v1/chat` — Source-Grounded Legal Query Submission
  - `GET /api/v1/conversations` — Scoped Conversation Session Listing
  - `GET /api/v1/conversations/{id}/messages` — Message Retrieval
  - `DELETE /api/v1/conversations/{id}` — Session Conversation Deletion
  - `POST /api/v1/feedback` — Evaluator Precision Feedback

---

## 2. Startup & Health Verification

1. **Start the Application**:
   ```bash
   python run_server.py
   ```
2. **Verify Liveness**:
   ```bash
   curl -s http://127.0.0.1:8000/api/v1/health
   # Expected: {"status":"healthy","app_name":"LegalMitra AI Chatbot",...}
   ```
3. **Verify Readiness**:
   ```bash
   curl -s http://127.0.0.1:8000/api/v1/ready
   # Expected: {"status":"ready","kb_status":"connected","chunks_indexed":1149,...}
   ```

---

## 3. Operational Troubleshooting

### Problem 1: `Knowledge base missing at data/legalmitra_kb.db`
- **Cause**: The statutory SQLite database was not found or the path is misconfigured.
- **Resolution**:
  - Verify that `data/legalmitra_kb.db` is present and non-zero in size.
  - Check the `LEGALMITRA_KB_PATH` environment variable.
  - The application will refuse to start silently with an empty database to protect legal validity.

### Problem 2: `429 Too Many Requests`
- **Cause**: Client exceeded the configured requests-per-minute threshold (default: 30 requests/min).
- **Resolution**:
  - Adjust `RATE_LIMIT_PER_MINUTE` in `.env` if legitimate load requires higher throughput.

### Problem 3: `404 Not Found` or `403 Forbidden` on conversation retrieval
- **Cause**: Session isolation security is active. A client with session ID `A` is attempting to access a conversation created by session ID `B`.
- **Resolution**: Expected security behavior. Ensure the client sends the proper session cookie (`legalmitra_session`) or header (`X-Session-ID`).

---

## 4. Graceful Shutdown & Maintenance

- Send `SIGINT` (Ctrl+C) or `SIGTERM` to the process.
- Uvicorn will stop accepting new requests, finish processing in-flight queries within the timeout window, and close SQLite database connection handles cleanly.

