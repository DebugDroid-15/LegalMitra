# LegalMitra Phase 32: Reproducible Training Experiments

**Phase:** 32 — Original Foundation Model Validation, Data Integrity & Generalization Gate  
**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Owner:** Team Shatrujeet  
**Date:** 2026-10-18  
**Classification:** Proprietary and Confidential  

---

## 1. Executive Summary

Phase 32 authored and executed a reproducible scientific experiment runner in `scripts/run_model_experiments.py`.

Six controlled experiments were conducted on the local NVIDIA GeForce RTX 2050 GPU, systematically investigating baseline reproduction, multi-seed stability, overfitting trajectories, memorization dynamics, split-strategy data leakage, and context-length scaling.

---

## 2. Experimental Results Ledger

All metrics recorded in `data/20_evaluation/model_experiment_results_v1.json`:

### Experiment 1: Baseline Prototype Reproduction
- **Objective:** Independently reproduce the 938,752-parameter prototype and 50-step training trajectory with separate train and validation tracking.
- **Hardware:** NVIDIA GeForce RTX 2050 Laptop GPU (CUDA 11.8).
- **Batch Size / Seq Len:** 8 / 128 tokens (tokens processed: 51,200).
- **Wall-Clock Duration:** **1.60 seconds** (Throughput: **32,000 tokens/second**).
- **Initial Training Loss:** `6.9647` $\rightarrow$ **Final Training Loss:** `5.6504` ($\Delta = -1.3143$).
- **Initial Validation Loss:** `6.9328` $\rightarrow$ **Final Validation Loss:** `5.8974` ($\Delta = -1.0354$).
- **Reproduced Checkpoint:** `research/original_model/checkpoints/exp1_reproduced_step50.pt` (SHA-256: `9fa24b4e...`).
- **Verdict:** **REPRODUCED & VALIDATED**. Both training and held-out validation loss decrease monotonically.

---

### Experiment 2: Multi-Seed Reproducibility Validation
- **Objective:** Evaluate if loss reduction is an artifact of seed 42 or holds across independent seeds.
- **Seeds Evaluated:** 42, 43, 44 (30 steps each):

| Random Seed | Initial Train Loss | Final Train Loss | Loss Reduction | Held-Out Val Loss |
|---|---|---|---|---|
| **Seed 42** | 6.9550 | 6.1470 | **-0.8080** | 6.1762 |
| **Seed 43** | 6.9741 | 6.1053 | **-0.8688** | 6.1654 |
| **Seed 44** | 6.9509 | 6.1629 | **-0.7880** | 6.1841 |
| **Mean** | **6.9600** | **6.1384** | **-0.8216** | **6.1752** |

- **Verdict:** **HIGHLY REPRODUCIBLE**. Variance across random seeds is under $0.05$ loss points.

---

### Experiment 3: Overfitting Diagnostic (100 Steps Trajectory)
- **Objective:** Detect whether training loss continues to drop while validation loss diverges (overfitting).
- **Trajectory Measured:**

```mermaid
xychart-beta
    title "100-Step Training vs Validation Loss"
    x-axis ["Step 10", "Step 25", "Step 50", "Step 75", "Step 100"]
    y-axis "Cross Entropy Loss" 5.0 --> 7.0
    line [6.58, 6.28, 5.83, 5.64, 5.46]
    line [6.57, 6.25, 5.93, 5.76, 5.61]
```

| Step | Training Loss | Held-Out Validation Loss | Generalization Gap |
|---|---|---|---|
| **Step 10** | 6.5834 | 6.5666 | -0.0168 |
| **Step 25** | 6.2797 | 6.2507 | -0.0290 |
| **Step 50** | 5.8328 | 5.9291 | +0.0963 |
| **Step 75** | 5.6375 | 5.7554 | +0.1179 |
| **Step 100**| 5.4648 | 5.6117 | +0.1469 |

- **Verdict:** **NO OVERFITTING AT 100 STEPS**. Validation loss drops from 6.5666 down to 5.6117 without plateauing or diverging. The model is steadily acquiring generalizable corpus statistics.

---

### Experiment 4: Memorization Capacity on Controlled Small Corpus
- **Objective:** Prove whether the architecture possesses the expressive capacity to memorize legal text to near-zero loss.
- **Corpus:** 5 fixed statutory chunks over 100 steps with learning rate $1 \times 10^{-3}$.
- **Memorization Loss:** `6.9539` $\rightarrow$ **`1.1184`** ($\Delta = -5.8355$, an **83.9% loss drop**).
- **Held-Out Generalization Loss:** `6.6543`.
- **Finding:** The transformer architecture has ample expressive capacity to memorize legal syntax. However, small-corpus memorization does not transfer to unseen text, proving memorization is completely distinct from generalization.

---

### Experiment 5: Split Strategy Ablation (Group-Aware vs Sequential)
- **Objective:** Quantify the optimistic bias caused by intra-document IT Act leakage in the sequential split.
- **Group-Aware Validation Loss (Zero Overlap):** `5.8974`
- **Sequential Validation Loss (With IT Act Leakage):** `5.8523`
- **Observed Bias:** Sequential split exhibits a $+0.0451$ artificially lower validation loss.
- **Conclusion:** Group-aware splitting is mandatory to prevent false optimism.

---

### Experiment 6: Context-Length Scaling & Hardware Sizing
- **Objective:** Measure memory and throughput as sequence length scales on the local RTX 2050 GPU:

| Sequence Length ($T$) | Trainable Parameters | Peak GPU VRAM | Throughput |
|---|---|---|---|
| **$T = 64$** | 930,560 | 124.63 MB | 39,912.5 tokens/sec |
| **$T = 128$** | 938,752 | 142.64 MB | 99,049.8 tokens/sec |
| **$T = 256$** | 955,136 | 243.82 MB | 138,681.5 tokens/sec |

- **Finding:** Peak memory remains under 250 MB VRAM even at $T=256$, leaving ample headroom for larger batch sizes.

