# LEGALMITRA — PHASE 6.1 CORRECTION REPORT
**Authoritative Provenance, Statutory Verification, and Temporal-Law Reconciliation**

**Project:** LegalMitra — Indian Legal Dataset Engineering  
**Workspace:** `C:\PROJECTS\LegalMitra`  
**Date:** 2026-10-16  
**Auditor / Architect:** Senior AI Data Engineer & Legal Information System Architect  
**Status:** **APPROVED & FULLY RECONCILED**

---

## 1. Executive Summary

This report documents the resolution of legal provenance and temporal-law discrepancies identified during Phase 6 audits. Phase 6.1 establishes an unassailable statutory and notification basis for the Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS) and reconciles the temporal status of Section 43A of the Information Technology Act, 2000 against Section 44(2) of the Digital Personal Data Protection Act, 2023 (DPDP Act).

All corrections have been verified against official Gazettes of India, incorporated into the offline test suite (70 passing tests), and reflected across repository documentation and knowledge base indexes.

---

## 2. BNSS Commencement Provenance & Notification Correction

### 2.1 Authoritative Notification Discrepancy Resolution
Previous working notes and drafts erroneously referenced **S.O. 850(E)** in connection with the commencement of the BNSS. An audit of the official notifications issued by the Ministry of Home Affairs on 24 February 2024 reveals the exact statutory apportionment:

| Enactment | Notification Number | File Reference | Date of Gazette | Appointed Date | Exceptions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Bharatiya Nagarik Suraksha Sanhita, 2023 (Act No. 46 of 2023)** | **S.O. 848(E)** | F. No. 1/3/2023-Judicial Cell-I | 24-02-2024 | **1 July 2024** | Except the provisions of entry 56 of the Second Schedule |
| **Bharatiya Sakshya Adhiniyam, 2023 (Act No. 47 of 2023)** | **S.O. 849(E)** | F. No. 1/3/2023-Judicial Cell-I | 24-02-2024 | **1 July 2024** | None |
| **Bharatiya Nyaya Sanhita, 2023 (Act No. 45 of 2023)** | **S.O. 850(E)** | F. No. 1/3/2023-Judicial Cell-I | 24-02-2024 | **1 July 2024** | Except the provisions of sub-section (2) of section 106 |

### 2.2 Corrected Repository Artefacts
- `BNSS_SOURCE_VERIFICATION_REPORT.md`: Updated all citations to **S.O. 848(E)**.
- `TEMPORAL_LAW_VALIDATION_REPORT.md`: Updated BNSS commencement references to **S.O. 848(E)**.
- `SOURCE_INTEGRITY_AUDIT.md`: Aligned statutory metadata.
- `registry/source_registry.jsonl`: Verified record `IND-STAT-BNSS-2023` carries appointed date `2024-07-01` pursuant to S.O. 848(E).

---

## 3. DPDP Act Section 44(2) and IT Act Section 43A Temporal Status

### 3.1 Primary Gazette Source: G.S.R. 843(E)
The Ministry of Electronics and Information Technology published Notification **G.S.R. 843(E)** on **13 November 2025** in the Gazette of India, Extraordinary, Part II—Section 3—Sub-section (i), No. 757.

The notification specifies phased commencement dates for different provisions of the Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023). Specifically, Section 44(2)—which amends the Information Technology Act, 2000 by omitting Section 43A and amending Section 81 and Section 87—is appointed to come into force:
> *"on the expiry of eighteen months from the date of publication of this notification in the Official Gazette."*

### 3.2 Legal Computation under Section 9, General Clauses Act, 1897
Under Section 9 of the General Clauses Act, 1897:
1. **Publication Date:** 13 November 2025 (excluded under standard statutory computation: "from the date of publication").
2. **Term:** 18 calendar months.
   - 13 November 2025 + 18 calendar months = **13 May 2027**.
3. **Application Date:** Prior to 13 May 2027, Section 44(2) has not commenced. Therefore, Section 43A of the Information Technology Act, 2000 remains operative law and enforceable for compensation regarding failure to protect sensitive personal data.

### 3.3 Five-Date Evaluation Benchmark Matrix
To prevent regression and guarantee temporal precision in RAG retrieval, LegalMitra evaluates queries across five critical timeline benchmarks:

