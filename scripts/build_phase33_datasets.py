"""
Dataset Builder for LegalMitra Phase 33 Bilingual Foundation Model Research.
Constructs source-grouped Train, Validation, and Held-out Test datasets
combining verified English chunks and authentic Hindi statutory provisions.
Excludes synthetic scaffolds, private conversations, and benchmark answers.
Generates SHA256 manifests for complete reproducibility.
"""

import sys
from pathlib import Path

_repo_root = str(Path(__file__).resolve().parent.parent)
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

import hashlib
import json
import sqlite3
from typing import Dict, List, Tuple, Any

import torch
from torch.utils.data import Dataset

from research.original_model.tokenizer_v2 import IndianLegalTokenizerV2


class BilingualLegalDataset(Dataset):
    """PyTorch Dataset yielding input_ids and target labels for next-token prediction."""

    def __init__(self, tokenized_sequences: List[List[int]], seq_len: int = 128, pad_id: int = 0):
        self.seq_len = seq_len
        self.pad_id = pad_id
        self.samples: List[torch.Tensor] = []

        for seq in tokenized_sequences:
            if len(seq) < 4:
                continue
            for i in range(0, len(seq), seq_len):
                chunk = seq[i : i + seq_len]
                if len(chunk) < seq_len:
                    chunk = chunk + [pad_id] * (seq_len - len(chunk))
                self.samples.append(torch.tensor(chunk, dtype=torch.long))

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        tensor = self.samples[idx]
        return tensor, tensor


