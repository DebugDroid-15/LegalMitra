"""
Phase 34 Controlled Model and Tokenizer Regression Experiment Runner.
Executes experiments on the expanded multilingual legal corpus:
- Exp 1: Baseline Prototype Reproduction on Expanded Corpus
- Exp 2: Expanded Multilingual Joint Pretraining (EN + Expanded HI)
- Exp 3: Parameter Scaling Comparison (1.07M vs 4.50M vs 10.55M)
- Exp 4: Multi-Seed Stability Check (Seeds 42, 43, 44)
- Exp 5: Held-Out Generalization Across New Jurisdictions & Precedents
Outputs results to data/20_evaluation/model_experiment_results_v3.json and
data/20_evaluation/generalization_eval_results_v3.json.
"""

import sys
from pathlib import Path

_repo_root = str(Path(__file__).resolve().parent.parent)
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

import hashlib
import json
import math
import time
from typing import Dict, List, Any, Tuple

import torch
from torch.utils.data import DataLoader

from research.original_model.model import LegalDecoderTransformer, LegalTransformerConfig
from research.original_model.tokenizer_v2 import IndianLegalTokenizerV2
from scripts.build_phase34_datasets import build_phase34_datasets, BilingualLegalDataset


def compute_checkpoint_hash(path: Path) -> str:
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def evaluate_loss(model: torch.nn.Module, dataloader: DataLoader, device: str) -> float:
    model.eval()
    total_loss = 0.0
    total_batches = 0
    with torch.no_grad():
        for inputs, targets in dataloader:
            inputs = inputs.to(device)
            targets = targets.to(device)
            _, loss = model(inputs, targets)
            total_loss += loss.item()
            total_batches += 1
    return total_loss / total_batches if total_batches > 0 else float("inf")


def train_model_step(
    exp_name: str,
    model: LegalDecoderTransformer,
    train_loader: DataLoader,
    val_loader: DataLoader,
    num_steps: int = 50,
    lr: float = 1e-3,
    device: str = "cuda",
    seed: int = 42,
    checkpoint_dir: str = "research/original_model/checkpoints",
) -> Dict[str, Any]:
    torch.manual_seed(seed)
    if device == "cuda":
        torch.cuda.manual_seed_all(seed)
        torch.cuda.reset_peak_memory_stats()

    model = model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)

    t0 = time.time()
    model.train()
    step = 0
    initial_loss = None
    initial_val_loss = evaluate_loss(model, val_loader, device)
    model.train()

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
        _, loss = model(inputs, targets)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()

        cur_loss = loss.item()
        if step == 0:
            initial_loss = cur_loss
        step += 1

    total_time = time.time() - t0
    final_loss = cur_loss
    final_val_loss = evaluate_loss(model, val_loader, device)

    peak_vram_mb = torch.cuda.max_memory_allocated() / (1024 * 1024) if device == "cuda" else 0.0
    total_tokens_trained = num_steps * train_loader.batch_size * 128
    tok_per_sec = total_tokens_trained / total_time

    # Save checkpoint
    ckpt_dir = Path(checkpoint_dir)
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    save_path = ckpt_dir / f"phase34_{exp_name}.pt"
    checkpoint_data = {
        "exp_name": exp_name,
        "seed": seed,
        "step": step,
        "model_config": model.config.__dict__,
        "model_state_dict": model.state_dict(),
        "final_train_loss": final_loss,
        "final_val_loss": final_val_loss,
    }
    torch.save(checkpoint_data, save_path)
    ckpt_hash = compute_checkpoint_hash(save_path)

    return {
        "experiment_name": exp_name,
        "seed": seed,
        "steps": num_steps,
        "model_parameters": model.count_parameters(),
        "initial_train_loss": round(initial_loss, 4),
        "final_train_loss": round(final_loss, 4),
        "initial_val_loss": round(initial_val_loss, 4),
        "final_val_loss": round(final_val_loss, 4),
        "train_loss_delta": round(final_loss - initial_loss, 4),
        "val_loss_delta": round(final_val_loss - initial_val_loss, 4),
        "tokens_per_second": round(tok_per_sec, 1),
        "total_time_seconds": round(total_time, 2),
        "peak_vram_mb": round(peak_vram_mb, 2),
        "checkpoint_file": str(save_path),
        "checkpoint_sha256": ckpt_hash,
    }


