# LegalMitra Phase 33: Data Rights, Legal Reuse & Provenance Audit

**Status:** `VERIFIED`  
**Execution Date:** 2026-10-18  
**Reference Artifact:** `data/20_evaluation/corpus_inventory_v1.json`  

---

## 1. Executive Summary

Public availability on the internet does not automatically confer an unrestricted right to train commercial or proprietary machine learning models. Phase 33 conducted an exhaustive legal rights audit across all 59 registered sources in LegalMitra to establish a lawful basis for pretraining under Indian copyright law, statutory exceptions, and open government data principles.

---

## 2. Statutory Rights Framework under Indian Law

All pretraining-eligible text in LegalMitra falls under strict statutory exceptions of the **Indian Copyright Act, 1957 (Act No. 14 of 1957)** and open government publishing licenses:

### 1. Central & State Legislation (Section 52(1)(q)(i))
- **Statutory Provision:** Section 52(1)(q)(i) explicitly provides that the reproduction or publication of any Act of a Legislature (accompanied by the original title and text) does NOT constitute an infringement of copyright.
- **Government Open Data License (GODL-India):** Official publications made available on India Code (`indiacode.nic.in`) and the Gazette of India (`egazette.gov.in`) are governed by the National Data Sharing and Accessibility Policy (NDSAP), granting permission to use, adapt, and transform public records for research and development.
- **Application in LegalMitra:** 36 Central Acts and 4 State/UT Acts are held under this exception.

### 2. Judicial Opinions and Orders (Section 52(1)(q)(iv))
- **Statutory Provision:** Section 52(1)(q)(iv) explicitly protects the reproduction or publication of any judgment or order of a court, tribunal or other judicial authority, unless prohibited by the court.
- **Official Portals:** Judgments ingested from official Supreme Court of India portals (`main.sci.gov.in`, `judgments.ecourts.gov.in`) and the Delhi High Court repository (`delhihighcourt.nic.in`) represent public judicial records.
- **Application in LegalMitra:** 17 landmark judgments are held under this exception.

### 3. Authoritative Hindi Statutory Texts
- **Article 394A, Constitution of India:** The Hindi text of the Constitution published under the authority of the President of India is deemed to be the authoritative text thereof in the Hindi language.
- **Authoritative Texts (Central Laws) Act, 1973 (Act No. 50 of 1973):** Provides that translation in Hindi of any Central Act published in the Official Gazette under the authority of the President is an authoritative text.
- **Application in LegalMitra:** 29 curated Hindi statutory provisions are ingested exclusively from official Gazette and Legislative Department publications.

---

## 3. Strict Pretraining Exclusions

| Excluded Resource | Category | Legal & Governance Justification |
|---|---|---|
| **`IND-JUD-DEL-2024-BAIL`** | Synthetic Scaffold | Quarantined to prevent benchmark contamination and model poisoning. |
| **`conversations.db`** | User Chat Records | Confidentiality & privacy protection under Section 43A IT Act & DPDP Act 2023. |
| **`data/07_batches/review/`** | Advocate Packages | 40 candidates in `pending_legal_review` status. Unapproved labels must not be trained on. |
| **`benchmarks/` (v1–v9)** | Evaluation Ground Truth | Held-out evaluation questions; training would constitute test-set leakage. |
| **Third-Party Headnotes** | Proprietary Commercial Law | SCC, AIR, or Manupatra proprietary headnotes are strictly prohibited; only verbatim judicial opinions are used. |

---

## 4. Provenance Traceability Matrix

Every ingested passage in the bilingual pipeline records:
1. `source_id`: Standardized institutional identifier.
2. `source_url`: Official Government of India or High Court portal URL.
3. `provenance`: Specific official gazette notification, act number, or judicial case citation.
4. `sha256`: Cryptographic content checksum verifying unadulterated reproduction.
5. `license_terms`: Explicit citation to Section 52(1)(q) or GODL-India.

