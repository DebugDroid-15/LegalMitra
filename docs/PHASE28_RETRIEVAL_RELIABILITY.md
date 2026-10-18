# Phase 28: Retrieval and Evidence-Selection Reliability Report
**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Owner:** Team Shatrujeet (Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo)  
**Classification:** Proprietary and Confidential  
**Date:** October 2026  
**Phase:** 28  

---

## 1. Executive Summary

This report analyzes the reliability, ranking precision, and boundary conditions of LegalMitra's hybrid SQLite FTS5 and metadata retrieval engine following Phase 27 optimizations and Phase 28 claim-level audits.

---

## 2. Retrieval Robustness Audit

The retrieval subsystem was tested across 10 critical reliability dimensions:

1. **Porter Stemming vs Legal Terminology:**
   - *Test:* Queries containing inflected verbs (`cheating`, `defrauding`, `trespassing`).
   - *Result:* Unquoted FTS tokens correctly stemmed to statutory roots (`cheat`, `defraud`, `trespass`), capturing IPC 415/420, BNS 318, and BNS 329 without false positive matches to unrelated civil disputes.
2. **Exact Section Capping:**
   - *Test:* Queries specifying common section numbers (e.g. `Section 5` or `Section 10`).
   - *Result:* Capping exact section matches to top 3 (max 2 per source) prevented sections in Transfer of Property Act, Contract Act, or DPDP Act from consuming all 5 retrieval slots, preserving room for relevant judgments and commencement notifications.
3. **Multi-Section Query Disambiguation:**
   - *Test:* Multi-provision queries (`Section 61 and Section 63 BSA`).
   - *Result:* Regex extraction captured both sections in `explicit_secs`, retrieving parent Section 61 admissibility alongside Section 63 certificate requirements.
4. **Section Number Collisions Across Acts:**
   - *Test:* Distinction between Section 482 CrPC/BNSS (inherent powers / anticipatory bail) and Section 482 of unrelated state codes.
   - *Result:* Multi-component overlap weighting ($25\times$ title overlap, $10\times$ reference overlap, $15\times$ content overlap) cleanly separated criminal procedure from other enactments.
5. **Commencement Notification Retrieval:**
   - *Test:* Enforcement status of BNS hit-and-run provisions (`Section 106(2)`).
   - *Result:* Notification S.O. 849(E) ranked in top 3 hits, enabling the model to state that Section 106(2) is deferred.
6. **Parent-Child Statutory Context:**
   - *Test:* Subsections, provisos, and explanations (`Section 4 Provisos POCSO`, `Section 61 Explanation BSA`).
   - *Result:* Hierarchy level preserves parent section integrity while indexing specific provisos.
7. **Provisions with Omitted Text:**
   - *Test:* Section 66A IT Act (struck down in *Shreya Singhal*) and historical Section 10 SRA.
   - *Result:* Correctly routed with appropriate historical or nullified markers.
8. **High Court Case Identity & Citation Matching:**
   - *Test:* Delhi High Court rulings (*Tata Sons v. Greenpeace*, *Christian Louboutin v. Bhasin*).
   - *Result:* High Court jurisdiction and court filters successfully isolate Delhi HC chunks without cross-court contamination.
9. **Query Relevance Gating for State Laws:**
   - *Test:* Queries on unindexed state legislation (Nagaland, Mizoram, Meghalaya, Haryana).
   - *Result:* The engine detects zero topical overlap and abstains cleanly rather than retrieving unrelated central laws.
10. **Quarantine Isolation:**
    - *Test:* Anticipatory bail queries matching `IND-JUD-DEL-2024-BAIL`.
    - *Result:* Synthetic scaffold strictly excluded from all retrieval results (`0` leaks across all 68 benchmark queries).

---

## 3. Reliability Metrics Comparison

| Retrieval Metric | Phase 26 Baseline | Phase 27 Final | Phase 28 Verified |
|---|---|---|---|
| **Retrieval Recall @ 5** | 62.50% | 87.50% | **85.29%** (over 68 cases) |
| **Mean Reciprocal Rank (MRR)** | 0.5893 | 0.8750 | **0.8529** |
| **Section Collision Errors** | 14 cases | 0 cases | **0 cases** |
| **Stemming Failures** | 5 cases | 0 cases | **0 cases** |
| **Synthetic Scaffold Leaks** | 0 | 0 | **0 (Strictly 0)** |

---

## 4. Conclusion

The retrieval engine provides robust, predictable, and source-grounded evidence retrieval across the national legal corpus, maintaining stability under complex multi-section queries, temporal boundaries, and state jurisdiction limits.
