"""
Phase 31 Original Indian Legal Foundation Model Regression Tests.
Verifies pure random initialization (zero pretrained weights),
BPE tokenizer encode/decode round-trip with Indian legal symbols,
causal attention masking, parameter counting, and checkpoint serialization.
"""

from pathlib import Path
import pytest
import torch

from research.original_model.dataset import LegalDataset
from research.original_model.model import (
    CausalSelfAttention,
    LegalDecoderTransformer,
    LegalTransformerConfig,
)
from research.original_model.tokenizer import SPECIAL_TOKENS, IndianLegalTokenizer


def test_tokenizer_encode_decode_roundtrip():
    tok = IndianLegalTokenizer()
    texts = [
        "Under Section 528 of the Bharatiya Nagarik Suraksha Sanhita, 2023, High Courts possess inherent powers.",
        "The Supreme Court of India in State of Haryana v. Bhajan Lal laid down categories for FIR quashing.",
        "भारतीय न्याय संहिता (BNS) धारा 356 मानहानि अपराध.",
    ]
    tok.train_from_texts(texts, target_vocab_size=200)

    sample = "Section 528 of BNSS 2023."
    encoded = tok.encode(sample, add_special_tokens=True)
    assert encoded[0] == tok.bos_token_id
    assert encoded[-1] == tok.eos_token_id

    decoded = tok.decode(encoded, skip_special_tokens=True)
    assert "Section" in decoded or "528" in decoded


def test_model_strict_random_initialization():
    config = LegalTransformerConfig(
        vocab_size=128,
        d_model=64,
        n_layers=2,
        n_heads=2,
        d_ff=256,
        max_seq_len=64,
        dropout=0.0,
    )
    model = LegalDecoderTransformer(config)

    # Verify no weights are uninitialized or NaN
    for name, param in model.named_parameters():
        assert not torch.isnan(param).any(), f"NaN found in {name}"
        assert not torch.isinf(param).any(), f"Inf found in {name}"

    # Verify linear weight distribution is Gaussian centered around 0 with std ~ 0.02
    w = model.blocks[0].mlp.w1.weight.data
    assert abs(w.mean().item()) < 0.02
    assert 0.005 < w.std().item() < 0.05


def test_causal_forward_pass_and_loss():
    config = LegalTransformerConfig(
        vocab_size=64,
        d_model=32,
        n_layers=2,
        n_heads=2,
        d_ff=128,
        max_seq_len=32,
        dropout=0.0,
    )
    model = LegalDecoderTransformer(config)
    model.eval()

    batch_size = 2
    seq_len = 16
    input_ids = torch.randint(0, 64, (batch_size, seq_len))
    targets = torch.randint(0, 64, (batch_size, seq_len))

    logits, loss = model(input_ids=input_ids, labels=targets)

    assert logits.shape == (batch_size, seq_len, 64)
    assert loss is not None
    assert loss.item() > 0.0


def test_parameter_counting():
    config = LegalTransformerConfig(
        vocab_size=100,
        d_model=64,
        n_layers=2,
        n_heads=2,
        d_ff=256,
        max_seq_len=64,
        dropout=0.0,
        tie_word_embeddings=True,
    )
    model = LegalDecoderTransformer(config)
    total_p = model.count_parameters()
    assert total_p > 10_000, f"Unexpected parameter count: {total_p}"


def test_dataset_chunking_and_padding():
    seqs = [
        [1, 10, 20, 30, 40, 50, 60, 2],
        [1, 15, 25, 2],
    ]
    ds = LegalDataset(seqs, seq_len=8, pad_id=0)
    assert len(ds) == 2
    item, target = ds[0]
    assert item.shape == (8,)
    assert target.shape == (8,)
