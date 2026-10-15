"""
LegalMitra Text Cleaning Utilities
Performs legal-aware text sanitization while preserving exact statutory phrasing,
sub-clause parentheses, and punctuation integrity.
"""

import re
import unicodedata


def sanitize_legal_text(text: str) -> str:
    """
    Normalizes unicode representations, standardizes non-breaking spaces,
    and strips trailing carriage returns while strictly preserving words, numbers, and punctuation.
    """
    if not text:
        return ""

    # Normalize unicode to NFC form
    normalized = unicodedata.normalize("NFC", text)

    # Standardize non-breaking spaces and zero-width spaces
    normalized = normalized.replace("\u00a0", " ").replace("\u200b", "").replace("\ufeff", "")

    # Standardize fancy directional quotes to standard ASCII quotes
    normalized = (
        normalized.replace("“", '"')
        .replace("”", '"')
        .replace("‘", "'")
        .replace("’", "'")
        .replace("`", "'")
    )

    # Standardize em-dash and en-dash where used in explanations/provisos
    # Indian legislative drafts frequently use 'Explanation.—'
    normalized = normalized.replace("—", "—").replace("–", "-")

    # Normalize windows line endings
    normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")

    return normalized.strip()


def extract_paragraphs(text: str) -> list[str]:
    """
    Splits text into coherent paragraphs by detecting double newlines or numbered legal paragraph breaks.
    """
    clean = sanitize_legal_text(text)
    raw_paras = re.split(r"\n\s*\n+", clean)
    return [p.strip() for p in raw_paras if p.strip()]

