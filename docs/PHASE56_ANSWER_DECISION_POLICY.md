# PHASE 56: ANSWER DECISION POLICY AND CALIBRATION REPORT

**Project:** LegalMitra  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Phase:** 56  
**Module:** `legalmitra.orchestration.decision_policy`  

---

## 1. Executive Summary

Phase 56 expands `LegalResponseState` to nine calibrated, auditable states, adding `ANSWER_PARTIAL` and `ANSWER_CONDITIONAL` to eliminate forced binary all-or-nothing responses.

---

## 2. Response State Taxonomy

1. `ANSWER_SUPPORTED`: Direct answer grounded in primary legislation and binding precedents.
2. `ANSWER_QUALIFIED`: Substantive answer subject to explicit statutory exceptions, provisos, stays, or larger bench referrals.
3. `ANSWER_CONDITIONAL` (*New in Phase 56*): Answer structured conditionally across verified alternative factual branches.
4. `ANSWER_PARTIAL` (*New in Phase 56*): Multi-issue response where substantively grounded issues are resolved and uncommenced or uncertain regimes are explicitly disclosed.
5. `CLARIFICATION_REQUIRED`: Missing material fact that would fundamentally alter governing law.
6. `ABSTAIN_INSUFFICIENT_EVIDENCE`: Zero matching verified source chunks in knowledge base.
7. `ABSTAIN_AUTHORITY_CONFLICT`: Unresolved coordinate High Court conflict with missing territorial jurisdiction.
8. `ABSTAIN_TEMPORAL_UNCERTAINTY`: Uncommenced enactment with pending commencement notification.
9. `ABSTAIN_SOURCE_INTEGRITY_FAILURE`: Fabricated neutral citation or quarantined synthetic scaffold detected.

---

## 3. Decision Evaluation Flow

```text
[Parsed Query + Evidence Set + Assembled Answer]
                     |
         [Fatal Blocker Check]
    - Fabricated citation? -> ABSTAIN_SOURCE_INTEGRITY_FAILURE
    - Zero evidence? -> ABSTAIN_INSUFFICIENT_EVIDENCE
                     |
        [Matrix Issue Evaluation]
    - Multi-issue partial support? -> ANSWER_PARTIAL
    - Factual contingency branches? -> ANSWER_CONDITIONAL
                     |
       [Single-Issue Blocker Check]
    - All uncommenced? -> ABSTAIN_TEMPORAL_UNCERTAINTY
    - High Court conflict without forum? -> ABSTAIN_AUTHORITY_CONFLICT
    - Missing decisive fact? -> CLARIFICATION_REQUIRED
                     |
       [Grounding & Qualification]
    - Qualifications / Provisos? -> ANSWER_QUALIFIED
    - All claims verified? -> ANSWER_SUPPORTED
```
