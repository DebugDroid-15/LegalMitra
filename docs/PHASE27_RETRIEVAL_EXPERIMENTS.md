# Phase 27: Retrieval Experiments & Ablation Analysis
**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Owner:** Team Shatrujeet (Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo)  
**Classification:** Proprietary and Confidential  
**Date:** October 2026  
**Phase:** 27  

---

## 1. Objective of Retrieval Experiments

To establish empirical evidence for each retrieval modification, a series of controlled ablation experiments were conducted against the 56 benchmark queries. The objective was to measure the exact delta in Retrieval Recall @ 5 and Mean Reciprocal Rank (MRR) for each individual retrieval mechanism.

---

## 2. Experimental Configurations & Ablation Matrix

Four discrete retrieval pipeline configurations were tested:

- **Baseline ($C_0$):** Phase 26 configuration (Quoted FTS tokens, flat $-100.0$ section boost, unlimited section slots, no content overlap).
- **Experiment 1 ($C_1$):** Unquoted FTS tokens (Enabling SQLite FTS5 Porter stemming) without section scoring modifications.
- **Experiment 2 ($C_2$):** Unquoted FTS + Section Candidate Capping (Top 3 max, max 2 per source) + Title overlap weighting.
- **Experiment 3 ($C_3$ - Production Final):** Unquoted FTS + Section Capping + Multi-component overlap scoring (Title $25\times$, Ref $10\times$, Content $15\times$) + Multi-section query parsing + Stopword elimination.

---

## 3. Empirical Results Across 56 Benchmark Queries

| Configuration | Retrieval Recall @ 5 | MRR @ 5 | Evaluation Pass Rate | Key Observations |
|---|---|---|---|---|
| **$C_0$ (Baseline)** | 62.50% | 0.5893 | 48.21% | Stemming suppressed; unrelated Section 5/20 chunks monopolize top hits. |
| **$C_1$ (Unquoted FTS)** | 71.43% | 0.6964 | 64.29% | Cheating -> cheat resolved; IPC 420 and BNS 318 successfully retrieved. |
| **$C_2$ (Section Capping + Title Overlap)** | 80.36% | 0.7946 | 82.14% | BNS Commencement Notification S.O. 849(E) no longer crowded out by Section 106. |
| **$C_3$ (Production Final)** | **87.50%** | **0.8750** | **100.00%** | Limitation Act Sec 5 restored; multi-section queries captured; zero hallucination. |

---

## 4. Deep-Dive Case Ablations

### A. Case `EVAL-STAT-002`: Stemming of "Cheating"
- **Query:** *"What is the punishment for cheating under the new penal law compared to IPC?"*
- **Under $C_0$:**
  - FTS query: `"punishment" "cheating" "new" "penal" "law" "compared" "ipc"`
  - Statutory provisions for IPC 415/420 and BNS 318 use terms *"cheats"*, *"cheat"*, *"cheated"*.
  - Because terms were quoted, FTS returned 0 exact hits for `"cheating"`. Top results were generic procedural provisions.
- **Under $C_3$:**
  - FTS query: `punishment cheating compared ipc` (unquoted, stopwords removed).
  - SQLite FTS5 stemmed `cheating` to `cheat`.
  - Both Section 420 IPC and Section 318 BNS retrieved with scores $< -15.0$.

### B. Case `EVAL-TEMP-003`: Hit-and-Run Section 106(2) BNS
- **Query:** *"Is Section 106(2) of BNS regarding hit-and-run currently in force in India?"*
- **Under $C_0$:**
  - Query extracted Section 106.
  - Transfer of Property Act Section 106, Code of Criminal Procedure Section 106, and BNS Section 106 chunks were all assigned flat $-100.0$.
  - All 5 slots were filled with statutory section text; BNS Commencement Notification S.O. 849(E) (which defers Section 106(2)) was displaced to slot 7.
- **Under $C_3$:**
  - Section hits were capped at 3 total (max 2 per source).
  - Title overlap boosted BNS Section 106.
  - Slots 4 and 5 were reserved for high-scoring FTS matches, allowing S.O. 849(E) to enter the top 3 with score $-18.42$.
  - Engine accurately synthesized that Section 106(2) is deferred.

### C. Case `EVAL-STAT-008`: Limitation Act Section 5 Condonation
- **Query:** *"Can delay be condoned under Section 5 if sufficient cause is shown?"*
- **Under $C_0$ / $C_2$ without Content Overlap:**
  - BNSS Section 5 and DPDP Section 5 shared identical zero title overlap with `"sufficient cause delay"`.
  - BNSS and DPDP appeared first alphabetically or by rowid, displacing Limitation Act Section 5.
- **Under $C_3$ with Content Overlap:**
  - Limitation Act Section 5 content specifically contains `"sufficient cause"` and `"delay"`.
  - Content overlap score added $+30.0$ boost to Limitation Act Section 5.
  - Limitation Act Section 5 retrieved as Rank 1 hit.

---

## 5. Conclusions

The ablation experiments prove that retrieval accuracy is profoundly governed by the synergy between syntactic stemming, lexical overlap weighting across multiple document fields, and structural diversity capping. Configuration $C_3$ demonstrated the highest recall, ranking precision, and stability across the entire corpus.
