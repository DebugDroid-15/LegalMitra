# LegalMitra — Phase 39: Precedent Graph Validation & Invariant Testing

**Document Version:** 1.0.0  
**Phase:** 39 — National Judicial Corpus Expansion & Precedent Verification  
**Status:** Completed & Validated  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  

---

## 1. Executive Summary

This document reports the verification and validation of the Precedent Graph Engine (Version 2) implemented in Phase 39 Workstream H. The graph models the binding nature of judicial precedents under Article 141 of the Constitution of India, coram bench numerical hierarchy, overruling lineages, and passage-level evidentiary anchors.

Machine-readable graph: `data/21_judicial_infrastructure/precedent_relationship_graph_v2.json`.

---

## 2. Article 141 Bench Strength Invariant Verification

Under Article 141 and settled constitutional law (*Union of India v. Raghubir Singh* (1989) 2 SCC 754; *Central Board of Dawoodi Bohra Community v. State of Maharashtra* (2005) 2 SCC 673):
- A judgment delivered by a bench of larger numerical strength is binding on benches of smaller or equal strength.
- A smaller bench cannot overrule a larger bench.

### Programmatic Invariant Verification
The [`PrecedentGraphEngine`](file:///c:/PROJECTS/LegalMitra/legalmitra/judicial/precedent_graph_engine.py) was tested against attempts by a 2-judge bench to overrule a 7-judge bench:
```python
# Jurisprudential Invariant Test (from test_phase38_judicial_infrastructure.py)
invalid_edge = PrecedentEdge(
    citing_case_id="BENCH2",
    cited_case_id="MANEKA",
    treatment=TreatmentType.OVERRULED,
    passage_anchor="Para 10",
    treatment_context="Improper attempt by smaller bench to overrule larger bench.",
)
with pytest.raises(ValueError, match="Jurisprudential Invariant Violation"):
    graph.add_edge(invalid_edge)
```
**Result:** **PASS**. The engine immediately raises an invariant violation error, mathematically safeguarding the integrity of Indian constitutional hierarchy.

---

## 3. Verified Overruling Chains

The graph traces key historical overruling trajectories:
1. **Fundamental Rights & Due Process**:
   *A.K. Gopalan* (6J, 1950) -> Distinguished in *R.C. Cooper* (11J, 1970) -> Expressly **OVERRULED** in *Maneka Gandhi* (7J, 1978).
2. **Constituent Amending Power**:
   *Sankari Prasad* (5J, 1951) & *Sajjan Singh* (5J, 1965) -> **OVERRULED** in *Golaknath* (11J, 1967) -> **OVERRULED** in *Kesavananda Bharati* (13J, 1973, establishing Basic Structure).
3. **Personal Liberty & Emergency**:
   *ADM Jabalpur* (5J, 1976) -> Expressly **OVERRULED** in *Puttaswamy* (9J, 2017), upholding Justice H.R. Khanna's dissent.
4. **Decriminalization of Section 377 IPC**:
   *Suresh Kumar Koushal* (2J, 2014) -> Expressly **OVERRULED** in *Navtej Singh Johar* (5J, 2018).
5. **Decriminalization of Adultery (Section 497 IPC)**:
   *Sowmithri Vishnu* (3J, 1985) -> Expressly **OVERRULED** in *Joseph Shine* (5J, 2018).

---

## 4. Good Law Determination

The [`is_good_law()`](file:///c:/PROJECTS/LegalMitra/legalmitra/judicial/precedent_graph_engine.py) method was validated across all nodes. It accurately reports that *ADM Jabalpur*, *Suresh Koushal*, and *Sowmithri Vishnu* are **not good law**, while *Kesavananda Bharati*, *Maneka Gandhi*, and *Puttaswamy* remain authoritative **good law**.
