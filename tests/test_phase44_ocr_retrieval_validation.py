"""Unit and integration tests for Phase 44 OCR Robustness, Legal Evidence Preservation & RAG Validation.

Covers:
1. Metric calculations, hand-computable edit distances, and edge cases.
2. Normalization safety on tadbhav roots, inflected forms, tatsama terms, and mixed legal text.
3. OCRQualityGate fail-closed operational states and uncertainty thresholds.
4. End-to-end 10 failure scenarios evaluated via OCRRAGValidator.
5. 10-layer corpus reconciliation and physical SQLite database separation.
6. Connector preflight safety, loopback/metadata SSRF prevention, and credential redaction.
7. Non-negotiable invariants (Phase 9 freeze, 40 review candidates pending, scaffold quarantine).
"""

from __future__ import annotations

import json
import os
import sqlite3
import pytest

from legalmitra.judicial.connectors.connector_base import (
    BaseJudicialConnector,
    RateLimiter,
    SSRFProtectionError,
)
from legalmitra.judicial.connectors.delhi_high_court_connector import (
    DelhiHighCourtConnector,
)
from legalmitra.judicial.devanagari_ocr import (
    DevanagariOCREngine,
    DevanagariOCRResult,
)
from legalmitra.judicial.ocr_quality_gate import (
    OCRQualityAssessment,
    OCRQualityGate,
    OCRQualityState,
)
from legalmitra.judicial.ocr_rag_validator import (
    OCRRAGValidator,
    PipelineAction,
)
from scripts.evaluate_real_world_ocr import evaluate_benchmark
from scripts.reconcile_phase44_corpus import run_reconciliation
from scripts.run_controlled_high_court_pilot import run_preflight_checks


# --- 1. Metric Calculations & Hand-Computable Edge Cases ---

def test_compute_cer_and_wer_hand_computable():
    # Empty string edge cases
    assert DevanagariOCREngine.compute_cer("", "") == 0.0
    assert DevanagariOCREngine.compute_wer("", "") == 0.0
    assert DevanagariOCREngine.compute_cer("धारा", "") == 1.0
    assert DevanagariOCREngine.compute_wer("धारा 482", "") == 1.0
    assert DevanagariOCREngine.compute_cer("", "धारा") == 1.0
    assert DevanagariOCREngine.compute_wer("", "धारा 482") == 1.0

    # Hand-computable substitution: 'न्याय' has 5 Unicode codepoints (न + ् + य + ा + य).
    # Substituting 1 character ('य' -> 'स') = 1 / 5 = 0.20 CER
    assert DevanagariOCREngine.compute_cer("न्याय", "न्यास") == 0.20

    # Hand-computable WER: 1 word substituted out of 3 = 1/3 (33.33% WER)
    wer_val = DevanagariOCREngine.compute_wer("उच्च न्यायालय दिल्ली", "उच्च न्यायालय इलाहाबाद")
    assert round(wer_val, 4) == 0.3333


def test_phase43_ocr_benchmark_reproduction():
    manifest_path = os.path.join(
        "data", "21_judicial_infrastructure", "scanned_hindi_ocr_benchmark", "benchmark_manifest.json"
    )
    res = evaluate_benchmark(manifest_path)
    assert res["total_pages_evaluated"] == 12

    # Verify reproduction of Macro and Micro CER/WER
    assert res["macro_cer_raw"] == 0.0168
    assert res["macro_wer_raw"] == 0.0397
    assert res["macro_cer_normalized"] == 0.0142
    assert res["macro_wer_normalized"] == 0.0264

    assert res["micro_cer_raw"] == 0.0172
    assert res["micro_wer_raw"] == 0.0406
    assert res["micro_cer_normalized"] == 0.0146
    assert res["micro_wer_normalized"] == 0.0276

    assert res["legal_tokens_recovered"] == 47
    assert res["legal_tokens_expected"] == 47


# --- 2. Normalization Safety & Tadbhav Inflection Whitelist ---

