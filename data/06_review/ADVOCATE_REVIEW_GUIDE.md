# LEGALMITRA ADVOCATE REVIEW GUIDE
**Controlled 20-Example Pilot Review Package**
*Version 1.0 — Phase 7.2 Release*

---

## 1. Overview and Purpose

Welcome to the LegalMitra Review Package. LegalMitra is an open-source Indian legal dataset engineering pipeline and retrieval-augmented generation (RAG) framework.

This package contains **20 carefully curated, source-grounded Question-and-Answer pairs** spanning:
1. **Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023)** and its phased commencement under Notification **G.S.R. 843(E)**.
2. **Information Technology Act, 2000 (Act No. 21 of 2000)** cyber offences and the operative validity of Section 43A.
3. **Bharatiya Sakshya Adhiniyam, 2023 (Act No. 47 of 2023)** electronic records admissibility (ss. 61 & 63).
4. **Bharatiya Nagarik Suraksha Sanhita, 2023 (Act No. 46 of 2023)** anticipatory bail exclusions (s. 482) and repeal/savings (s. 531).

All 20 records are currently designated as **`pending_legal_review`**. In accordance with legal-engineering ethics, automated validators are strictly prohibited from self-approving legal advice. We require your independent judgment as an advocate or legal scholar to review, score, and validate each record.

---

## 2. Review Artifacts

The review package in `data/06_review/` consists of:
1. **`ADVOCATE_REVIEW_GUIDE.md`** (this document): Review principles, statutory timeline, and scoring criteria.
2. **`pilot_20_review_sheet.csv`**: Review spreadsheet containing questions, answers, evidence spans, temporal tags, specific counsel questions, and blank decision/score fields.
3. **`pilot_20_source_bundle.json`**: Machine-readable JSON linking every record directly to raw statutory source texts, gazette notifications, and cryptographic checksums.
4. **`pilot_20_open_issues.md`**: In-depth legal analysis of the 6 prioritized statutory and procedural ambiguities.

---

## 3. Statutory Background & Temporal Timelines

To ensure accurate evaluation, please apply the following statutory milestones:

### A. Digital Personal Data Protection Act, 2023 (DPDP Act)
- **Enactment Date**: 11 August 2023 (Act No. 22 of 2023).
- **Commencement Schedule**: Notification **G.S.R. 843(E)** dated 13 November 2025:
  * **Group 1 (13 November 2025)**: Preliminary, definitions, Data Protection Board establishment, and specific oversight powers (ss. 2, 18–26, 35, 38–43, 44(1), 44(3)).
  * **Group 2 (13 November 2026 / 1 Year)**: Section 6(9) (notice of pre-existing consent) and Section 27(1)(d).
  * **Group 3 (13 May 2027 / 18 Months)**: Substantive consent and fiduciary obligations, Data Principal rights, penalties, and IT Act amendments (ss. 3–5, 6(1)–(8), (10), 7–17, balance of 27, 28–34, 36, 37, 44(2)).
  * *Note on Calculation*: 18 calendar months computed from 13 November 2025 under Section 9 of the General Clauses Act, 1897 concludes on **13 May 2027**.

### B. Information Technology Act, 2000 (IT Act)
- **Section 43A**: Compensation for failure to protect sensitive personal data.
- **Operative Status**: While DPDP Act s. 44(2)(a) omits s. 43A, Section 44(2) falls under Group 3 (13 May 2027). Therefore, **Section 43A remains fully operative, valid, and enforceable law until 13 May 2027**.
- **Cyber Offences**: ss. 66, 66C, 66D are in force since 27 October 2009 (Act 10 of 2009).

### C. Bharatiya Sakshya Adhiniyam, 2023 (BSA)
- **Commencement Date**: 1 July 2024 via Notification **S.O. 849(E)**.
- **Electronic Records**: Section 61 provides that electronic records have documentary enforceability, **subject to Section 63** and mandatory certificate under Section 63(4).

### D. Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)
- **Commencement Date**: 1 July 2024 via Notification **S.O. 848(E)**.
- **Section 482**: Anticipatory bail jurisdiction before High Court and Court of Session; sub-section (4) bars anticipatory bail for offences under BNS ss. 65 & 70(2).
- **Section 531 Anti-Conflation**: Section 531 is an **in-force provision** of the BNSS. It repeals the Code of Criminal Procedure, 1973 with savings for pending appeals, applications, trials, inquiries, and investigations.

---

## 4. Review Rubric & Scoring Criteria

When reviewing records in `pilot_20_review_sheet.csv`, please evaluate three dimensions on a **1 to 5 scale**:

### 1. Legal Accuracy (1 to 5)
- **5 (Exemplary)**: Completely sound legal reasoning; flawless interpretation of statutory terms; fully reflects Indian jurisprudence.
- **4 (Sound)**: Substantively correct; minor stylistic or terminology preference could improve clarity.
- **3 (Acceptable with Reservation)**: Correct in outcome but omits important nuances, qualifications, or provisos.
- **2 (Inaccurate)**: Mischaracterizes a statutory provision or confuses distinct legal standards.
- **1 (Legally Erroneous)**: Blatantly incorrect legal claim or hallucination.

### 2. Temporal Accuracy (1 to 5)
- **5 (Flawless)**: Precisely distinguishes current law from enacted-uncommenced provisions; accurately cites Gazette notifications.
- **4 (Substantially Accurate)**: Correctly identifies current vs future status; notification citation is accurate.
- **3 (Ambiguous)**: Notes that law is changing but does not clearly specify whether rights are currently enforceable today.
- **1–2 (Temporal Defect)**: Asserts that an uncommenced right is operative today, or falsely claims an in-force law is repealed.

### 3. Grounding & Zero-Hallucination (1 to 5)
- **5 (Strictly Grounded)**: Every proposition in the answer directly flows from the verbatim evidence passage.
- **4 (Well Grounded)**: Completely supported; slight restatement or synthesis without adding ungrounded facts.
- **3 (Extrapolated)**: Answer brings in general knowledge or commentary not present in the cited evidence passage.
- **1–2 (Ungrounded)**: Invented section numbers, non-existent qualifications, or fabricated facts.

---

## 5. Review Decisions

For each record, enter one of the following in the `review_decision` column:
- **`APPROVED`**: Record meets high standards of legal correctness and temporal grounding.
- **`REVISION_REQUIRED`**: Record is conceptually salvageable but requires specific edits to question, answer, or citation.
- **`REJECTED`**: Record has fundamental legal defects, is ungrounded, or misleads users.

---

## 6. How to Submit Your Review

1. Open `data/06_review/pilot_20_review_sheet.csv` in Excel, LibreOffice Calc, or your preferred CSV editor.
2. Review each record alongside the source texts provided in `pilot_20_source_bundle.json`.
3. Consult `pilot_20_open_issues.md` when reviewing the 6 prioritized ambiguity records.
4. Fill in `review_decision`, scores (1-5), `reviewer_comments`, `reviewer_name_initials`, and `review_date`.
5. Save the CSV and return it to the LegalMitra dataset maintainers.
