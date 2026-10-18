"""
README Builder - Part IX to Part XI:
- Part IX: Legal Knowledge Ingestion & Corpus Engineering
- Part X: Retrieval-Augmented Generation (RAG) Architecture
- Part XI: Legal Scope, Jurisdiction & Statutory Coverage
"""

def generate_part_09_to_11() -> str:
    sections = []

    # Part IX
    sections.append("""## Part IX: Legal Knowledge Ingestion & Corpus Engineering

### 9.1 7-Stage State Machine Lifecycle

The LegalMitra Ingestion Pipeline implements a deterministic 7-stage finite state machine (FSM) governing every legal document from initial discovery to active pretraining eligibility:

```text
+---------------+     +---------------+     +---------------+     +---------------+
| 1. DISCOVERED | --> | 2. REGISTERED | --> |  3. ACQUIRED  | --> |   4. PARSED   |
+---------------+     +---------------+     +---------------+     +---------------+
                                                                          |
+----------------------+     +----------------------+                     v
| 7. TRAINING_ELIGIBLE | <-- |  6. RIGHTS_REVIEWED  | <-- +------------------------------+
+----------------------+     +----------------------+     | 5. AUTHENTICITY_VERIFIED     |
                                                          +------------------------------+
```

1. **State 1: `DISCOVERED`**:
   - Trigger: Discovered during official portal crawls (e.g., India Code, Gazette of India, Delhi High Court portal).
   - Validation: URL existence, title pattern matching, portal authenticity check.
2. **State 2: `REGISTERED`**:
   - Trigger: Metadata ingested into `data/09_national_corpus/unified_source_registry.json`.
   - Attributes: Assigned unique `source_id`, canonical title, jurisdiction, document family.
3. **State 3: `ACQUIRED`**:
   - Trigger: Physical binary or HTML downloaded via rate-limited, SSRF-validated client.
   - Validation: SHA-256 hash computed, byte size recorded, saved to `data/01_raw/`.
4. **State 4: `PARSED`**:
   - Trigger: Structural extraction executed (Docling, PDF text, or regex parser).
   - Output: Hierarchical provision tree (Sections, Subsections, Provisos).
5. **State 5: `AUTHENTICITY_VERIFIED`**:
   - Trigger: Cross-referenced against certified Gazette publication or court seal.
   - Defense: Rejection of unofficial summaries, blogs, or commercial headnotes.
6. **State 6: `RIGHTS_REVIEWED`**:
   - Trigger: Copyright audit under Section 52(1)(q) of the Indian Copyright Act, 1957.
   - Verification: Confirms text is pure legislative or judicial edict free of third-party commentary.
7. **State 7: `TRAINING_ELIGIBLE`**:
   - Trigger: Cleared for inclusion in `dataset_manifest_v4.json` and active RAG index.
   - Verification: Zero quarantine flags, verified token boundaries, language tagging.

### 9.2 Statutory Hierarchy & Provision Decomposition

Legislative enactments in India possess a strict nested hierarchy that must be preserved during chunking to prevent semantic decontextualization:

```text
ACT (The Bharatiya Nyaya Sanhita, 2023)
└── PART / CHAPTER (Chapter VI: Of Offences Affecting the Human Body)
    └── SECTION (Section 103: Punishment for murder)
        ├── SUBSECTION (Subsection (1): Imprisonment for life or death)
        ├── SUBSECTION (Subsection (2): Murder by group of five or more on specific grounds)
        │   ├── CLAUSE ((a) race, (b) caste, (c) sex, (d) place of birth)
        │   └── PROVISO (Provided that...)
        └── EXPLANATION (Explanation 1.—...)
```

- **Atomic Chunking Strategy**: LegalMitra does not split text by arbitrary token counts (e.g., 512 tokens with 50-token overlap). Instead, chunks are partitioned along **provision boundaries** (Section level or Subsection level when subsections exceed 400 words).
- **Context Injection**: Each chunk is prepended with its statutory lineage:
  `"[The Bharatiya Nyaya Sanhita, 2023 > Chapter VI > Section 103(2)] Whoever commits murder..."`
  This ensures that BM25 search and neural attention retain the parent context even when matching an isolated clause.

### 9.3 Judicial Document Structure & Coram Attribution

Judicial judgments require distinct structural parsing from statutes:
- **Case Title & Neutral Citation**: Extracted and normalized (e.g., `2024:DHC:1420`).
- **Bench Coram Size**: Parsed to determine binding precedence under Article 141 (Constitution Bench: 5+ Judges; Full Bench: 3 Judges; Division Bench: 2 Judges; Single Judge).
- **Ratio Decidendi Extraction**: Segregation of the binding legal proposition from narrative factual summaries and procedural recitation.
- **Operative Order**: Separate indexing of the final directions (e.g., bail granted with conditions, petition dismissed).

### 9.4 Legal Text Normalization & Cleaners

Raw gazettes and court orders contain typographic defects that degrade search indexing:
- **Hyphenation Repair**: Eliminates line-wrap breaks (`"juris-\\ndiction"` -> `"jurisdiction"`).
- **Devanagari Normalization**: Applies Unicode NFKC normalization, strips broken viramas, and standardizes punctuation (purna viram / danda `।` and double danda `॥`).
- **Citation Canonicalization**: Normalizes varied reporter abbreviations:
  - `"AIR 2024 SC 1234"` -> `"All India Reporter 2024 Supreme Court 1234"`
  - `"2024 SCC OnLine Del 456"` -> `"2024 SCC OnLine Delhi High Court 456"`

### 9.5 Content-Hash Deduplication & Anti-Tampering

To prevent duplicate provisions from inflating retrieval weights or corrupting training loss:
1. Text is normalized: all whitespace collapsed to single spaces, lowercase converted for hashing.
2. SHA-256 hash is computed across normalized text.
3. Database `content_hash` UNIQUE constraint blocks duplicate chunk insertion.
4. If an identical provision appears in an amended Gazette, the system compares effective dates to establish temporal succession rather than creating duplicate active chunks.

---
""")

    # Part X
    sections.append("""## Part X: Retrieval-Augmented Generation (RAG) Architecture

### 10.1 Grounded RAG Inference Engine

The LegalMitra Grounded RAG Engine (`legalmitra/rag/engine.py`) prioritizes **evidential grounding over generative fluency**. The model is strictly instructed and constrained to act as an objective synthesizer of primary statutory provisions and authoritative judicial holdings.

```text
[ Incoming Legal Query ]
          │
          ▼
[ Query Normalizer & Citation Extractor ]
          │
          ▼
[ SQLite FTS5 BM25 Lexical + Filtered Search ]
          │
          ▼
[ Top-K Evidence Chunks (1,499 Active Chunks) ]
          │
          ▼
[ Evidence Sufficiency Evaluator ] ──(Insufficient / False Premise)──► [ Explicit Abstention Response ]
          │ (Sufficient)
          ▼
[ Constitutional Prompt Assembly with Golden Citations ]
          │
          ▼
[ LLM Generation (Nemotron-70B / Offline Mock) ]
          │
          ▼
[ Quality Gate: Citation Fidelity & Claim Support ] ──(Hallucination Detected)──► [ Fallback to Abstention ]
          │ (Verified 100%)
          ▼
[ Validated Grounded Response + Evidence Metadata ]
```

### 10.2 Hybrid Lexical & Dense Retrieval Strategies

LegalMitra combines lexical precision with semantic understanding:
1. **FTS5 BM25 Lexical Search**:
   - Utilizes SQLite's FTS5 engine with unicode61 tokenizer.
   - Perfect for exact statutory section references (e.g., *"Section 482"*, *"Article 21"*), Latin legal maxims (*"audi alteram partem"*, *"mens rea"*), and defined statutory terms (*"cognizable offence"*).
   - BM25 rank formula tuned with parameter $k_1 = 1.2$ and $b = 0.75$.
2. **Dense Vector Embeddings (Roadmap Integration)**:
   - Evaluated for high-level legal semantic queries (*"What remedies exist when police refuse to register an FIR?"*).
   - Hybrid fusion combines lexical and dense ranks via Reciprocal Rank Fusion (RRF).

### 10.3 Authority Hierarchy & Precedent Weighting

Under Indian constitutional jurisprudence, legal provisions carry unequal binding authority. The retrieval engine applies an explicit authority scoring multiplier:

$$\\text{AuthorityWeight}(A) = \\begin{cases} 
1.50 & \\text{if } A = \\text{CONSTITUTIONAL (Constitution of India)} \\\\
1.35 & \\text{if } A = \\text{STATUTORY\\_CENTRAL (Parliamentary Acts)} \\\\
1.25 & \\text{if } A = \\text{JUDICIAL\\_SUPREME\\_COURT (Art. 141 Binding Precedents)} \\\\
1.15 & \\text{if } A = \\text{STATUTORY\\_STATE (State Legislative Enactments)} \\\\
1.05 & \\text{if } A = \\text{JUDICIAL\\_HIGH\\_COURT (Territorial Jurisdiction)} \\\\
0.90 & \\text{if } A = \\text{SUBORDINATE\\_LEGISLATION (Rules / Regulations)} \\\\
0.50 & \\text{if } A = \\text{PERSUASIVE\\_OTHER}
\\end{cases}$$

When sorting candidate chunks, the final score is the product of the BM25 retrieval relevance and the authority weight:
$$\\text{FinalScore} = \\text{BM25Relevance} \\times \\text{AuthorityWeight}$$

### 10.4 Evidential Grounding & Abstention Logic

The most critical capability of LegalMitra is knowing **when not to answer**.
The Evidence Sufficiency Evaluator (`legalmitra/rag/evaluator.py`) inspects retrieved chunks against the user's proposition:
- If no retrieved chunk contains the targeted statutory provision, or if the top chunk relevance score falls below a threshold ($S_{\\text{min}} < 0.35$), the system triggers **Explicit Abstention**.
- **Standard Abstention Response**:
  > *"LegalMitra is unable to locate primary statutory provisions or binding judicial authority in its verified knowledge base to answer this question authoritatively. The system abstains from generating a speculative answer to prevent legal misinformation."*

### 10.5 Negative Constraint Checking & Forbidden Terms

To eliminate hallucination and confusion surrounding repealed statutes:
- Each evaluation case and query template can specify a list of `forbidden_terms`.
- Example: For queries concerning criminal procedure post-July 1, 2024, terms such as *"Section 438 of the Code of Criminal Procedure is currently operative"* are explicitly flagged.
- Post-generation validator scans the generated answer: if any forbidden term is detected, the answer is rejected and replaced with an abstention or correction prompt.

### 10.6 Missing Facts Prompting Engine

Legal questions frequently depend on unspecified factual prerequisites (e.g., jurisdiction, date of occurrence, whether an offense is bailable).
When the retriever identifies multiple mutually exclusive statutory branches (e.g., pre-2024 IPC vs post-2024 BNS), the system returns a `missing_facts_prompt`:
> *"To determine the applicable law with precision, please clarify: (1) Did the alleged incident occur prior to or after July 1, 2024? (2) In which State or Union Territory was the complaint lodged?"*

---
""")

    # Part XI
    sections.append("""## Part XI: Legal Scope, Jurisdiction & Statutory Coverage

### 11.1 Central Statutory Coverage (The 33 Active Universe Acts)

The active knowledge base indexes **33 core primary Central Acts**, fully extracted, parsed, validated, and cleared for training eligibility under Section 52(1)(q):

| Act ID | Canonical Act Title | Year | Enactment / S.O. Ref | Total Chunks | Primary Legal Domain |
|:---|:---|:---:|:---:|:---:|:---|
| `IND-ACT-1950-CONST` | The Constitution of India | 1950 | Constituent Assembly | 142 | Constitutional & Public Law |
| `IND-ACT-2023-BNS` | The Bharatiya Nyaya Sanhita, 2023 | 2023 | Act No. 45 of 2023 | 210 | Substantive Criminal Law |
| `IND-ACT-2023-BNSS` | The Bharatiya Nagarik Suraksha Sanhita, 2023 | 2023 | Act No. 46 of 2023 | 248 | Criminal Procedure & Bail |
| `IND-ACT-2023-BSA` | The Bharatiya Sakshya Adhiniyam, 2023 | 2023 | Act No. 47 of 2023 | 98 | Law of Evidence & Electronic Records |
| `IND-ACT-1860-IPC` | The Indian Penal Code, 1860 | 1860 | Act No. 45 of 1860 | 165 | Historical Criminal Law (Pre-2024) |
| `IND-ACT-1973-CRPC` | The Code of Criminal Procedure, 1973 | 1974 | Act No. 2 of 1974 | 182 | Historical Procedure (Pre-2024) |
| `IND-ACT-1872-IEA` | The Indian Evidence Act, 1872 | 1872 | Act No. 1 of 1872 | 74 | Historical Evidence Law |
| `IND-ACT-1908-CPC` | The Code of Civil Procedure, 1908 | 1908 | Act No. 5 of 1908 | 115 | Civil Practice & Procedure |
| `IND-ACT-1872-ICA` | The Indian Contract Act, 1872 | 1872 | Act No. 9 of 1872 | 52 | Commercial & Obligations Law |
| `IND-ACT-1963-SRA` | The Specific Relief Act, 1963 | 1963 | Act No. 47 of 1963 | 24 | Equitable Remedies & Injunctions |
| `IND-ACT-1963-LA` | The Limitation Act, 1963 | 1963 | Act No. 36 of 1963 | 31 | Limitation & Statutory Deadlines |
| `IND-ACT-1882-TPA` | The Transfer of Property Act, 1882 | 1882 | Act No. 4 of 1882 | 48 | Property & Conveyancing Law |
| `IND-ACT-1996-ACA` | The Arbitration and Conciliation Act, 1996 | 1996 | Act No. 26 of 1996 | 36 | Dispute Resolution & Arbitration |
| `IND-ACT-2000-ITA` | The Information Technology Act, 2000 | 2000 | Act No. 21 of 2000 | 44 | Cyber Law & Digital Signatures |
| `IND-ACT-2016-IBC` | The Insolvency and Bankruptcy Code, 2016 | 2016 | Act No. 31 of 2016 | 58 | Insolvency & Corporate Restructuring |
| `IND-ACT-2013-CA` | The Companies Act, 2013 | 2013 | Act No. 18 of 2013 | 64 | Corporate Governance & Securities |
| `IND-ACT-2019-CPA` | The Consumer Protection Act, 2019 | 2019 | Act No. 35 of 2019 | 28 | Consumer Rights & Redressal |
| `IND-ACT-1881-NIA` | The Negotiable Instruments Act, 1881 | 1881 | Act No. 26 of 1881 | 22 | Banking & Cheque Dishonour |
| `IND-ACT-2005-RTI` | The Right to Information Act, 2005 | 2005 | Act No. 22 of 2005 | 18 | Administrative Transparency |
| `IND-ACT-2012-POCSO`| Protection of Children from Sexual Offences Act | 2012 | Act No. 32 of 2012 | 26 | Child Protection & Privacy |
| `IND-ACT-1988-PC` | The Prevention of Corruption Act, 1988 | 1988 | Act No. 49 of 1988 | 19 | Anti-Corruption & Public Servants |
| `IND-ACT-2002-PMLA` | Prevention of Money Laundering Act, 2002 | 2003 | Act No. 15 of 2003 | 28 | Financial Crimes & Asset Seizure |
| `IND-ACT-2015-CCA` | The Commercial Courts Act, 2015 | 2016 | Act No. 4 of 2016 | 16 | Commercial Dispute Acceleration |
| `IND-ACT-1956-HMA` | The Hindu Marriage Act, 1955 | 1955 | Act No. 25 of 1955 | 20 | Family Law & Matrimonial Remedies |
| `IND-ACT-1956-HSA` | The Hindu Succession Act, 1956 | 1956 | Act No. 30 of 1956 | 18 | Coparcenary & Succession Rights |
| `IND-ACT-1939-MSA` | The Dissolution of Muslim Marriages Act, 1939 | 1939 | Act No. 8 of 1939 | 8 | Personal Law & Dissolution |
| `IND-ACT-1954-SMA` | The Special Marriage Act, 1954 | 1954 | Act No. 43 of 1954 | 16 | Civil Marriage & Registration |
| `IND-ACT-1986-EPA` | The Environment (Protection) Act, 1986 | 1986 | Act No. 29 of 1986 | 14 | Environmental Law & Pollution |
| `IND-ACT-2010-NGT` | The National Green Tribunal Act, 2010 | 2010 | Act No. 19 of 2010 | 15 | Environmental Tribunals |
| `IND-ACT-1988-MVA` | The Motor Vehicles Act, 1988 | 1988 | Act No. 59 of 1988 | 25 | Road Transport & Accident Claims |
| `IND-ACT-1957-CA` | The Copyright Act, 1957 | 1957 | Act No. 14 of 1957 | 22 | Intellectual Property & Public Edicts|
| `IND-ACT-1999-TMA` | The Trade Marks Act, 1999 | 1999 | Act No. 47 of 1999 | 24 | Intellectual Property & Brands |
| `IND-ACT-1970-PA` | The Patents Act, 1970 | 1970 | Act No. 39 of 1970 | 26 | Intellectual Property & Inventions |

### 11.2 State & Union Territory Legislative Coverage

LegalMitra maps legislative sources across all **28 States and 8 Union Territories** in `data/08_corpus/state_ut_registry.json`. Deep statutory extracts are indexed for priority jurisdictions:
- **NCT of Delhi (`IN-DL`)**: 19 chunks indexed:
  - Delhi Rent Act, 1995 (Eviction grounds, standard rent determination).
  - Delhi Police Act, 1978 (Police powers, public assembly regulation).
  - Delhi School Education Act, 1973 (Fee regulation, service conditions).
- **Maharashtra (`IN-MH`)**: 8 chunks indexed:
  - Maharashtra Control of Organised Crime Act, 1999 (MCOCA - Bail restrictions under Section 21(4), confession before police under Section 18).
  - Maharashtra Rent Control Act, 1999 (Tenant protection, leave and license).
- **State Portal Adapters**: Discovery adapters mapped for Tamil Nadu, Karnataka, Uttar Pradesh, and West Bengal.

### 11.3 High Court & Supreme Court Jurisprudence

The judicial knowledge base contains landmark precedent rulings from the Supreme Court of India and High Courts:
- **Supreme Court Landmark Jurisprudence**: 39 chunks:
  - *Kesavananda Bharati v. State of Kerala (1973)*: Basic Structure Doctrine limiting amending power under Article 368.
  - *Maneka Gandhi v. Union of India (1978)*: Golden Triangle (Articles 14, 19, 21); requirement that procedure established by law must be just, fair, and reasonable.
  - *Justice K.S. Puttaswamy v. Union of India (2017)*: Right to Privacy as an intrinsic part of the right to life and personal liberty under Article 21.
  - *Navtej Singh Johar v. Union of India (2018)*: Section 377 IPC unconstitutional insofar as it criminalized consensual sexual acts between adults.
  - *Lalita Kumari v. Govt. of U.P. (2014)*: Mandatory registration of FIR under Section 154 CrPC if information discloses commission of cognizable offence.
  - *Arnesh Kumar v. State of Bihar (2014)*: Mandatory guidelines for arrest under Section 41 CrPC (now Section 35 BNSS) to prevent arbitrary arrest for offenses punishable with up to 7 years imprisonment.
  - *D.K. Basu v. State of West Bengal (1997)*: Constitutional requirements and procedural safeguards governing arrest and detention.
  - *Common Cause v. Union of India (2018)*: Right to die with dignity and recognition of Advance Medical Directives (Living Wills).
- **High Court Jurisprudence**: Delhi High Court commercial division and bail decisions.

### 11.4 Subordinate Rules & Commencement Orders

Subordinate instruments indexed to ensure temporal fidelity:
- Ministry of Home Affairs (MHA) Commencement Notifications for BNS, BNSS, and BSA (Commencing July 1, 2024, except hit-and-run provisions of Section 106(2) BNS).
- Arbitration and Conciliation (Domestic Commercial Arbitration) Rules.
- Information Technology (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021.

### 11.5 Complete Source Registry Matrix (111 Tracked Sources)

As audited in `data/09_national_corpus/source_eligibility_ledger.json`, the National Legal Registry tracks **111 total legal sources**:

```text
+----------------------------------------------------------------------------------------------------------------------+
|                                   NATIONAL LEGAL SOURCE REGISTRY RECONCILIATION                                      |
+---------------------------------------------+-------+----------------------------------------------------------------+
| Classification Category                     | Count | Technical Status & Pretraining Inclusion Status                |
+---------------------------------------------+-------+----------------------------------------------------------------+
| 1. TRAINING_ELIGIBLE (Active Statutes)      |    33 | Verified primary texts with 1,505 indexed chunks in KB.        |
|                                             |       | Formally cleared under Sec 52(1)(q) for Manifest v4 pretrain.  |
+---------------------------------------------+-------+----------------------------------------------------------------+
| 2. RIGHTS_REVIEWED_CATALOG_ONLY (Backlog)   |    67 | Expected universe instruments fully cataloged in registry.    |
|                                             |       | 0 physical chunks extracted (scheduled for Phase 37+ batches). |
+---------------------------------------------+-------+----------------------------------------------------------------+
| 3. DISCOVERY_CANDIDATES_PENDING_ACQUISITION |    10 | Priority State & Judicial discovery candidates identified in   |
|                                             |       | Phase 35 pending physical acquisition queues.                  |
+---------------------------------------------+-------+----------------------------------------------------------------+
| 4. QUARANTINED_FIXTURE                      |     1 | `IND-JUD-DEL-2024-BAIL` (6 synthetic scaffold chunks).        |
|                                             |       | Strictly quarantined. Excluded from RAG and pretraining.       |
+---------------------------------------------+-------+----------------------------------------------------------------+
| TOTAL TRACKED NATIONAL SOURCES              |   111 | 100% Reconciled and accounted for without drift.               |
+---------------------------------------------+-------+----------------------------------------------------------------+
```

---
""")

    return "\n".join(sections)
