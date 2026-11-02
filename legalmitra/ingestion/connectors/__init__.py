"""
Phase 85: Multi-Source Connectors Package Init
"""

from legalmitra.ingestion.connectors.aikosh_connector import AIKoshConnector
from legalmitra.ingestion.connectors.base import BaseConnector, IngestionDocument, IngestionOrigin
from legalmitra.ingestion.connectors.huggingface_connector import HuggingFaceConnector
from legalmitra.ingestion.connectors.indiacode_connector import IndiaCodeConnector
from legalmitra.ingestion.connectors.kaggle_escr_connector import KaggleESCRConnector
from legalmitra.ingestion.connectors.orchestrator import IngestionResult, MultiSourceIngestionPipeline

__all__ = [
    "BaseConnector",
    "IngestionDocument",
    "IngestionOrigin",
    "IndiaCodeConnector",
    "AIKoshConnector",
    "HuggingFaceConnector",
    "KaggleESCRConnector",
    "MultiSourceIngestionPipeline",
    "IngestionResult",
]
