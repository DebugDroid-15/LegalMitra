"""
LegalMitra Normalization Package
"""

from legalmitra.normalization.clean_text import extract_paragraphs, sanitize_legal_text
from legalmitra.normalization.judgment_normalizer import JudgmentNormalizer
from legalmitra.normalization.normalizer import DocumentNormalizer
from legalmitra.normalization.statute_normalizer import StatuteNormalizer

__all__ = [
    "sanitize_legal_text",
    "extract_paragraphs",
    "StatuteNormalizer",
    "JudgmentNormalizer",
    "DocumentNormalizer",
]

