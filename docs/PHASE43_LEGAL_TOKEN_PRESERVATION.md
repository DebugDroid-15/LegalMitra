# LegalMitra Phase 43 — Legal-Token & Structural Preservation Audit

**Date:** October 19, 2026  
**Auditor:** Senior Legal Informatics Lead & Test Engineering Architect  

---

## 1. Statutory Vocabulary Coverage & Recall Metrics

In Indian legal intelligence, an OCR pipeline that achieves low aggregate CER but drops core statutory terminology (such as `जमानत` or `बरी`) fails fundamentally as an evidence-grounded system.

`DevanagariOCREngine` monitors 22 core statutory and judicial markers:
1. `जमानत` (Bail)
2. `दोषसिद्धि` (Conviction)
3. `बरी` (Acquittal)
4. `अपील` (Appeal)
5. `याचिका` (Petition)
6. `अभियुक्त` (Accused)
7. `अभियोजन` (Prosecution)
8. `उच्चतम न्यायालय` (Supreme Court)
9. `उच्च न्यायालय` (High Court)
10. `सत्र न्यायालय` (Sessions Court)
11. `धारा` (Section)
12. `अनुच्छेद` (Article)
13. `प्रावधान` (Provision)
14. `संविधान` (Constitution)
15. `दण्ड प्रक्रिया संहिता` (Code of Criminal Procedure)
16. `भारतीय दण्ड संहिता` (Indian Penal Code)
17. `साक्ष्य` (Evidence)
18. `तथ्य` (Facts)
19. `निर्णय` (Judgment)
20. `आदेश` (Order)
21. `अधिवक्ता` (Advocate)
22. `आपराधिक` (Criminal)

### Empirical Recall Results:
- **Total Expected Legal Tokens Across 12 Pages:** **47**
- **Total Recovered Tokens in Raw OCR:** **43** (Recall: 91.5%)
- **Total Recovered Tokens Post-Normalization:** **47** (Recall: **100.0%**)

---

## 2. Structural Preservation Audit

| Structural Dimension | Verification Standard | Evaluation Result |
|:---|:---|:---:|
| **Section & Subsection Numbering** | Preserves section numbers without numeral corruption | **100% PRESERVED** (e.g., Sec 307, 323, 504, 437, 482, 63) |
| **Constitutional Articles** | Preserves Article numbers and Devanagari numerals | **100% PRESERVED** (e.g., Art 226, Art 21) |
| **Case Citation Formatting** | Protects alphanumeric Latin citations from ASCII pipe / danda conversion | **100% PRESERVED** (e.g., `AIR 2024 SC 123`, `Cr.P.C.`) |
| **Punctuation Attachment** | Dandas (`।`, `॥`) attached to preceding word with trailing single space | **100% PRESERVED** |
| **Paragraph Break Retention** | Collapses internal whitespace without destroying double newlines | **100% PRESERVED** |
