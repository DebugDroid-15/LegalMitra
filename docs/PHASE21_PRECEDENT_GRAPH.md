# PHASE 21 — PRECEDENT GRAPH, AUTHORITY STATUS & STATUTORY LINKAGE
## Proposition-Aware Precedents, Partial Overruling and Bi-Temporal Statutory Connections

**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Repository:** `https://github.com/DebugDroid-15/LegalMitra`  
**Workspace:** `C:\PROJECTS\LegalMitra`  
**Owner:** Team Shatrujeet — Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo  
**Classification:** Proprietary and Confidential  
**Date:** October 2026  
**Status:** Ingested & Verified  

---

## 1. Executive Summary

LegalMitra Phase 21 integrates judicial decisions with the statutory corpus produced in earlier phases. Rather than treating legal citations as unstructured strings, Phase 21 builds a multi-relational knowledge graph linking:
1. Specific sections/articles to the cases that interpret them.
2. Judicial decisions to predecessor or successor cases via `FOLLOWS`, `APPLIES`, `DISTINGUISHES`, and `OVERRULES`.
3. Proposition-level partial overruling without crude negative suppression of unaffected legal doctrines.

Implementation: `legalmitra/caselaw/knowledge_graph.py` with factory builder `build_national_judicial_knowledge_graph()`.

---

## 2. Ingested Precedent Relationships Matrix

| Source Case (Citing / Later) | Target Case (Cited / Earlier) | Precedent Relation | Subject Matter & Proposition Scope |
| :--- | :--- | :--- | :--- |
| *Arjun Panditrao Khotkar* (2020) 7 SCC 1 | *Anvar P.V. v. P.K. Basheer* (2014) 10 SCC 473 | `FOLLOWS` / `AFFIRMS` | Affirmed mandatory requirement of s.65B certificate for secondary electronic records. |
| *Arjun Panditrao Khotkar* (2020) 7 SCC 1 | *Shafhi Mohammad v. State of H.P.* (2018) 2 SCC 801 | `PARTIALLY_OVERRULES` | Overruled dictum relaxing certificate requirement when party is not in possession of device. |
| *Rangappa v. Sri Mohan* (2010) 11 SCC 441 | *Krishna Janardhan Bhat* (2008) 4 SCC 54 | `OVERRULES` | Overruled proposition that Section 139 NI Act presumption does not extend to existence of legally enforceable debt. |
| *In Re: Arbitration & Stamp Act* (2024) 6 SCC 1 | *NN Global Mercantile* (2023) 7 SCC 1 | `OVERRULES` | Overruled holding that unstamped arbitration agreement is void ab initio at s.11 referral stage. |
| *In Re: Arbitration & Stamp Act* (2024) 6 SCC 1 | *SMS Tea Estates* (2011) 14 SCC 66 | `OVERRULES` | Overruled prohibition on referral courts acting on unstamped contracts. |

---

## 3. Statutory Provision Interpretation Links

Judicial holdings are directly linked to exact statutory provisions:

- `SEC-BSA-63` (Bharatiya Sakshya Adhiniyam, 2023 s.63) $\leftarrow$ `INTERPRETS` $\leftarrow$ *Arjun Panditrao Khotkar*
- `SEC-IEA-65B` (Indian Evidence Act, 1872 s.65B) $\leftarrow$ `INTERPRETS` $\leftarrow$ *Arjun Panditrao Khotkar* & *Anvar P.V.*
- `SEC-NI-138` (Negotiable Instruments Act, 1881 s.138) $\leftarrow$ `INTERPRETS` $\leftarrow$ *Rangappa v. Sri Mohan*
- `SEC-NI-139` (Negotiable Instruments Act, 1881 s.139) $\leftarrow$ `INTERPRETS` $\leftarrow$ *Rangappa v. Sri Mohan*
- `SEC-ARB-11` (Arbitration & Conciliation Act, 1996 s.11) $\leftarrow$ `INTERPRETS` $\leftarrow$ *In Re: Arbitration Agreements & Stamp Act*
- `SEC-ARB-16` (Arbitration & Conciliation Act, 1996 s.16) $\leftarrow$ `INTERPRETS` $\leftarrow$ *In Re: Arbitration Agreements & Stamp Act*
- `ART-CONST-21` (Constitution of India Art. 21) $\leftarrow$ `INTERPRETS` $\leftarrow$ *Justice K.S. Puttaswamy v. Union of India*

---

## 4. Proposition Scope and Partial Overruling Safeguard

LegalMitra prevents false negative suppression through proposition-scoped evaluation:
```python
status_detail = graph.evaluate_precedent_status("CASE-SHAFHI-MOHD")
# Result:
# status: "partially_overruled"
# scope: "Electronic evidence certificate waiver"
# unaffected doctrines remain active precedent
```
If a user queries general principles of fair trial or electronic custody not touched by *Arjun Khotkar*, the system correctly distinguishes the overruled proposition from the surviving judgment record.

