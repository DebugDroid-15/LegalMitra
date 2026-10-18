# Phase 35 Acquisition Engine Security Audit & SSRF Defense

**Project:** LegalMitra  
**Phase:** 35 — National Legal Data Engine, Source Verification & Corpus Scaling Infrastructure  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** VERIFIED  

---

## 1. Threat Model & Acquisition Vulnerabilities

Outbound document acquisition engines face severe security risks when fetching legal materials from external endpoints:
1. **Server-Side Request Forgery (SSRF):** Attacker injects a URL resolving to internal cloud metadata (`169.254.169.254`), container control planes (`kubernetes.default`), or loopback services (`127.0.0.1:8000`).
2. **Open Redirect Exploits:** An allowed official hostname (e.g. `indiacode.nic.in/redirect?url=...`) issues an HTTP 302 redirecting to an internal or malicious host.
3. **Resource Exhaustion (Zip Bombs & Infinite Streams):** Endpoints streaming hundreds of gigabytes of infinite zeroes or uncompressed data, causing Out-Of-Memory (OOM) or disk exhaustion.
4. **Content-Type Confusion:** Endpoints serving executable binaries (`.exe`, `.sh`) masquerading as PDF or HTML legal instruments.
5. **Partial / Corrupted Writes:** Network dropped mid-download, leaving truncated text in production storage.

---

## 2. Hardened Architecture (`legalmitra/corpus/secure_acquisition_engine.py`)

The Phase 35 acquisition engine implements strict defensive controls:

### A. Pre-Request URL and IP Resolution Check
Before issuing any network socket, the URL is parsed and resolved:
- Rejects non-HTTP schemes (`gopher://`, `ftp://`, `file://` over network).
- Resolves DNS hostname via `socket.getaddrinfo` to all IPv4 addresses.
- Validates that resolved IPs are neither loopback (`127.0.0.0/8`), private RFC 1918 (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), link-local (`169.254.0.0/16`), multicast (`224.0.0.0/4`), nor reserved.

### B. Hop-by-Hop Redirect SSRF Filtering
Implements a custom `SafeRedirectHandler` inheriting from `urllib.request.HTTPRedirectHandler`:
- Maximum redirect hops capped at 5 (`MAX_REDIRECTS = 5`).
- For every redirect hop, computes the absolute URL target (`urljoin(req.full_url, newurl)`).
- **Validates the target URL and resolved destination IP before following the redirect**. If a redirect attempts to hop to `127.0.0.1` or `169.254.169.254`, the request is immediately aborted and classified as `REDIRECT_SSRF_BLOCKED`.

### C. Resource Capping & Safe Atomic Writes
- **Maximum Response Cap:** 50 MB (`MAX_RESPONSE_BYTES = 52,428,800`). If a stream exceeds 50 MB, the temporary socket is destroyed, the temporary file is unlinked, and error `SIZE_EXCEEDED` is returned.
- **Minimum Valid Length:** Under 40 bytes is treated as `EMPTY_OR_TRUNCATED` and automatically moved to `data/09_national_corpus/quarantine/`.
- **Atomic Renaming:** Downloads stream into an isolated temporary file (`lm_acq_*.tmp`). The SHA-256 digest is computed on the fly. Only after complete download, size check, and hash generation is the file atomically moved to its canonical filename (`{source_id}_{hash[:16]}.{ext}`).
- **Bounded Backoff:** Exponential backoff with jitter capped at 8.0s, maximum 3 retries.
- **Domain Rate Limiting:** Minimum 0.5s inter-request pause per domain.

---

## 3. Test Suite Verification

Audit results against `tests/test_phase35_validation.py::test_secure_acquisition_ssrf_and_ip_checks`:

| Test Vector | Target URL | Expected Disposition | Actual Result |
|---|---|---|---|
| Prohibited Scheme | `gopher://127.0.0.1/doc` | Rejected | `INVALID_SCHEME` (Passed) |
| Localhost Loopback | `http://127.0.0.1:8000/legal` | Blocked | `PRIVATE_IP_BLOCKED` (Passed) |
| Named Localhost | `http://localhost/admin` | Blocked | `SSRF_BLOCKED` (Passed) |
| AWS/GCP Metadata | `http://169.254.169.254/latest/meta-data` | Blocked | `SSRF_BLOCKED` (Passed) |
| Truncated Stream | 12 bytes received | Quarantined | `EMPTY_OR_TRUNCATED` (Passed) |

Zero SSRF bypasses or payload inflation vulnerabilities were detected.
