# PHASE 53: EVIDENCE FAILURE TAXONOMY & DETERMINISTIC OUTCOMES

**Project:** LegalMitra  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Phase:** 53  

---

## 1. Exhaustive Outcome Taxonomy

LegalMitra enforces a standardized 8-outcome taxonomy for evidence validation:

1. **`SUPPORTED`**: Material claim fully supported by cited authority, text passage, and valid temporal window.
2. **`PARTIALLY_SUPPORTED`**: Authority identified, but passage-level match requires qualified review.
3. **`UNSUPPORTED`**: Cited authority is nonexistent, unverified, or fabricated (triggers fail-closed abstention).
4. **`CONTRADICTED`**: Proposition directly conflicts with verbatim statutory or judicial passage.
5. **`TEMPORALLY_UNCERTAIN`**: Authority or statutory basis was repealed or superseded at the query temporal anchor.
6. **`JURISDICTION_UNCERTAIN`**: Cited instrument lies outside verified Indian national and state registries.
7. **`PRECEDENT_STATUS_UNCERTAIN`**: Judicial decision was overruled, stayed, or referred to a larger bench (e.g. *ADM Jabalpur*).
8. **`INSUFFICIENT_EVIDENCE`**: Claim lacks any cited source identifier, statute, or passage anchor.
