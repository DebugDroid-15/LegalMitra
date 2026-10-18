"""
Tokenizer Quality and Unicode Audit for Phase 32.
Audits IndianLegalTokenizer across:
1. Special tokens and vocabulary distribution
2. Specific legal citations: Section 482(4), Section 63(4)(c), Article 21, BNSS 2023, BSA 2023, धारा 482
3. Mixed English-Hindi legal questions
4. Empty inputs, malformed text, unknown token handling
5. Compression ratio (tokens per word, tokens per character)
6. Vocabulary utilization on training vs held-out evaluation corpus
Outputs metrics to data/20_evaluation/tokenizer_audit_results.json
"""

import json
from pathlib import Path
import sqlite3
import sys

# Ensure UTF-8 output on Windows console
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

# Ensure repo root is on sys.path
sys.path.insert(0, ".")
from research.original_model.tokenizer import IndianLegalTokenizer


def run_tokenizer_audit() -> dict:
    tok_path = Path("research/original_model/tokenizer.json")
    assert tok_path.exists(), "Tokenizer file missing at research/original_model/tokenizer.json"
    tok = IndianLegalTokenizer.load(tok_path)

    print(f"=== IndianLegalTokenizer Quality Audit (Vocab Size: {tok.vocab_size}) ===")

    # 1. Required Legal and Multilingual Samples
    test_samples = [
        "Section 482(4)",
        "Section 63(4)(c)",
        "Article 21",
        "BNSS 2023",
        "BSA 2023",
        "धारा 482",
        "Whether criminal proceedings under धारा 482 can be quashed for commercial disputes?",
        "Under Section 528 of the BNSS, 2023, the High Court preserves inherent powers to prevent abuse of the process of any Court.",
        "",
        "   ",
        "!@#$%^&*()",
        "xyz123nonexistentword",
    ]

    sample_results = []
    for text in test_samples:
        encoded = tok.encode(text, add_special_tokens=True)
        decoded = tok.decode(encoded, skip_special_tokens=True)
        token_strings = [tok.id_to_token.get(i, "<unk>") for i in encoded]
        
        # Roundtrip match on clean text
        clean_orig = "".join(text.split())
        clean_dec = "".join(decoded.split())
        round_trip_match = (clean_orig == clean_dec)

        sample_results.append({
            "input": text,
            "encoded_ids": encoded,
            "token_count": len(encoded),
            "token_strings": token_strings,
            "decoded": decoded,
            "round_trip_match": round_trip_match,
        })
        print(f"Input: '{text}' -> Tokens ({len(encoded)}): {token_strings} | Match: {round_trip_match}")

    # 2. Vocabulary Utilization & Compression on In-Domain vs Held-Out Text
    conn = sqlite3.connect("data/legalmitra_kb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT source_id, content FROM legal_chunks WHERE is_synthetic_scaffold = 0")
    rows = cursor.fetchall()
    conn.close()

    # Partition into in-domain (BNSS) vs held-out (DPDP)
    train_texts = [r[1] for r in rows if r[0] == "IND-STAT-BNSS-2023"][:100]
    held_out_texts = [r[1] for r in rows if r[0] == "IND-STAT-DPDP-2023"][:100]

    def measure_stats(texts, name):
        total_chars = sum(len(t) for t in texts)
        total_words = sum(len(t.split()) for t in texts)
        used_token_ids = set()
        total_tokens = 0
        unk_count = 0

        for t in texts:
            enc = tok.encode(t, add_special_tokens=False)
            total_tokens += len(enc)
            for tid in enc:
                used_token_ids.add(tid)
                if tid == tok.unk_token_id:
                    unk_count += 1

        tokens_per_word = round(total_tokens / total_words, 3) if total_words else 0
        tokens_per_char = round(total_tokens / total_chars, 4) if total_chars else 0
        vocab_utilization = round(len(used_token_ids) / tok.vocab_size * 100, 2)
        unk_rate = round(unk_count / total_tokens * 100, 4) if total_tokens else 0

        print(f"\nCorpus: {name} ({len(texts)} samples, {total_words:,} words)")
        print(f"  Total tokens: {total_tokens:,}")
        print(f"  Tokens per word: {tokens_per_word}")
        print(f"  Tokens per char: {tokens_per_char}")
        print(f"  Vocab utilization: {vocab_utilization}% ({len(used_token_ids)}/{tok.vocab_size})")
        print(f"  Unknown token rate: {unk_rate}% ({unk_count} tokens)")

        return {
            "name": name,
            "sample_count": len(texts),
            "total_words": total_words,
            "total_tokens": total_tokens,
            "tokens_per_word": tokens_per_word,
            "tokens_per_char": tokens_per_char,
            "vocab_utilization_pct": vocab_utilization,
            "unk_rate_pct": unk_rate,
        }

    train_stats = measure_stats(train_texts, "In-Domain (BNSS)")
    held_out_stats = measure_stats(held_out_texts, "Held-Out (DPDP Act)")

    results = {
        "vocab_size": tok.vocab_size,
        "special_tokens": {tok_name: tok.vocab[tok_name] for tok_name in ["<pad>", "<s>", "</s>", "<unk>", "<sec>", "<court>", "<prov>", "<act>"]},
        "sample_evaluations": sample_results,
        "in_domain_corpus_stats": train_stats,
        "held_out_corpus_stats": held_out_stats,
    }

    out_path = Path("data/20_evaluation/tokenizer_audit_results.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nTokenizer audit written to {out_path}")
    return results


if __name__ == "__main__":
    run_tokenizer_audit()
