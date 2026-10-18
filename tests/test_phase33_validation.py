"""
Phase 33 Bilingual Legal Corpus Engineering & 10M Model Validation Tests.
Verifies Bilingual Pipeline, Tokenizer V2 whitespace restoration & Hindi merges,
source-grouped bilingual split integrity, model scaling parameter counts,
and checkpoint serialization.
"""

import json
from pathlib import Path
import pytest
import torch

from research.original_model.bilingual_pipeline import BilingualLegalPipeline
from research.original_model.tokenizer_v2 import IndianLegalTokenizerV2
from research.original_model.model import LegalDecoderTransformer, LegalTransformerConfig


def test_bilingual_pipeline_nfc_and_devanagari():
    pipeline = BilingualLegalPipeline()
    sample_text = "धारा 528\tउच्च न्यायालय\r\nकी अंतर्निहित शक्तियां   Article 21."
    norm = pipeline.normalize_text(sample_text)
    assert "\t" not in norm
    assert "\r" not in norm
    assert "धारा 528" in norm
    assert "Article 21" in norm

    lang = pipeline.detect_language(norm)
    assert lang == "mixed"

    cites = pipeline.extract_citations(norm)
    assert len(cites["hindi_citations"]) >= 1
    assert len(cites["english_citations"]) >= 1


def test_tokenizer_v2_whitespace_and_hindi_no_unk():
    tok_path = Path("research/original_model/tokenizer_v2.json")
    assert tok_path.exists(), "Tokenizer V2 file must exist"
    tok = IndianLegalTokenizerV2.load(tok_path)

    # Test Hindi legal sentence
    text_hi = "धारा 528 उच्च न्यायालय की अंतर्निहित शक्तियां"
    tokens = tok.encode(text_hi, add_special_tokens=False)
    assert tok.unk_token_id not in tokens, "Hindi legal text must not contain unk tokens in V2"

    decoded = tok.decode(tokens, skip_special_tokens=True)
    # Whitespace must be preserved
    assert "धारा 528" in decoded
    assert "उच्च न्यायालय" in decoded
    assert " " in decoded, "Spaces between words must be restored"


def test_source_grouped_bilingual_split_integrity():
    manifest_path = Path("research/original_model/manifests/dataset_manifest_v2.json")
    assert manifest_path.exists()
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    train_sources = set(data["train"]["source_ids"])
    val_sources = set(data["val"]["source_ids"])
    test_sources = set(data["test"]["source_ids"])

    # Invariant: Zero overlap
    assert len(train_sources & val_sources) == 0, "Train and Val sources must have 0 overlap"
    assert len(train_sources & test_sources) == 0, "Train and Test sources must have 0 overlap"
    assert len(val_sources & test_sources) == 0, "Val and Test sources must have 0 overlap"

    # Invariant: Scaffold excluded
    assert "IND-JUD-DEL-2024-BAIL" not in train_sources
    assert "IND-JUD-DEL-2024-BAIL" not in val_sources
    assert "IND-JUD-DEL-2024-BAIL" not in test_sources
    assert data["invariants"]["synthetic_scaffold_quarantined"] is True


def test_model_scaling_parameter_accounting():
    tok_v2 = IndianLegalTokenizerV2.load("research/original_model/tokenizer_v2.json")
    v_size = tok_v2.vocab_size

    # Prototype ~1.0M
    c_proto = LegalTransformerConfig(vocab_size=v_size, d_model=128, n_layers=4, n_heads=4, d_ff=512, max_seq_len=128, pad_token_id=tok_v2.pad_token_id)
    m_proto = LegalDecoderTransformer(c_proto)
    p_proto = m_proto.count_parameters()
    assert 900_000 < p_proto < 1_200_000, f"Prototype parameter count unexpected: {p_proto}"

    # Intermediate ~4.5M
    c_inter = LegalTransformerConfig(vocab_size=v_size, d_model=256, n_layers=5, n_heads=4, d_ff=1024, max_seq_len=128, pad_token_id=tok_v2.pad_token_id)
    m_inter = LegalDecoderTransformer(c_inter)
    p_inter = m_inter.count_parameters()
    assert 4_000_000 < p_inter < 5_000_000, f"Intermediate parameter count unexpected: {p_inter}"

    # Target 10M
    c_10m = LegalTransformerConfig(vocab_size=v_size, d_model=320, n_layers=8, n_heads=8, d_ff=1280, max_seq_len=128, pad_token_id=tok_v2.pad_token_id)
    m_10m = LegalDecoderTransformer(c_10m)
    p_10m = m_10m.count_parameters()
    assert 10_000_000 < p_10m < 11_500_000, f"Target 10M parameter count unexpected: {p_10m}"


def test_phase33_checkpoints_exist_and_reload():
    ckpt_dir = Path("research/original_model/checkpoints")
    for name in ["phase33_exp_a_baseline_reproduction.pt", "phase33_exp_d_multilingual_joint.pt"]:
        path = ckpt_dir / name
        assert path.exists(), f"Checkpoint {name} must exist"
        ckpt = torch.load(path, map_location="cpu")
        assert "model_state_dict" in ckpt
        assert "model_config" in ckpt
        assert ckpt["final_train_loss"] < ckpt["model_config"].get("initial_train_loss", 10.0)


def test_corpus_inventory_and_rights_audit_metrics():
    inv_path = Path("data/20_evaluation/corpus_inventory_v1.json")
    assert inv_path.exists()
    with open(inv_path, "r", encoding="utf-8") as f:
        inv = json.load(f)

    summary = inv["summary"]
    assert summary["quarantined_scaffold_chunks"] == 6
    assert summary["active_verified_chunks"] == 1499
    assert summary["eligible_pretraining_sources"] == 57
    assert summary["excluded_sources"] == 2

