"""
README Builder - Part XXI to Part XXV:
- Part XXI: Governance, Legal Risk Register & Open Ambiguities
- Part XXII: Deployment, Operations & Production Readiness
- Part XXIII: Complete Reference Tables & Appendices
- Part XXIV: Contribution Guidelines, Code Style & Integrity Standards
- Part XXV: Intellectual Property, Team Attribution & Future Roadmap
"""

def generate_part_21_governance() -> str:
    return """## Part XXI: Governance, Legal Risk Register & Open Ambiguities

### 21.1 The 6 Phase 9 Frozen Legal Ambiguities

During the Phase 9 freeze, Team Shatrujeet documented **6 critical open legal ambiguities** in Indian statutory jurisprudence (`data/06_review/pilot_20_open_issues.md` and `PHASE8_OPEN_LEGAL_ISSUES_REGISTER.md`). These represent unsettled questions of law where the platform deliberately refuses to provide definitive conclusions, instead presenting balanced judicial perspectives:

```text
+----------------------------------------------------------------------------------------------------------------------+
|                                    THE 6 PHASE 9 FROZEN LEGAL AMBIGUITIES                                            |
+-----+-----------------------------------------+------------------------------------+---------------------------------+
| No. | Legal Ambiguity Title                   | Statutory Conflict / Question      | Platform Governance Stance      |
+-----+-----------------------------------------+------------------------------------+---------------------------------+
| 01  | Temporal Applicability of Section 482   | Does Section 482 BNSS apply to     | Present jurisdictional split;   |
|     | BNSS vs Section 438 CrPC on FIRs lodged | FIRs registered post-July 1, 2024  | cite Section 531(2)(a) BNSS     |
|     | for offenses committed pre-July 1, 2024 | for pre-transition offenses?       | saving clause & High Court views|
+-----+-----------------------------------------+------------------------------------+---------------------------------+
| 02  | Electronic Evidence Certification under | Does Section 63 BSA render Section | Distinguish Section 63 BSA from |
|     | Section 63 BSA vs Section 65B IEA       | 65B certificate obsolete, or is a  | 65B IEA; cite *Arjun Panditrao* |
|     |                                         | formal certificate still required? | and emerging judicial notices   |
+-----+-----------------------------------------+------------------------------------+---------------------------------+
| 03  | Preliminary Enquiry Mandate under       | Does Section 173(3) BNSS conflict  | Abstain from declaring mandate  |
|     | Section 173(3) BNSS vs Lalita Kumari    | with the mandatory FIR rule in     | absolute; explain the 14-day    |
|     | Mandatory FIR Directive                 | *Lalita Kumari (2014) 2 SCC 1*?    | enquiry window for 3-7 yr cases |
+-----+-----------------------------------------+------------------------------------+---------------------------------+
| 04  | Police Custody Beyond Initial 15 Days   | Does Section 187(3) BNSS authorize | Note constitutional split; cite |
|     | under Section 187(3) BNSS               | police custody during the entire   | *CBI v. Anupam Kulkarni* and    |
|     |                                         | 40/60-day investigation window?    | pending Supreme Court references|
+-----+-----------------------------------------+------------------------------------+---------------------------------+
| 05  | Territorial High Court Writ Powers over | Can High Courts issue writs to     | Cite *Kusum Ingots (2004)*;     |
|     | Central Digital Intermediaries (Art 226)| central digital portals outside    | explain forum conveniens and    |
|     |                                         | territorial physical jurisdiction? | cause of action nexus under 226 |
+-----+-----------------------------------------+------------------------------------+---------------------------------+
| 06  | Hit-and-Run Commencement Under Section  | Has Section 106(2) BNS commenced   | State clearly that Section      |
|     | 106(2) of the Bharatiya Nyaya Sanhita   | following government assurances    | 106(2) BNS remains unnotified   |
|     |                                         | to transport worker federations?   | per Gazette S.O. notifications  |
+-----+-----------------------------------------+------------------------------------+---------------------------------+
```

### 21.2 The 40 Advocate Review Candidates Register

The platform maintains an authoritative **Review Tracking Register** (`data/07_batches/review/review_tracking_register.json`) managing **40 candidate records**:
- **Package A (Pilot 20 Snapshot)**: 20 foundational statutory and caselaw examples locked in Phase 9.
- **Package B (Batch 01 Candidate Expansion)**: 20 expanded commercial and procedural examples created in Phase 15.
- **Invariant**: All 40 records are locked in `pending_legal_review` status.
- **Integrity Rule**: No candidate record may be ingested into production training sets or active RAG indexing without an enrolled advocate's digital review signature, bar council registration number, and signed review sheet.

### 21.3 Synthetic Scaffold Quarantine Protocol

The synthetic scaffold case `IND-JUD-DEL-2024-BAIL` (6 chunks) remains strictly quarantined in `data/09_national_corpus/quarantine/`.
- Automatic CI checks verify that zero chunks from this fixture enter `data/legalmitra_kb.db` with `is_synthetic_scaffold = 0`.
- Pretraining dataset exporters actively verify and raise `QuarantineViolationError` if any reference to this case appears.

### 21.4 Criminal Law Transition Governance (IPC/CrPC/IEA vs BNS/BNSS/BSA)

LegalMitra implements strict constitutional governance regarding the 2024 Criminal Law Transition:
1. **Article 20(1) Non-Retroactivity**:
   - No person shall be convicted of any offence except for violation of the law in force at the time of the commission of the act.
   - For any offense committed prior to July 1, 2024, the substantive offense must be charged under the Indian Penal Code, 1860, not the Bharatiya Nyaya Sanhita, 2023.
2. **Procedural Savings Clause (Section 531 BNSS)**:
   - Pending investigations, inquiries, trials, and appeals instituted prior to July 1, 2024 continue under the Code of Criminal Procedure, 1973.
   - Procedural actions instituted on or after July 1, 2024 follow the Bharatiya Nagarik Suraksha Sanhita, 2023.

---
"""

