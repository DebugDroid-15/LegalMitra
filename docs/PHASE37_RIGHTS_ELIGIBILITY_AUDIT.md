# Phase 37 Rights & Training Eligibility Legal Audit

**Project:** LegalMitra  
**Phase:** 37 — Authorized National Corpus Acquisition, Hindi Legal Data Expansion & Milestone B Readiness  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** COMPLETED & VERIFIED  

---

## 1. Executive Summary

LegalMitra enforces strict legal rights and copyright governance over all training data. In accordance with Indian copyright law, no text is permitted into foundation model training manifests without affirmative verification of its lawful eligibility.

Phase 37 audited all 1,633 pretraining passages across English and Hindi against the Indian Copyright Act, 1957, judicial precedents on legal copyrightability, and project boundary invariants.

---

## 2. Statutory Rights Framework

### 2.1 Section 52(1)(q) of the Indian Copyright Act, 1957
Section 52(1)(q) provides statutory immunity from copyright infringement for the reproduction or publication of:
1. **Section 52(1)(q)(i):** Any matter which has been published in any Official Gazette (e.g. Gazette of India Extraordinary, Central/State notifications).
2. **Section 52(1)(q)(ii):** Any Act of a Legislature (Central Parliament and State Legislative Assemblies).
3. **Section 52(1)(q)(iii):** Any report of any committee, commission, or council appointed by the Government.
4. **Section 52(1)(q)(iv):** Any judgment or order of a court, tribunal, or other judicial authority.

### 2.2 Judicial Precedent: *Eastern Book Company v. D.B. Modak* (2008) 1 SCC 1
The Supreme Court of India held that while the raw, certified text of judicial judgments and statutory enactments is in the public domain under Section 52(1)(q), private editorial enhancements—such as commercial headnotes, case syllabi, selection and arrangement of passages, and editorial footnotes—are protected by copyright if they display a minimum degree of intellectual effort and creativity.

**Operational Rule:** LegalMitra ingests strictly bare, raw legislative and judicial text. All publisher headnotes, editorial summaries, and proprietary annotations are rigorously stripped and barred from pretraining manifests.

### 2.3 Hindi Legal Text Enactments
- **Constitutional Texts:** Authorized Hindi text published under presidential authority pursuant to **Article 394A** of the Constitution of India.
- **Central Acts in Hindi:** Published in the Official Gazette pursuant to **Section 5(1) of the Official Languages Act, 1963**, which provides that the Hindi translation published under the authority of the President in the Official Gazette shall be deemed to be the authoritative text thereof in Hindi.

---

## 3. Strict Boundary & Quarantine Verification

| Regulated Category | Database / Storage Location | Rights Decision | Training Manifest Eligibility | Audit Verification Status |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Statutory Texts (Bare)** | `data/legalmitra_kb.db`, `data/09_national_corpus/` | Cleared under Sec. 52(1)(q)(i)/(ii) | **ELIGIBLE** (1,633 passages) | 100% verified bare text |
| **Judicial Orders (Bare)** | `data/legalmitra_kb.db`, `data/09_national_corpus/` | Cleared under Sec. 52(1)(q)(iv) | **ELIGIBLE** | Bare orders only; 0 headnotes |
| **Synthetic Scaffold Chunks** | `data/legalmitra_kb.db` (`IND-JUD-DEL-2024-BAIL`) | Synthetic fixture; not authentic law | **BLOCKED & QUARANTINED** | Exactly 6 chunks quarantined; 0 exported |
| **Advocate Review Packages** | `data/07_batches/review/` (Package A & B) | Pending human legal review | **BLOCKED & EXCLUDED** | Exactly 40 candidates pending; 0 exported |
| **User Conversations DB** | `data/conversations.db` | Private user communications (DPDP Act) | **STRICTLY ISOLATED** | 0 records exported; isolated SQLite file |

---

## 4. Rights Audit Conclusion

The Phase 37 pretraining dataset (`dataset_manifest_v5.json`, 357,358 tokens) is 100% compliant with Section 52(1)(q), Article 394A, and Section 5(1) of the Official Languages Act, 1963. Zero private data, zero synthetic text, zero editorial annotations, and zero unverified review candidates are present in any pretraining partition.

