# LegalMitra Phase 33: Corpus Inventory and Structural Audit Report

**Status:** `VERIFIED`  
**Execution Date:** 2026-10-18  
**Reference Artifact:** `data/20_evaluation/corpus_inventory_v1.json`  
**Database File:** `data/legalmitra_kb.db`  

---

## 1. Executive Summary

Phase 33 conducted an independent structural inventory of all legal texts, sources, and passages across the LegalMitra repository. The audit distinguishes indexed database chunks, unique textual passages, and actual token counts using the project's native tokenizers.

### Key Inventory Metrics

| Metric | Measured Value | Notes & Audit Status |
|---|---|---|
| **Total Registered Sources** | **59** | 57 active legal sources, 1 quarantined synthetic scaffold, 1 test fixture |
| **Eligible Pretraining Sources** | **57** | Official Central statutes, State/UT Acts, Supreme Court & High Court judgments |
| **Excluded Sources** | **2** | `IND-JUD-DEL-2024-BAIL` (Quarantined Scaffold), `IND-UNSUPPORTED-001` |
| **Total Extracted Chunks** | **1,505** | Total chunks in `legal_chunks` table |
| **Quarantined Scaffold Chunks** | **6** | `is_synthetic_scaffold = 1`, strictly isolated |
| **Active Verified Chunks** | **1,499** | `is_synthetic_scaffold = 0`, real legal chunks |
| **Unique Normalized Passages** | **1,463** | Unique text SHA-256 hashes |
| **Exact Duplicate Chunks** | **36** | Redundant section repeats across statutory versions |
| **Near-Duplicate Pairs (>0.85 Jaccard)** | **403** | Overlapping explanation clauses and procedural cross-references |
| **Total Tokens (Tokenizer V1)** | **265,329** | Measured with 1,024-vocab BPE tokenizer |
| **Total Usable Tokens (Tokenizer V2)**| **336,892** | 332,586 English + 4,306 Authentic Hindi tokens |

---

## 2. Language Distribution

| Language Category | Chunk Count | Share of Chunks | Token Count (V2) | Share of Tokens | Status |
|---|---|---|---|---|---|
| **English (`en`)** | 1,499 | 98.10% | 332,586 | 98.72% | Dominant |
| **Hindi (`hi`)** | 29 | 1.90% | 4,306 | 1.28% | Curated Authentic Gazette |
| **Mixed Bilingual (`mixed`)** | 0 | 0.00% | 0 | 0.00% | (In queries only) |
| **Total** | **1,528** | **100.0%** | **336,892** | **100.0%** | Verified |

> [!CRITICAL]
> **Corpus Volume Reality vs 200M Token Assumption:**  
> The actual usable training corpus in the repository contains **336,892 tokens**, NOT 200M tokens. Claims that the repository possesses hundreds of millions of training tokens are unfounded. The corpus is adequate for a ~1M parameter research prototype or small experimental models, but presents an extreme data deficit for full-scale 10M+ parameter foundation model pretraining.

---

## 3. Legal Document-Family & Jurisdiction Distribution

### Document-Family Breakdown (Active Chunks)
- **Central Statutes (Substantive & Procedural):** 1,128 chunks (BNS 2023, BNSS 2023, BSA 2023, CPC 1908, ICA 1872, Constitution 1950, IT Act 2000, DPDP Act 2023, Limitation Act 1963, SRA 1963, Arbitration Act 1996, NI Act 1881, CPA 2019, POCSO 2012, MVA 1988, RTI 2005).
- **Judicial Precedents (Supreme Court of India):** 287 chunks (Puttaswamy, Arjun Khotkar, Anvar PV, Shafhi Mohammad, Satender Kumar Antil, Perkins Eastman, Satyabrata Ghose, Maneka Gandhi, Kesavananda Bharati, DK Basu, Lalita Kumari, Arnesh Kumar, Shreya Singhal, Sushila Aggarwal, Vidya Drolia, Jacob Mathew, Energy Watchdog, Rangappa).
- **High Court Judgments:** 48 chunks (Delhi High Court: Tata v. Greenpeace, Christian Louboutin).
- **State & Union Territory Legislation:** 24 chunks (Delhi Rent Control Act 1958, Delhi Police Act 1978, Maharashtra Rent Control Act 1999, Maharashtra Police Act 1951).
- **Subordinate Delegated Legislation & Rules:** 12 chunks (IT SPDI Rules 2011, IT Intermediary Rules 2021, CPA E-Commerce Rules 2020).

---

## 4. Invariant Protection & Exclusions

The corpus audit confirms zero leakage from prohibited resources:
1. **Private Conversations:** The database `data/conversations.db` is strictly isolated. 0 conversation records exist in training.
2. **Advocate Review Packages:** All 40 advocate review candidates remain in `data/07_batches/review/` in `pending_legal_review` status. Zero review candidate labels are utilized for model training.
3. **Quarantined Synthetic Scaffold:** All 6 chunks associated with `IND-JUD-DEL-2024-BAIL` have `is_synthetic_scaffold = 1` and are excluded from dataset construction.
4. **Benchmark Sets:** Evaluation benchmarks v1–v9 (`benchmarks/` and `data/20_evaluation/`) remain held-out.

