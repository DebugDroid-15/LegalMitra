"""
LegalMitra Core Enums
Defines standard enumerations for the Indian Legal Dataset Engineering Pipeline.
"""

from enum import Enum


class SourceType(str, Enum):
    STATUTE = "statute"
    JUDGMENT = "judgment"
    NOTIFICATION = "notification"
    RULES_REGULATION = "rules_regulation"
    GAZETTE = "gazette"
    CIRCULAR = "circular"
    TRIBUNAL_ORDER = "tribunal_order"
    OTHER = "other"


class Jurisdiction(str, Enum):
    INDIA_CENTRAL = "IN"
    DELHI = "IN-DL"
    MAHARASHTRA = "IN-MH"
    KARNATAKA = "IN-KA"
    WEST_BENGAL = "IN-WB"
    TAMIL_NADU = "IN-TN"
    UTTAR_PRADESH = "IN-UP"
    GUJARAT = "IN-GJ"
    KERALA = "IN-KL"
    TELANGANA = "IN-TG"
    OTHER = "IN-OTHER"


class CourtType(str, Enum):
    SUPREME_COURT = "Supreme Court of India"
    HIGH_COURT_DELHI = "High Court of Delhi"
    HIGH_COURT_BOMBAY = "High Court of Bombay"
    HIGH_COURT_CALCUTTA = "High Court of Calcutta"
    HIGH_COURT_MADRAS = "High Court of Madras"
    HIGH_COURT_ALLAHABAD = "High Court of Judicature at Allahabad"
    HIGH_COURT_KARNATAKA = "High Court of Karnataka"
    DISTRICT_COURT = "District and Sessions Court"
    NCLAT = "National Company Law Appellate Tribunal"
    NCLT = "National Company Law Tribunal"
    OTHER_TRIBUNAL = "Other Specialized Tribunal"
    NONE = "None (Statutory / Executive)"


class LegalReviewStatus(str, Enum):
    """
    Explicit status of legal review. Automated validation NEVER establishes legal correctness.
    """
    UNVERIFIED_AUTOMATED = "unverified_automated"
    PENDING_LEGAL_REVIEW = "pending_legal_review"
    LEGAL_EXPERT_APPROVED = "legal_expert_approved"
    LEGAL_EXPERT_REJECTED = "legal_expert_rejected"
    FLAGGED_UNSUPPORTED = "flagged_unsupported"


class ProcessingStatus(str, Enum):
    REGISTERED = "registered"
    EXTRACTED = "extracted"
    NORMALIZED = "normalized"
    VALIDATED = "validated"
    FAILED = "failed"


class SplitType(str, Enum):
    TRAIN = "train"
    VALIDATION = "validation"
    TEST = "test"

