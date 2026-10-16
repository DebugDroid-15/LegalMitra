"""
LegalMitra Case Law Package
"""

from legalmitra.caselaw.precedent import (
    BenchStrength,
    CaseLawMetadata,
    PrecedentHierarchyManager,
    PrecedentRelationship,
    PrecedentTreatment,
    build_default_precedent_manager,
)

__all__ = [
    "BenchStrength",
    "PrecedentTreatment",
    "PrecedentRelationship",
    "CaseLawMetadata",
    "PrecedentHierarchyManager",
    "build_default_precedent_manager",
]

