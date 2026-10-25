# LegalMitra Phase 59 — PIT-V14 Benchmark Design

**Release Version:** `0.59.0`  
**Phase Identifier:** `LEGALMITRA-PHASE59`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Suite Identifier:** `LEGALMITRA-BENCHMARK-PIT-V14`  
**Version:** `14.0.0`  
**Timestamp:** `2026-10-25T17:35:00Z`

---

## 1. Benchmark Expansion Strategy

The Point-in-Time (PIT) benchmark has been systematically expanded from 240 cases (PIT-V13) to **280 evidence-grade cases** (PIT-V14), adding 40 targeted diagnostic test cases.

### Split Composition:
- **Development Split:** 115 cases (PIT-01 to PIT-100, PIT-241 to PIT-255)
- **Validation Split:** 55 cases (PIT-101 to PIT-146, PIT-256 to PIT-264)
- **Held-Out Evaluation Split:** 110 cases (PIT-147 to PIT-240, PIT-265 to PIT-280)
- **Total Cases:** 280

---

## 2. Diagnostic Target Dimensions

The 40 newly added test cases directly evaluate:
1. **Citation existence vs substantive support** (PIT-241, PIT-255)
2. **Statutory bars and provisos** (PIT-242 SRA 20A, PIT-256 SARFAESI 34, PIT-259 HSA Proviso, PIT-264 RERA 79)
3. **Procedural condition precedents** (PIT-243 Commercial Courts 12A, PIT-244 NI Act 138)
4. **Clean slate and guarantor liability** (PIT-245 IBC Section 31)
5. **Exact midnight boundary transitions** (PIT-246, PIT-247, PIT-248, PIT-249)
6. **Enacted but uncommenced enactments** (PIT-250 Code on Wages, PIT-251 Industrial Relations Code)
7. **Proposition-level overruling** (PIT-252 SC/ST Act preliminary enquiry, PIT-253 surviving bail principles)
8. **Fabricated citation immunity & jailbreak defenses** (PIT-254, PIT-280)
9. **Bench strength hierarchy & territorial authority** (PIT-260, PIT-261, PIT-266)
10. **Quarantined scaffold immunity** (PIT-262)

---

## 3. Contamination & Isolation Safeguards

All 280 cases were audited via `ContaminationAuditor.audit_manifest`:
- Exact duplicate queries across splits: **0**
- Near duplicate queries across splits: **0**
- Maximum cross-split token Jaccard similarity: **0.6316** (Threshold $\le 0.85$)
- Cross-split isolation verdict: **PASS**
