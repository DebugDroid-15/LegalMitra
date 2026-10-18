# LegalMitra Phase 34: Ranked Legal Acquisition Priority Queue

**Status:** `VERIFIED`  
**Execution Date:** 2026-10-18  

---

## 1. Executive Summary

To reach pretraining volume milestones systematically rather than accumulating low-value text, Phase 34 established an objective, ranked acquisition priority queue. Sources are scored across five criteria:
1. **Legal Importance & Precedential Authority** (Weight: 25%)
2. **Corpus Coverage Gap Closure** (Weight: 25%)
3. **Multilingual (Hindi) Token Yield** (Weight: 20%)
4. **Source Reliability & Official Authenticity** (Weight: 15%)
5. **Clear Legal Reuse Rights under Section 52(1)(q)** (Weight: 15%)

---

## 2. Ranked Acquisition Priority Queue

| Rank | Candidate Source Entity | Authority Level | Target Language | Estimated Token Yield | Rights Clearance | Priority Score (0–100) |
|---|---|---|---|---|---|---|
| **1** | Full Official Gazette Edition of BNS 2023 | Central Statute | Hindi | ~45,000 | Section 52(1)(q)(i) | **96.5** |
| **2** | Full Official Gazette Edition of BNSS 2023 | Central Statute | Hindi | ~65,000 | Section 52(1)(q)(i) | **95.0** |
| **3** | Full Official Gazette Edition of BSA 2023 | Central Statute | Hindi | ~28,000 | Section 52(1)(q)(i) | **94.0** |
| **4** | Allahabad High Court Full Bench Landmark Rulings | High Court | English | ~50,000 | Section 52(1)(q)(iv)| **91.5** |
| **5** | Insolvency and Bankruptcy Code, 2016 (IBC) | Central Statute | English + Hindi | ~40,000 | Section 52(1)(q)(i) | **89.0** |
| **6** | Supreme Court Constitution Bench Judgments (2020–2024)| Supreme Court | English | ~120,000| Section 52(1)(q)(iv)| **88.5** |
| **7** | Income Tax Act, 1961 (Core Assessment & Penalty Clauses)| Central Statute | English + Hindi | ~85,000 | Section 52(1)(q)(i) | **86.0** |
| **8** | Gujarat High Court Landmark Commercial Decisions | High Court | English | ~35,000 | Section 52(1)(q)(iv)| **82.5** |
| **9** | NCLAT Precedents on Corporate Insolvency Resolution | Appellate Tribunal| English | ~40,000 | Section 52(1)(q)(iv)| **80.0** |
| **10**| Delhi Land Reforms Act & Urban Tenancy Notifications | State/UT Statute | English + Hindi | ~25,000 | Section 52(1)(q)(i) | **78.5** |

---

## 3. Acquisition Pipeline Enforcement Rules

1. **Prioritize Authenticity over Raw Volume:** Never scrape third-party blogs or summary articles. Only ingest official publications from India Code (`indiacode.nic.in`), the Official Gazette (`egazette.gov.in`), or the Supreme Court / High Court repositories (`sci.gov.in`, `ecourts.gov.in`).
2. **Mandatory SSRF Pre-flight Check:** Every prospective URL must pass `validate_outbound_legal_url()` before retrieval.
3. **Zero-Byte & Timeout Quarantine:** Outbound requests exceeding 30s timeout or returning 0 bytes must be quarantined immediately in the acquisition register.

