# LegalMitra Phase 34: Data Volume Milestones & Foundation Model Scaling Gates

**Status:** `VERIFIED`  
**Execution Date:** 2026-10-18  

---

## 1. Executive Summary

Phase 34 establishes strict, empirical data volume milestones and architectural scaling gates for training LegalMitra's original Indian legal language models.

We explicitly reject arbitrary scaling of parameter counts without the necessary training data. Increasing model size on an under-sized corpus worsens validation loss, accelerates memorization, and wastes compute.

---

## 2. Empirical Scaling Milestones & Token Budgets

Under Chinchilla scaling principles ($\text{Tokens} \approx 20 \times \text{Parameters}$):

| Model Scaling Tier | Target Parameters | Chinchilla Optimal Tokens | Available Verified Tokens in Repo | Data Deficit Ratio | Local Feasibility (RTX 2050 4GB) | Scaling Gate Verdict |
|---|---|---|---|---|---|---|
| **Tier 1: Prototype** | 1,069,824 (~1.07M) | 21,396,480 (~21.4M) | 342,965 tokens | **62.4x deficit** | Fully Feasible (Peak VRAM 112.9 MB) | **GO for Architectural Research** |
| **Tier 2: Intermediate** | 4,501,248 (~4.50M) | 90,024,960 (~90.0M) | 342,965 tokens | **262.5x deficit** | Fully Feasible (Peak VRAM 215.8 MB) | **CONDITIONAL GO for Capacity Ablations** |
| **Tier 3: Small-10M** | 10,550,400 (~10.55M)| 211,008,000 (~211.0M) | 342,965 tokens | **615.2x deficit** | Fits in VRAM (470.7 MB), but data-starved | **NO-GO for Full Pretraining** |
| **Tier 4: Base Foundation**| 125,000,000 (~125M) | 2,500,000,000 (~2.5B) | 342,965 tokens | **7,289x deficit** | Infeasible (OOM / 38 days) | **STRICT NO-GO Locally & Without Data** |
| **Tier 5: Full Foundation**| 1,300,000,000 (~1.3B) | 26,000,000,000 (~26.0B)| 342,965 tokens | **75,809x deficit** | Infeasible (OOM / 412 days) | **STRICT NO-GO** |

---

## 3. Empirical Scaling Evidence from Phase 34 Runs

In our controlled 50-step runs on the expanded 342k-token corpus (`data/20_evaluation/model_experiment_results_v3.json`):
- **Prototype (1.07M params):** Final Train Loss = **5.7543** | Final Val Loss = **5.9969**
- **Intermediate (4.50M params):** Final Train Loss = **5.7379** | Final Val Loss = **6.0616**
- **Target 10M (10.55M params):** Final Train Loss = **5.8190** | Final Val Loss = **6.0903**

> **The Empirical Law of Under-Data Scaling:**  
> When the training token volume is constrained ($342\text{k tokens}$ for $10.55\text{M parameters} = 0.0325\text{ tokens/parameter}$), the 10.55M model achieves **WORSE validation loss** than the 1.07M model ($6.0903$ vs $5.9969$). The larger model has $10\times$ more degrees of freedom with insufficient data to constrain them, resulting in parameter under-determination.

### Non-Negotiable Gate Criteria
1. **Corpus Expansion Threshold for 10M Model:** Training the 10.55M model beyond short capacity checks is **STRICTLY BLOCKED** until the verified bilingual corpus exceeds **50,000,000 tokens** (~150x expansion).
2. **Hindi Production Pretraining Threshold:** Generalization to complex unconstrained Hindi legal drafting requires at least **10,000,000 authentic Hindi tokens** (current: 8,617 tokens).
3. **No Unapproved Cloud Compute:** All pretraining research must remain confined to local hardware without unapproved provisioning of third-party cloud instances.

