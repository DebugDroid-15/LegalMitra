# LEGALMITRA — PHASE 48
## Cross-Statute Definition Taxonomy & Comparative Semantics

**Document ID:** `LM-DOC-PHASE48-CROSS-STATUTE-TAXONOMY-01`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Phase:** 48  
**Author:** Shatrujeet Legal Engineering Team  
**Status:** IMPLEMENTED AND EVIDENCE-VERIFIED  
**Date:** 2026-10-19  

---

### 1. Problem Statement

A frequent failure mode of legal AI systems is **illicit semantic conflation**—assuming that identical or similar legal terms carry the same meaning across different Indian enactments. In Indian jurisprudence, statutory definitions are strictly confined to their parent Act ("In this Act, unless the context otherwise requires..."). Conflating terms across statutory boundaries yields catastrophic legal misdirections.

---

### 2. Taxonomy Coverage

Phase 48 establishes `data/22_central_legislation/cross_statute_definitions.json` covering 8 critical terms across 18 statutory definitions:

1. **`workman_vs_worker_vs_employee`**:
   - `workman` under IDA 1947 s.2(s): Excludes managerial/administrative personnel and supervisors earning > ₹10,000/mo. IN FORCE.
   - `worker` under Factories Act 1948 s.2(l): Pertains to manufacturing process. IN FORCE.
   - `worker` under uncommenced IR Code 2020 s.2(zr): Supervisor threshold ₹18,000/mo. UNCOMMENCED.
   - `employee` under uncommenced Code on Wages 2019 s.2(k): Includes managerial staff. UNCOMMENCED.
2. **`industry`**:
   - IDA 1947 s.2(j): Governing triple test per *Bangalore Water Supply (1978)*. The 1982 legislative amendment remains UNNOTIFIED.
3. **`goods`**:
   - Sale of Goods Act 1930 s.2(7): Stocks and shares ARE goods; actionable claims are NOT goods.
   - CPA 2019 s.2(21): Incorporates SOGA s.2(7) and adds food under FSSA 2006.
   - CGST Act 2017 s.2(52): Movable property OTHER than money and securities (shares); actionable claims ARE goods.
   - **Critical Divergence**: In SOGA, shares are goods; in CGST, shares are NOT goods.
4. **`consumer`**:
   - CPA 1986 s.2(1)(d): Historical definition (repealed with savings).
   - CPA 2019 s.2(7): Expressly includes e-commerce, teleshopping, and direct selling.
5. **`invention`**:
   - Patents Act 1970 s.2(1)(j): Qualified by negative statutory filters under Section 3 (esp. 3(d) efficacy and 3(k) software/algorithms).
6. **`electronic_record`**:
   - IT Act 2000 s.2(1)(t): Foundational definition.
   - BSA 2023 s.2(1)(d): Incorporated by reference.
7. **`appropriate_government`**:
   - IDA 1947 s.2(a): Dual jurisdiction between Central and State Governments; governed by *SAIL (2001)* Constitution Bench.
8. **`company`**:
   - Companies Act 2013 s.2(20): Continuous statutory meaning across 1956 and 2013 Acts.

---

### 3. Query Engine

The engine provides:
```python
temporal_engine.compare_cross_statute_definitions(term: str, statute_ids: Optional[List[str]] = None) -> Dict[str, Any]
temporal_engine.resolve_term_definition(term: str, statute_id: str, query_date_str: Optional[str] = None) -> Dict[str, Any]
```
These methods return the verbatim statutory definitions, statutory inclusions/exclusions, operational status (`CURRENTLY_IN_FORCE` vs `ENACTED_UNCOMMENCED`), and explicit comparative semantic warnings.
