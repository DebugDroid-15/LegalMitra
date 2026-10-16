# LegalMitra — Advocate Review & Verification Schedule
**Document ID**: `REV-SCHED-2026-PHASE4-001`  
**Date**: October 2026  
**Status**: PENDING HUMAN ADVOCATE ACTION  

---

## 1. Statutory Mandate for Legal Review

Under Indian legal information standards and data governance principles, automated algorithmic verification (including Pydantic schema validation, SHA-256 cryptographic matching, and string-distance metrics) establishes **syntactic and data-engineering integrity only**.

> [!CAUTION]
> **No record in LegalMitra may be graduated to `data/04_verified/` or ingested into downstream Supervised Fine-Tuning (SFT) training sets without certification by an advocate enrolled under the Advocates Act, 1961.**

---

## 2. Priority 1 (CRITICAL): Flawed and Synthetic Scaffolds

The following records contain known jurisprudential contradictions or hallucinations and must be quarantined:

| Item Identifier | Record Location | Source Basis | Issue / Legal Defect | Required Advocate Action |
| :--- | :--- | :--- | :--- | :--- |
| `IND-JUD-DEL-2024-BAIL` | `data/01_raw/IND-JUD-DEL-2024-BAIL.txt`<br>`registry/source_registry.jsonl` | Purported Delhi High Court Decision | **Fatal Legal Impossibility**: State of NCT of Delhi named as Petitioner seeking anticipatory bail under BNSS s.482. In Indian criminal law, the State never petitions for anticipatory bail. | Formally certify as **SYNTHETIC TEST SCAFFOLD**. Maintain `verification_status: flagged_unsupported`. Ensure excluded from training corpora. |
| `DRAFT-BSA-63-APPLICATION-001` | `data/03_generated/drafting_examples.jsonl` | `IND-STAT-BSA-2023-SEC63` | **Statutory Title Hallucination**: Model fabricated title *"Information Technology (Adoption of Indian Standards for Electronic Records) Adhiniyam, 2023"*. | Redraft title to *Bharatiya Sakshya Adhiniyam, 2023*. Verify certificate clauses under Section 63(4). Update status to `FLAGGED_UNSUPPORTED` pending correction. |
| `PROC-BNSS-482-BAIL-001` | `data/03_generated/procedural_guide.jsonl` | `IND-JUD-DEL-2024-BAIL` | **Contaminated Provenance**: Procedural guide grounded on synthetic bail decision `IND-JUD-DEL-2024-BAIL`. | Review steps against actual text of Section 482 BNSS and Delhi High Court Rules. Replace evidence passages with authentic reported precedent (e.g. *Gurbaksh Singh Sibbia v. State of Punjab*). |

---

## 3. Priority 2 (HIGH): Temporal & Phased Commencement Verification

Indian legislation frequently separates enactment (Presidential assent) from commencement (Official Gazette notifications):

| Document ID | Legislation Title | Enactment Date | Documented Effective Date | Required Advocate Action |
| :--- | :--- | :--- | :--- | :--- |
| `IND-STAT-DPDP-2023` | Digital Personal Data Protection Act, 2023 | 2023-08-11 | Phased (Section 1(2)) | Audit current Gazette notifications to determine which sections (e.g., Data Protection Board establishment) have formally commenced. |
| `IND-STAT-IT-2000` | Information Technology Act, 2000 (Section 43A) | 2000-06-09 | 2000-10-17 | Verify whether Section 44(2) of the DPDP Act 2023 has been notified to repeal Section 43A and Section 87(2)(ob). |
| `IND-STAT-BSA-2023-SEC61`<br>`IND-STAT-BSA-2023-SEC63` | Bharatiya Sakshya Adhiniyam, 2023 | 2023-12-25 | 2024-07-01 | Confirm MHA Notification S.O. 848(E) applicability to pending trials vs new trials initiated on or after 1 July 2024. |

---

## 4. Priority 3 (MEDIUM): Extraction Failure Remediation

| Document ID | Document Title | Page Count | Failure Root Cause | Remediation Requirement |
| :--- | :--- | :--- | :--- | :--- |
| `IND-GUIDE-SCI-PROC-2025` | Supreme Court Handbook on Practice and Procedure | 278 pages | Exceeded Docling default 15-page limit | Advocate must identify target chapters (e.g., Special Leave Petitions, Bail Motions) for segmented chunk extraction. |

---

## 5. Priority 4: Generated Dataset Batch Review (27 Records)

All 27 records generated during Phase 3 remain in `unverified_automated` status:

- **11 Statutory Q&A Records** (`data/03_generated/legal_qa.jsonl`): Review accuracy of statutory interpretations regarding electronic records and POCSO penalties.
- **10 Case Reasoning Records** (`data/03_generated/legal_qa.jsonl`): Review *Puttaswamy* Article 21 fundamental right holdings.
- **3 Procedural Guidance Records** (`data/03_generated/procedural_guide.jsonl`): Verify court motion rules, limitation periods, and mandatory affidavits.
- **2 Judgment Analysis Records** (`data/03_generated/case_analysis.jsonl`): Verify ratio decidendi formulations.
- **1 Legal Drafting Record** (`data/03_generated/drafting_examples.jsonl`): Requires complete correction of statutory title hallucination.

---

## 6. Advocate Review Workflow Protocol

1. **Reviewer Qualifications**: Advocate enrolled with a State Bar Council under the Advocates Act, 1961 with minimum 3 years practice before High Courts or Supreme Court of India.
2. **Review Checklist**:
   - [ ] Is the cited statute currently in force?
   - [ ] Is the provision number and subsection accurate?
   - [ ] Does the holding represent binding precedent under Article 141 or persuasive precedent?
   - [ ] Are limitation periods and court jurisdiction accurate?
   - [ ] Are party names redacted in compliance with POCSO s.33(7) / JJ Act s.74?
3. **Status Graduation**:
   - If approved: Update `legal_review_status = "legal_expert_approved"` and move record to `data/04_verified/`.
   - If rejected: Update `legal_review_status = "legal_expert_rejected"` with explicit rejection rationale.

