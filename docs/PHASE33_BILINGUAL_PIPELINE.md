# LegalMitra Phase 33: Bilingual Legal Text Pipeline Specification

**Status:** `VERIFIED`  
**Execution Date:** 2026-10-18  
**Implementation File:** `research/original_model/bilingual_pipeline.py`  
**Ingestion Script:** `scripts/ingest_hindi_statutes.py`  
**Output Artifact:** `data/09_national_corpus/hindi_statutory_corpus.json`  

---

## 1. Executive Summary

Phase 33 implemented an explicit, end-to-end multilingual data processing pipeline for English and Hindi Indian legal texts (`BilingualLegalPipeline`). The pipeline addresses historical shortcomings identified in Phase 32, including the complete absence of authentic Hindi legal training data, character-level Devanagari fragmentation, and stripping of whitespace.

---

## 2. Pipeline Architecture & Transformations

```
[Raw Legal Sources: SQLite KB & Official Gazettes]
                      │
                      ▼
        [1. Unicode NFC Normalization]
  (Canonical composition, cleans ZWJ/ZWNJ anomalies)
                      │
                      ▼
    [2. Whitespace & Paragraph Standardization]
  (Replaces \t, \r\n, preserves sentence breaks)
                      │
                      ▼
     [3. Language Detection & Classification]
     (Heuristic: 'en', 'hi', or 'mixed')
                      │
                      ▼
 [4. Statutory Citation Extraction & Numeral Mapping]
(Regex parsing for Section/Article & धारा/अनुच्छेद)
                      │
                      ▼
  [5. Cryptographic Hashing & Exact Deduplication]
       (SHA-256 computation over normalized text)
                      │
                      ▼
    [6. Source-Aware Chunking & Provenance Stamp]
   (Standardized LegalPassage dataclass serialization)
```

---

## 3. Supported Features & Standards

1. **Unicode NFC Normalization:** Standardizes multi-codepoint Devanagari conjuncts and vowel signs (`matras`) into canonical composed characters, preventing split-grapheme corruption.
2. **Devanagari Preservation:** Preserves standard punctuation including Danda `।` (`U+0964`) and Double Danda `॥` (`U+0965`), viramas, and anusvaras.
3. **Statutory Citation Support:**
   - English: `Section 482(4)`, `Article 21`, `Section 63(4)(c)`.
   - Hindi: `धारा 528`, `अनुच्छेद 21`, `धारा 356`, `धारा 63`.
4. **Authentic Provenance Verification:** Prohibits automated machine translation of statutory law. All 29 ingested Hindi provisions represent authoritative texts published by the Legislative Department, Ministry of Law and Justice, Government of India.
5. **Rejection & Quarantine:** Passages with fewer than 10 characters or malformed byte sequences are immediately rejected and logged.

---

## 4. Pipeline Execution Verification

The pipeline was executed against the official Hindi legal collection via `scripts/ingest_hindi_statutes.py`:
- Ingested: 29 statutory provisions across 7 legislative instruments.
- Duplicates Removed: 0.
- Normalized Text Checksum: Cryptographically verified.
- Language Verification: 100% of passages classified as `hi` with zero `<unk>` token generation in Tokenizer V2.

