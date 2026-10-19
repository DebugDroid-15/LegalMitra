# PHASE 53: AUDITABLE SOURCE ACQUISITION WORKFLOW

**Project:** LegalMitra  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Phase:** 53  

---

## 1. Lifecycle State Machine Architecture

Phase 53 introduces `LegalAcquisitionEngine` (`legalmitra/corpus/acquisition_engine.py`) providing a formal, auditable 13-state deterministic lifecycle machine for Indian legal sources:

```
[IDENTIFIED] -> [EVALUATED] -> [RIGHTS_VERIFIED] -> [PROVENANCE_LOCATED] -> [STAGED]
      |
      v
 [FETCHED] -> [TEXT_EXTRACTED] -> [STRUCTURED] -> [VALIDATED] -> [REGISTERED]
      |
      v
  [INDEXED] -> [ACTIVE_PRODUCTION] (or [REJECTED] / [QUARANTINED])
```

### State Definitions & Enforced Prerequisites:
1. **`IDENTIFIED`**: Source cited in coverage gaps or statutory dependency trees.
2. **`EVALUATED`**: Legal relevance, domain urgency, and authority weight evaluated.
3. **`RIGHTS_VERIFIED`**: Verified under Section 52(1)(q) Copyright Act 1957; internal retrieval permitted; **training strictly prohibited**.
4. **`PROVENANCE_LOCATED`**: Official Gazette or authentic court registry URL confirmed.
5. **`STAGED`**: Raw candidate bundle registered in `data/01_raw/`.
6. **`FETCHED`**: Payload downloaded with SHA-256 integrity hash recorded.
7. **`TEXT_EXTRACTED`**: Gazette text or enactment body parsed into structured Unicode.
8. **`STRUCTURED`**: Sections, provisos, explanations, and marginal notes mapped into schema.
9. **`VALIDATED`**: Cross-referenced against gazette publication date and enactment number.
10. **`REGISTERED`**: Source registered in `sources` table with unique `document_id`.
11. **`INDEXED`**: Chunks ingested into `legal_chunks` table with deterministic hash.
12. **`ACTIVE_PRODUCTION`**: Source made retrievable by `EvidenceEligibilityEngine`.
13. **`QUARANTINED` / `REJECTED`**: Sources failing verification or held as scaffold.
