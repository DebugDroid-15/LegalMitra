# RUNBOOK 56: EVIDENCE ELIGIBILITY & RETRIEVAL SAFEGUARDS

**Project:** LegalMitra  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Date:** October 2026  

---

## 1. Safeguard Verification Procedure

1. **Verify Scaffold Quarantine**:
   - Query `data/legalmitra_kb.db` to verify that `is_synthetic_scaffold = 1` for `IND-JUD-DEL-2024-BAIL`.
   - Run `EvidenceEligibilityEngine().evaluate_chunk_eligibility("IND-JUD-DEL-2024-BAIL")` to verify rejection.
2. **Verify Format Fixture Rejection**:
   - Run `EvidenceEligibilityEngine().evaluate_chunk_eligibility("IND-UNSUPPORTED-001")` to verify `UNSUPPORTED_FIXTURE` verdict.
3. **Verify Temporal Guards**:
   - Verify that post-dated queries or unnotified provisions return `temporal_warning` in the eligibility verdict.