def generate_part_22_deployment() -> str:
    return """## Part XXII: Deployment, Operations & Production Readiness

### 22.1 Standalone Local Server Mode

To launch LegalMitra in a local development or offline workstation environment:

```powershell
# 1. Activate virtual environment
.\\.venv\\Scripts\\Activate.ps1

# 2. Start Uvicorn ASGI server with hot reloading
uvicorn legalmitra.web.app:app --host 127.0.0.1 --port 8000 --reload
```
Navigate to `http://localhost:8000/chat` to access the Google Stitch Constitutional Modernism web client.

### 22.2 High-Throughput Production Architecture

For production deployments serving multiple concurrent legal practitioners, LegalMitra runs behind Nginx with Gunicorn workers:

```text
[ Incoming HTTPS Client Traffic ]
               │
               ▼
[ Nginx Reverse Proxy / SSL Termination ]
  • TLS 1.3 / HSTS Enforcement
  • Static Asset Caching (/static)
  • Request Buffering & Rate Limiting (100 req/s ceiling)
               │
               ▼
[ Gunicorn Worker Cluster (4-8 Workers) ]
  • `gunicorn legalmitra.web.app:app -w 4 -k uvicorn.workers.UvicornWorker`
  • Shared Memory IPC
               │
        ┌──────┴──────┐
        ▼             ▼
[ legalmitra_kb.db ] [ conversations.db ]
(WAL Mode Shared)    (WAL Mode Concurrent)
```

#### Production Systemd Unit File (`/etc/systemd/system/legalmitra.service`):
```ini
[Unit]
Description=LegalMitra National Legal AI Intelligence Platform
After=network.target

[Service]
User=legalmitra
Group=legalmitra
WorkingDirectory=/opt/LegalMitra
Environment="PATH=/opt/LegalMitra/.venv/bin"
Environment="LEGALMITRA_ENV=production"
Environment="LEGALMITRA_KB_PATH=/opt/LegalMitra/data/legalmitra_kb.db"
Environment="LEGALMITRA_CONV_PATH=/opt/LegalMitra/data/conversations.db"
Environment="RATE_LIMIT_PER_MINUTE=60"
ExecStart=/opt/LegalMitra/.venv/bin/gunicorn legalmitra.web.app:app \\
          --workers 4 \\
          --worker-class uvicorn.workers.UvicornWorker \\
          --bind 127.0.0.1:8000 \\
          --access-logfile /var/log/legalmitra/access.log \\
          --error-logfile /var/log/legalmitra/error.log
Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

### 22.3 PostgreSQL & Vector DB Migration Strategy

As part of the enterprise scaling roadmap (Milestone D):
- **Structured Knowledge Storage**: Migrate `legalmitra_kb.db` to PostgreSQL 16+ with row-level security.
- **Dense Vector Search**: Incorporate `pgvector` extension to enable hybrid dense-lexical retrieval alongside `pg_trgm` and PostgreSQL full-text search.
- **Session High Availability**: Transition `conversations.db` to Amazon Aurora PostgreSQL or high-availability PostgreSQL clusters.

### 22.4 Monitoring, Alerting & Health Check Probes

- **Liveness Endpoint**: `http://localhost:8000/api/v1/health` (Probed every 10 seconds).
- **Readiness Endpoint**: `http://localhost:8000/api/v1/ready` (Probed before routing ingress traffic).
- **Alerting Triggers**:
  - Sustained HTTP 429 triggers (>5% of total requests) -> Trigger rate limit alert.
  - Average latency exceeding 3.0s -> Trigger compute scaling event.
  - SQLite database integrity check failure -> Trigger immediate failover to hot standby.

---
"""

