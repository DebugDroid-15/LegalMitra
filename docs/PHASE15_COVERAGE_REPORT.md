# LegalMitra Phase 15 — National Legal Corpus Coverage Report

**Generated Date:** 2026-10-17  
**Coverage Audit Script:** `scripts/corpus_coverage_report.py`  
**Inventory Files:** `data/08_corpus/coverage_inventory.json` & `coverage_inventory.csv`  
**Summary Metrics:** `data/08_corpus/coverage_summary.json`  
**Target Repository:** `c:\PROJECTS\LegalMitra`

---

## 1. Overall Corpus Metrics & Denominators

| Metric | Phase 14 Baseline | Phase 15 Batch 1 | Net Change |
| :--- | :---: | :---: | :---: |
| **Total Identified Universe (Denominator)** | 37 sources | 37 sources | 0 (Stable baseline) |
| **Indexed Primary Sources in KB** | 8 sources | **16 sources** | **+8 sources (+100%)** |
| **Total Chunks in Knowledge Base** | 1,149 chunks | **1,227 chunks** | **+78 chunks (+6.8%)** |
| **Fully Extracted & Validated Sources** | 8 (21.6%) | **16 (43.2%)** | **+8 sources (+21.6%)** |
| **Pending Ingestion Pipeline** | 27 (73.0%) | **19 (51.4%)** | **-8 sources (-21.6%)** |
| **Inaccessible / Backlog** | 2 (5.4%) | 2 (5.4%) | 0 |
| **Quarantined Synthetic Test Scaffolds** | 1 (6 chunks) | 1 (6 chunks) | 0 (Strictly isolated) |

---

## 2. Ingested vs. Pending Breakdown by Legal Domain

| Legal Domain | Total Sources | Indexed Sources | Chunks Indexed | Pending Sources | Ingestion Progress |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Constitutional & Public Law** | 9 | 2 | 27 | 7 | 22.2% |
| **Criminal Law & Procedure** | 5 | 2 | 783 | 3 | 40.0% |
| **Criminal Law & Evidence** | 3 | 2 | 6 | 1 | 66.7% |
| **Civil Justice & Commercial Law** | 3 | 3 | 26 | 0 | **100.0%** |
| **Business & Economic Law** | 3 | 2 | 9 | 1 | 66.7% |
| **Technology & Emerging Regulation** | 3 | 2 | 359 | 1 | 66.7% |
| **Other Specialized Domains** | 11 | 3 | 17 | 6 | 27.3% |
| **Total** | **37** | **16** | **1,227** | **19** | **43.2%** |

---

## 3. Breakdown by Document Class & Jurisdiction

### 3.1 Document Class Distribution
- **Central Acts:** 22 total in inventory (11 indexed, 11 pending).
- **Supreme Court Judgments:** 12 total in inventory (4 indexed, 8 pending).
- **Constitution:** 1 total (1 indexed: `IND-CONST-1950`, 20 chunks).
- **Practice Directions / Procedural Rules:** 1 total (pending).
- **Quarantined Synthetic Scaffolds:** 1 (`IND-JUD-DEL-2024-BAIL`, 6 quarantined chunks).

### 3.2 Jurisdiction Scope
- **National / Union (IN):** 36 sources (97.3%).
- **State Jurisdiction (IN-DL):** 1 source (2.7% — quarantined High Court test scaffold).

---

## 4. Complete Inventory of Indexed Primary Sources

| Source Identifier | Title | Domain | Class | Status | Chunks |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `IND-STAT-BNSS-2023` | Bharatiya Nagarik Suraksha Sanhita, 2023 | Criminal Procedure | Act | Current | 767 |
| `IND-STAT-IT-2000` | Information Technology Act, 2000 | Technology Law | Act | Current | 230 |
| `IND-STAT-DPDP-2023` | Digital Personal Data Protection Act, 2023 | Technology Law | Act | Current | 129 |
| `IND-CONST-1950` | The Constitution of India | Constitutional Law | Const | Current | 20 |
| `IND-STAT-BNS-2023` | Bharatiya Nyaya Sanhita, 2023 | Criminal Substantive | Act | Current | 16 |
| `IND-STAT-CPC-1908` | Code of Civil Procedure, 1908 | Civil Procedure | Act | Current | 11 |
| `IND-STAT-ICA-1872` | Indian Contract Act, 1872 | Commercial Law | Act | Current | 8 |
| `IND-STAT-LIMIT-1963` | Limitation Act, 1963 | Civil Procedure | Act | Current | 7 |
| `IND-STAT-SRA-1963` | Specific Relief Act, 1963 | Commercial Law | Act | Current | 7 |
| `IND-JUD-SC-2017-PUTTASWAMY` | Justice K.S. Puttaswamy (Retd.) v. Union of India | Constitutional Law | Judgment | Current | 7 |
| `IND-STAT-ARB-1996` | Arbitration and Conciliation Act, 1996 | Commercial Law | Act | Current | 5 |
| `IND-STAT-CPA-2019` | Consumer Protection Act, 2019 | Economic Law | Act | Current | 4 |
| `IND-STAT-POCSO-2012-SEC4` | Protection of Children from Sexual Offences Act, 2012 | Criminal Law | Act | Current | 4 |
| `IND-STAT-BSA-2023-SEC61` | Bharatiya Sakshya Adhiniyam, 2023 - Section 61 | Evidence Law | Act | Current | 3 |
| `IND-STAT-BSA-2023-SEC63` | Bharatiya Sakshya Adhiniyam, 2023 - Section 63 | Evidence Law | Act | Current | 3 |
| `IND-JUD-DEL-2024-BAIL` | Quarantined Synthetic Bail Scaffold | Criminal Procedure | Judgment | Quarantined | 6 |
| **Total Active Chunks** | — | — | — | — | **1,227** |

---

## 5. Next Priorities for Batch 2 Expansion

1. **State Legislation:** Delhi, Maharashtra, and Karnataka local municipal and tenancy laws.
2. **Supreme Court Constitutional Precedents:** Ingest *Kesavananda Bharati*, *Maneka Gandhi*, *Navtej Singh Johar*, and *Shreya Singhal*.
3. **Delegated Legislation:** Information Technology (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021 and SPDI Rules, 2011.

