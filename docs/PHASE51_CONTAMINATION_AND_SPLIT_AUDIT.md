# PHASE 51: CONTAMINATION & DATASET SPLIT INDEPENDENCE AUDIT

**Project:** LegalMitra  
**Auditor Module:** `legalmitra.evaluation.contamination.ContaminationAuditor`  
**Dataset Audited:** `LEGALMITRA-BENCHMARK-PIT-V7` (100 Cases)  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Date:** October 2026  

---

## 1. Contamination Audit Methodology

Data contamination and train-test leakage are the primary failure modes of synthetic benchmarks in applied AI. When models or heuristic pipelines are tuned on benchmark questions, reported metrics reflect rote memorization rather than legal reasoning capability.

The `ContaminationAuditor` performs three deterministic audits across all 100 benchmark queries:
1. **Normalized Exact Duplicate Detection**: Case-insensitive, whitespace-normalized string equivalence check.
2. **Token Jaccard Cross-Split Similarity**: Computes token-level Jaccard similarity between all pairwise combinations of queries across different splits (`development`, `validation`, and `held_out_evaluation`) after removing legal stopwords.
3. **High-Similarity Pair Flagging**: Flags any cross-split query pair with token Jaccard similarity exceeding the threshold of $0.85$.

---

## 2. Empirical Audit Results

| Audit Check | Permitted Threshold | Audited Actual | Status |
|:---|:---:|:---:|:---:|
| Total Benchmark Cases Audited | 100 cases | 100 cases | **PASS** |
| Development Split Size | Exactly 50 cases | 50 cases | **PASS** |
| Validation Split Size | Exactly 20 cases | 20 cases | **PASS** |
| Held-Out Evaluation Split Size | Exactly 30 cases | 30 cases | **PASS** |
| Exact Duplicate Queries Across Splits | 0 duplicates | **0 duplicates** | **PASS** |
| Near-Duplicate Queries (Jaccard > 0.85) | 0 near-duplicates | **0 near-duplicates** | **PASS** |
| Maximum Cross-Split Jaccard Similarity | <= 0.8500 | **0.2941** | **PASS** |
| Split Isolation Verdict | True Isolation | **ISOLATED (PASS)** | **PASS** |

---

## 3. Analysis of Maximum Similarity Pair

The maximum cross-split Jaccard similarity detected was **0.2941** between:
- **Case PIT-18 (Development)**: *Cheating and dishonestly inducing delivery of property across criminal law transition...*
- **Case PIT-78 (Held-Out Evaluation)**: *What is the maximum imprisonment term and governing statutory section for cheating under Indian law?*

While both queries address the statutory crime of cheating across the IPC/BNS transition, their legal targets and fact patterns are completely distinct: PIT-18 provides concrete transaction dates to test point-in-time statutory selection, whereas PIT-78 intentionally withholds transaction dates to evaluate deterministic clarification policy. The Jaccard similarity of 0.2941 reflects shared statutory terminology without factual or proposition leakage.

---

## 4. Auditor Conclusion

The held-out evaluation partition (`PIT-71` to `PIT-100`) is 100% clean, independent, and free from cross-split contamination.
