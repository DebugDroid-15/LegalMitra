# LegalMitra Phase 32: Generalization Evaluation & Capabilities Assessment

**Phase:** 32 — Original Foundation Model Validation, Data Integrity & Generalization Gate  
**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Owner:** Team Shatrujeet  
**Date:** 2026-10-18  
**Classification:** Proprietary and Confidential  

---

## 1. Executive Summary

Phase 32 answered the primary research question set by project governance:
> **Does the original model learn generalizable language and legal-text structure, or is the current result only evidence that the code executes and the training loss decreases?**

Using the evaluation harness in `scripts/evaluate_generalization.py`, the model was tested on unseen, held-out documents, judicial precedents, and multilingual text.

The empirical answer is nuanced and rigorous:
1. **Statistically Significant English Legal Language Learning:** On held-out English statutes and judicial precedents that the model never saw during training, it achieves cross-entropy loss of **6.0054 (PPL: 405.61)**, decisively beating the theoretical random guessing baseline (**6.9315, PPL: 1024**) by **0.9261 loss points**.
2. **Failure on Devanagari / Hindi:** On Hindi legal text (`धारा 528`), loss rises to **7.8277 (PPL: 2509.15)** because the pretraining chunks in Phase 31 were exclusively in English.
3. **No Legal Reasoning Capability:** A 0.94M parameter causal model is a language-modeling prototype. It cannot perform multi-step statutory deduction, identify conflicts of law, or provide reliable legal advice.

---

## 2. Empirical Generalization Matrix

All evaluations recorded in `data/20_evaluation/generalization_eval_results_v1.json`:

| Evaluation Target | Evaluated Text Description | Cross-Entropy Loss | Perplexity (PPL) | Delta vs Random Baseline |
|---|---|---|---|---|
| **Uniform Random Baseline** | Uninformed random guessing across $V=1,024$ | **6.9315** | 1,024.00 | $0.0000$ (Reference) |
| **Held-Out Statutes** | Unseen DPDP Act 2023 & Limitation Act 1963 chunks | **6.0054** | **405.61** | **-0.9261 (Learned)** |
| **Judicial Precedents** | Supreme Court judgments (Bhajan Lal, Arnesh Kumar) | **6.0776** | **435.98** | **-0.8539 (Learned)** |
| **English Legal Queries** | High Court quashing & arbitration annulment text | **6.1158** | **452.96** | **-0.8157 (Learned)** |
| **Rare Legal Terms** | *Res judicata pro veritate*, *writ of certiorari* | **6.2448** | **515.33** | **-0.6867 (Learned)** |
| **Mixed English-Hindi Text**| English legal queries with embedded `धारा 482` | **6.3886** | **595.02** | **-0.5429 (Learned)** |
| **Pure Devanagari Hindi Text**| Pure Hindi statutory definitions (`भारतीय नागरिक सुरक्षा...`) | **7.8277** | **2,509.15** | **+0.8962 (Unlearned)** |
| **Malformed / OOD Inputs** | Repeated punctuation, scrambled tokens | **6.4912** | **659.32** | Stable (No numerical divergence) |

---

## 3. Analysis of Capabilities & Limitations

### 3.1 What the Prototype Has Learned
- **Subword Legal Grammar:** Predicts legal tokens ("Section", "Act", "Court", "2023", "punishable") with significantly higher probability than random distribution.
- **Syntactic Structuring:** Learns punctuation transitions (parentheses around subsection numbers, periods following Act names).
- **In-Domain Transfer:** Outperforms random baseline on statutory texts from Acts not seen in training (e.g. DPDP Act), proving the subwords capture general statutory English rather than rote chunk memorization.

### 3.2 What the Prototype Has NOT Learned
- **Devanagari Transition Probabilities:** Because base characters were unseeded in Phase 31 training, the model treats Hindi as out-of-distribution noise.
- **Legal Answer Generation:** Next-token cross-entropy is completely separate from question answering. Generative sampling produces repetitive statutory fragments, not coherent legal counsel.
- **Factual Truth / Statutory Pinpointing:** It cannot distinguish whether a section has 3 subsections or 4 without grounding retrieval.

---

## 4. Governance Implications: Gate Ruling

- **Prototype Correctness:** **VERIFIED (GO)**. The architecture executes backpropagation, respects causal boundaries, and minimizes cross-entropy.
- **Generalization Gate:** **PARTIAL (CONDITIONAL)**. Generalizes to unseen English statutory syntax, but fails on Devanagari and lacks reasoning capacity.
- **Scaling Readiness:** **STRICT NO-GO FOR 125M / 1.3B PRETRAINING**. The model must not be scaled to 125M until the training dataset is expanded to include bilingual Hindi-English corpora and advocate-verified instruction datasets.

