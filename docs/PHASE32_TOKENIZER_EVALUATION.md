# LegalMitra Phase 32: Tokenizer Quality & Unicode Audit

**Phase:** 32 — Original Foundation Model Validation, Data Integrity & Generalization Gate  
**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Owner:** Team Shatrujeet  
**Date:** 2026-10-18  
**Classification:** Proprietary and Confidential  

---

## 1. Executive Summary

Phase 32 conducted an extensive empirical audit of the custom `IndianLegalTokenizer` (`research/original_model/tokenizer.py`), inspecting its vocabulary allocation, compression efficiency, legal token boundary preservation, Devanagari handling, and out-of-domain robustness.

The audit discovered that because Phase 31 trained BPE vocabulary solely on sampled English statutory chunks, **Devanagari characters were previously unseeded and defaulted to `<unk>` tokens**. Phase 32 remediated this by pre-seeding the complete ASCII and Devanagari Unicode blocks (`0x0900`–`0x097F`), achieving zero unknown-token collisions on Hindi legal text.

---

## 2. Tokenizer Architecture & Special Tokens

| Parameter | Configuration |
|---|---|
| **Tokenizer Type** | Character-preseeded Subword Byte-Pair Encoding (BPE) with memoized rank-lookup |
| **Vocabulary Size ($V$)** | 1,024 tokens |
| **Special Control Tokens** | `<pad>` (0), `<s>` (1), `</s>` (2), `<unk>` (3), `<sec>` (4), `<court>` (5), `<prov>` (6), `<act>` (7) |
| **Unicode Pre-seeding** | ASCII Printable (32..126) + Full Devanagari Block (`0x0900`..`0x097F`) |

---

## 3. Representative Sample Evaluations

Executed via `scripts/audit_tokenizer.py`:

| Input Sample Text | Token IDs Count | Token Substrings Produced | Round-Trip Match |
|---|---|---|---|
| `Section 482(4)` | 9 | `['<s>', 'Section', '4', '8', '2', '(', '4', ')', '</s>']` | **TRUE** |
| `Section 63(4)(c)` | 11 | `['<s>', 'Section', '6', '3', '(', '4', ')', '(', 'c', ')', '</s>']` | **TRUE** |
| `Article 21` | 4 | `['<s>', 'Article', '21', '</s>']` | **TRUE** |
| `BNSS 2023` | 7 | `['<s>', 'B', 'N', 'S', 'S', '2023', '</s>']` | **TRUE** |
| `BSA 2023` | 6 | `['<s>', 'B', 'S', 'A', '2023', '</s>']` | **TRUE** |
| `धारा 482` | 7 | `['<s>', 'ध', 'ा', 'र', 'ा', '482', '</s>']` *(Remediated: 0 `<unk>`)* | **TRUE** |
| *Mixed Hindi-English Legal Query* | 29 | Correct subwords, full preservation of `धारा 482` and English terms | **TRUE** |
| *Empty String `""`* | 2 | `['<s>', '</s>']` | **TRUE** |
| *Whitespace String `" "`* | 2 | `['<s>', '</s>']` | **TRUE** |
| `xyz123nonexistentword` | 14 | Graceful character-level fallback (`x`, `y`, `z`, `1`, `23`, `n`, `on`...) | **TRUE** |

---

## 4. Corpus Compression & Vocabulary Utilization

Evaluated across 100 in-domain chunks (BNSS) versus 100 held-out chunks (DPDP Act):

| Compression Metric | In-Domain Corpus (BNSS) | Held-Out Corpus (DPDP Act) | Implication |
|---|---|---|---|
| **Total Words Audited** | 12,736 words | 10,122 words | Substantial multi-paragraph samples |
| **Total Tokens Produced** | 20,110 tokens | 16,814 tokens | Stable length expansion |
| **Tokens Per Word** | **1.579** | **1.661** | Healthy subword granularity (~1.6 tokens/word) |
| **Tokens Per Character** | **0.2625** | **0.2790** | Highly efficient (~3.7 characters/token) |
| **Vocabulary Utilization** | **80.47%** (824 / 1,024) | **72.56%** (743 / 1,024) | High utilization, minimal dead vocabulary |
| **Unknown Token Rate (`<unk>`)** | **0.000%** (0 tokens) | **0.000%** (0 tokens) | Complete coverage of English & Hindi text |

---

## 5. Defect Discovery & Remediation: Devanagari Base Seeding

### Defect Analysis
In Phase 31, running `tok.encode("धारा 482")` produced `['<s>', '<unk>', '<unk>', '<unk>', '<unk>', '4', '8', '2', '</s>']`.
- Because training texts only contained English legal sections, Hindi glyphs were never observed during character frequency counting.
- Any character not in `self.vocab` was converted to `<unk>` (id 3).

### Remediation Implemented
1. Updated `train_from_texts()` in `research/original_model/tokenizer.py` to pre-seed `0x0900`–`0x097F` before computing merges.
2. Verified via `test_devanagari_preseeded_tokenization` in `tests/test_phase32_validation.py`.
3. Handled Windows `cp1252` console encoding by configuring `sys.stdout.reconfigure(encoding="utf-8")`.

