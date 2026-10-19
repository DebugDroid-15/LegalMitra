"""Unit and integration tests for Phase 43 Hindi Legal OCR & Ground Truth Verification.

Covers:
1. Micro-averaged and macro-averaged CER and WER metric accuracy.
2. Context-aware Chandrabindu-to-Anusvara normalization with tadbhav whitelist protection.
3. Provenance metadata completeness across all benchmark pages.
4. Rigorous legal-token, section, and citation structural preservation.
5. Invariant enforcement: exclusion of OCR benchmark pages from retrieval/training,
   scaffold quarantine, and physical database separation.
"""

import json
import os
import sqlite3
import pytest

from legalmitra.judicial.devanagari_ocr import (
    DevanagariOCREngine,
    DevanagariOCRResult,
)
from scripts.evaluate_real_world_ocr import evaluate_benchmark


# --- 1. Metric Accuracy & Micro vs Macro Calculations ---

def test_evaluate_benchmark_micro_and_macro_metrics():
    manifest_path = os.path.join(
        "data", "21_judicial_infrastructure", "scanned_hindi_ocr_benchmark", "benchmark_manifest.json"
    )
    res = evaluate_benchmark(manifest_path)
    assert res["total_pages_evaluated"] == 12

    # Check macro metrics
    assert res["macro_cer_raw"] == 0.0168
    assert res["macro_wer_raw"] == 0.0397
    assert res["macro_cer_normalized"] == 0.0142
    assert res["macro_wer_normalized"] == 0.0264

    # Check micro metrics (weighted by character and word lengths)
    assert res["micro_cer_raw"] == 0.0172
    assert res["micro_wer_raw"] == 0.0406
    assert res["micro_cer_normalized"] == 0.0146
    assert res["micro_wer_normalized"] == 0.0276

    # Check legal token recall
    assert res["legal_tokens_expected"] == 47
    assert res["legal_tokens_recovered"] == 47
    assert res["legal_token_sensitivity"] == 1.0


# --- 2. Normalization & Whitelist Protection Audit ---

def test_chandrabindu_normalization_with_whitelist_protection():
    engine = DevanagariOCREngine()

    # Legitimate tadbhav words with Chandrabindu must be preserved intact
    assert engine.normalize("गाँव").normalized_text == "गाँव"
    assert engine.normalize("माँ").normalized_text == "माँ"
    assert engine.normalize("पाँच").normalized_text == "पाँच"
    assert engine.normalize("यहाँ").normalized_text == "यहाँ"

    # OCR errors where Chandrabindu precedes a non-vowel consonant in tatsama legal terms must be normalized
    assert engine.normalize("सँविधान").normalized_text == "संविधान"
    assert engine.normalize("सँरक्षण").normalized_text == "संरक्षण"
    assert engine.normalize("सँख्या").normalized_text == "संख्या"
    assert engine.normalize("सँभावना").normalized_text == "संभावना"


def test_danda_preservation_and_period_protection():
    engine = DevanagariOCREngine()

    # Solitary pipe between Devanagari text becomes danda
    res = engine.normalize("न्यायालय उच्च न्यायालय इलाहाबाद |")
    assert res.normalized_text.endswith("इलाहाबाद।")

    # Latin period in citations and section references must not be altered
    res_cite = engine.normalize("Section 482 Cr.P.C. under AIR 2024 SC 123.")
    assert "Cr.P.C." in res_cite.normalized_text
    assert "AIR 2024 SC 123." in res_cite.normalized_text


# --- 3. Provenance Metadata Completeness ---

def test_benchmark_provenance_schema_completeness():
    manifest_path = os.path.join(
        "data", "21_judicial_infrastructure", "scanned_hindi_ocr_benchmark", "benchmark_manifest.json"
    )
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    required_keys = {
        "page_id",
        "court_or_source",
        "court_name",
        "document_type",
        "case_number",
        "year",
        "physical_page_number",
        "scan_quality",
        "rights_status",
        "reference_ground_truth",
        "raw_ocr_hypothesis",
        "legal_tokens_present",
        "source_url",
        "document_date",
        "acquisition_date",
        "reference_text_hash",
        "raw_ocr_text_hash",
        "normalized_ocr_text_hash",
        "scan_dimensions",
        "scan_resolution_dpi",
        "ocr_engine_version",
        "reference_verification_status",
        "privacy_assessment",
        "inclusion_rationale",
    }

    for p in data["pages"]:
        missing = required_keys - set(p.keys())
        assert not missing, f"Page {p.get('page_id')} missing keys: {missing}"
        assert len(p["reference_text_hash"]) == 64
        assert len(p["raw_ocr_text_hash"]) == 64
        assert len(p["normalized_ocr_text_hash"]) == 64
        assert p["reference_verification_status"] == "INDEPENDENTLY_HUMAN_VERIFIED"


# --- 4. Retrieval and Training Exclusion Invariants ---

def test_ocr_benchmark_excluded_from_kb_chunks():
    kb_path = os.path.join("data", "legalmitra_kb.db")
    con = sqlite3.connect(kb_path)
    cur = con.cursor()
    # Check that no benchmark page IDs exist in legal_chunks
    rows = cur.execute(
        "SELECT count(*) FROM legal_chunks WHERE chunk_id LIKE 'REAL-OCR-HI-%' OR source_id LIKE 'REAL-OCR-HI-%'"
    ).fetchone()[0]
    con.close()
    assert rows == 0, "OCR benchmark samples leaked into production knowledge base!"


def test_quarantined_scaffold_integrity():
    kb_path = os.path.join("data", "legalmitra_kb.db")
    con = sqlite3.connect(kb_path)
    cur = con.cursor()
    scaffold_rows = cur.execute(
        "SELECT count(*) FROM legal_chunks WHERE is_synthetic_scaffold = 1"
    ).fetchone()[0]
    con.close()
    assert scaffold_rows == 6, f"Expected 6 quarantined scaffold chunks, found {scaffold_rows}"
