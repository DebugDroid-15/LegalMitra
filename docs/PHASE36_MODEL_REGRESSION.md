# Phase 36 Small-Model Baseline Regression & Reproduction Report

**Project:** LegalMitra  
**Phase:** 36 — Corpus Eligibility Audit, Hindi Primary-Source Acquisition & Dataset Integrity  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** VERIFIED  

---

## 1. Executive Summary

Phase 36 independently verified the Phase 35 small-model baseline experiment (`LegalDecoderTransformer`, 1,069,824 parameters) using `scripts/reproduce_phase35_small_model_regression.py`.

The experiment verified checkpoint reload fidelity, state dict integrity, and evaluated loss on the held-out validation set (`val_manifest_v4.json`, 42 validation batches) without any optimization leakage from the test split.

---

## 2. Experimental Reproduction Results

Audit from `data/20_evaluation/model_regression_reproduction_phase36.json`:

```json
{
  "report_version": "v1.0.0",
  "audit_phase": 36,
  "checkpoint_file": "research\\original_model\\checkpoints\\phase35_1m_baseline_regression.pt",
  "checkpoint_sha256": "984dc882c92bd7960f1af98e2e1c76cf03e00f675c5e9c65ffa5fcabe5256711",
  "model_parameters": 1069824,
  "device": "cuda",
  "tokenizer": "IndianLegalTokenizerV2 (vocab 2,048)",
  "validation_samples": 42,
  "phase35_recorded_val_loss": 5.6607,
  "phase36_reproduced_val_loss": 5.6607,
  "val_loss_delta_vs_phase35": 0.0,
  "fidelity_status": "EXACT_MATCH"
}
```

### Detailed Parameter and Architecture Verification:
- **Architecture:** Causal Decoder-Only Transformer (`LegalDecoderTransformer`)
- **Total Parameters:** **1,069,824**
  - Token Embeddings: $2,048 \times 128 = 262,144$
  - Positional Embeddings: $128 \times 128 = 16,384$
  - Transformer Blocks (4 layers): 4 Multi-Head Attention + 4 Feed-Forward Networks = $791,296$
  - LayerNorms & LM Head (tied): LayerNorm weights + biases = $1,069,824$ total parameters.
- **Hardware & Runtime:** NVIDIA GeForce RTX 2050 (4GB VRAM, CUDA). Evaluation of all 42 validation batches completed in **0.263 seconds**.
- **Fidelity Status:** **EXACT_MATCH** ($\Delta = 0.0000$ vs reported validation loss of $5.6607$).

---

## 3. Pretraining Readiness Assessment

1. **Loss Decrease vs Legal Capability:** While the 1.07M model demonstrates causal next-token learning on legal vocabulary (training loss $7.65 \rightarrow 5.01$; val loss $7.65 \rightarrow 5.66$), **this does NOT imply legal reasoning capability**. A 50-step optimization run on 342k tokens merely proves pipeline functionality.
2. **Scaling Prohibition Reconfirmed:** Training runs for 10M, 50M, 125M, or 1.3B parameters remain **STRICTLY BLOCKED** until Milestone D (50M tokens) is achieved.
3. **Production Isolation:** The foundation model training code remains completely isolated from the production RAG engine (`legalmitra/rag/engine.py`), which continues to use grounded retrieval and verification safeguards.
