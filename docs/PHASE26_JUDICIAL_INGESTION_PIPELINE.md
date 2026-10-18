# LegalMitra Phase 26: Judicial Ingestion Pipeline & Quality Control

**Document ID:** LM-DOC-P26-ING-PIPE-01  
**Classification:** Engineering Specification  
**Phase:** 26  
**Date:** October 2026  
**Status:** Implemented  

---

## 1. Pipeline Overview

The LegalMitra Judicial Ingestion Pipeline transforms raw judicial records (judgments, orders, hearing listings, case status sheets) into verified, source-verifiable legal artifacts.

```
+-------------------------------------------------------------+
|  Primary Official High Court / Supreme Court Portal / PDF   |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|  1. Acquisition & Canonical Identifier Verification         |
|     - Neutral Citation Format (e.g. 2018:DHC:7175)          |
|     - Case Suit Number & Bench Composition                  |
|     - SHA-256 Digest Computation                            |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|  2. Structural Parsing & Proposition Decomposition          |
|     - Headnote / Metadata Extraction                        |
|     - Substantive Ratio Decidendi Extraction                |
|     - Holding & Operative Order Isolation                   |
|     - Verbatim Key Paragraph Quotations                     |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|  3. Knowledge Base & Graph Ingestion                        |
|     - sources: Source record registration                   |
|     - legal_chunks: Structured hierarchical chunking        |
|     - cases: Normalized case entity                         |
|     - judicial_documents: Interlocutory/final orders        |
|     - hearing_events: Sequential hearing timeline           |
|     - LegalKnowledgeGraph: Interpretation & Precedent edges |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|  4. Integrity Auditing & Review Escalation                  |
|     - FTS5 Full-Text Search indexing                        |
|     - LegalReviewStatus assignment (UNVERIFIED_AUTOMATED)   |
|     - Frozen Pilot quarantine boundary enforcement          |
+-------------------------------------------------------------+
```

---

## 2. Chunking Methodology for Judicial Precedents

To enable high-precision retrieval without context hallucination, judicial judgments are decomposed into distinct functional chunk types:

1. **`ChunkHierarchy.RATIO`**:
   The binding legal principle laid down by the court that forms the necessary ground of the decision.
2. **`ChunkHierarchy.HOLDING`**:
   The specific legal and factual determination applying the ratio to the dispute at hand.
3. **`ChunkHierarchy.PROVISO` / `PARAGRAPH`**:
   Verbatim key passages from the judgment containing judicial rationale, distinguishing analysis, or interpretation of statutory clauses.

---

## 3. High Court Ingestion Module (`delhi_high_court_phase26.py`)

The Phase 26 module implements deterministic builder methods:
- `build_christian_louboutin_judgment()`
- `build_christian_louboutin_case()`
- `build_christian_louboutin_documents()`
- `build_tata_greenpeace_judgment()`
- `build_tata_greenpeace_case()`
- `build_tata_greenpeace_documents()`

Each builder populates the complete schema with zero simulated citations, real party names, authentic bench names, and accurate disposal dates.

---

## 4. Execution & Audit Log

Ingestion executed via `scripts/run_phase26_delhi_hc.py` produced:
- Ingestion report: `data/08_corpus/phase26_delhi_hc_ingestion_report.json`
- Total registered sources: 59 (+2)
- Total chunks: 1,503 (+8)
- Total cases: 16 (+2)
- Total judicial documents: 9 (+2)
- Total hearing events: 8 (+2)
- Quarantined scaffold count: 6 (constant)
- Zero database constraint errors or foreign key violations.
