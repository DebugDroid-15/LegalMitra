# LegalMitra Phase 33: Held-Out Generalization & Legal Trust Boundaries Report

**Status:** `VERIFIED`  
**Execution Date:** 2026-10-18  
**Harness Script:** `scripts/evaluate_generalization_v2.py`  
**Checkpoint Evaluated:** `research/original_model/checkpoints/phase33_exp_d_multilingual_joint.pt`  
**Results Artifact:** `data/20_evaluation/generalization_eval_results_v2.json`  

---

## 1. Executive Summary

Phase 33 evaluated the multilingual causal Transformer on four strictly held-out evaluation sets with zero training and validation leakage.

The primary objective was to determine whether the model learns generalizable language syntax, structure, and vocabulary dependencies on unseen Indian legal documents, while strictly demarcating the boundaries between next-token statistical prediction and authoritative legal reasoning.

---

## 2. Held-Out Generalization Evaluation Table

Random Guessing Baseline: $\ln(2048) = 7.6246$ nats | Perplexity = **2,048.0**

| Evaluation Domain | Held-Out Legal Sources | Sample Count | Evaluated Tokens | Cross-Entropy Loss | Perplexity (PPL) | Delta vs Random Baseline | Generalization Verdict |
|---|---|---|---|---|---|---|---|
| **Held-Out English Statutes** | DPDP Act 2023, Limitation Act 1963 | 66 chunks | 22,140 | **5.6911** | **296.21** | **-1.9335** | **LEARNED & GENERALIZED** |
| **Held-Out Judicial Precedents**| Arjun Khotkar (SC 2020) | 4 chunks | 1,480 | **5.8787** | **357.33** | **-1.7460** | **LEARNED & GENERALIZED** |
| **Bilingual Statutory Queries** | Section 482 / धारा 528, Article 21 | 6 queries | 264 | **6.6705** | **788.79** | **-0.9541** | **LEARNED & GENERALIZED** |
| **Held-Out Hindi Statutes** | IT Act 2000 (Official Hindi) | 3 provisions | 382 | **8.0093** | **3,008.72** | **+0.3846** | **UNLEARNED (Corpus Scarcity)** |

---

## 3. Findings & Detailed Domain Analysis

1. **Held-Out English Statutes (DPDP & Limitation Act):**  
   The model achieves a loss of **5.6911 (PPL 296.21)**, outperforming random guessing by nearly $2.0$ loss points. Because neither the DPDP Act nor the Limitation Act appeared in the training or validation sets, this proves that the model has acquired generalizable knowledge of Indian statutory drafting conventions, legal syntax, and punctuation.
2. **Held-Out Judicial Precedent (Arjun Khotkar):**  
   The model achieves a loss of **5.8787 (PPL 357.33)** on the Supreme Court judgment on Section 65B electronic records, confirming transfer to complex judicial phrasing and ratio drafting.
3. **Bilingual Statutory Queries & Citations:**  
   On mixed English-Hindi procedural queries (e.g., `"Whether Section 482 of CrPC / धारा 528 BNSS allows quashing..."`), the model achieves a loss of **6.6705 (PPL 788.79)** ($\Delta = -0.9541$), demonstrating coherent next-token modeling across script transitions.
4. **Held-Out Hindi Statutes (IT Act 2000 Hindi):**  
   The model exhibits a loss of **8.0093 (PPL 3,008.72)** on held-out Hindi IT Act text. This reflects the severe deficit of Hindi training data (only 4,306 Hindi training tokens vs 332k English tokens). While the tokenizer parses Hindi flawlessly without `<unk>` tokens, the 1M model cannot generalize to unseen Hindi legal vocabulary without expanding the pretraining corpus.

---

## 4. Strict Legal Trust Boundaries & Non-Negotiable Safeguards

> [!CAUTION]
> **Next-Token Probability Prediction is NOT Legal Reasoning:**  
> A cross-entropy loss reduction on held-out statutes demonstrates statistical learning of legal vocabulary and grammar. It does **NOT** prove legal reasoning, factual correctness, temporal accuracy, or statutory interpretation.

### Non-Negotiable Operating Invariants:
1. **Never Connect Experimental Model Directly to Client Legal Answers:** The original model must remain an isolated research component. It must NEVER generate ungrounded legal counsel or advice.
2. **Authoritative Grounding Rests Exclusively with RAG:** All legal answers delivered to users must continue to be generated through LegalMitra's deterministic RAG pipeline, backed by SQLite full-text search, temporal law validation, and verified advocate review.
3. **No Zero-Hallucination Claims:** Next-token language models inherently predict probability distributions over tokens; hallucination prevention is achieved through strict context grounding, citation verification, and explicit refusal on unsupported premises.

