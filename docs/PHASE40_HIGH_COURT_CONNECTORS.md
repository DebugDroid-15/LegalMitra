# PHASE 40 — HIGH COURT SOURCE CONNECTORS SPECIFICATION & RUNTIME AUDIT

## 1. Executive Summary & Objective

In Phase 40, LegalMitra operationalized lawful, rate-limited, SSRF-guarded acquisition adapters for two major Indian High Courts:
1. **High Court of Delhi** (`IND-HC-DEL`, `SRC-HC-DEL-PORTAL`)
2. **High Court of Judicature at Bombay** (`IND-HC-BOM`, `SRC-HC-BOM-PORTAL`)

The objective is to replace ad-hoc scraping with a hardened, reproducible connector architecture governed by strict security, network politeness, and provenance standards.

---

## 2. Connector Architecture & Lifecycle

All connectors inherit from [`BaseJudicialConnector`](file:///c:/PROJECTS/LegalMitra/legalmitra/judicial/connectors/connector_base.py) and operate along a formal **9-state lifecycle**:

```
REGISTERED -> ACCESS_REVIEWED -> DISCOVERED -> ACQUIRED -> PARSED ->
AUTHENTICITY_CHECKED -> RIGHTS_REVIEWED -> INDEXED -> RETRIEVAL_ELIGIBLE
```

Terminal error states:
- `BLOCKED_ACCESS_DENIED`
- `BLOCKED_QUALITY_FAILED`

### Key Invariants Enforced

| Parameter | Specification | Enforcement Mechanism |
| :--- | :--- | :--- |
| **Outbound SSRF Guard** | Strict domain whitelisting | `validate_url_security()` rejects loopback (`127.0.0.1`), link-local (`169.254.169.254`), private RFC1918 subnets, and non-whitelisted domains with [`SSRFProtectionError`](file:///c:/PROJECTS/LegalMitra/legalmitra/judicial/connectors/connector_base.py). |
| **Network Politeness** | 1.0 QPS (60 RPM) ceiling default (Delhi: 15 RPM, Bombay: 12 RPM) | [`RateLimiter`](file:///c:/PROJECTS/LegalMitra/legalmitra/judicial/connectors/connector_base.py) token-bucket with adaptive delay. |
| **Payload Bounding** | 25 MB max response size | [`BoundedResponseError`](file:///c:/PROJECTS/LegalMitra/legalmitra/judicial/connectors/connector_base.py) raised if payload exceeds memory limits. |
| **Deduplication** | Cryptographic SHA-256 idempotency | Re-acquisition of identical payload hashes skipped automatically. |
| **Dry-Run Separation** | Default `dry_run=True` | Live egress requires explicit boolean flag and approved credentials; offline tests execute via verified fixtures. |

---

## 3. High Court of Delhi Connector (`DelhiHighCourtConnector`)

- **Identifier**: `SRC-HC-DEL-PORTAL`
- **Target Portal**: `https://delhihighcourt.nic.in`
- **Allowed Domains**: `delhihighcourt.nic.in`, `dhc.nic.in`, `delhicourts.nic.in`
- **Neutral Citation Parsing**: `YYYY:DHC:NNNN` (e.g., `2024:DHC:0042`)
- **Rate Limit**: 15 requests per minute (0.25 QPS)
- **Error Handling**: Exponential backoff with jitter on 429/503 responses; immediate failure on 403/404.

---

## 4. High Court of Judicature at Bombay Connector (`BombayHighCourtConnector`)

- **Identifier**: `SRC-HC-BOM-PORTAL`
- **Target Portal**: `https://bombayhighcourt.nic.in`
- **Allowed Domains**: `bombayhighcourt.nic.in`, `bhc.gov.in`
- **Bench Support**:
  - `OS`: Original Side (Mumbai) -> `YYYY:BHC-OS:NNNN`
  - `AS`: Appellate Side (Mumbai) -> `YYYY:BHC-AS:NNNN`
  - `NAG`: Nagpur Bench -> `YYYY:BHC-NAG:NNNN`
  - `AUR`: Aurangabad Bench -> `YYYY:BHC-AUR:NNNN`
  - `GOA`: Panaji Bench (Goa) -> `YYYY:BHC-GOA:NNNN`
- **Rate Limit**: 12 requests per minute (0.20 QPS)

---

## 5. Verification & Test Evidence

High Court connector functionality is verified in [`tests/test_phase40_operational_infrastructure.py`](file:///c:/PROJECTS/LegalMitra/tests/test_phase40_operational_infrastructure.py):
- `test_delhi_high_court_connector_init`: Verifies domain restrictions and configuration defaults.
- `test_delhi_high_court_connector_ssrf_blocking`: Verifies blocking of `127.0.0.1`, `169.254.169.254`, and private IPs.
- `test_delhi_high_court_connector_allowed_url`: Verifies legitimate portal URLs are permitted.
- `test_delhi_high_court_discovery_dry_run`: Verifies discovery item construction and citation synthesis.
- `test_bombay_high_court_connector_multi_bench`: Verifies multi-bench routing across Mumbai, Nagpur, Aurangabad, and Goa.
- `test_rate_limiter`: Verifies token-bucket rate limiting math.
