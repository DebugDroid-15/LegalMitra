"""LegalMitra Judicial Knowledge Infrastructure package.

Provides ontology, classification, citation parsing, precedent graphs,
legislative evolution tracking, privacy & restricted records policy,
coverage analytics, source inventory, identity resolution, corpus indexing,
and procedural history tracking.
"""

from legalmitra.judicial.judicial_ontology import (
    CourtEntity,
    InstitutionTier,
    JudicialSystemOntology,
    JurisdictionType,
)
from legalmitra.judicial.case_taxonomy import (
    CaseTaxonomyManager,
    DomainDefinition,
    ProceduralPosture,
    SubstantiveDomain,
)
from legalmitra.judicial.citation_normalizer import (
    CitationNormalizer,
    ParsedCitation,
    ReporterFamily,
)
from legalmitra.judicial.precedent_graph_engine import (
    BenchStrengthCategory,
    PrecedentEdge,
    PrecedentGraphEngine,
    PrecedentNode,
    TreatmentType,
)
from legalmitra.judicial.legislative_evolution import (
    JudicialActionOnStatute,
    JudicialStatuteInteraction,
    LegislativeActionType,
    LegislativeCausationLevel,
    LegislativeEvolutionEngine,
    LegislativeResponseToCase,
)
from legalmitra.judicial.restricted_records import (
    RedactionAuditResult,
    RestrictedRecordsPolicyEngine,
    RestrictionClassification,
)
from legalmitra.judicial.coverage_analytics import (
    CourtCoverageAssessment,
    CoverageTier,
    JudicialCoverageRegistry,
)
from legalmitra.judicial.source_inventory import (
    AccessRestriction,
    AcquisitionMethod,
    AcquisitionPriority,
    JudicialSourceDefinition,
    NationalJudicialSourceRegistry,
    ReuseStatus,
    SourceHealth,
    SourceType,
)
from legalmitra.judicial.identity_resolver import (
    CanonicalCaseIdentity,
    CaseIdentityResolver,
)
from legalmitra.judicial.corpus_indexer import (
    IndexedJudicialDocument,
    JudicialCorpusIndexer,
    ParagraphAnchor,
)
from legalmitra.judicial.procedural_history import (
    DisposalNature,
    ProceduralEvent,
    ProceduralHistoryGraph,
    ProceduralStage,
)

__all__ = [
    "CourtEntity",
    "InstitutionTier",
    "JudicialSystemOntology",
    "JurisdictionType",
    "CaseTaxonomyManager",
    "DomainDefinition",
    "ProceduralPosture",
    "SubstantiveDomain",
    "CitationNormalizer",
    "ParsedCitation",
    "ReporterFamily",
    "BenchStrengthCategory",
    "PrecedentEdge",
    "PrecedentGraphEngine",
    "PrecedentNode",
    "TreatmentType",
    "JudicialActionOnStatute",
    "JudicialStatuteInteraction",
    "LegislativeActionType",
    "LegislativeCausationLevel",
    "LegislativeEvolutionEngine",
    "LegislativeResponseToCase",
    "RedactionAuditResult",
    "RestrictedRecordsPolicyEngine",
    "RestrictionClassification",
    "CourtCoverageAssessment",
    "CoverageTier",
    "JudicialCoverageRegistry",
    "AccessRestriction",
    "AcquisitionMethod",
    "AcquisitionPriority",
    "JudicialSourceDefinition",
    "NationalJudicialSourceRegistry",
    "ReuseStatus",
    "SourceHealth",
    "SourceType",
    "CanonicalCaseIdentity",
    "CaseIdentityResolver",
    "IndexedJudicialDocument",
    "JudicialCorpusIndexer",
    "ParagraphAnchor",
    "DisposalNature",
    "ProceduralEvent",
    "ProceduralHistoryGraph",
    "ProceduralStage",
]
