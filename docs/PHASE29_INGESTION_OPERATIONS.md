# Phase 29: Ingestion Operations, Operator Workflow & Determinism Report
**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Owner:** Team Shatrujeet (Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo)  
**Classification:** Proprietary and Confidential  
**Date:** October 2026  
**Phase:** 29  

---

## 1. Operating Architecture & Standards

LegalMitra enforces idempotent, deterministically reproducible batch ingestion via `legalmitra/ingestion/national_corpus_pipeline.py`. The pipeline is built to execute without mutating existing verified records, corrupting FTS indices, or introducing duplicate chunks.

---

## 2. Ingestion Lifecycle Pipeline Stages

Every batch proceeds through 8 deterministic pipeline stages:
1. `DISCOVERED`: Verified against official portal or gazette URL.
2. `SOURCE_VALIDATED`: Confirmed schema compliance with `SourceRegistryRecord`.
3. `HASH_VERIFIED`: Computes cryptographic SHA-256 hash of payload.
4. `PARSED`: Decomposes text into sections, subsections, provisos, explanations, and judgment paragraphs.
5. `METADATA_RESOLVED`: Injects verified commencement, effective date, and authority levels.
6. `INDEXED`: Atomic SQLite transaction inserting into `sources`, `legal_chunks`, and `legal_chunks_fts`.
7. `GRAPH_UPDATED`: Adds nodes and typed edges into the national judicial knowledge graph.
8. `VERIFIED`: Confirms zero duplicate chunk IDs and validates BM25 retrievability.

---

## 3. Operator Workflow & Disaster Recovery

### Standard Batch Ingestion Command:
```python
from legalmitra.ingestion.national_corpus_pipeline import NationalCorpusPipeline
from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase

kb = LegalKnowledgeBase("data/legalmitra_kb.db")
pipeline = NationalCorpusPipeline(kb=kb)
manifest = pipeline.run_statute_batch(batch_id="BATCH-P29-01", statute_docs=new_statutes)
```

### Safety and Invariant Guarantees:
- **Resumability:** Checkpoints are persisted per document in `data/09_national_corpus/batches/`.
- **Dry-Run Mode:** `dry_run=True` calculates estimated chunks and validates schema syntax without writing to SQLite.
- **Atomic Rollback:** If any document within a batch fails validation, transaction rollback is triggered.
- **Scaffold Protection:** The synthetic scaffold `IND-JUD-DEL-2024-BAIL` remains permanently isolated with `is_synthetic_scaffold = 1` and is never included in training or production batches.
