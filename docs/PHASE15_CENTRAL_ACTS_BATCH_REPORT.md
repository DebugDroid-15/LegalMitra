# LegalMitra Phase 15 — Central Legislation Batch Report

**Batch Identifier:** `BATCH_15C_CENTRAL_ACTS`  
**Execution Timestamp:** 2026-10-16T18:41:22 to 2026-10-16T18:41:36  
**Status:** Completed & Validated  
**Target Repository:** `c:\PROJECTS\LegalMitra`  
**Knowledge Base Database:** `data/legalmitra_kb.db`

---

## 1. Executive Summary

Phase 15 Batch 1 successfully expanded the LegalMitra Indian Legal Knowledge Base from 8 previously indexed statutes to **16 indexed primary sources**, adding **78 new provision-level chunks** for 8 foundational Central Acts. The Knowledge Base now contains **1,227 chunks** across constitutional, criminal, civil, limitation, contract, specific relief, arbitration, and consumer protection domains.

All 8 documents were acquired via the resumable acquisition manager, normalized into validated `StatuteDocument` structures, verified against SHA-256 integrity checksums, and indexed into the SQLite + FTS5 full-text database with zero data corruption.

---

## 2. Ingested Central Legislation Summary Table

| Source ID | Official Title | Enactment / Commencement | Provisions Indexed | Chunks Indexed | SHA-256 Checksum |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `IND-CONST-1950` | The Constitution of India | 1949-11-26 / 1950-01-26 | 10 | 20 | `3bb22eb1b8b250216341bce80ec84d9be0b0f60b7213ed4fc99f9cf28fd3d4cc` |
| `IND-STAT-BNS-2023` | The Bharatiya Nyaya Sanhita, 2023 | 2023-12-25 / 2024-07-01 | 8 | 16 | `b6446d1394555e8943a3b257ad2b97d9c691f6d6fbeab09701757bfc165e079f` |
| `IND-STAT-CPC-1908` | The Code of Civil Procedure, 1908 | 1908-03-21 / 1909-01-01 | 7 | 11 | `d38a1cdae8edd3e2f44e88f862ff2b6ec14626fee088f05305ff6d55bad77d74` |
| `IND-STAT-LIMIT-1963` | The Limitation Act, 1963 | 1963-10-05 / 1964-01-01 | 6 | 7 | `9e4571ec30f6d899a8245f94ca71251ac092f87cdd718cfc27fd8002c8ef6aff` |
| `IND-STAT-ICA-1872` | The Indian Contract Act, 1872 | 1872-04-25 / 1872-09-01 | 7 | 8 | `ad4f49c36cc43f7235addfef3913e9b167aaadba63574b1803712468154dd136` |
| `IND-STAT-SRA-1963` | The Specific Relief Act, 1963 | 1963-12-13 / 1964-03-01 | 5 | 7 | `9af6d3f6f4f08139911c39575beb507f26418a3dc27631a6fd78262b45c1aaa9` |
| `IND-STAT-ARB-1996` | The Arbitration and Conciliation Act, 1996 | 1996-08-16 / 1996-08-22 | 5 | 5 | `832b3112b319a6686ea0d04eabcee8789da74aa46253d00763cb3e4d3a1e25c0` |
| `IND-STAT-CPA-2019` | The Consumer Protection Act, 2019 | 2019-08-09 / 2020-07-20 | 4 | 4 | `7f8c618e81a9ba3a2a32b171092dfc2badb0a28f2f4d10e39bb88fc10702055b` |
| **Batch 1 Total** | **8 Central Acts** | — | **52 Provisions** | **78 Chunks** | **All Verified** |

---

## 3. Provision-Level Detail of Ingested Sections

### 3.1 The Constitution of India (`IND-CONST-1950`)
- **Preamble:** Sovereign Socialist Secular Democratic Republic, Justice, Liberty, Equality, Fraternity.
- **Article 14:** Equality before law and equal protection of the laws.
- **Article 19:** Protection of certain rights regarding freedom of speech, assembly, association, movement, residence, and profession, with sub-clauses (1)(a)-(g) and reasonable restrictions under clauses (2)-(6).
- **Article 20:** Protection in respect of conviction for offences (ex post facto law, double jeopardy, self-incrimination).
- **Article 21:** Protection of life and personal liberty (*Maneka Gandhi* / *Puttaswamy* bedrock).
- **Article 21A:** Right to education for children aged 6 to 14 years.
- **Article 32:** Remedies for enforcement of Fundamental Rights (Supreme Court prerogative writs).
- **Article 226:** Power of High Courts to issue certain writs for enforcement of Part III and for any other purpose.
- **Article 368:** Power of Parliament to amend the Constitution and procedure therefor.
- **Article 330A:** Reservation of seats for women in the House of the People (Constitution 106th Amendment Act, 2023).

### 3.2 Bharatiya Nyaya Sanhita, 2023 (`IND-STAT-BNS-2023`)
- **Section 1:** Short title, commencement (01.07.2024 via S.O. 849(E)), and application.
- **Section 4:** Punishments (Death, Imprisonment for life, Imprisonment, Forfeiture of property, Fine, Community service).
- **Section 103:** Punishment for murder (subsection 1 individual murder, subsection 2 mob lynching by group of 5+ persons on grounds of race, caste, sex, place of birth, language, religion).
- **Section 111:** Organised crime (definition, syndicates, continuing unlawful activity, economic offences).
- **Section 303:** Theft (definition, taking dishonestly moveable property without consent).
- **Section 304:** Snatching (statutory codification distinguishing abrupt forceful seizure from general theft).
- **Section 318:** Cheating and dishonestly inducing delivery of property.
- **Section 358:** Repeal of Indian Penal Code, 1860 with savings for pre-01.07.2024 offences and pending proceedings.

