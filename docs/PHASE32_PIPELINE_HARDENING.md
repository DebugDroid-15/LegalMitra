# LegalMitra Phase 32: Training Pipeline Hardening

**Phase:** 32 — Original Foundation Model Validation, Data Integrity & Generalization Gate  
**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Owner:** Team Shatrujeet  
**Date:** 2026-10-18  
**Classification:** Proprietary and Confidential  

---

## 1. Executive Summary

Phase 32 hardened the experimental foundation model codebase under `research/original_model/`, transforming a prototype research script into an auditable, reproducible, and mathematically rigorous training pipeline.

---

## 2. Implemented Hardening Upgrades

### 2.1 Loss Objective Hardening (Padding Exclusion)
- **Problem:** `LegalDecoderTransformer.forward` previously used default `F.cross_entropy`, which ignores index `-100`. Because `<pad>` was token `0`, padding tokens were penalized and rewarded, corrupting loss dynamics.
- **Fix:** Added `pad_token_id: int = 0` to `LegalTransformerConfig` and passed `ignore_index=self.config.pad_token_id` in `F.cross_entropy`.
- **Verification:** `test_padding_token_loss_exclusion` verified that loss calculation is strictly confined to real content transitions.

### 2.2 Numerical Divergence & NaN/Inf Protection
- **Problem:** Deep transformers can suffer from gradient explosions, exploding attention scores, or sudden loss NaN collapses.
- **Fix:** Added explicit post-loss validation:
  ```python
  if torch.isnan(loss) or torch.isinf(loss):
      raise FloatingPointError("Loss diverged to NaN or Inf during forward pass")
  ```
  Coupled with global gradient norm clipping: `torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)`.

### 2.3 Devanagari & Unicode Base Seeding
- **Problem:** Hindi legal terms (e.g. `धारा`, `न्यायालय`) defaulted to `<unk>` tokens when the tokenizer was trained exclusively on English statutory text.
- **Fix:** Updated `train_from_texts()` in `research/original_model/tokenizer.py` to pre-seed all ASCII printable characters (`32..126`) and the entire Unicode Devanagari range (`0x0900`..`0x097F`).
- **Verification:** `test_devanagari_preseeded_tokenization` confirms zero `<unk>` collisions on Hindi legal text.

### 2.4 Document-Grouped Split & Versioned Manifests
- **Problem:** Sequential array slicing broke `IND-STAT-IT-2000` across splits, creating 6 duplicate chunks and 8 near-duplicate pairs.
- **Fix:** Implemented `split_strategy="source_grouped"` in `research/original_model/dataset.py`.
- **Artifacts:**
  - `research/original_model/manifests/train_manifest_v1.json` (SHA-256 verified)
  - `research/original_model/manifests/val_manifest_v1.json` (SHA-256 verified)
  - Cross-split source overlap: **0**. Cross-split text duplication: **0**.

### 2.5 Safe Checkpoint Serialization & Reloading
- **Fix:** Checkpoints serialize full metadata envelopes:
  - `step`: Integer step counter
  - `config`: Hyperparameter dictionary
  - `model_state_dict`: Weight tensors
  - `optimizer_state_dict`: AdamW momentum buffers
  - `final_train_loss` & `final_val_loss`
- **Verification:** `test_checkpoint_reproduced_integrity` tests that reloaded weights instantiate a functioning model with zero key mismatches.

### 2.6 Windows Console UTF-8 Stream Reconfiguration
- **Problem:** Printing Devanagari text on Windows consoles triggered `UnicodeEncodeError: 'charmap' codec can't encode characters`.
- **Fix:** Reconfigured standard output streams on Windows:
  ```python
  if sys.stdout.encoding.lower() != "utf-8":
      sys.stdout.reconfigure(encoding="utf-8")
  ```

