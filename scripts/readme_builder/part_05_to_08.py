"""
README Builder - Part V to Part VIII:
- Part V: Environment Setup, Hardware Profiles & Installation Guide
- Part VI: Configuration & Environment Variables Reference
- Part VII: Production Web API Reference
- Part VIII: Database Architecture & Data Storage Reference (Full DDL for all 10 tables)
"""

def generate_part_05_to_08() -> str:
    sections = []

    # Part V
    sections.append("""## Part V: Environment Setup, Hardware Profiles & Installation Guide

### 5.1 System Prerequisites & Supported Platforms

LegalMitra is built with native cross-platform support across modern 64-bit operating systems:
- **Operating Systems**: Windows 10/11 (PowerShell / Command Prompt), Ubuntu Linux 22.04 LTS+, Debian 12+, macOS Ventura / Sonoma.
- **Python Runtime**: Python 3.11.0 or higher (Strictly tested on Python 3.11.0 and 3.12.x). Python 3.10 is not supported due to modern Pydantic V2 and union typing requirements (`|`).
- **SQLite Engine**: SQLite version 3.35.0+ compiled with the FTS5 full-text search module (`SQLITE_ENABLE_FTS5`).
- **Git Version Control**: Git 2.30+ with support for long paths on Windows (`git config --system core.longpaths true`).

### 5.2 Hardware Profiling & Compute Tiers

LegalMitra dynamically adapts its computational profile depending on available hardware accelerators:

```text
+----------------------------------------------------------------------------------------------------------------------+
|                                        LEGALMITRA HARDWARE PROFILE TIERS                                             |
+-------------------+----------------------------+---------------------------+-----------------------------------------+
| Profile Tier      | Minimum Specifications     | Primary Operational Role  | Supported Operations                    |
+-------------------+----------------------------+---------------------------+-----------------------------------------+
| Tier 1: Local CPU | 4 CPU Cores, 8GB RAM       | Dev, Ingestion & RAG Test | Full test suite (315 tests), SQLite     |
| (Baseline)        | Integrated Graphics        | No GPU Pretraining        | FTS5 search, Mock LLM inference, Web UI |
+-------------------+----------------------------+---------------------------+-----------------------------------------+
| Tier 2: Entry GPU | 4-6 CPU Cores, 16GB RAM    | Fast Local Inference &    | 1.07M Transformer pretraining, 50-step  |
| (Current Baseline)| NVIDIA RTX 3050 (4-6GB VRAM| Tokenizer Experiments     | regressions (82K tokens/sec), PyTorch   |
+-------------------+----------------------------+---------------------------+-----------------------------------------+
| Tier 3: High GPU  | 8-16 CPU Cores, 32GB RAM   | Full Scale Pretraining &  | 10M Parameter Transformer training,     |
| (Research Server) | NVIDIA RTX 4090 / A5000    | Dense Embedding Indexing  | Large-batch bilingual pretraining       |
+-------------------+----------------------------+---------------------------+-----------------------------------------+
| Tier 4: Enterprise| 32+ CPU Cores, 128GB+ RAM  | Foundation Model Training | 100M+ Parameter sovereign pretraining,  |
| (Data Center)     | Multi-GPU (A100 / H100)    | High-Concurrency RAG Web  | Distributed Data Parallel (DDP)         |
+-------------------+----------------------------+---------------------------+-----------------------------------------+
```

### 5.3 Clean Virtual Environment Setup

To prevent dependency collisions with global Python packages, establish an isolated virtual environment:

#### On Windows (PowerShell):
```powershell
# Navigate to workspace
cd C:\PROJECTS\LegalMitra

# Create clean virtual environment with Python 3.11
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Upgrade core packaging tools
python -m pip install --upgrade pip setuptools wheel
```

#### On Linux / macOS (Bash / Zsh):
```bash
# Navigate to workspace
cd /path/to/LegalMitra

# Create clean virtual environment
python3.11 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Upgrade packaging tools
pip install --upgrade pip setuptools wheel
```

### 5.4 Step-by-Step Dependency Installation

Install the repository dependencies in editable mode to allow live module development:

```powershell
# 1. Install PyTorch with CUDA 12.1 (for GPU acceleration on Windows/Linux)
# Note: For CPU-only environments, omit the extra index URL
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 2. Install LegalMitra in editable development mode
pip install -e ".[dev]"

# 3. Optional: Install IBM Docling for advanced statutory PDF parsing
pip install docling
```

### 5.5 Verification & Smoke Testing

Execute the following commands to verify environment readiness, FTS5 availability, and invariant integrity:

```powershell
# Verify Python version and PyTorch CUDA availability
python -c "import sys, torch, sqlite3; print(f'Python: {sys.version}'); print(f'PyTorch CUDA Available: {torch.cuda.is_available()}'); print(f'SQLite Version: {sqlite3.sqlite_version}')"

# Run Phase 9 frozen review snapshot verification
python scripts/verify_freeze.py

# Run advocate review package integrity verification
python scripts/verify_review_packages.py

# Execute smoke test across core web and knowledge base modules
pytest tests/test_web_api.py tests/test_knowledge_base.py -v
```

---
""")

    # Part VI
    sections.append("""## Part VI: Configuration & Environment Variables Reference

### 6.1 Configuration Philosophy

LegalMitra follows the Twelve-Factor App methodology for application configuration:
- Zero hardcoded secrets, API tokens, or server addresses in version control.
- Sensible, production-hardened defaults for local development.
- Complete support for `.env` files via `python-dotenv` and explicit system environment variables.
- Strict type validation and bounds checking during application startup.

### 6.2 Complete Environment Variables Matrix

| Variable Name | Type | Default Value | Required? | Purpose & Behavioral Impact |
|:---|:---:|:---:|:---:|:---|
| `LEGALMITRA_ENV` | `str` | `"development"` | No | Environment mode: `"development"`, `"staging"`, or `"production"`. When set to `"production"`, Swagger UI (`/docs`) can be restricted and CORS tightened. |
| `LEGALMITRA_KB_PATH` | `str` | `"data/legalmitra_kb.db"` | No | Absolute or relative file path to the primary SQLite Knowledge Base. Must have read access. |
| `LEGALMITRA_CONV_PATH`| `str` | `"data/conversations.db"` | No | File path to the SQLite User Session and Conversation Store. Requires read/write access. |
| `LEGALMITRA_OFFLINE_EVAL` | `str` | `"0"` | No | Set to `"1"` during offline automated testing. Forces the RAG engine to bypass remote LLM API calls and utilize deterministic mock generation. |
| `NEMOTRON_API_KEY` | `str` | `None` | Conditional | NVIDIA Integrate API key for calling `nvidia/llama-3.1-nemotron-70b-instruct`. Required for live inference mode. |
| `NEMOTRON_BASE_URL` | `str` | `"https://integrate.api.nvidia.com/v1"` | No | Base API endpoint for the Nemotron LLM service. Can be pointed to a local vLLM or Ollama instance. |
| `NEMOTRON_MODEL_NAME` | `str` | `"nvidia/llama-3.1-nemotron-70b-instruct"` | No | Model identifier passed to the OpenAI-compatible completions endpoint. |
| `NEMOTRON_TIMEOUT_SECONDS` | `float` | `60.0` | No | Maximum time in seconds before an outbound LLM HTTP call times out and raises an exception. |
| `RATE_LIMIT_PER_MINUTE` | `int` | `30` | No | Maximum number of `/api/v1/chat` requests allowed per client IP address in a 60-second window. |
| `ALLOWED_ORIGINS` | `str` | `"*"` | No | Comma-separated list of allowed CORS origins for the FastAPI web server. In production, restrict to official domain. |
| `MAX_UPLOAD_SIZE_BYTES` | `int` | `10485760` | No | Maximum permitted file upload size in bytes (10MB default) to prevent memory exhaustion attacks. |
| `LOG_LEVEL` | `str` | `"INFO"` | No | System logging threshold: `"DEBUG"`, `"INFO"`, `"WARNING"`, `"ERROR"`, `"CRITICAL"`. |

### 6.3 Offline vs Online Evaluation Configuration

To switch between offline deterministic testing and live cloud inference:

```powershell
# Enable Offline Evaluation Mode (Fast, zero network calls, 100% reproducible):
$env:LEGALMITRA_OFFLINE_EVAL = "1"
pytest tests/test_rag.py

# Enable Live Production Inference Mode:
$env:LEGALMITRA_OFFLINE_EVAL = "0"
$env:NEMOTRON_API_KEY = "nvapi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
uvicorn legalmitra.web.app:app --host 0.0.0.0 --port 8000
```

### 6.4 Rate Limiting & Security Settings

The built-in sliding window rate limiter protects endpoints against volumetric denial of service:
- Tracks incoming client IP addresses using `X-Forwarded-For` header or direct socket client address.
- When client exceeds `RATE_LIMIT_PER_MINUTE`, the server rejects the request with HTTP 429 and includes a `Retry-After` header indicating remaining wait time in seconds.

---
""")

    # Part VII
    sections.append("""## Part VII: Production Web API Reference

### 7.1 API Architecture & OpenAPI Specification

LegalMitra exposes a production-hardened RESTful API built on FastAPI and Pydantic V2. 
- **Base URL**: `http://localhost:8000/api/v1`
- **Interactive Documentation**: `http://localhost:8000/docs` (Swagger UI) and `http://localhost:8000/redoc` (ReDoc)
- **Content Type**: `application/json; charset=utf-8`

### 7.2 System Probes (`/api/v1/health`, `/api/v1/ready`)

#### Liveness Probe: `GET /api/v1/health`
Checks whether the FastAPI application process is alive and responsive.
- **Request**: `GET /api/v1/health`
- **Response Headers**: `Content-Type: application/json`
- **Response Payload (HTTP 200 OK)**:
```json
{
  "status": "healthy",
  "service": "legalmitra-web-api",
  "version": "1.0.0",
  "environment": "development",
  "timestamp": "2026-10-18T22:30:00.000000"
}
```

#### Readiness Probe: `GET /api/v1/ready`
Verifies that underlying SQLite databases (`data/legalmitra_kb.db` and `data/conversations.db`) exist, are accessible, and have valid table structures.
- **Request**: `GET /api/v1/ready`
- **Response Payload (HTTP 200 OK)**:
```json
{
  "status": "ready",
  "knowledge_base": {
    "status": "connected",
    "chunks_count": 1505,
    "sources_count": 59
  },
  "conversation_store": {
    "status": "connected"
  },
  "timestamp": "2026-10-18T22:30:00.000000"
}
```

### 7.3 Legal Chat Engine (`POST /api/v1/chat`)

The primary intelligence endpoint for querying statutory law, procedural guidelines, and judicial precedents.

- **Endpoint**: `POST /api/v1/chat`
- **Headers**:
  - `Content-Type: application/json`
  - `Accept: application/json`

#### Request Schema (`ChatRequest`):
| Field | Type | Required | Description | Constraints |
|:---|:---:|:---:|:---|:---|
| `query` | `str` | Yes | The legal question or proposition | Min 3 chars, max 2000 chars |
| `conversation_id` | `str` | No | Existing session ID to maintain multi-turn context | Valid UUID4 format |
| `act_filter` | `str` | No | Restrict retrieval to a specific Act title | e.g., `"Bharatiya Nagarik Suraksha Sanhita"` |
| `section_filter` | `str` | No | Restrict retrieval to a specific Section reference | e.g., `"Section 482"` |
| `court_filter` | `str` | No | Restrict retrieval to a specific Court | e.g., `"Supreme Court of India"` |
| `limit` | `int` | No | Maximum evidence chunks to retrieve | Default: 4, Min: 1, Max: 10 |

#### Example Request:
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What are the statutory grounds and conditions for anticipatory bail under Section 482 of the Bharatiya Nagarik Suraksha Sanhita, 2023?",
       "act_filter": "Bharatiya Nagarik Suraksha Sanhita",
       "limit": 4
     }'
```

#### Response Schema (`ChatResponse`):
```json
{
  "conversation_id": "8f3b21aa-4c59-4de9-9e87-cb1a293847f1",
  "query": "What are the statutory grounds and conditions for anticipatory bail under Section 482 of the Bharatiya Nagarik Suraksha Sanhita, 2023?",
  "answer": "Under Section 482 of the Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS), when any person has reason to believe that he may be arrested on an accusation of having committed a non-bailable offence, he may apply to the High Court or the Court of Session for a direction that in the event of such arrest, he shall be released on bail.\n\nThe Court takes into account factors including: (i) the nature and gravity of the accusation; (ii) the antecedents of the applicant including whether he has previously undergone imprisonment on conviction; (iii) the possibility of the applicant fleeing from justice; and (iv) whether the accusation has been made with the object of injuring or humiliating the applicant.",
  "citations": [
    "Section 482 of the Bharatiya Nagarik Suraksha Sanhita, 2023",
    "Section 482(1) BNSS",
    "Section 482(2) BNSS"
  ],
  "evidence": [
    {
      "chunk_id": "BNSS-2023-SEC-482-P1",
      "source_id": "IND-ACT-2023-BNSS",
      "act_or_case_title": "The Bharatiya Nagarik Suraksha Sanhita, 2023",
      "provision_or_para_ref": "Section 482",
      "authority_level": "STATUTORY_CENTRAL",
      "verbatim_text": "482. Direction for grant of bail to person apprehending arrest.—(1) When any person has reason to believe that he may be arrested on an accusation of having committed a non-bailable offence, he may apply to the High Court or the Court of Session for a direction that in the event of such arrest, he shall be released on bail; and that Court may, after taking into consideration, inter alia, the following factors, namely:— (i) the nature and gravity of the accusation; (ii) the antecedents of the applicant...",
      "source_url": "https://www.indiacode.nic.in/handle/123456789/21804",
      "effective_date": "2024-07-01",
      "is_synthetic_scaffold": false
    }
  ],
  "evidence_sufficiency": "sufficient",
  "binding_authorities": [
    "The Bharatiya Nagarik Suraksha Sanhita, 2023 (Act No. 46 of 2023)"
  ],
  "persuasive_authorities": [],
  "missing_facts_prompt": null,
  "legal_disclaimer": "LegalMitra is an AI research and evidence retrieval platform. This response is grounded in primary statutory sources but does not constitute formal legal representation or legal opinion under the Advocates Act, 1961. Consult an enrolled advocate for legal advice.",
  "model_used": "nvidia/llama-3.1-nemotron-70b-instruct",
  "latency_seconds": 1.42,
  "timestamp": "2026-10-18T22:30:05.120450"
}
```

### 7.4 Conversation Session Management (`/api/v1/conversations`)

- **List Conversations**: `GET /api/v1/conversations?limit=20&offset=0`
  - Returns paginated list of previous user chat sessions with snippet titles and timestamps.
- **Get Messages**: `GET /api/v1/conversations/{conv_id}/messages`
  - Retrieves chronological transcript of messages exchanged within session `{conv_id}`.
- **Delete Conversation**: `DELETE /api/v1/conversations/{conv_id}`
  - Permanently purges conversation session and all associated messages from `data/conversations.db`.

### 7.5 User & Advocate Feedback Loop (`POST /api/v1/feedback`)

Allows users and enrolled advocates to submit quality evaluations on generated responses to inform continuous retrieval refinement.

- **Endpoint**: `POST /api/v1/feedback`
- **Request Body**:
```json
{
  "conversation_id": "8f3b21aa-4c59-4de9-9e87-cb1a293847f1",
  "query": "What are the statutory grounds and conditions for anticipatory bail under Section 482 of BNSS?",
  "is_helpful": true,
  "feedback_text": "Accurately distinguished Section 482 BNSS from repealed Section 438 CrPC."
}
```
- **Response**: `{"status": "feedback_recorded"}`

### 7.6 HTTP Error Matrix & Status Codes

| HTTP Status | Error Code | Trigger Condition & Remediation |
|:---:|:---|:---|
| `400 Bad Request` | `VALIDATION_ERROR` | Query string is shorter than 3 characters, exceeds 2000 characters, or payload JSON is malformed. |
| `404 Not Found` | `CONVERSATION_NOT_FOUND` | The specified `conversation_id` does not exist in `conversations.db`. |
| `422 Unprocessable`| `SCHEMA_ERROR` | Request body violates Pydantic data type constraints. |
| `429 Too Many Req`| `RATE_LIMIT_EXCEEDED` | Client IP exceeded 30 requests/min. Inspect `Retry-After` header. |
| `500 Server Error` | `INTERNAL_ERROR` | Unhandled runtime exception. Check structured logs in application console. |
| `503 Unavailable` | `DATABASE_UNAVAILABLE` | SQLite database file is locked or inaccessible. |

---
""")

    # Part VIII
    sections.append("""## Part VIII: Database Architecture & Data Storage Reference

### 8.1 Physical Segregation Principle

LegalMitra enforces a strict **Zero-Shared-State Database Architecture**. Rather than storing public legal knowledge and private user conversations in the same SQLite file, the platform partitions them into two physically distinct database files:

```text
+----------------------------------------------------+    +----------------------------------------------------+
|             DATA/LEGALMITRA_KB.DB                  |    |              DATA/CONVERSATIONS.DB                 |
+----------------------------------------------------+    +----------------------------------------------------+
| • Classification : Public / Authoritative Legal KB |    | • Classification : Private / User Session Store    |
| • Access Mode    : Strictly READ-ONLY at Runtime   |    | • Access Mode    : Read-Write                      |
| • Mutation       : Ingestion pipelines only        |    | • Mutation       : Web API endpoints               |
| • Concurrency    : Shared Read Locks (WAL Mode)    |    | • Concurrency    : Fast Write Locks (WAL Mode)     |
| • Security Gate  : Zero client write access        |    | • Security Gate  : Session UUID isolation          |
+----------------------------------------------------+    +----------------------------------------------------+
```

### 8.2 Knowledge Base Schema (`data/legalmitra_kb.db`)

The primary knowledge base contains 1,505 stored chunks and 59 registered sources.

#### 1. Table `sources`: Master metadata registry of primary legal sources.
```sql
CREATE TABLE sources (
    document_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    source_url TEXT,
    source_type TEXT NOT NULL,          -- 'statute', 'judgment', 'notification', etc.
    jurisdiction TEXT NOT NULL,         -- 'IN', 'IN-DL', 'IN-MH', etc.
    court TEXT,                         -- 'Supreme Court of India', 'Delhi High Court', etc.
    document_date TEXT,                 -- Date of enactment or judgment
    effective_date TEXT,                -- Commencement or enforceability date
    is_historical INTEGER DEFAULT 0,    -- 1 if repealed or pre-transition
    is_synthetic_scaffold INTEGER DEFAULT 0, -- 1 if quarantined test scaffold
    repeal_status TEXT DEFAULT 'active',-- 'active', 'repealed', 'partially_repealed'
    checksum TEXT,                      -- SHA-256 digest of original raw document
    verification_status TEXT DEFAULT 'verified',
    metadata_json TEXT                  -- Serialized JSON containing extra attributes
);
CREATE INDEX idx_sources_jurisdiction ON sources(jurisdiction);
CREATE INDEX idx_sources_source_type ON sources(source_type);
CREATE INDEX idx_sources_scaffold ON sources(is_synthetic_scaffold);
```

#### 2. Table `legal_chunks`: Atomic, retrievable legal text fragments.
```sql
CREATE TABLE legal_chunks (
    chunk_id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    doc_type TEXT NOT NULL,             -- 'statute', 'judgment', 'notification'
    act_or_case_title TEXT NOT NULL,
    provision_or_para_ref TEXT NOT NULL,-- e.g., 'Section 482' or 'Paragraph 14'
    hierarchy_level TEXT,               -- 'section', 'subsection', 'ratio', 'obiter'
    section_number TEXT,
    paragraph_number INTEGER,
    jurisdiction TEXT NOT NULL,
    court TEXT,
    document_date TEXT,
    effective_date TEXT,
    is_historical INTEGER DEFAULT 0,
    is_synthetic_scaffold INTEGER DEFAULT 0, -- 1 if quarantined scaffold
    authority_level TEXT NOT NULL,      -- 'CONSTITUTIONAL', 'STATUTORY_CENTRAL', etc.
    content TEXT NOT NULL,              -- Verbatim legal text of the chunk
    metadata_json TEXT,                 -- Serialized JSON containing structural tags
    FOREIGN KEY (source_id) REFERENCES sources(document_id) ON DELETE CASCADE
);
CREATE INDEX idx_chunks_source_id ON legal_chunks(source_id);
CREATE INDEX idx_chunks_scaffold ON legal_chunks(is_synthetic_scaffold);
CREATE INDEX idx_chunks_provision ON legal_chunks(provision_or_para_ref);
CREATE INDEX idx_chunks_authority ON legal_chunks(authority_level);
```

#### 3. Table `cases`: Judicial case metadata and precedent tracking.
```sql
CREATE TABLE cases (
    case_id TEXT PRIMARY KEY,
    court_code TEXT NOT NULL,           -- 'SC' (Supreme Court), 'DHC' (Delhi High Court)
    case_type TEXT NOT NULL,            -- 'W.P.(C)', 'Crl.A.', 'SLP(C)'
    case_number TEXT NOT NULL,
    filing_year INTEGER NOT NULL,
    petitioner_or_appellant TEXT NOT NULL,
    respondent TEXT NOT NULL,
    neutral_citation TEXT,              -- e.g., '2024:DHC:1420'
    institution_date TEXT,
    disposal_date TEXT,
    status TEXT DEFAULT 'disposed',     -- 'disposed', 'pending'
    metadata_json TEXT
);
CREATE INDEX idx_cases_neutral_citation ON cases(neutral_citation);
CREATE INDEX idx_cases_court ON cases(court_code);
```

#### 4. Table `judicial_documents`: Judicial orders, transcripts, and judgment briefs.
```sql
CREATE TABLE judicial_documents (
    document_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL,
    classification TEXT NOT NULL,       -- 'judgment', 'daily_order', 'interim_order'
    procedural_effect TEXT,             -- 'final_disposal', 'interim_stay', 'bail_granted'
    order_or_judgment_date TEXT NOT NULL,
    bench_coram_json TEXT,              -- Array of judges presiding
    verbatim_text TEXT NOT NULL,
    source_url TEXT,
    sha256_hash TEXT NOT NULL,
    is_synthetic_scaffold INTEGER DEFAULT 0,
    verification_status TEXT DEFAULT 'verified',
    metadata_json TEXT,
    FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE
);
CREATE INDEX idx_judicial_docs_case ON judicial_documents(case_id);
CREATE INDEX idx_judicial_docs_scaffold ON judicial_documents(is_synthetic_scaffold);
```

#### 5. Table `hearing_events`: Chronological hearing event timeline.
```sql
CREATE TABLE hearing_events (
    event_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL,
    listing_date TEXT NOT NULL,
    hearing_type TEXT,                  -- 'admission', 'final_arguments', 'bail_hearing'
    presiding_bench TEXT,
    procedural_outcome TEXT,            -- 'adjourned', 'reserved', 'dismissed'
    daily_order_id TEXT,
    next_listing_date TEXT,
    is_cause_list_verified INTEGER DEFAULT 1,
    metadata_json TEXT,
    FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE
);
CREATE INDEX idx_hearing_events_case ON hearing_events(case_id);
CREATE INDEX idx_hearing_events_date ON hearing_events(listing_date);
```

### 8.3 Full-Text Search Virtual Table (`legal_chunks_fts`)

High-performance BM25 lexical search is powered by an SQLite FTS5 external content table synchronized with `legal_chunks`:

```sql
CREATE VIRTUAL TABLE legal_chunks_fts USING fts5(
    chunk_id UNINDEXED,
    act_or_case_title,
    provision_or_para_ref,
    content,
    content='legal_chunks',
    content_rowid='rowid',
    tokenize='unicode61 remove_diacritics 2'
);

-- Automated Triggers for Real-Time FTS5 Synchronization:
CREATE TRIGGER trg_chunks_ai AFTER INSERT ON legal_chunks BEGIN
    INSERT INTO legal_chunks_fts(rowid, chunk_id, act_or_case_title, provision_or_para_ref, content)
    VALUES (new.rowid, new.chunk_id, new.act_or_case_title, new.provision_or_para_ref, new.content);
END;

CREATE TRIGGER trg_chunks_ad AFTER DELETE ON legal_chunks BEGIN
    INSERT INTO legal_chunks_fts(legal_chunks_fts, rowid, chunk_id, act_or_case_title, provision_or_para_ref, content)
    VALUES ('delete', old.rowid, old.chunk_id, old.act_or_case_title, old.provision_or_para_ref, old.content);
END;

CREATE TRIGGER trg_chunks_au AFTER UPDATE ON legal_chunks BEGIN
    INSERT INTO legal_chunks_fts(legal_chunks_fts, rowid, chunk_id, act_or_case_title, provision_or_para_ref, content)
    VALUES ('delete', old.rowid, old.chunk_id, old.act_or_case_title, old.provision_or_para_ref, old.content);
    INSERT INTO legal_chunks_fts(rowid, chunk_id, act_or_case_title, provision_or_para_ref, content)
    VALUES (new.rowid, new.chunk_id, new.act_or_case_title, new.provision_or_para_ref, new.content);
END;
```

### 8.4 User Session & Feedback Schema (`data/conversations.db`)

User sessions, queries, answers, and advocate reviews are stored in `data/conversations.db`:

```sql
CREATE TABLE conversations (
    conversation_id TEXT PRIMARY KEY,
    title TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_bookmarked INTEGER DEFAULT 0,
    session_id TEXT
);
CREATE INDEX idx_conversations_created ON conversations(created_at);

CREATE TABLE messages (
    message_id TEXT PRIMARY KEY,
    conversation_id TEXT NOT NULL,
    role TEXT NOT NULL,                 -- 'user', 'assistant', 'system'
    content TEXT NOT NULL,
    citations_json TEXT,                -- Serialized JSON array of citations
    evidence_json TEXT,                 -- Serialized JSON array of evidence items
    model_used TEXT,                    -- e.g., 'nvidia/llama-3.1-nemotron-70b-instruct'
    latency_seconds REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ON DELETE CASCADE
);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);

CREATE TABLE feedback (
    feedback_id TEXT PRIMARY KEY,
    conversation_id TEXT NOT NULL,
    query TEXT NOT NULL,
    is_helpful INTEGER NOT NULL,        -- 1 for helpful, 0 for unhelpful
    feedback_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id TEXT,
    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ON DELETE CASCADE
);
CREATE INDEX idx_feedback_conversation_id ON feedback(conversation_id);
```

### 8.5 Performance Tuning, Indexes & Integrity Auditing

Both databases are pre-configured with SQLite optimizations:
- **Write-Ahead Logging (WAL)**: `PRAGMA journal_mode = WAL;` enables concurrent readers alongside writers.
- **Synchronous Normal**: `PRAGMA synchronous = NORMAL;` ensures ACID durability without disk IO bottlenecks.
- **Cache Size Optimization**: `PRAGMA cache_size = -64000;` allocates 64MB memory cache for FTS5 index pages.
- **Integrity Verification Command**:
```powershell
python -c "import sqlite3; [print(db, sqlite3.connect(db).execute('PRAGMA integrity_check').fetchall()) for db in ['data/legalmitra_kb.db', 'data/conversations.db']]"
```

---
""")

    return "\n".join(sections)
