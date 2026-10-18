"""
README Builder - Part XII to Part XV:
- Part XII: Original Legal Language Model Research Track
- Part XIII: Custom Bilingual Tokenizer (Tokenizer v2) Architecture
- Part XIV: Training Data Governance, Split Integrity & Quarantine
- Part XV: Evaluation Framework, Benchmark v1–v9 & Metric Contracts
"""

def generate_part_12_to_15() -> str:
    sections = []

    # Part XII
    sections.append("""## Part XII: Original Legal Language Model Research Track

### 12.1 Motivation for an Original Indian Legal Foundation Model

While Track 1 utilizes evidential retrieval with commercial LLMs, true legal sovereignty and reliable long-term autonomy require foundation models trained natively on Indian legal language. Commercial models are fundamentally foreign to Indian statutory syntax, suffer severe token fragmentation on Indic scripts, and carry intellectual property encumbrances.

In Phase 31, Team Shatrujeet inaugurated the **Original Foundation Model Research Track**: constructing a decoder-only causal language model from scratch in PyTorch, with:
- Zero pretrained weights from HuggingFace, OpenAI, Meta, or Google.
- Zero pretrained word embeddings.
- Strict random weight initialization following $\\mathcal{N}(0, 0.02)$.
- Dedicated bilingual tokenizer trained exclusively on Indian legal corpora.

### 12.2 Causal Transformer Architecture & PyTorch Implementation

The architecture (`research/original_model/model.py`) implements a decoder-only causal Transformer optimized for high-throughput training on local workstations:

```text
Input Token Sequence [B, T]
         │
         ▼
[ Token Embedding (Vocab 2,048 -> d_model 128) ] + [ Positional Embedding (Max Seq 128/256) ]
         │
         ▼
[ Dropout (p = 0.1) ]
         │
         ▼
┌────────────────────────────────────────────────────────┐
│  TRANSFORMER BLOCK (Repeated N = 4 Layers)             │
│                                                        │
│  x ──► [ LayerNorm ] ──► [ Causal Multi-Head Attention ] ──(+)──► x1
│  │                                                       ▲
│  └───────────────────────────────────────────────────────┘
│                                                          │
│  x1 ──► [ LayerNorm ] ──► [ MLP: Linear 128->512->128 ] ──(+)──► x2
│  │                        (GELU Activation + Dropout)    ▲
│  └───────────────────────────────────────────────────────┘
└────────────────────────────────────────────────────────┘
         │
         ▼
[ Final LayerNorm (d_model 128) ]
         │
         ▼
[ Output Linear Head (d_model 128 -> Vocab 2,048) ] (Tied with Token Embedding)
         │
         ▼
Logits [B, T, Vocab 2,048] ──► CrossEntropyLoss(logits, targets)
```

#### Attention Formulation:
Multi-Head Attention projects queries, keys, and values across $h = 4$ heads with head dimension $d_k = 128 / 4 = 32$:
$$\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{Q K^T}{\\sqrt{d_k}} + M\\right) V$$
where $M$ is the upper-triangular causal mask ($M_{ij} = -\\infty$ for $j > i$ and $0$ for $j \\le i$).

### 12.3 Exact Parameter Accounting (1,069,824 Parameters)

Every parameter in the 1.07M model is mathematically accounted for:

```text
+----------------------------------------------------------------------------------------------------------------------+
|                                     1.07M TRANSFORMER PARAMETER BREAKDOWN                                            |
+-----------------------------------+------------------------------------------+------------------+--------------------+
| Subsystem Component               | Tensor Shape                             | Dimension Math   | Parameter Count    |
+-----------------------------------+------------------------------------------+------------------+--------------------+
| Token Embedding Table             | [vocab_size (2048), d_model (128)]       | 2,048 * 128      | 262,144            |
| Learned Positional Embedding      | [max_seq_len (256), d_model (128)]       | 256 * 128        | 32,768             |
| 4x Transformer Decoder Blocks:    |                                          |                  |                    |
|   • LayerNorm 1 (weight + bias)   | [128], [128]                             | 2 * 128 * 4      | 1,024              |
|   • Q Proj (Linear no bias)       | [d_model (128), d_model (128)]           | 128 * 128 * 4    | 65,536             |
|   • K Proj (Linear no bias)       | [d_model (128), d_model (128)]           | 128 * 128 * 4    | 65,536             |
|   • V Proj (Linear no bias)       | [d_model (128), d_model (128)]           | 128 * 128 * 4    | 65,536             |
|   • Out Proj (Linear no bias)     | [d_model (128), d_model (128)]           | 128 * 128 * 4    | 65,536             |
|   • LayerNorm 2 (weight + bias)   | [128], [128]                             | 2 * 128 * 4      | 1,024              |
|   • MLP Linear 1 (in_proj + bias) | [d_model (128), d_ff (512)], [512]       | (128*512+512) * 4| 264,192            |
|   • MLP Linear 2 (out_proj + bias)| [d_ff (512), d_model (128)], [128]       | (512*128+128) * 4| 262,656            |
| Final LayerNorm (weight + bias)   | [128], [128]                             | 2 * 128          | 256                |
| Output Projection Head            | [d_model (128), vocab_size (2048)]       | Tied to Embedding| 0 (Reused weights) |
+-----------------------------------+------------------------------------------+------------------+--------------------+
| TOTAL TRAINABLE PARAMETERS        |                                          |                  | 1,069,824 (1.07M)  |
+-----------------------------------+------------------------------------------+------------------+--------------------+
```

### 12.4 Empirical Pretraining Metrics & Loss Curves

The 1.07M model baseline was trained on Manifest v4 (`scripts/run_phase35_small_model_regression.py`) with complete seed reproducibility (Seed 42):
- **Optimizer**: AdamW ($\beta_1 = 0.9, \\beta_2 = 0.95, \\text{weight\\_decay} = 0.1, \\text{lr} = 3 \\times 10^{-4}$).
- **Batch Size**: 32 sequences (Sequence length 128 tokens).
- **Training Time**: 2.48 seconds for 50 steps on NVIDIA RTX 3050 Laptop GPU (CUDA).
- **Training Throughput**: **82,671.3 tokens / second**.
- **VRAM Utilization**: Peak VRAM 365.68 MB.
- **Initial Cross-Entropy Loss**:
  - Training Loss Step 0: $7.6468$ (Consistent with theoretical random guess $\\ln(2048) = 7.6246$).
  - Validation Loss Step 0: $7.6464$.
- **Final Cross-Entropy Loss (Step 50)**:
  - Training Loss Step 50: **$5.0069$** (Loss delta: $-2.6399$).
  - Validation Loss Step 50: **$5.6607$** (Loss delta: $-1.9858$).
- **Bitwise Checkpoint Reproducibility**:
  - Checkpoint saved to `research/original_model/checkpoints/phase35_1m_baseline_regression.pt`.
  - SHA-256: `984dc882c92bd7960f1af98e2e1c76cf03e00f675c5e9c65ffa5fcabe5256711`.
  - Independently re-evaluated in Phase 36: validation loss reproduced at exactly **$5.6607$** (`EXACT_MATCH`).

### 12.5 Chinchilla Scaling Heuristic & The 615x Token Deficit

In Phase 34 and Phase 35, Team Shatrujeet instituted a rigorous scientific gate governing when the model can be scaled from 1.07M to 10M+ parameters.
Under Hoffmann et al. (Chinchilla Scaling Laws, 2022), a causal language model requires approximately **20 tokens per parameter** for compute-optimal pretraining:
$$D_{\\text{optimal}} \\approx 20 \\times N$$

For our models:
1. **For the 1.07M Parameter Model**:
   $$D_{\\text{optimal}}(1.07\\text{M}) = 20 \\times 1,069,824 \\approx 21.4\\text{M tokens}$$
   - Active usable tokens in Manifest v4: **342,965 tokens**.
   - Deficit for 1.07M: $21,396,480 / 342,965 \\approx \\mathbf{62.4\\times \\text{ deficit}}$.
2. **For the Proposed 10.5M Parameter Model**:
   $$D_{\\text{optimal}}(10.5\\text{M}) = 20 \\times 10,550,000 \\approx 211\\text{M tokens}$$
   - Deficit for 10.5M: $211,000,000 / 342,965 \\approx \\mathbf{615.2\\times \\text{ deficit}}$.

> [!IMPORTANT]
> **GO/NO-GO SCALING GATE DECISION: HALTED (NO-GO)**
> Training a 10.5M parameter transformer on only 342K tokens results in catastrophic overfitting, validation loss divergence, and pure token memorization. In accordance with sound machine learning engineering, scaling to 10M parameters remains **gated** until national corpus acquisition expands the verified training dataset past 21.5M tokens (Milestone C).

---
""")

    # Part XIII
    sections.append("""## Part XIII: Custom Bilingual Tokenizer (Tokenizer v2) Architecture

### 13.1 Limitations of Standard Tokenizers on Indian Legal Text

Standard Byte-Pair Encoding (BPE) tokenizers (such as cl100k_base or LlamaTokenizer) treat Devanagari Hindi as an afterthought. Common Indian legal terms are fragmented into disjoint byte pairs:
- The word *"अधिनियम"* (Adhiniyam / Act) requires 6 to 8 tokens.
- The word *"उच्चतम न्यायालय"* (Supreme Court) requires 14 tokens.
This fragmentation destroys attention span, wastes compute, and produces severe cross-entropy loss spikes.

### 13.2 Byte-Pair Encoding Implementation & Byte Fallback

In Phase 33, Team Shatrujeet engineered `IndianLegalTokenizerV2` (`research/original_model/tokenizer_v2.py`), a sovereign bilingual BPE tokenizer featuring:
- **Base Character Coverage**: Complete ASCII printable character set + full Unicode Devanagari block (`\\u0900` to `\\u097F`).
- **Byte Fallback**: Any unseen Unicode character decomposes into its constituent UTF-8 hex bytes (`<0xE0>`, `<0xA4>`), guaranteeing **zero out-of-vocabulary (`<unk>`) errors**.
- **Special Tokens**:
  - `<pad>`: ID 0 (Padding token)
  - `<bos>`: ID 1 (Beginning of sequence)
  - `<eos>`: ID 2 (End of sequence)
  - `<unk>`: ID 3 (Unknown fallback)
  - `<mask>`: ID 4 (Mask token for bidirectional probes)

### 13.3 Vocabulary Construction & 1,811 Learned Merges

Tokenizer v2 was trained on the combined bilingual legal corpus:
- **Target Vocabulary Size**: 2,048 tokens.
- **Learned Merge Pairs**: 1,811 iteratively merged pairs.
- **Key Legal Vocabulary Merges**:
  - English: `"Section"`, `"Bharatiya"`, `"Nagarik"`, `"Suraksha"`, `"Sanhita"`, `"Court"`, `"Supreme"`, `"High"`, `"Procedure"`, `"Evidence"`, `"Arbitration"`.
  - Hindi: `"अधिनियम"` (Act), `"संहिता"` (Sanhita), `"न्यायालय"` (Court), `"धारा"` (Section), `"उच्चतम"` (Supreme), `"प्रक्रिया"` (Procedure), `"साक्ष्य"` (Evidence), `"जमानत"` (Bail).

### 13.4 Comparative Empirical Audit: Tokenizer v1 vs v2

An exhaustive empirical audit (`data/20_evaluation/tokenizer_v2_audit_results.json`) demonstrated massive performance gains over Tokenizer v1:

```text
+----------------------------------------------------------------------------------------------------------------------+
|                                    TOKENIZER V1 vs TOKENIZER V2 EMPIRICAL AUDIT                                      |
+----------------------------------------------+---------------------------+-------------------------------------------+
| Metric / Characteristic                      | Tokenizer v1 (Phase 31)   | Tokenizer v2 (Phase 33-36)                |
+----------------------------------------------+---------------------------+-------------------------------------------+
| Vocabulary Size                              | 1,024 tokens              | 2,048 tokens (+100% capacity)             |
| Learned BPE Merges                           | 933 merges                | 1,811 merges                              |
| Script Focus                                 | English Dominant          | Bilingual (English + Devanagari Hindi)    |
| Sample Text Characters                       | 736 characters            | 736 characters                            |
| Sample Text Words                            | 113 words                 | 113 words                                 |
| Total Generated Tokens                       | 402 tokens                | 238 tokens                                |
| Compression Ratio (Tokens / Word)            | 3.56 tokens / word        | 2.11 tokens / word                        |
| Overall Token Reduction                      | Baseline                  | 40.8% Reduction in Sequence Length        |
| Held-out English Unique Tokens Activated     | 337 unique tokens (32.9%) | 370 unique tokens (18.1%)                 |
| Held-out Hindi Unique Tokens Activated       | 14 unique tokens (1.37%)  | 190 unique tokens (9.28%)                 |
| Hindi Vocabulary Activation Expansion        | Baseline                  | 13.5x Increase in Unique Hindi Tokens     |
| Byte Fallback Support                        | No (Produced <unk>)       | Yes (100% UTF-8 Byte Coverage)            |
+----------------------------------------------+---------------------------+-------------------------------------------+
```

---
""")

    # Part XIV
    sections.append("""## Part XIV: Training Data Governance, Split Integrity & Quarantine

### 14.1 Dataset Manifest v4 Architecture

Pretraining data is managed through cryptographically verified manifests (`research/original_model/manifests/dataset_manifest_v4.json`). Every split is accompanied by an immutable SHA-256 digest:

```json
{
  "manifest_version": "v4.0.0",
  "created_at": "2026-10-18T16:12:24.781775",
  "tokenizer": "IndianLegalTokenizerV2 (vocab 2,048)",
  "total_passages": 1559,
  "total_usable_tokens": 342965,
  "en_tokens": 334348,
  "hi_tokens": 8617,
  "dataset_sha256": "15088ea8e24555478a54fcb7d44bddefe39a1370fe3597bb298d2e3511f3cc4e",
  "train_sha256": "cf3fc18f4bf87329e2f473ca49a9907fb2df16f86986cd1bc10ae98c06d0d822",
  "val_sha256": "2e96962c9859c3f7824093cd9d9b754f6c2fa6d07a02aeb8d3ffe906c4fbf118",
  "test_sha256": "818962fecbb7efafeddbf8080a7c3e2853a47bd38d9f28389c64e55e4abc0d23",
  "splits": {
    "train": { "passages": 1380, "tokens": 304291 },
    "val":   { "passages": 25,   "tokens": 3928 },
    "test":  { "passages": 154,  "tokens": 34746 }
  }
}
```

### 14.2 Source-Grouped Partitioning & Zero-Leakage Guarantee

Standard random chunk splitting leaks data between train and validation sets because adjacent sections of the same statute share structural phrasing, definitions, and terminology.
LegalMitra implements **Source-Grouped Partitioning** (`legalmitra/dataset/partitioner.py`):
1. Partitioning occurs at the **parent document / act level**.
2. If an Act (e.g., The Arbitration and Conciliation Act, 1996) is assigned to the Validation split, **100% of its provisions are allocated to Validation**.
3. Zero chunks from that Act may appear in Train or Test.
4. This guarantees that validation loss measures true generalization to unseen statutory enactments rather than memorization of adjacent sections.

### 14.3 Authentic Hindi Data Integration

Under Phase 34 and Phase 36, authentic primary-source Hindi legal texts were acquired from the Official Gazette of India and India Code:
- Authoritative Hindi translations of the Constitution of India (Article 394A).
- Authentic Hindi Gazette texts of the Bharatiya Nyaya Sanhita, 2023 and Bharatiya Nagarik Suraksha Sanhita, 2023.
- Combined authentic Hindi volume: **8,617 usable tokens** across 42 statutory passages.

### 14.4 Strict Quarantine Architecture (`IND-JUD-DEL-2024-BAIL`)

In Phase 8, a synthetic scaffold case (`IND-JUD-DEL-2024-BAIL`, 6 chunks) was created as a test fixture to validate pipeline error handling.
To protect production integrity, LegalMitra enforces a mathematical quarantine:
- **Database Quarantine Flag**: `is_synthetic_scaffold = 1` in `data/legalmitra_kb.db`.
- **RAG Filter**: Default SQL queries inject `WHERE is_synthetic_scaffold = 0`.
- **Pretraining Exclusion**: `training_exporter.py` strictly raises `QuarantineViolationError` if any chunk containing `IND-JUD-DEL-2024-BAIL` appears in pretraining candidate lists.
- **Verification Invariant**: `scripts/verify_freeze.py` asserts zero occurrences of the scaffold identifier across all frozen artifacts.

---
""")

    # Part XV
    sections.append("""## Part XV: Evaluation Framework, Benchmark v1–v9 & Metric Contracts

### 15.1 Evaluation Philosophy & The Benchmark Suite Evolution

Evaluation in LegalMitra is an empirical, contract-driven discipline. Over 36 phases, the evaluation benchmark evolved from an initial 20-case pilot to the comprehensive **Benchmark v9** containing 96 cases across 15 distinct categories:

```text
[ Phase 9: Pilot 20 ] ──► [ Phase 16: Benchmark v4 ] ──► [ Phase 24: Benchmark v7 ] ──► [ Phase 31: Benchmark v9 ]
  • 20 cases                 • 48 cases                   • 80 cases                   • 96 cases
  • Central Acts             • Central + Commercial       • Central + State + Precedents • 15 Failure Categories
```

### 15.2 Benchmark v9 Specification (96 Cases)

Benchmark v9 (`data/20_evaluation/evaluation_cases_v9.json`) exercises the entire spectrum of legal reasoning:

| Category Code | Category Description | Cases | Target Competency / Test Objective |
|:---|:---|:---:|:---|
| `single_provision` | Single-Provision Interpretation | 6 | Precise statutory analysis of an isolated section |
| `multi_provision` | Multi-Provision Synthesis | 7 | Cross-referencing sections across or within Acts |
| `statute_precedent_synthesis` | Statute & Case Law Synthesis | 7 | Harmonizing legislative text with judicial precedents |
| `overruled_precedent` | Overruled / Distinquished Caselaw | 6 | Detecting and refusing reliance on overruled law |
| `procedural_deadlines` | Procedural Timelines & Limitation | 6 | Computing statutory limitation periods under Limitation Act |
| `legal_remedies_steps` | Procedural Remedies & Step-by-Step| 6 | Formulating actionable legal procedural sequences |
| `multi_jurisdiction` | Multi-Jurisdictional Conflicts | 6 | Central vs State statutory precedence (List I vs II vs III) |
| `commencement_amendment`| Commencement & Amendment Timing | 7 | 2024 Criminal transition dates & amendment enforceability |
| `false_legal_premise` | Detection of False Legal Premises | 6 | Detecting impossible premises (e.g., anticipatory bail in trial) |
| `unanswerable_missing_evidence`| Unanswerable Questions / Abstention| 6 | Explicit abstention when knowledge base lacks evidence |
| `missing_ambiguous_facts`| Missing / Ambiguous Factual Probes| 7 | Prompting user for necessary factual clarifications |
| `multi_domain_scenario`| Complex Multi-Domain Scenarios | 7 | Intersecting criminal, corporate, and civil domains |
| `multi_turn_context` | Multi-Turn Conversational Retention| 7 | Maintaining statutory context across multi-turn sessions |
| `cautious_explanation` | Cautious Legal Nuance Explanation| 6 | Qualifying unsettled questions of law with neutrality |
| `adversarial_safety_bypass`| Adversarial Prompt Injection Defense| 6 | Defending against jailbreaks and statutory overrides |
| **TOTAL BENCHMARK V9**| **Exhaustive Evaluation Suite** | **96**| **Complete Legal AI Competency Matrix** |

### 15.3 The 15 Legal Question Evaluation Categories

Every case in Benchmark v9 contains:
- `eval_id`: Unique identifier (e.g., `V9-SING-001`, `V9-OVER-003`).
- `category`: One of the 15 categories above.
- `question`: Verbatim realistic legal query.
- `expected_type`: `affirmative_statute`, `abstention`, `clarification_prompt`, or `procedural_sequence`.
- `target_act_or_case`: Primary authoritative authority.
- `target_sections_or_paras`: Explicit statutory sections or judgment paragraphs.
- `golden_citations`: Mandatory citations that must appear in the answer.
- `forbidden_terms`: Prohibited terms that trigger immediate test failure.
- `should_abstain`: Boolean flag indicating whether the system must abstain.

### 15.4 Metric Contracts & Quality Gates

LegalMitra enforces 4 formal metric contracts across benchmark evaluations:

1. **Golden Citation Recall ($R_{\\text{citation}}$)**:
   $$R_{\\text{citation}} = \\frac{\\sum_{c \\in \\text{GoldenCitations}} \\mathbb{I}(c \\in \\text{GeneratedAnswer})}{|\\text{GoldenCitations}|}$$
   - Contract: Must achieve $\\ge 95\\%$ across affirmative cases. (Phase 30 Benchmark v8 achieved **100%**).
2. **Claim Grounding Support ($S_{\\text{claim}}$)**:
   $$S_{\\text{claim}} = \\frac{\\text{Supported Declarative Legal Claims}}{\\text{Total Declarative Legal Claims}}$$
   - Contract: Must achieve $\\ge 99.0\\%$. (Phase 30 achieved **668 / 669 claims = 99.85%**).
3. **Abstention Precision ($P_{\\text{abstain}}$)**:
   - For cases where `should_abstain == True` (unanswerable or false premise), the system must output an abstention signal.
   - Contract: Must achieve **100%** on unanswerable/false-premise test sets.
4. **Forbidden Terms Suppression**:
   - Zero occurrences of `forbidden_terms` permitted. Any single occurrence fails the evaluation run.

### 15.5 Automated Failure Attribution Engine

When an evaluation case fails, `legalmitra/evaluation/failure_attribution.py` automatically diagnoses the failure root cause into one of four attribution buckets:
1. `RETRIEVAL_MISS`: Target chunk was not retrieved in top-$K$.
2. `GROUNDING_SUPPRESSION`: Evidence was retrieved, but validator suppressed answer due to low confidence.
3. `LLM_HALLUCINATION`: Model introduced citations or assertions not present in retrieved chunks.
4. `TEMPORAL_CONFLATION`: Model referenced a repealed provision for a post-transition scenario.

---
""")

    return "\n".join(sections)
