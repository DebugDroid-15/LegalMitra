# LEGALMITRA — PHASE 48
## Central Delegated Legislation Registry Specification

**Document ID:** `LM-DOC-PHASE48-DELEGATED-REGISTRY-01`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Phase:** 48  
**Author:** Shatrujeet Legal Engineering Team  
**Status:** IMPLEMENTED AND EVIDENCE-VERIFIED  
**Date:** 2026-10-19  

---

### 1. Purpose and Scope

Delegated (subordinate) legislation—rules, regulations, orders, notifications, and bye-laws framed by executive authorities under enabling provisions of parent Central Acts—is an indispensable source of operational law. LegalMitra previously modeled primary statutes and amendments; Phase 48 implements a Central Delegated Legislation Registry (`delegated_legislation_manifest.json`) linking rules to parent enactments and tracking enabling sections, gazette publication dates, commencement dates, and historical supersessions.

---

### 2. Registered Delegated Instruments

| Instrument ID | Official Title | Parent Statute | Enabling Sections | Gazette Ref | Commencement | Supersedes |
|---|---|---|---|---|---|---|
| `IND-RULE-COPYRIGHT-2013` | Copyright Rules, 2013 | Copyright Act, 1957 (`IND-STAT-COPYRIGHT-1957`) | Section 78 | G.S.R. 172(E) | 2013-03-14 | Copyright Rules, 1958 |
| `IND-RULE-PATENTS-2003` | Patents Rules, 2003 | Patents Act, 1970 (`IND-STAT-PATENTS-1970`) | Section 159 | S.O. 493(E) | 2003-05-20 | Patents Rules, 1972 |
| `IND-RULE-COMP-CSR-2014` | Companies (CSR Policy) Rules, 2014 | Companies Act, 2013 (`IND-STAT-COMP-2013`) | Section 135, 469(1), 469(2) | G.S.R. 129(E) | 2014-04-01 | None (Fresh) |
| `IND-RULE-TRADEMARKS-2017` | Trade Marks Rules, 2017 | Trade Marks Act, 1999 (`IND-STAT-TRADEMARKS-1999`) | Section 157 | G.S.R. 199(E) | 2017-03-06 | Trade Marks Rules, 2002 |

---

### 3. Enabling Relationship Modeling

In the national judicial knowledge graph, enabling sections are connected to subordinate rules using the `EMPOWERS` relation:
- `SEC-COP-78` --`EMPOWERS`--> `RULE-COPYRIGHT-2013`
- `SEC-PAT-159` --`EMPOWERS`--> `RULE-PATENTS-2003`
- `SEC-CA-469` --`EMPOWERS`--> `RULE-COMPANIES-CSR-2014`
- `SEC-TM-157` --`EMPOWERS`--> `RULE-TRADEMARKS-2017`

The temporal engine exposes:
```python
temporal_engine.resolve_delegated_rule_for_statute(statute_id: str, section: Optional[str] = None) -> List[Dict[str, Any]]
```
This guarantees that queries regarding delegated rules return their verified gazette authority and parent section anchors.
