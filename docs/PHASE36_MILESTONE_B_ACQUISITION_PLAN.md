# Phase 36 Milestone B Acquisition Plan & Defensible Growth Roadmap

**Project:** LegalMitra  
**Phase:** 36 — Corpus Eligibility Audit, Hindi Primary-Source Acquisition & Dataset Integrity  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** VERIFIED  

---

## 1. Executive Summary

Milestone B establishes a target of **1,000,000 eligible unique tokens** as a provisional research gate before intermediate model scaling.

Phase 36 audited the current eligible corpus baseline (**342,965 tokens**) and the 10 cataloged discovery candidates. Because automated live downloads from `indiacode.nic.in` (Akamai HTTP 403) and `legislative.gov.in` (CCA India root cert validation failure) were properly blocked by our security controls without bypass, **Milestone B has NOT been achieved in Phase 36**.

Under strict project governance, **we do not fabricate a 1M-token corpus**. Instead, Phase 36 provides an evidence-based, prioritized acquisition plan to legitimately achieve Milestone B in Phase 37.

---

## 2. Token Deficit to Milestone B

$$\text{Milestone B Target} = 1,000,000 \text{ tokens}$$
$$\text{Current Verified Eligible} = 342,965 \text{ tokens}$$
$$\mathbf{Net\ Deficit\ to\ Milestone\ B} = \mathbf{657,035\ tokens\ (2.91\times\ growth\ required)}$$

### Language Composition Goal for Milestone B:
- **Target English Tokens:** ~700,000 tokens (70%)
- **Target Devanagari Hindi Tokens:** ~300,000 tokens (30%)
- Rebalancing the current severe Hindi deficit (8,617 tokens $\rightarrow$ 300,000 tokens) is the primary criterion for pretraining readiness.

---

## 3. Prioritized Milestone B Acquisition Queue

| Priority Rank | Candidate Identifier | Legal Instrument / Jurisdiction | Language | Legal Domain | Estimated Token Yield | Acquisition Blocker & Solution Strategy |
|---|---|---|---|---|---|---|
| **1** | `CAND-HI-BNSS-2023` | भारतीय नागरिक सुरक्षा संहिता, 2023 (BNSS Hindi) | hi | Criminal Procedure | ~52,000 tokens | **Blocker:** Akamai 403 on India Code.<br>**Solution:** Download official Gazette of India Extra. No. 46 PDF with custom CCA India Root CA installed. |
| **2** | `CAND-HI-BNS-2023` | भारतीय न्याय संहिता, 2023 (BNS Hindi) | hi | Substantive Criminal | ~45,000 tokens | **Blocker:** Akamai 403 on India Code.<br>**Solution:** Download official Gazette of India Extra. No. 45 PDF via CCA trust chain. |
| **3** | `CAND-HI-BSA-2023` | भारतीय साक्ष्य अधिनियम, 2023 (BSA Hindi) | hi | Evidence Law | ~25,000 tokens | **Blocker:** Akamai 403 on India Code.<br>**Solution:** Download Gazette of India Extra. No. 47 PDF via CCA trust chain. |
| **4** | `CAND-PROC-DEL-HC-ORIG-2018` | Delhi High Court (Original Side) Rules, 2018 | en | Civil Procedure | ~22,000 tokens | **Solution:** Fetch via Delhi High Court rules portal (`delhihighcourt.nic.in`). |
| **5** | `CAND-STATE-WB-LAND-1955` | West Bengal Land Reforms Act, 1955 | en | Property / State Law | ~18,000 tokens | **Solution:** Official e-Gazette West Bengal archive. |
| **6** | `CAND-STATE-TN-TRANSP-1991` | Tamil Nadu Transparency in Tenders Act, 1998 | en | Administrative Law | ~11,000 tokens | **Solution:** Tamil Nadu Government Legislative portal. |
| **7** | `CAND-DEL-RULES-IT-2021` | Information Technology Intermediary Rules, 2021 | en | Digital Media / Cyber | ~12,000 tokens | **Solution:** MeitY public gazette notification archive. |
| **8** | `UNIV-ACT-BNSS-2023` (Full) | Complete English BNSS 2023 (531 Sections) | en | Criminal Procedure | ~240,000 tokens | **Solution:** Ingest remaining 350+ sections from Gazette No. 46 English text. |
| **9** | `UNIV-ACT-BNS-2023` (Full) | Complete English BNS 2023 (358 Sections) | en | Substantive Criminal | ~180,000 tokens | **Solution:** Ingest remaining 300+ sections from Gazette No. 45 English text. |
| **10** | `UNIV-ACT-BSA-2023` (Full) | Complete English BSA 2023 (170 Sections) | en | Evidence Law | ~90,000 tokens | **Solution:** Ingest remaining 150+ sections from Gazette No. 47 English text. |
| **Total Projected Yield** | — | — | — | — | **~695,000 tokens** | **Sufficient to cross 1,000,000 tokens.** |

---

## 4. Operational Requirements for Phase 37 Ingestion

To execute this acquisition plan in Phase 37 without violating security policies:
1. **Provision India PKI Root Certificates:** Bundle the official Controller of Certifying Authorities (CCA India) root certificate into the local acquisition engine's trust store to resolve SSL verification failures on `legislative.gov.in` and `egazette.gov.in`.
2. **Batch Ingestion Script:** Create `scripts/ingest_milestone_b_batch.py` to parse, validate Unicode integrity, check for danda characters, and log FSM state transitions from `DISCOVERED` to `TRAINING_ELIGIBLE`.
3. **Versioned Manifest `v5.0.0`:** After physical verification, write manifests to `v5` without altering historical `v4` digests.
