# LegalMitra Phase 33: Defect & Risk Register

**Status:** `VERIFIED`  
**Execution Date:** 2026-10-18  

---

## 1. Summary of Identified Defects & Remediations

| Defect ID | Severity | Workstream | Description | Status | Remediation & Evidence |
|---|---|---|---|---|---|
| **DEF-3301** | High | Workstream C | Tokenizer V1 lacks Hindi BPE merges; every Hindi word tokenized character-by-character (5.8 tok/word) with word spaces stripped. | `REMEDIATED` | Created `IndianLegalTokenizerV2` with joint bilingual merges and whitespace marker (`Ġ` / `Ċ`). Reduced token count by 40.8% and preserved natural spaces. |
| **DEF-3302** | Critical | Workstream A | Corpus Volume Myth: Repository was assumed to have 200M pretraining tokens, but actual verified corpus contains only 336,892 tokens. | `REMEDIATED` | Conducted rigorous physical corpus audit (`scripts/audit_corpus_inventory.py`), documented exact counts (336k tokens), and placed strict gate on scaling. |
| **DEF-3303** | High | Workstream B | Complete absence of authentic Hindi legal training data in repository (0 Devanagari chunks in KB). | `REMEDIATED` | Built `BilingualLegalPipeline` and ingested 29 official Hindi statutory provisions from Official Gazette & Legislative Department (`data/09_national_corpus/hindi_statutory_corpus.json`). |
| **DEF-3304** | High | Workstream E/F | 10M Model Over-parameterization Risk: Training 10.55M model on 336k tokens yields 0.032 tokens/param (628x deficit vs Chinchilla optimum). | `REMEDIATED` | Profiled compute on RTX 2050; proved 10M model val loss is higher than 1M model on 336k tokens. Issued STRICT NO-GO for full-scale 10M pretraining until corpus expansion. |
| **DEF-3305** | Medium | Workstream G | Experiment Script Missing Import: `evaluate_loss` type annotation referenced unimported `nn_module`. | `REMEDIATED` | Corrected to `torch.nn.Module` in `scripts/run_phase33_experiments.py`. |

---

## 2. Open Risks & Mitigation Strategies

1. **Hindi Training Data Scarcity (Risk Level: HIGH)**
   - *Description:* With only 4,306 Hindi training tokens, the model cannot generalize to unseen Hindi statutes (PPL 3,008 on held-out IT Act text).
   - *Mitigation:* Curate full official Hindi Gazette editions of central penal codes (BNS, BNSS, BSA) and commercial acts from India Code in upcoming phases.
2. **Compute Scaling Boundary (Risk Level: MEDIUM)**
   - *Description:* Local RTX 2050 (4GB VRAM) throughput is 18,204 tok/s. Training 211M tokens would take ~3.2 hours, but training 2.5B tokens (125M model) would take ~38 days.
   - *Mitigation:* Retain 1M–4.5M configurations locally for research; reserve 125M+ scaling for approved cloud compute once 2.5B lawful tokens are curated.

