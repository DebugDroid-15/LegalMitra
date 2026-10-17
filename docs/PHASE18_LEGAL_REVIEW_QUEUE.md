# PHASE 18 — LEGAL REVIEW QUEUE & ADVOCATE BENCHMARK REGISTRY

**Workspace:** `C:\PROJECTS\LegalMitra`  
**Classification:** Proprietary & Confidential — Team Shatrujeet  
**Date:** October 2026  
**Status:** Canonical Operations Registry

---

## 1. Executive Summary

LegalMitra enforces a strict policy that no AI-generated answer or synthetic question-answer pair may be labeled as "ground truth", "verified", or "approved" without an auditable signature from an enrolled Indian advocate.

This document details the active Legal Review Queue across all 40 candidate records, tracking their status, governing source citations, and instructions for human review.

---

## 2. Active Review Batches Overview

| Batch ID | Candidate File | Review Sheet | Total Examples | Status | Target Jurisdiction |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Pilot Batch (Batch 0)** | `data/06_review/pilot_20_examples.jsonl` | `pilot_20_review_sheet.csv` | 20 | `pending_legal_review` | Pan-India (CrPC, IPC, NI Act, CPC) |
| **Expansion Batch 1** | `data/07_batches/batch_01_candidates/batch_01_candidates.jsonl` | `batch_01_review_sheet.csv` | 20 | `pending_legal_review` | Central Statutes & Modern Criminal Law |
| **Total in Queue** | — | — | **40** | **100% Pending** | — |

---

## 3. Reviewer Instructions & Adjudication Rubric

Enrolled advocates adjudicating candidate examples evaluate four statutory criteria:

1. **Substantive Accuracy (Score 1–5)**:
   - Does the answer correctly state the applicable statutory section, elements of the offence/cause of action, and exception clauses?
2. **Temporal Correctness (Score 1–5)**:
   - Does the answer accurately distinguish pre-July 2024 law (IPC/CrPC/IEA) from post-July 2024 law (BNS/BNSS/BSA), respecting Article 20(1) and BNSS Section 531 savings?
3. **Jurisdictional Precision (Score 1–5)**:
   - Does the answer avoid generalizing State-specific local amendments or High Court rules to other states?
4. **Citation Grounding (Score 1–5)**:
   - Are all cited sections, court decisions, and gazette references verifiable and free from hallucinated pinpoints?

### Allowable Advocate Decisions
- `APPROVED`: Answer is substantively sound, temporally accurate, and safely grounded.
- `MODIFICATION_REQUIRED`: Answer is broadly correct but requires specific text corrections.
- `REJECTED`: Answer contains substantive errors, hallucinates citations, or confuses temporal applicability.

---

## 4. Audit Safeguards Against Unauthorized Labeling

- `ReviewImporter` (`legalmitra/review/importer.py`) automatically aborts and rolls back transactions if:
  - Advocate enrollment number is missing or invalid.
  - Review decisions are populated by automated scripts.
  - Hash collisions or row discrepancies are detected against the frozen candidate files.
- The 40 examples will remain strictly in `pending_legal_review` until signed review sheets are officially submitted.

