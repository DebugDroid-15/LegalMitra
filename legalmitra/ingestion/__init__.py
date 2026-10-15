"""
LegalMitra Ingestion Package
"""

from legalmitra.ingestion.ingestor import DocumentIngestor
from legalmitra.ingestion.registry import SourceRegistryManager

__all__ = ["SourceRegistryManager", "DocumentIngestor"]

