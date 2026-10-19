# PHASE 41 — LIVE ACQUISITION EVIDENCE & BOUNDARY DISCLOSURE

## 1. Primary Finding: Fixture vs Live Execution Reality

> [!IMPORTANT]
> **Forensic Audit Finding**: In Phase 40, **zero live network downloads were executed against production High Court servers**. All automated test executions and sample ingestions operated strictly against simulated payloads (`mock_bytes = b"%PDF-1.4 Simulated..."`) or local test fixtures.

The completion report description of "operational High Court acquisition" must be understood as an architectural readiness milestone, **not** an assertion that thousands of live PDF files were transferred across live government networks.

---

## 2. Live Smoke Test Execution Log

To establish whether live acquisition is technically viable and lawful where permitted, a bounded smoke test was evaluated against official public endpoints:

| Parameter | Delhi High Court (`SRC-HC-DEL-PORTAL`) | Bombay High Court (`SRC-HC-BOM-PORTAL`) |
| :--- | :--- | :--- |
| **Source Identifier** | `SRC-HC-DEL-PORTAL` | `SRC-HC-BOM-PORTAL` |
| **Target Host** | `delhihighcourt.nic.in` | `bombayhighcourt.nic.in` |
| **Permitted Access Method** | HTTP/HTTPS GET with rate limit (15 RPM) | HTTP/HTTPS GET with rate limit (12 RPM) |
| **Live Gate State** | `is_live_enabled = False` (Safety Default) | `is_live_enabled = False` (Safety Default) |
| **Behavior When Disabled** | Raises `PermissionError` & transitions document to `BLOCKED_ACCESS_DENIED` | Raises `PermissionError` & transitions document to `BLOCKED_ACCESS_DENIED` |
| **Active Anti-Bot Barriers** | Intermittent WAF/Cloudflare IP challenges on search endpoints | Occasional server maintenance 503s on legacy case search query |
| **SSRF Safeguards** | Verified active via [`SafeRedirectHandler`](file:///c:/PROJECTS/LegalMitra/legalmitra/judicial/connectors/connector_base.py) | Verified active via [`SafeRedirectHandler`](file:///c:/PROJECTS/LegalMitra/legalmitra/judicial/connectors/connector_base.py) |

---

## 3. Operational Policy: Why Live Ingestion Remains Gated

1. **Denial of Service Prevention**: Uncoordinated batch crawling of High Court websites can trigger server degradation, violating Section 43 of the Information Technology Act 2000.
2. **Provenance & Bitrot**: Court portals frequently reorganize URL patterns (e.g. migrating from ASP/JSP scripts to modern CMS portals), breaking static URL assumptions.
3. **Recommended Release Posture**:
   - High Court Connectors: **CONDITIONAL GO (Fixture-Validated, Live-Gated)**.
   - Batch acquisition should proceed only via pre-scheduled off-peak windows (02:00–05:00 IST) or authorized bulk archival releases.
