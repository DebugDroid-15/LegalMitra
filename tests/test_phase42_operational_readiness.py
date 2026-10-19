"""Unit and integration tests for Phase 42 Operational Readiness.

Covers:
1. Authorized eCourts Adapter & semantic vs syntactic CNR validation.
2. Real-world scanned Hindi OCR benchmark evaluation & conservative normalization.
3. Controlled High Court connector pilot preflight checks and fixture fallback.
4. Corpus reconciliation layer integrity and physical database separation.
5. Invariant enforcement (synthetic chunk quarantine, review packages pending).
"""

import json
import os
import sqlite3
import pytest

from legalmitra.judicial.connectors.bombay_high_court_connector import (
    BombayHighCourtConnector,
)
from legalmitra.judicial.connectors.connector_base import (
    RateLimiter,
    SourceDocumentState,
    SSRFProtectionError,
)
from legalmitra.judicial.connectors.delhi_high_court_connector import (
    DelhiHighCourtConnector,
)
from legalmitra.judicial.devanagari_ocr import (
    DevanagariOCREngine,
    DevanagariOCRResult,
)
from legalmitra.judicial.ecourts_adapter import (
    AuthorizedECourtsAdapter,
    ECourtsAccessMode,
    ECourtsAdapterStatus,
    ECourtsCredentials,
)
from legalmitra.judicial.ecourts_protocol import (
    CNRDecomposition,
    ECourtsProtocolValidator,
    ECourtsWorkflowStage,
)
from scripts.evaluate_real_world_ocr import evaluate_benchmark
from scripts.reconcile_phase42_corpus import run_reconciliation
from scripts.run_controlled_high_court_pilot import (
    execute_controlled_pilot,
    run_preflight_checks,
)


# --- 1. Authorized eCourts Adapter & CNR Semantics Tests ---

def test_ecourts_adapter_staging_mode_default():
    adapter = AuthorizedECourtsAdapter()
    assert adapter.is_authorized_live is False
    assert adapter.status == ECourtsAdapterStatus.ACTIVE_STAGING


def test_ecourts_adapter_blocks_unauthorized_live_fetch():
    adapter = AuthorizedECourtsAdapter()
    # Attempting to fetch an un-staged CNR without credentials returns explicit blocker
    res = adapter.fetch_case_by_cnr("DLTH019999992023")
    assert res["status"] == "BLOCKED_PENDING_ECOMMITTEE_CREDENTIALS"
    assert res["is_authorized_live"] is False
    assert "CAPTCHA bypass is strictly prohibited" in res["message"]


def test_ecourts_adapter_retrieves_from_authorized_staging():
    adapter = AuthorizedECourtsAdapter()
    res = adapter.fetch_case_by_cnr("DLTH010012342023")
    assert res["status"] == "RETRIEVED_FROM_AUTHORIZED_STAGING"
    assert res["record"] is not None
    assert res["record"]["cnr_number"] == "DLTH010012342023"


def test_ecourts_cnr_semantic_validation_valid():
    validator = ECourtsProtocolValidator()
    res = validator.validate_cnr_semantic("DLTH010012342023")
    assert res["is_syntactically_valid"] is True
    assert res["is_semantically_valid"] is True
    assert res["decomposition"]["state_code"] == "DL"


def test_ecourts_cnr_semantic_validation_invalid_state():
    validator = ECourtsProtocolValidator()
    # State code 'ZZ' is not in the official state registry
    res = validator.validate_cnr_semantic("ZZTH010012342023")
    assert res["is_syntactically_valid"] is True
    assert res["is_semantically_valid"] is False
    assert "not recognized in CIS registry" in res["reason"]


def test_ecourts_adapter_semantic_validation_out_of_range_year():
    adapter = AuthorizedECourtsAdapter()
    # Year 1960 is syntactically within 1950-2030, but outside computerized CIS archive window (>=1980)
    sem_res = adapter.validate_cnr_semantic("DLTH010012341960")
    assert sem_res.is_syntactically_valid is True
    assert sem_res.is_semantically_verified is False
    assert "outside CIS computerized archive window" in sem_res.status_reason


