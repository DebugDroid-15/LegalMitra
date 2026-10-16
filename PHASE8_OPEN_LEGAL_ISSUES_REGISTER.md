# LEGALMITRA — PHASE 8 OPEN LEGAL ISSUES & UNCERTAINTY REGISTER
**Corpus Provenance, Statutory Ambiguity & Source-Version Audit**
*Document ID*: `REGISTER-2026-PHASE8-001`  
*Date*: 16 October 2026  
*Auditor / Evaluation Engineer*: Senior Legal AI Evaluation Engineer  
*Review Status*: ALL RECORDS PENDING HUMAN ADVOCATE REVIEW  

---

## 1. Statutory Context & Principles

In accordance with legal engineering ethics, automated dataset pipelines and generative models must **never** resolve legal statutory ambiguities by algorithmic fiat, lexical frequency, or unsupervised synthesis. Where statutory text is silent, facially conflicting, or subject to diverging High Court precedents, LegalMitra explicitly maintains an open issues register and flags the affected records for advocate review.

This register analyzes the **six prioritized legal ambiguities** identified during Phase 7.2 and Phase 8.

---

## 2. Issue-by-Issue Legal Analysis

### Issue 1: Scope of Anticipatory Bail Exclusion Under BNSS Section 482(4)

#### A. Exact Legal Question
Does the absolute statutory bar on anticipatory bail enacted in Section 482(4) of the Bharatiya Nagarik Suraksha Sanhita, 2023 for offences under Section 65 and Section 70(2) of the Bharatiya Nyaya Sanhita, 2023 extend to an accused charged solely with **abetment** (BNS s. 45 / IPC s. 109), **attempt** (BNS s. 62 / IPC s. 511), or **criminal conspiracy** (BNS s. 61 / IPC s. 120B) to commit those offences?

#### B. Provisions & Primary Sources Involved
1. **Primary Statute**: Bharatiya Nagarik Suraksha Sanhita, 2023 (Act No. 46 of 2023), Section 482(4).
2. **Substantive Penal Code**: Bharatiya Nyaya Sanhita, 2023 (Act No. 45 of 2023), Sections 45, 61, 62, 65, 70(2).
3. **Predecessor Criminal Procedure**: Code of Criminal Procedure, 1973 (Act No. 2 of 1974), Section 438(4) (inserted by Criminal Law (Amendment) Act, 2018).
4. **Commencement Notification**: Ministry of Home Affairs Notification **S.O. 848(E)** dated 24 February 2024 (effective 1 July 2024).

#### C. What the Current Corpus Directly Supports
- The authentic statutory text of Section 482(4) BNSS directly states:
  > *"Nothing in this section shall apply to any case involving the arrest of any person on accusation of having committed an offence under section 65 and sub-section (2) of section 70 of the Bharatiya Nyaya Sanhita, 2023."*
- Section 65 BNS prescribes punishment for rape of a woman under 16 or 12 years of age.
- Section 70(2) BNS prescribes punishment for gang rape of a woman under 18 years of age.
- The statutory text makes no mention of inchoate offences, conspiracy, or abetment.

#### D. What Remains Interpretive or Uncertain
- Under predecessor Section 438(4) CrPC (which similarly excluded IPC ss. 376(3), 376AB, 376DA, 376DB), High Courts delivered conflicting rulings:
  * Some High Courts held that because penal exclusions restrict fundamental liberty under Article 21, they must be construed strictly (*strictissimi juris*); therefore, an accused facing only conspiracy or abetment charges is not disqualified at the threshold.
  * Other High Courts held that criminal conspiracy and abetment merge with the substantive offence under Section 120B/109 IPC when the offence is committed, bringing the accused within the statutory bar.
- There is currently no definitive Supreme Court constitutional bench ruling resolving this conflict under BNSS Section 482(4).

#### E. What a Qualified Advocate Must Decide
1. Whether LegalMitra answers must explicitly issue a practice warning that Section 482(4) disqualification for conspiracy/abetment depends on the jurisdiction of the specific High Court.
2. What drafting posture should be recommended for anticipatory bail applications involving multi-accused FIRs where roles are segregated.

