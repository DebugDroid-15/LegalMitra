# LEGALMITRA — PHASE 48
## Supreme Court Constitution Bench Jurisprudence Architecture

**Document ID:** `LM-DOC-PHASE48-CONST-BENCH-01`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Phase:** 48  
**Author:** Shatrujeet Legal Engineering Team  
**Status:** IMPLEMENTED AND EVIDENCE-VERIFIED  
**Date:** 2026-10-19  

---

### 1. Executive Summary

Phase 48 establishes a structured constitutional jurisprudence layer in LegalMitra. While earlier phases modeled statutory sections and ordinary appellate precedents, Phase 48 models the foundational constitutional jurisprudence of the Supreme Court of India rendered by **Constitution Benches** (Article 145(3) benches consisting of 5 or more judges).

Eight landmark Constitution Bench decisions have been integrated with complete structural fidelity:
1. **Kesavananda Bharati v. State of Kerala (1973) 4 SCC 225** (13 Judges, 7:6 majority) — Basic Structure doctrine limiting amending power under Article 368; invalidation of unreviewable clause in Article 31C.
2. **Minerva Mills Ltd. v. Union of India (1980) 3 SCC 625** (5 Judges, 4:1 majority) — Invalidation of Article 368(4) and (5); harmony between Fundamental Rights and Directive Principles.
3. **Maneka Gandhi v. Union of India (1978) 1 SCC 248** (7 Judges, 7:0 unanimous) — Substantive due process; Golden Triangle (Articles 14, 19, 21); requirement that procedure established by law must be just, fair, and reasonable.
4. **I.R. Coelho v. State of Tamil Nadu (2007) 2 SCC 1** (9 Judges, 9:0 unanimous) — Post-24.04.1973 Ninth Schedule laws subject to judicial review against the Basic Structure and Part III rights.
5. **Justice K.S. Puttaswamy (Retd.) v. Union of India (2017) 10 SCC 1** (9 Judges, 9:0 unanimous) — Fundamental right to privacy under Article 21; express overruling of M.P. Sharma (1954) and ADM Jabalpur (1976); proportionality test.
6. **S.R. Bommai v. Union of India (1994) 3 SCC 1** (9 Judges) — Judicial review of Article 356 Presidential proclamations; secularism and federalism as basic features; floor test requirement before Legislative Assembly dissolution.
7. **In re: The Delhi Laws Act, 1912 (1951) SCR 747** (7 Judges) — Non-delegation of essential legislative functions under Articles 245/246.
8. **State of Madras v. Champakam Dorairajan (1951) SCR 525** (7 Judges, 7:0 unanimous) — Subordination of Directive Principles to Fundamental Rights; invalidation of Communal G.O.; directly prompted the Constitution (First Amendment) Act, 1951.

---

### 2. Constitution Bench Manifest Specification

All 8 cases are catalogued in `data/22_central_legislation/constitution_bench_manifest.json` under standard `LEGALMITRA-CONSTITUTIONAL-JURISPRUDENCE-SPEC-V1`. Each entry includes:
- Canonical citation and neutral citation (INSC).
- Bench strength and full verified roster of judges.
- Outcome breakdown and majority/dissent ratios.
- Target constitutional articles with paragraph-level anchor citations.
- Typed doctrinal relationships (`LIMITS`, `INTERPRETS`, `INVALIDATES`, `OVERRULES`, `PROMPTED_AMENDMENT`).
- Authenticity verification status.

---

### 3. Knowledge Graph and Temporal Engine Integration

The knowledge graph (`legalmitra/caselaw/knowledge_graph.py`) incorporates:
- Constitutional Article nodes (`ART-CONST-368`, `ART-CONST-31B`, `ART-CONST-31C`, `ART-CONST-245`, `ART-CONST-29`, `ART-CONST-15`, `ART-CONST-356`, `ART-CONST-21`).
- Constitution Bench case nodes (`CASE-SC-CONST-KESAVANANDA-1973`, etc.).
- Explicit interpretation and invalidation edges.

The temporal engine (`legalmitra/temporal/engine.py`) exposes:
```python
temporal_engine.resolve_constitution_bench_precedent(article_ref: str) -> List[Dict[str, Any]]
```
Resolving precedents against specific constitutional articles returns the governing Constitution Bench decisions, bench strengths, and doctrinal limits.
