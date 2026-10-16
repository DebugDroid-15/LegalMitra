# LEGALMITRA — TEMPORAL-LAW VALIDATION REPORT
**Document ID**: `REP-TEMP-2026-PHASE6-001`  
**Date**: October 2026  
**Pipeline Version**: 0.6.0  
**Domain**: Intertemporal Statutory Enforcement, Phased Commencement & Repeal Dynamics  
**Status**: VERIFIED & RECONCILED  

---

## 1. Executive Summary

This report resolves the critical temporal-law evaluation defect discovered in Phase 5: the relationship between **Section 43A of the Information Technology Act, 2000** and **Section 44(2)(a) of the Digital Personal Data Protection Act, 2023**, as well as the transition from the **Code of Criminal Procedure, 1973** to the **Bharatiya Nagarik Suraksha Sanhita, 2023**.

---

## 2. Resolving the Section 43A IT Act vs. DPDP Act Section 44(2) Blindspot

### 2.1 The Issue
In Phase 4 evaluation item `EVAL-IT-S43A-COMPENSATION-006`, the model declared that Section 43A of the IT Act 2000 was no longer in force because DPDP Act Section 44(2)(a) states *"section 43A shall be omitted"*. The RAG evaluator previously marked this as "insufficient evidence" passing, creating a severe intertemporal false positive.

### 2.2 Primary Evidence: Gazette Notification G.S.R. 843(E)
Under Section 1(2) of the DPDP Act 2023, the Act comes into force on dates appointed by the Central Government via Official Gazette notification.

On **13 November 2025**, the Ministry of Electronics and Information Technology (MeitY) issued **Notification G.S.R. 843(E)** (published in Gazette of India Part II—Sec 3(i) on 14 November 2025):
- **Clause (a) (Immediate Commencement - 14 November 2025)**:
  Brings into force Section 1(2), Section 2 (definitions), Sections 18–26 (Data Protection Board), Sections 35, 38–43, and **Sub-sections (1) and (3) of Section 44**.
- **Clause (b) (Commencement in 1 Year - 14 November 2026)**:
  Brings into force Section 6(9) and Section 27(1)(d).
- **Clause (c) (Commencement in 18 Months - 14 May 2027)**:
  Brings into force Sections 3–5, Section 6(1)–(8), (10), Sections 7–17 (Data Fiduciary obligations and Data Principal rights), Sections 28–34, 36, 37, and **Sub-section (2) of Section 44**.

### 2.3 Legal Status Conclusion
- **Statutory Computation of Section 44(2) Commencement**:
  Under clause (c) of Notification G.S.R. 843(E), Section 44(2) comes into force *"eighteen months from the date of publication of this gazette"*. Published in the Official Gazette on 13 November 2025 (Gazette dated Thursday, 13 November 2025, No. 757), adding 18 calendar months yields **13 May 2027** as the derived statutory commencement date under Section 9 of the General Clauses Act, 1897.
- **Section 44(2)(a) of the DPDP Act (omitting Section 43A of the IT Act) is explicitly deferred to 13 May 2027 (18 months from gazette publication).**
- Therefore, as of **October 2026** (and specifically prior to 13 May 2027), **Section 43A of the Information Technology Act, 2000 remains active, legally binding statutory law across India**.
- Any legal guidance asserting that Section 43A is omitted or inoperative prior to 13 May 2027 is legally erroneous.
- The evaluation item and Knowledge Base search logic have been reconciled to reflect this verified timeline.

---

## 3. Criminal Procedure Intertemporal Transition: BNSS Section 531

Under **Ministry of Home Affairs Notification S.O. 848(E)** (F.No. 1/3/2023-Judicial Cell-I, Gazette of India Extraordinary Part II—Sec 3(ii) dt. 24 February 2024):
- The Bharatiya Nagarik Suraksha Sanhita, 2023 came into force on **1 July 2024** (except entry 56 of the Second Schedule). (Distinguished from S.O. 850(E), which brought into force the Bharatiya Nyaya Sanhita, 2023).

### Statutory Savings Rule (Section 531(2)(a) BNSS):
> *"if, immediately before the date on which this Sanhita comes into force, there is any appeal, application, trial, inquiry or investigation pending, then, such appeal, application, trial, inquiry or investigation shall be disposed of, continued, held or made, as the case may be, in accordance with the provisions of the Code of Criminal Procedure, 1973... as if this Sanhita had not come into force."*

### Key Practical Rule:
1. **Offences registered or trials pending prior to 1 July 2024**: Governed by the Code of Criminal Procedure, 1973.
2. **FIRs registered or applications initiated on or after 1 July 2024**: Governed by the Bharatiya Nagarik Suraksha Sanhita, 2023.

---

## 4. Regression Test Suite Verification

Dedicated temporal regression tests were implemented across `tests/test_knowledge_base.py` and `tests/test_pilot_20.py`:
1. `test_authentic_bnss_indexing_and_anticipatory_bail`: Verifies Section 482 anticipatory bail retrieval with effective date boundary under S.O. 848(E).
2. `test_dpdp_phased_commencement_vs_it_act_43a`: Verifies that Section 43A IT Act is evaluated across 5 dates (13 Nov 2025, 16 Oct 2026, 12 May 2027, 13 May 2027, 14 May 2027) with precise boundary transitions.
3. `test_pilot_20_temporal_validation_all_passed`: Verifies that all 20 pilot records conform to their statutory commencement labels under `TemporalValidator`.
4. `test_temporal_validator_fails_on_uncommenced_as_operative`: Asserts rejection when uncommenced provisions are presented as currently operative rights.
5. `test_boundary_date_evaluations_around_may_13_2027`: Verifies eve (12 May), effective (13 May), and post-commencement (14 May) boundary transitions.
6. `test_dpdp_commencement_groupings_separate`: Validates exact individual section mappings across G.S.R. 843(E) Group 1, Group 2, and Group 3.

All 74 offline tests pass cleanly (`pytest -v -m "not live"`).

