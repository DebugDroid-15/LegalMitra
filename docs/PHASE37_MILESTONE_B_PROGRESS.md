# Phase 37 Milestone B Readiness & Scaling Gap Assessment

**Project:** LegalMitra  
**Phase:** 37 — Authorized National Corpus Acquisition, Hindi Legal Data Expansion & Milestone B Readiness  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** COMPLETED & VERIFIED  

---

## 1. Executive Summary

Milestone B defines the intermediate milestone toward training an original Indian legal foundation model: accumulating **1,000,000 verified, rights-cleared, bilingual legal tokens** with zero data leakage.

In accordance with Mandatory Rule 12, LegalMitra strictly prohibits fabricating token counts, synthesizing fictitious text, or bypassing portal security controls to falsely claim milestone achievement. This report provides an exact, transparent, and empirically measured accounting of current corpus volume against Milestone B and Chinchilla pretraining heuristics.

---

## 2. Milestone B Empirical Accounting

| Corpus Dimension | Phase 36 Baseline | Phase 37 Current Measured | Milestone B Target | Net Progress in Phase 37 | Remaining Milestone B Deficit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Total Verified Tokens** | 342,965 | **357,358** | 1,000,000 | +14,393 | **642,642 tokens (64.26% deficit)** |
| **Authentic Hindi Tokens** | 8,617 | **19,871** | 100,000 (target 10%) | +11,254 | **80,129 tokens deficit** |
| **English Tokens** | 334,348 | **337,487** | 900,000 (target 90%) | +3,139 | **562,513 tokens deficit** |
| **Total Passages** | 1,559 | **1,633** | ~4,500 | +74 | **~2,867 passages deficit** |
| **Training Eligible Sources** | 33 | **47** | 100 | +14 | **53 sources deficit** |

### Milestone B Progress Trajectory:
- **Baseline (Phase 36):** 34.30% of Milestone B reached.
- **Phase 37 Current:** **35.74% of Milestone B reached.**
- **Hindi Ratio:** Improved from 2.51% of corpus to **5.56% of corpus** (more than doubled).

---

## 3. Scaling Laws & Compute-Optimal Pretraining Feasibility

The Chinchilla scaling law (*Hoffmann et al., 2022*) establishes that compute-optimal pretraining requires approximately **20 tokens per model parameter**:

$$D_{\text{optimal}} \approx 20 \times N$$

| Model Architecture | Parameter Count ($N$) | Chinchilla Optimal Tokens ($D_{\text{optimal}}$) | Current Verified Corpus ($D = 357,358$) | Token Deficit Factor | Pretraining Feasibility Gate |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Prototype Transformer** | 938,752 (0.94M) | ~18.8 Million | 357,358 | **52.5x deficit** | EXPERIMENTAL REGRESSION ONLY |
| **Phase 35/37 Baseline** | 1,069,824 (1.07M) | ~21.4 Million | 357,358 | **59.9x deficit** | CONTROLLED REGRESSION ONLY |
| **Target Intermediate Model**| 10,550,000 (10.55M) | ~211.0 Million | 357,358 | **590.4x deficit** | **STRICT NO-GO** |
| **Standard Small LLM** | 125,000,000 (125M) | ~2.50 Billion | 357,358 | **6,995x deficit** | **STRICT NO-GO** |
| **Production Foundation LLM** | 1,300,000,000 (1.3B) | ~26.0 Billion | 357,358 | **72,756x deficit** | **STRICT NO-GO** |

---

## 4. Architectural Pretraining Gate Decision

1. **Large-Scale Pretraining Remains STRICT NO-GO:** Training a 10M, 50M, 125M, or 1.3B parameter model on 357,358 tokens guarantees severe catastrophic overfitting, zero out-of-distribution generalization, and extreme memorization.
2. **Small-Model Baseline Validated:** The 1.07M parameter model trained for 50 steps achieves stable loss reduction (from 7.6451 to 5.0750 train loss, and 5.8831 validation loss) without divergent gradients, serving as our empirical architectural baseline.
3. **Data Acquisition Must Precede Model Scaling:** Engineering priority must remain exclusively focused on authorized corpus expansion until Milestone B (1,000,000 tokens) and subsequent pretraining data milestones (20M+ tokens) are reached.

