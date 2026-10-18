"""LegalMitra Judicial Knowledge Infrastructure — Coverage Analytics & Gap Accounting.

Implements the 11-tier coverage framework (Tier 0 to Tier 10) to distinguish catalogued
institutions from acquired records, preventing misleading universal-coverage claims.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any, Dict, List, Optional


class CoverageTier(IntEnum):
    TIER_0_UNMAPPED = 0
    TIER_1_CATALOGUED = 1
    TIER_2_SOURCE_IDENTIFIED = 2
    TIER_3_PIPELINE_DESIGNED = 3
    TIER_4_PIPELINE_TESTED = 4
    TIER_5_SAMPLING_VALIDATED = 5
    TIER_6_SUBSTANTIAL_HOLDINGS = 6
    TIER_7_COMPREHENSIVE_ERA = 7
    TIER_8_PRECEDENT_INTEGRATED = 8
    TIER_9_MULTILINGUAL_EXPANDED = 9
    TIER_10_INDEPENDENTLY_EVALUATED = 10


@dataclass
class CourtCoverageAssessment:
    court_id: str
    court_name: str
    institutional_tier: str
    current_tier: CoverageTier
    total_estimated_historical_cases: int
    ingested_record_count: int
    verified_record_count: int
    ocr_average_confidence: float
    vernacular_languages_supported: List[str] = field(default_factory=list)
    precedent_graph_linked_nodes: int = 0
    known_coverage_gaps: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "court_id": self.court_id,
            "court_name": self.court_name,
            "institutional_tier": self.institutional_tier,
            "current_tier": int(self.current_tier),
            "tier_label": self.current_tier.name,
            "total_estimated_historical_cases": self.total_estimated_historical_cases,
            "ingested_record_count": self.ingested_record_count,
            "verified_record_count": self.verified_record_count,
            "ocr_average_confidence": self.ocr_average_confidence,
            "vernacular_languages_supported": self.vernacular_languages_supported,
            "precedent_graph_linked_nodes": self.precedent_graph_linked_nodes,
            "known_coverage_gaps": self.known_coverage_gaps,
        }


class JudicialCoverageRegistry:
    """Tracks empirical coverage across all Indian courts and tribunals."""

    def __init__(self) -> None:
        self._assessments: Dict[str, CourtCoverageAssessment] = {}
        self._populate_initial_matrix()

    def register_assessment(self, assessment: CourtCoverageAssessment) -> None:
        self._assessments[assessment.court_id] = assessment

    def get_assessment(self, court_id: str) -> Optional[CourtCoverageAssessment]:
        return self._assessments.get(court_id)

    def list_all_assessments(self) -> List[CourtCoverageAssessment]:
        return list(self._assessments.values())

    def get_national_summary(self) -> Dict[str, Any]:
        total_institutions = len(self._assessments)
        tier_counts = {t.name: 0 for t in CoverageTier}
        total_ingested = sum(a.ingested_record_count for a in self._assessments.values())
        total_verified = sum(a.verified_record_count for a in self._assessments.values())

        for a in self._assessments.values():
            tier_counts[a.current_tier.name] += 1

        return {
            "total_institutions_tracked": total_institutions,
            "total_ingested_records": total_ingested,
            "total_verified_records": total_verified,
            "tier_distribution": tier_counts,
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary": self.get_national_summary(),
            "assessments": {cid: a.to_dict() for cid, a in self._assessments.items()},
        }

    def _populate_initial_matrix(self) -> None:
        # Supreme Court
        self.register_assessment(CourtCoverageAssessment(
            court_id="IND-SC",
            court_name="Supreme Court of India",
            institutional_tier="APEX",
            current_tier=CoverageTier.TIER_5_SAMPLING_VALIDATED,
            total_estimated_historical_cases=75000,
            ingested_record_count=185,
            verified_record_count=185,
            ocr_average_confidence=0.985,
            vernacular_languages_supported=["en", "hi"],
            precedent_graph_linked_nodes=62,
            known_coverage_gaps=["Full retrospective archive 1950-1990 pending systematic batch acquisition"],
        ))

        # Delhi High Court
        self.register_assessment(CourtCoverageAssessment(
            court_id="IND-HC-DEL",
            court_name="High Court of Delhi",
            institutional_tier="HIGH_COURT",
            current_tier=CoverageTier.TIER_5_SAMPLING_VALIDATED,
            total_estimated_historical_cases=120000,
            ingested_record_count=112,
            verified_record_count=112,
            ocr_average_confidence=0.978,
            vernacular_languages_supported=["en"],
            precedent_graph_linked_nodes=24,
            known_coverage_gaps=["Pre-2000 digital unreported decisions unavailable on public portal"],
        ))

        # Bombay High Court
        self.register_assessment(CourtCoverageAssessment(
            court_id="IND-HC-BOM",
            court_name="High Court of Judicature at Bombay",
            institutional_tier="HIGH_COURT",
            current_tier=CoverageTier.TIER_2_SOURCE_IDENTIFIED,
            total_estimated_historical_cases=250000,
            ingested_record_count=22,
            verified_record_count=22,
            ocr_average_confidence=0.962,
            vernacular_languages_supported=["en", "mr"],
            precedent_graph_linked_nodes=8,
            known_coverage_gaps=["Nagpur, Aurangabad, and Goa benches require dedicated crawler adaptation"],
        ))

        # Armed Forces Tribunal
        self.register_assessment(CourtCoverageAssessment(
            court_id="IND-MIL-AFT",
            court_name="Armed Forces Tribunal",
            institutional_tier="MILITARY_JUSTICE",
            current_tier=CoverageTier.TIER_2_SOURCE_IDENTIFIED,
            total_estimated_historical_cases=35000,
            ingested_record_count=14,
            verified_record_count=14,
            ocr_average_confidence=0.954,
            vernacular_languages_supported=["en"],
            precedent_graph_linked_nodes=4,
            known_coverage_gaps=["Regional bench orders (Lucknow, Jaipur, Kochi) maintained in separate registries"],
        ))

        # NCLAT
        self.register_assessment(CourtCoverageAssessment(
            court_id="IND-TR-NCLAT",
            court_name="National Company Law Appellate Tribunal",
            institutional_tier="TRIBUNAL",
            current_tier=CoverageTier.TIER_3_PIPELINE_DESIGNED,
            total_estimated_historical_cases=15000,
            ingested_record_count=18,
            verified_record_count=18,
            ocr_average_confidence=0.981,
            vernacular_languages_supported=["en"],
            precedent_graph_linked_nodes=6,
            known_coverage_gaps=["Chennai Bench orders require distinct pagination handler"],
        ))

        # NGT
        self.register_assessment(CourtCoverageAssessment(
            court_id="IND-TR-NGT",
            court_name="National Green Tribunal",
            institutional_tier="TRIBUNAL",
            current_tier=CoverageTier.TIER_2_SOURCE_IDENTIFIED,
            total_estimated_historical_cases=28000,
            ingested_record_count=12,
            verified_record_count=12,
            ocr_average_confidence=0.974,
            vernacular_languages_supported=["en"],
            precedent_graph_linked_nodes=4,
            known_coverage_gaps=["Zonal bench orders (Western, Eastern, Southern, Central) to be integrated"],
        ))

        # Subordinate District Courts
        self.register_assessment(CourtCoverageAssessment(
            court_id="IND-DIST-GENERIC",
            court_name="Subordinate Judiciary Hierarchy (District & Sessions Level)",
            institutional_tier="DISTRICT_COURT",
            current_tier=CoverageTier.TIER_1_CATALOGUED,
            total_estimated_historical_cases=15000000,
            ingested_record_count=35,
            verified_record_count=35,
            ocr_average_confidence=0.941,
            vernacular_languages_supported=["en", "hi"],
            precedent_graph_linked_nodes=2,
            known_coverage_gaps=["680+ District Court establishments via eCourts require large-scale distributed architecture"],
        ))
