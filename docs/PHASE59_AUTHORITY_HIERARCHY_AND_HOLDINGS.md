# LegalMitra Phase 59 — Authority Hierarchy and Holdings

**Release Version:** `0.59.0`  
**Phase Identifier:** `LEGALMITRA-PHASE59`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Timestamp:** `2026-10-25T17:35:00Z`

---

## 1. Constitutional & Precedent Hierarchy

Under Article 141 of the Constitution of India, the law declared by the Supreme Court is binding on all courts within the territory of India.

LegalMitra implements strict precedence logic:
1. **Constitutional Bench Strength:**
   - 7-Judge Bench (*In Re Interplay*, 2024) binds and overrules 5-Judge Bench (*NN Global*, 2023).
   - 3-Judge Bench (*Vineeta Sharma*, 2020) binds and overrules 2-Judge Bench (*Prakash v. Phulavati*, 2016).
2. **Territorial Limits of High Court Authority:**
   - A decision of the High Court of Delhi binds the subordinate judiciary of the National Capital Territory of Delhi under Article 227.
   - It possesses high persuasive value, but is **not binding precedent**, upon the High Court of Bombay or subordinate courts of Maharashtra.
3. **Sub Judice Referrals:**
   - When a bench of coordinate jurisdiction doubts an earlier ruling and refers the question to a larger bench, the existing ruling remains operational until formally modified or overruled, but is flagged as `REFERRED_SUB_JUDICE`.

---

## 2. Precedent Conflict Resolution Matrix

| Authority A | Authority B | Issue | Resolution Status | Prevailing Binding Authority |
|:---|:---|:---|:---|:---|
| *In Re Interplay* (7-Judge) | *NN Global* (5-Judge) | Stamp duty & arbitration clause | `RESOLVED_BY_OVERRULING` | *In Re Interplay* |
| *Vineeta Sharma* (3-Judge) | *Prakash v. Phulavati* (2-Judge) | HSA Section 6 living father | `RESOLVED_BY_OVERRULING` | *Vineeta Sharma* |
| *Dawoodi Bohra* (5-Judge) | Coordinate Bench | Precedent doctrine | `RESOLVED_BY_BENCH_STRENGTH` | *Dawoodi Bohra* |
| Delhi HC Decision | Bombay HC Jurisdiction | Central statutory interpretation | `PERSUASIVE_NOT_BINDING` | Coordinate Persuasive |
