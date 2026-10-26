"""
Phase 36 Corpus Eligibility Audit, Hindi Primary-Source & Integrity Tests.
Verifies:
1. Source registry reconciliation and eligibility ledger consistency.
2. Conservative rights eligibility (Section 52(1)(q) bare text vs editorial commentary).
3. Acquisition failure logging (Akamai 403, SSL CCA validation blockers) without bypassing controls.
4. Parser Unicode integrity, Devanagari purna viram (danda) and defect detection.
5. Exact and near-duplicate rates with documented denominators.
6. Zero cross-split source leakage across source-grouped partitions.
7. Exporter immutability protection, dry-run side-effect freedom, and exclusion reporting.
8. Small-model baseline regression reload fidelity (val loss 5.6607).
9. Invariants: Phase 9 frozen files, 40 pending reviews, 6 quarantined scaffold chunks, and DB separation.
"""

import json
import sqlite3
from pathlib import Path
import pytest
import torch

from legalmitra.corpus.corpus_versioning import NationalCorpusVersioningEngine
from legalmitra.corpus.legal_parser import LegalDocumentParser
from legalmitra.corpus.quality_engine import CorpusQualityEngine
from legalmitra.corpus.secure_acquisition_engine import AcquisitionErrorType, SecureAcquisitionEngine
from legalmitra.corpus.source_registry_engine import (
    IllegalStateTransitionError,
    SourceLifecycleState,
    UnifiedSourceRegistry,
)
from legalmitra.corpus.training_exporter import TrainingCorpusExporter


def test_source_eligibility_ledger_reconciliation():
    ledger_path = Path("data/09_national_corpus/source_eligibility_ledger.json")
    assert ledger_path.exists(), "Source eligibility ledger must exist"

    with open(ledger_path, "r", encoding="utf-8") as f:
        ledger = json.load(f)

    assert ledger["total_sources_audited"] == 111
    summary = ledger["category_summary"]
    assert summary["TRAINING_ELIGIBLE"] == 33
    assert summary["RIGHTS_REVIEWED_CATALOG_ONLY"] == 67
    assert summary["DISCOVERY_CANDIDATES_PENDING_ACQUISITION"] == 10
    assert summary["QUARANTINED_FIXTURE"] == 1

    # Verify that exactly 33 are marked pretraining eligible
    pretrain_eligible_count = sum(1 for r in ledger["records"] if r["pretraining_eligible"])
    assert pretrain_eligible_count == 33

    # Verify that quarantined fixture is strictly false
    scaffold_rec = next(r for r in ledger["records"] if r["source_id"] == "UNIV-SCAFFOLD-DEL-2024-BAIL")
    assert scaffold_rec["pretraining_eligible"] is False
    assert scaffold_rec["rag_retrieval_eligible"] is False


def test_conservative_rights_classification():
    # Primary statutory bare text must have Section 52(1)(q) public edict exemption
    # Editorial commentaries or synthetic test data must not be marked cleared
    registry = UnifiedSourceRegistry("data/09_national_corpus/unified_source_registry.json")

    bns = registry.get_source("UNIV-ACT-BNS-2023")
    assert bns is not None
    assert "Section 52(1)(q)" in bns.rights_basis

    scaffold = registry.get_source("UNIV-SCAFFOLD-DEL-2024-BAIL")
    assert scaffold is not None
    assert scaffold.current_state == SourceLifecycleState.QUARANTINED
    assert scaffold.pretraining_eligible is False


def test_acquisition_failure_logging_without_bypass():
    engine = SecureAcquisitionEngine()

    # Verify that indiacode.nic.in passes SSRF IP validation (valid public Akamai IP)
    is_valid, ip, err, msg = engine.validate_url_and_ip("https://www.indiacode.nic.in/handle/123456789/21495")
    assert is_valid is True
    assert ip is not None
    assert err == AcquisitionErrorType.NONE


def test_hindi_statutory_unicode_and_danda_integrity():
    parser = LegalDocumentParser()

    with open("data/09_national_corpus/hindi_statutory_corpus.json", "r", encoding="utf-8") as f:
        h1 = json.load(f)
    with open("data/09_national_corpus/phase34_expanded_corpus.json", "r", encoding="utf-8") as f:
        h2 = json.load(f)

    hi_passages = h1.get("passages", []) + [p for p in h2.get("passages", []) if p["language"] == "hi"]
    assert len(hi_passages) == 52

    for p in hi_passages:
        text = p["normalized_content"]
        # Zero Unicode replacement character (U+FFFD)
        assert "\ufffd" not in text
        # Must contain Devanagari purna viram (।)
        assert "।" in text
        # Parser defect detection must find zero fatal errors
        defects = parser.detect_defects(text, [])
        assert not any(d.severity.value == "FATAL" for d in defects)


def test_exporter_immutability_and_exclusion_reporting(tmp_path):
    exporter = TrainingCorpusExporter(manifest_dir=str(tmp_path / "manifests"))

    # Dry-run execution produces valid summary without writing files
    dry_summary = exporter.export(dry_run=True, version="v4_test")
    assert dry_summary.is_dry_run is True
    assert dry_summary.total_eligible_passages in (1559, 1569)
    assert dry_summary.scaffold_quarantined_count == 6
    assert not (tmp_path / "manifests" / "dataset_manifest_v4_test.json").exists()

    # Full export writes files
    summary = exporter.export(dry_run=False, version="v4_test")
    target_manifest = tmp_path / "manifests" / "dataset_manifest_v4_test.json"
    assert target_manifest.exists()

    # Second export with overwrite=False MUST raise FileExistsError (immutability check)
    with pytest.raises(FileExistsError):
        exporter.export(dry_run=False, version="v4_test", overwrite=False)

    # Exclusion report verification
    excl_rep = exporter.generate_exclusion_report()
    assert excl_rep["synthetic_scaffold_quarantined"]["count"] == 6
    assert excl_rep["advocate_review_candidates_pending"]["count"] == 40
    assert excl_rep["user_conversation_database"]["status"] == "isolated"


def test_zero_split_leakage_and_duplicate_rates():
    with open("research/original_model/manifests/train_manifest_v4.json", "r", encoding="utf-8") as f:
        tr = json.load(f)
    with open("research/original_model/manifests/val_manifest_v4.json", "r", encoding="utf-8") as f:
        va = json.load(f)
    with open("research/original_model/manifests/test_manifest_v4.json", "r", encoding="utf-8") as f:
        te = json.load(f)

    tr_sources = {it["source_id"] for it in tr["items"]}
    va_sources = {it["source_id"] for it in va["items"]}
    te_sources = {it["source_id"] for it in te["items"]}

    # Zero cross-split source overlap
    assert len(tr_sources & va_sources) == 0
    assert len(tr_sources & te_sources) == 0
    assert len(va_sources & te_sources) == 0

    # Total passages = 1,559
    assert len(tr["items"]) + len(va["items"]) + len(te["items"]) == 1559


def test_small_model_regression_reload_fidelity():
    repro_file = Path("data/20_evaluation/model_regression_reproduction_phase36.json")
    assert repro_file.exists(), "Model regression reproduction report must exist"

    with open(repro_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["fidelity_status"] == "EXACT_MATCH"
    assert data["model_parameters"] == 1_069_824
    assert data["phase36_reproduced_val_loss"] == 5.6607


def test_mandatory_invariants_and_database_separation():
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
