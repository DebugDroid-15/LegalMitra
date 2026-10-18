# Phase 29: Benchmark v7 Design & Expansion Specification
**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Owner:** Team Shatrujeet (Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo)  
**Classification:** Proprietary and Confidential  
**Date:** October 2026  
**Phase:** 29  

---

## 1. Evolution of the LegalMitra Benchmark Suite

| Benchmark Version | Total Cases | Key Additions / Focus | SHA256 Checksum |
|---|---|---|---|
| **v1 (Phase 22)** | 18 | Foundational Central Acts & Landmark Judgments | `068ba046...` |
| **v2 (Phase 23)** | 24 | Adversarial Robustness & Temporal Boundaries | `1947b196...` |
| **v3 (Phase 24)** | 32 | Evidence Gating & Procedural Timelines | `1a3d9061...` |
| **v4 (Phase 25)** | 40 | Citation Audit & Privacy Guardrails | `33b00609...` |
| **v5 (Phase 26)** | 56 | High Court Entities & Procedural Orders | `ea2f4701...` |
| **v6 (Phase 28)** | 68 | Claim-Level Grounding & Authentic Dates | `eecda8fa...` |
| **v7 (Phase 29)** | **80** | National Coverage, High Courts & State Legislation | `fdeb9ac32325061948810121b7accbddb8dae52bde43ac2a20644cc7ccec02dc` |

---

## 2. Benchmark v7 Structure & Composition

Benchmark v7 strictly preserves all 68 predecessor cases from Benchmark v6 without mutation and introduces **12 new verified evaluation cases**:

### Statutory Pinpoint Cases (4 New)
1. `EVAL-P29-STAT-001`: Delhi Rent Control Act 1958, Section 14 grounds for eviction.
2. `EVAL-P29-STAT-002`: Maharashtra Rent Control Act 1999, Section 15 90-day demand notice.
3. `EVAL-P29-STAT-003`: Maharashtra Police Act 1951, Section 56 externment powers.
4. `EVAL-P29-STAT-004`: Delhi Police Act 1978, Section 28 regulation of traffic and public order.

### Precedent Authority Cases (4 New)
5. `EVAL-P29-PREC-001`: Delhi High Court in *Christian Louboutin* (Section 79 safe harbor forfeiture for active marketplace).
6. `EVAL-P29-PREC-002`: Delhi High Court in *Tata Sons v. Greenpeace* (Article 19(1)(a) protection against trademark disparagement injunction).
7. `EVAL-P29-PREC-003`: Supreme Court in *Satyawati Sharma* (Striking down residential limitation in Section 14(1)(e) DRC Act under Article 14).
8. `EVAL-P29-PREC-004`: Supreme Court in *Arjun Panditrao Khotkar* (Overruling *Shafhi Mohammad*; mandatory Section 65B(4) certificate).

### Procedural Timeline Case (1 New)
9. `EVAL-P29-PROC-001`: Delhi High Court in CS (OS) 1407/2010 (*Tata Sons v. Greenpeace*) daily order dated 2010-08-04 refusing ad-interim injunction under Order XXXIX Rules 1 & 2 CPC.

### Missing Evidence / State Boundary Abstention Cases (3 New)
10. `EVAL-P29-MISS-001`: Karnataka Land Revenue Act 1964 Section 136 revision before Divisional Commissioner (Unindexed state transparent abstention).
11. `EVAL-P29-MISS-002`: West Bengal Premises Tenancy Act 1997 Section 7 standard rent (Unindexed state transparent abstention).
12. `EVAL-P29-MISS-003`: Tamil Nadu Buildings (Lease and Rent Control) Act 1960 Section 21 repossession (Unindexed state transparent abstention).

---

## 3. Cryptographic Immutability & Manifest

- Target file: `data/18_evaluation/evaluation_cases_v7.json`
- Manifest: `data/18_evaluation/manifest_v7.json`
- SHA-256 Hash: `fdeb9ac32325061948810121b7accbddb8dae52bde43ac2a20644cc7ccec02dc`
