"""
LegalMitra Procedural Guidance Schema
Structures practical procedural workflows under Indian civil, criminal, and constitutional practice.
"""

from typing import List, Optional
from pydantic import BaseModel, Field

from legalmitra.core.enums import Jurisdiction, LegalReviewStatus
from legalmitra.schemas.legal_qa import EvidencePassage


class ProceduralStep(BaseModel):
    """A distinct sequential step in an Indian legal procedure."""
    step_number: int = Field(..., ge=1)
    step_title: str = Field(...)
    action_description: str = Field(...)
    responsible_party: str = Field(..., description="e.g. 'Petitioner', 'Advocate on Record', 'Registry', 'Police'")
    statutory_rule: str = Field(..., description="Specific statutory rule or High Court rule governing step")
    timeline_or_deadline: Optional[str] = Field(
        default=None,
        description="Statutory timeframe (e.g. 'Within 30 days under Limitation Act')"
    )
    mandatory_documents: List[str] = Field(default_factory=list)


class ProceduralGuidanceDocument(BaseModel):
    """
    Step-by-step guidance for legal actions before Indian courts or tribunals.
    """
    guide_id: str = Field(..., description="e.g. 'PROC-BNSS-482-ANTICIPATORY-BAIL'")
    procedure_title: str = Field(..., min_length=5)
    governing_statutes: List[str] = Field(..., min_length=1, description="e.g. ['Bharatiya Nagarik Suraksha Sanhita, 2023']")
    forum_or_court: str = Field(..., description="e.g. 'Court of Sessions / High Court'")
    jurisdiction: Jurisdiction = Field(default=Jurisdiction.INDIA_CENTRAL)
    limitation_period: Optional[str] = Field(default=None)
    prerequisite_conditions: List[str] = Field(default_factory=list)
    steps: List[ProceduralStep] = Field(..., min_length=1)
    statutory_forms: List[str] = Field(default_factory=list, description="Forms under second schedule of Code or Rules")
    supporting_source_ids: List[str] = Field(..., min_length=1)
    evidence_passages: List[EvidencePassage] = Field(..., min_length=1)
    legal_disclaimer: str = Field(
        default="Procedural rules vary by High Court jurisdiction and local court rules. Verify current practice directions.",
        description="Mandatory disclaimer for procedural guidance"
    )
    legal_review_status: LegalReviewStatus = Field(default=LegalReviewStatus.UNVERIFIED_AUTOMATED)

