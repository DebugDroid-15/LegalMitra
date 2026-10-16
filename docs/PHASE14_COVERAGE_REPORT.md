# LegalMitra National Indian Legal Corpus Coverage Report

**Specification Document — Phase 14I**  
**Version:** 1.0.0  
**Machine-Readable Audit Summary:** `data/08_corpus/coverage_summary.json`  
**Master Inventory:** `data/08_corpus/coverage_inventory.json`  
**Classification:** Empirical Coverage Audit & Gap Register

---

## 1. Metrics & Denominators

To ensure transparent reporting without exaggerating coverage:
- **Total Tracked Legal Sources (Denominator):** **37 sources**
- **Indexed Sources in Knowledge Base:** **8 sources** (1,149 chunks)
- **Fully Extracted & Validated:** **8 sources (21.6%)**
- **Pending Ingestion Pipeline:** **27 sources (73.0%)**
- **Inaccessible / Large Document Backlog:** **2 sources**
- **Strictly Quarantined Test Scaffolds:** **1 source** (6 chunks, isolated with `is_synthetic_scaffold = 1`)

---

## 2. Categorical Distribution

### 2.1 By Legal Status
| Status | Count | Percentage | Operational Meaning |
|---|:---:|:---:|---|
| `current` | 30 | 81.1% | Active enactments and operative precedents |
| `historical` | 4 | 10.8% | Pre-2024 criminal codes saved for pending matters |
| `quarantined` | 1 | 2.7% | Synthetic test scaffold excluded from retrieval |
| `inaccessible` | 1 | 2.7% | Large monolithic PDF awaiting chunked extraction |
| `unverified` | 1 | 2.7% | Format rejection test fixture |

### 2.2 By Document Class
- **Acts:** 22 (59.5%)
- **Judicial Precedents:** 12 (32.4%)
- **Constitutional Foundations:** 1 (2.7%)
- **Practice Directions:** 1 (2.7%)
- **Test Fixtures:** 1 (2.7%)

---

## 3. Prioritized Gap Register

The 27 pending sources are ranked by public importance, availability, and implementation complexity:

| Priority | Document / Domain | Document ID | Public Importance | Source Availability | Implementation Cost |
|:---:|---|---|:---:|:---:|:---:|
| **P1** | Bharatiya Nyaya Sanhita, 2023 | `IND-STAT-BNS-2023` | **Critical** | Available (India Code) | Low (JSON/Text) |
| **P1** | The Constitution of India | `IND-CONST-1950` | **Critical** | Available (Legislative Dept) | Medium (Articles/Schedules) |
| **P1** | Code of Civil Procedure, 1908 | `IND-STAT-CPC-1908` | **High** | Available (India Code) | Medium (Orders/Rules) |
| **P2** | Limitation Act, 1963 | `IND-STAT-LIMIT-1963` | **High** | Available (India Code) | Low (Single Act) |
| **P2** | Indian Contract Act, 1872 | `IND-STAT-ICA-1872` | **High** | Available (India Code) | Low (Single Act) |
| **P2** | Arbitration & Conciliation Act, 1996 | `IND-STAT-ARB-1996` | **High** | Available (India Code) | Low (Single Act) |
| **P2** | Companies Act, 2013 | `IND-STAT-COMP-2013` | **High** | Available (MCA/India Code) | High (470 sections) |
| **P3** | Landmark Supreme Court Precedents | Kesavananda, Maneka, Indra Sawhney, Bommai | **High** | Available (SCI Portal) | Medium (Ratio Extraction) |
| **P3** | SCI Practice Handbook (278 pages) | `IND-GUIDE-SCI-PROC-2025` | **Medium** | Available (SCI Portal) | Medium (Multi-part Chunking) |

