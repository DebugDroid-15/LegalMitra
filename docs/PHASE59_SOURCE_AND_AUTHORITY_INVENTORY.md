# Phase 59 Source and Authority Inventory

**Project:** LegalMitra  
**Phase Identifier:** LEGALMITRA-PHASE59  
**Inventory Scope:** Primary Indian Legislation, Delegated Rules, Judicial Precedents, and Knowledge Base Chunks  
**Database Path:** `data/legalmitra_kb.db`  
**Inventory Timestamp:** October 2026  

---

## 1. Database Table Breakdown

| Table Name | Record Count | Description / Role | Invariant Status |
| :--- | :--- | :--- | :--- |
| `sources` | 62 | Ingested statutory acts, amendment notifications, and case files. | Authentic primary sources |
| `legal_chunks` | 1,515 | Primary granular text chunks with statutory citations and provision references. | 1,509 active, 6 quarantined |
| `legal_chunks_fts` | 1,505 | Full-text search index (FTS5) for rapid semantic keyword matching. | In-sync with active chunks |
| `cases` | 16 | Registered high-court and supreme-court judicial proceeding records. | Authentic judicial cases |
| `judicial_documents` | 9 | Registered judgments, interim orders, and stay orders. | Authentic court orders |
| `hearing_events` | 8 | Chronological hearing dates, bench strengths, and referral milestones. | Verified hearing records |

---

## 2. Chunk Invariant & Quarantine Accounting

- **Total Chunks in `legal_chunks`:** **1,515**
- **Active Authentic Chunks:** **1,509**
- **Quarantined Synthetic Scaffold Chunks:** **6** (`source_id = 'IND-JUD-DEL-2024-BAIL'`, `is_synthetic_scaffold = 1`)
- **Distinct Acts / Cases in Corpus:** **60** unique legislative enactments and landmark case titles.

---

## 3. Registered Primary Central Enactments (Sample)

| Central Act | Year | Act No. | Key Provisions Ingested | Temporal Invariants |
| :--- | :--- | :--- | :--- | :--- |
| **Arbitration and Conciliation Act** | 1996 | 26 | Sec 2(1)(e), 8, 9, 11, 12(5), 16, 29A, 34, 37 | 2015 & 2019 Amendments tracked |
| **Specific Relief Act** | 1963 | 47 | Sec 10, 14, 14A, 16(c), 20, 20A, 20B, 20C, 41(ha) | 2018 Infrastructure bar tracked |
| **Hindu Succession Act** | 1956 | 30 | Sec 6, 6(1) proviso, 8, 14, 15, 23 | 2005 Coparcenary amendment tracked |
| **Commercial Courts Act** | 2015 | 4 of 2016 | Sec 2(1)(c), 12A, 19 | Mandatory pre-institution mediation |
| **Negotiable Instruments Act** | 1881 | 26 | Sec 138, 139, 141, 142, 143A, 148 | 2018 Interim deposit tracked |
| **Industrial Disputes Act** | 1947 | 14 | Sec 2(oo), 25F, 25FFA, 25FFF, 25N, 25O | Active vs uncommenced IR Code |
| **Insolvency and Bankruptcy Code** | 2016 | 31 | Sec 5(8), 7, 9, 14, 29A, 31(1), 32A, 238 | Clean slate & promoter liability |
| **Digital Personal Data Protection Act** | 2023 | 22 | Sec 1(2), 2, 4, 8, 18, 19 | Phased notification status tracked |
| **Bharatiya Nyaya Sanhita (BNS)** | 2023 | 45 | Commenced 01-07-2024 | IPC replacement with historical savings |
| **Bharatiya Nagarik Suraksha Sanhita (BNSS)**| 2023 | 46 | Commenced 01-07-2024 | CrPC replacement; Sec 531 savings |
| **Bharatiya Sakshya Adhiniyam (BSA)** | 2023 | 47 | Commenced 01-07-2024 | Evidence Act replacement |

---

## 4. Judicial Precedent Knowledge Graph Inventory

- **Total Graph Nodes:** **99** nodes (covering Constitutional articles, statutory sections, landmark Supreme Court judgments, High Court split decisions, stay orders, and referral orders).
- **Total Graph Edges:** **62** semantic authority edges spanning `OVERRULES`, `REVERSES`, `DISTINGUISHES`, `STAYED`, `REFERS_TO_LARGER_BENCH`, `CONFLICTS_WITH`, `INTERPRETS`, `APPLIES`.

---

## 5. Temporal Engine Registered Entities

- **Statutes Registered:** **28** full lifecycle statutes in `TemporalLawEngine._statutes`.
- **Temporal Provision Versions Registered:** **26** multi-version provisions in `TemporalLawEngine._versions`.
- **Statutory Applicability States Supported:** 7 canonical states:
  1. `IN_FORCE`
  2. `NOT_YET_IN_FORCE` (uncommenced enactment)
  3. `SUPERSEDED_OR_REPEALED`
  4. `CONFIRMED_HISTORICAL` (prior version saved under repeal/savings)
  5. `CONFLICTING_TEMPORAL_EVIDENCE` (overlapping gazettes)
  6. `RETROSPECTIVE_EFFECTIVE`
  7. `INSUFFICIENT_TEMPORAL_DATA`
