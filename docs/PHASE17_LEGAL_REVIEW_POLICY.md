# LEGALMITRA — PHASE 17G: ADVOCATE REVIEW POLICY FOR JUDICIAL PROPOSITIONS

**Workspace:** `c:\PROJECTS\LegalMitra`  
**Execution Date:** 2026-10-17  
**Status:** COMPLETE & VERIFIED  

---

## 1. Executive Summary

A core safeguard of LegalMitra is that **automated information extraction does not equal legal correctness**.

Machine models can readily extract sentences from court judgments; however, determining whether a judicial passage constitutes:
- The true **ratio decidendi** (binding legal rule necessary to the disposition),
- Mere **obiter dicta** (incidental observations having only persuasive value),
- A party's rejected submission quoted by the judge, or
- A legal proposition displaced by a later larger bench,
requires genuine professional legal review by licensed advocates.

---

## 2. Review Lifecycle for Case-Law Propositions

Every judgment proposition and extracted holding progresses through a strict, auditable lifecycle:

```
[Unverified Automated Extraction]
            │
            ▼
[Pending Legal Review]  <── (Initial Candidate State)
            │
    ┌───────┴───────────────────────────┐
    ▼                                   ▼
[Legal Expert Approved]         [Legal Expert Rejected]
(Requires Bar Council ID,       (Requires substantive reasoning
 reviewer signature, and         in advocate review sheet)
 confidence >= 4/5)
```

### Review Schema Fields:
1. `candidate_id`: Unique proposition ID (e.g. `PROP-ARJUN-001`).
2. `source_judgment_id`: Linked judgment (e.g. `IND-JUD-SC-2020-ARJUN-KHOTKAR`).
3. `extracted_proposition`: Text of the extracted legal proposition.
4. `supporting_passage_ref`: Exact paragraph or ratio reference (`Paragraph 51`).
5. `applicable_statutory_provisions`: Associated sections (`Section 63 BSA 2023`).
6. `proposed_precedent_treatment`: Treatment claim (`Overrules Shafhi Mohammad`).
7. `extraction_confidence`: Algorithmic extraction score (0.0 to 1.0).
8. `review_status`: Explicit state enum (`pending_legal_review`).
9. `advocate_decision`: Blank until genuinely reviewed by an advocate.
10. `advocate_notes`: Mandatory comments if rejected or revision required.

---

## 3. Strict Non-Negotiable Rules

1. **Zero Self-Approval**: Machine scripts are forbidden from writing `legal_expert_approved` to database records.
2. **Attribution Authenticity**: No fictitious advocate identities, fake Bar Council registration numbers, or mock reviewer signatures are ever generated.
3. **Quarantine Separation**: Synthetic scaffolds (such as `IND-JUD-DEL-2024-BAIL`) can never be marked eligible for advocate review or dataset fine-tuning.
4. **Current Candidate State**: All 40 existing review candidate records (20 Phase 9 pilot records + 20 Phase 12 Batch 1 records) remain strictly in `pending_legal_review`.

