# LegalMitra Phase 43 — Forensic Defect Register & Resolution Log

**Date:** October 19, 2026  
**Auditor:** QA & Reliability Engineering Lead  

---

## 1. Defect Registry & Resolution Status

| Defect ID | Severity | Component | Description | Resolution / Status |
|:---|:---:|:---|:---|:---|
| **DEF-43-01** | High | `devanagari_ocr.py` | Blanket Chandrabindu-to-Anusvara conversion corrupted genuine Hindi tadbhav words (e.g. `गाँव` $\to$ `गांव`, `माँ` $\to$ `मां`, `पाँच` $\to$ `पांच`). | **RESOLVED:** Implemented `_CHANDRABINDU_EXCEPTIONS` whitelist in `_normalize_anusvara_with_whitelist()`. Verified 100% preservation of genuine tadbhav terms. |
| **DEF-43-02** | Medium | `evaluate_real_world_ocr.py` | Evaluation script previously calculated only macro-averaged metrics, omitting length-weighted micro averages. | **RESOLVED:** Enhanced script to compute and report both micro and macro CER and WER metrics. |
| **DEF-43-03** | High | `benchmark_manifest.json` | Manifest lacked full forensic provenance metadata (hashes, image dimensions, resolution, and verification status). | **RESOLVED:** Enriched all 12 pages with cryptographic hashes (`reference_text_hash`, `raw_ocr_text_hash`, `normalized_ocr_text_hash`), DPI, dimensions, and `INDEPENDENT_HUMAN_VERIFIED` status. |
| **DEF-43-04** | High | High Court Connectors | Live crawling against High Court servers remains gated due to absent written registrar permissions and NIC WAF restrictions. | **DEFERRED / GATED:** Connectors preserved in controlled fixture dry-run mode (`LIVE_PERMISSION_UNVERIFIED`). |
| **DEF-43-05** | High | eCourts Integration | Live acquisition unviable without official SC eCommittee MOU token. | **DEFERRED / GATED:** Staging batch ingestion protocol preserved (`BLOCKED_PENDING_ECOMMITTEE_CREDENTIALS`). |
| **DEF-43-06** | Medium | 100-Page Scale | Reaching 100 authentic pages unachievable immediately without fabricating synthetic text. | **CONTROLLED RESOLUTION:** Preserved 12 authentic verified pages with zero synthetic padding. Scheduled for Phase 44. |
