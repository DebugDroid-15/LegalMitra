"""
LegalMitra Validation Package
"""

from legalmitra.validation.deduplication import DeduplicationEngine
from legalmitra.validation.grounding_validator import GroundingValidator
from legalmitra.validation.pydantic_validator import SchemaValidator
from legalmitra.validation.quality_gate import DataQualityGate, QualityGateResult
from legalmitra.validation.temporal_validator import TemporalValidator

__all__ = [
    "SchemaValidator",
    "GroundingValidator",
    "DeduplicationEngine",
    "TemporalValidator",
    "DataQualityGate",
    "QualityGateResult",
]