### 3.3 Code of Civil Procedure, 1908 (`IND-STAT-CPC-1908`)
- **Section 9:** Courts to try all civil suits unless expressly or impliedly barred.
- **Section 10:** Stay of suit (*res sub judice*).
- **Section 11:** *Res judicata* (Explosive explanations I through VIII detailing directly and substantially in issue, competence, constructive res judicata).
- **Section 80:** Notice to Government or public officers prior to institution of suit (2-month mandatory pre-litigation notice, urgency dispensation).
- **Section 89:** Settlement of disputes outside the Court (Arbitration, Conciliation, Judicial settlement including Lok Adalat, Mediation).
- **Section 151:** Saving of inherent powers of Court to make orders necessary for the ends of justice.
- **Order XXXIX Rule 1:** Cases in which temporary injunction may be granted (preservation of property, prevention of waste/damage).

### 3.4 The Limitation Act, 1963 (`IND-STAT-LIMIT-1963`)
- **Section 3:** Bar of limitation (dismissal of suit/appeal/application instituted after prescribed period even if limitation not pleaded).
- **Section 5:** Extension of prescribed period in certain cases (condonation of delay upon sufficient cause, excluding suits).
- **Section 12:** Exclusion of time in legal proceedings (day of judgment/order, time requisite for obtaining certified copy).
- **Section 14:** Exclusion of time of proceeding bona fide in court without jurisdiction.
- **Section 18:** Effect of acknowledgment in writing before expiration of prescribed period.
- **Section 27:** Extinguishment of right to property at the determination of the period limited for instituting a suit.

### 3.5 The Indian Contract Act, 1872 (`IND-STAT-ICA-1872`)
- **Section 2:** Interpretation-clause (proposal, acceptance, agreement, consideration, voidable contract, void agreement).
- **Section 10:** What agreements are contracts (free consent, competent parties, lawful consideration, lawful object).
- **Section 27:** Agreement in restraint of trade void (statutory rule and sole exception for sale of goodwill).
- **Section 28:** Agreements in restraint of legal proceedings void (preservation of arbitration exception).
- **Section 56:** Agreement to do impossible act; doctrine of frustration by subsequent impossible or unlawful event.
- **Section 73:** Compensation for loss or damage caused by breach of contract (*Hadley v. Baxendale* codification, remote damages excluded).
- **Section 74:** Compensation for breach of contract where penalty stipulated for (reasonable compensation not exceeding penalty).

### 3.6 The Specific Relief Act, 1963 (`IND-STAT-SRA-1963`)
- **Section 10:** Specific performance in respect of contracts (mandatory rule: "shall be enforced by the court" substituted by Act 18 of 2018).
- **Section 14:** Contracts not specifically enforceable (substituted performance obtained, performance of continuous duty, highly personal volition).
- **Section 20:** Substituted performance of contract (notice of 30 days to defaulting party, performance through third party at promisor's expense).
- **Section 20A:** Special provisions for contract relating to infrastructure projects (statutory prohibition on interim or permanent injunctions that cause impediment or delay).
- **Section 41:** Injunction when refused (grounds including availability of equally efficacious relief).

### 3.7 The Arbitration and Conciliation Act, 1996 (`IND-STAT-ARB-1996`)
- **Section 7:** Arbitration agreement (writing requirement, exchange of letters, telex, telegrams, electronic communications).
- **Section 8:** Power to refer parties to arbitration where there is an arbitration agreement (mandatory judicial referral upon prima facie existence).
- **Section 9:** Interim measures by Court (before, during, or after arbitral award before enforcement).
- **Section 29A:** Time limit for arbitral award (12 months from completion of pleadings for domestic arbitrations, fast-track option, judicial extension).
- **Section 34:** Application for setting aside arbitral award (grounds, patent illegality for domestic awards, express bar on merits review).

### 3.8 The Consumer Protection Act, 2019 (`IND-STAT-CPA-2019`)
- **Section 2:** Comprehensive definitions (consumer, product liability, unfair trade practice, electronic service provider, misleading advertisement).
- **Section 34:** Jurisdiction of District Commission (pecuniary threshold and territorial jurisdiction based on complainant's residence/employment).
- **Section 82:** Product liability action (statutory cause of action against manufacturer, service provider, or seller).
- **Section 107:** Repeal and savings (repeal of Consumer Protection Act, 1986 with savings for pending actions).

---

## 4. Ingestion Quality and Verification

1. **Schema Adherence:** 100% of the 8 documents validated cleanly against the Pydantic v2 `StatuteDocument` schema with `StatuteSection`, `StatuteSubSection`, `StatuteProviso`, and `StatuteExplanation` classes.
2. **Cryptographic Checksums:** Each raw document JSON was computed with SHA-256 and stored in `data/08_corpus/batch_01_central_acts_report.json` and `data/08_corpus/acquisition_checkpoint.json`.
3. **Knowledge Base Parity:** All 78 chunks are searchable in `data/legalmitra_kb.db`.
4. **Frozen Handoff Preservation:** `scripts/verify_freeze.py` passed with 100% bitwise integrity across all 6 Phase 9 review snapshot artifacts before and after ingestion.

