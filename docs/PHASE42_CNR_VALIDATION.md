# LegalMitra Phase 42 — CNR Validation & Decomposition Audit

**Date:** October 19, 2026  
**Component:** `legalmitra/judicial/ecourts_protocol.py`  
**Standard:** eCourts CIS 16-Character National Case Number Record Specification  

---

## 1. Syntactic vs Semantic CNR Validation

Prior to Phase 42, CNR validation relied primarily on a 16-character alphanumeric regular expression:
```regex
^([A-Z]{2})([A-Z]{2})([A-Z0-9]{2})(\d{6})(\d{4})$
```
While this verified the structural format `[State:2][District:2][Establishment:2][CaseNo:6][Year:4]`, it allowed syntactically valid but semantically impossible strings (such as state code `ZZ`, establishment `99`, or filing year `1951` for CIS electronic databases established decades later).

Phase 42 formally decoupled validation into two explicit functions:

### 1. `validate_cnr_syntax(cnr_text: str) -> CNRDecomposition`
- Enforces exact 16-character alphanumeric length.
- Decomposes into state, district, establishment, case sequence number, and year.
- Validates reasonable outer calendar boundaries (1950–2030).

### 2. `validate_cnr_semantic(cnr_text: str) -> Dict[str, Any]`
- Evaluates the state code against the official 20-jurisdiction CIS state registry (`DL`, `MH`, `UP`, `KA`, `TN`, `WB`, `GJ`, `RJ`, `PB`, `HR`, `MP`, `BR`, `AP`, `TS`, `KL`, `OD`, `AS`, `JH`, `CH`, `UK`).
- Validates that the establishment code maps to recognized court complexes (e.g. `DLTH01` for Tis Hazari Courts, `MHPU01` for Pune District Court, `UPAL01` for Allahabad District Court).
- Enforces temporal computerization boundaries: computerized CIS electronic archives commence from 1980 onwards. CNR filing years prior to 1980 are flagged as outside computerized archive thresholds.

---

## 2. Test Verification Matrix

| Test Case | CNR Input | Syntactic Result | Semantic Result | Reason / Outcome |
|:---|:---|:---:|:---:|:---|
| Tis Hazari Commercial Suit | `DLTH010012342023` | PASS | PASS | Valid state (`DL`), establishment (`TH01`), year (`2023`) |
| Unrecognized State Prefix | `ZZTH010012342023` | PASS | FAIL | State code `ZZ` not recognized in CIS state registry |
| Pre-Computerization Filing | `DLTH010012341960` | PASS | FAIL | Filing year 1960 outside CIS electronic archive window (>=1980) |
| Truncated Character Count | `DLTH0100123420` | FAIL | FAIL | CNR length 14 != 16 characters |
| Lowercase / Trailing Spaces | ` dlth010012342023 ` | PASS | PASS | Automatically normalized to uppercase trimmed string |
