# PHASE 47: PRECEDENT-TO-STATUTE KNOWLEDGE GRAPH SPECIFICATION

**Project:** LegalMitra  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Date:** October 19, 2026  

---

## 1. Architecture of Precedent-to-Statute Links

LegalMitra integrates judicial rulings directly into its statutory graph, connecting Supreme Court and High Court judgments to specific provisions, temporal validity intervals, and paragraph anchors.

The dedicated manifest `data/22_central_legislation/precedent_statute_manifest.json` under `LEGALMITRA-PRECEDENT-STATUTE-V1` models 10 verified precedent relationships.

---

## 2. Master Precedent-to-Statute Register

| Link ID | Case Title & Citation | Target Statute & Section | Validity Applied | Rel Type | Paragraph Anchor | Core Holding |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| `PREC-LINK-01` | *Novartis AG v. Union of India* (2013) 6 SCC 1 | Patents Act 1970 s.3(d) | `[2005-01-01, 9999)` | `INTERPRETS` | Paras 157–192 | Efficacy means therapeutic efficacy for medicines; polymorph physicochemical properties insufficient. |
| `PREC-LINK-02` | *Bayer Corp. v. Union of India* 2014 SCC OnLine Bom 563 | Patents Act 1970 s.84 | `[2003-05-20, 9999)` | `APPLIES` | Paras 42–65 | Upholds compulsory license to Natco for Sorafenib (Nexavar); ₹2.8L/month price unaffordable to public. |
| `PREC-LINK-03` | *Eastern Book Co. v. D.B. Modak* (2008) 1 SCC 1 | Copyright Act 1957 s.13 | `[1958-01-21, 9999)` | `INTERPRETS` | Paras 54–58 | Modicum of creativity standard for originality; headnotes protected, copy-editing mechanical. |
| `PREC-LINK-04` | *R.G. Anand v. Delux Films* (1978) 4 SCC 118 | Copyright Act 1957 s.51 | `[1958-01-21, 9999)` | `INTERPRETS` | Paras 45–46 | Idea-expression dichotomy; substantial similarity test; no copyright in themes or historical facts. |
| `PREC-LINK-05` | *Oxford Univ. v. Rameshwari Photocopy* (2016) 160 DRJ 678 | Copyright Act 1957 s.52(1)(i) | `[2012-06-21, 9999)` | `INTERPRETS` | Paras 81–94 | Course packs compiled for students by university/photocopy kiosk protected under fair dealing exception. |
| `PREC-LINK-06` | *Cadila Health Care v. Cadila Pharma* (2001) 5 SCC 73 | Trade Marks Act 1999 s.11/29 | `[2003-09-15, 9999)` | `INTERPRETS` | Paras 32–35 | Stricter test for medicinal trade marks; confusion can cause lethal consequences; Schedule H no defense. |
| `PREC-LINK-07` | *Bangalore Water Supply v. A. Rajappa* (1978) 2 SCC 213 | IDA 1947 s.2(j) | `[1947-04-01, 9999)` | `INTERPRETS` | Paras 140–143 | Triple test for industry: systematic activity, employer-employee cooperation, production/distribution. |
| `PREC-LINK-08` | *Excel Wear v. Union of India* (1978) 4 SCC 224 | IDA 1947 s.25-O | `[1976-03-05, 1978-09-29)`| `INVALIDATES` | Paras 28–34 | Struck down original Section 25-O closure permission under Art. 19(1)(g); prompted 1984 reenactment. |
| `PREC-LINK-09` | *Workmen of American Express v. Mgmt* (1985) 4 SCC 71 | IDA 1947 s.25F | `[1953-10-24, 9999)` | `APPLIES` | Paras 4–6 | Continuous service of 240 days includes Sundays and paid holidays for retrenchment compensation. |
| `PREC-LINK-10` | *Manish Kumar v. Union of India* (2021) 5 SCC 1 | IBC 2016 s.32A | `[2019-12-28, 9999)` | `APPLIES` | Paras 320–332 | Upholds Section 32A clean-slate immunity for corporate debtor and new resolution management. |
