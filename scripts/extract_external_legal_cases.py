"""
Phase 66 — External Case Law Ingestion & Metadata Normalizer.
Extracts clean, verified case law samples from KanoonGPT/indian-case-laws
in read-only mode, normalizing fields into isolated dataset records without
touching data/legalmitra_kb.db or the primary source registry.
"""

import json
import logging
import os
from pathlib import Path
import re
from typing import Any, Dict, List, Optional
import urllib.request

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] - %(message)s")
logger = logging.getLogger("extract_external_legal_cases")

KANOONGPT_SAMPLE_URL = (
    "https://huggingface.co/datasets/KanoonGPT/indian-case-laws/resolve/main/sample/v1/indian_case_laws_sample_v1.parquet"
)
OUTPUT_DIR = Path("data/23_external_training")


def clean_legal_text(text: Optional[str]) -> str:
    """Sanitize court judgment text, removing excess whitespace and artifacts."""
    if not text or not isinstance(text, str):
        return ""
    # Normalize unicode and collapse spaces
    cleaned = re.sub(r"\s+", " ", text).strip()
    return cleaned


def extract_ratio_or_summary(text: str, max_words: int = 150) -> str:
    """Extract a concise ratio/holding fragment from judgment text."""
    if not text:
        return ""
    words = text.split()
    return " ".join(words[:max_words])


def run_extraction(sample_limit: int = 500) -> Path:
    """Download and process high-signal case laws from KanoonGPT sample."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / "kanoongpt_normalized_cases.jsonl"

    logger.info(f"Fetching sample Parquet from {KANOONGPT_SAMPLE_URL}...")
    df = pd.read_parquet(KANOONGPT_SAMPLE_URL)
    logger.info(f"Loaded raw dataset shape: {df.shape}")

    # Prioritize cases with clear case title, court, decision date, and indexable text
    valid_df = df[
        df["case_title"].notna()
        & df["court_name"].notna()
        & df["indexable_text"].notna()
        & (df["indexable_text"].str.len() > 100)
    ].copy()

    logger.info(f"Filtered to {len(valid_df)} well-formed cases")

    records: List[Dict[str, Any]] = []
    count = 0

    for _, row in valid_df.iterrows():
        if count >= sample_limit:
            break

        title = clean_legal_text(row.get("case_title"))
        court = clean_legal_text(row.get("court_name"))
        date = str(row.get("decision_date")) if pd.notna(row.get("decision_date")) else ""
        docket = clean_legal_text(row.get("docket_number"))
        cnr = clean_legal_text(row.get("cnr_number"))
        neutral_citation = clean_legal_text(row.get("neutral_citation"))
        text = clean_legal_text(row.get("indexable_text"))
        disposition = clean_legal_text(row.get("disposition_text"))

        if not text:
            continue

        ratio = extract_ratio_or_summary(text, max_words=120)

        record = {
            "external_case_id": f"EXT-KAN-{row.get('id', count)}",
            "title": title,
            "court": court,
            "decision_date": date,
            "docket_number": docket,
            "cnr_number": cnr,
            "neutral_citation": neutral_citation,
            "disposition": disposition,
            "ratio_summary": ratio,
            "full_text_length": len(text),
            "text_excerpt": text[:1200],
            "dataset_origin": "KanoonGPT/indian-case-laws",
            "license": "Apache-2.0",
        }
        records.append(record)
        count += 1

    with open(out_file, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    logger.info(f"Successfully extracted {len(records)} normalized cases to {out_file}")
    return out_file


if __name__ == "__main__":
    run_extraction(sample_limit=500)