# --- 2. Real-World Scanned Hindi OCR Benchmark Tests ---

def test_scanned_hindi_ocr_benchmark_integrity():
    manifest_path = os.path.join(
        "data", "21_judicial_infrastructure", "scanned_hindi_ocr_benchmark", "benchmark_manifest.json"
    )
    assert os.path.exists(manifest_path)
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["metadata"]["total_staged_pages"] == 12
    assert len(data["pages"]) == 12


def test_scanned_hindi_ocr_evaluation_metrics():
    manifest_path = os.path.join(
        "data", "21_judicial_infrastructure", "scanned_hindi_ocr_benchmark", "benchmark_manifest.json"
    )
    res = evaluate_benchmark(manifest_path)
    assert res["total_pages_evaluated"] == 12
    # Realistic normalized CER should be under 5% (1.42% measured)
    assert res["avg_cer_normalized"] < 0.05
    # Realistic normalized WER should be under 8% (2.64% measured)
    assert res["avg_wer_normalized"] < 0.08
    # Legal token sensitivity should be high (>= 95%)
    assert res["legal_token_sensitivity"] >= 0.95


def test_devanagari_ocr_anusvara_normalization():
    engine = DevanagariOCREngine()
    # Anusvara normalization test: chandrabindu before consonant is normalized to anusvara
    raw = "सँविधान और सँरक्षण"
    res = engine.normalize(raw)
    assert "संविधान" in res.normalized_text
    assert "संरक्षण" in res.normalized_text


# --- 3. Controlled High Court Connector Pilot Tests ---

def test_high_court_pilot_preflight_checks():
    preflight = run_preflight_checks()
    assert preflight["preflight_status"] == "PASS"
    assert preflight["ssrf_protection_verified"] is True
    assert preflight["delhi_domain_whitelisted"] is True
    assert preflight["bombay_domain_whitelisted"] is True


def test_high_court_pilot_controlled_fixture_execution():
    pilot_res = execute_controlled_pilot(live_authorized=False, batch_size=2)
    assert pilot_res["mode"] == "CONTROLLED_FIXTURE_DRY_RUN"
    assert len(pilot_res["records_acquired"]) == 4  # 2 for Delhi, 2 for Bombay
    assert any(b["code"] == "LIVE_PERMISSION_UNVERIFIED" for b in pilot_res["blockers_encountered"])
    for rec in pilot_res["records_acquired"]:
        assert rec["is_fixture"] is True


# --- 4. Corpus Reconciliation & Database Separation Tests ---

def test_phase42_corpus_reconciliation():
    summary = run_reconciliation()
    assert summary["macro_institutional_catalog"]["total_catalogued_records"] == 615
    assert summary["macro_institutional_catalog"]["institutions_tracked"] == 19
    assert summary["granular_manifests"]["total_granular_manifest_records"] == 134
    assert summary["granular_manifests"]["staged_ecourts_records"] == 6
    assert summary["granular_manifests"]["staged_scanned_hindi_ocr_pages"] == 12
    assert summary["physical_sqlite_knowledge_base"]["registered_sources"] == 59
    assert summary["physical_sqlite_knowledge_base"]["landmark_case_briefs"] == 16
    assert summary["physical_sqlite_knowledge_base"]["judicial_documents"] == 9
    assert summary["physical_sqlite_knowledge_base"]["total_text_chunks"] == 1505
    assert summary["physical_sqlite_knowledge_base"]["quarantined_synthetic_chunks"] == 6
    assert summary["database_isolation"]["is_physically_separated"] is True


def test_database_isolation_no_cross_contamination():
    conv_con = sqlite3.connect("data/conversations.db")
    cur = conv_con.cursor()
    tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    conv_con.close()
    assert "legal_chunks" not in tables
    assert "sources" not in tables
    assert "cases" not in tables


def test_independent_benchmark_v4_cases():
    v4_path = os.path.join(
        "data", "21_judicial_infrastructure", "independent_judicial_benchmark_v4.json"
    )
    assert os.path.exists(v4_path)
    with open(v4_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["total_test_cases"] == 56
    assert len(data["cases"]) == 56

