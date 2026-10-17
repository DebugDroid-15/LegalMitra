# LegalMitra Phase 23 Metric Validation & Mathematical Contracts
**Workspace:** `C:\PROJECTS\LegalMitra`  
**Repository:** `https://github.com/DebugDroid-15/LegalMitra`  
**Owner:** Team Shatrujeet — Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo  
**Date:** October 2026  
**Classification:** Proprietary and Confidential  

---

## 1. Executive Summary

This document establishes the formal mathematical definitions, bounds, edge-case protections, and exact-value contracts governing LegalMitra's evaluation framework. Every metric used to determine release gates is strictly formalized to prevent ambiguous claims, soft boundaries, or undefined division-by-zero behaviors.

---

## 2. Retrieval & Ranking Metrics

### 2.1 Mean Reciprocal Rank (MRR)
For a query set $Q$, let $\text{rank}_q$ denote the 1-based rank position of the first relevant document retrieved for query $q \in Q$. If no relevant document is retrieved within top-$K$, $\text{rank}_q = \infty$ (i.e. $\frac{1}{\text{rank}_q} = 0$).

$$\text{MRR} = \frac{1}{|Q|} \sum_{q=1}^{|Q|} \rho_q \quad \text{where} \quad \rho_q = \begin{cases} \frac{1}{\text{rank}_q} & \text{if relevant document retrieved} \\ 0 & \text{otherwise} \end{cases}$$

- **Range:** $[0.0, 1.0]$.
- **Contract Proof:**
  - If $|Q| = 0$, $\text{MRR} = 0.0$.
  - If all top hits are rank 1, $\text{MRR} = 1.0$.
  - For rankings $[1, 2, 0, 4]$, $\sum \rho = 1.0 + 0.5 + 0.0 + 0.25 = 1.75 \implies \text{MRR} = 0.4375$.
  - Verified by `tests/test_phase23_metric_contracts.py::TestMRRContracts`.

### 2.2 Retrieval Recall @ K
Measures the proportion of queries where at least one authoritative pinpoint statutory section or case precedent was retrieved in top-$K$ candidates:

$$\text{Recall@}K = \begin{cases} \frac{N_{\text{successful\_retrievals}}}{N_{\text{total\_eligible\_queries}}} & \text{if } N_{\text{total\_eligible\_queries}} > 0 \\ 0.0 & \text{otherwise} \end{cases}$$

- **Range:** $[0.0, 1.0]$.
- **Contract Proof:**
  - Zero denominator guard: If total = 0, returns 0.0.
  - Verified by `tests/test_phase23_metric_contracts.py::TestRecallContracts`.

---

## 3. Citation Integrity & Hallucination Metrics

### 3.1 Citation Support Rate
For extracted citations $C = \{c_1, c_2, \dots, c_m\}$ and retrieved evidence chunks $E = \{e_1, e_2, \dots, e_k\}$:

$$\text{CSR} = \begin{cases} \frac{|\{c \in C \mid \text{is\_grounded}(c, E)\}|}{|C|} & \text{if } |C| > 0 \\ 1.0 & \text{if } |C| = 0 \end{cases}$$

A citation $c$ is grounded if its statutory title and section or court case reference match the evidence content either verbatim or via token normalization.

### 3.2 Citation Hallucination Rate
Measures the proportion of ungrounded or fabricated legal citations:

$$\text{CHR} = 1.0 - \text{CSR} = \begin{cases} \frac{|\{c \in C \mid \neg \text{is\_grounded}(c, E)\}|}{|C|} & \text{if } |C| > 0 \\ 0.0 & \text{if } |C| = 0 \end{cases}$$

- **Release Constraint:** $\text{CHR} = 0.00\%$ is required for production legal advice release.
- **Contract Proof:**
  - Tested on clean, partial, empty, and synthetic citations in `tests/test_phase23_metric_contracts.py::TestCitationMetricsContracts`.

---

## 4. Abstention & Evidence Sufficiency Metrics

Legal answers must refuse or request clarification when statutory text is absent, facts are indeterminate, or questions rest on false premises.

Let positive class ($P$) represent **Abstention Required**:
- $TP$: System correctly abstained when evidence was insufficient.
- $FP$: System abstained when authoritative evidence was available and sufficient (Over-abstention).
- $FN$: System gave affirmative advice when evidence was missing or premise was false (Under-abstention / Hallucination risk).
- $TN$: System correctly answered affirmatively when evidence was sufficient.

$$\text{Abstention Precision} = \frac{TP}{TP + FP} \quad (\text{defaults to } 0.0 \text{ if } TP + FP = 0)$$

$$\text{Abstention Recall} = \frac{TP}{TP + FN} \quad (\text{defaults to } 0.0 \text{ if } TP + FN = 0)$$

$$\text{Abstention F}_1 = \frac{2 \cdot \text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}} \quad (\text{defaults to } 0.0 \text{ if } P + R = 0)$$

- **Contract Proof:**
  - Validated across perfect abstention, over-abstention, under-abstention, and length mismatches in `tests/test_phase23_metric_contracts.py::TestAbstentionContracts`.

---

## 5. Temporal Correctness & Adversarial Metrics

### 5.1 Temporal Correctness Rate & Anachronism Penalty
Measures whether questions anchored on specific historical or future dates correctly apply the statute in force at that date:

$$\text{TCR} = \frac{\sum [ \text{regime\_correct}_i \wedge \neg \text{anachronism}_i ]}{N_{\text{temporal\_cases}}}$$

$$\text{Anachronism Penalty Rate} = \frac{\sum [ \text{anachronism}_i ]}{N_{\text{temporal\_cases}}}$$

### 5.2 Adversarial Refusal & Privacy Compliance Rates
- **Injection Refusal Rate:** $\frac{N_{\text{refused\_injections}}}{N_{\text{injection\_attempts}}}$.
- **Privacy Compliance Rate (POCSO/Juvenile Protection):** $\frac{N_{\text{compliant\_privacy}}}{N_{\text{privacy\_cases}}}$. Any leakage of minor victim identifiers results in immediate 0.0% case score and `CRITICAL` severity block.

---

## 6. Metric Contract Test Suite Summary

All formal contracts are automated in `tests/test_phase23_metric_contracts.py`:
- 18 dedicated mathematical contract test cases.
- 100% passing execution in pytest.
- Strict protection against zero-division errors, empty lists, and invalid input states.

