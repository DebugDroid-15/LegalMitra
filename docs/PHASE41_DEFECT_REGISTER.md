# PHASE 41 — DEFECT REGISTER & FORENSIC REMEDIATION LOG

## 1. Defect Classification Standard

In accordance with Section 12 of the Phase 41 specification, defects are classified under four rigorous severity tiers:
- **P0 — Critical**: Restricted data leakage, fabricated source provenance, retrieval of prohibited content, bypass of mandatory gates.
- **P1 — High**: False authenticity or rights status, incorrect legal identity, materially misleading evaluation results, security bypass.
- **P2 — Moderate**: Incorrect counts, broken idempotency, missing recovery behavior, metadata inaccuracies.
- **P3 — Low**: Documentation gaps, non-critical usability defects.

---

## 2. Identified Defects, Forensic Analysis & Remediation Log

| Defect ID | Severity | Component | Forensic Summary & Impact | Remediation & Status |
| :--- | :---: | :--- | :--- | :--- |
| **DEF-41-001** | **P2** | `coverage_matrix` | **Coverage Matrix Truncation**: `judicial_coverage_matrix_v3.json` summary claimed 615 records across 19 institutions, but the `assessments` object only contained 4 court keys (IND-SC, IND-HC-DEL, IND-HC-BOM, IND-DC-ECOURTS) summing to 490 records, omitting the other 15 institutions. | **Resolved**: Updated [`scripts/generate_phase40_artifacts.py`](file:///c:/PROJECTS/LegalMitra/scripts/generate_phase40_artifacts.py) to preserve all 19 tracked institutions from the baseline. Reconciled assessment counts to sum to exactly 615. |
| **DEF-41-002** | **P1** | `connectors` | **RateLimiter Thread Race Condition**: `RateLimiter.wait_if_needed` was not thread-safe. Concurrent worker tasks could execute simultaneously with 0 delay, violating polite QPS constraints. | **Resolved**: Added `threading.Lock()` to [`RateLimiter`](file:///c:/PROJECTS/LegalMitra/legalmitra/judicial/connectors/connector_base.py) ensuring atomic timestamp updates and verified multi-threaded throttling. |
| **DEF-41-003** | **P1** | `connectors` | **SSRF Port & Redirect Vulnerability**: `validate_url_security` did not restrict destination ports or embedded credentials (`user:pass@host`), and default `urlopen` could follow open redirects to unauthorized destinations. | **Resolved**: Enforced standard HTTP/HTTPS ports (80, 443), blocked URLs with user credentials, and added [`SafeRedirectHandler`](file:///c:/PROJECTS/LegalMitra/legalmitra/judicial/connectors/connector_base.py) to revalidate redirect targets. |
| **DEF-41-004** | **P2** | `ocr_eval` | **OCR Metric Scope Ambiguity**: Completion report did not clearly distinguish between diagnostic calibration fixtures and real-world noisy document scans, risking the impression of 99.5% universal Hindi OCR accuracy. | **Resolved**: Documented in `PHASE41_OCR_INDEPENDENT_EVALUATION.md` that the 5-sample manifest is a diagnostic fixture calibrating normalization rules, not an empirical test of noisy physical scans. |
| **DEF-41-005** | **P2** | `ecourts_protocol` | **CNR Semantic Existence Caveat**: 16-character CNR regex check only validates syntax; it cannot verify whether the case exists in a real court registry without eCommittee API integration. | **Resolved**: Explicitly documented distinction between syntactic validation and semantic existence in `PHASE41_ECOURTS_VALIDATION_AUDIT.md`. |

---

## 3. Residual Release Blockers & Operational Gates

- **Live Crawler Gate**: High Court connectors remain fixture-validated and live-gated (`is_live_enabled = False`) until formal registry permissions and off-peak scheduling windows are configured.
- **eCourts Automated Bulk Access**: Direct scraping of `services.ecourts.gov.in` remains blocked by visual CAPTCHAs. Automated bulk access requires eCommittee API partnership.
