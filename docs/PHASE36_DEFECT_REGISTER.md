# Phase 36 Defect Register & Technical Issue Audit

**Project:** LegalMitra  
**Phase:** 36 — Corpus Eligibility Audit, Hindi Primary-Source Acquisition & Dataset Integrity  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** VERIFIED  

---

## 1. Defect & Blocker Tracking Register

| Defect / Blocker ID | Description & Evidence | Component | Severity | Resolution Status | Verified Remediation |
|---|---|---|---|---|---|
| `BLK-36-01` | Programmatic automated HTTP acquisition from `indiacode.nic.in` returns `HTTP 403 Forbidden` due to Akamai CDN EdgeShield bot detection. | `legalmitra/corpus/secure_acquisition_engine.py` | HIGH | DOCUMENTED & BLOCKED | Complied with Rule 11 (no bot-evasion or fake headers). Recorded candidate status as blocked; scheduled for manual Gazette bundle ingestion in Phase 37. |
| `BLK-36-02` | Programmatic HTTPS requests to `legislative.gov.in` fail TLS certificate verification with `[SSL: CERTIFICATE_VERIFY_FAILED]` because CCA India intermediate CA is not in Mozilla/OpenSSL `certifi` store. | `legalmitra/corpus/secure_acquisition_engine.py` | HIGH | DOCUMENTED & MANAGED | Complied with Rule 11 (SSL verification not disabled). Documented requirement to provision CCA India root certificate bundle into local engine store in Phase 37. |
| `DEF-36-01` | Discrepancy between recorded checkpoint SHA-256 in `model_experiment_results_v4.json` (`4fea1cfa...`) and actual saved file `phase35_1m_baseline_regression.pt` (`984dc882...`). | `scripts/run_phase35_small_model_regression.py` | MEDIUM | RESOLVED & AUDITED | Phase 36 reproduction script confirmed exact val loss ($5.6607$) and recorded true file digest in `data/20_evaluation/model_regression_reproduction_phase36.json`. |
| `DEF-36-02` | `TrainingCorpusExporter` lacked overwrite guard, allowing accidental overwriting of historical versioned manifests if called with the same version tag. | `legalmitra/corpus/training_exporter.py` | MEDIUM | RESOLVED | Added explicit immutability check raising `FileExistsError` if target manifest exists unless `overwrite=True` is explicitly passed. |
| `DEF-36-03` | Python command line output on Windows CMD defaulted to CP1252, causing `UnicodeEncodeError` when printing Devanagari Hindi text directly. | Local Environment / CLI | LOW | RESOLVED | Configured UTF-8 stdout encoding (`sys.stdout.reconfigure(encoding='utf-8')`) in all runner scripts. |

---

## 2. Invariant Tracking Register

| Invariant | Requirement | Verified State |
|---|---|---|
| Phase 9 Frozen Assets | 6 files must remain byte-for-byte identical | **VERIFIED BITWISE** (All 6 SHA-256 digests match) |
| Advocate Review Candidates | 40 candidates must remain pending | **VERIFIED BITWISE** (20 Package A + 20 Package B pending) |
| Synthetic Scaffold | 6 chunks (`IND-JUD-DEL-2024-BAIL`) quarantined | **VERIFIED QUARANTINED** (0 chunks in pretraining manifests) |
| Database Separation | `data/legalmitra_kb.db` vs `data/conversations.db` | **VERIFIED ISOLATED** (Zero cross-database dependencies) |
| Benchmarks | Benchmark cases and thresholds remain unchanged | **VERIFIED UNCHANGED** |
