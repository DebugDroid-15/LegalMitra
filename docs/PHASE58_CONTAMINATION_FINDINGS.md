# Phase 58 Cross-Split Contamination & Leakage Audit

**Audit Engine:** `legalmitra.evaluation.contamination.ContaminationAuditor`  
**Benchmark Target:** PIT-V13 (240 cases)  
**Threshold Invariant:** Max cross-split token Jaccard <= 0.85; Zero exact duplicate cases.

---

## 1. Quantitative Leakage Metrics

| Metric | Measured Value | Threshold | Verdict |
| :--- | :--- | :--- | :--- |
| **Exact Cross-Split Duplicate Queries** | 0 | 0 | **PASS** |
| **Maximum Token-Level Jaccard Similarity** | 0.5926 | <= 0.85 | **PASS** |
| **Average Cross-Split Jaccard Similarity** | 0.1248 | <= 0.35 | **PASS** |
| **Shared Statutory Provisions Across Splits** | 39 provisions | Permissible (Shared law) | **PASS** |

---

## 2. Qualitative Legal Dispute Scenario Overlap Analysis

While token-level similarity is strictly within thresholds, semantic auditing identified 5 dispute scenario pairs where the underlying legal controversy recurs across splits:

1. **PIT-97 (Dev) vs PIT-195 (Held-Out):**
   - *Statute:* Section 53A Transfer of Property Act, 1882 (Registration Amendment Act 2001).
   - *Issue:* Unregistered agreement to sell executed after 2001 amendment claiming part performance.
   - *Assessment:* Natural legal recurrence. Queries feature distinct fact patterns (agricultural land vs commercial shop).
2. **PIT-108 (Dev) vs PIT-194 (Held-Out):**
   - *Statute:* Section 25F Industrial Disputes Act, 1947 vs Industrial Relations Code, 2020.
   - *Issue:* Retrenchment compensation and threshold applicability under uncommenced code.
3. **PIT-132 (Dev) vs PIT-214 (Held-Out):**
   - *Statute:* Section 12A Commercial Courts Act, 2015.
   - *Issue:* Mandatory pre-institution mediation and urgent interim relief exception under Patil Automation.
4. **PIT-76 (Dev) vs PIT-201 (Held-Out):**
   - *Statute:* Fabricated neutral citation injection (`2024 INSC 99999`).
5. **PIT-92 (Dev) vs PIT-188 (Held-Out):**
   - *Statute:* Hindu Succession Act, 1956 Section 6(1) proviso (pre-2004 registered partition).

**Recommendation:** The 5 pairs represent essential statutory doctrine testing across distinct fact patterns. They are maintained with split isolation documented in the benchmark manifest.
