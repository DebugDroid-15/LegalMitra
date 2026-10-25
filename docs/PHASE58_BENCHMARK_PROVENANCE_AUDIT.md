# Phase 58 Benchmark Provenance & Split Audit

**Benchmark Name:** Point-in-Time V13 Legal Evaluation Benchmark (PIT-V13)  
**Total Cases:** 240  
**Manifest Path:** `data/22_central_legislation/temporal_benchmark_manifest.json`  

---

## 1. Split Allocation & Provenance Distribution

| Split Name | Case Count | Ratio | Target Legal Domains | Provenance Source |
| :--- | :--- | :--- | :--- | :--- |
| **Development Calibration (`development`)** | 100 | 41.7% | Criminal, Constitutional, Commercial, Property | Authentic central acts, gazette notifications, SCC precedents |
| **Validation Tuning (`validation`)** | 46 | 19.2% | Arbitration, Labour, Data Protection, IBC | High Court split precedents, statutory amendment transitions |
| **Held-Out Independent Evaluation (`held_out_evaluation`)** | 94 | 39.2% | Complex multi-issue, provisos, uncommenced statutes | Held-out real-world legal queries with verified ground truth |
| **Total** | **240** | **100.0%** | Comprehensive Indian Law | Evidence-grade primary sources |

---

## 2. Benchmark Case Invariants

1. **Zero Exact Duplicates:** Audited across all 240 cases; exactly 0 pairwise duplicate query texts detected.
2. **Deterministic Grounding:** All 240 cases contain explicit `governing_provisions`, `query_date` (or temporal facts), and `target_legal_doctrines`.
3. **No Model Contamination:** No benchmark case queries or answers have been used for model pretraining or parameter fine-tuning.
