# LEGALMITRA — PHASE 49
## Amendment-Aware Precedent Tracking Architecture

**Document ID:** `LM-DOC-PHASE49-AMENDMENT-AWARE-01`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Phase:** 49  
**Author:** Shatrujeet Legal Engineering Team  
**Status:** IMPLEMENTED & TESTED  
**Date:** 2026-10-19  

---

### 1. The Statutory Evolution Challenge

Judicial decisions interpret statutory text operative on the date of the underlying cause of action. When Parliament amends that statute, the judgment does not cease to exist, but its applicability to post-amendment transactions changes fundamentally.

Phase 49 introduces:
```python
temporal_engine.resolve_amendment_impact_on_precedent(
    case_id: str,
    statute_id: str,
    section: str,
    query_date_str: str,
) -> Dict[str, Any]
```

---

### 2. Verified Legislative Supersession Scenarios

1. **Indian Contract Act Section 28 (*Vulcan Insurance (1976)*)**:
   - Pre-1997 (before 08.01.1997): *Vulcan Insurance* applies; clauses extinguishing contractual rights within specified periods are valid.
   - Post-1997 (after Act 1 of 1997): Section 28(b) renders extinguishment clauses void. *Vulcan Insurance* statutory basis is superseded.
2. **Transfer of Property Act Section 53A (*Part Performance*)**:
   - Pre-2001 (before 24.09.2001): Unregistered agreement shields possession.
   - Post-2001 (Act 48 of 2001): Section 53A TPA read with Section 17(1A) Registration Act requires mandatory registration. Pre-2001 rulings inapplicable.
3. **Income Tax Act Section 9(1)(i) (*Vodafone International Holdings (2012)*)**:
   - Pre-Finance Act 2012: Offshore transfer of holding company shares not taxable in India.
   - Post-Finance Act 2012: Explanations 4 & 5 inserted with retrospective effect from 01.04.1962, nullifying *Vodafone* holding.
4. **Industrial Disputes Act Section 25-O (*Closure Invalidation*)**:
   - Pre-1978: Section 25-O prior permission required.
   - 1978–1984: Section 25-O struck down in *Excel Wear (1978)*; prosecution invalid.
   - Post-1984: Re-enacted by Act 49 of 1984 with procedural safeguards.
