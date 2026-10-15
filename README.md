# LegalMitra — Indian Legal Dataset Engineering Foundation

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Docling Powered](https://img.shields.io/badge/Docling-v2.139-green.svg)](https://github.com/DS4SD/docling)
[![Tests Passing](https://img.shields.io/badge/Tests-39%20Passed-brightgreen.svg)]()
[![Code Coverage](https://img.shields.io/badge/Coverage-88%25-brightgreen.svg)]()

> [!IMPORTANT]
> **Legal Review Status Disclaimer**: Automated ingestion, Docling parsing, and Pydantic schema validation verify **syntactic structure, string preservation, and data integrity**. They do **not** establish substantive legal correctness. Every record in LegalMitra explicitly maintains its `LegalReviewStatus` (`unverified_automated`, `pending_legal_review`, `legal_expert_approved`, `legal_expert_rejected`, `flagged_unsupported`). No model fine-tuning is performed at this milestone.

---

## 1. Project Overview

**LegalMitra** is an Indian legal dataset engineering platform. It ingests legally sourced primary documents (central/state statutes, court judgments, gazette notifications), extracts structured text with IBM Docling, normalizes statutory hierarchies and court paragraph numbering, validates records against 7 Pydantic schemas, and partitions datasets into leakage-free Train/Val/Test splits for RAG and future fine-tuning.

---

## 2. Documented Project Structure

```text
c:\PROJECTS\LegalMitra\
├── .env.example                     # Sample configuration for Nemotron credentials
├── .gitignore                       # Standard legal engineering ignores (raw data, pycache)
├── pyproject.toml                   # Project dependencies and packaging
├── README.md                        # Project documentation and quickstart
├── ARCHITECTURE.md                  # Comprehensive architectural specification
├── EXTRACTION_FAILURE_REPORT.md     # Diagnostic audit report of extraction failures
├── run_pipeline.py                  # End-to-end milestone runner script
│
├── config/
│   ├── settings.py                  # Pydantic BaseSettings loading from environment
│   └── default_config.yaml          # Default pipeline parameters
│
├── data/                            # Segregated data lifecycle storage
│   ├── 01_raw/                      # Bit-for-bit raw incoming legal documents
│   ├── 02_normalized/               # Normalized structured JSON outputs
│   ├── 03_generated/                # Synthetic examples grounded in source text
│   ├── 04_verified/                 # Advocate-reviewed and certified examples
│   ├── 05_evaluation/               # Gold standard evaluation benchmark sets
│   └── splits/                      # Leakage-free train.jsonl, val.jsonl, test.jsonl
│
├── registry/
│   └── source_registry.jsonl        # Append-only ledger of document provenance & checksums
│
├── corpus/                          # Milestone sample test corpus
│   ├── sample_statute_bsa_s61.txt   # Section 61, Bharatiya Sakshya Adhiniyam, 2023
│   ├── sample_statute_bsa_s63.html  # Section 63 BSA 2023 (for Docling HTML testing)
│   ├── sample_statute_bsa_s61.pdf   # Section 61 BSA 2023 (for Docling PDF testing)
│   ├── sample_statute_pocso_s4.txt  # Section 4, POCSO Act, 2012 (with s.33(7) privacy)
│   ├── sample_judgment_sc_privacy.txt # Justice K.S. Puttaswamy (Retd.) v. UOI (2017) 10 SCC 1
│   ├── sample_judgment_bns_bail.txt # Delhi High Court anticipatory bail under BNSS
│   └── unsupported_dummy.xyz        # Unsupported binary file to test error diagnosis
│
├── legalmitra/
│   ├── core/                        # Core foundational utilities
│   │   ├── enums.py                 # SourceType, Jurisdiction, CourtType, ReviewStatus
│   │   ├── errors.py                # Custom domain exception hierarchy
│   │   ├── hashing.py               # SHA-256 and content fingerprinting
│   │   └── logging.py               # Structured logging
│   │
│   ├── schemas/                     # 7 Domain-specific Pydantic schemas + Registry
│   │   ├── registry.py              # SourceRegistryRecord
│   │   ├── statute.py               # StatuteDocument, Section, Subsection, Provisos
│   │   ├── judgment.py              # JudgmentDocument, Paragraphs, Coram, Citations
│   │   ├── legal_qa.py              # LegalQADocument & EvidencePassage
│   │   ├── case_analysis.py         # CaseAnalysisDocument (Ratio & Obiter)
│   │   ├── procedural_guide.py      # ProceduralGuidanceDocument & Steps
│   │   ├── drafting_example.py      # DraftingExampleDocument & Clauses
│   │   └── evaluation.py            # EvaluationQuestionDocument & Rubrics
│   │
│   ├── ingestion/                   # Document ingestion & provenance
│   │   ├── ingestor.py              # File ingestor with SHA-256 hashing
│   │   └── registry.py              # SourceRegistryManager (JSONL CRUD, deduplication)
│   │
│   ├── extraction/                  # Extraction backends & diagnostics
│   │   ├── base.py                  # BaseExtractor and ExtractionResult
│   │   ├── docling_extractor.py     # IBM Docling DocumentConverter wrapper
│   │   ├── text_extractor.py        # Text & Markdown statutory extractor
│   │   ├── dispatcher.py            # MIME/Extension router with failure logging
│   │   └── failure_reporter.py      # Diagnostic markdown/json failure generator
│   │
│   ├── normalization/               # Legal structure normalizers
│   │   ├── clean_text.py            # Unicode & quote sanitizer
│   │   ├── statute_normalizer.py    # Sections, provisos, explanations parser
│   │   ├── judgment_normalizer.py   # Coram, numbered paragraphs, ratio parser
│   │   └── normalizer.py            # Normalization orchestrator
│   │
│   ├── validation/                  # Schema, deduplication & zero-hallucination
│   │   ├── pydantic_validator.py    # SchemaValidator
│   │   ├── deduplication.py         # DeduplicationEngine
│   │   └── grounding_validator.py   # GroundingValidator (source evidence verification)
│   │
│   ├── dataset/                     # Partitioning & serialization
│   │   ├── jsonl_exporter.py        # Validated JSONL reader/writer
│   │   ├── partitioner.py           # DatasetPartitioner (grouped by source_id)
│   │   └── pipeline.py              # High-level pipeline coordinator
│   │
│   └── llm/                         # Model integration interfaces
│       ├── interface.py             # BaseLLMProvider, LLMMessage, LLMResponse
│       ├── nemotron.py              # NVIDIA Nemotron provider (dynamic env vars)
│       └── mock_provider.py         # Deterministic mock provider for CI/CD
│
└── tests/                           # 39 Unit and Integration Tests
    ├── conftest.py                  # Pytest fixtures and temporary environments
    ├── test_schemas.py              # Tests for all 7 schemas
    ├── test_registry.py             # Tests for registry manager & ingestion
    ├── test_extraction.py           # Tests for Docling, text extraction & failures
    ├── test_normalization.py        # Tests for statute & judgment parsing
    ├── test_validation.py           # Tests for Pydantic schema validation
    ├── test_grounding.py            # Tests for evidence verification & hallucination traps
    ├── test_deduplication.py        # Tests for checksums & semantic near-duplicates
    ├── test_partitioner.py          # Tests for zero-leakage dataset partitioning
    ├── test_nemotron_interface.py   # Tests for Nemotron client & credentials
    └── test_end_to_end_pipeline.py  # Full end-to-end integration test
```

---

## 3. Dependency and Setup Instructions

### 3.1 Prerequisites
- Python 3.10+ (Tested on Python 3.11.0 on Windows amd64).
- C++ build tools for layout detection packages (if building from source).

### 3.2 Installation
```powershell
# Navigate to repository
cd c:\PROJECTS\LegalMitra

# Install dependencies in editable mode
pip install -e .

# Install development & test dependencies
pip install pytest pytest-cov
```

Key dependencies:
- `docling>=2.0.0`: IBM Docling structured document conversion.
- `pydantic>=2.5.0` & `pydantic-settings>=2.0.0`: Schema validation and settings management.
- `requests>=2.31.0`: HTTP client for NVIDIA Nemotron NIM endpoints.
- `pytest>=7.4.0` & `pytest-cov>=4.1.0`: Testing and test coverage auditing.

---

## 4. Running the Pipeline and Test Suite

### 4.1 Running All Automated Tests
Run pytest across all 39 tests:
```powershell
pytest
```

Run tests with line-by-line coverage analysis:
```powershell
pytest --cov=legalmitra --cov-report=term-missing
```

**Actual Test Results**:
```text
============================= 39 passed in 11.11s =============================
TOTAL Code Coverage: 88%
```

### 4.2 Executing the End-to-End Milestone Pipeline
Run the milestone pipeline over the test corpus:
```powershell
python run_pipeline.py
```
This command:
1. Ingests all test documents in `corpus/` into `data/01_raw/`.
2. Computes SHA-256 digests and logs entries in `registry/source_registry.jsonl`.
3. Dispatches extraction (Docling for HTML/PDF, Text for TXT/MD).
4. Generates normalized structured JSON models in `data/02_normalized/`.
5. Logs unsupported/corrupted documents in `EXTRACTION_FAILURE_REPORT.md`.
6. Produces verified source-grounded JSONL examples in `data/03_generated/`.
7. Partitions normalized documents into `data/splits/train.jsonl`, `val.jsonl`, and `test.jsonl` with zero cross-split leakage.

---

## 5. Example Source Records and JSONL Outputs

### 5.1 Source Registry Record (`registry/source_registry.jsonl`)
```json
{
  "document_id": "IND-STAT-BSA-2023-SEC61",
  "title": "Bharatiya Sakshya Adhiniyam, 2023 - Section 61",
  "source_url": "https://www.indiacode.nic.in/handle/123456789/20000",
  "source_type": "statute",
  "jurisdiction": "IN",
  "court": "None (Statutory / Executive)",
  "document_date": "2023-12-25",
  "effective_date": "2024-07-01",
  "retrieval_timestamp": "2026-10-15T17:16:19.452000Z",
  "version": "1.0.0",
  "licence_or_terms": "Government of India Open Data License (GODL-India)",
  "checksum": "3b22e06180356c39f01eef9ae3b5a14d59f7dfddb35cf013ef17f4007ad94766",
  "verification_status": "unverified_automated",
  "processing_status": "normalized",
  "raw_file_path": "C:\\PROJECTS\\LegalMitra\\data\\01_raw\\IND-STAT-BSA-2023-SEC61.txt",
  "file_format": ".txt",
  "byte_size": 918
}
```

### 5.2 Source-Grounded Legal Q&A Record (`data/03_generated/legal_qa.jsonl`)
```json
{
  "qa_id": "QA-BSA-S61-001",
  "question": "Under the Bharatiya Sakshya Adhiniyam, 2023, on what grounds can an electronic record NOT be denied admissibility?",
  "answer": "Under Section 61 of the Bharatiya Sakshya Adhiniyam, 2023, nothing in the Adhiniyam shall apply to deny the admissibility of an electronic or digital record in evidence solely on the ground that it is an electronic or digital record. Such record holds the same legal validity, effect, and enforceability as any physical document, subject to the certification requirement set out in Section 63.",
  "supporting_source_ids": ["IND-STAT-BSA-2023-SEC61"],
  "evidence_passages": [
    {
      "source_id": "IND-STAT-BSA-2023-SEC61",
      "section_or_para_ref": "Section 61",
      "verbatim_text": "Nothing in this Adhiniyam shall apply to deny the admissibility of an electronic or digital record in the evidence on the ground that it is an electronic or digital record, and such record shall have the same legal effect, validity and enforceability as other document, subject to the provisions of section 63.",
      "page_number": 1
    }
  ],
  "legal_domain": "Criminal Law - Evidence",
  "jurisdiction": "IN",
  "statutory_citations": [
    "Section 61, Bharatiya Sakshya Adhiniyam, 2023",
    "Section 63, Bharatiya Sakshya Adhiniyam, 2023"
  ],
  "case_citations": [],
  "flagged_unsupported": false,
  "legal_disclaimer": "This information is provided for educational and analytical purposes under Indian law and does not constitute formal legal counsel or advocate-client representation.",
  "legal_review_status": "unverified_automated"
}
```

---

## 6. Extraction Failure & Unsupported Case Reporting

When an unextractable or unsupported document is passed (such as `corpus/unsupported_dummy.xyz`):
1. The pipeline catches the failure without crashing.
2. The record in `registry/source_registry.jsonl` is marked with `processing_status="failed"` and records the diagnostic stack.
3. `ExtractionFailureReporter` compiles a report into `EXTRACTION_FAILURE_REPORT.md`:

| Document ID | Format | Failure Category | Suggested Remediation |
|---|---|---|---|
| `IND-UNSUPPORTED-001` | `.xyz` | **UNSUPPORTED_FORMAT** | Convert file from '.xyz' to standard PDF, DOCX, HTML, or TXT before ingestion. |

---

## 7. Connecting NVIDIA Nemotron

The pipeline provides an interchangeable provider interface (`legalmitra/llm/nemotron.py`) designed to interface with NVIDIA Nemotron models (e.g., `nvidia/llama-3.1-nemotron-70b-instruct` or `nvidia/nemotron-4-340b-instruct`) without hardcoding endpoints.

### Step 1: Set Credentials in Environment
Copy `.env.example` to `.env` or set environment variables:
```powershell
$env:NEMOTRON_API_KEY="nvapi-your-secret-api-key"
$env:NEMOTRON_BASE_URL="https://integrate.api.nvidia.com/v1"
$env:NEMOTRON_MODEL_NAME="nvidia/llama-3.1-nemotron-70b-instruct"
$env:NEMOTRON_API_FORMAT="openai_compatible"
$env:NEMOTRON_TIMEOUT_SECONDS="60.0"
```

### Step 2: Use in Python Code
```python
from legalmitra.llm.nemotron import NemotronLLMProvider
from legalmitra.llm.interface import LLMMessage

# Automatically loads credentials from environment variables
provider = NemotronLLMProvider()

if provider.is_available():
    messages = [
        LLMMessage(role="system", content="You are a legal assistant operating under Indian law."),
        LLMMessage(role="user", content="Summarize the legal effect of Section 61 of BSA 2023.")
    ]
    response = provider.generate(messages, temperature=0.1)
    print("Response:", response.content)
else:
    print("NEMOTRON_API_KEY not configured.")
```
