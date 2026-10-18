# Phase 36 Source Registry Reconciliation Report

**Project:** LegalMitra  
**Phase:** 36 — Corpus Eligibility Audit, Hindi Primary-Source Acquisition & Dataset Integrity  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** VERIFIED  

---

## 1. Executive Summary

A core question posed in the Phase 36 mandate is: **Why are 111 records tracked in the unified source registry, but only 33 reported as training-eligible?**

Phase 36 performed an individual, record-by-record audit of all 111 sources, reconciling the high-level legal universe inventory against actual database chunks, raw downloaded files, and pretraining manifests. The results are captured machine-readably in `data/09_national_corpus/source_eligibility_ledger.json`.

---

## 2. Source Registry Composition Analysis

The 111 tracked source records in `data/09_national_corpus/unified_source_registry.json` break down into four distinct categories:

```
Total Tracked Records: 111
├── (1) Physically Indexed & Training Eligible: 33 (30.0%)
├── (2) Legal Universe Catalog (Unindexed / 0 Chunks): 67 (60.4%)
├── (3) Priority Discovery Candidates (Pending Acquisition): 10 (9.0%)
└── (4) Synthetic Test Fixture (Strictly Quarantined): 1 (0.9%)
```

### Detailed Breakdown:

| Category | Record Count | FSM Lifecycle State | Physical Evidence State | RAG Retrieval Eligible | Pretraining Eligible |
|---|---|---|---|---|---|
| **Primary Indexed Universe Statutes** | 33 | `TRAINING_ELIGIBLE` | Chunks present in `legalmitra_kb.db` (1,499 chunks) | **YES** | **YES** |
| **Cataloged Universe Backlog** | 67 | `RIGHTS_REVIEWED` | Catalog only (`expected_to_exist`); **0 chunks** | **NO** | **NO** |
| **National Discovery Candidates** | 10 | `REGISTERED` | URL identified; **pending acquisition batch** | **NO** | **NO** |
| **Synthetic Scaffold Fixture** | 1 | `QUARANTINED` | 6 chunks in KB; strictly isolated | **NO** | **NO** |
| **Total** | **111** | — | — | **33** | **33** |

---

## 3. The 111 vs 33 Reconciliation Explained

1. **Why are only 33 reported training-eligible?**  
   Because only 33 primary statutory universe instruments (e.g. `UNIV-CONST-1950`, `UNIV-ACT-BNS-2023`, `UNIV-ACT-BNSS-2023`, `UNIV-ACT-BSA-2023`, `UNIV-ACT-CPC-1908`, `UNIV-ACT-ICA-1872`, `UNIV-ACT-IT-2000`) have had their text physically extracted, validated, and indexed into actual chunks.
2. **What are the remaining 78 records?**  
   - **67 records** represent the unindexed statutory universe inventory (e.g. Constitutional Amendments 42nd, 44th, 86th, 101st; regional state acts). Their legal rights under Section 52(1)(q) have been reviewed conceptually, but because no physical text has been extracted, they possess **0 chunks** and are rightfully blocked from pretraining manifests.
   - **10 records** represent newly discovered national candidates (including the three Hindi criminal codes) cataloged in Phase 35, which await physical acquisition batches.
   - **1 record** is `UNIV-SCAFFOLD-DEL-2024-BAIL`, which is an adversarial test fixture that must never be trained on.

---

## 4. Evidentiary States vs Conceptual Registry States

Phase 36 formally establishes that conceptual registry states must never be conflated with physical evidence states:

$$\text{DISCOVERED} \neq \text{REGISTERED} \neq \text{ACQUIRED} \neq \text{PARSED} \neq \text{AUTHENTICITY\_VERIFIED} \neq \text{RIGHTS\_REVIEWED} \neq \text{TRAINING\_ELIGIBLE}$$

### Evidence Completeness Scores in Ledger:
- **1.0 (Full Evidence):** 33 records. Physical text exists, SHA-256 verified, indexed in `legal_chunks`, included in manifests.
- **0.4 (Catalog Only):** 67 records. Legislative metadata cataloged from official universe inventory; zero physical text downloaded.
- **0.2 (Candidate Only):** 10 records. Official portal URL cataloged; download blocked or pending acquisition.
- **1.0 (Quarantined Evidence):** 1 record (`UNIV-SCAFFOLD-DEL-2024-BAIL`). Physical text exists, but legally quarantined.

The complete record-by-record ledger is maintained at [`data/09_national_corpus/source_eligibility_ledger.json`](file:///c:/PROJECTS/LegalMitra/data/09_national_corpus/source_eligibility_ledger.json).
