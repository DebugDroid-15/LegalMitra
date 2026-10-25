# LegalMitra Phase 59 — Statutory Exception and Premise Dependency Audit

**Release Version:** `0.59.0`  
**Phase Identifier:** `LEGALMITRA-PHASE59`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Timestamp:** `2026-10-25T17:35:00Z`

---

## 1. Provisos & Statutory Bars

Indian statutory law is replete with provisos that reverse the legal consequence of the general rule. Emitting an absolute proposition without its qualifying proviso is a severe legal safety defect.

### Audited Statutory Provisos:
1. **Hindu Succession Act, 1956 — Section 6(1) Proviso:**
   - *General Rule:* Daughter is a coparcener by birth.
   - *Proviso Exception:* Any disposition, alienation, partition, or testamentary disposition executed or registered before 20 December 2004 cannot be invalidated or reopened.
2. **Specific Relief Act, 1963 — Section 20A:**
   - *General Rule:* Courts may grant injunctions in civil disputes.
   - *Statutory Bar:* Injunction shall not be granted in respect of infrastructure projects specified in the Schedule if it causes impediment or delay.
3. **Commercial Courts Act, 2015 — Section 12A:**
   - *General Rule:* Pre-institution mediation is mandatory.
   - *Exception:* Suits contemplating urgent interim relief are exempt from pre-institution mediation.
4. **Negotiable Instruments Act, 1881 — Section 138:**
   - *Condition Precedent:* Demand notice within 30 days of dishonour and 15 days cure window before cause of action arises.
5. **Insolvency and Bankruptcy Code, 2016 — Section 31:**
   - *Clean Slate:* Debts of corporate debtor extinguished; personal guarantor liability survives.

---

## 2. Premise Dependency Propagation

When a downstream legal assertion depends upon a prerequisite condition, the failure of the prerequisite must invalidate or condition the downstream conclusion.

- If a contract is determinable under Section 14(d) SRA, specific performance is barred; an assertion affirming specific performance is rejected as `PREMISE_DEPENDENCY_FAILED`.
- If an agreement to sell immovable property is unregistered post-2001, Section 53A TPA part performance defense is legally unavailable under Registration Act Section 17(1A).
