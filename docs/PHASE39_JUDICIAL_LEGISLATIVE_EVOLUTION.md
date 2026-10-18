# LegalMitra — Phase 39: Judicial-Legislative Evolution Graph V2

**Document Version:** 1.0.0  
**Phase:** 39 — National Judicial Corpus Expansion & Precedent Verification  
**Status:** Completed & Validated  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  

---

## 1. Executive Summary

This document specifies the bidirectional Judicial-to-Legislative Evolution Graph (Version 2) implemented in Phase 39 Workstream F. The system enforces strict evidentiary causation standards, explicitly preventing the false inference of causation from mere temporal sequence.

Machine-readable graph: `data/21_judicial_infrastructure/judicial_legislative_evolution_graph_v2.json`.

---

## 2. Seven Mandatory Relationship Categories

| Category | Strict Legal Definition | Evidentiary Requirement |
| :--- | :--- | :--- |
| `DIRECT_LEGISLATIVE_RESPONSE` | Statute or amendment enacted directly to codify or supersede a judicial holding | Official Statement of Objects and Reasons (SOR), Parliamentary Debates, or Act preamble explicitly naming the decision |
| `EXPRESS_STATUTORY_REFERENCE` | Statute expressly references a judicial doctrine or case | Direct textual reference within statutory section or explanation |
| `OFFICIAL_REFORM_RECOMMENDATION`| Law Commission of India or official expert committee recommended statutory amendment | Numbered Law Commission Report or Committee Report explicitly citing the judgment |
| `DOCUMENTED_POLICY_INFLUENCE` | Official policy paper or White Paper cites the judgment | Official Ministry publication or Gazetted policy |
| `DOCTRINAL_INTERACTION` | Iterative constitutional dialogue between judiciary and legislature | Doctrinal jurisprudence without single causal enactment |
| `TEMPORAL_SEQUENCE_ONLY` | Legislation enacted subsequent to judgment without documented official causation | Non-causal classification; strictly barred from claiming legislative response |
| `HYPOTHESIZED_AWAITING_VERIFICATION`| Candidate link under research | Marked unverified; excluded from production RAG assertions |

---

## 3. Verified Bidirectional Evolution Edges

1. **`EVO-01-VISHAKA-POSH`**: *Vishaka v. State of Rajasthan* (AIR 1997 SC 3011) -> *Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013* (`DIRECT_LEGISLATIVE_RESPONSE`). Proven by SOR, POSH Bill No. 144 of 2010.
2. **`EVO-02-SHAHBANO-MWACT`**: *Mohd. Ahmed Khan v. Shah Bano Begum* (AIR 1985 SC 945) -> *Muslim Women (Protection of Rights on Divorce) Act, 1986* (`DIRECT_LEGISLATIVE_RESPONSE`). Proven by SOR, Act 25 of 1986.
3. **`EVO-03-DKBASU-CRPC2008`**: *D.K. Basu v. State of West Bengal* (AIR 1997 SC 610) -> *Code of Criminal Procedure (Amendment) Act, 2008* (Act 5 of 2009) (`DIRECT_LEGISLATIVE_RESPONSE`). Proven by Law Commission 177th Report (2001) & SOR CrPC Amendment Act 2008.
4. **`EVO-04-PUTTASWAMY-DPDPA`**: *Justice K.S. Puttaswamy v. Union of India* ((2017) 10 SCC 1) -> *Digital Personal Data Protection Act, 2023* (Act 22 of 2023) (`DIRECT_LEGISLATIVE_RESPONSE`). Proven by Justice Srikrishna Committee Report (2018) & SOR DPDP Act 2023.
5. **`EVO-05-JOSEPHSHINE-BNS`**: *Joseph Shine v. Union of India* (AIR 2018 SC 4898) -> *Bharatiya Nyaya Sanhita 2023* (Act 45 of 2023) (`DIRECT_LEGISLATIVE_RESPONSE`). Proven by Parliamentary Standing Committee on Home Affairs Report No. 246 (2023).
6. **`EVO-06-SHAYARA-TRIPLE-TALAQ`**: *Shayara Bano v. Union of India* ((2017) 9 SCC 1) -> *Muslim Women (Protection of Rights on Marriage) Act, 2019* (Act 20 of 2019) (`DIRECT_LEGISLATIVE_RESPONSE`). Proven by SOR Act 20 of 2019.
7. **`EVO-07-MCMEHTA-NGT`**: *M.C. Mehta v. Union of India* ((1987) 1 SCC 395) -> *National Green Tribunal Act, 2010* (`OFFICIAL_REFORM_RECOMMENDATION`). Proven by Law Commission of India 186th Report (2003).
8. **`EVO-08-BANKNAT-TEMPORAL`**: *R.C. Cooper v. Union of India* (AIR 1970 SC 564) -> *Banking Companies (Acquisition and Transfer of Undertakings) Act, 1970* (`DIRECT_LEGISLATIVE_RESPONSE`). Proven by Statement of Objects and Reasons, Act 5 of 1970.

---

## 4. Evidentiary Invariant Enforcement

The Python engine [`LegislativeEvolutionEngine`](file:///c:/PROJECTS/LegalMitra/legalmitra/judicial/legislative_evolution.py) programmatically validates that any relationship registered under direct response or official reform carries a verified, non-empty primary evidentiary citation, guaranteeing that speculative causation can never enter the knowledge base.
