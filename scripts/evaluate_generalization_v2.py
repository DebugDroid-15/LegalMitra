"""
Held-Out Generalization Evaluation Harness for LegalMitra Phase 33.
Evaluates trained models across strictly held-out English and Hindi legal texts:
- Held-out English Statutes (DPDP Act 2023, Limitation Act 1963)
- Held-out English Judicial Precedents (Arjun Khotkar SC 2020)
- Held-out Hindi Statutes (IT Act 2000 Hindi Provisions)
- Bilingual queries and statutory citations
Measures Cross-Entropy Loss, Perplexity, and Delta against Random Guessing Baseline.
Outputs data/20_evaluation/generalization_eval_results_v2.json.
"""

import sys
from pathlib import Path

_repo_root = str(Path(__file__).resolve().parent.parent)
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

import json
import math
import sqlite3
import torch
from torch.utils.data import DataLoader

from research.original_model.model import LegalDecoderTransformer, LegalTransformerConfig
from research.original_model.tokenizer_v2 import IndianLegalTokenizerV2
from scripts.build_phase33_datasets import BilingualLegalDataset


def evaluate_generalization_v2(
    checkpoint_path: str = "research/original_model/checkpoints/phase33_exp_d_multilingual_joint.pt",
    tokenizer_path: str = "research/original_model/tokenizer_v2.json",
    output_path: str = "data/20_evaluation/generalization_eval_results_v2.json",
):
    print("=== Running Phase 33 Generalization Evaluation ===")
    device = "cuda" if torch.cuda.is_available() else "cpu"

    tok = IndianLegalTokenizerV2.load(tokenizer_path)
    random_baseline_loss = math.log(tok.vocab_size)
    random_baseline_ppl = float(tok.vocab_size)

    # Load Model Checkpoint
    ckpt = torch.load(checkpoint_path, map_location=device)
    cfg_dict = ckpt["model_config"]
    cfg = LegalTransformerConfig(**cfg_dict)
    model = LegalDecoderTransformer(cfg).to(device)
    model.load_state_dict(ckpt["model_state_dict"])
    model.eval()

    # Load Held-Out Test Data from SQLite and Hindi Corpus
    conn = sqlite3.connect("data/legalmitra_kb.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # 1. Held-Out English Statutes: DPDP Act & Limitation Act
    c.execute("""
        SELECT content FROM legal_chunks
        WHERE source_id IN ('IND-STAT-DPDP-2023', 'IND-STAT-LIMIT-1963')
        AND is_synthetic_scaffold = 0
    """)
    held_out_en_statutes = [r["content"] for r in c.fetchall()]

    # 2. Held-Out English Judicial Precedent: Arjun Khotkar
    c.execute("""
        SELECT content FROM legal_chunks
        WHERE source_id = 'IND-JUD-SC-2020-ARJUN-KHOTKAR'
        AND is_synthetic_scaffold = 0
    """)
    held_out_en_precedent = [r["content"] for r in c.fetchall()]
    conn.close()

    # 3. Held-Out Hindi Statutes: IT Act 2000 Hindi Provisions
    with open("data/09_national_corpus/hindi_statutory_corpus.json", "r", encoding="utf-8") as f:
        hi_corpus = json.load(f)
    held_out_hi_statutes = [
        p["normalized_content"]
        for p in hi_corpus["passages"]
        if p["source_id"] == "IND-STAT-IT-2000-HI"
    ]

    # 4. Bilingual Legal Queries
    bilingual_queries = [
        "Under Section 482 of CrPC and Section 528 of BNSS 2023, High Courts possess inherent jurisdiction to quash criminal proceedings.",
        "Section 63 of Bharatiya Sakshya Adhiniyam, 2023 requires conditions for electronic evidence admissibility.",
        "Article 21 of the Constitution guarantees protection of life and personal liberty against arbitrary executive action.",
        "धारा 528. उच्च न्यायालय की अंतर्निहित शक्तियों की व्यावृत्ति न्याय के उद्देश्यों की प्राप्ति के लिए आवश्यक है।",
        "धारा 356 के अनुसार किसी व्यक्ति की ख्याति की अपहानि करने वाला लांछन मानहानि का अपराध है।",
        "Whether Section 482 of CrPC / धारा 528 BNSS allows quashing of FIR where civil dispute is criminalized?",
    ]

    eval_domains = [
        ("Held-Out English Statutes (DPDP + Limitation)", held_out_en_statutes),
        ("Held-Out English Judicial Precedents (Arjun Khotkar)", held_out_en_precedent),
        ("Held-Out Hindi Statutes (IT Act 2000 HI)", held_out_hi_statutes),
        ("Bilingual Statutory Queries & Citations", bilingual_queries),
    ]

    domain_results = []

    def compute_domain_loss(texts):
        tokens_list = [tok.encode(t) for t in texts]
        ds = BilingualLegalDataset(tokens_list, seq_len=128, pad_id=tok.pad_token_id)
        if len(ds) == 0:
            return float("nan"), float("nan"), 0
        loader = DataLoader(ds, batch_size=8, shuffle=False)
        total_loss = 0.0
        n_batches = 0
        with torch.no_grad():
            for inputs, targets in loader:
                inputs = inputs.to(device)
                targets = targets.to(device)
                _, loss = model(inputs, targets)
                total_loss += loss.item()
                n_batches += 1
        avg_loss = total_loss / n_batches
        ppl = math.exp(min(avg_loss, 20.0))
        total_tokens = sum(len(x) for x in tokens_list)
        return avg_loss, ppl, total_tokens

    for name, texts in eval_domains:
        loss, ppl, n_toks = compute_domain_loss(texts)
        delta_vs_random = loss - random_baseline_loss
        learned = delta_vs_random < -0.3

        domain_results.append({
            "domain_name": name,
            "sample_count": len(texts),
            "token_count": n_toks,
            "cross_entropy_loss": round(loss, 4),
            "perplexity": round(ppl, 2),
            "random_baseline_loss": round(random_baseline_loss, 4),
            "random_baseline_ppl": round(random_baseline_ppl, 2),
            "delta_vs_random": round(delta_vs_random, 4),
            "learned_distribution": learned,
        })

    report = {
        "evaluation_version": "v2.0.0",
        "phase": 33,
        "model_evaluated": checkpoint_path,
        "tokenizer_used": tokenizer_path,
        "vocabulary_size": tok.vocab_size,
        "random_guessing_baseline": {
            "loss": round(random_baseline_loss, 4),
            "perplexity": round(random_baseline_ppl, 2),
        },
        "domain_evaluations": domain_results,
        "trust_boundaries": {
            "is_autonomous_legal_reasoner": False,
            "substitutes_for_rag": False,
            "rag_mandatory_for_statutory_grounding": True,
            "hallucination_warning": "Next-token probability prediction does not imply factual statutory veracity. Grounded retrieval remains non-negotiable.",
        },
    }

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"Generalization evaluation written to {output_path}")
    for d in domain_results:
        print(f"  {d['domain_name']}: Loss = {d['cross_entropy_loss']} | PPL = {d['perplexity']} (Delta vs Random: {d['delta_vs_random']})")
    return report


if __name__ == "__main__":
    evaluate_generalization_v2()

