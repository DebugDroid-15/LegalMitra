"""
Phase 85: AI Kosh (IndiaAI Knowledge Hub) Connector
Ingests sovereign datasets, administrative gazette notifications, and official
policy blueprints published by the Ministry of Electronics & IT (MeitY) / IndiaAI.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from legalmitra.core.enums import SourceType
from legalmitra.ingestion.connectors.base import BaseConnector, IngestionDocument, IngestionOrigin

logger = logging.getLogger("aikosh_connector")

# Curated catalog of AI Kosh sovereign datasets & gazette archives
AI_KOSH_CATALOG = [
    {
        "document_id": "AIKOSH-GAZ-2024-MHA-SO848E",
        "title": "MHA Commencement Notification S.O. 848(E) - BNS 2023 Enforcement",
        "source_url": "https://aikosh.indiaai.gov.in/datasets/mha-bns-enforcement-notification",
        "document_date": "2024-02-23",
        "effective_date": "2024-07-01",
        "source_type": SourceType.GAZETTE,
        "jurisdiction": "IN",
        "content": """MINISTRY OF HOME AFFAIRS NOTIFICATION
New Delhi, the 23rd February, 2024
S.O. 848(E).—In exercise of the powers conferred by sub-section (3) of section 1 of the Bharatiya Nyaya Sanhita, 2023 (45 of 2023), the Central Government hereby appoints the 1st day of July, 2024 as the date on which the provisions of the said Sanhita, except the provisions of sub-section (2) of section 106, shall come into force.
[F. No. 25014/14/2023-Judl.Cell-I]
PRAVEEN VASISHTA, Addl. Secy.
"""
    },
    {
        "document_id": "AIKOSH-GAZ-2024-MHA-SO849E",
        "title": "MHA Commencement Notification S.O. 849(E) - BNSS 2023 Enforcement",
        "source_url": "https://aikosh.indiaai.gov.in/datasets/mha-bnss-enforcement-notification",
        "document_date": "2024-02-23",
        "effective_date": "2024-07-01",
        "source_type": SourceType.GAZETTE,
        "jurisdiction": "IN",
        "content": """MINISTRY OF HOME AFFAIRS NOTIFICATION
New Delhi, the 23rd February, 2024
S.O. 849(E).—In exercise of the powers conferred by sub-section (3) of section 1 of the Bharatiya Nagarik Suraksha Sanhita, 2023 (46 of 2023), the Central Government hereby appoints the 1st day of July, 2024 as the date on which the provisions of the said Sanhita shall come into force.
[F. No. 25014/14/2023-Judl.Cell-I]
PRAVEEN VASISHTA, Addl. Secy.
"""
    },
    {
        "document_id": "AIKOSH-DATASET-2024-LEGAL-TERMINOLOGY",
        "title": "IndiaAI / AI Kosh Standardized Bilingual Legal Terminology Lexicon",
        "source_url": "https://aikosh.indiaai.gov.in/datasets/indiaai-legal-lexicon-v1",
        "document_date": "2024-05-10",
        "effective_date": "2024-05-10",
        "source_type": SourceType.OTHER,
        "jurisdiction": "IN",
        "content": """# INDIA-AI SOVEREIGN LEGAL TERMINOLOGY LEXICON (ENGLISH - HINDI)
Jurisdiction: National Legal Knowledge Graph
Publisher: MeitY & IndiaAI Consortium

TERMS:
1. "First Information Report (FIR)" -> "प्रथम सूचना रिपोर्ट" (Section 173 BNSS)
2. "Cognizable Offence" -> "संज्ञेय अपराध" (Police may arrest without warrant)
3. "Non-bailable Offence" -> "गैर-जमानती अपराध" (Bail is judicial discretion)
4. "Anticipatory Bail" -> "अग्रिम जमानत" (Section 482 BNSS)
5. "Criminal Breach of Trust" -> "आपराधिक विश्वासघात" (Section 316 BNS)
6. "Cheating" -> "धोखाधड़ी" (Section 318 BNS)
7. "Quashing of FIR" -> "प्राथमिकी रद्द करना" (Section 528 BNSS)
8. "Data Principal" -> "डेटा स्वामी" (Section 2(j) DPDP Act 2023)
9. "Data Fiduciary" -> "डेटा न्यासी" (Section 2(i) DPDP Act 2023)
"""
    }
]


class AIKoshConnector:
    """Connector for AI Kosh sovereign datasets and gazettes."""
    origin = IngestionOrigin.AI_KOSH

    def __init__(self, catalog: Optional[List[Dict[str, Any]]] = None):
        self.catalog = catalog or AI_KOSH_CATALOG

    def fetch_documents(self, limit: Optional[int] = None) -> List[IngestionDocument]:
        documents: List[IngestionDocument] = []
        target = self.catalog[:limit] if limit else self.catalog

        for item in target:
            doc = IngestionDocument(
                document_id=item["document_id"],
                title=item["title"],
                source_url=item["source_url"],
                source_type=item["source_type"],
                jurisdiction=item["jurisdiction"],
                document_date=item["document_date"],
                effective_date=item.get("effective_date"),
                origin=self.origin,
                content_raw=item["content"],
                file_format=".txt",
                metadata={"platform": "AI Kosh / IndiaAI", "dataset_id": item["document_id"]},
                license_or_terms="Government of India Open Data License (GODL-India)"
            )
            documents.append(doc)

        logger.info(f"AIKoshConnector prepared {len(documents)} sovereign records.")
        return documents