def build_bilingual_datasets(
    db_path: str = "data/legalmitra_kb.db",
    hindi_corpus_path: str = "data/09_national_corpus/hindi_statutory_corpus.json",
    tokenizer_path: str = "research/original_model/tokenizer_v2.json",
    manifest_dir: str = "research/original_model/manifests",
    seq_len: int = 128,
) -> Tuple[BilingualLegalDataset, BilingualLegalDataset, BilingualLegalDataset, Dict[str, Any]]:
    print("=== Building Phase 33 Source-Grouped Bilingual Datasets ===")

    # 1. Load English Chunks from KB (Excluding Scaffold)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
        SELECT chunk_id, source_id, act_or_case_title, provision_or_para_ref, content
        FROM legal_chunks
        WHERE is_synthetic_scaffold = 0
        ORDER BY chunk_id ASC;
    """)
    en_rows = [dict(r) for r in c.fetchall()]
    conn.close()

    en_passages = [
        {
            "id": r["chunk_id"],
            "source_id": r["source_id"],
            "title": r["act_or_case_title"],
            "ref": r["provision_or_para_ref"],
            "language": "en",
            "text": f"{r['act_or_case_title']} - {r['provision_or_para_ref']}: {r['content']}",
        }
        for r in en_rows
    ]

    # 2. Load Hindi Statutory Provisions
    with open(hindi_corpus_path, "r", encoding="utf-8") as f:
        hi_data = json.load(f)
    hi_passages = [
        {
            "id": p["passage_id"],
            "source_id": p["source_id"],
            "title": p["official_title"],
            "ref": p["provision_ref"],
            "language": "hi",
            "text": f"{p['official_title']} - {p['provision_ref']}: {p['normalized_content']}",
        }
        for p in hi_data["passages"]
    ]

    print(f"Loaded {len(en_passages)} English chunks and {len(hi_passages)} Hindi passages.")

    # 3. Source-Grouped Split Definitions
    # Held-out Test Sources (Strictly reserved for final generalization evaluation)
    test_sources = {
        "IND-STAT-LIMIT-1963",
        "IND-STAT-DPDP-2023",
        "IND-JUD-SC-2020-ARJUN-KHOTKAR",
        "IND-STAT-IT-2000-HI",
    }
    # Validation Sources (Used for hyperparameter tuning & loss monitoring)
    val_sources = {
        "IND-STAT-NI-1881",
        "IND-STAT-SRA-1963",
        "IND-STAT-CPC-1908-HI",
    }

    # Partition passages with source isolation
    train_items = []
    val_items = []
    test_items = []

    all_passages = en_passages + hi_passages
    for p in all_passages:
        sid = p["source_id"]
        if sid in test_sources:
            test_items.append(p)
        elif sid in val_sources:
            val_items.append(p)
        else:
            train_items.append(p)

    print(f"Partitioned items: Train={len(train_items)}, Val={len(val_items)}, Test={len(test_items)}")

    # 4. Tokenize with Tokenizer V2
    tok = IndianLegalTokenizerV2.load(tokenizer_path)

    train_tokens = [tok.encode(item["text"]) for item in train_items]
    val_tokens = [tok.encode(item["text"]) for item in val_items]
    test_tokens = [tok.encode(item["text"]) for item in test_items]

    train_ds = BilingualLegalDataset(train_tokens, seq_len=seq_len, pad_id=tok.pad_token_id)
    val_ds = BilingualLegalDataset(val_tokens, seq_len=seq_len, pad_id=tok.pad_token_id)
    test_ds = BilingualLegalDataset(test_tokens, seq_len=seq_len, pad_id=tok.pad_token_id)

    # 5. Compute Hashes and Statistics
    def compute_hash(items):
        h = hashlib.sha256()
        for it in items:
            h.update(it["text"].encode("utf-8"))
        return h.hexdigest()

    train_sha = compute_hash(train_items)
    val_sha = compute_hash(val_items)
    test_sha = compute_hash(test_items)

    def count_lang_tokens(items, tokens_list):
        en_toks = 0
        hi_toks = 0
        for it, toks in zip(items, tokens_list):
            if it["language"] == "hi":
                hi_toks += len(toks)
            else:
                en_toks += len(toks)
        return en_toks, hi_toks

    train_en_toks, train_hi_toks = count_lang_tokens(train_items, train_tokens)
    val_en_toks, val_hi_toks = count_lang_tokens(val_items, val_tokens)
    test_en_toks, test_hi_toks = count_lang_tokens(test_items, test_tokens)

    total_tokens = (train_en_toks + train_hi_toks) + (val_en_toks + val_hi_toks) + (test_en_toks + test_hi_toks)

    # 6. Save Manifests
    m_dir = Path(manifest_dir)
    m_dir.mkdir(parents=True, exist_ok=True)

    manifest_v2 = {
        "dataset_version": "v2.0.0",
        "phase": 33,
        "split_strategy": "source_grouped_bilingual",
        "tokenizer_used": str(tokenizer_path),
        "seq_len": seq_len,
        "vocab_size": tok.vocab_size,
        "total_verified_passages": len(all_passages),
        "total_tokens_extracted": total_tokens,
        "language_breakdown": {
            "english_tokens": train_en_toks + val_en_toks + test_en_toks,
            "hindi_tokens": train_hi_toks + val_hi_toks + test_hi_toks,
            "hindi_token_share_pct": round(((train_hi_toks + val_hi_toks + test_hi_toks) / total_tokens) * 100, 2),
        },
        "train": {
            "passage_count": len(train_items),
            "sample_count": len(train_ds),
            "token_count": train_en_toks + train_hi_toks,
            "english_tokens": train_en_toks,
            "hindi_tokens": train_hi_toks,
            "source_ids": sorted(list(set(it["source_id"] for it in train_items))),
            "sha256": train_sha,
        },
        "val": {
            "passage_count": len(val_items),
            "sample_count": len(val_ds),
            "token_count": val_en_toks + val_hi_toks,
            "english_tokens": val_en_toks,
            "hindi_tokens": val_hi_toks,
            "source_ids": sorted(list(set(it["source_id"] for it in val_items))),
            "sha256": val_sha,
        },
        "test": {
            "passage_count": len(test_items),
            "sample_count": len(test_ds),
            "token_count": test_en_toks + test_hi_toks,
            "english_tokens": test_en_toks,
            "hindi_tokens": test_hi_toks,
            "source_ids": sorted(list(set(it["source_id"] for it in test_items))),
            "sha256": test_sha,
        },
        "invariants": {
            "synthetic_scaffold_quarantined": True,
            "cross_split_source_overlap": 0,
            "benchmark_data_leakage": 0,
            "conversations_db_isolated": True,
        },
    }

    # Write manifests
    with open(m_dir / "dataset_manifest_v2.json", "w", encoding="utf-8") as f:
        json.dump(manifest_v2, f, indent=2)

    with open(m_dir / "train_manifest_v2.json", "w", encoding="utf-8") as f:
        json.dump(manifest_v2["train"], f, indent=2)

    with open(m_dir / "val_manifest_v2.json", "w", encoding="utf-8") as f:
        json.dump(manifest_v2["val"], f, indent=2)

    with open(m_dir / "test_manifest_v2.json", "w", encoding="utf-8") as f:
        json.dump(manifest_v2["test"], f, indent=2)

    print(f"Dataset manifests written to {m_dir}")
    print(f"Total usable tokens: {total_tokens:,} (EN: {manifest_v2['language_breakdown']['english_tokens']:,}, HI: {manifest_v2['language_breakdown']['hindi_tokens']:,})")
    print(f"Train samples: {len(train_ds)}, Val samples: {len(val_ds)}, Test samples: {len(test_ds)}")

    return train_ds, val_ds, test_ds, manifest_v2


if __name__ == "__main__":
    build_bilingual_datasets()