def generate_part_23_appendices_intro() -> str:
    return """## Part XXIII: Complete Reference Tables & Appendices

### Appendix A: Complete API Endpoint Matrix

| Method | Path | Request Body | Response Body | Auth / Permissions | Purpose |
|:---:|:---|:---|:---|:---:|:---|
| `GET` | `/` | None | HTML / Redirect | Public | Root portal landing page |
| `GET` | `/chat` | None | HTML Web App | Public | Google Stitch Constitutional Chat UI |
| `GET` | `/api/v1/health` | None | `HealthResponse` | Public | Application liveness probe |
| `GET` | `/api/v1/ready` | None | `ReadyResponse` | Public | Database readiness probe |
| `POST`| `/api/v1/chat` | `ChatRequest` | `ChatResponse` | Rate Limited (30/min)| Core legal inference & RAG |
| `GET` | `/api/v1/conversations` | Query params | `List[ConversationItem]`| Session Bound | Lists user previous chat sessions |
| `GET` | `/api/v1/conversations/{id}/messages`| None | `List[MessageItem]`| Session Bound | Returns message transcript |
| `DELETE`| `/api/v1/conversations/{id}`| None | `DeleteStatus` | Session Bound | Purges session and history |
| `POST`| `/api/v1/feedback` | `FeedbackRequest` | `FeedbackResponse` | Session Bound | Records accuracy feedback |
| `GET` | `/docs` | None | Swagger UI | Dev / Staging | OpenAPI documentation |
| `GET` | `/redoc` | None | ReDoc UI | Dev / Staging | ReDoc API specification |

### Appendix B: Database Tables & Columns Master Catalog

```text
DATABASE: data/legalmitra_kb.db
├── sources (document_id, title, source_url, source_type, jurisdiction, court, document_date, effective_date, is_historical, is_synthetic_scaffold, repeal_status, checksum, verification_status, metadata_json)
├── legal_chunks (chunk_id, source_id, doc_type, act_or_case_title, provision_or_para_ref, hierarchy_level, section_number, paragraph_number, jurisdiction, court, document_date, effective_date, is_historical, is_synthetic_scaffold, authority_level, content, metadata_json)
├── legal_chunks_fts (FTS5 VIRTUAL TABLE: chunk_id UNINDEXED, act_or_case_title, provision_or_para_ref, content)
├── cases (case_id, court_code, case_type, case_number, filing_year, petitioner_or_appellant, respondent, neutral_citation, institution_date, disposal_date, status, metadata_json)
├── judicial_documents (document_id, case_id, classification, procedural_effect, order_or_judgment_date, bench_coram_json, verbatim_text, source_url, sha256_hash, is_synthetic_scaffold, verification_status, metadata_json)
└── hearing_events (event_id, case_id, listing_date, hearing_type, presiding_bench, procedural_outcome, daily_order_id, next_listing_date, is_cause_list_verified, metadata_json)

DATABASE: data/conversations.db
├── conversations (conversation_id, title, created_at, updated_at, is_bookmarked, session_id)
├── messages (message_id, conversation_id, role, content, citations_json, evidence_json, model_used, latency_seconds, created_at)
└── feedback (feedback_id, conversation_id, query, is_helpful, feedback_text, created_at, session_id)
```

### Appendix C: Environment Variables Master Catalog

| Environment Variable | Format / Type | Default | Criticality |
|:---|:---:|:---:|:---:|
| `LEGALMITRA_ENV` | String enum | `"development"` | High |
| `LEGALMITRA_KB_PATH` | File path | `"data/legalmitra_kb.db"` | Critical |
| `LEGALMITRA_CONV_PATH` | File path | `"data/conversations.db"` | Critical |
| `LEGALMITRA_OFFLINE_EVAL` | Flag (`"0"` or `"1"`) | `"0"` | Critical |
| `NEMOTRON_API_KEY` | Hex / Alphanumeric | `None` | High (Live mode) |
| `NEMOTRON_BASE_URL` | HTTPS URL | `"https://integrate.api.nvidia.com/v1"` | Medium |
| `NEMOTRON_MODEL_NAME` | String identifier | `"nvidia/llama-3.1-nemotron-70b-instruct"` | Medium |
| `NEMOTRON_TIMEOUT_SECONDS` | Float | `60.0` | Medium |
| `RATE_LIMIT_PER_MINUTE` | Integer | `30` | High |
| `ALLOWED_ORIGINS` | Comma-separated URLs | `"*"` | High |
| `MAX_UPLOAD_SIZE_BYTES` | Integer bytes | `10485760` | Medium |
| `LOG_LEVEL` | String log level | `"INFO"` | Low |

### Appendix E: HTTP Status Codes & Error Messages Catalog

```text
HTTP 200 OK
  Success: Query processed, evidence retrieved, and grounded answer generated.

HTTP 400 Bad Request
  Error: Query string shorter than 3 characters or exceeding 2000 characters.
  Payload: {"detail": "Query must be between 3 and 2000 characters."}

HTTP 404 Not Found
  Error: The requested conversation_id does not exist in conversations.db.
  Payload: {"detail": "Conversation session not found."}

HTTP 422 Unprocessable Entity
  Error: Pydantic validation failure. Missing required fields or incorrect data types.
  Payload: {"detail": [{"loc": ["body", "query"], "msg": "field required", "type": "value_error.missing"}]}

HTTP 429 Too Many Requests
  Error: Client exceeded 30 requests per minute rate limit ceiling.
  Headers: Retry-After: 35
  Payload: {"detail": "Rate limit exceeded. Please wait 35 seconds before retrying."}

HTTP 500 Internal Server Error
  Error: Unhandled exception during retrieval, prompt assembly, or database interaction.
  Payload: {"detail": "Internal server error. Telemetry logged."}

HTTP 503 Service Unavailable
  Error: Database locked or unreachable.
  Payload: {"detail": "Knowledge base temporarily unavailable. Please retry."}
```
"""

