# LegalMitra Data Storage, Search, and Retrieval Architecture

**System Architecture Specification — Phase 14G**  
**Version:** 1.0.0  
**Engine Implementation:** `legalmitra/knowledge/knowledge_base.py`  
**Database File:** `data/legalmitra_kb.db`  
**Classification:** Core Storage, FTS5 Indexing & Multi-Filter Retrieval Engine

---

## 1. Storage Layer Design

LegalMitra uses a dual-engine architecture:
- **SQLite 3 + FTS5:** High-performance, portable, deterministic relational and full-text search database.
- **Physical Isolation:** `data/legalmitra_kb.db` (Public Knowledge Base) is physically segregated from `data/conversations.db` (User Sessions & Feedback), preventing data leakage and privacy breaches.

### Schema Structure:
- `sources`: Master table containing document IDs, titles, URLs, document types, jurisdiction, court, document dates, effective dates, checksums, and quarantine flags.
- `legal_chunks`: Granular legislative and case-law chunks preserving:
  - `chunk_id`: Hierarchical key (e.g. `IND-STAT-BNSS-2023:SEC:531:SUB:2:CLAUSE:a`).
  - `source_id`: Foreign key to `sources`.
  - `hierarchy_level`: `SECTION`, `SUBSECTION`, `PROVISO`, `EXPLANATION`, `RATIO`, `HOLDING`, `PARAGRAPH`.
  - `authority_level`: `BINDING_STATUTE`, `BINDING_PRECEDENT`, `PERSUASIVE_PRECEDENT`, `SUBORDINATE_RULE`.
  - `is_synthetic_scaffold`: Flag enforcing permanent exclusion of test scaffolds.
- `legal_chunks_fts`: SQLite FTS5 virtual table indexing `content`, `title`, `act_or_case_title`, and `provision_or_para_ref` with Porter stemmer and BM25 ranking.

---

## 2. Multi-Filter Query Engine

The retrieval pipeline supports combined faceted searches via `SearchFilters`:
1. **Full-Text BM25 Search:** Matches legal terms across titles, section headers, and verbatim statutory bodies.
2. **Exact Statutory Lookup:** Fast direct lookups by `(statute_id, section_number)`.
3. **Temporal Point-in-Time Filtering:** `as_of_date` filter excluding provisions whose commencement date is subsequent to the queried date or whose repeal date precedes it.
4. **Jurisdiction Filtering:** Central (`IN`) vs State (`IN-DL`, `IN-MH`, etc.).
5. **Authority Re-ranking:** Weighted scoring elevating Supreme Court Constitution Benches and Central Acts over subordinate or persuasive orders.
6. **Mandatory Quarantine Exclusion:** Query invariant `WHERE is_synthetic_scaffold = 0`.

