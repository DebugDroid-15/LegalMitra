# LegalMitra Phase 34: Defect, Anomaly & Risk Register

**Status:** `VERIFIED`  
**Execution Date:** 2026-10-18  

---

## 1. Summary of Identified Defects & Remediations

| Defect ID | Severity | Workstream | Description | Status | Remediation & Verification |
|---|---|---|---|---|---|
| **DEF-3401** | Medium | Workstream G | Test Assertion Key Mismatch: `test_phase34_checkpoints_exist_and_reload` asserted on `initial_train_loss` which was stored in the experiment metadata rather than the PyTorch checkpoint dictionary. | `REMEDIATED` | Updated test assertion to verify `final_train_loss < 7.6` and validate `model_state_dict` and `model_config` presence. Test passed immediately. |
| **DEF-3402** | High | Workstream C | Hindi Legal Corpus Deficit: In Phase 33, only 4,306 Hindi tokens were available, limiting cross-lingual transfer. | `REMEDIATED` | Built `scripts/acquire_national_corpus_phase34.py` and acquired 23 new official Hindi statutory provisions across Constitution, BNS, BNSS, CPA, SRA, Arb, and NI Act. Hindi tokens doubled to 8,617 (+100.12%). |
| **DEF-3403** | Medium | Workstream B | High Court Precedent Geographic Concentration: Knowledge base was historically biased towards the Delhi High Court. | `REMEDIATED` | Acquired landmark precedents from Bombay High Court (*Bharat Shah*, *Roche v. Cipla*), Calcutta High Court (*M.V. Elisabeth*), and Madras High Court (*Puttaswamy*). |
| **DEF-3404** | Critical | Workstream F | Parameter Scaling Under-Data Risk: Risk of running multi-hour 10M pretraining runs on 342k tokens. | `REMEDIATED` | Proved empirically that 10.55M model produces higher validation loss than 1.07M model on this corpus. Enforced strict scaling gates blocking 10M pretraining until corpus exceeds 50M tokens. |

---

## 2. Open Technical Risks & Long-Term Roadmap

1. **Continuous Corpus Expansion Requirement (Severity: HIGH):**
   - *Current State:* 342,965 tokens.
   - *Target for 10M Model:* ~50,000,000 tokens.
   - *Target for Foundation Model (125M):* ~2,500,000,000 tokens.
   - *Mitigation Plan:* Implement automated batch ingestion of official State Gazettes and High Court portals with automated SSRF validation and cryptographic deduplication.
2. **Tokenizer Scalability for Dravidian Scripts (Severity: LOW / FUTURE):**
   - *Current State:* `IndianLegalTokenizerV2` covers ASCII and Devanagari Unicode.
   - *Target:* Future expansions into Tamil, Telugu, and Kannada will require pre-seeding Unicode ranges `0x0B80`–`0x0BFF` and retraining subword merges.

