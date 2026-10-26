# PHASE 61 SOURCE ELIGIBILITY AUDIT
**Release Candidate:** 0.61.0  
**Phase Identifier:** LEGALMITRA-PHASE61  
**Audit Purpose:** Verify Rights, Eligibility, and Absolute Training Exclusion  

---

## 1. Statutory Rights and Ingestion Eligibility

LegalMitra acquires and indexes official Indian legal authorities pursuant to established public interest principles and statutory exceptions:

1. **Section 52(1)(q) of the Copyright Act, 1957:**
   - Reproduction or publication of any matter published in any Official Gazette.
   - Reproduction of any Act of a Legislature.
   - Reproduction of any report of a committee appointed by Government or Legislature.
   - Reproduction of any judgment or order of a court, tribunal or other judicial authority.
2. **Open Access Judicial Registries:**
   - Ingestion is conducted exclusively from authorized official portals (India Code, eCourts, Supreme Court of India, High Courts).
   - Automated polling adheres strictly to rate limits (maximum 20 requests per minute) and terms of access.

---

## 2. Absolute Model Training Exclusion

> [!CAUTION]
> **STRICT INVARIANT: ZERO MODEL PRETRAINING OR FINE-TUNING.**  
> Under no circumstances may any document in the LegalMitra corpus, advocate review packages, or evaluation benchmark be used for pretraining, fine-tuning, adapter training (e.g. LoRA/QLoRA), or parameter updates of any neural model.

LegalMitra operates purely as an **evidence-retrieval, reasoning-orchestration, and rule-governed validation pipeline** using frozen weights and deterministic verification algorithms.

### Governance Verifications:
- `is_synthetic_scaffold = 1` chunks are strictly excluded from retrieval context during operational execution.
- No training scripts, parameter update harnesses, or gradient optimization dependencies exist in the repository.
- Model pretraining and fine-tuning are classified as strict NO-GO release blockers.
