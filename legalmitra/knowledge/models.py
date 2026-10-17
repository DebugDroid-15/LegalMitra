"""
LegalMitra Knowledge Base Models
Defines search filters, result representations, and indexing hierarchy
for the Indian Legal Knowledge Base.
"""

from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ChunkHierarchy(str, Enum):
    SECTION = "section"
    SUBSECTION = "subsection"
    PROVISO = "proviso"
    EXPLANATION = "explanation"
    ILLUSTRATION = "illustration"
    PARAGRAPH = "paragraph"
    HOLDING = "holding"
    RATIO = "ratio"
    OBITER = "obiter"


class AuthorityLevel(str, Enum):
    BINDING_STATUTE = "binding_statute"
    BINDING_PRECEDENT = "binding_precedent"        # Supreme Court of India under Art. 141
    PERSUASIVE_PRECEDENT = "persuasive_precedent"  # High Court outside territorial jurisdiction
    UNVERIFIED_SCAFFOLD = "unverified_scaffold"    # Synthetic or unverified mock document


class SearchFilters(BaseModel):
    """
    Search and retrieval metadata filters.
    Enforces jurisdictional, temporal, and authority boundaries.
    """
    jurisdiction: Optional[str] = Field(
        default=None,
        description="Jurisdiction code (e.g. 'IN', 'IN-DL')"
    )
    court: Optional[str] = Field(
        default=None,
        description="Court name (e.g. 'Supreme Court of India', 'High Court of Delhi')"
    )
    doc_type: Optional[str] = Field(
        default=None,
        description="'statute' or 'judgment'"
    )
    as_of_date: Optional[date] = Field(
        default=None,
        description="Filter for law in force on this specific date (distinguishes historical/superseded law)"
    )
    is_historical: Optional[bool] = Field(
        default=None,
        description="Explicitly query historical or repealed provisions if True"
    )
    include_synthetic: bool = Field(
        default=False,
        description="Safety flag: If False, completely excludes unverified synthetic scaffolds (e.g. IND-JUD-DEL-2024-BAIL)"
    )
    act_title: Optional[str] = Field(
        default=None,
        description="Filter by specific Act title or Case title"
    )
    section_number: Optional[str] = Field(
        default=None,
        description="Filter by specific section number (e.g. '61', '63', '43A')"
    )
    paragraph_number: Optional[int] = Field(
        default=None,
        description="Filter by specific judgment paragraph number"
    )
    hierarchy_level: Optional[str] = Field(
        default=None,
        description="Filter by hierarchy level: 'section', 'subsection', 'ratio', 'holding', 'paragraph'"
    )
    case_citation: Optional[str] = Field(
        default=None,
        description="Filter or lookup by official or neutral citation (e.g. '(2020) 7 SCC 1', '2020 INSC 452')"
    )


class SearchResult(BaseModel):
    """
    Structured legal search result returned from the Knowledge Base.
    Preserves exact verbatim content, provenance, and legal authority ranking.
    """
    chunk_id: str
    source_id: str
    doc_type: str
    act_or_case_title: str
    provision_or_para_ref: str
    hierarchy_level: str
    section_number: Optional[str] = None
    paragraph_number: Optional[int] = None
    jurisdiction: str
    court: str
    document_date: date
    effective_date: Optional[date] = None
    is_historical: bool = False
    is_synthetic_scaffold: bool = False
    authority_level: AuthorityLevel
    content: str
    source_url: str
    score: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)