def generate_part_24_contribution() -> str:
    return """## Part XXIV: Contribution Guidelines, Code Style & Integrity Standards

### 24.1 Branching Strategy & Git Workflows

To preserve technical stability, LegalMitra enforces a strict Git trunk-based branch workflow:
- **Protected Trunk**: The `main` branch is protected. Direct commits are restricted to validated phase releases.
- **Development Branches**: Feature and research work occurs on isolated branches prefixed by phase or capability:
  - `feature/phase37-corpus-acquisition`
  - `research/tokenizer-v3-devanagari`
  - `fix/ssrf-ipv6-edge-cases`
- **Rebase Policy**: Always rebase on latest `main` before submitting pull requests. Merge commits must be signed and retain linear history.

### 24.2 Commit Message Standards

Commits must follow the Conventional Commits specification:
```text
<type>(<scope>): <short descriptive imperative summary>

[optional body providing technical context, rationale, and issue links]

[optional footer noting breaking changes or phase references]
```
- **Allowed Types**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `security`.
- **Allowed Scopes**: `core`, `corpus`, `ingestion`, `knowledge`, `rag`, `web`, `research`, `evaluation`, `review`.
- **Example**: `docs: comprehensively document LegalMitra architecture and workflows`

### 24.3 Coding Conventions & Linting

All Python code must satisfy strict formatting standards:
- **Code Formatter**: Black with line length 100 characters.
- **Linter**: Flake8 with zero ignored syntax errors.
- **Type Annotations**: Strict type hints across all function signatures using modern Python 3.11 union syntax (`str | None`, `List[T]`).
- **Docstrings**: Google-style docstrings with explicit Args, Returns, and Raises sections.

### 24.4 Invariant Enforcement & Pre-Commit Checks

Before staging or committing any changes, developers must execute the three mandatory invariant verifications:

```powershell
# Invariant Check 1: Verify Phase 9 Frozen Artifacts (Must be 6/6 identical)
python scripts/verify_freeze.py

# Invariant Check 2: Verify Advocate Review Packages (Must be 40/40 pending)
python scripts/verify_review_packages.py

# Invariant Check 3: Run Full Pytest Suite (Must pass 315 tests)
pytest -q
```

---
"""

