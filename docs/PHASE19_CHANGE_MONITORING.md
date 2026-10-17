# PHASE 19 — CONTINUOUS LEGAL SOURCE MONITORING & RECONCILIATION

**Workspace:** `C:\PROJECTS\LegalMitra`  
**Classification:** Proprietary & Confidential — Team Shatrujeet  
**Date:** October 2026  
**Status:** Canonical Reference

---

## 1. Executive Summary

A continuous legal update service must balance **corpus freshness** with **strict respect for public institutional infrastructure**. Aggressive or unauthenticated polling of government portals risks IP blacklisting, CAPTCHA triggering, or denial of service to genuine citizens.

LegalMitra's **Continuous Source Monitor (`legalmitra/corpus/source_monitor.py`)** provides a controlled, rate-limited polling architecture executed via manual operator command (`scripts/check_legal_source_updates.py`).

---

## 2. Monitored Official Repositories

| Portal Code | Name & Authority | Monitoring Target | Rate Limit | Permitted Interval |
| :--- | :--- | :--- | :--- | :--- |
| `MON-INDIA-CODE` | India Code (Legislative Dept, MoL&J) | Newly gazetted Central Acts & Amendments | $\le 20$ req/min | 24 Hours |
| `MON-EGAZETTE` | e-Gazette of India (DoP) | Extraordinary Gazette S.O. & G.S.R. notices | $\le 10$ req/min | 12 Hours |
| `MON-SCI-DIGISCR` | Digital SCR (Supreme Court of India) | Reportable judgments & neutral citations | $\le 20$ req/min | 12 Hours |
| `MON-HIGH-COURTS` | High Court Portals (Delhi, Bombay, etc.) | Reported appellate judgments & court rules | $\le 15$ req/min | 24 Hours |

---

## 3. Rate-Limiting & Exponential Backoff Controls

1. **Strict Operator Control**: Background daemon loops that ping external web servers indefinitely without supervision are prohibited.
2. **Backoff Mechanism**:
   - If an official endpoint returns HTTP 429 (Too Many Requests) or HTTP 503 (Service Unavailable), the monitor automatically doubles the wait interval ($2 \times \text{previous backoff}$).
   - After 3 consecutive errors, the source is transitioned to `MonitoringStatus.RATE_LIMITED` and queued for manual administrator review.
3. **State Persistence**: Monitoring metrics and last-known SHA-256 hashes are persisted to `data/09_national_corpus/source_monitoring_state.json`.

---

## 4. Triage Workflow for Detected Changes

When a content hash shift is confirmed:
1. `NEW_DOCUMENT` $\to$ Discovered candidate created and prioritized in `AcquisitionQueue`.
2. `CHANGED_SOURCE_FILE` $\to$ Evaluated via `LegalDiffEngine` to check for substantive statutory amendment vs. minor corrigendum.
3. `SUBSTANTIVE_LEGAL_CHANGE` $\to$ Ingested via `NationalCorpusPipeline` and routed to the Advocate Review Queue.

