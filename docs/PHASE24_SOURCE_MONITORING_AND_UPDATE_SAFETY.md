# LEGALMITRA PHASE 24: SOURCE MONITORING & UPDATE SAFETY PROTOCOL

**Classification:** Proprietary & Confidential — Team Shatrujeet  
**Phase:** 24 — Master Expansion  
**Date:** October 2026  
**Status:** Ingested & Verified  

---

## 1. Executive Summary

LegalMitra ingests legal sources exclusively from authoritative, authenticated institutional portals, including India Code (`indiacode.nic.in`), eGazette (`egazette.gov.in`), and official Court portals (Digital SCR at `digiscr.sci.gov.in` and `main.sci.gov.in`).

To ensure that incoming statutory amendments, gazette notifications, and appellate reversals do not corrupt the existing grounded knowledge base, LegalMitra enforces continuous source monitoring and atomic update safety guards.

---

## 2. Source Traceability & Cryptographic Verification

1. **SHA-256 Checksum Validation**:
   - Every registered source document and chunk has its contents hashed using SHA-256 upon initial retrieval.
   - Any modification in upstream text generates a checksum mismatch alert, blocking automated updates until verified by human legal review.

2. **Immutable Versioning**:
   - When a statute or rule is amended, previous versions are preserved with temporal applicability dates (`effective_date`, `is_historical = 1`) rather than overwriting historical statutory text.
   - Criminal offenses committed prior to July 1, 2024 remain anchored to IPC/CrPC provisions pursuant to Article 20(1) and Section 531 of BNSS.

---

## 3. Scaffolding & Unverified Candidate Quarantine

1. **Synthetic Scaffold Isolation**:
   - Scaffold sources (specifically `IND-JUD-DEL-2024-BAIL`) remain segregated with `is_synthetic_scaffold = 1`.
   - Production retrieval routines and LLM context builders filter out scaffold rows at the database level (`WHERE is_synthetic_scaffold = 0`).

2. **Candidate Review Pipeline**:
   - Batches undergoing review (such as Pilot 20 and Batch 01 Candidate Expansion) remain strictly locked in `pending_legal_review` status.
   - No unverified candidate is promoted to `verified_authoritative` without explicit advocate sign-off in the tracking register.
