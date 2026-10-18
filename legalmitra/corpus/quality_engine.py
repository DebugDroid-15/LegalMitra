"""
LegalMitra National Corpus Quality & Deduplication Engine (Phase 35).
Computes exact duplicate rates, near-duplicate similarity (Jaccard 3-grams),
document family distributions, jurisdictional coverage, language ratios,
token counts under IndianLegalTokenizerV2, and strictly validates against
intra-split data leakage (source-grouped partitioning).
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass
class QualityMetricsReport:
    timestamp: str
    tokenizer_version: str
    total_raw_passages: int
    total_eligible_passages: int
    excluded_passages_count: int
    exact_duplicates_count: int
    exact_duplicate_rate: float
    near_duplicates_count: int
    near_duplicate_rate: float
    total_tokens: int
    eligible_en_tokens: int
    eligible_hi_tokens: int
    excluded_tokens_count: int
    jurisdiction_breakdown: Dict[str, int]
    language_breakdown: Dict[str, int]
    document_family_breakdown: Dict[str, int]
    leakage_detected: bool
    leakage_details: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CorpusQualityEngine:
    """
    Evaluates corpus textual quality, exact/near duplicates, and split leakage.
    """

    def __init__(self, tokenizer_path: str = "research/original_model/tokenizer_v2.json"):
        self.tokenizer_path = Path(tokenizer_path)
        self.tokenizer = None
        self._load_tokenizer()

    def _load_tokenizer(self) -> None:
        if self.tokenizer_path.exists():
            try:
                from research.original_model.tokenizer_v2 import IndianLegalTokenizerV2
                self.tokenizer = IndianLegalTokenizerV2.load(str(self.tokenizer_path))
            except Exception:
                self.tokenizer = None

    @staticmethod
    def _get_ngrams(words: List[str], n: int = 3) -> Set[Tuple[str, ...]]:
        if len(words) < n:
            return {tuple(words)}
        return {tuple(words[i : i + n]) for i in range(len(words) - n + 1)}

    def jaccard_similarity(self, text_a: str, text_b: str, n: int = 3) -> float:
        words_a = re.findall(r"\w+", text_a.lower())
        words_b = re.findall(r"\w+", text_b.lower())
        if not words_a or not words_b:
            return 0.0
        set_a = self._get_ngrams(words_a, n)
        set_b = self._get_ngrams(words_b, n)
        intersection = len(set_a.intersection(set_b))
        union = len(set_a.union(set_b))
        return intersection / union if union > 0 else 0.0

    def audit_corpus(
        self,
        passages: List[Dict[str, Any]],
        train_sources: Optional[Set[str]] = None,
        val_sources: Optional[Set[str]] = None,
        test_sources: Optional[Set[str]] = None,
        near_dup_threshold: float = 0.85,
    ) -> QualityMetricsReport:
        """
        Audit passages for duplicates, token distribution, coverage, and cross-split leakage.
        """
        total_passages = len(passages)
        seen_exact_hashes: Dict[str, str] = {}  # sha -> passage_id
        exact_dups = 0
        near_dups = 0

        jurisdictions: Dict[str, int] = {}
        languages: Dict[str, int] = {}
        families: Dict[str, int] = {}

        total_tokens = 0
        en_tokens = 0
        hi_tokens = 0
        excluded_tokens = 0
        excluded_passages = 0

        # Sample for near-dup checks (first 300 to maintain fast determinism)
        sample_for_near = passages[:300]
        for i in range(len(sample_for_near)):
            text_i = sample_for_near[i].get("normalized_content") or sample_for_near[i].get("text", "")
            for j in range(i + 1, min(i + 15, len(sample_for_near))):
                text_j = sample_for_near[j].get("normalized_content") or sample_for_near[j].get("text", "")
                if self.jaccard_similarity(text_i, text_j) >= near_dup_threshold:
                    near_dups += 1
                    break

        for p in passages:
            # Check exclusions
            is_scaffold = p.get("is_synthetic_scaffold", False) or "IND-JUD-DEL-2024-BAIL" in p.get("source_id", "")
            if is_scaffold:
                excluded_passages += 1

            text = p.get("normalized_content") or p.get("text", "")
            lang = p.get("language", "en")
            jur = p.get("jurisdiction", "IN")
            fam = p.get("document_family", "statutory")

            jurisdictions[jur] = jurisdictions.get(jur, 0) + 1
            languages[lang] = languages.get(lang, 0) + 1
            families[fam] = families.get(fam, 0) + 1

            # Exact duplicate check
            h = hashlib.sha256(text.encode("utf-8")).hexdigest()
            if h in seen_exact_hashes:
                exact_dups += 1
            else:
                seen_exact_hashes[h] = p.get("id") or p.get("passage_id", "")

            # Token counting
            if self.tokenizer:
                tok_len = len(self.tokenizer.encode(text))
            else:
                tok_len = len(text.split())

            if is_scaffold:
                excluded_tokens += tok_len
            else:
                total_tokens += tok_len
                if lang == "hi":
                    hi_tokens += tok_len
                else:
                    en_tokens += tok_len

        # Leakage verification between train/val/test
        leakage_detected = False
        leakage_details = []
        if train_sources and val_sources:
            overlap = train_sources.intersection(val_sources)
            if overlap:
                leakage_detected = True
                leakage_details.append(f"Train/Val overlap on sources: {overlap}")
        if train_sources and test_sources:
            overlap = train_sources.intersection(test_sources)
            if overlap:
                leakage_detected = True
                leakage_details.append(f"Train/Test overlap on sources: {overlap}")
        if val_sources and test_sources:
            overlap = val_sources.intersection(test_sources)
            if overlap:
                leakage_detected = True
                leakage_details.append(f"Val/Test overlap on sources: {overlap}")

        eligible_passages = total_passages - excluded_passages
        exact_rate = round(exact_dups / total_passages, 4) if total_passages > 0 else 0.0
        near_rate = round(near_dups / len(sample_for_near), 4) if sample_for_near else 0.0

        return QualityMetricsReport(
            timestamp=datetime.utcnow().isoformat(),
            tokenizer_version="v2.0.0-bilingual (vocab 2,048)",
            total_raw_passages=total_passages,
            total_eligible_passages=eligible_passages,
            excluded_passages_count=excluded_passages,
            exact_duplicates_count=exact_dups,
            exact_duplicate_rate=exact_rate,
            near_duplicates_count=near_dups,
            near_duplicate_rate=near_rate,
            total_tokens=total_tokens,
            eligible_en_tokens=en_tokens,
            eligible_hi_tokens=hi_tokens,
            excluded_tokens_count=excluded_tokens,
            jurisdiction_breakdown=jurisdictions,
            language_breakdown=languages,
            document_family_breakdown=families,
            leakage_detected=leakage_detected,
            leakage_details=leakage_details,
        )