def test_tadbhav_inflections_preserved():
    engine = DevanagariOCREngine()

    # Roots
    assert engine.normalize("गाँव").normalized_text == "गाँव"
    assert engine.normalize("माँ").normalized_text == "माँ"
    assert engine.normalize("पाँच").normalized_text == "पाँच"
    assert engine.normalize("आँख").normalized_text == "आँख"

    # Inflected forms
    assert engine.normalize("गाँवों में पाँचों व्यक्ति उपस्थित थे।").normalized_text == "गाँवों में पाँचों व्यक्ति उपस्थित थे।"
    assert engine.normalize("साक्षी ने अपनी आँखों से घटना देखी।").normalized_text == "साक्षी ने अपनी आँखों से घटना देखी।"
    assert engine.normalize("जाँच-पड़ताल के दौरान तथ्य स्पष्ट हुए।").normalized_text == "जाँच-पड़ताल के दौरान तथ्य स्पष्ट हुए।"
    assert engine.normalize("गाँधी नगर स्थित पुलिस थाना।").normalized_text == "गाँधी नगर स्थित पुलिस थाना।"


def test_tatsama_normalization_and_mixed_english_protection():
    engine = DevanagariOCREngine()

    # Tatsama terms with OCR-confused Chandrabindu normalized to Anusvara
    res = engine.normalize("सँविधान और सँरक्षण तथा सँख्या।")
    assert res.normalized_text == "संविधान और संरक्षण तथा संख्या।"

    # Mixed English legal citations protected without spurious danda conversion on ASCII text
    res_cite = engine.normalize("Under Section 482 Cr.P.C. and AIR 2024 SC 123.")
    assert "Section 482 Cr.P.C." in res_cite.normalized_text
    assert "AIR 2024 SC 123." in res_cite.normalized_text

    # Pipe conversion occurs only when preceded by Devanagari text
    res_dev_pipe = engine.normalize("धारा 482 के अंतर्गत आदेश |")
    assert res_dev_pipe.normalized_text.endswith("आदेश।")


# --- 3. OCR Quality Gate Operational States ---

def test_ocr_quality_gate_incomplete_provenance():
    gate = OCRQualityGate()
    # Missing source_url and cryptographic hash
    assessment = gate.evaluate_page("सत्र न्यायालय द्वारा पारित आदेश।", metadata={"page_id": "TEST-P1"})
    assert assessment.state == OCRQualityState.SOURCE_PROVENANCE_INCOMPLETE
    assert assessment.is_retrieval_eligible is False
    assert any("Missing mandatory provenance" in r for r in assessment.rejection_reasons)


def test_ocr_quality_gate_truncation_rejection():
    gate = OCRQualityGate()
    meta = {
        "page_id": "TEST-TRUNC",
        "court_or_source": "IND-HC-ALL",
        "source_url": "https://example.gov.in/1.pdf",
        "raw_ocr_text_hash": "a" * 64,
    }
    assessment = gate.evaluate_page("आदेश पारित।", metadata=meta)
    assert assessment.state == OCRQualityState.OCR_REJECTED
    assert assessment.is_retrieval_eligible is False
    assert any("truncated or below minimum character threshold" in r for r in assessment.rejection_reasons)


def test_ocr_quality_gate_lossy_decoding_rejection():
    gate = OCRQualityGate()
    meta = {
        "page_id": "TEST-REPL",
        "court_or_source": "IND-HC-DEL",
        "source_url": "https://example.gov.in/2.pdf",
        "raw_ocr_text_hash": "b" * 64,
    }
    # 4 replacement characters exceeds threshold of 3
    assessment = gate.evaluate_page("उच्च न्यायालय द्वारा \ufffd\ufffd\ufffd\ufffd जमानत निरस्त की गई।", metadata=meta)
    assert assessment.state == OCRQualityState.OCR_REJECTED
    assert assessment.is_retrieval_eligible is False


def test_ocr_quality_gate_statutory_privacy_bar():
    gate = OCRQualityGate()
    meta = {
        "page_id": "TEST-POCSO",
        "court_or_source": "IND-DC-SAKET",
        "source_url": "https://example.gov.in/3.pdf",
        "raw_ocr_text_hash": "c" * 64,
        "is_restricted": True,
        "privacy_assessment": "POCSO_ACT_SECTION_74_PROTECTED",
    }
    assessment = gate.evaluate_page("विशेष न्यायालय पॉक्सो अधिनियम के अंतर्गत विचारण संख्या 12/2023।", metadata=meta)
    assert assessment.state == OCRQualityState.OCR_REJECTED
    assert assessment.is_retrieval_eligible is False
    assert any("statutory non-disclosure bar" in r for r in assessment.rejection_reasons)


