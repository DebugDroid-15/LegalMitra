# LegalMitra Central Legislation Acquisition Pipeline

**System Architecture Specification — Phase 15B**  
**Version:** 1.0.0  
**Engine Implementation:** `legalmitra/ingestion/acquisition.py`  
**Checkpoint File:** `data/08_corpus/acquisition_checkpoint.json`  
**Classification:** Resumable Retrieval, Checkpointing & Provenance Verification

---

## 1. Architectural Purpose

The Acquisition Pipeline provides an auditable, rate-limited, and fault-tolerant mechanism to ingest official Indian central legislation into LegalMitra. It establishes a verifiable boundary between raw acquired network payloads and parsed knowledge chunks.

### Core Acquisition Standards:
1. **Official Government Endpoints Only:** Ingestion connects exclusively to authenticated repositories (`indiacode.gov.in`, `egazette.gov.in`, `legislative.gov.in`, `sci.gov.in`).
2. **Deterministic Checkpointing:** The state of every acquired document is recorded in `data/08_corpus/acquisition_checkpoint.json`. Re-runs verify local disk checksums against the checkpoint, ensuring zero unnecessary re-downloads.
3. **Throttled Pacing:** A strict 30 requests-per-minute throttle is enforced, coupled with exponential backoff for network resilience.
4. **Cryptographic Checksum Verification:** SHA-256 digests are computed immediately upon disk write. Any modification or truncation triggers quarantine.
5. **Zero-Byte Quarantine:** Empty or incomplete files are automatically flagged with `is_quarantined = True` and excluded from downstream parsing.

---

## 2. Ingestion Metadata Model

For every acquired legal document, the acquisition record captures:
- `document_id`: Canonical stable identifier (e.g. `IND-CONST-1950`, `IND-STAT-BNS-2023`).
- `official_title`: Exact official title as enacted by Parliament.
- `source_url`: Verifiable URL on government portal.
- `local_path`: Immutable raw file storage in `data/01_raw/`.
- `checksum`: SHA-256 cryptographic hash of the raw payload.
- `byte_size`: File size in bytes.
- `retrieval_timestamp`: ISO 8601 acquisition timestamp.
- `http_status`: HTTP response code (200 for successful pulls).
- `is_quarantined`: Boolean flag indicating quarantine status.
- `quarantine_reason`: Reason for quarantine if flagged.
- `verification_tier`: `primary_official` or `regulatory_official`.

