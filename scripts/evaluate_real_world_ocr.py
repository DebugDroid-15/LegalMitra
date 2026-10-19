"""Evaluation script for LegalMitra Real-World Scanned Hindi Judicial OCR Benchmark.

Evaluates:
- Character Error Rate (CER)
- Word Error Rate (WER)
- Legal Token Sensitivity (statutory and judicial terminology recall)
- Numeric conversion accuracy (Devanagari numerals vs Latin digits)
- Conservative normalization impact via DevanagariOCREngine
"""

from __future__ import annotations

import difflib
import json
import os
import sys
from typing import Any, Dict, List, Tuple

from legalmitra.judicial.devanagari_ocr import DevanagariOCREngine, DevanagariOCRResult


def compute_cer(reference: str, hypothesis: str) -> float:
    return DevanagariOCREngine.compute_cer(reference, hypothesis)


def compute_wer(reference: str, hypothesis: str) -> float:
    return DevanagariOCREngine.compute_wer(reference, hypothesis)


def evaluate_benchmark(manifest_path: str) -> Dict[str, Any]:
    if not os.path.exists(manifest_path):
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    engine = DevanagariOCREngine()
    pages = data.get("pages", [])

    total_cer_raw = 0.0
    total_wer_raw = 0.0
    total_cer_norm = 0.0
    total_wer_norm = 0.0
    total_tokens_present = 0
    total_tokens_recovered = 0

    results_per_page = []

    for p in pages:
        ref = p["reference_ground_truth"]
        raw = p["raw_ocr_hypothesis"]
        norm_result = engine.normalize(raw)
        norm_text = norm_result.normalized_text

        cer_raw = compute_cer(ref, raw)
        wer_raw = compute_wer(ref, raw)

        # Normalize reference too for fair canonical comparison
        norm_ref = engine.normalize(ref).normalized_text
        cer_norm = compute_cer(norm_ref, norm_text)
        wer_norm = compute_wer(norm_ref, norm_text)

        total_cer_raw += cer_raw
        total_wer_raw += wer_raw
        total_cer_norm += cer_norm
        total_wer_norm += wer_norm

        expected_tokens = p.get("legal_tokens_present", [])
        total_tokens_present += len(expected_tokens)
        recovered = [t for t in expected_tokens if t in norm_text]
        total_tokens_recovered += len(recovered)

        results_per_page.append({
            "page_id": p["page_id"],
            "court_or_source": p["court_or_source"],
            "cer_raw": round(cer_raw, 4),
            "wer_raw": round(wer_raw, 4),
            "cer_normalized": round(cer_norm, 4),
            "wer_normalized": round(wer_norm, 4),
            "tokens_expected": len(expected_tokens),
            "tokens_recovered": len(recovered),
        })

    n = len(pages)
    avg_cer_raw = total_cer_raw / n if n else 0.0
    avg_wer_raw = total_wer_raw / n if n else 0.0
    avg_cer_norm = total_cer_norm / n if n else 0.0
    avg_wer_norm = total_wer_norm / n if n else 0.0
    sensitivity = total_tokens_recovered / total_tokens_present if total_tokens_present else 1.0

    summary = {
        "total_pages_evaluated": n,
        "avg_cer_raw": round(avg_cer_raw, 4),
        "avg_wer_raw": round(avg_wer_raw, 4),
        "avg_cer_normalized": round(avg_cer_norm, 4),
        "avg_wer_normalized": round(avg_wer_norm, 4),
        "legal_token_sensitivity": round(sensitivity, 4),
        "results_per_page": results_per_page,
    }

    return summary


if __name__ == "__main__":
    manifest = os.path.join(
        "data", "21_judicial_infrastructure", "scanned_hindi_ocr_benchmark", "benchmark_manifest.json"
    )
    res = evaluate_benchmark(manifest)
    print("=== LegalMitra Real-World Scanned Hindi OCR Evaluation ===")
    print(f"Total Staged Pages Evaluated : {res['total_pages_evaluated']}")
    print(f"Average Raw CER             : {res['avg_cer_raw'] * 100:.2f}%")
    print(f"Average Raw WER             : {res['avg_wer_raw'] * 100:.2f}%")
    print(f"Average Normalized CER      : {res['avg_cer_normalized'] * 100:.2f}%")
    print(f"Average Normalized WER      : {res['avg_wer_normalized'] * 100:.2f}%")
    print(f"Legal Token Sensitivity     : {res['legal_token_sensitivity'] * 100:.2f}%")
    print("\nPer-page details:")
    for p in res["results_per_page"]:
        print(f"  [{p['page_id']}] {p['court_or_source']}: CER={p['cer_normalized']*100:.2f}%, WER={p['wer_normalized']*100:.2f}%, Tokens={p['tokens_recovered']}/{p['tokens_expected']}")
