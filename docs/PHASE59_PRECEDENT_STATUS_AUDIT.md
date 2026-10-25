# LegalMitra Phase 59 — Precedent Status Audit

**Release Version:** `0.59.0`  
**Phase Identifier:** `LEGALMITRA-PHASE59`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Timestamp:** `2026-10-25T17:35:00Z`

---

## 1. Precedent Overruling & Scope Disentanglement

A primary failure mode in legal NLP is the **coarse collapse of judicial precedent**: treating an entire landmark judgment as invalid when only a single proposition or direction was overruled.

In Phase 59, LegalMitra enforces proposition-level holding scopes via `LegalKnowledgeGraph.is_case_overruled(case_id, target_proposition=...)`.

### Case Study: *Subhash Kashinath Mahajan v. State of Maharashtra* (2018) 6 SCC 454
- **Overruled Direction:** The direction mandating a preliminary enquiry and prior written approval of the appointing authority before registering an FIR under the SC/ST Act was recalled and overruled in *Union of India v. State of Maharashtra* (2020) 4 SCC 761 and nullified by Parliament inserting Section 18A.
- **Surviving Doctrine:** The core jurisprudence that an anticipatory bail application is not completely barred under Section 18 if the complaint, taken on its face, fails to make out a prima facie case, remains binding law affirmed in *Prathvi Raj Chauhan v. Union of India* (2020) 4 SCC 727.

---

## 2. Test Execution Verification

```python
# 1. Querying overruled proposition correctly reports overruling
is_overruled, reason = kg.is_case_overruled(
    "CASE-SC-SUBHASH-KASHINATH-2018",
    target_proposition="preliminary enquiry"
)
assert is_overruled is True

# 2. Querying general anticipatory bail principles avoids false overruling
is_overruled, reason = kg.is_case_overruled(
    "CASE-SC-SUBHASH-KASHINATH-2018",
    target_proposition="general principles of anticipatory bail where no prima facie offence made out"
)
assert is_overruled is False
```
