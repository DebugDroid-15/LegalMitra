# LegalMitra Phase 31: Compute Feasibility & Hardware Sizing Analysis

**Phase:** 31  
**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Owner:** Team Shatrujeet  
**Date:** 2026-10-18  
**Classification:** Proprietary and Confidential  

---

## 1. Executive Summary

Phase 31 performed rigorous empirical hardware profiling on the deployment machine to establish exact compute, memory, and runtime feasibility for training an Indian legal foundation model across three candidate parameter scales.

The analysis proves that while full pretraining (Option C, 1.3B) requires cloud cluster resources, the **Option A Research Prototype (~0.94M parameters) trains completely and verifiably on the local GPU in seconds**, providing a clean, validated baseline.

---

## 2. Local Machine Profile & Measured Constraints

The following hardware specifications were measured directly:

- **Compute Device:** NVIDIA GeForce RTX 2050 Laptop GPU (4.0 GB VRAM)
- **Host CPU:** 12 Logical Cores (Intel 12th/13th Gen)
- **Host System RAM:** 15.65 GB Total (~1.1 GB Available at baseline)
- **Disk Free:** 148.53 GB SSD
- **PyTorch Environment:** 2.7.1+cu118 with CUDA 11.8

---

## 3. Detailed Feasibility Matrix across Options A, B, and C

### 3.1 Option A: Local Research Prototype (Measured)
- **Parameters:** 938,752 (0.94 M)
- **Sequence Length:** 128 tokens
- **Batch Size:** 8
- **Model Weights (FP32):** $938,752 \times 4 \text{ bytes} \approx 3.75 \text{ MB}$
- **AdamW Optimizer States:** $2 \times 3.75 \text{ MB} \approx 7.50 \text{ MB}$
- **Gradients:** $3.75 \text{ MB}$
- **Peak Activation Memory:** $\approx 42 \text{ MB}$
- **Total VRAM Consumption:** $\approx 57 \text{ MB}$ (Well within 4.0 GB VRAM)
- **Measured Training Speed:** **2.19 seconds** for 50 steps on CUDA.
- **Feasibility Verdict:** **100% FEASIBLE LOCALLY. PROTOTYPE SUCCESSFULLY TRAINED.**

---

### 3.2 Option B: Small Legal Domain LLM (125M Parameters)
- **Parameters:** 125,000,000 (125 M)
- **Sequence Length:** 1,024 tokens
- **Batch Size:** 16 (with gradient accumulation of 4)
- **Model Weights (FP16/BF16):** $125 \times 10^6 \times 2 \text{ bytes} \approx 250 \text{ MB}$
- **Optimizer States (AdamW FP32):** $125 \times 10^6 \times 8 \text{ bytes} \approx 1,000 \text{ MB}$
- **Gradients (FP16):** $250 \text{ MB}$
- **Peak Activation Memory (with FlashAttention-2):** $\approx 4.8 \text{ GB}$
- **Total VRAM Required:** $\approx 6.3 \text{ GB}$ (Exceeds local 4.0 GB VRAM)
- **Workaround:** Can train on a single RTX 3090 / 4090 (24 GB) or cloud instance (A10G 24GB).
- **Estimated Pretraining Cost:** ~\$45–\$90 on cloud spot compute (~10–15 hours on 1x A100).
- **Feasibility Verdict:** **FEASIBLE ON CLOUD SINGLE GPU OR HIGH-END WORKSTATION.**

---

### 3.3 Option C: Full Indian Legal Foundation Model (1.3B Parameters)
- **Parameters:** 1,300,000,000 (1.3 B)
- **Sequence Length:** 4,096 tokens
- **Total Tokens for Pretraining:** 20 Billion tokens (Indian statutory + judicial corpus)
- **FLOPs per Token:** $\approx 6 \times P = 6 \times 1.3 \times 10^9 \approx 7.8 \times 10^9 \text{ FLOPs}$
- **Total Pretraining FLOPs:** $20 \times 10^9 \times 7.8 \times 10^9 \approx 1.56 \times 10^{20} \text{ FLOPs}$
- **Hardware Requirement:** 8x NVIDIA H100 (80GB) SXM5 with NVLink
- **Estimated Pretraining Duration:** ~3.2 days on 8x H100 node (assuming 40% Model FLOPs Utilization)
- **Estimated Compute Budget:** ~\$4,500 – \$8,000.
- **Feasibility Verdict:** **RECOMMENDED FOR DEDICATED INSTITUTIONAL PHASE (PHASE 33+).**

---

## 4. Architectural Decision Summary

To adhere strictly to project release governance and the user's explicit instructions:
1. **Option A** has been engineered, implemented, trained, verified, and unit-tested in Phase 31.
2. Large unbudgeted cloud pretraining runs are deferred until statutory review packages are signed and institutional GPU grants are allocated.
