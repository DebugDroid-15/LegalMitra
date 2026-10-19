# LegalMitra Phase 42 — Controlled High Court Connector Pilot

**Date:** October 19, 2026  
**Execution Script:** `scripts/run_controlled_high_court_pilot.py`  
**Target Connectors:** `DelhiHighCourtConnector` (`IND-HC-DEL`), `BombayHighCourtConnector` (`IND-HC-BOM`)  
**Execution Mode:** `CONTROLLED_FIXTURE_DRY_RUN`  

---

## 1. Pilot Mission & Operational Context

Phase 40 introduced High Court connector classes with SSRF defenses and rate-limiting token buckets. Phase 42 executes a bounded pilot to determine operational readiness under real-world infrastructure constraints.

### Preflight Verification Results:
- **SSRF Protection:** PASSED. Verified rejection of loopback (`127.0.0.1`), link-local (`169.254.169.254`), non-standard ports (`:8080`, `:22`), embedded credentials, and IPv6 loopback (`::1`).
- **Domain Whitelist:** PASSED. Verified strict allowlists: `delhihighcourt.nic.in` for Delhi and `bombayhighcourt.nic.in` for Bombay.
- **Thread-Safe Rate Limiter:** PASSED. Validated concurrency locks guaranteeing a maximum request frequency of 1.0 request/sec (60 req/min).

---

## 2. Operational Blocker: `LIVE_PERMISSION_UNVERIFIED`

While the connectors and networking pipelines are technically fully functional, live unauthenticated crawling against High Court servers poses severe operational and legal risks:
1. **Robots.txt & WAF Protection:** NIC / High Court gateways enforce Web Application Firewalls (WAF) that return HTTP 403 Forbidden and block IP ranges upon detecting automated scraping headers.
2. **Permission Safeguards:** Official terms of use require institutional identification for automated harvesting of judicial orders.

**Phase 42 Execution Decision:**  
In strict compliance with LegalMitra security policies, the connectors operated in **`CONTROLLED_FIXTURE_DRY_RUN`** mode:
- 3 candidate documents discovered and validated for Delhi High Court (`YYYY:DHC:NNNN` format).
- 3 candidate documents discovered and validated for Bombay High Court Appellate Side (`YYYY:BHC-AS:NNNN` format).
- All 6 discovered documents transitioned through the 9-stage lifecycle: `DISCOVERED` -> `ACQUIRED` -> `PARSED` -> `AUTHENTICITY_CHECKED` -> `RIGHTS_REVIEWED`.
- Active Blocker Logged: `LIVE_PERMISSION_UNVERIFIED`.
