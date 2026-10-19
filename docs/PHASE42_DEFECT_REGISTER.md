# LegalMitra Phase 42 — Forensic Defect Register & Resolution Log

**Date:** October 19, 2026  
**Auditor:** QA & Reliability Engineering Lead  

---

## 1. Active, Resolved & Deferred Defect Registry

| Defect ID | Severity | Component | Description | Resolution / Status |
|:---|:---:|:---|:---|:---|
| **DEF-42-01** | High | `ecourts_protocol.py` | CNR validation lacked semantic checks, allowing non-existent state codes (e.g. `ZZ`) to pass validation. | **RESOLVED:** Added `validate_cnr_semantic()` enforcing 20-jurisdiction official state code table and establishment checks. |
| **DEF-42-02** | High | `ecourts_adapter.py` | eCourts adapter previously lacked institutional token header handlers and local staging fallback. | **RESOLVED:** Implemented `AuthorizedECourtsAdapter` supporting bearer tokens and explicit `BLOCKED_PENDING_ECOMMITTEE_CREDENTIALS` gating. |
| **DEF-42-03** | Medium | `devanagari_ocr.py` | Devanagari OCR failed to normalize chandrabindu (`\u0901`) before consonants, degrading legal token sensitivity in words like `सँविधान`. | **RESOLVED:** Added context-aware anusvara normalization rule; legal token sensitivity reached 100.0%. |
| **DEF-42-04** | Medium | `evaluate_real_world_ocr.py` | Key naming discrepancy (`avg_cer_norm` vs `avg_cer_normalized`) caused script runtime failure on first run. | **RESOLVED:** Fixed key mappings and standardized Levenshtein distance calculations. |
| **DEF-42-05** | High | High Court Connectors | Live automated crawling against High Court portals unviable due to NIC WAF 403 blocks and absent written permissions. | **DEFERRED / GATED:** Connectors operate in controlled fixture mode with explicit blocker `LIVE_PERMISSION_UNVERIFIED`. |
| **DEF-42-06** | Medium | OCR Benchmark Scale | 100-page target unachievable immediately without fabricating unverified synthetic text. | **CONTROLLED RESOLUTION:** Staged 12 fully authentic, verified pages with zero synthetic padding; scheduled 100-page expansion for Phase 43. |
