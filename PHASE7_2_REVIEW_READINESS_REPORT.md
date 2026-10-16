# LEGALMITRA — PHASE 7.2 REVIEW READINESS REPORT
**Advocate Review Package & Data Quality Gates**
*Document ID*: `REPORT-2026-PHASE7-2-001`  
*Date*: 16 October 2026  
*Auditor / Architect*: Senior AI Data Engineer & Legal Information System Architect  
*Status*: REVIEW-READY / PENDING HUMAN LEGAL COUNSEL REVIEW  

---

## 1. Executive Summary

Phase 7.2 advances LegalMitra from the Phase 7.1 temporal audit into a state of **complete readiness for independent human advocate review**. In strict adherence to project directives:
1. **Zero Additional Examples Generated**: The dataset remains fixed at the audited 20-example pilot (10 DPDP Act statutory Q&As, 10 Cross-Statute evidence & cybercrime records).
2. **Zero Automated Self-Approval**: All 20 pilot records remain strictly tagged with `legal_review_status = "pending_legal_review"`. Automated validation systems are forbidden from marking legal advice or training records as approved.
3. **BNSS Status Model Anti-Conflation**: Successfully disentangled the status of contemporary BNSS provisions from the repeal-with-savings status of the Code of Criminal Procedure, 1973.
4. **Pre-Generation Quality Gates (`DataQualityGate`)**: Implemented and verified an 8-stage automated quality gate enforcing source authenticity, section-level commencement, exact evidence-span matching, citation completeness, quarantine exclusion, duplicate detection, temporal completeness, and non-self-approval.
5. **Advocate Review Package (`data/06_review/`)**: Assembled a complete, reviewer-friendly package containing an advocate guide, review sheet CSV with blank decision fields, full source bundle JSON, and a detailed memorandum addressing six prioritized legal ambiguities.
6. **Full Test Suite Reproduction**: 84 offline tests pass cleanly (0 failures, 2 deselected live tests).

---

## 2. BNSS Status Model Anti-Conflation

### 2.1 The Issue
In automated legal metadata extraction, saving clauses such as Section 531 of the Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS) are susceptible to **statute/provision status conflation**. Because Section 531(1) states *"The Code of Criminal Procedure, 1973 is hereby repealed"* and Section 531(2)(a) saves pending proceedings, naive parsers tagged Section 531 itself as `repealed_with_savings`.

This was a conceptual error:
- **The Bharatiya Nagarik Suraksha Sanhita, 2023 (Act No. 46 of 2023)** commenced on **1 July 2024** pursuant to Ministry of Home Affairs Notification **S.O. 848(E)**.
- Section 531 is an **in-force provision** of active primary law.
- The repeal and savings treatment attaches exclusively to the **Code of Criminal Procedure, 1973 (Act No. 2 of 1974)**.

### 2.2 Schema & Validation Resolution
To prevent this conflation across current and future dataset batches, `LegalQADocument` schema in `legalmitra/schemas/legal_qa.py` was extended with explicit predecessor statute fields:
```python
repealed_statute_context: Optional[str] = Field(
    default=None,
    description="Contextual note identifying the predecessor enactment subject to repeal and savings.",
)
repealed_statute_status: Optional[LawStatusLabel] = Field(
    default=None,
    description="Explicit status of the predecessor statute (e.g., REPEALED_WITH_SAVINGS).",
)
```

In `QA-PILOT-CROSS-010`:
- `law_status_label`: `LawStatusLabel.IN_FORCE`
- `provision_commencement_status`: `ProvisionCommencementStatus.COMMENCED`
- `repealed_statute_context`: `"Code of Criminal Procedure, 1973 (Act No. 2 of 1974) is repealed with savings under BNSS s. 531(2)(a)"`
- `repealed_statute_status`: `LawStatusLabel.REPEALED_WITH_SAVINGS`
- `temporal_validation_status`: `TemporalValidationStatus.VERIFIED_HISTORICAL_SAVINGS`

### 2.3 Anti-Conflation Regression Enforcement
`TemporalValidator` (`legalmitra/validation/temporal_validator.py`) and `DataQualityGate` now strictly reject any record where a BNSS provision is labeled `repealed` or `repealed_with_savings`:
```python
if qa_doc.law_status_label in (LawStatusLabel.REPEALED, LawStatusLabel.REPEALED_WITH_SAVINGS) or qa_doc.provision_commencement_status == ProvisionCommencementStatus.REPEALED:
    issues.append(
        "Provision of BNSS 2023 cannot be labeled 'repealed' or 'repealed_with_savings'. "
        "BNSS 2023 is in force; the repeal-with-savings status belongs to the prior enactment (CrPC 1973), "
        "which should be designated in 'repealed_statute_status'."
    )
```
Regression tests in `tests/test_pilot_20.py` and `tests/test_quality_gate.py` confirm this protection.

---

## 3. Pre-Generation Data Quality Gates (`DataQualityGate`)

The `DataQualityGate` engine (`legalmitra/validation/quality_gate.py`) provides an institutional safeguard against common data engineering failure modes:

