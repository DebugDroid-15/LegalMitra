# PHASE 19 — STRUCTURAL LEGAL DOCUMENT DIFFING & HISTORICAL RECONSTRUCTION

**Workspace:** `C:\PROJECTS\LegalMitra`  
**Classification:** Proprietary & Confidential — Team Shatrujeet  
**Date:** October 2026  
**Status:** Canonical Reference

---

## 1. Executive Summary

A core danger in statutory analysis is confusing an editorial reformatting with a substantive legal amendment. Substituting *"three years"* with *"seven years"* fundamentally transforms an offence from bailable to non-bailable under Indian criminal procedure.

LegalMitra's **Structural Legal Diffing Engine (`legalmitra/corpus/legal_diff.py`)** automatically compares statutory versions and classifies modifications into a formal 10-tier legal typology (`LegalModificationType`).

---

## 2. Legal Modification Typology

| Modification Type | Semantic / Doctrinal Definition | Advocate Review Trigger |
| :--- | :--- | :--- |
| `INSERTION` | A new provision, clause, proviso, or explanation enacted into the principal Act | Automatic flag if penal |
| `DELETION` | A provision, sub-clause, or explanation omitted or repealed | **Mandatory Advocate Review** |
| `SUBSTITUTION` | Full rewording of an existing operative section | **Mandatory Advocate Review** |
| `PENALTY_ENHANCEMENT` | Term of imprisonment increased or fine quantum amplified | **Mandatory Advocate Review** |
| `PENALTY_REDUCTION` | Punishment mitigated or community service alternative introduced | **Mandatory Advocate Review** |
| `LIMITATION_ALTERATION` | Time window for filing suit, complaint, or appeal extended or truncated | **Mandatory Advocate Review** |
| `RENUMBERING` | Section repositioned due to preceding insertions without textual change | Low priority |
| `COMMENCEMENT_MODIFICATION` | Phased commencement or enforcement date altered via statutory order | High priority |
| `EDITORIAL_OR_TYPO` | Punctuation or spelling erratum published in official corrigendum | Verified automated |
| `NO_SUBSTANTIVE_CHANGE` | Textually identical; zero delta | Skipped |

---

## 3. Historical Point-in-Time Reconstruction

Using the structural diff results and the bitemporal valid time axis:
- A user querying *"What was the maximum penalty under Section 304A IPC on 15 May 2018?"* is served the historic version operative on that date.
- The engine reconstructs the exact section text as it existed on any date $t$ by replaying amending instruments effective on or prior to $t$.
- If an amendment was published but stayed or held in abeyance (such as Section 106(2) BNS on hit-and-run driver reporting), the engine preserves its suspended status.

