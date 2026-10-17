# PHASE 21 — UNIFIED CASE IDENTITY, ORDER CLASSIFICATION & PROCEDURAL LIFECYCLE
## Disentangling Cases, Proceedings, Orders, Hearings and Cause Lists

**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Repository:** `https://github.com/DebugDroid-15/LegalMitra`  
**Workspace:** `C:\PROJECTS\LegalMitra`  
**Owner:** Team Shatrujeet — Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo  
**Classification:** Proprietary and Confidential  
**Date:** October 2026  
**Status:** Ingested & Verified  

---

## 1. Doctrinal Foundations

In judicial data systems, conflating a *case* with a *document* or an *event* causes severe data corruption:
- A single **Case** (e.g., Civil Appeal Nos. 2082-2083 of 2018) spans years and generates multiple filings, daily orders, interim orders, and one final judgment.
- A **Hearing** is a physical or virtual proceeding on a specific listing date.
- A **Cause List Entry** proves that a matter was *scheduled*; it does not establish that arguments were heard or an order was passed.
- An **Interim Order** (e.g., notice or stay) differs fundamentally in legal effect and finality from a **Final Judgment** on the merits.

Phase 21 introduces `legalmitra/caselaw/case_identity.py` and dedicated relational schema tables (`cases`, `judicial_documents`, `hearing_events`) in `data/legalmitra_kb.db`.

---

## 2. Relational Schema Architecture

```
                  +-----------------------------------+
                  |             CASES                 |
                  | (case_id, court_code, case_type,  |
                  |  case_number, filing_year, ...)   |
                  +-----------------+-----------------+
                                    |
          +-------------------------+-------------------------+
          | 1:N                                               | 1:N
          v                                                   v
+-------------------------------+             +-------------------------------+
|       JUDICIAL_DOCUMENTS      |             |         HEARING_EVENTS        |
| (document_id, classification, |             | (event_id, listing_date,      |
|  procedural_effect, date,     |             |  hearing_type, outcome,       |
|  verbatim_text, sha256_hash)  |             |  daily_order_id, next_date)   |
+-------------------------------+             +-------------------------------+
```

---

## 3. Controlled Document Taxonomy

| Classification | Legal Definition | Typical Procedural Effect |
| :--- | :--- | :--- |
| `FINAL_JUDGMENT` | Conclusive determination of rights and liabilities on merits | Appeal allowed/dismissed, conviction affirmed/reversed |
| `FINAL_ORDER` | Conclusive disposal of an application or proceeding | Disposed of with directions |
| `INTERIM_ORDER` | Interlocutory relief pending final adjudication | Interim stay granted, status quo, reference to larger bench |
| `DAILY_ORDER` | Record of proceedings on a particular hearing date | Matter adjourned, arguments part-heard |
| `NOTICE_ORDER` | Formal process requiring respondent appearance | Notice issued returnable in N weeks |
| `STAY_ORDER` | Injunction restraining operation of decree or executive action | Operation stayed subject to deposit/conditions |
| `BAIL_ORDER` | Release of undertrial or convict on bail bond | Regular bail granted/rejected, anticipatory bail |
| `CAUSE_LIST` | Official schedule of matters posted before a bench | Matter listed (outcome unverified until order published) |

---

## 4. Deterministic Identity Resolution

The `CaseIdentityResolver` enforces strict deterministic matching based on:
$$\text{Match}(\text{CourtCode}, \text{CaseType}, \text{CaseNumber}, \text{FilingYear})$$
Fuzzy matching on party names is strictly confined to candidate generation and never automatically merges records across distinct courts or years.