def generate_part_25_ownership_and_roadmap() -> str:
    return """## Part XXV: Intellectual Property, Team Attribution & Future Roadmap

### 25.1 Team Shatrujeet Ownership & Authorship

LegalMitra was conceived, architected, and engineered in October 2026 by **Team Shatrujeet**:

```text
========================================================================================================================
                                             TEAM SHATRUJEET — CORE FOUNDERS
========================================================================================================================
  • Amar Khera        : Lead Architect, RAG Systems, Original Transformer Pretraining & Scaling Gate
  • Ananya Rout       : Senior Legal Data Architect, Statutory Taxonomy, Pydantic Schema Contracts
  • Lucky Kumar       : Senior Infrastructure Engineer, SQLite/FTS5 Engineering, Security Red-Team Lead
  • Omm Prakash Sahoo : Senior UI/UX Engineer, Advocate Review Operations, Web API Architecture
========================================================================================================================
```

### 25.2 Proprietary License Terms

Copyright © October 2026 Team Shatrujeet. All Rights Reserved.

This software, including its source code, compiled binaries, neural weights, tokenizers, database schemas, and documentation, is **PROPRIETARY AND CONFIDENTIAL**. 

1. **Strictly Restricted Access**: Unauthorized copying, reverse engineering, redistribution, scraping, modification, or academic misappropriation of this software, via any medium, is strictly prohibited.
2. **No Commercial Use**: No part of this platform may be deployed for commercial services or integrated into third-party applications without prior express written authorization from Team Shatrujeet.
3. **Research Sovereignty**: The original model architectures and datasets are created exclusively for advancing Indian legal AI sovereignty.

### 25.3 Third-Party Component Attributions

LegalMitra acknowledges the foundational contributions of the following open-source libraries:
- **PyTorch**: Deep learning and neural tensor library by the PyTorch Foundation.
- **FastAPI & Pydantic**: Modern, high-performance web framework and data validation by Sebastián Ramírez.
- **SQLite & FTS5**: Public domain relational database and full-text search engine by D. Richard Hipp.
- **IBM Docling**: Document layout parsing and structural PDF extraction library by IBM Research.

### 25.4 Future Roadmap: Milestones B through E

With the completion of Phase 36 and the comprehensive documentation audit in Phase 35.5, Team Shatrujeet has established the execution roadmap for subsequent development milestones:

```text
+----------------------------------------------------------------------------------------------------------------------+
|                                          LEGALMITRA STRATEGIC ROADMAP (2026-2027)                                    |
+-------------+---------------------------+---------------------------------+------------------------------------------+
| Milestone   | Target Horizon            | Primary Technical Objective     | Core Deliverables & Metric Targets       |
+-------------+---------------------------+---------------------------------+------------------------------------------+
| Milestone B | Post-Phase 36             | 1 Million Bilingual Tokens      | Expand authentic Hindi statutes past     |
|             |                           | Expanded Ingestion Pipeline     | 100K tokens; 50 new Central Acts indexed |
+-------------+---------------------------+---------------------------------+------------------------------------------+
| Milestone C | Pretraining Scale Gate    | 21.5 Million National Tokens    | Achieve Chinchilla optimality for 1.07M  |
|             |                           | (Pass Scaling Heuristic Gate)   | model; index all 28 State Legislatures   |
+-------------+---------------------------+---------------------------------+------------------------------------------+
| Milestone D | Multi-GPU Pretraining     | 10.5 Million Parameter Model    | Scale to 10M transformer on 211M tokens; |
|             | Distributed Compute       | Multi-GPU DDP Training Cluster  | Distributed AdamW with FlashAttention-2  |
+-------------+---------------------------+---------------------------------+------------------------------------------+
| Milestone E | Advocate Pilot Deployment | Bar Association Field Pilot     | 100 Enrolled Advocates Pilot in Supreme  |
|             | Institutional Ingress     | Production PostgreSQL Migration | Court of India & Delhi High Court        |
+-------------+---------------------------+---------------------------------+------------------------------------------+
```

---

```text
========================================================================================================================
                      END OF LEGALMITRA COMPREHENSIVE ARCHITECTURE & OPERATIONAL REFERENCE
                                          TEAM SHATRUJEET — OCTOBER 2026
========================================================================================================================
```
"""