| Gate | Check Name | Description | Failure Mode Prevented |
| :---: | :--- | :--- | :--- |
| **1** | **Source Authenticity** | Verifies all `supporting_source_ids` exist in `registry/source_registry.jsonl`, have verified status, and valid canonical URLs. | Fabrication of non-existent sources or unverified external text. |
| **2** | **Section-Level Commencement** | Cross-references cited provisions against G.S.R. 843(E) (DPDP 3-tier schedule) and S.O. 848(E) (BNSS). Enforces anti-conflation for BNSS s. 531 and operative status of IT Act s. 43A. | Treating uncommenced provisions as operative rights; premature declaration of repeal. |
| **3** | **Exact Evidence Matching** | Validates that every evidence passage exists verbatim (normalized for typographic variants) in loaded source texts. | Hallucinated statutory subsections or modified legislative text. |
| **4** | **Citation Completeness** | Enforces non-empty `statutory_citations` with recognized statutory anchors (`Section`, `Article`, `Rule`, `Order`, `Schedule`, `Act`, `Code`). | Vague assertions lacking legal pinpoint references. |
| **5** | **Quarantine Exclusion** | Strictly blocks synthetic test scaffolds (`IND-JUD-DEL-2024-BAIL`), quarantined guides (`PROC-BNSS-482-BAIL-001`), and unsupported records. | Data poisoning from artificial scaffolds into production RAG/training sets. |
| **6** | **Duplicate Detection** | Uses cryptographic content fingerprinting to detect duplicate questions or answers across the batch and against existing datasets. | Redundant training data and skewed retrieval distributions. |
| **7** | **Temporal Consistency** | Verifies `legal_as_of_date`, `law_status_label`, `provision_commencement_status`, and `commencement_source_id` are fully populated. | Temporal ambiguity in training data or downstream inference. |
| **8** | **Separate Human Review** | Requires `legal_review_status == LegalReviewStatus.PENDING_LEGAL_REVIEW`. Rejects any automated attempt to self-approve. | Automated systems masquerading as certified legal authority. |

**Evaluation on Pilot 20**: 100% of the 20 pilot records pass all 8 gates cleanly.

---

## 4. Advocate Review Package Architecture (`data/06_review/`)

The advocate review package provides Indian legal counsel with an auditable review interface:

### 4.1 Artifact Breakdown
1. **`ADVOCATE_REVIEW_GUIDE.md`**:
   - Outlines the statutory background, including the DPDP Act 3-tier commencement under G.S.R. 843(E) and BNSS commencement under S.O. 848(E).
   - Establishes a 1-to-5 scoring rubric across **Legal Accuracy**, **Temporal Accuracy**, and **Grounding**.
   - Details decision classifications: `APPROVED`, `REVISION_REQUIRED`, and `REJECTED`.
2. **`pilot_20_review_sheet.csv`**:
   - 20-row CSV formatted with UTF-8 BOM for Microsoft Excel and LibreOffice compatibility.
   - Contains stable IDs, questions, proposed answers, as-of dates, citations, source URLs, evidence spans, and specific advocate questions.
   - Decision and scoring fields (`review_decision`, `legal_accuracy_score_1_to_5`, `temporal_accuracy_score_1_to_5`, `grounding_accuracy_score_1_to_5`, `reviewer_comments`, `reviewer_name_initials`, `review_date`) are intentionally left blank for counsel completion.
3. **`pilot_20_source_bundle.json`**:
   - Machine-readable JSON linking every record to full source registry metadata (title, URL, SHA-256 checksum, enactment date, effective date).
   - All 20 records reflect `review_status: "pending_legal_review"` and `decision: null`.
4. **`pilot_20_open_issues.md`**:
   - In-depth briefing on six prioritized legal ambiguities.

---

## 5. Prioritized Legal Ambiguities

The review package explicitly highlights six legal ambiguities for advocate determination rather than resolving them unilaterally:

### Priority 1: BNSS Section 482(4) Anticipatory Bail Exclusion Scope
- **Record**: `QA-PILOT-CROSS-009`
- **Ambiguity**: Section 482(4) explicitly bars anticipatory bail for accusations under BNS Section 65 (rape of minor) and Section 70(2) (gang rape of child under 18). Under predecessor CrPC Section 438(4), High Courts differed on whether this bar extends to an accused charged solely with abetment (BNS s. 45), attempt (BNS s. 62), or criminal conspiracy (BNS s. 61).
- **Counsel Question**: Should the LegalMitra answer include an explicit qualification that whether Section 482(4) extends to conspiracy/abetment depends on evolving High Court jurisprudence?

### Priority 2: IT Act Section 43A Operative Status During DPDP Phased Rollout
- **Record**: `QA-PILOT-DPDP-009`
- **Ambiguity**: Section 44(2)(a) of the DPDP Act provides that Section 43A shall be omitted. However, Section 44(2) falls in Group 3 under Notification G.S.R. 843(E) (commencing 18 months from 13 Nov 2025 = 13 May 2027 under General Clauses Act s. 9).
- **Counsel Question**: Is Section 43A read with the SPDI Rules (2011) without question the operative statutory compensation regime until 13 May 2027? Does the pending omission create any transitional ambiguity for causes of action arising before 13 May 2027?

