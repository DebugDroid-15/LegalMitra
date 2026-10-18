# Phase 37 Dataset Manifests Specification & Cryptographic Registry

**Project:** LegalMitra  
**Phase:** 37 — Authorized National Corpus Acquisition, Hindi Legal Data Expansion & Milestone B Readiness  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** COMPLETED & VERIFIED  

---

## 1. Executive Summary

Phase 37 generated version 5.0.0 of the LegalMitra pretraining dataset manifests. The manifests document every eligible legal passage, its cryptographic digest, source provenance, language classification, and source-grouped split assignment.

In accordance with Mandatory Rule 5, all historical manifests (`v2`, `v3`, `v4`) remain completely immutable and byte-for-byte unchanged.

---

## 2. Version 5 Manifest Summary Table

| Manifest File | Relative Repository Path | Passages | Token Count | Cryptographic SHA-256 Digest |
| :--- | :--- | :--- | :--- | :--- |
| **Dataset Manifest v5** | `research/original_model/manifests/dataset_manifest_v5.json` | 1,633 | 357,358 | `ecc7fa69ab3ba5269e295e87e25bacfe6645054266fd59e631886a15cd845c6a` |
| **Train Manifest v5** | `research/original_model/manifests/train_manifest_v5.json` | 1,408 | 310,605 | `1382f8ab217bb62f7de779e6955208848a8a575aeef2244bc890913a6c242879` |
| **Val Manifest v5** | `research/original_model/manifests/val_manifest_v5.json` | 43 | 6,961 | `1de2c18ca940173235bc91f4b385226f35eae83ac6a27da75bc5144ba04a6cac` |
| **Test Manifest v5** | `research/original_model/manifests/test_manifest_v5.json` | 182 | 39,792 | `90be57b5df25329331553a6b9a4d7e0135be79e7eaabf0d50cba7144139daacd` |

---

## 3. Linguistic Breakdown across Partitions

| Partition Split | Total Passages | English Passages | Hindi Passages | English Tokens | Hindi Tokens | Total Split Tokens |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Train Split** | 1,408 | 1,335 | 73 | 296,898 | 13,707 | 310,605 |
| **Validation Split**| 43 | 28 | 15 | 4,772 | 2,189 | 6,961 |
| **Test Split** | 182 | 157 | 25 | 35,817 | 3,975 | 39,792 |
| **Total Corpus** | **1,633** | **1,520** | **113** | **337,487** | **19,871** | **357,358** |

---

## 4. Historical Manifest Immutability Audit

Historical manifests from Phase 33 (`v2`), Phase 34 (`v3`), and Phase 35/36 (`v4`) were audited to ensure zero in-place mutation:

| Historical Manifest | Phase Origin | Expected SHA-256 Digest | Audit Status |
| :--- | :--- | :--- | :--- |
| `dataset_manifest_v4.json` | Phase 35/36 | `15088ea8e24555478a54fcb7d44bddefe39a1370fe3597bb298d2e3511f3cc4e` | **EXACT MATCH (Bitwise Identical)** |
| `train_manifest_v4.json` | Phase 35/36 | `cf3fc18f4bf87329e2f473ca49a9907fb2df16f86986cd1bc10ae98c06d0d822` | **EXACT MATCH (Bitwise Identical)** |
| `val_manifest_v4.json` | Phase 35/36 | `2e96962c9859c3f7824093cd9d9b754f6c2fa6d07a02aeb8d3ffe906c4fbf118` | **EXACT MATCH (Bitwise Identical)** |
| `test_manifest_v4.json` | Phase 35/36 | `818962fecbb7efafeddbf8080a7c3e2853a47bd38d9f28389c64e55e4abc0d23` | **EXACT MATCH (Bitwise Identical)** |
| `dataset_manifest_v3.json` | Phase 34 | `d5aa11f93e36e6e22f759a2245b91b9ceec87ec5ffec25a6e87f6511ec7f1c1f` | **EXACT MATCH (Bitwise Identical)** |
| `dataset_manifest_v2.json` | Phase 33 | `10caea93fa0592e8ca929a287955519db8271701bcf5e796e95cefafeea86d70` | **EXACT MATCH (Bitwise Identical)** |

---

## 5. Exporter Immutability Safeguards

The `TrainingCorpusExporter` enforces write-once protection:
- Attempting to export an existing manifest version with `overwrite=False` raises `FileExistsError`.
- Manifest generation in dry-run mode (`--dry-run`) calculates all metrics, summaries, and digests without writing to disk or altering timestamps.

