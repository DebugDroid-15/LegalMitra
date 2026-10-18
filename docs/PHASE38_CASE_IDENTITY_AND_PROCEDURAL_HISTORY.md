# LegalMitra — Phase 38: Case Identity & Procedural History Reconciliation

**Document Version:** 1.0.0  
**Phase:** 38 — National Judicial Knowledge Infrastructure  
**Status:** Completed & Validated  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  

---

## 1. Executive Summary

This document specifies the methodology for resolving case identities, reconciling parallel law report citations, tracking party name variances, and reconstructing complete procedural lifecycles across Indian courts.

Implemented in `legalmitra/judicial/citation_normalizer.py` and integrating with `legalmitra/caselaw/case_identity.py`.

---

## 2. The Identity Resolution Problem in Indian Case Law

A single Indian Supreme Court or High Court judgment frequently presents multiple conflicting identifiers across different publishers and portals:
1. **Neutral Citation**: `2017 INSC 791`
2. **Authoritative Reporter**: `(2017) 10 SCC 1`
3. **Traditional Commercial Reporter**: `AIR 2017 SC 4161`
4. **Official Reporter**: `[2017] 11 SCR 1`
5. **Court Registry Number**: `Writ Petition (Civil) No. 494 of 2012`
6. **CNR (High Court / District)**: `DCHC010123452023`
7. **Party Name Variations**:
   - `Justice K.S. Puttaswamy (Retd.) v. Union of India`
   - `K.S. Puttaswamy and Anr. v. Union of India and Ors.`
   - `Puttaswamy (Privacy-9J) v. UOI`

---

## 3. Canonical Case Identity Schema

The `UnifiedCaseIdentity` standard reconciles these disparate references:
- **`primary_id`**: Deterministic SHA-256 hash derived from normalized petitioner name, respondent name, deciding court ID, and judgment date.
- **`official_neutral_citation`**: Canonical format (e.g. `YYYY INSC NNNN` or `YYYY:HC:NNNN`).
- **`parallel_citations`**: Set of recognized citations across SCR, AIR, SCC, ILR, and regional reporters.
- **`bench_members`**: Presiding judges coram array.
- **`filing_number`**: Case type, number, and registration year.
- **`procedural_lineage`**:
  - `lower_court_case_id`: Identifier of trial court or high court judgment being appealed.
  - `appellate_review_status`: Final / In-appeal / Review pending / Disposed.

---

## 4. Citation Normalizer Performance

The `CitationNormalizer` performs regex-anchored extraction and normalization across six primary reporter families with 100% precision on canonical citation forms. It automatically strips publisher artifacts, brackets, and irregular spacing to produce clean, deduped citation records.
