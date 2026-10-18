# LegalMitra Phase 34: Data Rights, Legal Eligibility & Provenance Audit

**Status:** `VERIFIED`  
**Execution Date:** 2026-10-18  

---

## 1. Executive Summary

Phase 34 re-evaluated the legal eligibility of every source incorporated into the pretraining corpus. We explicitly reject the assumption that public internet accessibility constitutes an implied license to train machine learning models. Every acquired source in LegalMitra must be grounded in an explicit statutory exception or open-access mandate under Indian law.

---

## 2. Statutory Authority & Copyright Exceptions

All text incorporated into the Phase 34 expanded pretraining corpus is legally authorized under the **Indian Copyright Act, 1957 (Act No. 14 of 1957)**:

### 1. Reproduction of Legislative Acts (Section 52(1)(q)(i))
- Under Section 52(1)(q)(i), the reproduction or publication of any Act of a Legislature (accompanied by the original title) does NOT constitute copyright infringement.
- Applicable to: All Central Acts, State Acts, and Delegated Rules in the corpus.

### 2. Publication of Judicial Decrees & Orders (Section 52(1)(q)(iv))
- Under Section 52(1)(q)(iv), the publication of any judgment, decree, or order of a court, tribunal, or other judicial authority constitutes fair dealing and is exempt from copyright restrictions, provided the text is an accurate reproduction without proprietary annotations.
- Applicable to: Supreme Court and High Court judgments (Bombay HC, Calcutta HC, Madras HC, Delhi HC).

### 3. Authoritative Hindi Translations (Article 394A & Act 50 of 1973)
- Under Article 394A of the Constitution of India and the Authoritative Texts (Central Laws) Act, 1973, translations in Hindi published in the Official Gazette under the authority of the President of India constitute authoritative legal texts in the public domain.
- Applicable to: 52 curated Hindi statutory provisions across Constitution, BNS, BNSS, BSA, CPA, SRA, Arb, NI Act, and Limitation Act.

---

## 3. Strict Pretraining Exclusions Register

The following resources remain strictly excluded from model pretraining:
1. **User Conversations Database (`data/conversations.db`):** Contains private pair-programming and client interactions protected under Section 43A of the Information Technology Act, 2000 and the Digital Personal Data Protection Act, 2023.
2. **Pending Advocate Review Packages (`data/07_batches/review/`):** 40 candidate records remain in `pending_legal_review` status. Unverified candidates cannot be converted into training labels.
3. **Synthetic Scaffold (`IND-JUD-DEL-2024-BAIL`):** 6 artificial test chunks isolated in `data/legalmitra_kb.db` with `is_synthetic_scaffold = 1`.
4. **Evaluation Benchmark Manifests (v1 through v9):** Held-out QA test cases; inclusion in pretraining would cause catastrophic benchmark contamination.
5. **Commercial Publisher Annotations:** Proprietary headnotes, editorial catchwords, and case summaries from commercial legal databases (SCC, AIR, Manupatra) are strictly prohibited.

