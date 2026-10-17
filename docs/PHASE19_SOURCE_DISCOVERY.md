# PHASE 19 — AUTOMATED LEGAL SOURCE DISCOVERY & CHANGE DETECTION SPECIFICATION

**Workspace:** `C:\PROJECTS\LegalMitra`  
**Classification:** Proprietary & Confidential — Team Shatrujeet  
**Date:** October 2026  
**Status:** Canonical Reference

---

## 1. Executive Summary

Legal materials in India evolve unpredictably: new Gazette notifications issue daily, High Courts hand down decisions continuously, and legislative amendments are published with varying commencement dates.

LegalMitra's **National Source Discovery Engine (`legalmitra/corpus/discovery_engine.py`)** provides a robust, non-intrusive discovery layer capable of:
1. Detecting new statutory enactments and gazette instruments.
2. Computing cryptographic SHA-256 signatures to detect true substantive changes vs. cosmetic layout modifications.
3. Classifying change events into an auditable 9-category taxonomy (`ChangeClassification`).
4. Preventing duplicate ingestion and preserving full provenance chains.

---

## 2. Multi-Repository Source Adapters

LegalMitra interfaces with authoritative official endpoints without violating rate limits or terms of access:

| Repository / Portal | Authority Level | Access Method | Change Detection Mechanism |
| :--- | :--- | :--- | :--- |
| **India Code (`indiacode.nic.in`)** | Central & State Primary | REST / Direct HTTP | Act number, enactment year, and PDF hash checking |
| **e-Gazette of India (`egazette.gov.in`)** | Statutory Orders & GSRs | Structured Portal Pull | S.O. / G.S.R. number, Extraordinary Gazette date |
| **Digital SCR (`digiscr.sci.gov.in`)** | Supreme Court Judgments | Direct HTTP / API | Neutral citation indexing (`YYYY INSC NNN`), volume hashes |
| **High Court Portals** | State Appellate Benches | Portal Search | Case type / number / judgment upload timestamps |
| **State Legislation Portals** | 28 States & 8 UTs | Portal Pull | State Gazette notifications and State Code listings |

---

## 3. Change Classification Taxonomy

When an official document is polled or discovered, the engine evaluates it against existing knowledge base records:

1. `NEW_DOCUMENT`: Completely new legal instrument not previously catalogued.
2. `EXACT_DUPLICATE`: Cryptographic SHA-256 matches an existing document exactly; skips processing.
3. `UPDATED_METADATA`: Canonical metadata enriched (e.g. commencement date added) without text change.
4. `CHANGED_SOURCE_FILE`: Raw PDF/HTML file bytes changed; triggers structural diff analysis.
5. `CHANGED_EXTRACTED_TEXT`: Text extracted from source document differs from existing normalized version.
6. `NEW_LEGAL_VERSION`: A post-amendment version of a section or statute has commenced.
7. `CORRECTED_OCR`: Better OCR run replaces unreadable text without altering underlying legal words.
8. `SUPERSEDED_DOCUMENT`: A newer gazette edition or consolidated Act replaces an older draft.
9. `UNRESOLVED_CHANGE`: Ambiguous delta routed to the Advocate Review Queue.

---

## 4. Reversible Diff Workflow

Every detected change is recorded as a `DocumentDiffRecord` storing:
- `diff_id`: Sequential identifier.
- `previous_hash` and `new_hash`: SHA-256 cryptographic checkpoints.
- `classification`: Operational change category.
- `detected_at`: ISO 8601 UTC timestamp.
- `requires_human_review`: Boolean flag routing substantial legal changes to licensed advocates.

