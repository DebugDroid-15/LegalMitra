# PHASE 55: PRECEDENT HIERARCHY & CONFLICT CALIBRATION

**Project:** LegalMitra  
**Component:** `legalmitra.caselaw.knowledge_graph`  
**Phase:** 55  
**Date:** October 2026  
**Classification:** PROPRIETARY AND CONFIDENTIAL  

---

## 1. Doctrinal Foundations

Precedent conflict resolution in Indian law is governed by Article 141 of the Constitution and the coordinate bench doctrine established in landmark Constitution Bench decisions (*Dawoodi Bohra*, *Pranay Sethi*, *Subhash Chandra*).

Phase 55 calibrated `LegalKnowledgeGraph.resolve_precedent_conflict` across four essential distinctions:

### 1. Referral vs. Final Overruling
- An order referring an earlier decision to a larger bench (`REFERS_TO_LARGER_BENCH`) doubts the earlier reasoning, but does **not** overrule it.
- Until the larger bench renders its final judgment, the earlier ratio remains operative, albeit with status `REFERRED_SUB_JUDICE` and `requires_qualification=True`.

### 2. Distinguishing vs. Overruling
- An authority distinguishing a prior ruling on factual or statutory grounds (`DISTINGUISHES`) leaves the prior authority good law for its original proposition.
- Status is classified as `DISTINGUISHED_NOT_OVERRULED`.

### 3. Ratio Decidendi vs. Obiter Dicta
- Observations made *in passing* without forming the necessary basis of the decision constitute obiter dicta.
- While Supreme Court obiter has persuasive value, it cannot displace a binding ratio decidendi on that point (`PERSUASIVE_OBITER_NOT_BINDING_RATIO`).

### 4. Co-Equal Coordinate Benches
- Where two benches of identical strength (e.g. two 2-Judge Benches of the Supreme Court) deliver conflicting holdings without referencing each other, neither overrules the other.
- Status is preserved neutrally as `UNRESOLVED_CO_EQUAL_BENCH_SPLIT`.
