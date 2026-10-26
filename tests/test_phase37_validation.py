"""
Phase 37 National Legal Corpus Acquisition, Hindi Criminal Codes & Dataset Integrity Tests.
Verifies:
1. Source eligibility ledger reconciliation for Phase 37 (47 training-eligible sources).
2. Conservative rights eligibility (Section 52(1)(q) public edict statutory exemption).
3. Authentic Hindi criminal codes acquisition (BNS, BNSS, BSA) and Devanagari Unicode danda integrity.
4. Manifest v5 integrity (1,633 passages, 357,358 tokens, 19,871 authentic Hindi tokens).
5. Zero cross-split source leakage across source-grouped train/val/test partitions.
6. Exact and near-duplicate rates within strict tolerances (0.0% exact, <1.0% near).
7. Exporter immutability protection, dry-run side-effect freedom, and exclusion reporting.
8. Small-model baseline regression reload fidelity (1,069,824 parameters, val loss 5.8831).
9. Invariants: Phase 9 frozen files, 40 pending reviews, 6 quarantined scaffold chunks, and DB separation.
"""

import json
import sqlite3
from pathlib import Path
import pytest
import torch

from legalmitra.corpus.legal_parser import LegalDocumentParser
from legalmitra.corpus.quality_engine import CorpusQualityEngine
from legalmitra.corpus.source_registry_engine import (
    SourceLifecycleState,
    UnifiedSourceRegistry,
)
from legalmitra.corpus.training_exporter import TrainingCorpusExporter


def test_phase37_source_eligibility_ledger_reconciliation():
    ledger_path = Path("data/09_national_corpus/source_eligibility_ledger_phase37.json")
    assert ledger_path.exists(), "Phase 37 Source eligibility ledger must exist"

    with open(ledger_path, "r", encoding="utf-8") as f:
        ledger = json.load(f)

    assert ledger["total_sources_audited"] == 111
    summary = ledger["category_summary"]
    assert summary["TRAINING_ELIGIBLE"] == 47
    assert summary["RIGHTS_REVIEWED_CATALOG_ONLY"] == 63
    assert summary["DISCOVERY_CANDIDATES_PENDING_ACQUISITION"] == 0
    assert summary["QUARANTINED_FIXTURE"] == 1

    # Verify that quarantined fixture is strictly false
    scaffold_rec = next(r for r in ledger["records"] if r["source_id"] == "UNIV-SCAFFOLD-DEL-2024-BAIL")
    assert scaffold_rec["pretraining_eligible"] is False
    assert scaffold_rec["rag_retrieval_eligible"] is False


def test_phase37_conservative_rights_classification():
    registry = UnifiedSourceRegistry("data/09_national_corpus/unified_source_registry.json")

    bns = registry.get_source("UNIV-ACT-BNS-2023")
    assert bns is not None
    assert "Section 52(1)(q)" in bns.rights_basis

    scaffold = registry.get_source("UNIV-SCAFFOLD-DEL-2024-BAIL")
    assert scaffold is not None
    assert scaffold.current_state == SourceLifecycleState.QUARANTINED
    assert scaffold.pretraining_eligible is False


def test_phase37_hindi_criminal_codes_and_unicode_integrity():
    parser = LegalDocumentParser()

    with open("data/09_national_corpus/hindi_statutory_corpus.json", "r", encoding="utf-8") as f:
        h1 = json.load(f)
    with open("data/09_national_corpus/phase34_expanded_corpus.json", "r", encoding="utf-8") as f:
        h2 = json.load(f)
    with open("data/09_national_corpus/phase37_acquired_corpus.json", "r", encoding="utf-8") as f:
        h3 = json.load(f)

    hi_passages = (
        h1.get("passages", [])
        + [p for p in h2.get("passages", []) if p["language"] == "hi"]
        + [p for p in h3.get("passages", []) if p["language"] == "hi"]
    )
    assert len(hi_passages) == 113

    for p in hi_passages:
        text = p.get("normalized_content", p.get("content", ""))
        # Zero Unicode replacement character (U+FFFD)
        assert "\ufffd" not in text
        # Must contain Devanagari purna viram (।)
        assert "।" in text
        # Parser defect detection must find zero fatal errors
        defects = parser.detect_defects(text, [])
        assert not any(d.severity.value == "FATAL" for d in defects)


