# LEGALMITRA: RAG RELIABILITY & FAILURE MODES ANALYSIS

**Date:** 2026-10-16  
**Document Classification:** Legal Intelligence Reliability & Boundary Enforcement  
**Reference Document:** `PHASE8_OPEN_LEGAL_ISSUES_REGISTER.md`  

---

## 1. Grounding Principles & Failure Mode Taxonomy

The LegalMitra RAG engine is architected around strict evidential containment. An answer is only generated if supporting statutory sections or binding judicial paragraphs are retrieved from `data/legalmitra_kb.db`.

Below is the verified behavioral matrix across all 10 critical legal failure modes:

| Failure Mode | Inbound Scenario | System Response & Safeguard | Status |
|:---|:---|:---|:---|
| **1. No Evidence Retrieved** | Query on non-existent or unindexed domain (e.g. extraterrestrial mineral rights). | `LegalRAGEngine` detects 0 chunks, abstains from generative speculation, returns explicit insufficient evidence notice, and prompts for missing facts. | **Verified** |
| **2. Irrelevant Evidence Retrieved** | High-level search terms match distant statute text without addressing the legal query. | Prompt specifies that if retrieved sources do not address the query directly, the model must explicitly state insufficiency. | **Verified** |
| **3. Unsupported Claims** | LLM attempts to extrapolate beyond verbatim provisions. | Quality gates and groundness validator flag invented statutory sections or uncommenced claims. | **Verified** |
| **4. Phantom Citations** | Model references an Act or Case not in the retrieved evidence list. | `_extract_citations()` only parses citations that match retrieved `SearchResult` records. | **Verified** |
| **5. Temporal Uncertainty** | Question concerns transition between IPC/CrPC and BNS/BNSS (commenced 1 July 2024). | `_detect_missing_facts()` inspects query for criminal terms and returns an advisory prompt stating that applicability depends on whether the offence occurred before or after 1 July 2024. | **Verified** |
| **6. Statutory Conflict / Phased Repeal** | DPDP Act 2023 Sec 44 vs IT Act Sec 43A. | Knowledge base chunks explicitly index commencement notifications (S.O. 848(E) for BNSS; S.O. 3727(E) / G.S.R. 518(E) for DPDP). | **Verified** |
| **7. Endpoint Timeout / Failure** | LLM provider endpoint is unreachable or times out. | Handled via try-except block, logged with sanitized category, returns safe HTTP 500 without leaking stack trace or API tokens. | **Verified** |
| **8. Quarantined Content Exposure** | Attempt to query or cite synthetic scaffold `IND-JUD-DEL-2024-BAIL`. | Excluded at database query time (`WHERE is_synthetic_scaffold = 0`). Quality gate rejects any output referencing quarantined records. | **Verified** |
| **9. Definitive Conclusion Request** | User asks "Will my FIR definitely be quashed?" | Disclaimer footer and system prompt enforce that assistant provides statutory analysis, not judicial outcome guarantees or formal legal advice. | **Verified** |
| **10. Missing Procedural Facts** | User asks for High Court quashing or limitation procedure without naming state. | `_detect_missing_facts()` flags missing High Court jurisdiction due to inter-state procedural variation. | **Verified** |

---

## 2. Unresolved Legal Issues Register Continuity

In accordance with non-negotiable project constraints, the six open legal issues documented in `PHASE8_OPEN_LEGAL_ISSUES_REGISTER.md` remain strictly unresolved pending formal advocate review:
1. **BNSS Section 482(4)**: Compounding limitation for private complaints.
2. **IT Act Section 43A vs. DPDP Section 44**: Phased commencement and repeal timing.
3. **DPDP Section 6(9)**: Notice requirements for legacy processing activities.
4. **BNSS Section 531 Savings vs. CrPC**: Pending inquiry and trial continuity under S.O. 848(E).
5. **BSA Section 63 Certificate Requirement**: Certificate necessity vs. primary electronic records.
6. **Extrapolation Beyond Cited Statutory Text**: Restraint against generalizing beyond enacted clauses.

