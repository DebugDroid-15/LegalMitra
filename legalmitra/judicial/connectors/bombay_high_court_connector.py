"""LegalMitra Judicial Knowledge Infrastructure — High Court of Judicature at Bombay Connector.

Specialized adapter for Bombay High Court official judgment portal (SRC-HC-BOM-PORTAL).
Supports multi-bench selections (Mumbai Original Side, Appellate Side, Nagpur, Aurangabad, Panaji-Goa)
and bench-specific neutral citation formats (YYYY:BHC-OS:NNNN, YYYY:BHC-AS:NNNN, YYYY:BHC-NAG:NNNN).
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

from legalmitra.judicial.connectors.connector_base import (
    AcquiredPayload,
    BaseJudicialConnector,
    BoundedResponseError,
    DiscoveredDocument,
    SourceDocumentState,
    SSRFProtectionError,
)


class BombayHighCourtConnector(BaseJudicialConnector):
    """Adapter for Bombay High Court multi-bench judgments."""

    _VALID_BENCHES = {"OS": "Original Side (Mumbai)", "AS": "Appellate Side (Mumbai)", "NAG": "Nagpur Bench", "AUR": "Aurangabad Bench", "GOA": "Panaji Bench (Goa)"}

    def __init__(
        self,
        requests_per_minute: int = 12,
        max_response_bytes: int = 25 * 1024 * 1024,
        request_timeout_seconds: int = 30,
        is_live_enabled: bool = False,
        dry_run: bool = True,
        fixture_payloads: Optional[Dict[str, bytes]] = None,
    ) -> None:
        super().__init__(
            source_id="SRC-HC-BOM-PORTAL",
            court_id="IND-HC-BOM",
            allowed_domains=["bombayhighcourt.nic.in", "bhc.gov.in"],
            requests_per_minute=requests_per_minute,
            max_response_bytes=max_response_bytes,
            request_timeout_seconds=request_timeout_seconds,
            is_live_enabled=is_live_enabled,
            dry_run=dry_run,
        )
        self.fixture_payloads = fixture_payloads or {}

    def discover_documents(self, filter_params: Dict[str, Any]) -> List[DiscoveredDocument]:
        bench_code = filter_params.get("bench_code", "OS").upper()
        if bench_code not in self._VALID_BENCHES:
            raise ValueError(f"Invalid Bombay High Court bench '{bench_code}'. Valid benches: {list(self._VALID_BENCHES.keys())}")

        year = filter_params.get("year", 2023)
        limit = filter_params.get("limit", 10)
        case_type = filter_params.get("case_type", "WP")

        discovered: List[DiscoveredDocument] = []
        for i in range(1, limit + 1):
            doc_id = f"BOM-{bench_code}-{year}-{case_type}-{i:04d}"
            neutral_cit = f"{year}:BHC-{bench_code}:{i:04d}"
            url = f"https://bombayhighcourt.nic.in/judgments/{bench_code.lower()}/{year}/{doc_id}.pdf"

            doc = DiscoveredDocument(
                document_id=doc_id,
                court_id=self.court_id,
                source_id=self.source_id,
                source_url=url,
                case_number=f"{case_type} No. {i} of {year}",
                neutral_citation=neutral_cit,
                decision_date=f"{year}-06-20",
                party_title=f"Commercial Petitioner {i} v. State of Maharashtra & Ors.",
                discovered_timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                current_state=SourceDocumentState.DISCOVERED,
            )
            discovered.append(doc)

        return discovered

    def acquire_document(self, discovered_doc: DiscoveredDocument) -> AcquiredPayload:
        self.validate_url_security(discovered_doc.source_url)
        self.rate_limiter.wait_if_needed()

        if self.dry_run:
            discovered_doc.transition(SourceDocumentState.ACQUIRED, "Dry-run acquisition simulated")
            mock_bytes = b"%PDF-1.4 Simulated Bombay High Court Payload"
            sha = self.compute_sha256(mock_bytes)
            return AcquiredPayload(
                document_id=discovered_doc.document_id,
                source_url=discovered_doc.source_url,
                content_bytes=mock_bytes,
                sha256_hash=sha,
                content_type="application/pdf",
                byte_count=len(mock_bytes),
                acquisition_timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                is_dry_run=True,
            )

        if discovered_doc.document_id in self.fixture_payloads:
            content = self.fixture_payloads[discovered_doc.document_id]
            if len(content) > self.max_response_bytes:
                raise BoundedResponseError(f"Response size {len(content)} exceeds ceiling {self.max_response_bytes}")

            sha = self.compute_sha256(content)
            self.record_hash(sha)
            discovered_doc.transition(SourceDocumentState.ACQUIRED, "Fixture payload acquired successfully")
            return AcquiredPayload(
                document_id=discovered_doc.document_id,
                source_url=discovered_doc.source_url,
                content_bytes=content,
                sha256_hash=sha,
                content_type="application/pdf",
                byte_count=len(content),
                acquisition_timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                is_dry_run=False,
            )

        if not self.is_live_enabled:
            discovered_doc.transition(SourceDocumentState.BLOCKED_ACCESS_DENIED, "Live mode is disabled by safety policy")
            raise PermissionError("Live endpoint acquisition disabled. Enable is_live_enabled=True with approved authorization.")

        # Live request (safe urllib)
        import urllib.request
        req = urllib.request.Request(
            discovered_doc.source_url,
            headers={"User-Agent": "LegalMitra-Academic-Research/1.0 (Indian Legal Source Ingestion)"},
        )
        with urllib.request.urlopen(req, timeout=self.request_timeout_seconds) as resp:
            content_type = resp.headers.get_content_type()
            raw_data = resp.read(self.max_response_bytes + 1)
            if len(raw_data) > self.max_response_bytes:
                raise BoundedResponseError(f"Live response exceeded {self.max_response_bytes} bytes")

        sha = self.compute_sha256(raw_data)
        self.record_hash(sha)
        discovered_doc.transition(SourceDocumentState.ACQUIRED, "Live payload acquired successfully")
        return AcquiredPayload(
            document_id=discovered_doc.document_id,
            source_url=discovered_doc.source_url,
            content_bytes=raw_data,
            sha256_hash=sha,
            content_type=content_type,
            byte_count=len(raw_data),
            acquisition_timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            is_dry_run=False,
        )
