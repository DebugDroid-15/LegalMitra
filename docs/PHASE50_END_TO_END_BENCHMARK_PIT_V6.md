# LEGALMITRA — PHASE 50
## End-to-End Legal Query Benchmark (LEGALMITRA-BENCHMARK-PIT-V6)

**Document ID:** `LM-DOC-PHASE50-BENCHMARK-V6-01`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Phase:** 50  
**Author:** Shatrujeet Legal Engineering Team  
**Status:** EXPANDED & 100% PASSING  
**Date:** 2026-10-19  

---

### 1. Benchmark Suite Expansion

The benchmark manifest (`data/22_central_legislation/temporal_benchmark_manifest.json`) was expanded from 60 to **80 source-grounded test cases** under suite ID `LEGALMITRA-BENCHMARK-PIT-V6`.

### 2. Breakdown of Phase 50 Benchmark Scenarios (PIT-61 to PIT-80)

- **PIT-61 (Overtime Computation):** Factories Act 1948 s.59 overtime at 2x rate -> `ANSWER_SUPPORTED`.
- **PIT-62 (Copyright 2012 Boundary):** Coursepack reproduction under pre-2012 s.52 -> `ANSWER_QUALIFIED`.
- **PIT-63 (Uncommenced Labour Code):** National Floor Minimum Wage under Code on Wages -> `ABSTAIN_TEMPORAL_UNCERTAINTY`.
- **PIT-64 (BNSS Savings Clause):** Pre-July 2024 pending bail application governed by CrPC under BNSS s.531 -> `ANSWER_SUPPORTED`.
- **PIT-65 (Patent Working Statement):** Commercial working Form 27 under Patents Rules 2003 -> `ANSWER_SUPPORTED`.
- **PIT-66 (Minerva Mills Constitution Bench):** Unconstitutional amendment to Art. 368(4)-(5) -> `ANSWER_SUPPORTED`.
- **PIT-67 (Overruled Emergency Precedent):** Majority view in ADM Jabalpur overruled by Puttaswamy -> `ANSWER_SUPPORTED`.
- **PIT-68 (Larger Bench Referral):** Magistrate further investigation under s.173(8) referred -> `ANSWER_QUALIFIED`.
- **PIT-69 (Interim Stayed Precedent):** St. Stephen's minority admission stay -> `ANSWER_QUALIFIED`.
- **PIT-70 (High Court Co-Equal Conflict):** Section 29A mandate extension coordinate split -> `ANSWER_QUALIFIED`.
- **PIT-71 (Cross-Statute Definition Divergence):** Supervisor as "workman" (IDA) vs "employee" (Code on Wages) -> `ANSWER_SUPPORTED`.
- **PIT-72 (Missing Rent Jurisdiction):** Eviction under Rent Control requiring State jurisdiction -> `CLARIFICATION_REQUIRED`.
- **PIT-73 (Missing Offence Date):** Cheating offence transitioning IPC s.420 to BNS s.318 -> `CLARIFICATION_REQUIRED`.
- **PIT-74 (Rent Control Cap Conflict):** Lease rent INR 15,000 exceeds Delhi Rent Control s.3(c) limit -> `ANSWER_SUPPORTED`.
- **PIT-75 (Sibbia Bail Inversion):** Police claim of exceptional murder restriction refuted -> `ANSWER_SUPPORTED`.
- **PIT-76 (Fabricated Citation):** *Rameshwar v. UOI 2024 INSC 99999* detected and rejected -> `ABSTAIN_SOURCE_INTEGRITY_FAILURE`.
- **PIT-77 (Kesavananda Amending Power):** Part III amendment power subject to Basic Structure -> `ANSWER_SUPPORTED`.
- **PIT-78 (Unverified Circular Provenance):** 50% gratuity deduction circular rejected under Gratuity Act s.4(6) -> `ANSWER_SUPPORTED`.
- **PIT-79 (Adversarial Prompt Injection):** Prompt instruction to disregard Contract Act mitigated -> `ANSWER_QUALIFIED`.
- **PIT-80 (Multi-Issue Retrenchment):** 4 continuous years factory service compensation under IDA s.25F -> `ANSWER_SUPPORTED`.

**Result:** 80/80 benchmark scenarios execute and pass deterministically.
