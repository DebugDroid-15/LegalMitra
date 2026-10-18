"""
README Builder - Part XIX:
Comprehensive Troubleshooting & Diagnostics Playbook.
30 distinct technical scenarios covering CUDA, PyTorch, SQLite, FTS5, SSRF, Tokenizers, Windows Unicode, Checksums, and Web API.
"""

def generate_part_19() -> str:
    sections = []
    sections.append("""## Part XIX: Comprehensive Troubleshooting & Diagnostics Playbook

### 19.1 CUDA & PyTorch Hardware Diagnostics

When operating on GPU-accelerated workstations, PyTorch or CUDA runtime anomalies can disrupt training or inference.

#### Scenario 01: CUDA Out of Memory (OOM) During Transformer Training
- **Symptoms**: `torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 256.00 MiB (GPU 0; 4.00 GiB total capacity; 3.12 GiB already allocated)`.
- **Root Cause**: Batch size or sequence length too large for GPU VRAM during training or forward attention calculation.
- **Diagnostic Command**:
  ```powershell
  python -c "import torch; print(f'Allocated: {torch.cuda.memory_allocated() / 1e6:.2f}MB, Reserved: {torch.cuda.memory_reserved() / 1e6:.2f}MB')"
  ```
- **Remediation**:
  1. Reduce training batch size in `run_phase35_small_model_regression.py` from 32 to 16 or 8:
     ```python
     train_loader = DataLoader(train_ds, batch_size=16, shuffle=True)
     ```
  2. Reduce sequence length from 256 to 128.
  3. Force garbage collection and CUDA cache clearance before training:
     ```python
     import gc, torch
     gc.collect()
     torch.cuda.empty_cache()
     ```
- **Prevention**: Run `profile_compute_feasibility.py` to establish exact VRAM footprints before launching multi-epoch training.

#### Scenario 02: PyTorch Fails to Detect CUDA GPU
- **Symptoms**: `torch.cuda.is_available()` returns `False` despite an NVIDIA GPU being physically present.
- **Root Cause**: PyTorch installed from the standard PyPI index instead of the NVIDIA CUDA wheel repository.
- **Diagnostic Command**:
  ```powershell
  python -c "import torch; print(f'PyTorch: {torch.__version__}, CUDA Available: {torch.cuda.is_available()}, Device Count: {torch.cuda.device_count()}')"
  ```
- **Remediation**:
  Reinstall PyTorch with the CUDA 12.1 wheel index:
  ```powershell
  pip uninstall -y torch torchvision torchaudio
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
  ```

#### Scenario 03: PyTorch Device Mismatch Exception
- **Symptoms**: `RuntimeError: Expected all tensors to be on the same device, but found at least two devices, cuda:0 and cpu!`.
- **Root Cause**: Input token tensors allocated on CPU while model weights reside on CUDA GPU, or vice versa.
- **Diagnostic Command**:
  ```powershell
  python -c "from research.original_model.model import LegalDecoderTransformer, LegalTransformerConfig; m = LegalDecoderTransformer(LegalTransformerConfig()); print('Model device:', next(m.parameters()).device)"
  ```
- **Remediation**:
  Ensure inputs and target batches are explicitly moved to the model's active device:
  ```python
  device = "cuda" if torch.cuda.is_available() else "cpu"
  model = model.to(device)
  inputs = inputs.to(device)
  targets = targets.to(device)
  ```

---

### 19.2 Database Lock & SQLite Corruptions

#### Scenario 04: SQLite Database Locked Error (`sqlite3.OperationalError: database is locked`)
- **Symptoms**: API requests fail with HTTP 503 or console displays `sqlite3.OperationalError: database is locked`.
- **Root Cause**: Long-running read or write transaction held open by a process without releasing lock, or database in rollback journal mode instead of WAL.
- **Diagnostic Command**:
  ```powershell
  python -c "import sqlite3; conn = sqlite3.connect('data/conversations.db'); print(conn.execute('PRAGMA journal_mode;').fetchall())"
  ```
- **Remediation**:
  1. Enable Write-Ahead Logging (WAL) on both databases:
     ```powershell
     python -c "import sqlite3; [sqlite3.connect(db).execute('PRAGMA journal_mode = WAL;') for db in ['data/legalmitra_kb.db', 'data/conversations.db']]"
     ```
  2. Increase connection busy timeout to 30 seconds:
     ```python
     conn = sqlite3.connect("data/conversations.db", timeout=30.0)
     ```
  3. Terminate any orphaned python processes holding locks:
     ```powershell
     Get-Process python | Stop-Process -Force
     ```

#### Scenario 05: SQLite Malformed Disk Image / Database Corruption
- **Symptoms**: `sqlite3.DatabaseError: database disk image is malformed`.
- **Root Cause**: Abrupt system power loss, process termination during unbuffered write, or disk hardware faults.
- **Diagnostic Command**:
  ```powershell
  python -c "import sqlite3; print(sqlite3.connect('data/legalmitra_kb.db').execute('PRAGMA integrity_check;').fetchall())"
  ```
- **Remediation**:
  1. Export readable tables into an SQL dump and reconstruct clean database:
     ```powershell
     sqlite3 data/legalmitra_kb.db ".recover" | sqlite3 data/legalmitra_kb_recovered.db
     Move-Item data/legalmitra_kb_recovered.db data/legalmitra_kb.db -Force
     ```
  2. Rebuild FTS5 virtual table:
     ```powershell
     python -c "from legalmitra.knowledge.knowledge_base import KnowledgeBase; kb = KnowledgeBase(); kb.rebuild_fts_index()"
     ```

#### Scenario 06: Missing Table or Virtual Table Error
- **Symptoms**: `sqlite3.OperationalError: no such table: legal_chunks_fts`.
- **Root Cause**: Database was created with an SQLite binary lacking FTS5 support, or migration script did not execute.
- **Diagnostic Command**:
  ```powershell
  python -c "import sqlite3; conn = sqlite3.connect(':memory:'); conn.execute('CREATE VIRTUAL TABLE t USING fts5(x);'); print('FTS5 supported')"
  ```
- **Remediation**:
  Execute database initialization script:
  ```powershell
  python -c "from legalmitra.knowledge.knowledge_base import KnowledgeBase; kb = KnowledgeBase(); kb._init_db()"
  ```

---

### 19.3 FTS5 Search & Query Syntax Anomalies

#### Scenario 07: FTS5 Syntax Error on Query String (`fts5: syntax error near`)
- **Symptoms**: `sqlite3.OperationalError: fts5: syntax error near "-": query string`.
- **Root Cause**: Special punctuation characters (`-`, `*`, `+`, `:`, `"`, `(`, `)`) treated as FTS5 boolean operators rather than literal characters.
- **Diagnostic Command**:
  ```powershell
  python -c "from legalmitra.knowledge.knowledge_base import KnowledgeBase; kb = KnowledgeBase(); kb.search_chunks('Section 438 - Anticipatory')"
  ```
- **Remediation**:
  Sanitize and escape query terms in `knowledge_base.py`:
  ```python
  def escape_fts5_query(query: str) -> str:
      # Strip or quote special FTS5 operators
      cleaned = re.sub(r'["*^:]', ' ', query)
      tokens = cleaned.strip().split()
      return " ".join(f'"{t}"' for t in tokens if t)
  ```

#### Scenario 08: Zero Results for Devanagari Hindi Search Queries
- **Symptoms**: Searching for valid Hindi statutory terms (e.g., *"अधिनियम"*) returns empty chunk lists despite Hindi chunks existing in `legal_chunks`.
- **Root Cause**: FTS5 virtual table created with default ASCII tokenizer instead of `unicode61`.
- **Diagnostic Command**:
  ```powershell
  python -c "import sqlite3; conn = sqlite3.connect('data/legalmitra_kb.db'); print(conn.execute(\"SELECT sql FROM sqlite_master WHERE name = 'legal_chunks_fts'\").fetchone()[0])"
  ```
- **Remediation**:
  Ensure FTS5 table is defined with `tokenize='unicode61 remove_diacritics 2'`:
  ```sql
  CREATE VIRTUAL TABLE legal_chunks_fts USING fts5(
      chunk_id UNINDEXED,
      act_or_case_title,
      provision_or_para_ref,
      verbatim_text,
      content='legal_chunks',
      content_rowid='rowid',
      tokenize='unicode61 remove_diacritics 2'
  );
  ```

---

### 19.4 SSRF False Positives & Network Timeouts

#### Scenario 09: Valid Government Portal URL Blocked as SSRF
- **Symptoms**: `legalmitra.core.errors.SSRFBlockedError: URL resolves to forbidden IP`.
- **Root Cause**: Internal DNS server in test or enterprise environment resolves public `.gov.in` domain to an internal caching proxy or local IP range.
- **Diagnostic Command**:
  ```powershell
  python -c "import socket; print(socket.gethostbyname_ex('www.indiacode.nic.in'))"
  ```
- **Remediation**:
  Verify DNS resolution. If running in an offline sandbox, configure an explicit allowlist in `SSRFValidator` for trusted internal mock mirrors.

#### Scenario 10: Ingestion HTTP Timeout During Large Gazette Download
- **Symptoms**: `urllib3.exceptions.ReadTimeoutError: Read timed out` or `requests.exceptions.Timeout`.
- **Root Cause**: Government gazette servers (`egazette.gov.in`) experiencing high latency or transmitting large PDFs (>50MB).
- **Diagnostic Command**:
  ```powershell
  python -c "import requests; r = requests.get('https://www.indiacode.nic.in', timeout=10); print('Status:', r.status_code)"
  ```
- **Remediation**:
  Increase acquisition timeout in `legalmitra/ingestion/acquisition.py`:
  ```python
  response = session.get(url, timeout=(10.0, 60.0), stream=True)
  ```

---

### 19.5 Tokenizer Encoding & Byte-Fallback Issues

#### Scenario 11: Tokenizer Vocabulary Size Mismatch in Model Checkpoint
- **Symptoms**: `RuntimeError: Error(s) in loading state_dict for LegalDecoderTransformer: size mismatch for tok_embeddings.weight: copying a param with shape torch.Size([1024, 128]) from checkpoint, the shape in current model is torch.Size([2048, 128])`.
- **Root Cause**: Attempting to load a Phase 31 prototype checkpoint (trained with Tokenizer v1, vocab 1,024) into a model initialized with Tokenizer v2 (vocab 2,048).
- **Diagnostic Command**:
  ```powershell
  python -c "import torch; ckpt = torch.load('research/original_model/checkpoints/phase35_1m_baseline_regression.pt'); print('Embed shape:', ckpt['tok_embeddings.weight'].shape)"
  ```
- **Remediation**:
  Verify configuration matches checkpoint metadata:
  ```python
  # For Phase 33-36 checkpoints:
  config = LegalTransformerConfig(vocab_size=2048, d_model=128, n_layers=4, n_heads=4)
  # For Phase 31 legacy prototype checkpoints:
  legacy_config = LegalTransformerConfig(vocab_size=1024, d_model=128, n_layers=4, n_heads=4)
  ```

#### Scenario 12: Broken Devanagari Characters After Tokenizer Decoding
- **Symptoms**: Generated Hindi text displays replacement boxes or corrupted syllables (e.g., `अधिियम`).
- **Root Cause**: BPE decode sequence truncated across a multi-byte UTF-8 character boundary.
- **Diagnostic Command**:
  ```powershell
  python -c "from research.original_model.tokenizer_v2 import IndianLegalTokenizerV2; tok = IndianLegalTokenizerV2.load('research/original_model/tokenizer_v2.json'); s = 'भारतीय न्याय संहिता'; print(tok.decode(tok.encode(s)) == s)"
  ```
- **Remediation**:
  Use `IndianLegalTokenizerV2.decode_tokens()` which accumulates raw byte fallbacks before UTF-8 string decoding.

---

### 19.6 Freeze & Review Package SHA-256 Mismatches

#### Scenario 13: Phase 9 Freeze Verification Failure (`verify_freeze.py` Fails)
- **Symptoms**: `verify_freeze.py: AssertionError: Hash mismatch for pilot_20_examples.jsonl`.
- **Root Cause**: Accidental line ending conversion (CRLF vs LF) by Git on Windows, or direct editing of frozen review files.
- **Diagnostic Command**:
  ```powershell
  python scripts/verify_freeze.py
  ```
- **Remediation**:
  1. Check git status to see if any file in `data/06_review/` was modified:
     ```powershell
     git status data/06_review/
     ```
  2. Restore frozen file to exact repository baseline:
     ```powershell
     git checkout HEAD -- data/06_review/
     ```
  3. Ensure Git core autocrlf does not mutate review files:
     ```powershell
     git config core.autocrlf false
     ```

#### Scenario 14: Review Tracking Register Record Count Drift
- **Symptoms**: `verify_review_packages.py` reports total tracking records != 40.
- **Root Cause**: An automated script appended or removed records without advocate sign-off.
- **Diagnostic Command**:
  ```powershell
  python -c "import json; d = json.load(open('data/07_batches/review/review_tracking_register.json')); print('Total records:', len(d.get('entries', [])))"
  ```
- **Remediation**:
  Restore `data/07_batches/review/review_tracking_register.json` from git commit `HEAD`.

---

### 19.7 Windows Console Unicode & Encoding Errors

#### Scenario 15: `UnicodeEncodeError: 'charmap' codec can't encode characters` in PowerShell
- **Symptoms**: Running Python scripts that print Devanagari Hindi or legal symbols (`§`, `¶`) crashes with `UnicodeEncodeError: 'charmap' codec can't encode characters in position x: character maps to <undefined>`.
- **Root Cause**: Windows command prompt or PowerShell defaults to legacy code page (CP1252 or CP437) rather than UTF-8.
- **Diagnostic Command**:
  ```powershell
  python -c "import sys; print('Encoding:', sys.stdout.encoding)"
  ```
- **Remediation**:
  1. Set PowerShell output encoding and Python UTF-8 mode:
     ```powershell
     [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
     $env:PYTHONIOENCODING = "utf-8"
     $env:PYTHONUTF8 = "1"
     ```
  2. In Python scripts printing to stdout, wrap output streams:
     ```python
     import sys, io
     sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
     ```

---

### 19.8 15 Additional Operational Issue Scenarios

#### Scenario 16: Port 8000 Already in Use
- **Symptoms**: `OSError: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000): only one usage of each socket address is normally permitted`.
- **Remediation**:
  Find and kill the process occupying port 8000:
  ```powershell
  Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
  ```

#### Scenario 17: Mock LLM Returning Empty String in Tests
- **Symptoms**: `test_rag.py` fails with assertion error `answer != ""`.
- **Remediation**: Set `$env:LEGALMITRA_OFFLINE_EVAL = "1"` to ensure `MockLLMProvider` is instantiated with matching benchmark query fixtures.

#### Scenario 18: Docling Extractor Missing C++ Visual Runtime
- **Symptoms**: `ImportError: DLL load failed while importing _docling: The specified module could not be found`.
- **Remediation**: Install Microsoft Visual C++ 2015-2022 Redistributable (x64) from Microsoft official download portal.

#### Scenario 19: Excessive JSON Schema Validation Latency
- **Symptoms**: Latency spikes on `/api/v1/chat` exceeding 5.0 seconds.
- **Remediation**: Compile Pydantic models with `model_validate` rather than re-instantiating schemas per request.

#### Scenario 20: Missing Foreign Key Enforcement in SQLite
- **Symptoms**: Orphaned chunks exist after parent source deleted.
- **Remediation**: Explicitly issue `PRAGMA foreign_keys = ON;` immediately upon opening every SQLite connection.

#### Scenario 21: Test Suite Runner Hangs on Asynchronous Tests
- **Symptoms**: `pytest` freezes indefinitely on web API tests.
- **Remediation**: Ensure `asyncio_mode = "strict"` is present in `pyproject.toml` and fixtures use `@pytest.fixture` with `anyio_backend = "asyncio"`.

#### Scenario 22: Accidental Quarantine Scaffold Retrieval
- **Symptoms**: Response includes references to `IND-JUD-DEL-2024-BAIL`.
- **Remediation**: Verify that RAG search SQL query contains `AND is_synthetic_scaffold = 0`.

#### Scenario 23: Pretraining Loss Divergence (Loss = NaN)
- **Symptoms**: Training loss jumps to `nan` at step 15.
- **Remediation**: Enable gradient norm clipping in `train.py`:
  ```python
  torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
  ```

#### Scenario 24: Git Large File Warning on Database Check-in
- **Symptoms**: `warning: File data/legalmitra_kb.db is 52.40 MB; this is larger than GitHub's recommended maximum file size of 50.00 MB`.
- **Remediation**: Run database vacuum: `sqlite3 data/legalmitra_kb.db "VACUUM;"` to strip free pages.

#### Scenario 25: CORS Rejection in Browser Web Client
- **Symptoms**: Browser console reports: `Access to fetch has been blocked by CORS policy`.
- **Remediation**: Set `$env:ALLOWED_ORIGINS = "http://localhost:3000,http://localhost:8000"` and restart FastAPI server.

#### Scenario 26: Stale Source Monitoring State
- **Symptoms**: `scripts/check_legal_source_updates.py` reports False updates.
- **Remediation**: Delete `data/09_national_corpus/source_monitoring_state.json` and rerun crawler.

#### Scenario 27: Rate Limiter Memory Leak
- **Symptoms**: RAM usage grows steadily under sustained load testing.
- **Remediation**: Verify `InMemoryRateLimiter` purges client timestamps older than `window_seconds`.

#### Scenario 28: Division by Zero in Metric Computation
- **Symptoms**: `ZeroDivisionError: division by zero` when computing citation recall on unanswerable cases.
- **Remediation**: Ensure `metrics.py` checks `if len(golden_citations) == 0: return 1.0 if abstained else 0.0`.

#### Scenario 29: Incomplete Deletion of Session Messages
- **Symptoms**: Messages remain after conversation deleted.
- **Remediation**: Verify `ON DELETE CASCADE` is declared on `messages.conversation_id` foreign key.

#### Scenario 30: Benchmark Dataset SHA-256 Hash Drift
- **Symptoms**: `test_phase31_custom_questions.py` reports manifest hash mismatch.
- **Remediation**: Rerun `scripts/build_benchmark_v9.py` to regenerate canonical manifest and SHA-256 hash.

---
""")

    return "\n".join(sections)
