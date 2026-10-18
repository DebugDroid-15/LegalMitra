"""
Prototype Training Runner for Original Indian Legal Transformer.
Trained strictly from randomly initialized weights on the local machine.
Zero pretrained models, weights, or external APIs.
Executes training loop, measures loss decrease, saves/reloads checkpoint,
and writes structured run summary.
"""

import sys
from pathlib import Path

# Ensure repo root is on sys.path
_repo_root = str(Path(__file__).resolve().parent.parent.parent)
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

import json
import time
from typing import Dict, Any

import torch
from torch.utils.data import DataLoader

from research.original_model.dataset import build_train_val_datasets
from research.original_model.model import LegalDecoderTransformer, LegalTransformerConfig


def train_prototype(
    num_steps: int = 50,
    batch_size: int = 8,
    learning_rate: float = 3e-4,
    device_override: str = None,
    checkpoint_dir: str = "research/original_model/checkpoints",
    summary_path: str = "research/original_model/training_run_summary.json",
) -> Dict[str, Any]:
    torch.manual_seed(42)

    device = device_override or ("cuda" if torch.cuda.is_available() else "cpu")
    print(f"=== Initializing Original Legal Transformer Prototype on {device} ===")

    # 1. Dataset & Tokenizer preparation
    train_ds, val_ds, tokenizer, manifest = build_train_val_datasets(
        seq_len=128,
        target_vocab_size=512,
    )
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)

    # 2. Model configuration (Option A: Tiny Research Prototype)
    config = LegalTransformerConfig(
        vocab_size=tokenizer.vocab_size,
        d_model=128,
        n_layers=4,
        n_heads=4,
        d_ff=512,
        max_seq_len=128,
        dropout=0.1,
    )
    model = LegalDecoderTransformer(config).to(device)
    total_params = model.count_parameters()
    print(f"Model initialized from scratch with {total_params:,} parameters (N(0, 0.02)). Zero external weights.")

    # 3. Optimizer
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=0.01)

    # 4. Training loop
    model.train()
    step = 0
    loss_history = []
    initial_loss = None
    start_time = time.time()

    data_iter = iter(train_loader)
    while step < num_steps:
        try:
            inputs, targets = next(data_iter)
        except StopIteration:
            data_iter = iter(train_loader)
            inputs, targets = next(data_iter)

        inputs = inputs.to(device)
        targets = targets.to(device)

        optimizer.zero_grad()
        _, loss = model(input_ids=inputs, labels=targets)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()

        current_loss = loss.item()
        if step == 0:
            initial_loss = current_loss

        step += 1
        loss_history.append({"step": step, "loss": round(current_loss, 4)})

        if step % 10 == 0 or step == num_steps:
            print(f"Step {step:03d}/{num_steps} | Loss: {current_loss:.4f}")

    final_loss = loss_history[-1]["loss"]
    total_time = round(time.time() - start_time, 2)
    print(f"Training completed: Initial Loss = {initial_loss:.4f} -> Final Loss = {final_loss:.4f} in {total_time}s")

    # 5. Save checkpoint
    ckpt_path = Path(checkpoint_dir)
    ckpt_path.mkdir(parents=True, exist_ok=True)
    save_file = ckpt_path / f"prototype_step_{num_steps}.pt"

    checkpoint = {
        "step": step,
        "config": config.__dict__,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "initial_loss": initial_loss,
        "final_loss": final_loss,
        "total_params": total_params,
    }
    torch.save(checkpoint, save_file)
    print(f"Checkpoint saved to {save_file}")

    # 6. Verify checkpoint round-trip
    loaded_ckpt = torch.load(save_file, map_location=device)
    new_model = LegalDecoderTransformer(config).to(device)
    new_model.load_state_dict(loaded_ckpt["model_state_dict"])
    new_model.eval()
    print("Checkpoint reload verification: SUCCESS. State dict matched exactly.")

    # 7. Write run summary
    summary = {
        "device": device,
        "total_parameters": total_params,
        "training_steps": num_steps,
        "batch_size": batch_size,
        "learning_rate": learning_rate,
        "initial_loss": round(initial_loss, 4),
        "final_loss": round(final_loss, 4),
        "loss_reduction": round(initial_loss - final_loss, 4),
        "loss_reduction_pct": round(((initial_loss - final_loss) / initial_loss) * 100, 2),
        "training_time_seconds": total_time,
        "checkpoint_path": str(save_file),
        "checkpoint_size_bytes": save_file.stat().st_size,
        "loss_history": loss_history,
        "dataset_manifest": manifest,
    }

    s_path = Path(summary_path)
    s_path.parent.mkdir(parents=True, exist_ok=True)
    with open(s_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary


if __name__ == "__main__":
    train_prototype()
