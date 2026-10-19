# PHASE 52: FAILURE TAXONOMY & REMEDIATION MATRIX

**Project:** LegalMitra  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Date:** October 2026  

---

## 1. Evidence Reliability Failure Taxonomy

1. **Category E1: Unverified Synthetic Scaffold Ingestion**
   - *Risk*: Using mock cases as binding precedent.
   - *Defense*: Mandatory `is_synthetic_scaffold = 1` flag + eligibility engine rejection.
2. **Category E2: Premature Enforcement of Unnotified Enactments**
   - *Risk*: Citing enacted but unnotified codes (e.g. Labour Codes, DPDP s.44).
   - *Defense*: Gazette commencement verification + temporal warning generation.
3. **Category E3: Copyright & Model Training Infringement**
   - *Risk*: Using statutory corpus to train public/proprietary foundation model weights.
   - *Defense*: Non-negotiable architectural invariant: zero pretraining, zero fine-tuning.
4. **Category E4: Domain Coverage Silence / Hallucination**
   - *Risk*: Hallucinating answers in low-coverage domains (e.g. personal law, IBC).
   - *Defense*: Fail-closed calibrated abstention (`ABSTAIN_UNSUPPORTED`).