#### F. Records Requiring Revision if Interpretation Changes
- Primary Record: `QA-PILOT-CROSS-009` (currently answers strictly on the four corners of s. 482(4)).
- Downstream Modules: Criminal procedural drafting templates and bail evaluation benchmarks.

---

### Issue 2: Operative Validity of IT Act Section 43A During DPDP Phased Rollout

#### A. Exact Legal Question
What is the precise operational and enforceable status of Section 43A of the Information Technology Act, 2000 as of 16 October 2026, and on what exact date does its omission under Section 44(2)(a) of the Digital Personal Data Protection Act, 2023 take legal effect?

#### B. Provisions & Primary Sources Involved
1. **Primary Statute**: Information Technology Act, 2000 (Act No. 21 of 2000), Section 43A.
2. **Subordinate Legislation**: Information Technology (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011 (SPDI Rules).
3. **Amending Statute**: Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023), Section 44(2)(a).
4. **Commencement Notification**: Ministry of Electronics and Information Technology Notification **G.S.R. 843(E)** dated 13 November 2025.
5. **Statutory Interpretation**: General Clauses Act, 1897 (Act No. 10 of 1897), Section 9.

#### C. What the Current Corpus Directly Supports
- Section 44(2)(a) DPDP Act enacts: *"section 43A shall be omitted"*.
- Notification G.S.R. 843(E) dated 13 November 2025 schedules Section 44(2) for commencement *"on the expiry of eighteen months from the date of publication of this notification in the Official Gazette"*.
- Computing 18 calendar months from 13 November 2025 under Section 9 of the General Clauses Act, 1897 excludes the day of publication and terminates on **13 May 2027**.
- On any date prior to 13 May 2027 (including our pilot baseline of 16 October 2026), Section 44(2) is enacted but uncommenced.

#### D. What Remains Interpretive or Uncertain
- Several commercial legal databases and trade journals prematurely reported Section 43A as omitted upon presidential assent on 11 August 2023.
- Whether corporate entities can be subjected to parallel inquiries under both the IT Act Adjudicating Officer (for pre-May 2027 data breaches) and the newly formed Data Protection Board of India (which commenced under Group 1 on 13 November 2025).

#### E. What a Qualified Advocate Must Decide
1. Confirm that Section 43A remains the sole statutory civil damages route for corporate failure to protect sensitive personal data prior to 13 May 2027.
2. Advise whether causes of action arising before 13 May 2027 survive omission under Section 6 of the General Clauses Act, 1897.

#### F. Records Requiring Revision if Interpretation Changes
- Primary Records: `QA-PILOT-DPDP-004`, `QA-PILOT-DPDP-009`, `QA-PILOT-DPDP-010`.
- Knowledge Base: RAG evaluation questions on cyber compensation.

---

### Issue 3: Asymmetrical Commencement of DPDP Act Section 6(9) vs General Consent

#### A. Exact Legal Question
How can a Data Fiduciary comply with Section 6(9) of the DPDP Act, 2023 (scheduled to commence on 13 November 2026 under Group 2) when the substantive notice contents under Section 5 and withdrawal mechanisms under Section 6(4) do not commence until 13 May 2027 (Group 3)?

#### B. Provisions & Primary Sources Involved
1. **Primary Statute**: Digital Personal Data Protection Act, 2023, Section 5, Section 6(1)–(10), Section 40 (rule-making power).
2. **Commencement Notification**: Notification **G.S.R. 843(E)** dated 13 November 2025.

#### C. What the Current Corpus Directly Supports
- Notification G.S.R. 843(E) places Section 6(9) in Group 2 (1 year / 13 Nov 2026).
- The rest of Section 6—sub-sections (1) to (8) and (10)—and Section 5 are placed in Group 3 (18 months / 13 May 2027).
- Section 6(9) requires notice to Data Principals who consented prior to the Act's commencement *"as soon as it is reasonably practicable"*.