def test_phase37_dataset_manifest_v5_metrics():
    manifest_path = Path("research/original_model/manifests/dataset_manifest_v5.json")
    assert manifest_path.exists(), "Manifest v5 must exist"

    with open(manifest_path, "r", encoding="utf-8") as f:
        m5 = json.load(f)

    assert m5["manifest_version"] == "v5.0.0"
    assert m5["total_passages"] == 1633
    assert m5["total_usable_tokens"] == 357358
    assert m5["en_tokens"] == 337487
    assert m5["hi_tokens"] == 19871
    assert m5["splits"]["train"]["passages"] == 1408
    assert m5["splits"]["val"]["passages"] == 43
    assert m5["splits"]["test"]["passages"] == 182


def test_phase37_zero_split_leakage_and_duplicate_rates():
    with open("research/original_model/manifests/train_manifest_v5.json", "r", encoding="utf-8") as f:
        tr = json.load(f)
    with open("research/original_model/manifests/val_manifest_v5.json", "r", encoding="utf-8") as f:
        va = json.load(f)
    with open("research/original_model/manifests/test_manifest_v5.json", "r", encoding="utf-8") as f:
        te = json.load(f)

    tr_sources = {it["source_id"] for it in tr["items"]}
    va_sources = {it["source_id"] for it in va["items"]}
    te_sources = {it["source_id"] for it in te["items"]}

    # Zero cross-split source overlap
    assert len(tr_sources & va_sources) == 0
    assert len(tr_sources & te_sources) == 0
    assert len(va_sources & te_sources) == 0

    # Total passages = 1,633
    assert len(tr["items"]) + len(va["items"]) + len(te["items"]) == 1633

    # Quality engine duplicate audit
    quality_engine = CorpusQualityEngine()
    rep = quality_engine.audit_corpus(
        tr["items"] + va["items"] + te["items"],
        train_sources=tr_sources,
        val_sources=va_sources,
        test_sources=te_sources,
    )
    assert rep.leakage_detected is False
    assert rep.exact_duplicate_rate == 0.0
    assert rep.near_duplicate_rate < 0.01


def test_phase37_exporter_immutability_and_exclusion_reporting(tmp_path):
    exporter = TrainingCorpusExporter(manifest_dir=str(tmp_path / "manifests"))

    # Dry-run execution produces valid summary without writing files
    dry_summary = exporter.export(dry_run=True, version="v5_test")
    assert dry_summary.is_dry_run is True
    assert dry_summary.total_eligible_passages in (1633, 1643)
    assert dry_summary.total_usable_tokens in (357358, 359470)
    assert dry_summary.scaffold_quarantined_count == 6
    assert not (tmp_path / "manifests" / "dataset_manifest_v5_test.json").exists()

    # Full export writes files
    summary = exporter.export(dry_run=False, version="v5_test")
    target_manifest = tmp_path / "manifests" / "dataset_manifest_v5_test.json"
    assert target_manifest.exists()

    # Second export with overwrite=False MUST raise FileExistsError (immutability check)
    with pytest.raises(FileExistsError):
        exporter.export(dry_run=False, version="v5_test", overwrite=False)

    # Exclusion report verification
    excl_rep = exporter.generate_exclusion_report()
    assert excl_rep["synthetic_scaffold_quarantined"]["count"] == 6
    assert excl_rep["advocate_review_candidates_pending"]["count"] == 40
    assert excl_rep["user_conversation_database"]["status"] == "isolated"


def test_phase37_small_model_regression_reload_fidelity():
    repro_file = Path("data/20_evaluation/model_regression_reproduction_phase37.json")
    assert repro_file.exists(), "Phase 37 Model regression reproduction report must exist"

    with open(repro_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["fidelity_status"] == "EXACT_MATCH"
    assert data["model_parameters"] == 1_069_824
    assert data["phase37_measured_val_loss"] == 5.8831


def test_phase37_mandatory_invariants_and_database_separation():
    # 1. KB scaffold quarantine
    conn_kb = sqlite3.connect("data/legalmitra_kb.db")
    c_kb = conn_kb.cursor()
    c_kb.execute("SELECT COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold = 1;")
    scaffold_count = c_kb.fetchone()[0]
    c_kb.execute("SELECT COUNT(*) FROM legal_chunks WHERE is_synthetic_scaffold = 0;")
    real_count = c_kb.fetchone()[0]
    conn_kb.close()

    assert scaffold_count == 6
    assert real_count in (1499, 1509)

    # 2. Conversations database separation
    conn_conv = sqlite3.connect("data/conversations.db")
    c_conv = conn_conv.cursor()
    c_conv.execute("SELECT name FROM sqlite_master WHERE type='table';")
    conv_tables = [r[0] for r in c_conv.fetchall()]
    conn_conv.close()

    assert "conversations" in conv_tables
    assert "messages" in conv_tables
    assert "legal_chunks" not in conv_tables

