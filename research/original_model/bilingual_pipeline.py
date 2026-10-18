"""
Bilingual Legal Text Pipeline for LegalMitra Phase 33.
Processes English, Hindi (Devanagari), and mixed bilingual legal texts.
Provides Unicode normalization (NFC), Devanagari preservation, citation parsing,
deduplication, provenance tracking, and source-aware chunking.
"""

import hashlib
import json
import re
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any


@dataclass
class LegalPassage:
    """Standardized bilingual legal passage with full provenance."""
    passage_id: str
    source_id: str
    official_title: str
    document_family: str
    language: str  # 'en', 'hi', 'mixed'
    provision_ref: str
    authority_level: str
    jurisdiction: str
    content: str
    normalized_content: str
    token_count: int = 0
    char_count: int = 0
    sha256: str = ""
    is_official_translation: bool = False
    source_provenance: str = ""
    license_terms: str = "Section 52(1)(q) Indian Copyright Act 1957 / GODL-India"


class BilingualLegalPipeline:
    """
    Multilingual preprocessing and normalization engine for Indian statutory & judicial texts.
    Guarantees strict provenance, Unicode integrity, and Devanagari preservation.
    """

    def __init__(self):
        # Regex patterns for Hindi/Devanagari and English
        self.devanagari_regex = re.compile(r"[\u0900-\u097F]")
        self.english_regex = re.compile(r"[A-Za-z]")
        
        # Statutory citation patterns
        self.en_section_regex = re.compile(r"(?:Section|Sec\.|Article|Art\.|Clause)\s+(\d+[A-Za-z]*(?:\(\d+\))*(?:\([a-z]+\))*)", re.IGNORECASE)
        self.hi_section_regex = re.compile(r"(?:धारा|अनुच्छेद|खंड)\s+([0-9\u0966-\u096F]+[A-Za-z\u0900-\u097F]*(?:\([0-9\u0966-\u096F]+\))*(?:\([a-z\u0900-\u097F]+\))*)")
        
        # Devanagari numeral translation table
        self.devanagari_digits = "०१२३४५६७८९"
        self.ascii_digits = "0123456789"
        self.dev_to_ascii = str.maketrans(self.devanagari_digits, self.ascii_digits)

    def normalize_text(self, text: str) -> str:
        """
        Normalize text to Unicode NFC, standardize whitespace,
        and preserve valid Devanagari matras and conjuncts.
        """
        if not text:
            return ""
        
        # 1. Unicode NFC Normalization (canonical composition)
        text = unicodedata.normalize("NFC", text)
        
        # 2. Standardize carriage returns and tabs
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = text.replace("\t", " ")
        
        # 3. Collapse multiple non-newline whitespaces
        lines = []
        for line in text.split("\n"):
            line = re.sub(r"[^\S\n]+", " ", line).strip()
            if line:
                lines.append(line)
        
        normalized = "\n".join(lines)
        return normalized

    def detect_language(self, text: str) -> str:
        """Classify passage as English ('en'), Hindi ('hi'), or Mixed ('mixed')."""
        has_devanagari = bool(self.devanagari_regex.search(text))
        has_english = bool(self.english_regex.search(text))
        
        if has_devanagari and has_english:
            return "mixed"
        elif has_devanagari:
            return "hi"
        else:
            return "en"

    def extract_citations(self, text: str) -> Dict[str, List[str]]:
        """Extract statutory citations across English and Hindi notation."""
        en_citations = self.en_section_regex.findall(text)
        hi_citations = self.hi_section_regex.findall(text)
        return {
            "english_citations": en_citations,
            "hindi_citations": hi_citations,
        }

    def process_passage(
        self,
        passage_id: str,
        source_id: str,
        title: str,
        document_family: str,
        provision_ref: str,
        content: str,
        authority_level: str = "central_statute",
        jurisdiction: str = "IN",
        is_official: bool = True,
        provenance: str = "Government of India Official Gazette / India Code",
    ) -> Optional[LegalPassage]:
        """
        Process, normalize, validate, and hash a legal passage.
        Rejects zero-length or malformed passages.
        """
        normalized = self.normalize_text(content)
        if len(normalized.strip()) < 10:
            # Reject malformed or empty text
            return None
        
        lang = self.detect_language(normalized)
        sha256_hash = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
        
        return LegalPassage(
            passage_id=passage_id,
            source_id=source_id,
            official_title=title,
            document_family=document_family,
            language=lang,
            provision_ref=provision_ref,
            authority_level=authority_level,
            jurisdiction=jurisdiction,
            content=content,
            normalized_content=normalized,
            char_count=len(normalized),
            sha256=sha256_hash,
            is_official_translation=is_official,
            source_provenance=provenance,
        )

    def deduplicate_passages(self, passages: List[LegalPassage]) -> Tuple[List[LegalPassage], int]:
        """Deduplicate passages based on exact SHA256 of normalized text."""
        seen_hashes = set()
        unique_passages = []
        duplicate_count = 0
        
        for p in passages:
            if p.sha256 in seen_hashes:
                duplicate_count += 1
            else:
                seen_hashes.add(p.sha256)
                unique_passages.append(p)
                
        return unique_passages, duplicate_count

