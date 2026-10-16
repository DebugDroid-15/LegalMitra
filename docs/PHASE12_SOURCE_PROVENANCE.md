# LEGALMITRA PHASE 12: SOURCE PROVENANCE AND QUALITY GATES

**Date:** 2026-10-16  
**Document Classification:** Source Verification & Legal Provenance Standards  

---

## 1. Authoritative Source Standards

LegalMitra requires every legal claim to be traceable to an authentic primary legal source:

1. **Central Acts & Statutes**: Sourced directly from **India Code** (`indiacode.gov.in`) or legislative text published by the Ministry of Law and Justice.
2. **Commencement Notifications**: Official Gazette of India notifications (e.g. S.O. 848(E) for BNSS; S.O. 3727(E) & G.S.R. 843(E) for DPDP).
3. **Supreme Court Judgments**: Official Supreme Court digital repository (`sci.gov.in`) or authoritative law reports (SCC).
4. **High Court Orders**: Official High Court portal records.

---

## 2. Source Registry Provenance Inventory

The repository registry at `registry/source_registry.jsonl` contains the following authentic sources:

| Source ID | Document Title | Source Authority & URL | Commencement Notification | Verified Status |
|:---|:---|:---|:---|:---|
| `IND-STAT-BNSS-2023` | Bharatiya Nagarik Suraksha Sanhita, 2023 | India Code (Act 46 of 2023) | S.O. 848(E) (w.e.f. 2024-07-01) | **Authentic** |
| `IND-STAT-DPDP-2023` | Digital Personal Data Protection Act, 2023 | India Code (Act 22 of 2023) | S.O. 3727(E) & G.S.R. 843(E) | **Authentic** |
| `IND-STAT-BSA-2023-SEC61` | Bharatiya Sakshya Adhiniyam, 2023 - Sec 61 | India Code (Act 47 of 2023) | S.O. 849(E) (w.e.f. 2024-07-01) | **Authentic** |
| `IND-STAT-BSA-2023-SEC63` | Bharatiya Sakshya Adhiniyam, 2023 - Sec 63 | India Code (Act 47 of 2023) | S.O. 849(E) (w.e.f. 2024-07-01) | **Authentic** |
| `IND-STAT-POCSO-2012-SEC4` | POCSO Act, 2012 - Section 4 | India Code (Act 32 of 2012) | S.O. 2642(E) (w.e.f. 2012-11-14) | **Authentic** |
| `IND-STAT-IT-2000` | Information Technology Act, 2000 | India Code (Act 21 of 2000) | G.S.R. 788(E) (w.e.f. 2000-10-17) | **Authentic** |
| `IND-JUD-SC-2017-PUTTASWAMY` | K.S. Puttaswamy v. Union of India (Privacy) | Supreme Court of India ((2017) 10 SCC 1) | Decided 2017-08-24 | **Authentic** |
| `IND-JUD-DEL-2024-BAIL` | Synthetic Bail Test Scaffold | Unverified Test Scaffold | N/A | **QUARANTINED** |

---

## 3. Seven Provenance Enforcement Gates

Every candidate example generated or considered for review must satisfy:

1. **Registered Source Requirement**: All `supporting_source_ids` must exist in `registry/source_registry.jsonl`.
2. **Quarantine Exclusion**: If `IND-JUD-DEL-2024-BAIL` or any flagged synthetic scaffold is present, the candidate is immediately rejected.
3. **Exact Evidence-Span Matching**: Every `EvidencePassage.verbatim_text` must be an exact substring of the normalized source text.
4. **Commencement Check**: `commencement_date` and `commencement_source_id` must match Gazette notifications.
5. **Temporal Label Consistency**: If `legal_as_of_date < commencement_date`, the status MUST be `enacted_not_yet_in_force` or `uncommenced`.
6. **Statute-Provision Non-Conflation**: A replacement statute provision (e.g. BNSS 531) cannot inherit the `repealed` status of the prior act (CrPC 1973).
7. **No Unreviewed Promotion**: Automated passing only sets `pending_legal_review`. Human approval is required for `legal_expert_approved`.

