# Phase 58 Complete Defect Register & Resolution Ledger

**Phase:** LEGALMITRA-PHASE58  
**Audit Status:** Complete & Verified  

---

## Defect Inventory & Resolution Details

| Defect ID | Severity | Component | Problem Statement | Resolution Details | Verification Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DEF-58-01** | High | `independent_evaluator.py` | Column names `title` and `citation` queried in `legal_chunks` did not exist, throwing swallowed `OperationalError` and causing false accusations of fabricated citations. | Corrected columns to `act_or_case_title` and `provision_or_para_ref`. Expanded regex patterns for Indian statutes and precedents. | Trustworthiness on held-out sample restored from 0.59 to 0.9711. Tested in `test_phase57_independent_evaluation.py`. |
| **DEF-58-02** | High | `release_gates.py` | Gates RG-03, RG-05, RG-06, and RG-09 were static declarations returning `GateStatus.PASSED` without dynamic checks. | Implemented dynamic checks via `build_national_judicial_knowledge_graph`, pipeline execution on negative fixtures, and SHA-256 freeze checks. | Tested in `TestPhase58ReleaseGateNegativeControls` (6 negative control tests passing). |
| **DEF-58-03** | Medium | `differential_evaluator.py` | Newly added benchmark cases (PIT-213 to PIT-240) were silently discarded from differential comparison. | Added separate tracking for `newly_added_cases` and enforced detection of 10 critical safety regression invariants. | Tested in `test_differential_separation_of_newly_added_cases` and 10 safety invariant unit tests. |
| **DEF-58-04** | Medium | `temporal_benchmark_manifest.json` | 5 dispute scenarios recurred across development and held-out splits. | Documented recurrence of legitimate legal dispute patterns across distinct facts; verified split isolation. | Documented in `PHASE58_CONTAMINATION_FINDINGS.md`. |
