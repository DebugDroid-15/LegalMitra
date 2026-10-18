# Phase 35 Defect Register & Resolution Tracking

**Project:** LegalMitra  
**Phase:** 35 — National Legal Data Engine, Source Verification & Corpus Scaling Infrastructure  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** VERIFIED  

---

## 1. Defect Log Summary

| Defect ID | Description | Component | Severity | Resolution Status | Verified Fix |
|---|---|---|---|---|---|
| `DEF-35-01` | Atomic file replace on Windows raised `PermissionError: [WinError 5] Access is denied` during high-frequency FSM state transitions | `legalmitra/corpus/source_registry_engine.py` | HIGH | RESOLVED | Added exception handling with direct write fallback and `auto_save=False` parameter for batch FSM operations |
| `DEF-35-02` | Section pattern regex failed on statutory lines containing periods after the section number (e.g. `Section 1. Title`) | `legalmitra/corpus/legal_parser.py` | MEDIUM | RESOLVED | Updated `SECTION_PATTERN_EN` and `SECTION_PATTERN_HI` to make period optional `(?:Section\s+(\d+[A-Z]?)\.?\|(\d+[A-Z]?)\.)` |
| `DEF-35-03` | Header/footer defect detection was executed against already-cleaned text rather than raw text, masking contamination artifacts | `legalmitra/corpus/legal_parser.py` | MEDIUM | RESOLVED | Passed `raw_text` to `detect_defects` before normalisation in `parse_statute` and `parse_judgment` |
| `DEF-35-04` | Pre-existing token deficit (615x vs Chinchilla 211M) for 10.55M model pretraining | Pretraining Planning | HIGH | MANAGED / BLOCKED | Implemented strict scaling gate prohibiting 10M, 125M, and 1.3B training runs until Milestone D (50M tokens) is reached |

---

## 2. Invariant Tracking Register

| Invariant | Requirement | Verified State |
|---|---|---|
| Phase 9 Frozen Assets | 6 files must remain byte-for-byte identical | **VERIFIED BITWISE** (All 6 SHA-256 digests match) |
| Advocate Review Candidates | 40 candidates must remain pending | **VERIFIED BITWISE** (20 Package A + 20 Package B pending) |
| Synthetic Scaffold | 6 chunks (`IND-JUD-DEL-2024-BAIL`) quarantined | **VERIFIED QUARANTINED** (Excluded from export manifests) |
| Database Separation | `data/legalmitra_kb.db` vs `data/conversations.db` | **VERIFIED ISOLATED** (Zero cross-database dependencies) |
| Benchmarks | Benchmark cases and thresholds remain unchanged | **VERIFIED UNCHANGED** |