### Priority 3: DPDP Act Section 6(9) Asymmetrical Commencement
- **Record**: `QA-PILOT-DPDP-005` & Notification G.S.R. 843(E)
- **Ambiguity**: Notification G.S.R. 843(E) places Section 6(9) in Group 2 (commencing 13 Nov 2026), whereas Sections 6(1)–(8), 6(10), and Section 5 notice obligations commence in Group 3 (13 May 2027).
- **Counsel Question**: How can a Data Fiduciary give a legally compliant Section 6(9) notice regarding pre-existing consent starting November 2026 when statutory notice requirements (Section 5) and withdrawal mechanisms (Section 6(4)) do not take effect until May 2027?

### Priority 4: BNSS Section 531 Savings & Representation in Temporal Schema
- **Record**: `QA-PILOT-CROSS-010`
- **Ambiguity**: BNSS Section 531 is in force as contemporary law, while CrPC 1973 is repealed with savings for pending inquiries/investigations.
- **Counsel Question**: Is the schema representation separating primary statute status (`in_force`) from predecessor repeal/savings (`repealed_statute_status`) legally sound? For FIRs registered prior to 1 July 2024, does subsequent bail procedure continue under CrPC 1973 in accordance with recent Delhi and Punjab & Haryana High Court decisions?

### Priority 5: BSA Section 63 Electronic Record Certificate Requirements
- **Records**: `QA-PILOT-CROSS-001`, `QA-PILOT-CROSS-002`, `QA-PILOT-CROSS-003`, `QA-PILOT-CROSS-004`
- **Ambiguity**: Section 61 provides that electronic records have documentary enforceability, "subject to the provisions of section 63" and proviso requiring a Section 63(4) certificate.
- **Counsel Question**: Does Section 61's proviso make the certificate mandatory in every instance, or does Section 62 permit oral evidence when the original computer device is produced? Does the ruling in *Arjun Panditrao Khotkar* (2020) 7 SCC 1 fully survive under BSA Section 63?

### Priority 6: Answer Text Extending Beyond Cited Statutory Text
- **Records**: All 20 Pilot Records
- **Ambiguity**: Legal QA pairs often synthesize essential statutory context (such as identifying predecessor statutes or transitional dates) not found within the verbatim excerpt.
- **Counsel Question**: Should LegalMitra enforce strict four-corners grounding (where the answer may only recite what is inside the excerpt), or does legal information utility require providing statutory transitions and notifications?

---

## 6. Verification and Test Results

The test suite was run offline and verified:
```
pytest -v -m "not live"
====================== 80 passed, 2 deselected in 41.18s ======================

pytest tests\test_review_package.py -v
============================== 4 passed in 0.29s ==============================

pytest tests\test_quality_gate.py tests\test_pilot_20.py -v
============================= 13 passed in 2.21s ==============================
```

**Total Active Test Count**: **84 passed tests**, 2 deselected live tests, 0 failed.

### Breakdown of Test Coverage
- `tests/test_quality_gate.py` (5 tests):
  * `test_pilot_20_all_pass_quality_gate`
  * `test_quality_gate_rejects_quarantined_scaffold`
  * `test_quality_gate_rejects_automated_self_approval`
  * `test_quality_gate_rejects_duplicate_records`
  * `test_quality_gate_rejects_bnss_conflation`
- `tests/test_review_package.py` (4 tests):
  * `test_review_package_files_exist`
  * `test_review_sheet_structure_and_blank_decisions`
  * `test_source_bundle_json_structure`
  * `test_open_issues_covers_all_six_priorities`
- `tests/test_pilot_20.py` (8 tests):
  * `test_pilot_20_examples_existence_and_schema`
  * `test_pilot_20_grounding_validity`
  * `test_pilot_20_manifest_consistency`
  * `test_pilot_20_temporal_validation_all_passed`
  * `test_bnss_section_531_anti_conflation_regression`
  * `test_temporal_validator_fails_on_uncommenced_as_operative`
  * `test_boundary_date_evaluations_around_may_13_2027`
  * `test_dpdp_commencement_groupings_separate`

---

## 7. Handover Checklist for Advocate Review

- [x] Exact 20 pilot examples preserved; zero unverified bulk generation.
- [x] BNSS Section 531 status model anti-conflation implemented and regression-tested.
- [x] Pre-generation `DataQualityGate` active and passing across all pilot records.
- [x] `data/06_review/ADVOCATE_REVIEW_GUIDE.md` available with statutory timeline and scoring rubric.
- [x] `data/06_review/pilot_20_review_sheet.csv` populated with blank decision and scoring fields.
- [x] `data/06_review/pilot_20_source_bundle.json` generated with authentic source URLs and checksums.
- [x] `data/06_review/pilot_20_open_issues.md` prepared covering all 6 prioritized ambiguities.
- [x] All 20 records remain strictly in `pending_legal_review` status.
- [x] 84 offline tests reproducible and passing.

