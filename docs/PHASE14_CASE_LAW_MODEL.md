# LegalMitra Case Law and Precedent Hierarchy Model

**System Architecture Specification — Phase 14F**  
**Version:** 1.0.0  
**Engine Implementation:** `legalmitra/caselaw/precedent.py`  
**Classification:** Precedent Hierarchy, Bench Strength & Treatment Specification

---

## 1. Constitutional Basis (Article 141)

In the Indian legal system, judicial precedent is governed strictly by the Constitution of India and doctrine of stare decisis:
1. **Article 141 of the Constitution:** Declares that the law declared by the Supreme Court shall be binding on all courts within the territory of India.
2. **Bench Strength Hierarchy:** A bench of larger strength binds benches of co-equal or smaller strength of the Supreme Court. A 5-Judge Constitution Bench cannot overrule a 7-Judge Bench; only a 9-Judge or larger bench may do so (e.g., *Puttaswamy I* 9-Judge Bench overruling *M.P. Sharma* 8-Judge Bench and *Kharak Singh* 6-Judge Bench).
3. **High Court Precedents:** Judgments of a High Court are binding on all subordinate courts and single benches within its territorial jurisdiction, but hold only persuasive authority before other High Courts.

---

## 2. Precedent Data Schema

### 2.1 Bench Strength Enum (`BenchStrength`)
- `SINGLE_JUDGE`: 1 Judge.
- `DIVISION_BENCH`: 2 Judges.
- `FULL_BENCH`: 3 Judges.
- `CONSTITUTION_BENCH_5`: 5 Judges.
- `CONSTITUTION_BENCH_7`: 7 Judges.
- `CONSTITUTION_BENCH_9`: 9 Judges.
- `LARGEST_BENCH_13`: 13 Judges (*Kesavananda Bharati*).

### 2.2 Precedent Treatment Enum (`PrecedentTreatment`)
- `CITED`: Referenced without substantive expansion or departure.
- `FOLLOWED`: Principle applied directly to the dispute.
- `DISTINGUISHED`: Factual or statutory differences justify departing from the ruling.
- `OVERRULED`: Expressly held bad law by a larger bench of the Supreme Court.
- `AFFIRMED`: Higher appellate court affirms the ruling of the lower court.
- `REVERSED`: Appellate court sets aside the ruling of the court below.

---

## 3. Precedent Relationships & Overruling Tracking

The `PrecedentHierarchyManager` tracks direct treatment relationships:
- **`REL-PUTTASWAMY-OVERRULES-MPSHARMA`:** Overruled *M.P. Sharma* (1954) on privacy.
- **`REL-PUTTASWAMY-OVERRULES-KHARAK`:** Overruled *Kharak Singh* (1963) majority on privacy.
- **`REL-PUTTASWAMY-OVERRULES-ADMJABALPUR`:** Expressly overruled *ADM Jabalpur* (1976) majority.
- **`REL-NAVTEJ-OVERRULES-KOUSHAL`:** Overruled *Suresh Kumar Koushal* (2014) on Section 377 IPC.

When an overruled precedent is queried, the engine flags `is_binding = False` and directs the user to the overruling authority, preventing the retrieval of obsolete jurisprudence as good law.

