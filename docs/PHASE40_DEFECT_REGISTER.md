# PHASE 40 — DEFECT REGISTER & REMEDIATION LOG

## 1. Overview

This defect register tracks all issues, regressions, anomalies, and architectural deficiencies identified during the implementation, testing, and audit of Phase 40.

---

## 2. Identified Defects & Remediation Status

| Defect ID | Severity | Component | Summary | Remediation / Status |
| :--- | :---: | :--- | :--- | :--- |
| **DEF-40-001** | High | `devanagari_ocr` | Danda spacing formatting attached irregular whitespace before danda (`की ।`), causing character mismatch against standard Hindi typography. | **Resolved**: Updated regex in [`DevanagariOCREngine`](file:///c:/PROJECTS/LegalMitra/legalmitra/judicial/devanagari_ocr.py) to strip whitespace before dandas (`की।`) and enforce standard single space following danda when adjacent to words. |
| **DEF-40-002** | High | `ecourts_protocol` | Subordinate court records requiring redaction were transitioning to `ELIGIBLE_INDEXED` rather than being quarantined. | **Resolved**: Enforced privacy gate in [`ECourtsProtocolValidator`](file:///c:/PROJECTS/LegalMitra/legalmitra/judicial/ecourts_protocol.py) so any record with `requires_redaction=True` transitions to `BLOCKED_RESTRICTED` until certified human redaction is completed. |
| **DEF-40-003** | Medium | `connectors` | Method signature mismatch between base connector and test assertions (`validate_url_security` vs `validate_url_safety`). | **Resolved**: Standardized method name to `validate_url_security` across tests and base classes. |
| **DEF-40-004** | Medium | `conflict_triage` | Parameter name mismatch in conflict resolution method (`rationale` vs `decision_rationale`). | **Resolved**: Aligned test invocation to `rationale` parameter and enforced minimum 15-character rationale length. |
| **DEF-40-005** | Low | `devanagari_ocr` | OCR byte decoding error (`\ufffd`) in Delhi High Court fixture caused silent pipeline pass without operator notification. | **Resolved**: Added anomaly detection for `\ufffd` in `DevanagariOCREngine` which sets `has_replacement_characters=True` and `requires_human_review=True`. |

---

## 3. Residual Known Issues & Technical Debt

1. **eCourts Public CAPTCHA**: Ingestion of live district court records cannot be automated via public web portals without violating CAPTCHA terms. Mitigated via staged local dumps and eCommittee API tokens.
2. **Archival OCR Microfilms**: Pre-1970 decisions from state archives have significant speckling and ink bleed; full integration is deferred to dedicated historical scanning phases.