#### D. What Remains Interpretive or Uncertain
- If Section 5 (which prescribes the mandatory contents of a notice) has not commenced, what statutory benchmark determines the legal validity of a Section 6(9) notice issued between November 2026 and May 2027?
- Can a Data Principal validly exercise a right of withdrawal under Section 6(4) in response to a Section 6(9) notice before Section 6(4) itself is in force?

#### E. What a Qualified Advocate Must Decide
1. Whether Section 6(9) in Group 2 implies an executive intent to issue subordinate rules under Section 40 governing transitional notices prior to November 2026.
2. Whether answers in LegalMitra should explicitly advise fiduciaries of this 6-month statutory hiatus.

#### F. Records Requiring Revision if Interpretation Changes
- Primary Records: `QA-PILOT-DPDP-005`, `QA-PILOT-DPDP-006`.

---

### Issue 4: Modeling BNSS Section 531 Savings vs CrPC 1973 Repeal

#### A. Exact Legal Question
How should legal AI schemas represent the status of Section 531 of the Bharatiya Nagarik Suraksha Sanhita, 2023 without conflating its contemporary primary validity with the repealed status of the Code of Criminal Procedure, 1973?

#### B. Provisions & Primary Sources Involved
1. **Contemporary Statute**: Bharatiya Nagarik Suraksha Sanhita, 2023, Section 531.
2. **Repealed Enactment**: Code of Criminal Procedure, 1973 (Act No. 2 of 1974), Sections 1–484.
3. **Commencement Notification**: Ministry of Home Affairs Notification **S.O. 848(E)** (effective 1 July 2024).

#### C. What the Current Corpus Directly Supports
- BNSS Section 531(1) expressly repeals the CrPC, 1973.
- Section 531(2)(a) mandates that any appeal, application, trial, inquiry, or investigation pending immediately before 1 July 2024 shall be disposed of, continued, held, or made in accordance with the CrPC, 1973 as if the BNSS had not come into force.
- Section 531 itself is fully in force and unrepealed.

#### D. What Remains Interpretive or Uncertain
- Recent High Court judgments (e.g. Delhi High Court in *Krishan Joshi v. State*, Punjab & Haryana High Court in *XXX v. State*) have debated whether bail applications filed *after* 1 July 2024 in respect of FIRs registered *before* 1 July 2024 must be instituted under CrPC Section 438/439 or BNSS Section 482/483.
- The prevailing view is that pending investigations remain governed by CrPC, but forum procedural choices continue to trigger preliminary objections in trial courts.

#### E. What a Qualified Advocate Must Decide
1. Endorse the Phase 7.2 schema decoupling: `law_status_label = in_force` for BNSS Section 531, while storing `repealed_statute_context = "CrPC 1973"` and `repealed_statute_status = repealed_with_savings`.
2. Confirm the guidance given to litigants regarding bail petitions arising from pre-July 2024 FIRs.

#### F. Records Requiring Revision if Interpretation Changes
- Primary Record: `QA-PILOT-CROSS-010`.

---

### Issue 5: Electronic Records Admissibility: BSA Section 61 vs Section 63 Certificate

#### A. Exact Legal Question
Does Section 61 of the Bharatiya Sakshya Adhiniyam, 2023 grant independent documentary admissibility to electronic records, or does its proviso read with Section 63 perpetuate the mandatory certificate requirement established in *Arjun Panditrao Khotkar* (2020) 7 SCC 1?

#### B. Provisions & Primary Sources Involved
1. **Primary Statute**: Bharatiya Sakshya Adhiniyam, 2023 (Act No. 47 of 2023), Sections 61, 62, 63.
2. **Predecessor Enactment**: Indian Evidence Act, 1872 (Act No. 1 of 1872), Sections 65A, 65B.
3. **Judicial Authority**: *Arjun Panditrao Khotkar v. Kailash Kushanrao Gorantyal* (2020) 7 SCC 1.
4. **Commencement Notification**: Ministry of Home Affairs Notification **S.O. 849(E)** (effective 1 July 2024).

