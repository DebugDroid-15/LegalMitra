# LegalMitra — Phase 38: Precedent Graph Design & Evidentiary Model

**Document Version:** 1.0.0  
**Phase:** 38 — National Judicial Knowledge Infrastructure  
**Status:** Completed & Validated  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  

---

## 1. Executive Summary

This document specifies the typed precedent graph model designed and implemented in LegalMitra Phase 38. The graph models the binding nature of judicial precedents under Article 141 of the Constitution of India, coram bench strength, overruling lineages, and citation treatments anchored to specific passages.

Implemented in `legalmitra/judicial/precedent_graph_engine.py` and exported to `data/21_judicial_infrastructure/precedent_relationship_graph.json`.

---

## 2. Article 141 Bench Strength Hierarchy

Under Article 141 and established constitutional jurisprudence (*Union of India v. Raghubir Singh* (1989) 2 SCC 754; *Central Board of Dawoodi Bohra Community v. State of Maharashtra* (2005) 2 SCC 673):
- A judgment delivered by a bench of larger numerical strength is binding on benches of smaller or equal strength.
- A bench of smaller strength cannot overrule, doubt, or depart from a judgment delivered by a bench of larger strength.
- If a subsequent bench doubts the correctness of a larger bench decision, it may only refer the matter to the Chief Justice for constitution of an even larger bench.

### Bench Categories

| Category | Numerical Strength | Illustrative Benchmark Precedent |
| :--- | :--- | :--- |
| `SINGLE_BENCH` | 1 Judge | Interlocutory and routine single judge orders |
| `DIVISION_BENCH` | 2 Judges | Regular appellate and SLP division benches |
| `FULL_BENCH` | 3 Judges | *Sowmithri Vishnu* (1985), reference benches |
| `CONSTITUTION_BENCH` | 5 Judges | *Sankari Prasad* (1951), *Shah Bano* (1985), *Joseph Shine* (2018), *Navtej Johar* (2018) |
| `LARGER_BENCH` | 7 or 9 Judges | *Maneka Gandhi* (7 judges, 1978), *Puttaswamy* (9 judges, 2017), *Bommai* (9 judges, 1994) |
| `SPECIAL_LARGEST_BENCH` | 11 or 13 Judges | *Golaknath* (11 judges, 1967), *R.C. Cooper* (11 judges, 1970), *Kesavananda Bharati* (13 judges, 1973) |

---

## 3. Precedent Treatment Types

Every citation edge connecting a citing judgment to a cited judgment carries an explicit treatment type:
1. `FOLLOWED`: The legal principle was accepted, applied, and formed part of the ratio.
2. `DISTINGUISHED`: The cited case was held inapplicable due to material factual or statutory differences.
3. `OVERRULED`: The holding of the cited case was formally declared bad law and invalidated by a larger bench.
4. `DOUBTED`: The reasoning was questioned, but not formally overruled due to coram limitations.
5. `EXPLAINED`: The scope or ratio was interpreted and clarified.
6. `REFERRED_TO`: The precedent was noted without substantive doctrinal expansion or departure.
7. `AFFIRMED`: Decision of lower court confirmed on appeal.
8. `REVERSED_ON_APPEAL`: Decision of lower court set aside on appeal.

---

## 4. Software Invariant: Bench Strength Protection

The `PrecedentGraphEngine` enforces a strict invariant:
```python
if edge.treatment == TreatmentType.OVERRULED:
    if citing_node.bench_judge_count < cited_node.bench_judge_count:
        raise ValueError(
            f"Jurisprudential Invariant Violation: Citing bench ({citing_node.bench_judge_count} judges) "
            f"cannot overrule larger bench ({cited_node.bench_judge_count} judges)."
        )
```
This protects against incorrect legal claims such as alleging a 2-judge bench overruled a 5-judge Constitution bench.
