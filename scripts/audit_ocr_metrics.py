"""Independently audit Devanagari OCR metrics and manifest fidelity."""

import json
import sys
from legalmitra.judicial.devanagari_ocr import DevanagariOCREngine

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

def audit_ocr():
    print("=== Workstream C Devanagari OCR Metric Reproduction ===")
    path = "data/21_judicial_infrastructure/devanagari_ocr_eval_manifest.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    meta = data.get("metadata", {})
    samples = data.get("samples", [])
    print(f"Reported metadata: {meta}")
    print(f"Total samples: {len(samples)}")

    engine = DevanagariOCREngine()

    reproduced_samples = []
    total_ref_chars = 0
    total_char_errors = 0
    total_ref_words = 0
    total_word_errors = 0

    all_tokens_found = set()

    for s in samples:
        sid = s["sample_id"]
        ref = s["reference_text"]
        raw = s["raw_ocr_text"]
        rep_cer = s["metrics"]["cer"]
        rep_wer = s["metrics"]["wer"]

        # Run fresh normalization
        res = engine.normalize(raw)
        calc_cer = engine.compute_cer(ref, res.normalized_text)
        calc_wer = engine.compute_wer(ref, res.normalized_text)

        # Character errors
        ref_chars = len(ref)
        total_ref_chars += ref_chars
        total_char_errors += round(calc_cer * ref_chars)

        ref_words = len(ref.split())
        total_ref_words += ref_words
        total_word_errors += round(calc_wer * ref_words)

        all_tokens_found.update(res.legal_tokens_detected)

        print(f"\nSample {sid}:")
        print(f"  Reference length: chars={len(ref)}, words={len(ref.split())}")
        print(f"  Reported CER={rep_cer}, Calculated CER={calc_cer:.4f}")
        print(f"  Reported WER={rep_wer}, Calculated WER={calc_wer:.4f}")
        print(f"  Requires human review: {res.requires_human_review} (has \ufffd: {res.has_replacement_characters})")
        print(f"  Legal tokens detected: {res.legal_tokens_detected}")

    macro_avg_cer = sum(s["metrics"]["cer"] for s in samples) / len(samples)
    macro_avg_wer = sum(s["metrics"]["wer"] for s in samples) / len(samples)

    micro_cer = total_char_errors / total_ref_chars if total_ref_chars > 0 else 0.0
    micro_wer = total_word_errors / total_ref_words if total_ref_words > 0 else 0.0

    print("\n--- Summary Reproduction ---")
    print(f"Macro-averaged CER: {macro_avg_cer:.4f} (Reported: {meta.get('average_cer')})")
    print(f"Macro-averaged WER: {macro_avg_wer:.4f} (Reported: {meta.get('average_wer')})")
    print(f"Micro-averaged CER: {micro_cer:.4f}")
    print(f"Micro-averaged WER: {micro_wer:.4f}")
    print(f"Unique legal tokens detected across sample set: {len(all_tokens_found)}")

if __name__ == "__main__":
    audit_ocr()
