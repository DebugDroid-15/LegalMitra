# LEGALMITRA PHASE 26: ADVOCATE REVIEW PILOT PROTOCOL

**Classification:** Proprietary & Confidential — Team Shatrujeet  
**Phase:** 26 — Human Legal Review Operations, Structured Statutory Modeling & High Court Precedent Expansion  
**Date:** October 2026  
**Operational Status:** PREPARED & READY (AWAITING LICENSED HUMAN ADVOCATE PARTICIPATION)  

---

## 1. Protocol Purpose & Scope

This protocol establishes the standardized instructions, evaluation rubrics, conflict of interest safeguards, and procedural guidelines for licensed advocates conducting human legal evaluation on LegalMitra candidate Q&A examples.

To maintain professional and ethical standards, **no fictitious advocate reviews are simulated or fabricated**. The 40 candidate records remain strictly in `pending_legal_review` status until physical or cryptographic digital sign-off by practicing advocates enrolled with a State Bar Council.

---

## 2. Reviewer Instructions & Evaluation Rubric

Each empanelled advocate reviewer is provided with:
1. The candidate question, generated answer, and source citations.
2. The primary legal source bundle containing official Gazette text, India Code sections, or reported judicial rulings.
3. The bitemporal applicability anchor (e.g. pre-July 2024 vs post-July 2024).

### Scoring Matrix (1.0 to 5.0)

| Score Range | Legal Assessment Criteria | Action Required |
| :--- | :--- | :--- |
| **5.0 (Flawless)** | Complete statutory accuracy, precise section/sub-section pinpoints, exact judicial precedent citations, correct temporal applicability, and appropriate cautionary disclaimers. | Mark `APPROVED`. |
| **4.0 (Substantially Correct)** | Accurate on the substantive legal proposition, minor stylistic variation, citations resolve correctly. | Mark `APPROVED` with optional commentary. |
| **3.0 (Partially Deficient)** | Missing a material qualification, proviso, or subsequent amendment; core answer is technically accurate but requires nuance. | Mark `NEEDS_REVISION` with required amendments. |
| **2.0 (Material Error)** | Conflates predecessor and successor statutes (e.g., retroactively applying BNS 103 to pre-July 2024 murder), cites an overruled precedent, or omits a crucial statutory bar. | Mark `REJECTED` with specific statutory/judicial citations. |
| **1.0 (Critical Failure)** | Severe legal hallucination, invented statutory section, non-existent case citation, or disclosure of protected victim identity. | Mark `REJECTED` with critical alert. |

---

## 3. Disqualification & Conflict of Interest Rules

A reviewing advocate must mark a matter as `ABSTAINED` under the following circumstances:
1. **Prior Representation**: The advocate or their law firm represented any party in the litigation referenced in the question.
2. **Specialized Conflict**: The matter involves proprietary client matters or ongoing sub-judice litigation.
3. **Unsettled Jurisprudence**: The legal question involves an active conflicting reference before a larger bench of the Supreme Court where no authoritative consensus exists.

---

## 4. Current Pilot Package State

- **Package A**: 20 Pilot Examples (`data/07_batches/review/pilot_20_review_sheet.csv`) -> Status: 20/20 `pending_legal_review`.
- **Package B**: 20 Candidate Records (`data/07_batches/review/batch_01_review_sheet.csv`) -> Status: 20/20 `pending_legal_review`.
- **Readiness**: Dry-run verification script and schema validation are active and tested. Operational pilot is **ready for advocate onboarding**.
