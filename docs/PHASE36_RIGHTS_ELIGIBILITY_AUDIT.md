# Phase 36 Rights & Training Eligibility Legal Audit

**Project:** LegalMitra  
**Phase:** 36 — Corpus Eligibility Audit, Hindi Primary-Source Acquisition & Dataset Integrity  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** VERIFIED  

---

## 1. Executive Summary

A critical directive of Phase 36 is to audit any blanket assumption that legal texts are automatically reusable for foundation model pretraining under interchangeable legal labels.

The audit examined three distinct legal regimes often conflated in automated legal pipelines:
1. **Section 52(1)(q) of the Indian Copyright Act, 1957** (Public Edict Statutory Exemption).
2. **Article 394A of the Constitution of India** (Authoritative Hindi Text of the Constitution).
3. **Government Open Data License (GODL-India)** (National Data Sharing & Accessibility Policy).

---

## 2. Comparative Legal Regime Analysis

| Legal Basis | Applicable Subject Matter | Pretraining Eligibility Scope | Critical Limitations |
|---|---|---|---|
| **Section 52(1)(q) Copyright Act, 1957** | Acts of Legislature, Official Gazette publications, Judicial judgments/orders | **PERMITTED** for bare legislative text and unedited court decisions | **Does NOT protect:** Commercial headnotes (SCC Online, Manupatra), editorial commentaries, proprietary compilations, or private translations (*Eastern Book Company v. D.B. Modak* (2008) 1 SCC 1). |
| **Article 394A of the Constitution** | The Constitution of India in the Hindi language | **PERMITTED** for constitutional Hindi text published under presidential authority | **Strictly confined to the Constitution.** Does not apply to Central Acts, State Acts, or court judgments. (Statutory Hindi translations are governed separately by Section 5(1) of the Official Languages Act, 1963). |
| **GODL-India License** | Datasets published on `data.gov.in` under NDSAP | **PERMITTED** only where explicitly published under GODL-India terms | **Cannot be inferred.** The mere fact that a PDF is hosted on a `.gov.in` or `.nic.in` domain does not mean it is released under GODL-India unless explicitly declared. |

---

## 3. Corpus Rights Classification Audit

All 1,559 eligible pretraining passages in `dataset_manifest_v4.json` were audited for rights compliance:

1. **Bare Statutory Enactments (Central & State Acts):** 100% verified as bare public edicts published in the Gazette of India or state gazettes without private editorial headnotes. Cleared under Section 52(1)(q)(i) and (ii).
2. **Judicial Decisions (Supreme Court & High Courts):** Bare certified judgment texts without commercial headnotes, syllabus, or publisher footnotes. Cleared under Section 52(1)(q)(iv).
3. **Constitutional Hindi Provisions:** Verified against the authoritative Hindi text published by the Legislative Department under Article 394A.
4. **Statutory Hindi Provisions:** Verified against the official bilingual Gazette publications under Section 5(1) of the Official Languages Act, 1963.
5. **Private User Conversations (`conversations.db`):** 100% excluded. User queries, messages, and feedback are private property under DPDP Act 2023 principles and strictly prohibited from pretraining manifests.
6. **Synthetic Test Fixtures (`IND-JUD-DEL-2024-BAIL`):** 100% quarantined. Synthetic text is not genuine law and is barred from pretraining.

---

## 4. Policy Determinations

- **Grounded RAG Eligibility vs Pretraining Eligibility:** These remain separate gates. A document may be indexed in the RAG knowledge base for reference search without automatically qualifying for pretraining manifests unless its reuse rights are affirmatively verified.
- **Conservative Default:** If a source possesses unresolved editorial commentary or unclear licensing, it must be marked `RIGHTS_UNRESOLVED` and excluded from export.
