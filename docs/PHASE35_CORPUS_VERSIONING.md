# Phase 35 National Legal Corpus Versioning and Temporal Integrity

**Project:** LegalMitra  
**Phase:** 35 — National Legal Data Engine, Source Verification & Corpus Scaling Infrastructure  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** VERIFIED  

---

## 1. Temporal Integrity Architecture

A primary point of legal failure in AI models is **temporal conflation**: applying an amendment before it commences, or assuming that the enactment date equals the date of enforcement.

In Indian law, an Act is frequently passed by Parliament (enacted) months or years before the Central Government issues an official Gazette notification appointing the date on which it comes into force (commencement date).

Phase 35 implements `NationalCorpusVersioningEngine` in `legalmitra/corpus/corpus_versioning.py` and maintains an auditable version ledger in `data/09_national_corpus/corpus_version_ledger.json`.

---

## 2. Temporal Version Record Specification

Each version transition records:
- `version_id`: Stable compound key (e.g. `IND-STAT-BNS-2023:1.0.0-commenced`).
- `source_id`: Canonical legal instrument identifier.
- `semantic_version`: Version label tracking mutations.
- `change_type`: `INITIAL_CREATION`, `AMENDMENT`, `REPEAL`, `COMMENCEMENT_NOTIFICATION`, `PARSER_UPGRADE`, `TEXT_CORRECTION`.
- `enactment_date`: Formal date of legislative assent.
- `commencement_date`: Date appointed by Gazette notification for coming into force.
- `repealed_by_source_id`: Pointer to successor enactment if repealed.
- `superseded_source_id`: Pointer to predecessor enactment.
- `authoritative_gazette_ref`: Official Gazette of India notification number.

---

## 3. Seed Temporal Transitions & Repeal Mappings

The version ledger currently tracks 6 active baseline transition records:

| Old Instrument | Repealed / Superseded By | Enactment Date | Commencement Date | Gazette Notification |
|---|---|---|---|---|
| Indian Penal Code, 1860 (`IND-STAT-IPC-1860`) | Bharatiya Nyaya Sanhita, 2023 (`IND-STAT-BNS-2023`) | 2023-12-25 | **2024-07-01** | Gazette of India S.O. 850(E) |
| Code of Criminal Procedure, 1973 (`IND-STAT-CRPC-1973`) | Bharatiya Nagarik Suraksha Sanhita, 2023 (`IND-STAT-BNSS-2023`) | 2023-12-25 | **2024-07-01** | Gazette of India S.O. 849(E) |
| Indian Evidence Act, 1872 (`IND-STAT-IEA-1872`) | Bharatiya Sakshya Adhiniyam, 2023 (`IND-STAT-BSA-2023`) | 2023-12-25 | **2024-07-01** | Gazette of India S.O. 851(E) |

### Key Guarantees:
1. **No Destructive Overwriting:** The historic texts of IPC 1860, CrPC 1973, and IEA 1872 are preserved bitwise in the corpus. They are not erased or overwritten by the 2023 codes.
2. **Temporal Traceability:** When retrieving legal provisions or generating pretraining manifests, the version ledger provides explicit temporal boundaries.
3. **Database Separation:** The version ledger exists solely in `data/09_national_corpus/corpus_version_ledger.json` and does not mutate `data/legalmitra_kb.db` or `data/conversations.db`.
