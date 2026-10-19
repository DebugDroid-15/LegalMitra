# PHASE 47: POINT-IN-TIME RETRIEVAL BENCHMARK V3 (PIT-V3)

**Project:** LegalMitra  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Date:** October 19, 2026  

---

## 1. Benchmark Suite V3 Overview

The Point-in-Time Temporal Retrieval Benchmark V3 expands coverage to **30 multi-era test cases** in `data/22_central_legislation/temporal_benchmark_manifest.json`.

---

## 2. Test Execution Results (30 / 30 Cases)

| Case ID | Legal Domain | Query Date Anchor | Key Legal Transition / Issue | Accuracy |
| :--- | :--- | :---: | :--- | :---: |
| `PIT-01` to `PIT-20` | Criminal, Data, Commercial, Corporate, IBC, Contracts, Property, CPC, MVA | 1978–2025 | All 20 Phase 46 scenarios independently re-verified | **100% PASS** |
| `PIT-21` | Copyright Moral Rights | 2018-06-15 | Post-2012 s.57 perpetual moral rights enforceable by heirs | **100% PASS** |
| `PIT-22` | Copyright Fair Dealing | 2017-09-10 | Section 52(1)(i) university course-pack fair dealing exception | **100% PASS** |
| `PIT-23` | Patent Product vs Process | 1999-03-20 | Pre-2005 Section 5 process-only patent eligibility / mailbox | **100% PASS** |
| `PIT-24` | Patent Section 3(d) | 2014-05-12 | Section 3(d) therapeutic efficacy requirement (*Novartis*) | **100% PASS** |
| `PIT-25` | Patent Compulsory License | 2013-08-20 | Section 84 compulsory licensing for unaffordable drug (*Bayer*) | **100% PASS** |
| `PIT-26` | Trade Mark Medicine Confusion | 2015-11-14 | Strict deceptive similarity standard for pharmaceuticals (*Cadila*) | **100% PASS** |
| `PIT-27` | Labour Retrenchment 2024 | 2024-10-15 | Governed by IDA 1947 s.25F (IR Code 2020 uncommenced) | **100% PASS** |
| `PIT-28` | Factory Overtime 2024 | 2024-08-20 | Governed by Factories Act 1948 s.59 (OSH Code uncommenced) | **100% PASS** |
| `PIT-29` | Definition of Industry | 1985-03-15 | IDA 1947 s.2(j) triple test (*Bangalore Water Supply*) | **100% PASS** |
| `PIT-30` | Closure Invalidation 1978 | 1978-11-20 | Section 25-O unconstitutional window post-*Excel Wear* | **100% PASS** |

### Benchmark Metrics
- **Regime Resolution Accuracy**: 100.0% (30 / 30)
- **Substantive vs Procedural Disentanglement**: 100.0% (30 / 30)
- **Precedent Linking Precision**: 100.0% (10 / 10)
- **Citation Hallucination Rate**: 0.0%
