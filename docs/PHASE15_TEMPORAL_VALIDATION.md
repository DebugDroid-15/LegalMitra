# LegalMitra Phase 15 — Historical & Current-Law Temporal Validation

**Engine Module:** `legalmitra/temporal/engine.py`  
**Test Suite:** `tests/test_corpus_scale.py` & `tests/test_corpus_pipeline.py`  
**Validation Status:** Passed (100% automated test coverage across temporal boundaries)  
**Target Repository:** `c:\PROJECTS\LegalMitra`

---

## 1. Executive Summary

Indian law undergoes phased commencements, major statutory substitutions, and complex repeal-and-savings transitions. A legal AI system that fails to account for temporal dates will provide wrong answers—for example, citing the Indian Penal Code 1860 for offences committed in late 2024, or stating that specific performance remains an equitable discretionary remedy under the Specific Relief Act after 1 October 2018.

In Phase 15, the `TemporalLawEngine` was extended to support multi-regime temporal resolution and provision versioning across 13 Central Statutes.

---

## 2. Key Transition Boundaries Modeled

| Legal Domain / Regime | Key Transition Date | Pre-Transition Law | Post-Transition Law | Statutory Authority |
| :--- | :---: | :--- | :--- | :--- |
| **Specific Performance** | **2018-10-01** | Discretionary equitable remedy; damages primary rule | Mandatory statutory rule ("shall be enforced") | Act No. 18 of 2018; S.O. 4888(E) |
| **Infrastructure Injunctions** | **2018-10-01** | Civil courts had discretion to grant interim injunctions | Statutory prohibition on injunctions delaying infrastructure | SRA 1963 Section 20A; S.O. 4888(E) |
| **Arbitral Setting Aside (s.34)** | **2015-10-23** | Expansive public policy merits review (*Saw Pipes*) | Restricted patent illegality (domestic only; merits bar) | Act No. 3 of 2016; Ordinance 23 Oct 2015 |
| **Arbitral Timelines (s.29A)** | **2015-10-23** | No statutory deadline for award completion | Mandatory 12-month timeline from pleadings | Act No. 3 of 2016; 2019 Amendment |
| **Consumer Protection** | **2020-07-20** | CPA 1986 (no product liability, no CCPA) | CPA 2019 (CCPA, statutory product liability, e-commerce) | Act No. 35 of 2019; S.O. 2351(E) |
| **Substantive Criminal Law** | **2024-07-01** | Indian Penal Code, 1860 | Bharatiya Nyaya Sanhita, 2023 | Act No. 45 of 2023; S.O. 849(E); Art. 20(1) |
| **Criminal Procedure** | **2024-07-01** | CrPC 1973 (saved for pre-01.07.2024 pending proceedings) | BNSS 2023 | Act No. 46 of 2023; S.O. 848(E); s.531(2)(a) |
| **Evidence & Electronic Records** | **2024-07-01** | Indian Evidence Act, 1872 (s.65B) | Bharatiya Sakshya Adhiniyam, 2023 (s.61, 63) | Act No. 47 of 2023; S.O. 850(E); s.170(2) |
| **Data Protection / Compensation** | **Ongoing (Phased)** | IT Act 2000 Section 43A + SPDI Rules 2011 | DPDP Act 2023 (substantive sections pending s.1(2) notice) | DPDP Act 2023 s.1(2) & s.44(2) |
| **Women's Representation** | **2023-09-28** | No statutory quota in Lok Sabha | 33% reservation under Article 330A | Constitution (106th Amendment) Act, 2023 |

---

## 3. Dedicated Regime Resolvers in `TemporalLawEngine`

### 3.1 Specific Relief Regime Resolver
```python
def resolve_specific_relief_regime(self, contract_date_str: str) -> Dict[str, Any]
```
- **Inputs:** `contract_date_str` (ISO format `YYYY-MM-DD`).
- **Logic:** Compares contract date against `2018-10-01`.
- **Pre-2018 Output:** `regime: Specific Relief Act, 1963 (Pre-2018 Amendment)`, `specific_performance_character: Equitable and Discretionary (former Section 20)`, `infrastructure_bar_active: False`.
- **Post-2018 Output:** `regime: Specific Relief Act, 1963 (Post-2018 Amendment by Act 18 of 2018)`, `specific_performance_character: Mandatory Statutory Rule ('shall be enforced')`, `infrastructure_bar_active: True`.

### 3.2 Arbitration Regime Resolver
```python
def resolve_arbitration_regime(self, arbitration_commence_date_str: str) -> Dict[str, Any]
```
- **Inputs:** `arbitration_commence_date_str` (e.g. date of notice under Section 21).
- **Logic:** Compares commencement date against `2015-10-23`.
- **Pre-2015 Output:** `s34_patent_illegality_scope: Broad public policy review (ONGC v. Saw Pipes standard)`, `s29a_timeline_mandate: False`, `merits_review_expressly_barred: False`.
- **Post-2015 Output:** `s34_patent_illegality_scope: Restricted patent illegality (domestic awards only; patent on the face of award)`, `s29a_timeline_mandate: True`, `merits_review_expressly_barred: True`.

### 3.3 Consumer Protection Regime Resolver
```python
def resolve_consumer_regime(self, cause_of_action_date_str: str) -> Dict[str, Any]
```
- **Inputs:** `cause_of_action_date_str`.
- **Logic:** Compares date against `2020-07-20`.
- **Pre-2020 Output:** `regime: Consumer Protection Act, 1986`, `repealed: True`, `savings_applicable: True` (Section 107(2) saves pre-existing complaints), `product_liability_statutory_claim: False`.
- **Post-2020 Output:** `regime: Consumer Protection Act, 2019`, `repealed: False`, `product_liability_statutory_claim: True`, `central_regulator_ccpa: True`.

---

## 4. Provision-Level Versioning & Point-in-Time Querying

Using `query_provision_at_date(provision_id, query_date)`, the engine resolves which statutory text was in force on any arbitrary date in Indian legal history:

1. **`SRA-SEC-10` Query:**
   - On `2015-05-01` -> Returns Version 1 (discretionary).
   - On `2022-05-01` -> Returns Version 2 (mandatory).
2. **`ARB-SEC-29A` Query:**
   - On `2014-01-01` -> Returns `None` (provision did not exist).
   - On `2020-01-01` -> Returns Version 1 (12-month statutory award mandate).
3. **`CONST-ART-330A` Query:**
   - On `2022-01-01` -> Returns `None` (article did not exist).
   - On `2024-01-01` -> Returns Version 1 (33% reservation for women in Lok Sabha).
4. **`IEA-SEC-65B` vs `BSA-SEC-63` Query:**
   - On `2020-01-01` -> Returns `IEA-SEC-65B` (operative).
   - On `2025-01-01` -> `IEA-SEC-65B` is repealed; returns `BSA-SEC-63` (operative).

---

## 5. Automated Verification & Regression Testing

All temporal resolvers and point-in-time lookups are comprehensively tested in `tests/test_corpus_scale.py`:
- `test_temporal_specific_relief_transition` -> PASSED
- `test_temporal_arbitration_transition` -> PASSED
- `test_temporal_consumer_protection_transition` -> PASSED
- `test_temporal_provision_versioning_sra_arb_const` -> PASSED
- `test_temporal_criminal_law_transition` -> PASSED
- `test_temporal_data_protection_regime` -> PASSED
- `test_temporal_provision_version_lookup` -> PASSED

