# LegalMitra — Phase 39: Citation & Case Identity Resolution Architecture

**Document Version:** 1.0.0  
**Phase:** 39 — National Judicial Corpus Expansion & Precedent Verification  
**Status:** Completed & Validated  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  

---

## 1. Executive Summary

This document specifies the enhanced citation normalization and case identity resolution architecture implemented in [`CaseIdentityResolver`](file:///c:/PROJECTS/LegalMitra/legalmitra/judicial/identity_resolver.py) and [`CitationNormalizer`](file:///c:/PROJECTS/LegalMitra/legalmitra/judicial/citation_normalizer.py). It addresses the complex multi-identifier reality of Indian judicial reporting, resolving parallel citations, normalizing institutional party variations, and preventing wrongful case mergers.

---

## 2. Parallel Citation Reconciliation

Indian legal research relies on competing official and commercial reporters. LegalMitra normalizes and cross-indexes these to a single [`CanonicalCaseIdentity`](file:///c:/PROJECTS/LegalMitra/legalmitra/judicial/identity_resolver.py):

```
+-----------------------------------------------------------------------------------+
|                        CANONICAL CASE IDENTITY RECORD                             |
| ID: IND-SC-1973-KESAVANANDA                                                       |
| Title: Kesavananda Bharati Sripadagalvaru v. State of Kerala                      |
| Court: IND-SC | Year: 1973 | Coram: 13 Judges                                     |
+-----------------------------------------------------------------------------------+
       ^                           ^                           ^
       |                           |                           |
+------+------+             +------+------+             +------+------+
| (1973) 4    |             | AIR 1973    |             | [1973] Supp |
| SCC 225     |             | SC 1461     |             | SCR 1       |
+-------------+             +-------------+             +-------------+
```

---

## 3. Litigant Name Normalization Rules

Common abbreviations and party suffixes are standardized deterministically:
- `UOI`, `U.O.I.`, `Govt. of India` -> `Union of India`
- `State of NCT of Delhi`, `State of Delhi` -> `State (NCT of Delhi)`
- `State of Raj.`, `State of Raj` -> `State of Rajasthan`
- `State of Mah.`, `State of Mah` -> `State of Maharashtra`
- `State of U.P.`, `State of UP` -> `State of Uttar Pradesh`
- `State of W.B.`, `State of WB` -> `State of West Bengal`
- `and others`, `& others` -> `& Ors.`
- `and another`, `& another` -> `& Anr.`

---

## 4. Disambiguation & Anti-Merger Safeguards

To prevent wrongful merging of distinct cases sharing similar parties:
1. **Court & Year Boundary**: Two cases are never merged if their deciding court IDs or decision years differ.
2. **Procedural Posture Separation**: A bail order, an interlocutory revision, and a final conviction appeal in the same trial maintain distinct event IDs within a shared [`case_chain_id`](file:///c:/PROJECTS/LegalMitra/legalmitra/judicial/procedural_history.py).
3. **Ambiguity Flagging**: If a citation match yields conflicting coram or dates, the record is flagged `is_ambiguous = True` with human-auditable notes, retaining candidate status until verified.
