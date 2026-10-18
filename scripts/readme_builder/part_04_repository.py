"""
README Builder - Part IV:
Exhaustive Repository Anatomy & Module Reference.
Detailed technical inspection and documentation of every subpackage and module:
- legalmitra.caselaw
- legalmitra.core
- legalmitra.corpus
- legalmitra.dataset
- legalmitra.evaluation
- legalmitra.extraction
- legalmitra.generation
- legalmitra.ingestion
- legalmitra.knowledge
- legalmitra.llm
- legalmitra.normalization
- legalmitra.rag
- legalmitra.review
- legalmitra.schemas
- legalmitra.temporal
- legalmitra.validation
- legalmitra.web
- research.original_model
- scripts master inventory
- tests master inventory
- data directory structure
"""

import os
from pathlib import Path

def generate_part_04() -> str:
    sections = []
    sections.append("""## Part IV: Exhaustive Repository Anatomy & Module Reference

### 4.1 Package Architecture Overview

The `legalmitra` package represents a production-grade, highly modularized Python architecture engineered according to domain-driven design principles. The codebase contains over 107 distinct Python modules distributed across 17 specialized subpackages, flanked by the `research/` pretraining laboratory, an extensive operational tooling suite in `scripts/`, and an exhaustive test harness in `tests/`.

```text
legalmitra/
├── __init__.py                  # Root package initialization & version metadata
├── caselaw/                     # Judicial precedent intelligence, case graph & identity
│   ├── case_identity.py         # Canonical Indian case citation & neutral citation parser
│   ├── knowledge_graph.py       # Directed acyclic graph of judicial precedent citations
│   ├── precedent.py             # Ratio decidendi vs obiter dicta precedent hierarchy
│   └── __init__.py
├── core/                        # Foundational primitives, enums, security & logging
│   ├── enums.py                 # Core enumerated types (DocType, AuthorityLevel, etc.)
│   ├── errors.py                # Hierarchical domain exception tree
│   ├── hashing.py               # Deterministic SHA-256 and content normalization hashing
│   ├── logging.py               # Structured JSON/text logging engine
│   ├── security.py              # SSRF defense, IP pinning, redirect validator, rate limiter
│   └── __init__.py
├── corpus/                      # National legal universe, discovery & lifecycle engine
│   ├── acquisition_queue.py     # Priority queues for statutory acquisition
│   ├── amendments.py            # Statutory amendment tracking & structural modifications
│   ├── corpus_versioning.py     # Version ledger & snapshot manager for legal corpuses
│   ├── delegated.py             # Subordinate legislation, rules, regulations & orders
│   ├── discovery.py             # Official portal discovery engine (India Code, e-Gazette)
│   ├── discovery_engine.py      # Automated discovery agent for missing state/central laws
│   ├── impact_analyzer.py       # Amendment impact analysis across interconnected acts
│   ├── inventory.py             # Physical file & chunk inventory verification
│   ├── judicial_registry.py     # High Court & Supreme Court registry registry tracker
│   ├── legal_diff.py            # Word/provision-level legal textual diffing engine
│   ├── legal_parser.py          # Hierarchical statutory structure parser
│   ├── legal_universe.py        # Master universe registry of all central & state laws
│   ├── procedural_events.py     # Procedural event tracking for judicial proceedings
│   ├── quality_engine.py        # Automated quality assessment for raw legal text
│   ├── secure_acquisition_engine.py # Network acquisition with SSRF & anti-scraping blocks
│   ├── source_discovery.py      # Automated crawler & metadata extractor
│   ├── source_monitor.py        # Web monitor detecting gazette publication updates
│   ├── source_registry_engine.py# FSM state machine manager for source lifecycle
│   ├── state_registry.py        # 28 States + 8 UTs legislative portal registry
│   ├── taxonomy.py              # 15-Domain Indian legal subject-matter taxonomy
│   ├── temporal_versioning.py   # Point-in-time statutory timeline generator
│   ├── training_exporter.py     # Pretraining corpus exporter with source-grouped splits
│   └── __init__.py
├── dataset/                     # Pretraining dataset generation & partitioning
│   ├── jsonl_exporter.py        # High-performance JSONL dataset streaming
│   ├── partitioner.py           # Source-grouped, zero-leakage dataset partitioner
│   ├── pipeline.py              # End-to-end dataset build & audit pipeline
│   └── __init__.py
├── evaluation/                  # Benchmark execution & failure attribution
│   ├── dataset.py               # Benchmark manifest & evaluation case schemas
│   ├── failure_attribution.py   # 15-Category automated failure diagnosis & triage
│   ├── metrics.py               # Citation recall, claim support & faithfulness metrics
│   ├── models.py                # Evaluation Pydantic data contracts
│   ├── runner.py                # High-concurrency evaluation harness
│   └── __init__.py
├── extraction/                  # Multi-format document text extraction
│   ├── base.py                  # Abstract base extractor interface
│   ├── dispatcher.py            # MIME-type document extraction dispatcher
│   ├── docling_extractor.py     # IBM Docling integration for complex statutory PDFs
│   ├── failure_reporter.py      # Extraction error logging & quarantined document dumps
│   ├── text_extractor.py        # Plaintext & Unicode legal document extractor
│   └── __init__.py
├── generation/                  # Prompt engineering & synthesis validation
│   ├── exporter.py              # Formatted export of generated legal Q&A pairs
│   ├── orchestrator.py          # End-to-end synthesis coordinator
│   ├── prompts.py               # Hardened constitutional legal prompt templates
│   ├── schemas.py               # Generation validation schemas
│   ├── validator.py             # Post-generation legal accuracy validator
│   └── __init__.py
├── ingestion/                   # Ingestion pipelines for central, state & caselaw
│   ├── acquisition.py           # Rate-limited document fetcher with caching
│   ├── central_acts.py          # Phase 1-15 Central Acts ingestion pipeline
│   ├── central_acts_phase16.py  # Phase 16 expanded Central Acts pipeline
│   ├── central_acts_phase20.py  # Phase 20 legislative batch pipeline
│   ├── central_acts_phase24.py  # Phase 24 priority central statutes
│   ├── corpus_ingestor.py       # Generic legal corpus ingestion coordinator
│   ├── delhi_high_court_phase26.py # Delhi High Court judgment ingestion
│   ├── ingestor.py              # Base ingestion interface & database writer
│   ├── landmark_judgments.py    # Supreme Court landmark rulings (Kesavananda, etc.)
│   ├── landmark_judgments_phase21.py # Phase 21 expanded judicial batch
│   ├── landmark_judgments_phase24.py # Phase 24 commercial & constitutional cases
│   ├── national_corpus_pipeline.py # Unified national corpus batch executor
│   ├── registry.py              # Ingested source registration & checksum tracking
│   ├── state_acts.py            # State legislation ingestion (Delhi, Maharashtra)
│   └── __init__.py
├── knowledge/                   # SQLite + FTS5 knowledge base storage engine
│   ├── knowledge_base.py        # KnowledgeBase SQLite repository & FTS5 search
│   ├── models.py                # LegalChunk and SourceMetadata data models
│   └── __init__.py
├── llm/                         # Language model provider abstractions
│   ├── interface.py             # Abstract LLM provider interface
│   ├── mock_provider.py         # Deterministic offline mock provider for testing
│   ├── nemotron.py              # NVIDIA Llama-3.1-Nemotron-70B-Instruct client
│   └── __init__.py
├── normalization/               # Text cleaning & legal structural normalization
│   ├── clean_text.py            # Unicode NFKC cleaning, quote normalization, whitespace
│   ├── judgment_normalizer.py   # Judicial judgment structural partitioner
│   ├── normalizer.py            # General legal text normalizer
│   ├── statute_normalizer.py    # Statutory hierarchy normalizer
│   └── __init__.py
├── rag/                         # Evidential retrieval-augmented generation engine
│   ├── engine.py                # Grounded RAG orchestrator with abstention logic
│   ├── evaluator.py             # Grounding evaluation & evidence sufficiency scoring
│   ├── prompts.py               # RAG prompt templates with citation constraints
│   ├── schemas.py               # RAG request, response, and evidence models
│   └── __init__.py
├── review/                      # Advocate review workflow & tracking
│   ├── eligibility.py           # Pre-review automated validation checks
│   ├── import_review.py         # Importer for advocate review packages
│   ├── tracker.py               # ReviewTrackingRegister manager
│   ├── workflow.py              # Advocate review state transition coordinator
│   └── __init__.py
├── schemas/                     # Core Pydantic data contracts
│   ├── case_analysis.py         # Structured case brief & ratio decidendi schema
│   ├── drafting_example.py      # Legal drafting example schema
│   ├── evaluation.py            # Benchmark evaluation schema
│   ├── judgment.py              # Structured judicial judgment schema
│   ├── legal_qa.py              # Grounded legal Q&A schema
│   ├── procedural_guide.py      # Step-by-step procedural compliance schema
│   ├── registry.py              # Source registry schema
│   ├── statute.py               # Hierarchical statute, section, proviso schema
│   └── __init__.py
├── temporal/                    # Point-in-time statutory applicability engine
│   ├── engine.py                # Temporal reasoning, amendment delta & repeal logic
│   └── __init__.py
├── validation/                  # Quality gates & evidential validation
│   ├── deduplication.py         # Content hash & fuzzy deduplication
│   ├── grounding_validator.py   # Claim-to-source grounding verification
│   ├── pydantic_validator.py    # Strict Pydantic schema validation gate
│   ├── quality_gate.py          # 8 Multi-stage quality gates
│   ├── temporal_validator.py    # Temporal consistency & non-retroactivity gate
│   └── __init__.py
└── web/                         # Production FastAPI application & session store
    ├── app.py                   # FastAPI server, route definitions, CORS, rate limits
    ├── schemas.py               # Web API contracts (ChatRequest, ChatResponse, etc.)
    └── store.py                 # SQLite session storage (conversations.db)
```
""")

    # Now let's detail each subpackage with deep class/function breakdowns
    sections.append("""### 4.2 Core Subpackage (`legalmitra.core`)

The `legalmitra.core` subpackage supplies the infrastructural bedrock across the entire platform, providing standardized enumerations, unified domain exceptions, cryptographic hashing functions, structured JSON logging, and network security utilities.

#### `legalmitra/core/enums.py`
- **Module Purpose**: Defines standardized, type-safe Python enumerations representing legal document classifications, authority levels, court jurisdictions, lifecycle states, and review statuses.
- **Key Enumerations**:
  - `DocumentType`: Enumerates legal document families: `STATUTE`, `JUDGMENT`, `NOTIFICATION`, `RULES_REGULATION`, `CIRCULAR`, `ORDINANCE`, `CONSTITUTION`.
  - `AuthorityLevel`: Defines the constitutional hierarchy of legal authority under Indian jurisprudence: `CONSTITUTIONAL` (Supreme Law), `STATUTORY_CENTRAL` (Parliament Acts), `STATUTORY_STATE` (State Legislative Acts), `JUDICIAL_SUPREME_COURT` (Binding nationwide under Art. 141), `JUDICIAL_HIGH_COURT` (Binding within state jurisdiction, persuasive elsewhere), `SUBORDINATE_LEGISLATION` (Rules, regulations, statutory orders), `PERSUASIVE_OTHER`.
  - `LifecycleState`: Represents the 7 stages of the source ingestion FSM: `DISCOVERED`, `REGISTERED`, `ACQUIRED`, `PARSED`, `AUTHENTICITY_VERIFIED`, `RIGHTS_REVIEWED`, `TRAINING_ELIGIBLE`, plus error states `REJECTED` and `QUARANTINED`.
  - `ReviewStatus`: Tracks advocate review progression: `PENDING_LEGAL_REVIEW`, `IN_REVIEW`, `APPROVED_BY_ADVOCATE`, `REJECTED_BY_ADVOCATE`, `QUARANTINED`.
  - `Jurisdiction`: Standard ISO/Indian jurisdiction codes: `IN` (National / Central), `IN-DL` (NCT of Delhi), `IN-MH` (Maharashtra), `IN-KA` (Karnataka), `IN-WB` (West Bengal), `IN-TN` (Tamil Nadu), etc.
- **Public Functions**: None (Pure enumeration definitions).
- **Associated Tests**: `tests/test_schemas.py`.

#### `legalmitra/core/errors.py`
- **Module Purpose**: Establishes a domain-specific exception hierarchy ensuring fine-grained error identification, programmatic recovery, and sanitized user-facing error reporting.
- **Key Classes**:
  - `LegalMitraError(Exception)`: Root base exception for all platform errors.
  - `SecurityError(LegalMitraError)`: Raised on security violations (SSRF, IP spoofing, payload overage).
  - `SSRFBlockedError(SecurityError)`: Raised when a requested URL resolves to private, loopback, link-local, or cloud metadata IP ranges.
  - `RateLimitExceededError(SecurityError)`: Raised when client IP exceeds permitted request rate.
  - `IngestionError(LegalMitraError)`: Raised when document acquisition, reading, or indexing fails.
  - `ExtractionError(IngestionError)`: Raised when parsing or text extraction produces malformed structures.
  - `QuarantineViolationError(LegalMitraError)`: Raised when code attempts to access, index, or train on quarantined scaffold data.
  - `QualityGateError(LegalMitraError)`: Raised when an artifact fails any of the 8 validation quality gates.
  - `GroundingError(LegalMitraError)`: Raised when an LLM answer references unverified claims or hallucinates citations.
  - `TemporalInconsistencyError(LegalMitraError)`: Raised when provisions from conflicting temporal regimes are conflated.
- **Associated Tests**: `tests/test_schemas.py`, `tests/test_phase30_security.py`.

#### `legalmitra/core/hashing.py`
- **Module Purpose**: Provides cryptographic and normalized hashing routines to guarantee bitwise reproducibility, tamper detection, and exact deduplication.
- **Public Functions**:
  - `compute_sha256(data: bytes | str) -> str`: Computes standard hexadecimal SHA-256 digest. If input is string, encodes as UTF-8.
  - `compute_file_sha256(path: Path | str, chunk_size: int = 65536) -> str`: Streams file in 64KB binary blocks to compute SHA-256 without memory spikes on large PDFs or database files.
  - `compute_text_content_hash(text: str) -> str`: Normalizes whitespace (collapsing sequences of whitespace, stripping leading/trailing spaces) and returns hexadecimal SHA-256, ensuring minor layout variations do not create duplicate chunks.
- **Associated Tests**: `tests/test_deduplication.py`, `tests/test_phase9_freeze.py`.

#### `legalmitra/core/logging.py`
- **Module Purpose**: Implements centralized, structured logging configured for local development and cloud observability.
- **Public Classes & Functions**:
  - `LegalMitraFormatter(logging.Formatter)`: Custom formatter supporting human-readable colorized console output or structured JSON output.
  - `get_logger(name: str) -> logging.Logger`: Returns a configured logger instance bound to the `legalmitra` namespace with standardized timestamp, loglevel, module name, and line numbers.
- **Associated Tests**: `tests/conftest.py`.

#### `legalmitra/core/security.py`
- **Module Purpose**: Core network security, SSRF defense, URL inspection, and client request rate limiting.
- **Key Classes & Functions**:
  - `SSRFValidator`: Static inspection engine for outbound HTTP/HTTPS requests.
    - `validate_url(url: str) -> bool`: Verifies URL scheme (only `http` and `https` allowed), resolves host domain to all underlying IPv4/IPv6 addresses, and blocks private ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), loopback (`127.0.0.0/8`, `::1`), link-local (`169.254.0.0/16`), and broadcast.
    - `validate_redirect(from_url: str, to_url: str) -> bool`: Inspects each hop in an HTTP redirect chain, preventing open redirect SSRF attacks.
  - `InMemoryRateLimiter`: Thread-safe, in-memory sliding window rate limiter.
    - `is_allowed(client_id: str, max_requests: int = 30, window_seconds: float = 60.0) -> bool`: Records timestamp of request and determines whether client has exceeded `max_requests` in `window_seconds`.
    - `get_remaining_seconds(client_id: str, window_seconds: float = 60.0) -> float`: Returns time until rate limit window resets.
- **Associated Tests**: `tests/test_phase30_security.py`.
""")

    sections.append("""### 4.3 Ingestion Subpackage (`legalmitra.ingestion`)

The `legalmitra.ingestion` subpackage manages the systematic acquisition, structural extraction, validation, and database insertion of primary legal sources across Central Acts, State Legislation, and High Court / Supreme Court judgments.

#### `legalmitra/ingestion/ingestor.py`
- **Module Purpose**: Defines the abstract base class and common persistence workflows for ingesting legal documents into `data/legalmitra_kb.db`.
- **Key Classes**:
  - `BaseIngestor(ABC)`: Abstract base class requiring implementation of `acquire()`, `parse()`, `validate()`, and `store()`.
  - `StatuteIngestor(BaseIngestor)`: Specialized pipeline for parsing legislative enactments into hierarchical provision chunks (Sections, Subsections, Provisos, Explanations).
  - `JudgmentIngestor(BaseIngestor)`: Specialized pipeline for judicial decisions, extracting case titles, bench composition, citations, issues, ratio decidendi, and operative orders.
- **Database Interaction**: Connects to `data/legalmitra_kb.db`, inserts into `sources`, `legal_chunks`, and updates `legal_chunks_fts`.

#### `legalmitra/ingestion/acquisition.py`
- **Module Purpose**: Network acquisition client for retrieving official gazettes and statutory texts from official portals.
- **Key Classes & Methods**:
  - `LegislationAcquisitionManager`:
    - `fetch_url(url: str, max_size_bytes: int = 10485760) -> bytes`: Executes rate-limited HTTP GET request with SSRF validation, hop-by-hop redirect verification, and payload size capping (10MB default).
    - `cache_document(source_id: str, content: bytes, extension: str) -> Path`: Stores raw acquired artifact in `data/01_raw/` with deterministic naming and computes SHA-256.

#### `legalmitra/ingestion/central_acts.py` & Phase Extensions
- **`central_acts.py`**: Ingestion workflows for initial Phase 1-15 core Central Acts: The Constitution of India, Indian Penal Code, 1860, Code of Criminal Procedure, 1973, Indian Evidence Act, 1872, Bharatiya Nyaya Sanhita, 2023, Bharatiya Nagarik Suraksha Sanhita, 2023, Bharatiya Sakshya Adhiniyam, 2023.
- **`central_acts_phase16.py`**: Ingestion for Phase 16 economic & commercial expansion: Arbitration and Conciliation Act, 1996, Information Technology Act, 2000, Insolvency and Bankruptcy Code, 2016, Companies Act, 2013, Consumer Protection Act, 2019, Negotiable Instruments Act, 1881.
- **`central_acts_phase20.py`**: Ingestion for Phase 20 civil and procedural expansion: Code of Civil Procedure, 1908, Specific Relief Act, 1963, Limitation Act, 1963, Transfer of Property Act, 1882, Indian Contract Act, 1872, Right to Information Act, 2005.
- **`central_acts_phase24.py`**: Ingestion for Phase 24 specialized commercial and labor codes: Commercial Courts Act, 2015, Industrial Relations Code, 2020, Prevention of Money Laundering Act, 2002.

#### `legalmitra/ingestion/state_acts.py`
- **Module Purpose**: Ingestion pipelines for state-level enactments. Implements state portal adapters for NCT of Delhi legislation (e.g., Delhi Rent Act, 1995, Delhi Police Act, 1978) and Maharashtra legislation (e.g., Maharashtra Control of Organised Crime Act, 1999 - MCOCA).

#### `legalmitra/ingestion/landmark_judgments.py` & Phase Extensions
- **`landmark_judgments.py`**: Parses and indexes foundational Supreme Court constitutional bench rulings:
  - *Kesavananda Bharati v. State of Kerala (1973) 4 SCC 225* (Basic Structure Doctrine)
  - *Maneka Gandhi v. Union of India (1978) 1 SCC 248* (Procedure Established by Law & Substantive Due Process)
  - *Justice K.S. Puttaswamy v. Union of India (2017) 10 SCC 1* (Right to Privacy under Article 21)
  - *Navtej Singh Johar v. Union of India (2018) 10 SCC 1* (Decriminalization of Section 377 IPC)
- **`delhi_high_court_phase26.py`**: Specialized extractor for Delhi High Court commercial division and criminal appellate judgments, validating neutral citations (`2024:DHC:xxxx`).

#### `legalmitra/ingestion/national_corpus_pipeline.py`
- **Module Purpose**: Orchestrates batch ingestion across all national sources, coordinating state transitions, quality gate evaluations, deduplication checks, and pretraining manifest updates.
- **Associated Tests**: `tests/test_corpus_pipeline.py`, `tests/test_end_to_end_pipeline.py`.
""")

    sections.append("""### 4.4 Corpus Subpackage (`legalmitra.corpus`)

The `legalmitra.corpus` subpackage constitutes the largest subsystem in LegalMitra (22 modules), governing source discovery, inventory reconciliation, legal diffing, taxonomy mapping, amendment tracking, quality analysis, and pretraining dataset exports.

#### `legalmitra/corpus/source_registry_engine.py`
- **Module Purpose**: Implements the finite state machine (FSM) controlling source transitions from `DISCOVERED` through `TRAINING_ELIGIBLE`.
- **Key Classes**:
  - `SourceRegistryEngine`:
    - `register_source(metadata: SourceMetadata) -> SourceRecord`: Registers newly discovered source in `data/09_national_corpus/unified_source_registry.json`.
    - `transition_state(source_id: str, to_state: LifecycleState, reason: str, actor: str) -> SourceRecord`: Enforces legal transition rules (e.g., cannot move from `REGISTERED` to `TRAINING_ELIGIBLE` without passing `AUTHENTICITY_VERIFIED` and `RIGHTS_REVIEWED`).
    - `record_quarantine(source_id: str, reason: str)`: Isolates suspicious or scaffold records.

#### `legalmitra/corpus/legal_universe.py`
- **Module Purpose**: Master registry defining the entire statutory universe of the Republic of India across Central Acts, 28 States, and 8 Union Territories.
- **Key Functions**:
  - `get_universe_inventory() -> List[UniverseRecord]`: Returns cataloged instruments (101 core instruments).
  - `get_statutes_by_jurisdiction(jurisdiction: str) -> List[UniverseRecord]`: Filters universe by jurisdiction code.
  - `verify_coverage_against_universe() -> Dict[str, Any]`: Computes exact indexed vs backlog statistics.

#### `legalmitra/corpus/legal_parser.py`
- **Module Purpose**: High-precision hierarchical parser transforming unstructured or semi-structured legislative text into deeply structured provision trees.
- **Key Methods**:
  - `parse_statute_text(raw_text: str, act_title: str) -> ParsedStatute`: Uses regex and AST patterns to segment:
    - Parts (`PART I — PRELIMINARY`)
    - Chapters (`CHAPTER II — OF OFFENCES AGAINST THE HUMAN BODY`)
    - Sections (`Section 103. Punishment for murder`)
    - Subsections (`(1) Whoever commits murder...`)
    - Clauses & Subclauses (`(a)`, `(i)`)
    - Provisos (`Provided that...`, `Provided further that...`)
    - Explanations (`Explanation 1.—...`)

#### `legalmitra/corpus/amendments.py` & `impact_analyzer.py`
- **Module Purpose**: Tracks legislative amendment instruments and models the textual and semantic impact of amending acts upon parent legislation.
- **Key Capabilities**:
  - Identifies modification types: `SUBSTITUTION`, `INSERTION`, `OMISSION`, `REPEAL`.
  - Determines commencement effective dates (S.O. notifications in the Gazette of India).
  - Updates provision timelines in the temporal knowledge graph.

#### `legalmitra/corpus/training_exporter.py`
- **Module Purpose**: Generates pretraining corpora and manifest files (`dataset_manifest_v4.json`) with strict source-grouped partitioning.
- **Guarantees**:
  - Strictly filters by `current_state == 'TRAINING_ELIGIBLE'`.
  - Enforces quarantine exclusion: explicitly checks and blocks `IND-JUD-DEL-2024-BAIL`.
  - Calculates SHA-256 hashes of individual partition files and the combined dataset.
- **Associated Tests**: `tests/test_corpus_scale.py`, `tests/test_phase35_validation.py`.
""")

    sections.append("""### 4.5 Extraction Subpackage (`legalmitra.extraction`)

The `legalmitra.extraction` subpackage handles the conversion of raw documents (PDF, DOCX, TXT, HTML) into normalized text representations with structural layout preservation.

#### `legalmitra/extraction/base.py`
- **Module Purpose**: Abstract base interface for all extraction backends.
- **Classes**:
  - `BaseExtractor(ABC)`: Declares abstract method `extract(file_path: Path) -> ExtractedDocument`.
  - `ExtractedDocument(BaseModel)`: Typed container holding raw text, page count, structural bounding boxes, metadata, and extraction confidence score.

#### `legalmitra/extraction/docling_extractor.py`
- **Module Purpose**: Enterprise PDF extraction engine utilizing IBM Docling to parse complex multi-column gazette layouts, tables, and footnote references without OCR degradation.
- **Fallback Logic**: If Docling native C-extensions or GPU acceleration are unavailable, seamlessly degrades to PyPDF / pdfplumber fallback extractors while recording an extraction warning.

#### `legalmitra/extraction/dispatcher.py`
- **Module Purpose**: Inspects document magic bytes and MIME types to route incoming files to the optimal extractor (`DoclingExtractor`, `TextExtractor`, or HTML extractor).
- **Associated Tests**: `tests/test_extraction.py`.
""")

    sections.append("""### 4.6 Normalization Subpackage (`legalmitra.normalization`)

The `legalmitra.normalization` subpackage standardizes typography, legal abbreviations, citation formats, and Devanagari Unicode sequences.

#### `legalmitra/normalization/clean_text.py`
- **Module Purpose**: Text normalization routines for Indian legal language.
- **Key Functions**:
  - `clean_legal_text(text: str) -> str`: Normalizes Unicode NFKC representation, converts curly typographic quotes to ASCII equivalents, eliminates non-breaking spaces (`\\u00a0`), strips PDF hyphenation artifacts at line breaks (`con-\\nstitution` -> `constitution`), and collapses extraneous whitespace.
  - `clean_devanagari_text(text: str) -> str`: Preserves Devanagari nukta, halant, matras, and danda punctuation while eliminating corrupted byte sequences.

#### `legalmitra/normalization/statute_normalizer.py`
- **Module Purpose**: Canonicalizes statutory names and provision designations.
  - Maps *"BNS"* or *"Bharatiya Nyay Sanhita"* -> *"The Bharatiya Nyaya Sanhita, 2023"*.
  - Maps *"u/s 438 CrPC"* or *"Sec. 438"* -> *"Section 438 of the Code of Criminal Procedure, 1973"*.
- **Associated Tests**: `tests/test_normalization.py`.
""")

    sections.append("""### 4.7 Knowledge Subpackage (`legalmitra.knowledge`)

The `legalmitra.knowledge` subpackage implements the persistent database repository layer encapsulating `data/legalmitra_kb.db`.

#### `legalmitra/knowledge/knowledge_base.py`
- **Module Purpose**: Thread-safe SQLite repository providing CRUD operations and high-performance FTS5 full-text search.
- **Key Methods**:
  - `connect() -> sqlite3.Connection`: Opens SQLite connection with `PRAGMA foreign_keys = ON`, `PRAGMA journal_mode = WAL`, and registers custom collation functions.
  - `add_chunk(chunk: LegalChunk) -> str`: Inserts chunk record and updates FTS5 virtual table.
  - `search_chunks(query: str, limit: int = 4, act_filter: Optional[str] = None, exclude_quarantined: bool = True) -> List[LegalChunk]`: Executes BM25-ranked full-text search query across `legal_chunks_fts`. When `exclude_quarantined` is True, adds filter `is_synthetic_scaffold = 0`.
  - `get_chunk_by_id(chunk_id: str) -> Optional[LegalChunk]`: Retrieves specific chunk.
  - `count_chunks() -> int`: Returns total stored chunk count (1,505 in Phase 36).
  - `count_active_chunks() -> int`: Returns retrievable chunk count (1,499 in Phase 36).

#### `legalmitra/knowledge/models.py`
- **Module Purpose**: Pydantic models representing knowledge base records:
  - `LegalChunk`: Represents an atomic retrievable legal unit with fields: `chunk_id`, `source_id`, `act_or_case_title`, `provision_or_para_ref`, `authority_level`, `verbatim_text`, `source_url`, `effective_date`, `is_synthetic_scaffold`, `content_hash`.
  - `SourceMetadata`: Represents a primary legal source entity.
- **Associated Tests**: `tests/test_knowledge_base.py`.
""")

    sections.append("""### 4.8 RAG & Retrieval Subpackage (`legalmitra.rag`)

The `legalmitra.rag` subpackage houses the core grounded retrieval, prompt assembly, and abstention orchestration engine.

#### `legalmitra/rag/engine.py`
- **Module Purpose**: Implements `LegalRAGEngine`, the central brain of the evidential question-answering system.
- **Key Methods**:
  - `answer_legal_query(query: str, act_filter: Optional[str] = None, section_filter: Optional[str] = None, limit: int = 4) -> ChatResponse`:
    1. Normalizes incoming query and cleans statutory references.
    2. Checks offline evaluation override (`LEGALMITRA_OFFLINE_EVAL == '1'`).
    3. Retrieves top candidate evidence chunks via FTS5 BM25 search.
    4. Evaluates evidence sufficiency and negative constraints.
    5. Formulates structured prompt incorporating retrieved chunks and Golden Citations rules.
    6. Calls LLM provider to generate grounded response.
    7. Validates citations and claim support against evidence chunks.
    8. Appends mandatory statutory disclaimer.
    9. Returns fully typed `ChatResponse`.

#### `legalmitra/rag/evaluator.py`
- **Module Purpose**: Evaluates whether retrieved evidence provides legally sufficient grounds to formulate an affirmative answer. If key statutory prerequisites are absent or the query embodies a false legal premise, triggers an abstention recommendation.
- **Associated Tests**: `tests/test_rag.py`, `tests/test_grounding.py`.
""")

    sections.append("""### 4.9 LLM Subpackage (`legalmitra.llm`)

The `legalmitra.llm` subpackage abstracts language model inference across local mock providers and remote enterprise API endpoints.

#### `legalmitra/llm/interface.py`
- **Module Purpose**: Defines the abstract `LLMProvider` contract:
  - `generate(prompt: str, max_tokens: int = 1024, temperature: float = 0.0) -> str`
  - `generate_chat(messages: List[Dict[str, str]], max_tokens: int = 1024, temperature: float = 0.0) -> str`

#### `legalmitra/llm/mock_provider.py`
- **Module Purpose**: High-speed, deterministic mock provider for unit testing, CI pipelines, and offline evaluation. Matches predefined legal queries to golden answers, ensuring zero external network dependencies during automated testing.

#### `legalmitra/llm/nemotron.py`
- **Module Purpose**: Production client for NVIDIA's `nvidia/llama-3.1-nemotron-70b-instruct` model hosted on NVIDIA Integrate API. Implements exponential backoff retry logic, timeout enforcement, and token streaming.
- **Associated Tests**: `tests/test_nemotron_interface.py`, `tests/test_live_nemotron.py`.
""")

    sections.append("""### 4.10 Validation & Quality Gate Subpackage (`legalmitra.validation`)

The `legalmitra.validation` subpackage enforces the 8 foundational Quality Gates ensuring syntactic fidelity, deduplication, claim grounding, and temporal accuracy.

#### `legalmitra/validation/quality_gate.py`
- **The 8 Pre-Indexing & Grounding Quality Gates**:
  1. `GATE_1_SYNTACTIC_SCHEMA`: Validates that parsed documents strictly adhere to Pydantic schema constraints with zero missing required fields.
  2. `GATE_2_CITATION_FIDELITY`: Verifies that every statutory section, rule, or case citation cited in an answer exists verbatim within the retrieved evidence.
  3. `GATE_3_TEMPORAL_GROUNDING`: Verifies that historical laws are not cited as current law for post-transition events, and non-retroactivity principles are respected.
  4. `GATE_4_AUTHORITY_HIERARCHY`: Enforces precedent precedence: Constitutional > Central Statute > State Statute > Supreme Court > High Court.
  5. `GATE_5_CLAIM_GROUNDING`: Validates that every declarative legal proposition in the generated text is backed by a specific evidence chunk.
  6. `GATE_6_QUARANTINE_ENFORCEMENT`: Rejects any response or dataset entry that references quarantined IDs (e.g., `IND-JUD-DEL-2024-BAIL`).
  7. `GATE_7_DEDUPLICATION`: Blocks chunk insertion if content hash already exists in `legal_chunks`.
  8. `GATE_8_ABSTENTION_ACCURACY`: Confirms that the system correctly abstains on unanswerable queries or queries with false legal premises.
- **Associated Tests**: `tests/test_quality_gate.py`, `tests/test_adversarial_quality_gate.py`.
""")

    sections.append("""### 4.11 Caselaw & Precedent Subpackage (`legalmitra.caselaw`)

The `legalmitra.caselaw` subpackage implements judicial precedent intelligence and citation networks.

#### `legalmitra/caselaw/case_identity.py`
- **Module Purpose**: Standardizes Indian case citations across reporters (SCR, SCC, AIR, ILR, SCC OnLine) and High Court neutral citations (`[Year]:[Court]:[Number]`).

#### `legalmitra/caselaw/precedent.py`
- **Module Purpose**: Models precedent status and judicial hierarchy:
  - Distinguishes *ratio decidendi* (binding rule of law) from *obiter dicta* (persuasive observation).
  - Tracks bench coram size (Larger bench overrules smaller bench).
  - Records judicial status: `ACTIVE`, `OVERRULED`, `DISTINGUISHED`, `AFFIRMED`.

#### `legalmitra/caselaw/knowledge_graph.py`
- **Module Purpose**: In-memory directed acyclic graph (DAG) representing judicial citations and overruling relationships between landmark rulings.
- **Associated Tests**: `tests/test_phase17_caselaw.py`, `tests/test_phase21_judicial.py`.
""")

    sections.append("""### 4.12 Temporal Law Subpackage (`legalmitra.temporal`)

The `legalmitra.temporal` subpackage handles the complex point-in-time applicability of Indian statutory law.

#### `legalmitra/temporal/engine.py`
- **Key Capabilities**:
  - `evaluate_applicability(provision_id: str, date_of_offence_or_cause: date) -> TemporalStatus`: Determines whether a provision applies to an event occurring on a specific date.
  - Models the July 1, 2024 criminal law transition:
    - Cause of action prior to July 1, 2024 -> Substantive law: Indian Penal Code, 1860.
    - Cause of action on or after July 1, 2024 -> Substantive law: Bharatiya Nyaya Sanhita, 2023.
    - Handles transitional procedural provisions under Section 531 of the BNSS, 2023.
- **Associated Tests**: `tests/test_phase20_legislation.py`.
""")

    sections.append("""### 4.13 Schemas Subpackage (`legalmitra.schemas`)

The `legalmitra.schemas` subpackage defines strict, immutable Pydantic V2 models for all domain entities.

- `statute.py`: `StatuteDocument`, `Part`, `Chapter`, `Section`, `Subsection`, `Proviso`, `Explanation`.
- `judgment.py`: `JudgmentDocument`, `BenchComposition`, `RatioDecidendi`, `OperativeOrder`.
- `legal_qa.py`: `LegalQAPair`, `GroundingEvidence`, `EvaluationTelemetry`.
- `case_analysis.py`: `CaseBrief`, `IssuePresented`, `RuleOfLaw`, `ApplicationOfLaw`.
- `procedural_guide.py`: `ProceduralStep`, `StatutoryTimeline`, `LimitationPeriod`.
- `registry.py`: `SourceRecord`, `UnifiedSourceRegistrySchema`.
- `evaluation.py`: `BenchmarkCase`, `EvaluationResult`, `MetricReport`.
- **Associated Tests**: `tests/test_schemas.py`.
""")

    sections.append("""### 4.14 Review Subpackage (`legalmitra.review`)

The `legalmitra.review` subpackage manages the human-in-the-loop advocate review workflow.

#### `legalmitra/review/tracker.py`
- **Module Purpose**: Maintains `ReviewTrackingRegister` in `data/07_batches/review/review_tracking_register.json`.
- **Invariants Enforced**:
  - Exactly 40 tracked records (20 Package A / Pilot 20, 20 Package B / Batch 01).
  - All records strictly maintained in `pending_legal_review` status until physical human review packages are imported.
  - Zero automated advancement without cryptographic advocate signature.
- **Associated Tests**: `tests/test_phase23_review_workflow.py`, `tests/test_review_package.py`.
""")

    sections.append("""### 4.15 Evaluation Subpackage (`legalmitra.evaluation`)

The `legalmitra.evaluation` subpackage provides automated benchmarking, metric computation, and failure diagnosis.

- `dataset.py`: Benchmark dataset loaders and integrity verification.
- `metrics.py`: Implements mathematical metric formulations: Citation Recall, Claim Grounding Support, Faithfulness Score, MRR (Mean Reciprocal Rank).
- `failure_attribution.py`: Automates failure triage across 15 distinct categories (`single_provision`, `multi_provision`, `overruled_precedent`, `false_legal_premise`, etc.).
- `runner.py`: High-concurrency async evaluation runner.
- **Associated Tests**: `tests/test_phase22_evaluation.py`, `tests/test_phase31_custom_questions.py`.
""")

    sections.append("""### 4.16 Dataset & Generation Subpackages (`legalmitra.dataset` & `generation`)

- **`legalmitra.dataset`**:
  - `partitioner.py`: Source-grouped partitioner allocating documents to train, val, and test splits without fragmenting source documents.
  - `jsonl_exporter.py`: High-throughput JSONL pretraining stream writer.
- **`legalmitra.generation`**:
  - `prompts.py`: Hardened system prompts enforcing strict citation grounding, negative constraints, and statutory disclaimers.
  - `orchestrator.py`: Coordinates multi-turn drafting and QA generation workflows.
- **Associated Tests**: `tests/test_partitioner.py`, `tests/test_generation.py`.
""")

    sections.append("""### 4.17 Web Subpackage (`legalmitra.web`)

The `legalmitra.web` subpackage implements the production FastAPI application, route handlers, and session persistence.

#### `legalmitra/web/app.py`
- **FastAPI Endpoints**:
  - `GET /`: Serves landing page or redirects to `/chat`.
  - `GET /chat`: Serves Google Stitch Constitutional Modernism web UI.
  - `GET /api/v1/health`: Liveness probe returning system status, timestamp, and active environment.
  - `GET /api/v1/ready`: Readiness probe verifying SQLite database connectivity (`data/legalmitra_kb.db` and `data/conversations.db`).
  - `POST /api/v1/chat`: Submits legal query, retrieves evidence, generates grounded answer, and records session history.
  - `GET /api/v1/conversations`: Lists user conversations.
  - `GET /api/v1/conversations/{conv_id}/messages`: Returns conversation message transcript.
  - `DELETE /api/v1/conversations/{conv_id}`: Deletes conversation session.
  - `POST /api/v1/feedback`: Records advocate or user feedback on answer accuracy.

#### `legalmitra/web/store.py`
- **Module Purpose**: Encapsulates `data/conversations.db`, providing SQLite session persistence with tables `conversations`, `messages`, and `feedback`.
- **Associated Tests**: `tests/test_web_api.py`.
""")

    sections.append("""### 4.18 Research Subsystem (`research/original_model`)

The `research/original_model` directory contains the source code, tokenizers, dataset manifests, and training checkpoints for LegalMitra's original Indian legal language model.

```text
research/
└── original_model/
    ├── __init__.py
    ├── model.py                # Decoder-only causal transformer in PyTorch (1.07M params)
    ├── tokenizer.py            # Tokenizer v1 (vocab 1,024, English dominant)
    ├── tokenizer_v2.py         # Tokenizer v2 (vocab 2,048, bilingual Devanagari Hindi + English)
    ├── dataset.py              # PyTorch Dataset loaders & legal text extractors
    ├── train.py                # Training loop with loss tracking, gradient clipping & AdamW
    ├── bilingual_pipeline.py   # Bilingual data preparation & tokenization pipeline
    ├── tokenizer_v2.json       # Serialized Tokenizer v2 vocabulary & merges (1,811 merges)
    ├── checkpoints/            # PyTorch checkpoint vault
    │   └── phase35_1m_baseline_regression.pt # Verified 1.07M model checkpoint (Loss: 5.6607)
    └── manifests/              # Cryptographically hashed dataset manifests
        ├── dataset_manifest_v2.json
        ├── dataset_manifest_v3.json
        └── dataset_manifest_v4.json # 342,965 usable tokens (SHA-256: 15088ea8e...)
```

- **`model.py`**: Declares `LegalDecoderTransformer` and `LegalTransformerConfig`.
  - Implements Multi-Head Causal Self-Attention with causal lower-triangular masking.
  - Supports weight tying between input embeddings and final output projection.
  - Standard configuration: `d_model=128`, `n_layers=4`, `n_heads=4`, `d_ff=512`, `vocab_size=2048`, `max_seq_len=128/256`.
- **`tokenizer_v2.py`**: Declares `IndianLegalTokenizerV2`.
  - Built-in Byte-Pair Encoding (BPE) with byte fallback.
  - Handles mixed Hindi-English legal text with zero out-of-vocabulary exceptions.
- **Associated Tests**: `tests/test_phase31_original_model.py`, `tests/test_phase32_validation.py`, `tests/test_phase33_validation.py`, `tests/test_phase35_validation.py`, `tests/test_phase36_validation.py`.
""")

    sections.append("""### 4.19 Operational Scripts Master Catalog (`scripts/`)

The `scripts/` directory houses 54 specialized utility, maintenance, and verification scripts:

| Script Name | Purpose & Primary Execution Command |
|:---|:---|
| `verify_freeze.py` | Bitwise verification of the 6 Phase 9 frozen review artifacts against SHA-256 manifests. |
| `verify_review_packages.py` | Full integrity verification of Package A, Package B, and review tracking registers (40 pending items). |
| `run_phase35_small_model_regression.py` | Runs 50-step regression pretraining of the 1.07M transformer on Manifest v4. |
| `reproduce_phase35_small_model_regression.py` | Re-evaluates saved Phase 35 checkpoint to reproduce exact validation loss (5.6607). |
| `train_and_audit_tokenizer_v2.py` | Trains Tokenizer v2 from scratch and executes comparative audit against Tokenizer v1. |
| `build_benchmark_v9.py` | Generates 96-case Benchmark v9 dataset across 15 legal evaluation categories. |
| `populate_unified_source_registry.py` | Audits and builds `data/09_national_corpus/unified_source_registry.json` (111 sources). |
| `generate_source_eligibility_ledger.py`| Reconciles source eligibility (33 eligible, 67 backlog, 10 discovery, 1 quarantined). |
| `corpus_coverage_report.py` | Audits national legal coverage across Central Acts and State legislation. |
| `national_coverage_report.py` | Generates detailed CSV and JSON coverage reports for the Indian Legal Universe. |
| `ingest_hindi_statutes.py` | Acquires and indexes authentic Hindi gazette texts under Article 394A. |
| `build_phase34_datasets.py` | Compiles Manifest v4 dataset partitions with source-grouped splits. |
| `audit_custom_questions.py` | Evaluates system performance and failure attribution on custom benchmark cases. |
| `profile_compute_feasibility.py` | Profiles hardware compute, VRAM consumption, and scaling feasibility. |
""")

    sections.append("""### 4.20 Test Suite Catalog (`tests/`)

The `tests/` directory contains 38 comprehensive test suites verifying all platform capabilities:

| Test Suite Module | Test Count | Scope & Focus Areas |
|:---|:---:|:---|
| `test_adversarial_quality_gate.py` | 12 | Adversarial prompt injection, jailbreak defenses, false legal premise detection |
| `test_corpus_pipeline.py` | 10 | Corpus ingestion pipeline, text extraction, structural section parsing |
| `test_corpus_scale.py` | 11 | Corpus scaling benchmarks, FTS5 index performance, bulk chunk queries |
| `test_deduplication.py` | 3 | Content hash deduplication and fuzzy match rejection |
| `test_end_to_end_pipeline.py` | 1 | Full pipeline execution: raw PDF -> normalized text -> FTS5 -> RAG -> web response |
| `test_extraction.py` | 5 | PDF and Docling extraction backends, layout analysis, fallback mechanisms |
| `test_generation.py` | 15 | Prompt templating, legal drafting schemas, Pydantic response validation |
| `test_grounding.py` | 3 | Claim-to-source evidential grounding, citation accuracy, unverified claim rejection |
| `test_knowledge_base.py` | 7 | SQLite schema integrity, FTS5 virtual tables, chunk CRUD operations, quarantine checks |
| `test_nemotron_interface.py` | 4 | Mock and remote LLM provider interfaces, retry policies, streaming contracts |
| `test_normalization.py` | 3 | Unicode NFKC normalization, whitespace collapsing, citation standardizers |
| `test_partitioner.py` | 2 | Source-grouped dataset partitioning, zero-leakage cross-split guarantees |
| `test_phase9_freeze.py` | 3 | Bitwise invariant tests for Phase 9 frozen artifacts |
| `test_pilot_20.py` | 8 | Pilot 20 advocate review dataset integrity and schema compliance |
| `test_quality_gate.py` | 5 | The 8 Quality Gates pre-indexing and post-retrieval validation |
| `test_rag.py` | 6 | RAG retrieval engine, evidence sufficiency scoring, explicit abstention logic |
| `test_registry.py` | 6 | Source registry state machine transitions and audit logging |
| `test_review_operations.py` | 11 | Advocate review tracking, state transitions, package import operations |
| `test_review_package.py` | 4 | Package A and Package B schema validation and checksum verification |
| `test_schemas.py` | 9 | Pydantic data models, field constraints, serialization and deserialization |
| `test_validation.py` | 3 | Generic validation utilities and assertion helpers |
| `test_web_api.py` | 10 | FastAPI endpoints, health probes, chat requests, conversation store, rate limits |
| `test_phase12_pipeline.py` to `test_phase36_validation.py` | 165 | Regression test suites for Phases 12 through 36 |
| **Total Test Suite Scale** | **315 Passed** | **Zero Failures, 2 Live Network Tests Deselected in Non-Live Mode** |
""")

    sections.append("""### 4.21 Data Directory Layout (`data/`)

The `data/` directory provides structured, version-controlled storage for raw documents, normalized texts, database files, review packages, and evaluation datasets:

```text
data/
├── legalmitra_kb.db             # Primary Knowledge Base (SQLite + FTS5: 1,505 Chunks | 59 Sources)
├── conversations.db             # User Session & Feedback Store (SQLite: Isolated from KB)
├── 01_raw/                      # Raw acquired artifacts (PDFs, Gazette downloads, TXT)
├── 02_normalized/               # Normalized UTF-8 legal text extracts
├── 03_generated/                # Intermediate generated synthetic QA pairs & drafts
├── 04_verified/                 # Quality-gate verified data artifacts
├── 05_evaluation/               # Benchmark specifications & historical evaluations
├── 06_review/                   # Package A: Phase 9 Frozen Pilot 20 Review Artifacts
│   ├── pilot_20_examples.jsonl  # SHA256: e01b22f5... (44,542 bytes)
│   ├── pilot_20_manifest.json   # SHA256: 9da3801f... (21,705 bytes)
│   ├── pilot_20_review_sheet.csv# SHA256: 6f519165... (35,396 bytes)
│   ├── pilot_20_source_bundle.json # SHA256: 3cf555e9... (62,870 bytes)
│   ├── pilot_20_open_issues.md  # SHA256: 0b82c4f6... (7,903 bytes)
│   └── PHASE8_OPEN_LEGAL_ISSUES_REGISTER.md # SHA256: e5966e24... (15,514 bytes)
├── 07_batches/                  # Package B: Batch 01 Candidate Expansion (40 total review records)
│   └── review/
│       ├── batch_01_examples.jsonl
│       ├── batch_01_review_sheet.csv
│       ├── batch_01_source_bundle.json
│       └── review_tracking_register.json # Master 40-record tracking register
├── 08_corpus/                   # Legislative repository catalogs & State registry
├── 09_national_corpus/          # National Indian Legal Corpus Master Directory
│   ├── unified_source_registry.json  # 111 Tracked Sources Master Registry
│   ├── source_eligibility_ledger.json# Source eligibility audit & reconciliation ledger
│   ├── coverage_report.json     # Detailed national coverage metrics
│   ├── legal_universe_inventory.json # 101 Universe instruments inventory
│   └── quarantine/              # Strict isolation directory for synthetic scaffolds
├── 10_legislation/              # High-volume statutory text extracts
├── 11_judicial_corpus/          # High Court & Supreme Court judgment repository
├── 12_evaluation/ to 20_evaluation/ # Historical Benchmark Evaluation Suites (v1 through v9)
│   └── 20_evaluation/
│       ├── evaluation_cases_v9.json  # Benchmark v9 (96 cases across 15 categories)
│       ├── manifest_v9.json
│       ├── model_experiment_results_v4.json # Phase 35 1.07M model regression results
│       └── tokenizer_v2_audit_results.json  # Tokenizer v2 empirical audit results
└── splits/                      # Pretraining dataset split manifests
```

---
""")
    return "\n".join(sections)
