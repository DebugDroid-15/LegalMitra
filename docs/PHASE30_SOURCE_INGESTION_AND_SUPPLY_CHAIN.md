# Phase 30: Source Ingestion, Supply-Chain & Dependency Security Audit
**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Owner:** Team Shatrujeet (Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo)  
**Classification:** Proprietary and Confidential  
**Date:** October 2026  
**Phase:** 30  

---

## 1. Supply-Chain & Dependency Inventory

The application dependencies in `pyproject.toml` were audited:
- `pydantic>=2.5.0` (Robust data parsing and typed validation)
- `pydantic-settings>=2.0.0`
- `docling>=2.0.0`
- `requests>=2.31.0` (Patched against CVE-2023-32681)
- `pyyaml>=6.0.0` (Uses safe loading semantics)
- `python-dotenv>=1.0.0`

### Secret Hygiene Check:
- Verified that zero API keys, database credentials, or secret tokens are committed in code or configuration files.
- Configuration defaults use environment variables (`LEGALMITRA_KB_PATH`, `LEGALMITRA_CONV_PATH`, `RATE_LIMIT_PER_MINUTE`, `ALLOWED_ORIGINS`).

---

## 2. Ingestion Pipeline Hardening

The ingestion subsystem (`LegislationAcquisitionManager` in `legalmitra/ingestion/acquisition.py`) enforces strict intake controls:

1. **Cryptographic Checksum Verification:** Every incoming payload computes a SHA-256 hash using `compute_file_sha256`. If the on-disk hash does not match the checkpoint, re-indexing is flagged.
2. **Zero-Byte Payload Quarantine:** Empty or truncated files automatically trigger `is_quarantined = True` with `quarantine_reason = "Zero-byte file payload detected."`
3. **Outbound SSRF Sanitization:** Outbound acquisition URLs are validated using `validate_outbound_legal_url`. Private IP literals, loopbacks, cloud metadata endpoints (`169.254.169.254`), and non-HTTP protocols are automatically rejected and quarantined with `quarantine_reason = "Security quarantine: Prohibited or malformed source URL"`.
4. **Idempotent Checkpointing:** Checkpoint records are atomically written to `acquisition_checkpoint.tmp` before renaming, preventing file corruption upon sudden power loss or process kill.
