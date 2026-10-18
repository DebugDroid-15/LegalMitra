"""
Indian Legal Corpus Dataset Builder for Original Foundation Model Research.
Loads verified legal chunks from SQLite (quarantining synthetic scaffolds),
tokenizes using IndianLegalTokenizer, performs deterministic 90/10 split,
and creates PyTorch datasets with SHA256 manifest.
"""

import sys
from pathlib import Path

# Ensure repo root is on sys.path
_repo_root = str(Path(__file__).resolve().parent.parent.parent)
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

import hashlib
import json
import sqlite3
from typing import Dict, List, Optional, Tuple

import torch
from torch.utils.data import Dataset

from research.original_model.tokenizer import IndianLegalTokenizer


class LegalDataset(Dataset):
    """PyTorch Dataset yielding input_ids and target labels for next-token prediction."""

    def __init__(self, tokenized_sequences: List[List[int]], seq_len: int = 128, pad_id: int = 0):
        self.seq_len = seq_len
        self.pad_id = pad_id
        self.samples: List[torch.Tensor] = []

        for seq in tokenized_sequences:
            if len(seq) < 4:
                continue
            # Chunk or pad into seq_len chunks
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


def extract_verified_legal_texts(db_path: str = "data/legalmitra_kb.db") -> List[Dict[str, str]]:
    """Extract verified non-synthetic chunks from legal knowledge base."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Quarantine synthetic scaffold strictly: is_synthetic_scaffold must be 0
    query = """
        SELECT chunk_id, act_or_case_title, provision_or_para_ref, content
        FROM legal_chunks
        WHERE is_synthetic_scaffold = 0
        ORDER BY chunk_id ASC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "chunk_id": row["chunk_id"],
            "title": row["act_or_case_title"],
            "ref": row["provision_or_para_ref"],
            "text": f"{row['act_or_case_title']} - {row['provision_or_para_ref']}: {row['content']}",
        }
        for row in rows
    ]


def build_train_val_datasets(
    db_path: str = "data/legalmitra_kb.db",
    tokenizer: Optional[IndianLegalTokenizer] = None,
    tokenizer_path: str = "research/original_model/tokenizer.json",
    manifest_path: str = "research/original_model/dataset_manifest.json",
    train_ratio: float = 0.9,
    seq_len: int = 128,
    target_vocab_size: int = 1024,
) -> Tuple[LegalDataset, LegalDataset, IndianLegalTokenizer, Dict]:
    """Package database text into train/val datasets with deterministic split."""
    chunks = extract_verified_legal_texts(db_path)
    texts = [c["text"] for c in chunks]

    # Train or load tokenizer
    if tokenizer is None:
        tok_file = Path(tokenizer_path)
        if tok_file.exists():
            tokenizer = IndianLegalTokenizer.load(tok_file)
        else:
            tokenizer = IndianLegalTokenizer()
            # Sample evenly distributed chunks across statutes and judgments for vocabulary extraction
            sample_texts = texts[::15]
            tokenizer.train_from_texts(sample_texts, target_vocab_size=target_vocab_size)
            tokenizer.save(tok_file)

    # Deterministic split (deterministic ordering)
    split_idx = int(len(texts) * train_ratio)
    train_texts = texts[:split_idx]
    val_texts = texts[split_idx:]

    train_tokens = [tokenizer.encode(t) for t in train_texts]
    val_tokens = [tokenizer.encode(t) for t in val_texts]

    train_ds = LegalDataset(train_tokens, seq_len=seq_len, pad_id=tokenizer.pad_token_id)
    val_ds = LegalDataset(val_tokens, seq_len=seq_len, pad_id=tokenizer.pad_token_id)

    # Calculate corpus hash
    hasher = hashlib.sha256()
    for t in texts:
        hasher.update(t.encode("utf-8"))
    corpus_sha256 = hasher.hexdigest()

    total_tokens = sum(len(toks) for toks in train_tokens) + sum(len(toks) for toks in val_tokens)

    manifest = {
        "corpus_sha256": corpus_sha256,
        "total_verified_chunks": len(chunks),
        "total_tokens_extracted": total_tokens,
        "train_chunks_count": len(train_texts),
        "val_chunks_count": len(val_texts),
        "train_samples_count": len(train_ds),
        "val_samples_count": len(val_ds),
        "seq_len": seq_len,
        "vocab_size": tokenizer.vocab_size,
        "synthetic_scaffold_quarantined": True,
    }

    m_path = Path(manifest_path)
    m_path.parent.mkdir(parents=True, exist_ok=True)
    with open(m_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    return train_ds, val_ds, tokenizer, manifest
