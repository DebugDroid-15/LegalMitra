# LEGALMITRA PHASE 24: JUDICIAL ACQUISITION & CORPUS EXPANSION REPORT

**Classification:** Proprietary & Confidential — Team Shatrujeet  
**Phase:** 24 — Master Expansion  
**Date:** October 2026  
**Status:** Ingested & Verified  

---

## 1. Executive Summary

In Phase 24, LegalMitra expanded its authoritative judicial corpus from 11 decisions to 21 decisions, acquiring 10 landmark Supreme Court precedents across constitutional law, criminal procedure, personal liberty, digital speech, arbitration, medical jurisprudence, and commercial contract law.

All acquired decisions were indexed from verified official sources (Supreme Court Digital SCR / main.sci.gov.in / Judgments Information System) under statutory public-domain provisions (Section 52(1)(q)(iv) of the Copyright Act, 1957).

Total chunks indexed for judicial decisions grew by 33 chunks, maintaining exact paragraph-level attribution, structured holdings, bench coram details, and constitutional ratio decidendi.

---

## 2. Inventory of Phase 24 Judicial Decisions

| Document ID | Case Title & Citation | Bench Strength | Primary Subject / Proposition |
| :--- | :--- | :--- | :--- |
| `IND-JUD-SC-1978-MANEKA-GANDHI` | *Maneka Gandhi v. Union of India* (1978) 1 SCC 248 | 7 Judges | Article 21 'procedure established by law' must be just, fair and reasonable; Golden Triangle (Arts 14, 19, 21). |
| `IND-JUD-SC-1973-KESAVANANDA` | *Kesavananda Bharati v. State of Kerala* (1973) 4 SCC 225 | 13 Judges | Basic Structure Doctrine; Parliament cannot alter the basic structure under Article 368. |
| `IND-JUD-SC-1997-DK-BASU` | *D.K. Basu v. State of West Bengal* (1997) 1 SCC 416 | 2 Judges | Mandatory guidelines for arrest and detention under Articles 21 and 22(1); memo of arrest, medical exam. |
| `IND-JUD-SC-2014-LALITA-KUMARI` | *Lalita Kumari v. Govt. of U.P.* (2014) 2 SCC 1 | 5 Judges | Section 154 CrPC mandatory registration of FIR upon disclosure of cognizable offence; preliminary inquiry scope. |
| `IND-JUD-SC-2014-ARNESH-KUMAR` | *Arnesh Kumar v. State of Bihar* (2014) 8 SCC 273 | 2 Judges | Section 41 CrPC mandatory compliance for offences punishable up to 7 years; checklist, arrest safeguards. |
| `IND-JUD-SC-2015-SHREYA-SINGHAL` | *Shreya Singhal v. Union of India* (2015) 5 SCC 1 | 2 Judges | Striking down Section 66A of IT Act as unconstitutional; discussion vs. advocacy vs. incitement. |
| `IND-JUD-SC-2020-SUSHILA-AGGARWAL` | *Sushila Aggarwal v. State (NCT of Delhi)* (2020) 5 SCC 1 | 5 Judges | Section 438 CrPC anticipatory bail cannot be restricted to a fixed period; affirms *Gurbaksh Singh Sibbia*. |
| `IND-JUD-SC-2021-VIDYA-DROLIA` | *Vidya Drolia v. Durga Trading Corp.* (2021) 2 SCC 1 | 3 Judges | Four-fold test for non-arbitrability; overrules *Himangni Enterprises*; tenancy disputes under TPA are arbitrable. |
| `IND-JUD-SC-2005-JACOB-MATHEW` | *Jacob Mathew v. State of Punjab* (2005) 6 SCC 1 | 3 Judges | Medical negligence under Section 304A IPC; *Bolam* test adoption; gross negligence standard. |
| `IND-JUD-SC-2017-ENERGY-WATCHDOG` | *Energy Watchdog v. CERC* (2017) 14 SCC 80 | 2 Judges | Section 32 & 56 Contract Act; frustration vs. contingent contract; rise in price does not constitute frustration. |

---

## 3. Storage Hierarchy & Table Reconciliation

The Phase 24 batch script `scripts/run_phase24_judicial_batch.py` updated the primary relational tables in `data/legalmitra_kb.db`:

- **`sources` table**: 57 total sources registered (+10 landmark decisions).
- **`legal_chunks` table**: 1,495 total chunks (+33 chunks from 10 judgments: ratios, holdings, verbatim paragraphs).
- **`cases` table**: 14 unified cases (+10 cases with deterministic case IDs and neutral citations).
- **`judicial_documents` table**: 7 order/proceeding records (+4 interim orders and notice orders).
- **`hearing_events` table**: 6 dated hearing events (+4 verified cause-list / listing events).

---

## 4. Preservation & Quarantine Adherence

1. **Synthetic Scaffold Quarantine**: `IND-JUD-DEL-2024-BAIL` remains strictly isolated (`is_synthetic_scaffold = 1`). Exact count of scaffold chunks remains 6.
2. **Phase 9 Freeze Integrity**: Verified 100% bitwise matching via `scripts/verify_freeze.py`.
3. **Pending Review Packages**: All 40 advocate review records in Package A and Package B verified in `pending_legal_review` status via `scripts/verify_review_packages.py`.
4. **No Synthetic Precedents**: All judgments are genuine reported decisions with official SCC and INSC citations.