def run_phase34_all_experiments(
    output_path: str = "data/20_evaluation/model_experiment_results_v3.json",
    gen_eval_output_path: str = "data/20_evaluation/generalization_eval_results_v3.json",
):
    print("=== Executing Phase 34 Controlled Model Regressions ===")
    device = "cuda" if torch.cuda.is_available() else "cpu"

    tok = IndianLegalTokenizerV2.load("research/original_model/tokenizer_v2.json")
    train_ds, val_ds, test_ds, manifest_v3 = build_phase34_datasets(seq_len=128)
    train_loader = DataLoader(train_ds, batch_size=8, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=8, shuffle=False)
    test_loader = DataLoader(test_ds, batch_size=8, shuffle=False)

    cfg_proto = LegalTransformerConfig(vocab_size=tok.vocab_size, d_model=128, n_layers=4, n_heads=4, d_ff=512, max_seq_len=128, pad_token_id=tok.pad_token_id)
    cfg_inter = LegalTransformerConfig(vocab_size=tok.vocab_size, d_model=256, n_layers=5, n_heads=4, d_ff=1024, max_seq_len=128, pad_token_id=tok.pad_token_id)
    cfg_10m = LegalTransformerConfig(vocab_size=tok.vocab_size, d_model=320, n_layers=8, n_heads=8, d_ff=1280, max_seq_len=128, pad_token_id=tok.pad_token_id)

    experiments = []

    # Exp 1: Baseline Prototype on Expanded Corpus
    print("\n--- Running Exp 1: Baseline Prototype on Expanded Corpus ---")
    m_proto = LegalDecoderTransformer(cfg_proto)
    res_1 = train_model_step("exp1_proto_expanded", m_proto, train_loader, val_loader, num_steps=50, lr=1e-3, device=device, seed=42)
    experiments.append(res_1)

    # Exp 2: Parameter Scaling on Expanded Corpus (Intermediate ~4.5M)
    print("\n--- Running Exp 2: Intermediate Model on Expanded Corpus ---")
    m_inter = LegalDecoderTransformer(cfg_inter)
    res_2 = train_model_step("exp2_inter_expanded", m_inter, train_loader, val_loader, num_steps=50, lr=1e-3, device=device, seed=42)
    experiments.append(res_2)

    # Exp 3: Parameter Scaling on Expanded Corpus (Target 10.5M)
    print("\n--- Running Exp 3: Target 10.5M Model on Expanded Corpus ---")
    m_10m = LegalDecoderTransformer(cfg_10m)
    res_3 = train_model_step("exp3_10m_expanded", m_10m, train_loader, val_loader, num_steps=50, lr=1e-3, device=device, seed=42)
    experiments.append(res_3)

    # Exp 4: Multi-Seed Stability Check (Seeds 42, 43, 44)
    print("\n--- Running Exp 4: Multi-Seed Stability Check ---")
    seed_runs = []
    for s in [42, 43, 44]:
        m_s = LegalDecoderTransformer(cfg_proto)
        r_s = train_model_step(f"exp4_seed_{s}", m_s, train_loader, val_loader, num_steps=50, lr=1e-3, device=device, seed=s)
        seed_runs.append({
            "seed": s,
            "train_loss_delta": r_s["train_loss_delta"],
            "final_val_loss": r_s["final_val_loss"],
            "checkpoint_sha256": r_s["checkpoint_sha256"],
        })
    deltas = [sr["train_loss_delta"] for sr in seed_runs]
    mean_d = sum(deltas) / len(deltas)
    var_d = sum((d - mean_d) ** 2 for d in deltas) / len(deltas)
    experiments.append({
        "experiment_name": "exp4_multi_seed_stability",
        "seeds_tested": [42, 43, 44],
        "results": seed_runs,
        "mean_loss_delta": round(mean_d, 4),
        "loss_delta_variance": round(var_d, 6),
        "is_stable": var_d < 0.05,
    })

    # Save Experiment Summary
    exp_report = {
        "report_version": "v3.0.0",
        "phase": 34,
        "dataset_manifest_ref": "research/original_model/manifests/dataset_manifest_v3.json",
        "total_corpus_tokens": manifest_v3["total_tokens_extracted"],
        "experiments": experiments,
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(exp_report, f, indent=2)
    print(f"Experiment summary written to {output_path}")

    # -------------------------------------------------------------
    # Generalization Evaluation across Held-Out Jurisdictions
    # -------------------------------------------------------------
    print("\n--- Running Held-Out Generalization Evaluation (Phase 34) ---")
    random_baseline_loss = math.log(tok.vocab_size)
    random_baseline_ppl = float(tok.vocab_size)

    # Evaluate best model (Prototype trained on expanded multilingual corpus)
    m_eval = m_proto
    m_eval.eval()

    # Held-out domains:
    # 1. Held-out English Statutes (DPDP + Limitation)
    # 2. Held-out Precedents (Arjun Khotkar SC 2020 + Roche v Cipla Bombay HC)
    # 3. Held-out Hindi Statutes (IT Act 2000 HI)
    # 4. Expanded Bilingual Queries & Citations
    with open("data/09_national_corpus/phase34_expanded_corpus.json", "r", encoding="utf-8") as f:
        p34_data = json.load(f)
    roche_text = [p["content"] for p in p34_data["passages"] if "ROCHE" in p["source_id"]]

    with open("data/09_national_corpus/hindi_statutory_corpus.json", "r", encoding="utf-8") as f:
        p33_hi_data = json.load(f)
    it_hi_text = [p["content"] for p in p33_hi_data["passages"] if "IT-2000" in p["source_id"]]

    bilingual_queries = [
        "Under Section 482 of CrPC and Section 528 of BNSS 2023, High Courts possess inherent jurisdiction.",
        "धारा 528. उच्च न्यायालय की अंतर्निहित शक्तियों की व्यावृत्ति न्याय के उद्देश्यों की प्राप्ति के लिए आवश्यक है।",
        "धारा 34. निजी प्रतिरक्षा का अधिकार प्रत्येक व्यक्ति को अपने शरीर और संपत्ति की रक्षा करने का अधिकार देता है।",
        "Section 10 of the Specific Relief Act, 1963 mandates that specific performance of contracts shall be enforced by the court.",
        "Under Section 138 of Negotiable Instruments Act, dishonour of cheque for insufficiency of funds attracts criminal liability.",
        "The public interest doctrine in patent injunctions balances pharmaceutical exclusivity with patient access to affordable medicine.",
    ]

    domains = [
        ("Held-Out English Precedents (Roche v Cipla / High Court)", roche_text),
        ("Held-Out Hindi Statutes (IT Act 2000 HI)", it_hi_text),
        ("Expanded Bilingual Legal Queries & Citations", bilingual_queries),
    ]

    gen_results = []
    for dname, dtexts in domains:
        tokens_list = [tok.encode(t) for t in dtexts]
        ds_dom = BilingualLegalDataset(tokens_list, seq_len=128, pad_id=tok.pad_token_id)
        if len(ds_dom) == 0:
            continue
        loader_dom = DataLoader(ds_dom, batch_size=8, shuffle=False)
        t_loss = 0.0
        n_b = 0
        with torch.no_grad():
            for inp, tgt in loader_dom:
                inp = inp.to(device)
                tgt = tgt.to(device)
                _, loss = m_eval(inp, tgt)
                t_loss += loss.item()
                n_b += 1
        avg_loss = t_loss / n_b
        ppl = math.exp(min(avg_loss, 20.0))
        delta = avg_loss - random_baseline_loss

        gen_results.append({
            "domain_name": dname,
            "sample_count": len(dtexts),
            "token_count": sum(len(x) for x in tokens_list),
            "cross_entropy_loss": round(avg_loss, 4),
            "perplexity": round(ppl, 2),
            "random_baseline_loss": round(random_baseline_loss, 4),
            "delta_vs_random": round(delta, 4),
            "generalization_verdict": "LEARNED" if delta < -0.3 else "UNLEARNED_DATA_DEFICIT",
        })

    gen_report = {
        "report_version": "v3.0.0",
        "phase": 34,
        "model_evaluated": "phase34_exp1_proto_expanded.pt",
        "random_baseline": {
            "loss": round(random_baseline_loss, 4),
            "perplexity": round(random_baseline_ppl, 2),
        },
        "domain_evaluations": gen_results,
    }
    with open(gen_eval_output_path, "w", encoding="utf-8") as f:
        json.dump(gen_report, f, indent=2)

    print(f"Generalization evaluation written to {gen_eval_output_path}")
    for gr in gen_results:
        print(f"  {gr['domain_name']}: Loss = {gr['cross_entropy_loss']} | PPL = {gr['perplexity']} (Delta: {gr['delta_vs_random']})")
    return exp_report, gen_report


if __name__ == "__main__":
    run_phase34_all_experiments()

