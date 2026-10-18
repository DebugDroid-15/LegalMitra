# LegalMitra Phase 32: Defect Register

**Phase:** 32 — Original Foundation Model Validation, Data Integrity & Generalization Gate  
**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Owner:** Team Shatrujeet  
**Date:** 2026-10-18  
**Classification:** Proprietary and Confidential  

---

## 1. Executive Summary

This register records all defects, root causes, severity levels, remediation actions, and verification statuses identified during the Phase 32 architecture audit, data leakage audit, and generalization evaluation.

---

## 2. Active Defect Ledger

| Defect ID | Defect Description | Severity | Root Cause | Status in Phase 32 | Verification Evidence |
|---|---|---|---|---|---|
| **DEF-3201** | Padding token loss contamination in causal LM objective | Medium-High | `F.cross_entropy` omitted `ignore_index=pad_token_id`, allowing model to reduce loss by predicting padding tokens | **RESOLVED** | Added `pad_token_id: int = 0` to config; `ignore_index` active in loss calculation; verified via `test_padding_token_loss_exclusion` |
| **DEF-3202** | Devanagari characters mapped to `<unk>` in tokenizer | High | Tokenizer training corpus only contained English statutory chunks, so Devanagari base characters were unseeded | **RESOLVED** | Pre-seeded `0x0900`–`0x097F` and ASCII printable range in base vocabulary; verified via `test_devanagari_preseeded_tokenization` |
| **DEF-3203** | Intra-document data leakage in sequential 90/10 split | High | Sequential array slice split `IND-STAT-IT-2000` across train and val, causing identical boilerplate across partitions | **RESOLVED** | Implemented `split_strategy="source_grouped"`; cross-split source overlap reduced to **0**; verified via `test_document_grouped_split_leakage_zero` |
| **DEF-3204** | Sequential split overwrote primary train/val manifests | Medium | Hardcoded manifest filenames in `dataset.py` overwritten during ablation testing | **RESOLVED** | Manifest filenames dynamically suffixed by split strategy (`train_manifest_v1.json` vs `train_manifest_sequential_v1.json`) |
| **DEF-3205** | Windows console `cp1252` crash when printing Hindi characters | Medium | Default Windows console encoding unable to handle Devanagari UTF-8 strings | **RESOLVED** | Added `sys.stdout.reconfigure(encoding="utf-8")` to experiment and audit runners |
| **DEF-3206** | Generalization deficit on Devanagari text | Medium-High | Pretraining corpus consists exclusively of English legal enactments | **REGISTERED** | Generalization harness recorded PPL 2509.15 on Hindi text; bilingual legal corpus expansion planned for scaling phase |
| **DEF-3207** | Prototype incapable of complex legal reasoning | High (if deployed as advisor) | 0.94M parameter next-token predictor lacks multi-layer depth for statutory deduction | **REGISTERED (By Design)** | System architecture strictly enforces RAG grounding; prototype barred from serving ungrounded legal counsel |

---

## 3. Residual Risk Assessment

- **Implementation Integrity:** Zero unresolved engineering defects in the transformer architecture, causal attention, or tokenizer.
- **Leakage Integrity:** Completely eliminated data leakage in the validation partition.
- **Safety Safeguard:** The prototype model is strictly quarantined within `research/original_model/` and is disconnected from production legal answer endpoints.

