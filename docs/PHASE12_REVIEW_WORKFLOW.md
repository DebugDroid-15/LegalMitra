# LEGALMITRA PHASE 12: ADVOCATE REVIEW WORKFLOW SPECIFICATION

**Date:** 2026-10-16  
**Module:** `legalmitra.review.import_review`  
**Schema Definition:** `legalmitra.schemas.legal_qa.LegalQADocument`  
**Status:** **ACTIVE, EXTENDED & AUDITED**  

---

## 1. Data Model & Field Standards

Every reviewable example in LegalMitra follows the `LegalQADocument` schema with complete provenance, citation mapping, and explicit human review demarcation:

| Attribute | Schema Field | Type | Description |
|:---|:---|:---|:---|
| **Identifier** | `qa_id` | `str` | Stable unique record ID (e.g. `QA-PILOT-DPDP-001`) |
| **Question** | `question` | `str` | Substantive legal query |
| **Proposed Answer** | `answer` | `str` | Source-grounded candidate response |
| **Supporting Sources** | `supporting_source_ids` | `List[str]` | Traceable source record IDs in `source_registry.jsonl` |
| **Verbatim Evidence** | `evidence_passages` | `List[EvidencePassage]` | Exact statutory sections or judgment paragraphs |
| **Citations** | `statutory_citations` | `List[str]` | Formal citation strings |
| **Legal As-Of Date** | `legal_as_of_date` | `date` | Point-in-time statutory evaluation date |
| **Commencement Source** | `commencement_source_id` | `str` | Official Gazette notification reference (e.g. S.O. 848(E)) |
| **Commencement Date** | `commencement_date` | `date` | Statutory effective date under notification |
| **Temporal Status** | `law_status_label` | `LawStatusLabel` | `in_force`, `enacted_not_yet_in_force`, `repealed_with_savings` |
| **Validation Status** | `temporal_validation_status` | `TemporalValidationStatus` | Automated temporal validity check |
| **Review Status** | `legal_review_status` | `LegalReviewStatus` | Explicit human advocate review status |
| **Reviewer Comments** | `reviewer_comments` | `Optional[str]` | Substantive corrections, ratio analysis, reasoning |
| **Reviewer Initials** | `reviewer_name_initials` | `Optional[str]` | Enrolled advocate identifier |
| **Review Date** | `review_date` | `Optional[date]` | Date review was completed |

---

## 2. Review Decision Enums & State Mapping

The system supports strict advocate decision values in review sheets:

| Review Sheet Decision | Target `LegalReviewStatus` | Semantic Meaning | Export Eligibility |
|:---|:---|:---|:---|
| *(Blank / Empty)* | `pending_legal_review` | Unreviewed candidate; never inferred as approved | **Ineligible** (Excluded) |
| `APPROVED` | `legal_expert_approved` | Formally approved by qualified Indian advocate | **Eligible** for fine-tuning |
| `REVISION_REQUIRED` | `revision_required` | Substantively sound but requires wording/citation revision | **Ineligible** (Requires edit) |
| `REJECTED` | `legal_expert_rejected` | Factually incorrect, conflated, or unsupported | **Ineligible** (Quarantined) |
| `NEEDS_MORE_EVIDENCE` | `needs_more_evidence` | Statutory provision alone cannot answer factual scenario | **Ineligible** (Needs sources) |
| `DEFERRED` | `deferred` | Unresolved legal ambiguity (e.g. pending before SC bench) | **Ineligible** (Frozen) |

---

## 3. Atomic Safety & Anti-Tampering Rules

1. **Atomic Pre-Validation**: The entire review CSV is validated upfront. If a single row contains an unknown `record_id`, malformed score, missing comment on rejection, or invalid enum, the entire import aborts with a `ReviewImportError` without touching any dataset.
2. **Mandatory Reviewer Comments**: Rejections and revisions require substantive justification in `reviewer_comments`.
3. **Immutable Audit Ledger**: Every import operation generates a timestamped audit log in `data/06_review/audit/review_audit_log_YYYYMMDD_HHMMSS.jsonl` recording previous status, new status, reviewer initials, scores, and an exact snapshot of the pre-import record.
4. **Frozen Pilot Protection**: The review importer operates on targeted dataset files. The frozen pilot in `data/03_generated/` is strictly guarded by `scripts/verify_freeze.py` and cannot be modified without failing the cryptographic SHA-256 manifest check.

