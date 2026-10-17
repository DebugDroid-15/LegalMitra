# LegalMitra Phase 23 Dataset Governance & Provenance Policy
**Workspace:** `C:\PROJECTS\LegalMitra`  
**Repository:** `https://github.com/DebugDroid-15/LegalMitra`  
**Owner:** Team Shatrujeet — Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo  
**Date:** October 2026  
**Classification:** Proprietary and Confidential  

---

## 1. Governance Objectives & Principles

The integrity of LegalMitra depends on the absolute provenance of its datasets. We operate under three non-negotiable governance principles:
1. **Zero Synthetic Approval:** No automated test, script, or model is permitted to approve or alter the decision status of review candidates. Human advocate reviews must originate from verified advocates enrolled with the Bar Council of India or state Bar Councils.
2. **Cryptographic Immutability:** Any frozen dataset or benchmark release is accompanied by a SHA-256 manifest. Any modification of a single byte invalidates the release gate.
3. **Partition Separation:**
   - **Evaluation Datasets (`data/12_evaluation/`, `data/13_evaluation/`):** Dedicated to independent regression and benchmark testing.
   - **Review Candidates (`data/03_generated/`, `data/06_review/`, `data/07_batches/`):** Tracked candidates awaiting advocate evaluation.
   - **Core Corpus (`data/01_raw/`, `data/02_processed/`, `data/legalmitra_kb.db`):** Authoritative legal enactments and judicial judgments.

---

## 2. Directory Hierarchy & Dataset Manifests

```
data/
├── 01_raw/                    # Unmodified authoritative primary legal source texts
├── 02_processed/              # Cleaned, segmented legal provisions and judgments
├── 03_generated/              # Pilot 20 frozen snapshot and generation artifacts
├── 06_review/                 # Package A: Frozen pilot review sheet and open issues
├── 07_batches/                # Package B: Batch 1 candidate expansion & review register
├── 12_evaluation/             # Phase 22 Benchmark Suite v1 (18 cases, manifest v1)
└── 13_evaluation/             # Phase 23 National Benchmark Suite v2 (26 cases, manifest v2)
```

### Manifest Details:
- **Suite v1:**
  - File: `data/12_evaluation/evaluation_cases_v1.json`
  - Manifest: `data/12_evaluation/manifest_v1.json`
  - Records: 18
  - SHA256: `6e4d284a1236db6d8aa32a0c2c19e593a1c3ce0445d3151df25026df12879a92`
- **Suite v2:**
  - File: `data/13_evaluation/evaluation_cases_v2.json`
  - Manifest: `data/13_evaluation/manifest_v2.json`
  - Records: 26
  - SHA256: `339b7a6108c02b6b5ba756971d3c879408ff7cc30cc223b40c3122e5ece41343`

---

## 3. Provenance & Quarantine Rules

1. **Quarantine of Synthetic Scaffolding:**
   The placeholder record `IND-JUD-DEL-2024-BAIL` remains permanently quarantined (`is_synthetic_scaffold=1`) in `legal_chunks`. Ingestion engines and search queries strictly filter out all quarantined rows.
2. **Advocate Review Candidate Freeze:**
   The 40 records in Package A (Pilot 20) and Package B (Batch 1) are under permanent freeze until authenticated human advocate import.
   Automated checks (`scripts/verify_freeze.py` and `scripts/verify_review_packages.py`) are integrated into the continuous test pipeline.

