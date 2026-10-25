# PHASE 55: TEMPORAL INTERVAL SEMANTICS & STATUTORY LIFECYCLE AUDIT

**Project:** LegalMitra  
**Component:** `legalmitra.temporal.engine`  
**Phase:** 55  
**Date:** October 2026  
**Classification:** PROPRIETARY AND CONFIDENTIAL  

---

## 1. Executive Summary

Phase 55 conducted an exhaustive semantic audit of temporal interval representations, boundary transitions, and statutory commencement rules across the LegalMitra repository. The audit calibrated interval mathematics to guarantee that statutory enactments, gazette commencement notifications, retrospective holdings, and savings clauses are interpreted in strict fidelity with Indian administrative and constitutional law.

---

## 2. Temporal Interval Mathematics: `[effective_from, effective_until]`

In Phase 54, LegalMitra adopted inclusive calendar intervals `[effective_from, effective_until]` where both endpoints represent days on which the provision was operative.

### 2.1 Boundary Invariants Formalized:
1. **Inclusive End-of-Day Transition:**
   - Where a provision version has `version_effective_until = "2012-06-20"`, queries on `2012-06-20` resolve to Version 1 (`CONFIRMED_HISTORICAL` or `CONFIRMED_APPLICABLE`).
   - A query on `2012-06-21` (effective commencement of Version 2) cleanly transitions to Version 2 (`CONFIRMED_APPLICABLE`).
2. **Promulgation vs. In-Force Barrier:**
   - Publication of an Act in the Official Gazette or receipt of Presidential assent does **not** bring the provisions into force if the statute contains an appointed-day commencement clause under Section 1(2) or 1(3) appointing a future date.
   - For queries prior to the appointed date, the provision is definitively classified as `NOT_YET_IN_FORCE`.
3. **Overlapping Interval Conflict Detection:**
   - Where two incompatible versions of the same provision concurrently match a query date without an authoritative legislative or retrospective resolution, the engine avoids silent arbitrary selection and returns `CONFLICTING_TEMPORAL_EVIDENCE`.
4. **Conflicting Gazette Notification Protection:**
   - Where contradictory commencement notifications appear in official gazettes without gazette corrigendum, status resolves to `CONFLICTING_TEMPORAL_EVIDENCE`.
5. **Retrospective Statutory Bases:**
   - Retrospective statutory effects (e.g. *Vineeta Sharma v. Rakesh Sharma* (2020) 9 SCC 1 on Section 6 Hindu Succession Act 1956) are modeled explicitly with `is_retrospective=True` and documented `retrospective_basis`.
6. **Repeal with Savings:**
   - Under savings provisions (e.g., Section 531(2)(a) BNSS saving pending CrPC proceedings), a repealed provision remains accessible as `CONFIRMED_HISTORICAL` with `savings_applied=True`.