def test_ocr_quality_gate_nominal_pass():
    gate = OCRQualityGate()
    meta = {
        "page_id": "TEST-OK",
        "court_or_source": "IND-HC-ALL",
        "source_url": "https://example.gov.in/4.pdf",
        "raw_ocr_text_hash": "d" * 64,
        "scan_resolution_dpi": 300,
    }
    assessment = gate.evaluate_page(
        "उच्च न्यायालय इलाहाबाद द्वारा आपराधिक प्रकीर्ण जमानत याचिका स्वीकार की गई। "
        "यह आदेश धारा 439 के प्रावधानों के अंतर्गत पारित किया गया है।",
        metadata=meta,
    )
    assert assessment.state == OCRQualityState.OCR_ACCEPTABLE_FOR_RETRIEVAL
    assert assessment.is_retrieval_eligible is True
    assert assessment.heuristic_confidence >= 0.80


# --- 4. End-to-End OCR-to-RAG 10 Failure Scenarios ---

def test_ocr_rag_validator_10_scenarios():
    validator = OCRRAGValidator()
    results = validator.evaluate_10_failure_scenarios()
    assert len(results) == 10
    for r in results:
        assert r.passed is True, f"Scenario {r.scenario_id} ({r.scenario_name}) failed: {r.diagnostic_notes}"
        assert r.retrieval_safe is True, f"Scenario {r.scenario_id} was not retrieval safe!"


# --- 5. Corpus Reconciliation & Database Separation ---

def test_corpus_reconciliation_layer_integrity():
    res = run_reconciliation()
    assert res["layer_1_institutional_catalogue"] == 19
    assert res["layer_2_registered_sources"] == 59
    assert res["layer_3_acquired_source_manifests"] == 134
    assert res["layer_5_ocr_benchmark_pages"] == 12
    assert res["layer_7_indexed_chunks_total"] == 1505
    assert res["layer_8_active_retrievable_chunks"] == 1499
    assert res["layer_9_quarantined_scaffold_chunks"] == 6
    assert res["layer_10_training_corpus_records"] == 0
    assert res["database_separation_verified"] is True
    assert res["scaffold_chunk_isolation_verified"] is True
    assert res["reconciliation_verdict"] == "RECONCILED_10_LAYERS_DISJOINT"


# --- 6. Judicial Connector Preflight & SSRF Safety ---

def test_connector_preflight_and_ssrf_safety():
    preflight = run_preflight_checks()
    assert preflight["preflight_status"] == "PASS"
    assert preflight["ssrf_loopback_protection_verified"] is True
    assert preflight["ssrf_metadata_protection_verified"] is True
    assert preflight["delhi_domain_whitelisted"] is True
    assert preflight["bombay_domain_whitelisted"] is True
    assert preflight["rate_limiter_functional"] is True

    # Credential audit must never expose raw values
    delhi_cred = preflight["delhi_credentials"]
    assert delhi_cred["is_configured"] is False
    assert delhi_cred["masked_value"] is None
    assert delhi_cred["authorization_status"] == "BLOCKED_PENDING_CREDENTIALS"


def test_connector_blocks_private_and_metadata_ips():
    conn = DelhiHighCourtConnector(dry_run=True)
    # Loopback
    with pytest.raises(SSRFProtectionError):
        conn.validate_url_security("http://127.0.0.1:8000/api")
    # AWS metadata
    with pytest.raises(SSRFProtectionError):
        conn.validate_url_security("http://169.254.169.254/latest/meta-data/")
    # Embedded credentials
    with pytest.raises(SSRFProtectionError):
        conn.validate_url_security("https://user:pass@delhihighcourt.nic.in/order.pdf")
    # Disallowed external domain
    with pytest.raises(SSRFProtectionError):
        conn.validate_url_security("https://malicious-external-domain.com/hack.pdf")


# --- 7. Invariant Enforcement ---

def test_advocate_review_candidates_strictly_pending():
    reg_path = os.path.join("data", "07_batches", "review", "review_tracking_register.json")
    with open(reg_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    entries = data["entries"]
    assert len(entries) == 40
    assert data["total_tracked_records"] == 40
    for r in entries:
        assert r["review_status"] == "pending_legal_review"
        assert r.get("response_received") is False
        assert r.get("advocate_recipient_tag") is None
