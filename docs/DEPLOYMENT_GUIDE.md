# LEGALMITRA: LOCAL STAGING & DEPLOYMENT GUIDE

## 1. Prerequisites

- Python 3.10+ (tested on Python 3.11)
- Modern web browser (Chrome, Edge, Firefox, Safari)
- Optional: NVIDIA NIM API Key (if live cloud LLM inference is desired; falls back gracefully to deterministic Mock Provider if omitted)

---

## 2. Environment Configuration

1. Copy the example environment template:
   ```bash
   cp .env.example .env
   ```
2. Populate the required environment variables:
   ```env
   # LLM Provider Configuration
   NVIDIA_API_KEY=nvapi-...
   NEMOTRON_MODEL=meta/llama-3.2-11b-vision-instruct
   
   # Server Configuration
   LEGALMITRA_HOST=127.0.0.1
   LEGALMITRA_PORT=8000
   ```

---

## 3. Dependency Installation

Install LegalMitra and web runtime dependencies:
```bash
pip install -e .
pip install fastapi uvicorn httpx pytest
```

---

## 4. Starting the Application

Run the server using the production runner:
```bash
python run_server.py
```
Or directly via Uvicorn:
```bash
uvicorn legalmitra.web.app:app --host 127.0.0.1 --port 8000
```

Once started:
- **Landing Page**: Open `http://127.0.0.1:8000/`
- **Interactive Legal Chat**: Open `http://127.0.0.1:8000/chat`
- **API Documentation (Swagger UI)**: Open `http://127.0.0.1:8000/docs`
- **Health Check Endpoint**: Open `http://127.0.0.1:8000/api/v1/health`

---

## 5. Verification & Testing

Execute the test suites to ensure full system integrity:

```bash
# 1. Run all offline unit, quality gate, and freeze tests (104 tests)
python -m pytest -m "not live"

# 2. Run the Web API and UI endpoint tests
python -m pytest tests/test_web_api.py

# 3. Verify the frozen review snapshot integrity
python scripts/verify_freeze.py
```

---

## 6. Backup & Recovery

- **Knowledge Base**: Back up `data/legalmitra_kb.db` (read-only in production).
- **User Conversations**: Back up `data/conversations.db` using standard SQLite snapshot tools:
  ```bash
  sqlite3 data/conversations.db ".backup 'backups/conversations_backup.db'"
  ```
- **Frozen Review Pilot**: `data/03_generated/` and `data/06_review/` are permanently frozen under SHA-256 manifests.

