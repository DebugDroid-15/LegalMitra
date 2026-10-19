# PHASE 41 — HIGH COURT CONNECTORS OPERATIONAL AUDIT

## 1. Audit Scope & Component Architecture

This audit evaluated the operational reliability, security posture, concurrency safety, and execution states of the High Court connectors introduced in Phase 40:
- [`BaseJudicialConnector`](file:///c:/PROJECTS/LegalMitra/legalmitra/judicial/connectors/connector_base.py)
- [`DelhiHighCourtConnector`](file:///c:/PROJECTS/LegalMitra/legalmitra/judicial/connectors/delhi_high_court_connector.py) (`SRC-HC-DEL-PORTAL`)
- [`BombayHighCourtConnector`](file:///c:/PROJECTS/LegalMitra/legalmitra/judicial/connectors/bombay_high_court_connector.py) (`SRC-HC-BOM-PORTAL`)

---

## 2. Connector Execution Modes & Status Classification

In accordance with Section 3.1 of the Phase 41 specification, the connectors were audited across seven operational lifecycle capabilities:

| Execution Capability | Delhi HC Connector | Bombay HC Connector | Evidence & Operational Reality |
| :--- | :---: | :---: | :--- |
| **1. Interface / Architecture** | **VERIFIED** | **VERIFIED** | Abstract class hierarchy, 9-state lifecycle model, dataclasses, and error classes fully implemented. |
| **2. Deterministic Fixtures** | **VERIFIED** | **VERIFIED** | `dry_run=True` simulation and `fixture_payloads` lookup execute reliably and pass automated tests. |
| **3. Live Source Discovery** | **CONDITIONAL** | **CONDITIONAL** | Pattern-based neutral citation generation (`YYYY:DHC:NNNN`, `YYYY:BHC-OS:NNNN`) implemented; live DOM scraping of search forms requires network session. |
| **4. Live Document Acquisition** | **BLOCKED** | **BLOCKED** | Live network download disabled by default (`is_live_enabled=False`). Calling `acquire_document` without explicit authorization raises `PermissionError`. |
| **5. Authenticity Verification** | **VERIFIED** | **VERIFIED** | Cryptographic SHA-256 hash calculated over acquired/fixture payload bytes and recorded in `_acquired_hashes` set. |
| **6. Rights-Reviewed Indexing** | **VERIFIED** | **VERIFIED** | Verified under Section 52(1)(q) Copyright Act 1957; only raw judgments ingested without proprietary commercial headnotes. |
| **7. Retrieval Publication** | **VERIFIED** | **VERIFIED** | Clean documents transition to `RETRIEVAL_ELIGIBLE` and integrate with grounded RAG indices. |

---

## 3. Rate Limiting & Concurrency Hardening (DEF-41-002)

### The Defect
The Phase 40 [`RateLimiter`](file:///c:/PROJECTS/LegalMitra/legalmitra/judicial/connectors/connector_base.py) implementation used an unsynchronized `_last_request_time` timestamp. Under multithreaded ingestion or asynchronous task workers, race conditions allowed simultaneous requests to proceed with zero delay, potentially exceeding the 15 RPM (Delhi) and 12 RPM (Bombay) limits.

### Hardening Applied
In Phase 41, `RateLimiter` was hardened with thread synchronization:
```python
class RateLimiter:
    def __init__(self, requests_per_minute: int = 20) -> None:
        self.rpm = requests_per_minute
        self.min_interval = 60.0 / requests_per_minute
        self._last_request_time = 0.0
        self._lock = threading.Lock()

    def wait_if_needed(self) -> float:
        with self._lock:
            now = time.time()
            elapsed = now - self._last_request_time
            if elapsed < self.min_interval:
                delay = self.min_interval - elapsed
                time.sleep(delay)
                self._last_request_time = time.time()
                return delay
            self._last_request_time = now
            return 0.0
```
Verified in [`tests/test_phase41_forensic_audit.py::test_rate_limiter_multithreaded_safety`](file:///c:/PROJECTS/LegalMitra/tests/test_phase41_forensic_audit.py): 5 concurrent threads attempting immediate execution are properly throttled.

---

## 4. SSRF Defense Hardening & Open Redirect Protection (DEF-41-003)

### The Defect
1. `validate_url_security` in Phase 40 did not explicitly validate the target port, allowing potential port scanning (e.g. `https://delhihighcourt.nic.in:8080` or `:22`).
2. URLs with embedded user credentials (`https://user:pass@host/`) were not blocked.
3. Default `urllib.request.urlopen` follows HTTP 301/302 redirects automatically without re-validating the redirect target against the SSRF whitelist.

### Hardening Applied
1. **Port Restriction**: Explicitly restricted to standard HTTP/HTTPS ports (80, 443).
2. **Credential Blocking**: Rejecting URLs with `parsed.username` or `parsed.password`.
3. **IPv6 Parsing**: Stripped brackets `[]` and validated IPv6 loopback (`::1`), link-local (`fe80::`), and private IPv6 ranges.
4. **Redirect Revalidation**: Created [`SafeRedirectHandler`](file:///c:/PROJECTS/LegalMitra/legalmitra/judicial/connectors/connector_base.py) subclassing `HTTPRedirectHandler`:
```python
class SafeRedirectHandler(HTTPRedirectHandler):
    def __init__(self, security_validator) -> None:
        self.security_validator = security_validator
        super().__init__()

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.security_validator(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)
```
Verified in [`tests/test_phase41_forensic_audit.py`](file:///c:/PROJECTS/LegalMitra/tests/test_phase41_forensic_audit.py):
- `test_connector_ssrf_non_standard_port` -> PASSED
- `test_connector_ssrf_embedded_credentials` -> PASSED
- `test_connector_ssrf_ipv6_loopback_and_linklocal` -> PASSED
- `test_connector_safe_redirect_handler` -> PASSED
