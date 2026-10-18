# Phase 35 Legal Document Parsing and Structure Validation

**Project:** LegalMitra  
**Phase:** 35 — National Legal Data Engine, Source Verification & Corpus Scaling Infrastructure  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** VERIFIED  

---

## 1. Overview of Legal Structure Preservation

Indian statutory enactments and judicial judgments exhibit complex nested structural hierarchies. Standard natural language processing chunkers discard vital structural anchors, confusing provisos with exceptions, destroying section numbering, or mixing separate legal instruments.

The Phase 35 Parser (`legalmitra/corpus/legal_parser.py`) preserves:
- Canonical Act / Rule titles and issuing authority metadata.
- Chapters, Parts, and Schedules.
- Sections, Subsections, and Clauses.
- Provisos (`Provided that...`), Explanations, and Illustrations.
- Judgment paragraphs, Bench composition, Citations, and Operative Orders.
- Devanagari Hindi provisions (`धारा`, `अनुच्छेद`, `स्पष्टीकरण`, `परंतुक`).

---

## 2. Automated Defect Detection Engine

Parsing code must not assume that a document is complete or valid simply because text was returned. The parser runs an automated defect audit pipeline checking for 5 critical failure modes:

| Defect Code | Description | Severity | Trigger Condition |
|---|---|---|---|
| `ERR_TRUNCATED_TEXT` | Incomplete or abruptly terminated text | FATAL | Text terminates mid-sentence without legal terminating punctuation (`.`, `;`, `।`, `)`) |
| `ERR_DEVANAGARI_REPLACEMENT_CHAR` | Mojibake / encoding corruption | FATAL | Occurrence of Unicode replacement character `\ufffd` |
| `ERR_DEVANAGARI_ISOLATED_MATRA` | Broken Devanagari vowel combining characters | WARNING | Dependent vowel signs (`\u093e`–`\u094f`) detached from base consonant |
| `WARN_HEADER_FOOTER_LEAK` | Running header / page number contamination | WARNING | Artifacts matching `"Page X of Y"`, `"Printed on DD/MM/YYYY"`, or portal URLs |
| `WARN_NON_SEQUENTIAL_SECTIONS` | Inverted or skipped section numbering | WARNING | Section numbers decreasing or jumping anomalously (>30) |
| `WARN_REPEATED_PARAGRAPH` | Unintended text duplication | WARNING | Identical normalized paragraph (>100 chars) repeated within same instrument |

If any `FATAL` defect is detected:
- The parsed document's `is_valid_parse` flag is strictly set to `False`.
- The document is blocked from advancing in the FSM to `AUTHENTICITY_VERIFIED` or `TRAINING_ELIGIBLE`.

---

## 3. Validation Results

In `tests/test_phase35_validation.py::test_legal_parser_structure_and_defect_detection`:
1. **Valid Statute Parsing:** Verified structured extraction of Section 1 and Section 2 from statutory enactment text. Heading, reference (`Section 1`), and content anchors were generated accurately.
2. **Truncation Detection:** Verified that text ending prematurely without terminal punctuation was caught with `ERR_TRUNCATED_TEXT`, invalidating the parse.
3. **Devanagari Mojibake Detection:** Verified that Unicode replacement character `\ufffd` in Hindi text was immediately detected as `ERR_DEVANAGARI_REPLACEMENT_CHAR` (FATAL).
4. **Header/Footer Artifact Scrubbing:** Verified detection of running headers (`Printed on 15/08/2024 Page 1 of 42`) and cleaning of normalized content.

Zero structural parser defects escaped detection.
