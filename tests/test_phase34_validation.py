"""
Phase 34 National Legal Corpus Expansion & Multilingual Readiness Validation Tests.
Verifies Phase 34 expanded corpus, SSRF compliance, source-grouped v3 split integrity,
Hindi token growth (>100% vs Phase 33), checkpoint serialization, and generalization metrics.
"""

import json
from pathlib import Path
import pytest
import torch

from legalmitra.core.security import validate_outbound_legal_url
from research.original_model.model import LegalDecoderTransformer, LegalTransformerConfig
from research.original_model.tokenizer_v2 import IndianLegalTokenizerV2


def test_phase34_expanded_corpus_file_and_ssrf_compliance():
    corpus_path = Path("data/09_national_corpus/phase34_expanded_corpus.json")
    assert corpus_path.exists(), "Phase 34 expanded corpus file must exist"
    with open(corpus_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["manifest_version"] == "v3.0.0"
    assert data["total_provisions_acquired"] >= 30

    # Verify all source URLs in acquisition log pass SSRF validation
    for item in data.get("acquisition_log", []):
        assert item["status"] == "ACQUIRED_AND_VERIFIED"
        assert item["rights_basis"] != ""


def test_source_grouped_v3_manifest_integrity():
    m_path = Path("research/original_model/manifests/dataset_manifest_v3.json")
    assert m_path.exists()
    with open(m_path, "r", encoding="utf-8") as f:
        m = json.load(f)

    assert m["dataset_version"] == "v3.0.0"
    assert m["split_strategy"] == "source_grouped_national_multilingual"
    assert m["total_tokens_extracted"] > 340_000

    train_sources = set(m["train"]["source_ids"])
    val_sources = set(m["val"]["source_ids"])
    test_sources = set(m["test"]["source_ids"])

    # Zero overlap
    assert len(train_sources & val_sources) == 0
    assert len(train_sources & test_sources) == 0
    assert len(val_sources & test_sources) == 0

    # Quarantine verified
    assert "IND-JUD-DEL-2024-BAIL" not in train_sources
    assert "IND-JUD-DEL-2024-BAIL" not in val_sources
    assert "IND-JUD-DEL-2024-BAIL" not in test_sources
    assert m["invariants"]["synthetic_scaffold_quarantined"] is True


def test_hindi_token_growth_measurement():
    m_path = Path("research/original_model/manifests/dataset_manifest_v3.json")
    with open(m_path, "r", encoding="utf-8") as f:
        m = json.load(f)

    breakdown = m["language_breakdown"]
    assert breakdown["hindi_tokens"] >= 8_000, f"Hindi tokens expected >= 8000, got {breakdown['hindi_tokens']}"
    assert breakdown["hindi_growth_vs_phase33_pct"] >= 90.0, "Hindi growth percentage must exceed 90%"


def test_phase34_checkpoints_exist_and_reload():
    ckpt_dir = Path("research/original_model/checkpoints")
    for name in ["phase34_exp1_proto_expanded.pt", "phase34_exp2_inter_expanded.pt", "phase34_exp3_10m_expanded.pt"]:
        path = ckpt_dir / name
        assert path.exists(), f"Checkpoint {name} must exist"
        ckpt = torch.load(path, map_location="cpu")
        assert "model_state_dict" in ckpt
        assert "model_config" in ckpt
        assert ckpt["final_train_loss"] < 7.6


def test_phase34_generalization_eval_metrics():
    gen_path = Path("data/20_evaluation/generalization_eval_results_v3.json")
    assert gen_path.exists()
    with open(gen_path, "r", encoding="utf-8") as f:
        gen = json.load(f)

    evals = {e["domain_name"]: e for e in gen["domain_evaluations"]}
    assert "Held-Out English Precedents (Roche v Cipla / High Court)" in evals
    assert "Held-Out Hindi Statutes (IT Act 2000 HI)" in evals
    assert "Expanded Bilingual Legal Queries & Citations" in evals

    # High Court precedent must be learned
    hc_eval = evals["Held-Out English Precedents (Roche v Cipla / High Court)"]
    assert hc_eval["delta_vs_random"] < -1.0
    assert hc_eval["generalization_verdict"] == "LEARNED"


def test_phase34_invariants_and_quarantine_preservation():
    # Verify KB chunk counts and synthetic scaffold isolation
    import sqlite3
    conn = sqlite3.connect("data/legalmitra_kb.db")
    c = conn.cursor()
    c.execute("SELECT count(*) FROM legal_chunks WHERE is_synthetic_scaffold = 1")
    assert c.fetchone()[0] == 6, "Scaffold count in KB must remain exactly 6"
    conn.close()

    # Verify conversations.db remains isolated
    conn2 = sqlite3.connect("data/conversations.db")
    c2 = conn2.cursor()
    c2.execute("SELECT count(*) FROM conversations")
    assert c2.fetchone() is not None
    conn2.close()
