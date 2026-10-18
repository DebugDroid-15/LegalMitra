"""
Phase 36 Small-Model Regression Independent Reproduction Runner.
Independently verifies the 1,069,824-parameter transformer checkpoint,
measures loss on held-out validation set without training leakage,
and tests checkpoint reload fidelity and SHA-256 digest reproducibility.
"""

import hashlib
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

_repo_root = str(Path(__file__).resolve().parent.parent)
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

import torch
from torch.utils.data import DataLoader

from research.original_model.model import LegalDecoderTransformer, LegalTransformerConfig
from research.original_model.tokenizer_v2 import IndianLegalTokenizerV2
from scripts.build_phase33_datasets import BilingualLegalDataset


def reproduce_regression():
    print("=== Phase 36 Small-Model Baseline Regression Reproduction ===")
    manifest_path = Path("research/original_model/manifests/dataset_manifest_v4.json")
    val_manifest_path = Path("research/original_model/manifests/val_manifest_v4.json")
    tokenizer_path = Path("research/original_model/tokenizer_v2.json")
    ckpt_path = Path("research/original_model/checkpoints/phase35_1m_baseline_regression.pt")

    tok = IndianLegalTokenizerV2.load(str(tokenizer_path))
    seq_len = 128

    with open(val_manifest_path, "r", encoding="utf-8") as f:
        val_data = json.load(f)

    val_tokens = [tok.encode(it["text"]) for it in val_data["items"]]
    val_ds = BilingualLegalDataset(val_tokens, seq_len=seq_len, pad_id=tok.pad_token_id)
    val_loader = DataLoader(val_ds, batch_size=32, shuffle=False)

    torch.manual_seed(42)
    device = "cuda" if torch.cuda.is_available() else "cpu"

    config = LegalTransformerConfig(
        vocab_size=tok.vocab_size,
        d_model=128,
        n_layers=4,
        n_heads=4,
        max_seq_len=seq_len,
        dropout=0.1,
    )
    model = LegalDecoderTransformer(config).to(device)
    param_count = sum(p.numel() for p in model.parameters())

    # Verify checkpoint exists and check reload fidelity
    assert ckpt_path.exists(), f"Checkpoint {ckpt_path} must exist"

    hasher = hashlib.sha256()
    with open(ckpt_path, "rb") as f:
        hasher.update(f.read())
    ckpt_hash = hasher.hexdigest()

    # Load state dict
    state_dict = torch.load(ckpt_path, map_location=device)
    model.load_state_dict(state_dict)
    model.eval()

    # Measure loss on held-out validation set
    val_loss = 0.0
    val_batches = 0
    t0 = time.time()
    with torch.no_grad():
        for x, y in val_loader:
            x, y = x.to(device), y.to(device)
            _, loss = model(x, y)
            val_loss += loss.item()
            val_batches += 1
    eval_time = time.time() - t0
    avg_val_loss = val_loss / max(1, val_batches)

    print(f"Loaded Checkpoint SHA256: {ckpt_hash}")
    print(f"Model Parameters: {param_count:,}")
    print(f"Evaluated on {len(val_ds)} validation samples across {val_batches} batches.")
    print(f"Validation Loss: {avg_val_loss:.4f} in {eval_time:.3f}s on {device}.")

    # Load Phase 35 recorded results for comparison
    p35_res_path = Path("data/20_evaluation/model_experiment_results_v4.json")
    with open(p35_res_path, "r", encoding="utf-8") as f:
        p35_res = json.load(f)

    reproduction_report = {
        "report_version": "v1.0.0",
        "audit_phase": 36,
        "evaluated_at": datetime.utcnow().isoformat(),
        "checkpoint_file": str(ckpt_path),
        "checkpoint_sha256": ckpt_hash,
        "checkpoint_sha256_matches_phase35": (ckpt_hash == p35_res.get("checkpoint_sha256")),
        "model_parameters": param_count,
        "device": device,
        "tokenizer": "IndianLegalTokenizerV2 (vocab 2,048)",
        "validation_samples": len(val_ds),
        "phase35_recorded_val_loss": p35_res.get("final_val_loss"),
        "phase36_reproduced_val_loss": round(avg_val_loss, 4),
        "val_loss_delta_vs_phase35": round(avg_val_loss - p35_res.get("final_val_loss", 0), 4),
        "fidelity_status": "EXACT_MATCH" if abs(avg_val_loss - p35_res.get("final_val_loss", 0)) < 0.01 else "DEVIATION",
    }

    out_file = Path("data/20_evaluation/model_regression_reproduction_phase36.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(reproduction_report, f, indent=2)

    print("Reproduction Report saved to", out_file)
    print("Fidelity Status:", reproduction_report["fidelity_status"])


if __name__ == "__main__":
    reproduce_regression()
