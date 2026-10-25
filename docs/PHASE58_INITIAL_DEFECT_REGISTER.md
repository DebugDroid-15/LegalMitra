# Phase 58 Initial Defect Register

**Phase:** LEGALMITRA-PHASE58  
**Audit Scope:** Evaluator Independence, Benchmark Validity, Release Gates  
**Status:** All 4 initial defects triaged and remediated.

---

## Defect Summary Table

| Defect ID | Severity | Category | Component | Description | Remediation Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DEF-58-01** | High | Evaluator Bug | `independent_evaluator.py` | Column name mismatch (`title`/`citation` vs `act_or_case_title`/`provision_or_para_ref`) caused silent lookup failures and false accusations of fabricated citations. | **RESOLVED** |
| **DEF-58-02** | High | Governance | `release_gates.py` | Release gates RG-03, RG-05, RG-06, and RG-09 were static declarations failing open with zero dynamic failure mechanisms under negative controls. | **RESOLVED** |
| **DEF-58-03** | Medium | Evaluation Engine | `differential_evaluator.py` | Newly added benchmark cases (e.g. 28 cases between PIT-V12 and PIT-V13) were silently omitted from comparison reports without separate tracking. | **RESOLVED** |
| **DEF-58-04** | Medium | Benchmark Integrity | `temporal_benchmark_manifest.json` | 5 query pairs across development and held-out splits shared identical legal dispute scenarios and statutory transitions. | **RESOLVED** (Documented & isolated) |

---

## Detailed Defect Records

### DEF-58-01: SQLite Column Mismatch in Citation Verification
- **Impact:** Evaluator threw `sqlite3.OperationalError: no such column: title`, which was swallowed by an unconstrained `try/except Exception: pass`. Authentic legal citations (e.g. *Rangappa v. Sri Mohan*, *Constitution of India Article 226*) were falsely flagged as fabricated, dropping trustworthiness from 0.97 to 0.59.
- **Root Cause:** Query string targeted legacy column names not present in `legal_chunks`.
- **Fix:** Corrected SQL statement to query `act_or_case_title` and `provision_or_para_ref`. Expanded regex valid patterns to include Constitution, Articles, Sanhitas, Adhiniyams, Rules, and Paragraph references. Trustworthiness restored to **0.9711**.

### DEF-58-02: Self-Reporting / Fail-Open Release Gates
- **Impact:** Gates RG-03, RG-05, RG-06, and RG-09 returned `GateStatus.PASSED` statically. If precedent hierarchy collapsed or fabricated citations were accepted, the gates would still pass.
- **Root Cause:** Placeholder implementation in Phase 57.
- **Fix:** Converted all 4 gates to live dynamic verifications using `build_national_judicial_knowledge_graph`, pipeline execution on negative fixtures, and cryptographic SHA-256 freeze checks.
