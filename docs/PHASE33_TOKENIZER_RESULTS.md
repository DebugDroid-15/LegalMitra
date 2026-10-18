# LegalMitra Phase 33: Tokenizer Evaluation and V2 Improvement Report

**Status:** `VERIFIED`  
**Execution Date:** 2026-10-18  
**Tokenizer V1:** `research/original_model/tokenizer.json` (Vocab: 1,024, Merges: 933)  
**Tokenizer V2:** `research/original_model/tokenizer_v2.json` (Vocab: 2,048, Merges: 1,811)  
**Audit Artifact:** `data/20_evaluation/tokenizer_v2_audit_results.json`  

---

## 1. Executive Summary

Phase 32 identified severe limitations in `IndianLegalTokenizer` (V1): although individual Devanagari codepoints were pre-seeded, zero BPE merges existed for Hindi words because the tokenizer was trained purely on English text. Consequently, every Hindi character was tokenized as an isolated subword, creating extreme token inflation (5.8 tokens per word) and stripping all whitespace on decode.

Phase 33 engineered `IndianLegalTokenizerV2` (`research/original_model/tokenizer_v2.py`), trained jointly from scratch on English and Hindi legal texts with whitespace markers (`Ġ` / `Ċ`).

---

## 2. Side-by-Side Architectural Comparison

| Architectural Property | Tokenizer V1 | Tokenizer V2 | Improvement |
|---|---|---|---|
| **Vocabulary Size** | 1,024 | 2,048 | 2.0x capacity |
| **Learned BPE Merges** | 933 | 1,811 | 1.94x merge rules |
| **Devanagari Subword Merges** | **0** | **480+** | Full Hindi morpheme merges |
| **Whitespace Preservation** | NO (Words concatenated) | **YES (`Ġ` space marker)** | Exact roundtrip text reconstruction |
| **Special Language Tags** | 8 special tokens | 10 special tokens (`<hi>`, `<en>`) | Explicit bilingual tagging |
| **Unknown Token Rate (Hindi)**| **95.2%** (on legacy serialized) | **0.0%** | Zero `<unk>` tokens |

---

## 3. Empirical Compression & Segmentation Results

Measured across 7 standard Indian legal test cases (English statutory, Hindi constitutional, mixed query):

| Metric | Tokenizer V1 | Tokenizer V2 | Delta / Improvement |
|---|---|---|---|
| **Total Test Sample Tokens** | 402 tokens | 238 tokens | **-40.8% total token reduction** |
| **Average Tokens per Word** | 3.56 tok/word | 2.11 tok/word | **40.7% compression efficiency gain** |
| **Section 528 BNSS (Hindi)** | 93 tokens | **20 tokens** | **78.49% token reduction** |
| **Section 356 Defamation (Hindi)**| 71 tokens | **19 tokens** | **73.24% token reduction** |
| **Constitutional Preamble (Hindi)**| 104 tokens | **50 tokens** | **51.92% token reduction** |
| **English Article 21** | 23 tokens | 28 tokens | Slight expansion due to whitespace tokens |
| **Mixed Query (CrPC 482 / BNSS 528)**| 46 tokens | 44 tokens | 4.35% reduction + natural spaces |

---

## 4. Held-Out Vocabulary Activation

Evaluated against held-out English and Hindi text collections:
- **V1 English Activation:** 337 / 1,024 (32.91%) | **V1 Hindi Activation:** 14 / 1,024 (1.37%)
- **V2 English Activation:** 370 / 2,048 (18.07%) | **V2 Hindi Activation:** 190 / 2,048 (9.28%)

**Key Finding:** Tokenizer V2 achieves a **6.77x higher vocabulary activation rate on Hindi legal text** (190 distinct subwords vs 14 isolated characters in V1), proving genuine multi-character subword abstraction.

