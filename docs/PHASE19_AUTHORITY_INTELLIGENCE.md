# PHASE 19 — ENHANCED LEGAL AUTHORITY & PRECEDENT INTELLIGENCE

**Workspace:** `C:\PROJECTS\LegalMitra`  
**Classification:** Proprietary & Confidential — Team Shatrujeet  
**Date:** October 2026  
**Status:** Canonical Reference

---

## 1. Executive Summary

A critical weakness of naive legal graph tools is **blunt negative suppression**: if a later judgment states that an earlier ruling was *"doubted"* or *"overruled on point X"*, a naive system marks the entire historic precedent as invalid. In Indian jurisprudence, however:
- A decision may be overruled solely regarding one statutory clause while remaining the binding authority on all other holdings (e.g. *Shafhi Mohammad* overruled regarding mandatory Section 65B(4) certificates by *Arjun Khotkar*, while general technological principles remain sound).
- A 9-judge bench (*Puttaswamy*) overruled *ADM Jabalpur* (1976) regarding Article 21 suspension during emergency and *M.P. Sharma* regarding privacy searches, while leaving unrelated procedural holdings intact.

Phase 19 enhances LegalMitra's **Precedent Intelligence Engine** with **proposition-aware, scope-delimited precedent evaluation**.

---

## 2. 20-Tier Precedent Treatment Typology

Every citation link in the knowledge graph is enriched with:
- `citing_case_id` & `cited_case_id`
- `treatment`: Formal classification from `PrecedentTreatment`:
  1. `FOLLOWED`: Direct application of ratio.
  2. `APPLIED`: Extended to analogous factual/statutory context.
  3. `APPROVED`: Superior court endorses lower court doctrine.
  4. `AFFIRMED`: Decree confirmed on appeal.
  5. `DISTINGUISHED`: Inapplicable due to material factual difference.
  6. `EXPLAINED`: Meaning clarified by coordinate/superior bench.
  7. `CLARIFIED`: Latent ambiguity resolved.
  8. `REFERRED_TO_LARGER_BENCH`: Coordinate bench doubts prior view.
  9. `DOUBTED`: Soundness questioned without formal overruling.
  10. `OVERRULED`: Explicitly stripped of authority by larger bench.
  11. `PARTIALLY_OVERRULED`: Specific proposition invalidated; remainder binding.
  12. `REVERSED`: Subordinate judgment overturned in same matter.
  13. `SET_ASIDE`: Quashed on jurisdictional/procedural defects.
  14. `MODIFIED`: Relief altered.
  15. `READ_DOWN`: Narrowed to preserve constitutional validity.
  16. `SUPERSEDED_BY_LEGISLATION`: Nullified by subsequent legislative enactment.
- `treatment_passage_ref`: Exact paragraph or page number where the court delivers its analysis.

---

## 3. Proposition-Aware Negative Precedent Evaluation

Implemented in `legalmitra/caselaw/knowledge_graph.py`:
- `is_case_overruled(case_node_id, target_proposition=None)`
- `evaluate_precedent_status(case_node_id, target_proposition=None)`

### Behavioral Rules
1. **Full Overruling**: If a case is overruled across its entirety, positive citations are suppressed, and an explicit disclaimer is attached to any historical retrieval.
2. **Partial Overruling**: If a case is partially overruled (e.g. *Anvar P.V.* clarified by *Arjun Khotkar*), the system permits citation for unaffected propositions while presenting a targeted alert:
   > *"Warning: Proposition 'X' in this decision was overruled by [Court] in [Case]. The remainder of the decision remains valid law."*
3. **Preservation for Historical Research**: LegalMitra never permanently erases overruled cases. Historical point-in-time queries require access to the law as it stood at the time of the transaction.

