# LegalMitra Historical and Temporal Law Model

**System Architecture Specification — Phase 14D**  
**Version:** 1.0.0  
**Engine Implementation:** `legalmitra/temporal/engine.py`  
**Classification:** Core Temporal Grounding & Point-in-Time Resolution Engine

---

## 1. The Temporal Challenge in Indian Law

A legal answer in India cannot merely retrieve the latest statutory text; it must determine what law governed a specific event on the date it occurred. Three recurring scenarios illustrate this:

1. **The 1 July 2024 Criminal Transition:**
   - **Substantive Law:** An offence committed on 30 June 2024 is punishable exclusively under the Indian Penal Code, 1860 (Article 20(1) Constitution of India guarantees protection against retrospective criminalization; BNS Section 358(2) saves pre-commencement offenses). An offence on 2 July 2024 is punishable under the Bharatiya Nyaya Sanhita, 2023.
   - **Procedural Law:** An investigation or trial instituted on or before 30 June 2024 continues under the Code of Criminal Procedure, 1973 by virtue of Section 531(2)(a) of the BNSS, 2023.
2. **Electronic Evidence Certificates (IEA s.65B vs BSA s.63):**
   - BSA Section 63 governs electronic certificates in proceedings instituted on or after 1 July 2024, whereas prior admitted certificates retain validity under BSA Section 170(2).
3. **Phased Digital Data Protection (DPDP Act s.1(2) vs IT Act s.43A):**
   - The DPDP Act received Presidential assent on 11 August 2023, but Section 1(2) specifies that its provisions come into force on dates appointed by Central Government notification.
   - Section 44(2) of the DPDP Act omits Section 43A of the IT Act, 2000. However, because Section 44 has not been notified as appointed, Section 43A remains currently operative in law.

---

## 2. Temporal Data Model

The `TemporalLawEngine` structures temporal reality through two core abstractions:

### 2.1 `StatuteLifecycle`
- `statute_id`: Canonical identifier (e.g. `IND-STAT-BNSS-2023`).
- `enactment_date`: Date passed by Parliament.
- `assent_date`: Date of Presidential assent.
- `commencement_date`: Date brought into force.
- `commencement_notification`: Official Gazette S.O. number (e.g. S.O. 848(E)).
- `repeal_date`: Date repealed by successor statute.
- `savings_clause_ref`: Statutory savings provision (e.g. BNSS s.531(2)(a)).

### 2.2 `ProvisionTemporalVersion`
- `provision_id`: Canonical provision identifier (e.g. `IT-ACT-SEC-43A`).
- `version_number`: Monotonically increasing version counter.
- `version_effective_from`: Start of the legally operative window.
- `version_effective_until`: End of the legally operative window (or `None` if currently in force).
- `repeal_date`: Explicit repeal date.
- `savings_applies_to_pending`: Boolean flag indicating if pending proceedings are saved.

---

## 3. Query Capabilities & APIs

1. `query_provision_at_date(provision_id: str, query_date: str) -> Optional[ProvisionTemporalVersion]`  
   Retrieves the exact provision text in force on the queried date.
2. `resolve_criminal_law_regime(offence_date_str: str, proceedings_institute_date_str: Optional[str]) -> Dict[str, Any]`  
   Automatically determines governing substantive (IPC vs BNS) and procedural (CrPC vs BNSS) law based on Article 20(1) and BNSS Section 531(2)(a).
3. `resolve_data_protection_regime(query_date_str: str) -> Dict[str, Any]`  
   Correctly identifies IT Act Section 43A as operative law while marking DPDP substantive provisions as unappointed.

---

## 4. Quality Gate Integration

Gate 4 (Temporal Validity) and Gate 5 (Anti-Conflation) of `DataQualityGate` directly interface with `TemporalLawEngine`:
- **Uncommenced as Operative Check:** Rejects any generated answer asserting that an uncommenced statute is in force.
- **Conflation Rejection:** Strictly prevents a repealed statute's status from being assigned to its replacement statute (e.g., asserting that BNSS Section 531 is repealed because CrPC was repealed).

