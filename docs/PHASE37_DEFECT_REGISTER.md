# Phase 37 Defect & Blocker Register

**Project:** LegalMitra  
**Phase:** 37 — Authorized National Corpus Acquisition, Hindi Legal Data Expansion & Milestone B Readiness  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** ACTIVE REGISTER  

---

## 1. Executive Summary

The Defect & Blocker Register provides continuous tracking of technical, security, legal, and operational blockers identified during Phase 37 execution. In accordance with project integrity standards, blockers are transparently documented rather than concealed or bypassed.

---

## 2. Active Defect & Blocker Items

| Defect ID | Severity | Category | Blocker Description | Operational Impact | Mitigation / Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DEF-P37-01** | HIGH | Network / CDN | `indiacode.nic.in` returns HTTP 403 Forbidden to programmatic requests due to Akamai EdgeShield bot management. | Automated crawling blocked without browser session spoofing. | **RESOLVED COMPLIANTLY:** Enforce Rule 11 (no bot-evasion); ingest bare gazette extracts and open gazette repositories. |
| **DEF-P37-02** | HIGH | PKI / TLS | `legislative.gov.in` TLS certificate chain signed by CCA India intermediate CA, failing standard Mozilla/OpenSSL `certifi` bundle. | Programmatic HTTPS requests fail SSL verification. | **RESOLVED COMPLIANTLY:** Enforce Rule 11 (no disabling SSL verification); utilize authorized gazette channels with standard trusted PKI. |
| **DEF-P37-03** | CRITICAL | Machine Learning | Token deficit of 642,642 tokens against Milestone B (1,000,000 tokens), and 590x deficit against 10M Chinchilla scaling heuristic. | 10M+ foundation model pretraining would suffer catastrophic overfitting. | **ACTIVE POLICY GATE:** Large-scale pretraining (10M, 50M, 125M, 1.3B) remains **STRICT NO-GO**. Controlled 1.07M regression runs permitted. |
| **DEF-P37-04** | MEDIUM | Legal / Regulatory | Section 106(2) of Bharatiya Nyaya Sanhita, 2023 (hit-and-run penalty) remained uncommenced under Notification S.O. 850(E). | Uncommenced statutory section must not be represented as in force. | **RESOLVED:** Version ledger and annotations explicitly flag Section 106(2) as uncommenced as of July 1, 2024. |
| **DEF-P37-05** | MEDIUM | Invariant / Freeze | Six Phase 9 frozen review artifacts must maintain bitwise identical SHA-256 manifests across all phases. | Any unintentional file edit would violate freeze protocol. | **MONITORED:** `scripts/verify_freeze.py` executed and passing bitwise identical (6/6 match). |
| **DEF-P37-06** | MEDIUM | Human Review | 40 advocate-review candidate records in `review_tracking_register.json` remain pending legal review. | Candidates cannot be exported into pretraining manifests or active RAG. | **MONITORED:** `scripts/verify_review_packages.py` executed and passing; 40/40 strictly pending. |
| **DEF-P37-07** | HIGH | Data Quarantine | Synthetic scaffold fixture `IND-JUD-DEL-2024-BAIL` (6 chunks in KB) must never leak into training manifests. | Synthetic hallucinated legal text would pollute pretraining. | **ENFORCED:** `legalmitra_kb.db` query explicitly filters `is_synthetic_scaffold = 0`; 0 chunks exported. |

---

## 3. Resolution Verification Summary

All seven tracked defects are either compliantly resolved through authorized alternatives or strictly enforced via automated testing and architectural invariants. Zero security or rights violations occurred during Phase 37.

