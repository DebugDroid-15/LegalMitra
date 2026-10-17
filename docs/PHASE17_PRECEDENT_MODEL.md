# LEGALMITRA — PHASE 17D: PRECEDENT RELATIONSHIPS & JUDICIAL HISTORY REPORT

**Workspace:** `c:\PROJECTS\LegalMitra`  
**Execution Date:** 2026-10-17  
**Status:** COMPLETE & VERIFIED  

---

## 1. Executive Summary

Under **Article 141 of the Constitution of India**, the law declared by the Supreme Court of India is binding on all courts within the territory of India. However, judicial precedent is dynamic: earlier rulings are affirmed, distinguished, doubted, or overruled by larger benches or subsequent statutory enactments.

In Phase 17D, LegalMitra updated its precedent relationship engine (`legalmitra/caselaw/precedent.py`) to model bidirectional judicial treatment relationships with explicit passage references, bench strengths, and human verification flags.

All 6 active landmark relationships were exported to `data/08_corpus/precedent_relationships.json`.

---

## 2. Precedent Treatment Graph

```
                                [Anvar P.V. (2014)]
                                        ^
                                        | (AFFIRMED)
                                        |
  [Shafhi Mohammad (2018)] <--- (OVERRULED) --- [Arjun Panditrao Khotkar (2020)]
                                                         (3-Judge Bench)
```

```
[M.P. Sharma (1954, 8-J)] <--- (OVERRULED) --- [K.S. Puttaswamy (2017)]
[Kharak Singh (1963, 6-J)] <--- (OVERRULED) ---          ^
[ADM Jabalpur (1976, 5-J)] <--- (OVERRULED) ------------| (9-Judge Bench)
```

```
[Suresh Koushal (2014)] <--- (OVERRULED) --- [Navtej Singh Johar (2018)]
                                                   (5-Judge Bench)
```

---

## 3. Explicit Relationship Manifest

| Relationship ID | Citing Case | Cited Case | Treatment | Governing Statute / Subject | Passage Reference | Verification Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `REL-ARJUN-AFFIRMS-ANVAR` | *Arjun Panditrao Khotkar* (2020) | *Anvar P.V.* (2014) | `AFFIRMED` | BSA s.63 / IEA s.65B Electronic Records | Paras 51 & 72 | `is_human_reviewed=True` |
| `REL-ARJUN-OVERRULES-SHAFHI` | *Arjun Panditrao Khotkar* (2020) | *Shafhi Mohammad* (2018) | `OVERRULED` | BSA s.63 / IEA s.65B Certificate Dispensation | Para 72 | `is_human_reviewed=True` |
| `REL-PUTTASWAMY-OVERRULES-MPSHARMA` | *K.S. Puttaswamy* (2017) | *M.P. Sharma* (1954) | `OVERRULED` | Constitution Art. 21 Right to Privacy | Ratio Decidendi | `is_human_reviewed=True` |
| `REL-PUTTASWAMY-OVERRULES-KHARAK` | *K.S. Puttaswamy* (2017) | *Kharak Singh* (1964) | `OVERRULED` | Constitution Art. 21 Domiciliary Visits | Ratio Decidendi | `is_human_reviewed=True` |
| `REL-PUTTASWAMY-OVERRULES-ADMJABALPUR` | *K.S. Puttaswamy* (2017) | *ADM Jabalpur* (1976) | `OVERRULED` | Constitution Art. 21 Emergency Suspension | Ratio Decidendi | `is_human_reviewed=True` |
| `REL-NAVTEJ-OVERRULES-KOUSHAL` | *Navtej Singh Johar* (2018) | *Suresh Kumar Koushal* (2014) | `OVERRULED` | IPC s.377 / BNS Consensual Relationships | Ratio Decidendi | `is_human_reviewed=True` |

---

## 4. Bench Hierarchy & Article 141 Evaluation Rules

1. **Bench Strength Supremacy**: A decision delivered by a larger bench of the Supreme Court binds smaller benches and co-equal benches (*Central Board of Dawoodi Bohra Community v. State of Maharashtra* (2005) 2 SCC 673).
2. **Per Incuriam & Overruled Status**: When an earlier decision is expressly overruled (e.g. *Shafhi Mohammad* overruled by *Arjun Khotkar*), it ceases to have binding precedential authority.
3. **High Court Territorial Limitation**: Rulings of a High Court (e.g. Delhi High Court or Bombay High Court) are binding on subordinate courts within that State/UT, but hold persuasive authority before other High Courts.

