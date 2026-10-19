# LEGALMITRA — PHASE 49
## Precedent Conflict Resolution & Enhanced Relationship Semantics

**Document ID:** `LM-DOC-PHASE49-CONFLICT-RESOLUTION-01`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Phase:** 49  
**Author:** Shatrujeet Legal Engineering Team  
**Status:** IMPLEMENTED & TESTED  
**Date:** 2026-10-19  

---

### 1. Expanded Precedent Relation Types

Phase 49 extends `RelationType` in `legalmitra/caselaw/knowledge_graph.py` with explicit legal semantics:
- `STAYED`: Identifies that the operation of a judgment has been stayed by an appellate court (e.g. Supreme Court interim stay in *St. Stephen's College v. University of Delhi*).
- `VACATED`: Identifies an order or injunction set aside by subsequent proceedings.
- `LIMITS`: Models explicit constitutional or doctrinal boundaries (e.g. *Kesavananda Bharati* limits amending power under Article 368).
- `CONFLICTS_WITH`: Formally tags divergent interpretations across co-equal High Courts or intra-court benches without declaring an automated winner.
- `SUPERSEDES_STATUTORY_BASIS`: Identifies instances where Parliament enacts an amendment nullifying the statutory foundation of a judicial ruling.

---

### 2. Deterministic Conflict Resolution Rules

The engine implements strict separation between:
1. **Express Overruling**: Delivered by a larger or co-equal competent bench explicitly reversing legal doctrine (e.g. 7-judge bench in *In Re: Interplay (2024)* overruling 5-judge bench in *NN Global (2023)*).
2. **Distinguishing**: A court identifies factual or statutory differences without disturbing the earlier ratio (e.g. *Arnesh Kumar (2014)* distinguishing mechanical arrest from justified arrest).
3. **Referral to Larger Bench**: A bench doubts an earlier precedent and refers the question to the Chief Justice. **Rule:** A referral does NOT overrule or stay the binding nature of the precedent under Article 141 until the larger bench delivers judgment.
4. **Interim Stay**: Freezes execution between parties but does NOT lay down a binding declaration of law under Article 141.
5. **Legislative Supersession**: Legislative amendments alter statutory text, rendering earlier case law inapplicable to post-amendment disputes.
