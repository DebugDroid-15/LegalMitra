# LEGALMITRA PHASE 24: CASE IDENTITY & PROCEDURAL TIMELINES REPORT

**Classification:** Proprietary & Confidential — Team Shatrujeet  
**Phase:** 24 — Master Expansion  
**Date:** October 2026  
**Status:** Ingested & Verified  

---

## 1. Executive Summary

Phase 24 expanded the deterministic litigation records of LegalMitra from 4 cases to 14 unified cases across the Supreme Court of India. Each case record models canonical case identifiers (`court_code`, `case_type`, `case_number`, `filing_year`), party names, disposal status, neutral citations, and reporter citations.

Additionally, interim orders, notice orders, reference orders to Constitution Benches, and dated hearing events were reconstructed into `data/legalmitra_kb.db`.

---

## 2. Reconstructed Case Entities (Cases Table)

| Canonical Case ID | Court | Case Number | Parties | Disposal Date | Neutral Citation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `IN-SC-WP-231-1977` | IN-SC | WP (C) 231/1977 | Maneka Gandhi v. Union of India | 1978-01-25 | 1978 INSC 16 |
| `IN-SC-WP-135-1970` | IN-SC | WP (C) 135/1970 | Kesavananda Bharati v. State of Kerala | 1973-04-24 | 1973 INSC 258 |
| `IN-SC-WP-592-1987` | IN-SC | WP (Crl) 592/1987 | D.K. Basu v. State of West Bengal | 1996-12-18 | 1996 INSC 1599 |
| `IN-SC-WP-68-2008` | IN-SC | WP (Crl) 68/2008 | Lalita Kumari v. Govt of UP | 2013-11-12 | 2013 INSC 798 |
| `IN-SC-CRL-1277-2014` | IN-SC | Crl.A. 1277/2014 | Arnesh Kumar v. State of Bihar | 2014-07-02 | 2014 INSC 492 |
| `IN-SC-WP-167-2012` | IN-SC | WP (Crl) 167/2012 | Shreya Singhal v. Union of India | 2015-03-24 | 2015 INSC 244 |
| `IN-SC-SLP-7281-2017` | IN-SC | SLP (Crl) 7281/2017 | Sushila Aggarwal v. State (NCT of Delhi) | 2020-01-29 | 2020 INSC 106 |
| `IN-SC-CA-2402-2019` | IN-SC | CA 2402/2019 | Vidya Drolia v. Durga Trading Corp | 2020-12-14 | 2020 INSC 697 |
| `IN-SC-CRL-144-2004` | IN-SC | Crl.A. 144/2004 | Jacob Mathew v. State of Punjab | 2005-08-05 | 2005 INSC 372 |
| `IN-SC-CA-5399-2016` | IN-SC | CA 5399/2016 | Energy Watchdog v. CERC | 2017-04-11 | 2017 INSC 328 |

---

## 3. Order & Hearing Timeline Reconstruction

The Knowledge Base engine method `kb.get_case_procedural_timeline(case_id)` was validated across multi-stage proceedings:

1. **`IN-SC-WP-231-1977` (*Maneka Gandhi*)**:
   - `1977-07-18`: Hearing Event `EVT-SC-1977-07-18` (Admission Hearing, Presiding Bench: Beg C.J., Bhagwati J.).
   - `1977-07-18`: Notice Order `IND-ORD-SC-1977-MANEKA-NOTICE` (Rule Nisi issued returnable in two weeks).
   - `1978-01-25`: Final Judgment `IND-JUD-SC-1978-MANEKA-GANDHI` (7-Judge Constitution Bench).

2. **`IN-SC-SLP-7281-2017` (*Sushila Aggarwal*)**:
   - `2018-05-15`: Regular Hearing Event `EVT-SC-2018-05-15` (Kurian Joseph J., Mohan M. Shantanagoudar J.).
   - `2018-05-15`: Reference Order `IND-ORD-SC-2018-SUSHILA-REF` (Referred to 5-Judge Constitution Bench due to conflicting lines on whether anticipatory bail can be time-limited).
   - `2020-01-29`: Final Judgment `IND-JUD-SC-2020-SUSHILA-AGGARWAL` (Anticipatory bail ordinarily should not be limited in duration).

3. **`IN-SC-CA-2402-2019` (*Vidya Drolia*)**:
   - `2019-02-28`: Regular Hearing Event `EVT-SC-2019-02-28` (A.K. Sikri J., S. Abdul Nazeer J.).
   - `2019-02-28`: Reference Order `IND-ORD-SC-2019-VIDYA-REF` (Doubting *Himangni Enterprises* regarding landlord-tenant disputes arbitrability; referring to 3-Judge Bench).
   - `2020-12-14`: Final Judgment `IND-JUD-SC-2021-VIDYA-DROLIA` (Overruling *Himangni Enterprises*; establishing four-fold arbitrability test).
