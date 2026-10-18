# Phase 35 Small-Model Baseline Regression Results

**Project:** LegalMitra  
**Phase:** 35 — National Legal Data Engine, Source Verification & Corpus Scaling Infrastructure  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** VERIFIED  

---

## 1. Experiment Objective & Protocol

Workstream I requires executing a small-model regression experiment on the verified v4 pretraining manifests using the 1,069,824-parameter baseline transformer (`LegalDecoderTransformer`).

The objective is to establish that:
1. The model code and tokenization pipeline remain stable and free of regressions.
2. The model exhibits consistent causal convergence on the bilingual pretraining dataset.
3. Training loss decreases measurably without diverging or generating NaN loss values.
4. Checkpoints serialize deterministically and match state dict reload checks.

---

## 2. Experimental Setup

- **Model:** `LegalDecoderTransformer`
  - Vocabulary Size: 2,048 (`IndianLegalTokenizerV2`)
  - Hidden Dimension ($d_{\text{model}}$): 128
  - Layers ($n_{\text{layers}}$): 4
  - Attention Heads ($n_{\text{heads}}$): 4
  - Context Window ($max\_seq\_len$): 128
  - Total Parameters: **1,069,824**
- **Optimizer:** AdamW ($lr = 10^{-3}$, weight decay $= 0.01$, gradient clipping $= 1.0$)
- **Batch Size:** 32
- **Hardware:** NVIDIA GeForce RTX 2050 (4GB VRAM, CUDA 12.x)
- **Random Seed:** 42

---

## 3. Measured Training Results

Audit from `data/20_evaluation/model_experiment_results_v4.json`:

```json
{
  "report_version": "v4.0.0",
  "phase": 35,
  "model_name": "LegalDecoderTransformer-1.07M",
  "parameters": 1069824,
  "seed": 42,
  "steps": 50,
  "initial_train_loss": 7.6468,
  "final_train_loss": 5.0069,
  "initial_val_loss": 7.6464,
  "final_val_loss": 5.6607,
  "train_loss_delta": -2.6399,
  "val_loss_delta": -1.9857,
  "tokens_per_second": 82671.3,
  "total_time_seconds": 2.48,
  "peak_vram_mb": 113.4,
  "checkpoint_file": "research\\original_model\\checkpoints\\phase35_1m_baseline_regression.pt",
  "checkpoint_sha256": "4fea1cfa191c2f0705d0f2bae9b8bac45082c38db9d9eabddd84280cd0764832",
  "device": "cuda",
  "manifest_ref": "research\\original_model\\manifests\\dataset_manifest_v4.json"
}
```

### Key Findings:
1. **Convergence:** Train loss reduced from 7.6468 to 5.0069 ($\Delta = -2.6399$), while held-out validation loss decreased from 7.6464 to 5.6607 ($\Delta = -1.9857$).
2. **Execution Speed:** 50 steps completed in 2.48 seconds on CUDA with a throughput of 82,671.3 tokens/second.
3. **Memory Footprint:** Peak VRAM consumption was 113.4 MB, demonstrating high local computational efficiency.
4. **Isolation:** The foundation model training code remains completely isolated from the production RAG path (`legalmitra/api/routes.py`, `legalmitra/rag/engine.py`).
