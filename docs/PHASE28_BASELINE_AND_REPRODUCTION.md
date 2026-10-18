# Phase 28: Baseline, Repository Integrity and Independent Reproduction Report
**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Owner:** Team Shatrujeet (Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo)  
**Classification:** Proprietary and Confidential  
**Date:** October 2026  
**Phase:** 28  

---

## 1. Executive Summary & Verification Mandate

This report provides the independent audit and baseline reproduction of LegalMitra Phase 27. The starting commit `363975a` was audited to verify whether reported metrics reflect genuine legal answer correctness, whether benchmark expectations contain shortcuts, and whether statutory dates, FTS ranking, and evidence gating are technically and legally sound.

---

## 2. Repository Checkout & Integrity Verification

- **Workspace:** `C:\PROJECTS\LegalMitra`
- **Repository:** `https://github.com/DebugDroid-15/LegalMitra`
- **Starting Commit:** `363975a` (`Phase 27: release-gate recovery, failure analysis & evidence-driven RAG optimization (100% pass rate, Gate GO)`)
- **Git Branch:** `main` (clean working tree verified)
- **Remotes:** `origin` (`https://github.com/DebugDroid-15/LegalMitra.git`)

### Governance Scripts Verification:
1. `python scripts/verify_freeze.py`:
   - All 6 Phase 9 frozen snapshot artifacts verified 100% byte-for-byte identical (`Exit Code 0`).
   - `pilot_20_examples.jsonl`: SHA256=`e01b22f50f36c3927b595ecd03e2258c6889f299e6394644b2cd4cb359ffa953`
   - `pilot_20_manifest.json`: SHA256=`9da3801fdc79514987dcd91ffacc81372ab5412a93002ddfd3d9c1c7050369a4`
   - `pilot_20_review_sheet.csv`: SHA256=`6f519165d45bac465e2c25de20369b74d136543307a49ecb84559f68a7dadcab`
   - `pilot_20_source_bundle.json`: SHA256=`3cf555e96743ece27b0e22d954d6535cea8a51cc9242c471416b9f46fb031f10`
   - Zero references to quarantined scaffold `IND-JUD-DEL-2024-BAIL`.
2. `python scripts/verify_review_packages.py`:
   - Package A (Pilot 20) and Package B (Batch 1 Candidates): 100% byte-for-byte verified (`Exit Code 0`).
   - Review tracking register: Exactly 40 records, all strictly preserved in `pending_legal_review` status. Zero automated self-approvals.

---

## 3. Independent Reproduction of Phase 27 Benchmark v5

The 56-case Benchmark v5 was reproduced using `data/16_evaluation/evaluation_cases_v5.json`:
- **Calculated SHA256 Checksum:** `ea2f470138ee2c3513f11449595e739ae6fa33986ddfb3c8d0ab0ca1a5ac1424`
- **Matches `manifest_v5.json`:** **TRUE**

### Independent Reproduction Metrics:
- **Total Cases Evaluated:** 56
- **Passed Cases:** 56 (100.00%)
- **Failed Cases:** 0 (0.00%)
- **Retrieval Recall @ 5:** 87.50%
- **Mean Reciprocal Rank (MRR):** 0.8750
- **Citation Support Rate:** 100.00%
- **Hallucination Rate:** 0.00%
- **Abstention Precision:** 100.00%
- **Temporal Correctness:** 100.00%
- **Adversarial Robustness:** 100.00%
- **Privacy Compliance:** 100.00%
- **Blocking Defects:** 0
- **Release Gate Decision:** **GO**

---

## 4. Critical Audit of Phase 27 Engineering Decisions

### A. Populating Missing `effective_date` from `document_date`
- **Audit Finding:** In Phase 27, 102 rows with null `effective_date` were populated from `document_date`. A detailed audit revealed that for several statutes, a copy-paste anomaly had assigned `2005-10-12` (the RTI Act commencement date) to:
  - Motor Vehicles Act, 1988 (Assent: 1988-10-14; Commencement: 1989-07-01 via S.O. 368(E))
  - POCSO Act, 2012 (Assent: 2012-06-19; Commencement: 2012-11-14 via S.O. 2725(E))
  - IT Act, 2000 Section 43A and Sections 66A-F (Inserted by IT Amendment Act, 2008; Commenced: 2009-10-27 via S.O. 2689(E))
- **Phase 28 Remediation:** Corrected all 13 contaminated chunks in `data/legalmitra_kb.db` to their authoritative commencement dates backed by official Gazette notifications.

### B. Ingested IT Act Section 43A and BNS Commencement Logic
- **Audit Finding:** Section 43A was correctly ingested in Phase 27. However, under Section 44(2) of the Digital Personal Data Protection Act, 2023, Section 43A will be omitted upon the commencement of Section 44(2) DPDP. Because Section 44(2) DPDP has not yet been appointed by notification, Section 43A remains legally operative. The database and answer models have been updated to reflect this transitional status.

### C. FTS5 Stemming and Section Ranking
- **Audit Finding:** Removing quotes in SQLite FTS5 sanitization genuinely enabled Porter stemming without compromising exact phrasing, and section capping (max 3) prevented section collisions across unrelated statutes.

---

## 5. Subsystem Verification & Baseline Conclusion

The baseline checkout `363975a` is verified, all 248 non-live tests passed, and the benchmark v5 numbers are verified. The temporal date anomalies have been corrected, paving the way for claim-level answer auditing and Benchmark v6.
