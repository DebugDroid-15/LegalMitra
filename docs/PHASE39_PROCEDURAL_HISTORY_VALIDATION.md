# LegalMitra — Phase 39: District-to-Supreme-Court Procedural History Validation

**Document Version:** 1.0.0  
**Phase:** 39 — National Judicial Corpus Expansion & Precedent Verification  
**Status:** Completed & Validated  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  

---

## 1. Executive Summary

This document specifies the validation of the District-to-Supreme-Court Procedural History Graph implemented in Phase 39 Workstream I and [`ProceduralHistoryGraph`](file:///c:/PROJECTS/LegalMitra/legalmitra/judicial/procedural_history.py). Litigation in India rarely proceeds as an isolated appellate step; rather, it traverses trial courts, High Court division benches, appeals, reviews, and curative remedies.

Machine-readable graph: `data/21_judicial_infrastructure/procedural_history_graph.json`.

---

## 2. End-to-End Procedural Trajectory Case Studies

### 2.1 Trajectory 1: Constitutional Decriminalization of Section 377 IPC
- **Chain ID:** `CHAIN-SEC377-DECRIM`
- **Stage 1 (High Court Division Bench)**: High Court of Delhi (*Naz Foundation*, WP (C) No. 7455/2001, decided July 2, 2009 by A.P. Shah C.J. and S. Muralidhar J.). Read down Section 377 IPC.
- **Stage 2 (Supreme Court Appeal)**: Supreme Court of India (*Suresh Kumar Koushal*, Civil Appeal No. 10972/2013, decided Dec 11, 2013 by G.S. Singhvi and S.J. Mukhopadhaya JJ.). Reversed Delhi High Court.
- **Stage 3 (Constitution Bench Final Adjudication)**: Supreme Court of India (*Navtej Singh Johar*, WP (Crl) No. 76/2016, decided Sept 6, 2018 by 5-Judge Constitution Bench). Overruled *Suresh Koushal* and restored decriminalization.

### 2.2 Trajectory 2: Complete Capital Punishment & Curative Lifecycle (Nirbhaya Case)
- **Chain ID:** `CHAIN-NIRBHAYA-MURDER`
- **Stage 1 (Trial Court Final Judgment)**: Court of Additional Sessions Judge (Fast Track), Saket Courts, New Delhi (Sessions Case No. 114/2013, decided Sept 13, 2013). Convicted and sentenced to death.
- **Stage 2 (High Court Confirmation & Appeal)**: High Court of Delhi (Death Sentence Reference No. 6/2013, decided March 13, 2014). Confirmed capital sentence under Section 368 CrPC.
- **Stage 3 (Supreme Court Criminal Appeal)**: Supreme Court of India (Criminal Appeal Nos. 607-608/2017, decided May 5, 2017). Affirmed death penalty under rarest of rare doctrine.
- **Stage 4 (Supreme Court Review Petition)**: Supreme Court of India (Review Petition (Crl.) Nos. 670-671/2017, decided July 9, 2018). Dismissed review.
- **Stage 5 (Supreme Court Curative Petition)**: Supreme Court of India (Curative Petition (Crl.) Nos. 1-4/2020, decided Jan 14, 2020 by 5-Judge Bench). Dismissed curative petition under *Rupa Ashok Hurra* principles.

---

## 3. Grounded Procedural Graph Verification

Every recorded event is tied to an explicit filing number, order date, presiding judge coram, disposal nature, and preceding event identifier. Unsubstantiated or speculative procedural links are strictly barred.
