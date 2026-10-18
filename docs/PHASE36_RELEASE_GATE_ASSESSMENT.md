# Phase 36 Release Gate Assessment & Governance Decisions

**Project:** LegalMitra  
**Phase:** 36 — Corpus Eligibility Audit, Hindi Primary-Source Acquisition & Dataset Integrity  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** VERIFIED  

---

## 1. Release Gate Framework

LegalMitra enforces strict, independent release decisions across technical and operational subsystems to prevent premature scaling, unverified data contamination, or user-facing hallucination risks.

---

## 2. Independent Subsystem Gate Decisions

### 1. Source Registry Integrity: **GO**
- **Justification:** All 111 tracked sources have been reconciled and audited individually in `data/09_national_corpus/source_eligibility_ledger.json`.
- The 111 vs 33 discrepancy is fully resolved: exactly 33 are physically indexed and pretraining-eligible; 67 are unindexed catalog records; 10 are discovery candidates; and 1 is a quarantined test fixture.
- Finite State Machine enforces transition rules and rejects illegal state skips.

### 2. Hindi Source Authenticity and Structural Quality: **GO**
- **Justification:** All 52 authentic Hindi statutory provisions in the corpus were audited with 0 Unicode replacement characters, 0 detached combining diacritics, and 100% official Devanagari purna viram (`।`) preservation.
- Primary provenance verified against official Gazette of India Extraordinary publications (Acts 45, 46, and 47 of 2023).

### 3. Rights and Training Eligibility: **GO**
- **Justification:** Primary public edicts are legally verified under Section 52(1)(q) of the Indian Copyright Act, 1957.
- Constitutional Hindi text is verified under Article 394A.
- Commercial headnotes, editorial summaries, and private conversations (`conversations.db`) are strictly excluded.

### 4. Dataset Export Reproducibility: **GO**
- **Justification:** `TrainingCorpusExporter` hardened with manifest immutability protection and automated exclusion reporting.
- Manifest digests reproduced bitwise. Dry-run mode verified side-effect free.

### 5. Milestone B (1,000,000 Eligible Tokens): **NOT ACHIEVED (BLOCKED / PENDING PHASE 37)**
- **Justification:** Baseline pretraining tokens stand at **342,965 tokens** (net deficit of 657,035 tokens).
- Live acquisition of full BNS, BNSS, and BSA text from official portals was blocked by CDN anti-bot policies (HTTP 403) and CCA root certificate trust chain requirements.
- Under project rules, **we do not fabricate tokens**. Milestone B remains pending physical batch ingestion in Phase 37.

### 6. Original-Model Experimentation: **GO (Small-Scale Prototype Only)**
- **Justification:** 1,069,824-parameter transformer reproduction confirmed exact validation loss fidelity ($5.6607$). Controlled experiments on verified v4 manifests are permitted.

### 7. Large-Scale Pretraining (10M / 50M / 125M / 1.3B): **STRICT NO-GO**
- **Justification:** A 615x token deficit remains against Chinchilla compute-optimal pretraining requirements for a 10.55M model. Large-scale pretraining is strictly prohibited until Milestone D (50M tokens) is achieved.

### 8. Production Legal Answers (Grounded RAG): **GO**
- **Justification:** Production RAG pipeline in `legalmitra/rag/engine.py` remains isolated, fully operational, and covered by 307 passing automated non-live tests.
- 100% frozen asset and advocate review package preservation maintained.

---

## 3. Governance Summary Table

| Gate | Decision | Core Rationale | Next Phase Requirement |
|---|---|---|---|
| Source Registry Integrity | **GO** | 111 records reconciled; FSM enforced | Maintain auditable transition logs |
| Hindi Source Authenticity | **GO** | 52 provisions 100% Unicode intact | Ingest full Gazette text in Phase 37 |
| Rights & Training Eligibility | **GO** | Section 52(1)(q) public edicts verified | Maintain exclusion of proprietary commentary |
| Dataset Export Reproducibility | **GO** | Manifest immutability & digests verified | Preserve v4 digests |
| Milestone B (1M Tokens) | **NOT ACHIEVED** | 657k token deficit; acquisition blocked | Resolve PKI trust store in Phase 37 |
| Original Model Experimentation | **GO** | 1.07M model val loss reproduced ($5.6607$) | Keep experiments small-scale and isolated |
| Large-Scale Pretraining | **STRICT NO-GO** | 615x token deficit vs Chinchilla | Maintain strict gate |
| Production Legal Answers | **GO** | 307 non-live tests pass; RAG isolated | Maintain advocate review workflow |