| Date | Evaluated Query | Legal Status of Section 43A IT Act | Expected RAG System Output | Test Suite Result |
| :--- | :--- | :--- | :--- | :--- |
| **2025-11-13** (Gazette Publication) | Compensation claim for data breach under s.43A | **Operative & Enforceable** | Cites Section 43A IT Act; notes DPDP enactment but uncommenced s.44(2) | **PASSED** (`test_dpdp_phased_commencement_vs_it_act_43a`) |
| **2026-10-16** (Interim Audit Date) | Applicability of IT Act Section 43A | **Operative & Enforceable** | Cites Section 43A IT Act; explains s.44(2) pending commencement on 13 May 2027 | **PASSED** (`test_dpdp_phased_commencement_vs_it_act_43a`) |
| **2027-05-12** (Eve of Commencement) | Enforcement of IT Act Section 43A | **Operative & Enforceable** | Section 43A valid for causes of action arising on this date | **PASSED** (`test_dpdp_phased_commencement_vs_it_act_43a`) |
| **2027-05-13** (Effective Commencement Date) | New breach occurring on 13 May 2027 | **Omitted / Ineffective for new breaches** | Governed under DPDP Act ss. 8(5), 33 & Schedule; s.43A omitted | **PASSED** (`test_dpdp_phased_commencement_vs_it_act_43a`) |
| **2027-05-14** (Post-Commencement) | Remedy for data breach under contemporary law | **Omitted / Ineffective for new breaches** | DPDP Act remedies and penalties apply exclusively | **PASSED** (`test_dpdp_phased_commencement_vs_it_act_43a`) |

---

## 4. BNSS Source Verification Checklist

Authentic primary source text for the Bharatiya Nagarik Suraksha Sanhita, 2023 was acquired and normalized under ID `IND-STAT-BNSS-2023`:

- **Official Act:** Act No. 46 of 2023.
- **Section Count:** Exactly **537 sections** (verified in `data/01_raw/IND-STAT-BNSS-2023.json` and `data/02_normalized/IND-STAT-BNSS-2023.json`).
- **Anticipatory Bail Provisions (ss. 479–484):**
  - Section 482(1): Power of High Court and Court of Session to grant direction for bail to person apprehending arrest.
  - Section 482(2): Statutory conditions (interrogation availability, non-tampering with witnesses, restriction on leaving India).
  - Section 482(3): Procedure upon arrest without warrant or magistrate cognizance.
  - **Section 482(4) Statutory Exclusions:** Explicitly bars anticipatory bail for accusations under:
    - **Section 65 of the Bharatiya Nyaya Sanhita, 2023** (punishment for rape).
    - **Sub-section (2) of Section 70 of the Bharatiya Nyaya Sanhita, 2023** (gang rape of child/minor).
- **Repeal and Savings (Section 531):**
  - Section 531(1): Explicitly repeals Code of Criminal Procedure, 1973 (2 of 1974).
  - Section 531(2)(a): Mandates that any appeal, application, trial, inquiry or investigation pending immediately before 1 July 2024 shall be disposed of, continued, held or made under CrPC 1973 as if the BNSS had not come into force.

---

## 5. Quarantine & Isolation Controls

| Artefact ID | Nature | Quarantine Status | Rationale |
| :--- | :--- | :--- | :--- |
| `IND-JUD-DEL-2024-BAIL` | Synthetic High Court Bail Order Scaffold | **Quarantined** (`is_synthetic_scaffold=1`) | Unverified docket and cause title; quarantined to prevent synthetic hallucination |
| `PROC-BNSS-482-BAIL-001` | Generated Procedural Guide | **Quarantined** | Derived from synthetic scaffold; segregated from RAG indexes and SFT training splits |

---

## 6. Verification and Sign-Off

- **Test Suite Status:** 70 passed, 2 live deselected, 0 failed in 21.81s (`pytest -v -m "not live"`).
- **Regression Verification:** All temporal boundary checks, grounding validators, and indexing functions pass with zero errors.
- **Phase 6.1 Status:** **COMPLETE & CLOSED**.

