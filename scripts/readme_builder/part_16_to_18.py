"""
README Builder - Part XVI to Part XVIII:
- Part XVI: Security, Privacy & Compliance Architecture
- Part XVII: Automated Testing & Continuous Verification Reference
- Part XVIII: Operational Runbooks & Developer Workflows
"""

def generate_part_16_to_18() -> str:
    sections = []

    # Part XVI
    sections.append("""## Part XVI: Security, Privacy & Compliance Architecture

### 16.1 Threat Modeling & Adversarial Defense

LegalMitra operates in an environment where legal integrity, adversarial prompt injection, and data confidentiality are paramount. In Phase 30, a comprehensive Red-Team validation was executed across 7 attack vectors:

```text
+----------------------------------------------------------------------------------------------------------------------+
|                                     LEGALMITRA SECURITY & THREAT MITIGATION MATRIX                                   |
+-------------------+----------------------------+------------------------------------+--------------------------------+
| Threat Vector     | Attack Methodology         | Security Impact                    | Defense / Mitigation Mechanism |
+-------------------+----------------------------+------------------------------------+--------------------------------+
| Server-Side       | Outbound HTTP fetch to     | Cloud metadata exfiltration,       | SSRFValidator: DNS resolution, |
| Request Forgery   | 169.254.169.254, internal  | port scanning, private network     | loopback/private IP rejection, |
| (SSRF)            | loopback (127.0.0.1)       | compromise                         | hop-by-hop redirect audit      |
+-------------------+----------------------------+------------------------------------+--------------------------------+
| Adversarial RAG   | Prompt injection in query; | Jailbreak system prompts, bypass   | Strict role separation, prompt |
| Injection         | "Ignore legal statutes"    | disclaimers, hallucinate laws      | hardening, negative constraint |
+-------------------+----------------------------+------------------------------------+--------------------------------+
| Denial of Service | Rapid-fire API queries;    | Process starvation, SQLite lock    | Sliding window rate limiter    |
| (DoS / Resource)  | giant JSON payloads (100MB)| exhaustion, disk fill              | (30 req/min), 64KB input cap   |
+-------------------+----------------------------+------------------------------------+--------------------------------+
| SQL Injection     | Tainted query strings;     | Knowledge base corruption,         | Parameterized SQLite queries,  |
|                   | `OR 1=1; DROP TABLE`       | data exfiltration                  | strict FTS5 query escape sanit |
+-------------------+----------------------------+------------------------------------+--------------------------------+
| Child Identity    | Queries citing POCSO       | Statutory violation of Section     | Automated POCSO Redaction      |
| Disclosure        | victims by name            | 33(7) POCSO & Sec 228A IPC/BNS     | Engine (anonymization filter)  |
+-------------------+----------------------------+------------------------------------+--------------------------------+
```

### 16.2 SSRF Protection & Hop-by-Hop Redirect Inspection

Outbound document acquisition (`legalmitra/core/security.py`) employs an airtight SSRF defense engine:
1. **URL Scheme Enforcement**: Only `http://` and `https://` schemes permitted. `file://`, `gopher://`, `ftp://` rejected immediately.
2. **DNS Resolution & IP Pinning**: Resolves hostname to all underlying IPv4 and IPv6 socket addresses before opening connections.
3. **Blacklisted IP Ranges**:
   - Loopback: `127.0.0.0/8`, `::1`
   - Private RFC 1918: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`
   - Link-Local & Cloud Metadata: `169.254.0.0/16` (Blocks AWS/GCP/Azure instance metadata endpoints), `fe80::/10`
   - Carrier-Grade NAT: `100.64.0.0/10`
4. **Hop-by-Hop Redirect Validation**: If a server responds with an HTTP 301/302/307 redirect, the target redirect URL is recursively validated. This prevents attackers from bypassing SSRF filters via an external server redirecting to `169.254.169.254`.

### 16.3 Rate Limiting, Payload Capping & Injection Prevention

- **Sliding-Window Rate Limiting**: The `InMemoryRateLimiter` enforces a 30-request-per-minute ceiling per IP address.
- **Payload Size Capping**: Request bodies sent to `/api/v1/chat` are hard-capped at 64KB, and individual query strings are bounded between 3 and 2,000 characters.
- **SQL / FTS5 Parameterization**: All database lookups utilize SQLite parameterized queries (`?`). Full-text search queries undergo token cleaning and operator escaping, preventing FTS5 syntax injection attacks (e.g., mismatched quotes or malicious boolean operators).

### 16.4 Privacy Compliance & POCSO Redaction Engine

Under Section 33(7) of the Protection of Children from Sexual Offences Act, 2012 (POCSO) and Section 72 of the Bharatiya Nyaya Sanhita, 2023 (formerly Section 228A IPC), disclosing the identity of a victim of sexual offenses or child abuse is a criminal offense.
- **POCSO Redaction Filter**: When indexing judicial judgments or answering sensitive factual queries, the system scans for victim names, parental affiliations, and identifying addresses.
- **Anonymization**: Replaces sensitive identifiers with standardized legal pseudonyms (*"Victim X"*, *"Child A"*, *"Prosecutrix P"*), preserving legal jurisprudence while guaranteeing absolute privacy compliance.

### 16.5 Immutable Audit Logging & Telemetry

Every request, query execution, rate limit trigger, and security exception is recorded with structured JSON telemetry:
- Client IP (hashed in production logs for privacy).
- Conversation session ID.
- Exact latency breakdown (retrieval time vs generation time).
- Tokens generated and model identifier.

---
""")

    # Part XVII
    sections.append("""## Part XVII: Automated Testing & Continuous Verification Reference

### 17.1 Test Strategy & Pytest Architecture

Testing in LegalMitra is organized into hierarchical tiers: unit tests, integration tests, adversarial security tests, freeze invariant checks, and regression suites.
- **Test Runner**: `pytest` 7.4.3+ with `pytest-asyncio` (strict mode) and `pytest-cov`.
- **Configuration**: Managed in `pyproject.toml`.
- **Baseline Test Result (Phase 36 Verified)**:
  - **315 Passed**
  - **0 Failed**
  - **2 Deselected** (Live network tests deselected in standard non-live mode)
  - **Execution Time**: ~48 seconds on standard multi-core hardware.

### 17.2 Inventory of Test Suites (38 Test Modules)

The test harness covers every layer of the architecture:

```text
tests/
├── conftest.py                          # Global pytest fixtures, mock clients & test databases
├── test_adversarial_quality_gate.py    # 12 tests: Jailbreaks, prompt injections, false premises
├── test_corpus_pipeline.py              # 10 tests: Statutory parsing, extraction, token counts
├── test_corpus_scale.py                 # 11 tests: FTS5 query scaling, large chunk performance
├── test_deduplication.py                # 3 tests: SHA-256 deduplication & content hash checks
├── test_end_to_end_pipeline.py          # 1 test: Complete PDF -> FTS5 -> RAG -> Chat flow
├── test_extraction.py                   # 5 tests: PDF layout, Docling fallbacks, error handling
├── test_generation.py                   # 15 tests: Prompt formatting, legal schemas, Pydantic gates
├── test_grounding.py                    # 3 tests: Claim grounding, citation support contracts
├── test_knowledge_base.py               # 7 tests: SQLite schema, FTS5 sync triggers, CRUD ops
├── test_live_nemotron.py                # 2 tests: Live NVIDIA API tests (deselected in non-live)
├── test_nemotron_interface.py           # 4 tests: Mock LLM client, retry policy, error mappings
├── test_normalization.py                # 3 tests: Unicode NFKC, Devanagari cleaners, whitespace
├── test_partitioner.py                  # 2 tests: Source-grouped split integrity, zero-leakage
├── test_phase9_freeze.py                # 3 tests: Bitwise invariant tests for Phase 9 frozen files
├── test_pilot_20.py                     # 8 tests: Pilot 20 review sheet schemas & integrity
├── test_quality_gate.py                 # 5 tests: Pre-indexing and post-retrieval Quality Gates
├── test_rag.py                          # 6 tests: RAG search, sufficiency scoring, abstention
├── test_registry.py                     # 6 tests: 7-State FSM transitions and registry audits
├── test_review_import.py                # 5 tests: Advocate review package import and validation
├── test_review_operations.py            # 11 tests: Review tracking register updates and states
├── test_review_package.py               # 4 tests: Package A and B schemas and hashes
├── test_schemas.py                      # 9 tests: Pydantic model serialization & validations
├── test_validation.py                   # 3 tests: General validation helpers and assert macros
├── test_web_api.py                      # 10 tests: FastAPI routes, session store, rate limits
└── test_phase12_pipeline.py to test_phase36_validation.py # 165 regression validation tests
```

### 17.3 Freeze Integrity Test Suite (`verify_freeze.py`)

A non-negotiable invariant across all phases: the **6 Phase 9 frozen review artifacts** must remain byte-for-byte identical to their locked cryptographic signatures:

```powershell
python scripts/verify_freeze.py
```

#### Verified Invariants:
1. `pilot_20_examples.jsonl`: Exactly 44,542 bytes | SHA256: `e01b22f50f36c3927b595ecd03e2258c6889f299e6394644b2cd4cb359ffa953`
2. `pilot_20_manifest.json`: Exactly 21,705 bytes | SHA256: `9da3801fdc79514987dcd91ffacc81372ab5412a93002ddfd3d9c1c7050369a4`
3. `pilot_20_review_sheet.csv`: Exactly 35,396 bytes | SHA256: `6f519165d45bac465e2c25de20369b74d136543307a49ecb84559f68a7dadcab`
4. `pilot_20_source_bundle.json`: Exactly 62,870 bytes | SHA256: `3cf555e96743ece27b0e22d954d6535cea8a51cc9242c471416b9f46fb031f10`
5. `pilot_20_open_issues.md`: Exactly 7,903 bytes | SHA256: `0b82c4f6df0d9b6c755c6bf15ffb582c07cc6788a28d8ff610de4b645251f45e`
6. `PHASE8_OPEN_LEGAL_ISSUES_REGISTER.md`: Exactly 15,514 bytes | SHA256: `e5966e245c15f6cb96e48d57ede8e81be8a89ebe3aa843098afc961e86c2c508`
- All 20 records remain strictly in `pending_legal_review` status.
- Zero references to quarantined scaffold `IND-JUD-DEL-2024-BAIL`.

### 17.4 Review Package Verification Suite (`verify_review_packages.py`)

Validates Package A (Pilot 20 frozen snapshot), Package B (Batch 01 candidate expansion), and the master review tracking register:

```powershell
python scripts/verify_review_packages.py
```
- Package A: 100% byte-for-byte verified (20 records).
- Package B: 100% verified (20 records).
- Master Tracking Register: Exactly 40 records, all strictly `pending_legal_review`.

### 17.5 Reproducing the Complete Test Suite (315 Passing Tests)

To reproduce the verified baseline locally:

```powershell
# Run the entire non-live test suite with quiet progress output
pytest -q

# Run with full verbose output
pytest -v

# Run with coverage report
pytest --cov=legalmitra --cov-report=term-missing
```

---
""")

    # Part XVIII
    sections.append("""## Part XVIII: Operational Runbooks & Developer Workflows

### 18.1 Runbook 1: Ingesting a New Central or State Statute

Follow this procedure to ingest, validate, and index a newly enacted legislative Act:

1. **Acquire Official PDF or Gazette Copy**:
   Download authoritative text directly from official portals (`indiacode.nic.in` or `egazette.gov.in`).
2. **Register Source Candidate in Registry**:
   ```python
   from legalmitra.corpus.source_registry_engine import SourceRegistryEngine
   from legalmitra.knowledge.models import SourceMetadata

   engine = SourceRegistryEngine()
   meta = SourceMetadata(
       source_id="IND-ACT-2024-DPDP",
       official_title="The Digital Personal Data Protection Act, 2023",
       source_type="statute",
       jurisdiction="IN",
       issuing_authority="Parliament of India",
       source_url="https://www.indiacode.nic.in/handle/123456789/21800",
       publication_date="2023-08-11",
       commencement_date="2023-08-11"
   )
   engine.register_source(meta)
   ```
3. **Parse and Structure Text**:
   Run the statutory parser to generate structured provision chunks:
   ```powershell
   python -m legalmitra.corpus.legal_parser --source-id "IND-ACT-2024-DPDP" --input-file "data/01_raw/dpdp_act_2023.txt"
   ```
4. **Execute Quality Gate Verification**:
   Verify syntactic schema, content hashing, and deduplication:
   ```powershell
   pytest tests/test_quality_gate.py -k "test_statutory_quality_gate"
   ```
5. **Promote State to Training Eligible**:
   ```powershell
   python -c "from legalmitra.corpus.source_registry_engine import SourceRegistryEngine; SourceRegistryEngine().transition_state('IND-ACT-2024-DPDP', 'TRAINING_ELIGIBLE', 'Audited under Sec 52(1)(q)', 'admin')"
   ```

### 18.2 Runbook 2: Indexing High Court / Supreme Court Precedents

To index a landmark judicial ruling:
1. Obtain certified copy or official neutral citation transcript (`[Year]:[Court]:[Number]`).
2. Extract case header: Bench coram size, presiding author judge, date of decision.
3. Segregate *ratio decidendi* paragraphs from factual background.
4. Insert into `cases` table and chunk ratio paragraphs into `legal_chunks` with `authority_level = 'JUDICIAL_HIGH_COURT'`.
5. Update FTS5 virtual table and execute regression tests:
   ```powershell
   pytest tests/test_phase17_caselaw.py tests/test_phase21_judicial.py
   ```

### 18.3 Runbook 3: Executing Evaluation Benchmarks

To run the complete Benchmark v9 evaluation suite and diagnose failures:

```powershell
# 1. Run offline benchmark evaluation
$env:LEGALMITRA_OFFLINE_EVAL = "1"
python scripts/audit_custom_questions.py

# 2. View generated evaluation results and failure attribution
python -c "import json; d = json.load(open('data/20_evaluation/evaluation_results_v9.json')); print(f'Passed: {d[\"passed\"]}/{d[\"total\"]}')"
```

### 18.4 Runbook 4: Pretraining & Benchmarking the Original Model

To reproduce the 1.07M parameter model training run:

```powershell
# 1. Verify Dataset Manifest v4 integrity
python scripts/build_phase34_datasets.py

# 2. Execute 50-step regression pretraining run
python scripts/run_phase35_small_model_regression.py

# 3. Verify reproduction of validation loss (5.6607)
python scripts/reproduce_phase35_small_model_regression.py
```

### 18.5 Runbook 5: Generating & Verifying Advocate Review Packages

When preparing candidate examples for external advocate legal review:

```powershell
# 1. Generate Batch 01 review bundle
python scripts/build_batch_01_bundle.py

# 2. Verify all review packages remain strictly pending review
python scripts/verify_review_packages.py

# 3. Print review tracking summary
python scripts/review_status_summary.py
```

### 18.6 Runbook 6: Database Maintenance & Vacuum Procedures

Periodically optimize SQLite knowledge base and conversation storage:

```powershell
python -c "
import sqlite3
for db in ['data/legalmitra_kb.db', 'data/conversations.db']:
    conn = sqlite3.connect(db)
    conn.execute('PRAGMA optimize;')
    conn.execute('VACUUM;')
    print(f'Optimized and vacuumed {db}')
    conn.close()
"
```

---
""")

    return "\n".join(sections)
