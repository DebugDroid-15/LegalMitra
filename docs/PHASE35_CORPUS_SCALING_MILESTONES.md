# Phase 35 Corpus Scaling Milestones and Compute Feasibility Roadmap

**Project:** LegalMitra  
**Phase:** 35 — National Legal Data Engine, Source Verification & Corpus Scaling Infrastructure  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** VERIFIED  

---

## 1. Corpus Scaling Philosophy

Model scaling must never precede corpus readiness. In Phase 34, we identified that training a 10.55M-parameter causal transformer on a 342k token corpus resulted in **severe overfitting and validation loss degradation** compared to a 1.07M model. Under standard Chinchilla compute-optimal scaling ($N \approx 20D$), a 10.55M-parameter model requires approximately **211,000,000 tokens**.

Attempting to train large foundation models without lawful, verified pretraining corpora produces poor generation and severe hallucination risks.

---

## 2. Progressive Corpus Scaling Milestones

Phase 35 establishes 5 empirical milestones for national legal corpus expansion:

```
[Milestone A] (342k Tokens) - Current Baseline
      │
      ▼
[Milestone B] (1.0M Tokens) - Expanded Central & State Statutes + BNS/BNSS/BSA Hindi
      │
      ▼
[Milestone C] (10.0M Tokens) - Full Central Code + 28 States + High Court Precedents
      │
      ▼
[Milestone D] (50.0M Tokens) - Comprehensive National Statutory & Judicial Corpus
      │
      ▼
[Milestone E] (211.0M+ Tokens) - Chinchilla Compute-Optimal Pretraining Target
```

### Detailed Milestone Specifications:

| Milestone | Target Tokens | Current Eligible | Token Deficit | Primary Sources Required | Target Model Architecture |
|---|---|---|---|---|---|
| **Milestone A** | 342,965 | 342,965 | **0** (1.0x) | 33 Indexed Acts + Hindi Statutes | 1.07M Prototype |
| **Milestone B** | 1,000,000 | 342,965 | **657,035** (2.9x) | Ingest 10 Phase 35 candidates + BNS Hindi | 1.07M – 2.5M Baseline |
| **Milestone C** | 10,000,000 | 342,965 | **9,657,035** (29.1x) | Central Acts + 10 State Law Portals | 4.5M Intermediate |
| **Milestone D** | 50,000,000 | 342,965 | **49,657,035** (145.8x) | All 28 States + Delhi/Bombay/Calcutta HC | 10.55M (Provisional Gate) |
| **Milestone E** | 211,000,000 | 342,965 | **210,657,035** (615.2x) | Complete National Judicial Precedent Archive | 10.55M Compute-Optimal |

---

## 3. Local Hardware Constraints (RTX 2050 4GB)

Empirical execution tests on local development infrastructure:
- **1.07M Model:** 112.9 MB peak VRAM, 82,671 tokens/sec on CUDA. Highly feasible.
- **4.50M Model:** 215.8 MB peak VRAM, 14,024 tokens/sec on CUDA. Feasible.
- **10.55M Model:** 470.7 MB peak VRAM, 10,704 tokens/sec on CUDA. Physically fits in VRAM, but **training on <50M tokens is scientifically invalid due to data starvation**.
- **125M / 1.3B Models:** STRICT NO-GO. Would exceed local VRAM by 8x–30x and requires unapproved cloud infrastructure.
