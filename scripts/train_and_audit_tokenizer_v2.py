"""
Train and Audit IndianLegalTokenizerV2 for LegalMitra Phase 33.
Compares Tokenizer V1 vs Tokenizer V2 on English, Hindi, and Mixed Indian legal text.
Outputs data/20_evaluation/tokenizer_v2_audit_results.json.
"""

import sys
from pathlib import Path

_repo_root = str(Path(__file__).resolve().parent.parent)
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

import hashlib
import json
import sqlite3
from typing import Dict, List, Any

from research.original_model.tokenizer import IndianLegalTokenizer
from research.original_model.tokenizer_v2 import IndianLegalTokenizerV2


def train_and_audit_tokenizer_v2(
    db_path: str = "data/legalmitra_kb.db",
    hindi_corpus_path: str = "data/09_national_corpus/hindi_statutory_corpus.json",
    v1_path: str = "research/original_model/tokenizer.json",
    v2_save_path: str = "research/original_model/tokenizer_v2.json",
    audit_output_path: str = "data/20_evaluation/tokenizer_v2_audit_results.json",
) -> Dict[str, Any]:
    print("=== Training and Auditing IndianLegalTokenizerV2 ===")

    # 1. Load English texts from KB
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT content FROM legal_chunks WHERE is_synthetic_scaffold = 0")
    en_texts = [r[0] for r in c.fetchall()]
    conn.close()

    # 2. Load Hindi texts from national corpus
    with open(hindi_corpus_path, "r", encoding="utf-8") as f:
        hi_data = json.load(f)
    hi_texts = [p["content"] for p in hi_data["passages"]]

    print(f"Loaded {len(en_texts)} English chunks and {len(hi_texts)} Hindi passages.")

    # 3. Create joint training dataset for Tokenizer V2
    # Sample every 12th English chunk to balance with Hindi texts
    joint_texts = en_texts[::12] + hi_texts * 4

    # 4. Train Tokenizer V2
    tok_v2 = IndianLegalTokenizerV2()
    tok_v2.train_from_texts(joint_texts, target_vocab_size=2048)
    tok_v2.save(v2_save_path)
    print(f"Tokenizer V2 trained and saved to {v2_save_path} (Vocab size: {tok_v2.vocab_size})")

    # 5. Load Tokenizer V1 for side-by-side comparison
    tok_v1 = IndianLegalTokenizer.load(v1_path)

    # 6. Evaluation test cases
    test_cases = [
        {
            "category": "english_statutory_citation",
            "text": "Under Section 482(4) of the Bharatiya Nagarik Suraksha Sanhita, 2023, High Courts possess inherent jurisdiction.",
        },
        {
            "category": "english_evidence_clause",
            "text": "Section 63(4)(c) of Bharatiya Sakshya Adhiniyam, 2023 mandates certificate for electronic record admissibility.",
        },
        {
            "category": "english_constitutional_liberty",
            "text": "Article 21 of the Constitution of India guarantees protection of life and personal liberty.",
        },
        {
            "category": "hindi_constitutional_preamble",
            "text": "हम, भारत के लोग, भारत को एक संपूर्ण प्रभुत्व-संपन्न समाजवादी पंथनिरपेक्ष लोकतंत्रात्मक गणराज्य बनाने के लिए संकल्पित हैं।",
        },
        {
            "category": "hindi_statutory_inherent_powers",
            "text": "धारा 528. उच्च न्यायालय की अंतर्निहित शक्तियों की व्यावृत्ति न्याय के उद्देश्यों की प्राप्ति के लिए आवश्यक है।",
        },
        {
            "category": "hindi_defamation_offence",
            "text": "धारा 356 के अनुसार किसी व्यक्ति की ख्याति की अपहानि करने वाला लांछन मानहानि का अपराध है।",
        },
        {
            "category": "mixed_bilingual_query",
            "text": "Whether Section 482 of CrPC / धारा 528 BNSS allows quashing of FIR where civil dispute is criminalized?",
        },
    ]

    results = []
    v1_total_tokens = 0
    v2_total_tokens = 0
    total_chars = 0
    total_words = 0

    for tc in test_cases:
        txt = tc["text"]
        cat = tc["category"]
        n_chars = len(txt)
        n_words = len(txt.split())
        total_chars += n_chars
        total_words += n_words

        # Tokenize V1
        enc_v1 = tok_v1.encode(txt, add_special_tokens=False)
        dec_v1 = tok_v1.decode(enc_v1, skip_special_tokens=True)
        unk_v1 = sum(1 for tid in enc_v1 if tid == tok_v1.unk_token_id)
        v1_total_tokens += len(enc_v1)

        # Tokenize V2
        enc_v2 = tok_v2.encode(txt, add_special_tokens=False)
        dec_v2 = tok_v2.decode(enc_v2, skip_special_tokens=True)
        unk_v2 = sum(1 for tid in enc_v2 if tid == tok_v2.unk_token_id)
        v2_total_tokens += len(enc_v2)

        results.append({
            "category": cat,
            "text_sample": txt,
            "char_count": n_chars,
            "word_count": n_words,
            "v1_metrics": {
                "token_count": len(enc_v1),
                "tokens_per_word": round(len(enc_v1) / n_words, 2),
                "unk_count": unk_v1,
                "decoded_preview": dec_v1[:60],
            },
            "v2_metrics": {
                "token_count": len(enc_v2),
                "tokens_per_word": round(len(enc_v2) / n_words, 2),
                "unk_count": unk_v2,
                "decoded_preview": dec_v2[:60],
                "compression_improvement_pct": round(((len(enc_v1) - len(enc_v2)) / len(enc_v1)) * 100, 2),
            },
        })

    # Vocabulary utilization on held-out test chunks
    held_out_en = en_texts[100:110]
    held_out_hi = hi_texts[-5:]

    def measure_utilization(tok, texts):
        used_ids = set()
        total_toks = 0
        for t in texts:
            e = tok.encode(t, add_special_tokens=False)
            used_ids.update(e)
            total_toks += len(e)
        return {
            "unique_tokens_activated": len(used_ids),
            "vocabulary_activation_pct": round((len(used_ids) / tok.vocab_size) * 100, 2),
            "total_tokens_generated": total_toks,
        }

    v1_util_en = measure_utilization(tok_v1, held_out_en)
    v1_util_hi = measure_utilization(tok_v1, held_out_hi)
    v2_util_en = measure_utilization(tok_v2, held_out_en)
    v2_util_hi = measure_utilization(tok_v2, held_out_hi)

    audit_summary = {
        "audit_version": "v2.0.0",
        "phase": 33,
        "v1_spec": {
            "path": v1_path,
            "vocab_size": tok_v1.vocab_size,
            "merges_count": len(tok_v1.merges),
        },
        "v2_spec": {
            "path": v2_save_path,
            "vocab_size": tok_v2.vocab_size,
            "merges_count": len(tok_v2.merges),
        },
        "aggregate_comparison": {
            "total_sample_characters": total_chars,
            "total_sample_words": total_words,
            "v1_total_tokens": v1_total_tokens,
            "v2_total_tokens": v2_total_tokens,
            "v1_tokens_per_word": round(v1_total_tokens / total_words, 2),
            "v2_tokens_per_word": round(v2_total_tokens / total_words, 2),
            "overall_token_reduction_pct": round(((v1_total_tokens - v2_total_tokens) / v1_total_tokens) * 100, 2),
        },
        "vocabulary_utilization_held_out": {
            "v1_english": v1_util_en,
            "v1_hindi": v1_util_hi,
            "v2_english": v2_util_en,
            "v2_hindi": v2_util_hi,
        },
        "test_cases": results,
    }

    out_file = Path(audit_output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(audit_summary, f, indent=2, ensure_ascii=False)

    print(f"Audit results written to {audit_output_path}")
    print(f"V1 Tokens: {v1_total_tokens} | V2 Tokens: {v2_total_tokens}")
    print(f"Overall token reduction: {audit_summary['aggregate_comparison']['overall_token_reduction_pct']}%")
    return audit_summary


if __name__ == "__main__":
    train_and_audit_tokenizer_v2()

