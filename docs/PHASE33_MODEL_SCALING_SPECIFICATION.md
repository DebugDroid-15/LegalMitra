# LegalMitra Phase 33: Model Scaling Architecture Specification

**Status:** `VERIFIED`  
**Execution Date:** 2026-10-18  
**Architecture Implementation:** `research/original_model/model.py`  
**Evaluation Script:** `scripts/profile_compute_feasibility.py`  

---

## 1. Executive Summary

Phase 33 evaluated the architectural scaling design of LegalMitra's decoder-only causal Transformer across three precise configurations:
1. **Prototype Configuration (~1.09M parameters)**: Tiny baseline research architecture.
2. **Intermediate Configuration (~4.50M parameters)**: Mid-tier scaling model.
3. **Target 10M Configuration (~10.55M parameters)**: Target multi-head transformer.

All architectures adhere strictly to the original foundation model mandate: zero pretrained weights, zero imported embeddings, causal self-attention, and random Gaussian weight initialization $\mathcal{N}(0, 0.02^2)$.

---

## 2. Model Family Hyperparameters & Parameter Accounting

| Architectural Parameter | Prototype (~1M) | Intermediate (~4.5M) | Target (~10.5M) |
|---|---|---|---|
| **Vocabulary Size ($V$)** | 2,048 | 2,048 | 2,048 |
| **Model Dimension ($d_{\text{model}}$)** | 128 | 256 | 320 |
| **Transformer Layers ($L$)** | 4 | 5 | 8 |
| **Attention Heads ($H$)** | 4 | 4 | 8 |
| **Head Dimension ($d_{\text{head}}$)** | 32 | 64 | 40 |
| **Feed-Forward Dimension ($d_{\text{ff}}$)** | 512 ($4 \times d$) | 1,024 ($4 \times d$) | 1,280 ($4 \times d$) |
| **Max Sequence Length ($T_{\text{max}}$)** | 128 / 256 | 128 / 256 | 128 / 256 |
| **Dropout Rate** | 0.1 | 0.1 | 0.1 |
| **Weight Tying** | True (`lm_head.weight = tok_embeddings.weight`) | True | True |
| **Token Embedding Parameters** | 262,144 | 524,288 | 655,360 |
| **Positional Embedding Parameters**| 32,768 | 65,536 | 81,920 |
| **Per-Block Attention Parameters**| 65,536 | 262,144 | 409,600 |
| **Per-Block MLP Parameters** | 131,712 | 525,568 | 819,200 |
| **Total Measured Trainable Params**| **1,069,824** | **4,501,248** | **10,550,400** |

---

## 3. Strict Original Initialization Verification

Every configuration is initialized from scratch:
- **Linear Layers:** Weights sampled from Gaussian distribution with mean $0.0$ and standard deviation $0.02$. Biases initialized to zero.
- **Embedding Layers:** Random normal $\mathcal{N}(0, 0.02^2)$.
- **LayerNorm Layers:** Weights initialized to $1.0$, biases initialized to $0.0$.
- **Attention Masking:** Strictly causal lower-triangular mask buffer, preventing information flow from token $t+k$ to token $t$.
- **Loss Computation:** Next-token cross-entropy loss with explicit target sequence shifting (`logits[..., :-1, :]` vs `labels[..., 1:]`) and `ignore_index = pad_token_id` to eliminate artificial padding-induced loss reduction.