#### C. What the Current Corpus Directly Supports
- Section 61 BSA provides that electronic records have the same legal effect as other documents, but expressly opens with *"subject to the provisions of section 63"*.
- The proviso to Section 61 mandates: *"Provided that where any electronic record is produced in evidence, it shall be accompanied by a certificate referred to in sub-section (4) of section 63."*
- Section 63(4) provides a structured certificate mechanism (Schedule, Part A, Part B) signed by a person in charge or an expert.

#### D. What Remains Interpretive or Uncertain
- Some early commentary suggested that BSA Section 61 eliminated the mandatory *Arjun Panditrao* requirement. However, statutory analysis of the proviso confirms that a Section 63(4) certificate remains an indispensable statutory accompaniment.
- Whether producing the physical original device under Section 62 obviates the need for a certificate under Section 63 remains an active subject of trial court debate.

#### E. What a Qualified Advocate Must Decide
1. Validate whether LegalMitra answers must take the conservative position that certificate compliance under Section 63(4) is mandatory in all electronic evidence tenders.
2. Advise whether failure to file the certificate with the initial police report under BNSS Section 193(3) can be cured by supplementary filing before charge framing.

#### F. Records Requiring Revision if Interpretation Changes
- Primary Records: `QA-PILOT-CROSS-001`, `QA-PILOT-CROSS-002`, `QA-PILOT-CROSS-003`, `QA-PILOT-CROSS-004`.

---

### Issue 6: Extrapolation Beyond Cited Statutory Excerpts

#### A. Exact Legal Question
To what extent may an automated legal Q&A dataset incorporate transitional context, cross-statute references, or Gazette notification citations not found within the verbatim four corners of the cited statutory excerpt?

#### B. Primary Evidence & Corpus Context
- In `QA-PILOT-DPDP-004`, the answer explains that until 13 May 2027, data security practices remain governed by the IT Act, 2000.
- In `QA-PILOT-CROSS-005`, the answer incorporates IPC Sections 24 and 25 referenced in the statutory Explanation to IT Act Section 66.
- Strict verbatim grounding validators might flag these answers as "unsupported" because the words do not appear in the primary excerpt.

#### C. What Remains Interpretive or Uncertain
- A balance exists between **zero-hallucination lexical grounding** (which limits answers strictly to the quoted passage) and **practical legal utility** (which requires explaining commencement dates, Gazette notifications, and statutory transitions).

#### D. What a Qualified Advocate Must Decide
1. Provide editorial guidelines establishing whether transitional notes should be formatted in distinct parenthetical remarks `(Note: ...)` or integrated into the substantive text.
2. Formulate threshold rules for prompt engineering in Phase 9 generation batches.

#### F. Records Requiring Revision if Interpretation Changes
- All 20 Pilot Records (`QA-PILOT-DPDP-001` through `QA-PILOT-CROSS-010`).

---

## 3. Summary of Source-Version Risks

| Risk Identifier | Statutory Instrument | Nature of Version Risk | Pipeline Mitigation |
| :--- | :--- | :--- | :--- |
| **VR-01** | DPDP Act, 2023 | 3-tier phased commencement creates temporal traps if questions lack a fixed `legal_as_of_date`. | All records enforce `legal_as_of_date = 2026-10-16` and check against G.S.R. 843(E) tiers. |
| **VR-02** | IT Act, 2000 | Pending omission of Section 43A creates future obsolescence. | Explicitly dated to 13 May 2027; regression tests prevent premature repeal claims. |
| **VR-03** | BNSS, 2023 | Section 531 savings conflation with CrPC repeal. | Anti-conflation model in `LegalQADocument` separates contemporary status from predecessor status. |
| **VR-04** | BSA, 2023 | Misattributing BSA commencement to S.O. 848(E) rather than S.O. 849(E). | Corrected in all registry records, manifests, and audit reports. |

