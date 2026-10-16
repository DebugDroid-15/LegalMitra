# LegalMitra — Extraction & Diagnostic Failure Report
**Phase 3 Comprehensive Audit**
**Date**: October 2026 | **Pipeline Version**: 0.3.0

---

## 1. Executive Summary

The LegalMitra extraction subsystem parses heterogeneous Indian legal source formats (Gazette PDFs, Supreme Court judgment transcripts, High Court orders, legislative markdown) into high-fidelity structured text. 

This report provides an exhaustive technical analysis of:
1. Supported extraction engines and performance benchmarks.
2. Observed extraction failures, edge cases, and unsupported document types.
3. Docling page limit and multi-column parsing dynamics.
4. Prescribed engineering remediations for production ingestion.

---

## 2. Ingestion & Extraction Engine Architecture

| Engine | Target Formats | Implementation File | Key Strengths | Known Limitations |
| :--- | :--- | :--- | :--- | :--- |
| **Docling Document Converter** | `.pdf` (Central Gazettes, High Court judgments) | `legalmitra/ingestion/docling_extractor.py` | State-of-the-art layout analysis; table preservation; OCR fallback; markdown emission. | Memory footprint; CPU latency (~15-30s on long documents); strict `max_num_pages` guardrails. |
| **Plain Text / UTF-8 Extractor** | `.txt`, `.md` (Raw statutory sections) | `legalmitra/ingestion/extractors.py` | Zero overhead; deterministic section extraction; 100% character fidelity. | Requires pre-stripped text; lacks visual layout comprehension. |
| **HTML / Gazette Web Extractor** | `.html`, `.htm` (Legislative portals) | `legalmitra/ingestion/docling_extractor.py` | Traverses DOM; removes headers/scripts; isolates statutory text blocks. | Inconsistent portal DOMs; dynamic JavaScript tables require headless rendering. |

---

## 3. Extraction Successes & Production Corpus Benchmarks

| Document ID | Source Type | Raw Format | Raw Size | Extracted Character Count | Structured Sections / Paragraphs | Extraction Time | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `IND-STAT-DPDP-2023` | Statute (Full Act) | PDF | 446 KB | 69,281 chars | 91 sections & definitions | 24.1s | **SUCCESS** |
| `IND-STAT-IT-2000` | Statute (Full Act) | PDF | 838 KB | 144,958 chars | 316 sections & schedules | 41.5s | **SUCCESS** |
| `IND-STAT-BSA-2023-SEC61` | Statute (Section) | TXT/MD | 823 B | 823 chars | Section 61 (Admissibility) | 0.01s | **SUCCESS** |
| `IND-STAT-BSA-2023-SEC63` | Statute (Section) | TXT/MD | 1,412 B | 1,412 chars | Section 63 (Certificate) | 0.01s | **SUCCESS** |
| `IND-STAT-POCSO-2012-SEC4` | Statute (Section) | TXT/MD | 1,189 B | 1,189 chars | Section 4 (Penetrative Assault) | 0.01s | **SUCCESS** |
| `IND-JUD-DEL-2024-BAIL` | Judgment (High Court) | PDF | 185 KB | 3,842 chars | 12 judicial paragraphs | 3.2s | **SUCCESS** |
| `IND-JUD-SC-2017-PUTTASWAMY` | Judgment (Constitution Bench) | MD/PDF | 4,210 B | 4,210 chars | 14 material paragraphs | 0.02s | **SUCCESS** |

---

## 4. Extraction Failures and Unsupported Edge Cases

```
Total Processed in Pipeline Tests: 9
Successful Extractions: 7
Registered Pending Large-Scale: 1 (SCI Handbook, 8.4MB)
Intentional Negative Test Cases: 1 (IND-UNSUPPORTED-001.xyz)
```

### Detailed Failure Diagnostics

#### Case 1: IND-UNSUPPORTED-001 (Negative Test Validation)
- **File**: `data/01_raw/IND-UNSUPPORTED-001.xyz`
- **Failure Code**: `UNSUPPORTED_FORMAT`
- **Diagnostic Log**:
  ```
  legalmitra.core.errors.ExtractionError: No extractor registered for file extension: '.xyz'
  ```
- **Remediation**: The dispatcher strictly verifies MIME types and file extensions. Ingestion must reject unsupported binary blobs before registry allocation.

#### Case 2: Docling Strict Page Range Violation (`max_num_pages`)
- **Observed Behaviour**: When extracting large omnibus gazettes (e.g., BNSS 2023 at 300+ pages), configuring Docling with `max_num_pages=10` raises `docling.exceptions.ConversionError: Number of pages (348) exceeds maximum allowed (10)`.
- **Diagnostic**: Docling treats `max_num_pages` as an upper-bound check rather than a slicing window.
- **Remediation**: For targeted chapter/section extraction from voluminous acts:
  1. Slice the target page range using `pypdf` prior to passing to Docling.
  2. Or configure Docling's page range options directly.

#### Case 3: Watermarked High Court PDFs & Scanned Judicial Orders
- **Observed Behaviour**: Certain High Court orders (e.g. Allahabad, Bombay) publish scanned raster images with diagonal "CONFIDENTIAL" or "TRUE COPY" stamps.
- **Diagnostic**: Pure programmatic text extractors (pdfminer) return garbage tokens; OCR engines misread watermarks as statutory headers.
- **Remediation**: Use Docling's layout pipeline with table-former and OCR backend (EasyOCR/Tesseract) enabled.

---

## 5. Verification Commands

To reproduce extraction verification and failure tracking:
```powershell
# Run extraction test suite
pytest tests/test_extraction.py -v

# Validate all registered sources
python run_pipeline.py validate-sources
```
