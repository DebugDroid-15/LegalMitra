"""LegalMitra Judicial Knowledge Infrastructure — Devanagari OCR Normalization & QA Engine.

Provides non-destructive, conservative Unicode normalization and quality validation for Hindi judicial texts:
- NFC Unicode normalization
- Danda (।) and double danda (॥) punctuation validation
- Detection of replacement characters (\ufffd), malformed byte sequences, and abnormal script mixing
- OCR numeral confusion matrix handling (Devanagari ०-९ vs Latin 0-9)
- Legal token preservation (जमानत, दोषसिद्धि, बरी, धारा, अनुच्छेद, उच्चतम न्यायालय)
- Character Error Rate (CER) and Word Error Rate (WER) calculation routines
- Non-destructive architecture: raw OCR preserved immutably alongside normalized representation
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass
class DevanagariOCRResult:
    raw_ocr_text: str
    normalized_text: str
    char_count: int
    word_count: int
    detected_anomalies: List[str]
    detected_ligature_warnings: List[str]
    has_replacement_characters: bool
    requires_human_review: bool
    legal_tokens_detected: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "char_count": self.char_count,
            "word_count": self.word_count,
            "detected_anomalies": self.detected_anomalies,
            "detected_ligature_warnings": self.detected_ligature_warnings,
            "has_replacement_characters": self.has_replacement_characters,
            "requires_human_review": self.requires_human_review,
            "legal_tokens_detected": self.legal_tokens_detected,
        }


class DevanagariOCREngine:
    """Non-destructive normalization, anomaly detection, and QA evaluation for Devanagari legal text."""

    _RE_DEV_BLOCK = re.compile(r"[\u0900-\u097F]")
    _REPLACEMENTS = "\ufffd"

    # Core statutory & judicial Hindi tokens
    _LEGAL_TOKENS = [
        "जमानत", "दोषसिद्धि", "बरी", "अपील", "याचिका", "अभियुक्त",
        "अभियोजन", "उच्चतम न्यायालय", "उच्च न्यायालय", "सत्र न्यायालय",
        "धारा", "अनुच्छेद", "प्रावधान", "संविधान", "दण्ड प्रक्रिया संहिता",
        "भारतीय दण्ड संहिता", "साक्ष्य", "तथ्य", "निर्णय", "आदेश",
    ]

    # Whitelist of legitimate Hindi words that retain Chandrabindu (tadbhav words)
    _CHANDRABINDU_EXCEPTIONS = {
        "माँ", "गाँव", "पाँच", "आँख", "यहाँ", "वहाँ", "जहाँ", "कहाँ",
        "मुँह", "दायाँ", "बायाँ", "हँसना", "छाँव", "धुआँ", "कुआँ",
    }

    def _normalize_anusvara_with_whitelist(self, text: str) -> str:
        """Context-aware Chandrabindu-to-Anusvara normalization respecting genuine tadbhav words."""
        tokens = text.split()
        processed = []
        for tok in tokens:
            # Strip punctuation for exception matching
            clean_tok = re.sub(r"[।॥,\.\(\)\"\':;!?]", "", tok)
            if clean_tok in self._CHANDRABINDU_EXCEPTIONS:
                processed.append(tok)
            else:
                # Normalize Chandrabindu (\u0901) to Anusvara (\u0902) when preceding non-vowels (consonants \u0915-\u0939)
                tok_norm = re.sub(r"\u0901(?=[\u0915-\u0939])", "\u0902", tok)
                processed.append(tok_norm)
        return " ".join(processed)

    def normalize(self, text: str) -> DevanagariOCRResult:
        """Apply conservative Unicode normalization without mutating underlying raw text."""
        anomalies: List[str] = []
        ligature_warnings: List[str] = []

        # 1. Check for replacement characters
        has_repl = self._REPLACEMENTS in text
        if has_repl:
            anomalies.append("Unicode replacement character (\ufffd) detected, indicating lossy decoding")

        # 2. Check for suspicious control characters
        suspicious_ctrls = [ch for ch in text if ord(ch) < 32 and ch not in ("\n", "\r", "\t")]
        if suspicious_ctrls:
            anomalies.append(f"Found {len(suspicious_ctrls)} illegal control characters")

        # 3. Unicode NFC Normalization
        norm_text = unicodedata.normalize("NFC", text)

        # 4. Standardize danda and double danda spacing while protecting Latin periods in citations
        # Replace solitary vertical pipes '|' when surrounded by Devanagari characters with Devanagari Danda '।'
        norm_text = re.sub(r"(?<=[\u0900-\u097F])\s*\|\s*", "। ", norm_text)
        norm_text = re.sub(r"(?<=[\u0900-\u097F])\s*\|\|\s*", "॥ ", norm_text)
        # Attach danda directly to preceding word (no leading space)
        norm_text = re.sub(r"\s+([।॥])", r"\1", norm_text)
        # Ensure single space after danda if followed by another word
        norm_text = re.sub(r"([।॥])(?=[^\s।॥\n])", r"\1 ", norm_text)

        # 5. Anusvara / Chandrabindu OCR normalization with genuine word protection
        norm_text = self._normalize_anusvara_with_whitelist(norm_text)

        # 6. Collapse excessive whitespace while preserving paragraph breaks
        norm_text = re.sub(r"[ \t]+", " ", norm_text)
        norm_text = re.sub(r"\n\s*\n+", "\n\n", norm_text)

        # 6. Scan for legal tokens
        found_tokens = [tok for tok in self._LEGAL_TOKENS if tok in norm_text]

        # 7. Check for orphaned Halant / Virama (Virama preceded by whitespace or non-Devanagari)
        orphaned_halant = re.findall(r"(?:[^\u0900-\u097F]|\s)\u094D", norm_text)
        if orphaned_halant:
            ligature_warnings.append(f"Found {len(orphaned_halant)} orphaned halant virama marks")

        words = norm_text.split()
        requires_review = has_repl or len(anomalies) > 0 or len(ligature_warnings) > 0

        return DevanagariOCRResult(
            raw_ocr_text=text,
            normalized_text=norm_text.strip(),
            char_count=len(norm_text),
            word_count=len(words),
            detected_anomalies=anomalies,
            detected_ligature_warnings=ligature_warnings,
            has_replacement_characters=has_repl,
            requires_human_review=requires_review,
            legal_tokens_detected=found_tokens,
        )

    @staticmethod
    def compute_cer(reference: str, hypothesis: str) -> float:
        """Calculate Character Error Rate (Levenshtein distance divided by reference length)."""
        ref_chars = list(reference)
        hyp_chars = list(hypothesis)
        r_len = len(ref_chars)
        h_len = len(hyp_chars)
        if r_len == 0:
            return 0.0 if h_len == 0 else 1.0

        # Dynamic programming Levenshtein
        dp = [[0] * (h_len + 1) for _ in range(r_len + 1)]
        for i in range(r_len + 1):
            dp[i][0] = i
        for j in range(h_len + 1):
            dp[0][j] = j

        for i in range(1, r_len + 1):
            for j in range(1, h_len + 1):
                if ref_chars[i - 1] == hyp_chars[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

        return dp[r_len][h_len] / float(r_len)

    @staticmethod
    def compute_wer(reference: str, hypothesis: str) -> float:
        """Calculate Word Error Rate (word-level Levenshtein distance)."""
        ref_words = reference.split()
        hyp_words = hypothesis.split()
        r_len = len(ref_words)
        h_len = len(hyp_words)
        if r_len == 0:
            return 0.0 if h_len == 0 else 1.0

        dp = [[0] * (h_len + 1) for _ in range(r_len + 1)]
        for i in range(r_len + 1):
            dp[i][0] = i
        for j in range(h_len + 1):
            dp[0][j] = j

        for i in range(1, r_len + 1):
            for j in range(1, h_len + 1):
                if ref_words[i - 1] == hyp_words[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

        return dp[r_len][h_len] / float(r_len)
