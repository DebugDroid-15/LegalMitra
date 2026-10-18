"""
README Builder - Part I to Part III:
- Root Header, Badges, Classifications & Ethical Warnings
- Exhaustive Table of Contents
- Part I: Project Identity, Governance & Ethical Scope
- Part II: Executive Summary & Dual-Track System Architecture
- Part III: Architectural Diagrams & Subsystem Boundaries
"""

def generate_header() -> str:
    return """# LegalMitra — National Indian Legal AI Intelligence Platform

```text
========================================================================================================================
                                     LEGALMITRA — PROPRIETARY & CONFIDENTIAL
========================================================================================================================
  CLASSIFICATION : PROPRIETARY & CONFIDENTIAL — STRICTLY RESTRICTED ACCESS
  OWNED BY       : Team Shatrujeet
  CORE AUTHORS   : Amar Khera | Ananya Rout | Lucky Kumar | Omm Prakash Sahoo
  ORGANIZATION   : LegalMitra AI Research Group / Team Shatrujeet
  CREATED        : October 2026
  LICENSE        : Team Shatrujeet Proprietary Software License (All Rights Reserved)
  STATUS         : Phase 36 Complete (315 Tests Passing | 111 Tracked Sources | 1,505 Chunks | 1.07M Param Model)
  NOTICE         : STRICTLY PRIVATE. NOT FOR PUBLIC RELEASE. NOT TO BE COPIED, SCRAPED, OR DISTRIBUTED.
========================================================================================================================
```

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary%20%26%20Confidential-red.svg?logo=lock&logoColor=white)](LICENSE)
[![PyTorch 2.0+](https://img.shields.io/badge/PyTorch-2.0%2B%20%7C%20CUDA-EE4C2C.svg?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Test Suite](https://img.shields.io/badge/Test%20Suite-315%20Passed%20%7C%200%20Failed%20%7C%202%20Deselected-brightgreen.svg?logo=pytest&logoColor=white)]()
[![Corpus Scale](https://img.shields.io/badge/Corpus-1%2C505%20Chunks%20%7C%20111%20Sources-gold.svg?logo=database&logoColor=white)]()
[![Benchmark v9](https://img.shields.io/badge/Benchmark%20v9-96%20Cases%20%7C%2015%20Categories-purple.svg?logo=checkmarx&logoColor=white)]()
[![Tokenizer](https://img.shields.io/badge/Tokenizer%20v2-Bilingual%20BPE%20%282%2C048%20Vocab%29-blueviolet.svg)]()
[![Original Model](https://img.shields.io/badge/Original%20Model-1.07M%20Causal%20Transformer-orange.svg)]()
[![Advocate Review](https://img.shields.io/badge/Advocate%20Review-40%20Pending%20%7C%200%25%20Hallucinated-teal.svg)]()
[![Freeze Snapshot](https://img.shields.io/badge/Freeze%20Integrity-100%25%20Bitwise%20Verified%20%286%2F6%29-success.svg?logo=shield&logoColor=white)]()
[![FastAPI](https://img.shields.io/badge/API-FastAPI%200.104%2B%20Hardened-009688.svg?logo=fastapi&logoColor=white)](http://localhost:8000)

> [!CAUTION]
> **PROPRIETARY & CONFIDENTIAL ASSET**: This software, including its neural architectures, retrieval algorithms, SQLite/FTS5 knowledge bases, structural parsing schemas, design tokens, trained tokenizer merges, checkpoint weights, and curated datasets, is the exclusive intellectual property of **Team Shatrujeet** (Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo). Created in October 2026, it is strictly private software not licensed for public use, open-source redistribution, reverse engineering, academic plagiarism, or commercial exploitation.

> [!IMPORTANT]
> **LEGAL ACCREDITATION & ETHICS DISCLAIMER**: LegalMitra is an advanced legal knowledge engineering platform for legal practitioners, jurists, advocates, and judicial data engineers. While automated extraction, Pydantic schemas, and quality gates guarantee **syntactic fidelity, source citation, and temporal grounding**, they do **not** substitute for formal legal representation or opinions by an enrolled advocate under the Advocates Act, 1961. No attorney-client relationship is created by the operation or consumption of this system.

---
"""


def generate_table_of_contents() -> str:
    return """## Table of Contents

- [Part I: Project Identity, Governance & Ethical Scope](#part-i-project-identity-governance--ethical-scope)
  - [1.1 Mission Statement & Problem Formulation](#11-mission-statement--problem-formulation)
  - [1.2 Institutional Background & Team Credits](#12-institutional-background--team-credits)
  - [1.3 Legal Disclaimers & Statutory Boundaries](#13-legal-disclaimers--statutory-boundaries)
  - [1.4 Statutory Public Edict Doctrine (Section 52(1)(q))](#14-statutory-public-edict-doctrine-section-521q)
  - [1.5 Bilingual Authenticity Mandate (Article 394A & Official Languages Act)](#15-bilingual-authenticity-mandate-article-394a--official-languages-act)
  - [1.6 Explicit Non-Goals & System Limitations](#16-explicit-non-goals--system-limitations)
- [Part II: Executive Summary & Dual-Track System Architecture](#part-ii-executive-summary--dual-track-system-architecture)
  - [2.1 The Dual-Track Technical Paradigm](#21-the-dual-track-technical-paradigm)
  - [2.2 Why Generic LLMs Fail on Indian Jurisprudence](#22-why-generic-llms-fail-on-indian-jurisprudence)
  - [2.3 Core Performance & Scale Metrics (Phase 36 Verified)](#23-core-performance--scale-metrics-phase-36-verified)
  - [2.4 Technical Innovation Summary](#24-technical-innovation-summary)
- [Part III: Architectural Diagrams & Subsystem Boundaries](#part-iii-architectural-diagrams--subsystem-boundaries)
  - [3.1 End-to-End Grounded-RAG Inference Architecture](#31-end-to-end-grounded-rag-inference-architecture)
  - [3.2 7-State National Legal Ingestion & Parsing Pipeline](#32-7-state-national-legal-ingestion--parsing-pipeline)
  - [3.3 Bilingual Foundation Model Pretraining & Tokenizer Pipeline](#33-bilingual-foundation-model-pretraining--tokenizer-pipeline)
  - [3.4 Two-Tier Advocate Review & Quarantine Boundary](#34-two-tier-advocate-review--quarantine-boundary)
  - [3.5 Strict Physical Database Segregation](#35-strict-physical-database-segregation)
- [Part IV: Exhaustive Repository Anatomy & Module Reference](#part-iv-exhaustive-repository-anatomy--module-reference)
  - [4.1 Package Architecture Overview](#41-package-architecture-overview)
  - [4.2 Core Subpackage (`legalmitra.core`)](#42-core-subpackage-legalmitracore)
  - [4.3 Ingestion Subpackage (`legalmitra.ingestion`)](#43-ingestion-subpackage-legalmitraingestion)
  - [4.4 Corpus Subpackage (`legalmitra.corpus`)](#44-corpus-subpackage-legalmitracorpus)
  - [4.5 Extraction Subpackage (`legalmitra.extraction`)](#45-extraction-subpackage-legalmitraextraction)
  - [4.6 Normalization Subpackage (`legalmitra.normalization`)](#46-normalization-subpackage-legalmitranormalization)
  - [4.7 Knowledge Subpackage (`legalmitra.knowledge`)](#47-knowledge-subpackage-legalmitraknowledge)
  - [4.8 RAG & Retrieval Subpackage (`legalmitra.rag`)](#48-rag--retrieval-subpackage-legalmitrarag)
  - [4.9 LLM Subpackage (`legalmitra.llm`)](#49-llm-subpackage-legalmitrallm)
  - [4.10 Validation & Quality Gate Subpackage (`legalmitra.validation`)](#410-validation--quality-gate-subpackage-legalmitravalidation)
  - [4.11 Caselaw & Precedent Subpackage (`legalmitra.caselaw`)](#411-caselaw--precedent-subpackage-legalmitracaselaw)
  - [4.12 Temporal Law Subpackage (`legalmitra.temporal`)](#412-temporal-law-subpackage-legalmitratemporal)
  - [4.13 Schemas Subpackage (`legalmitra.schemas`)](#413-schemas-subpackage-legalmitraschemas)
  - [4.14 Review Subpackage (`legalmitra.review`)](#414-review-subpackage-legalmitrareview)
  - [4.15 Evaluation Subpackage (`legalmitra.evaluation`)](#415-evaluation-subpackage-legalmitraevaluation)
  - [4.16 Dataset Subpackage (`legalmitra.dataset`)](#416-dataset-subpackage-legalmitradataset)
  - [4.17 Generation Subpackage (`legalmitra.generation`)](#417-generation-subpackage-legalmitrageneration)
  - [4.18 Web Subpackage (`legalmitra.web`)](#418-web-subpackage-legalmitraweb)
  - [4.19 Research Subsystem (`research.original_model`)](#419-research-subsystem-researchoriginal_model)
  - [4.20 Operational Scripts Catalog (`scripts/`)](#420-operational-scripts-catalog-scripts)
  - [4.21 Test Suite Catalog (`tests/`)](#421-test-suite-catalog-tests)
  - [4.22 Data Directory Layout (`data/`)](#422-data-directory-layout-data)
- [Part V: Environment Setup, Hardware Profiles & Installation Guide](#part-v-environment-setup-hardware-profiles--installation-guide)
  - [5.1 System Prerequisites & Supported Platforms](#51-system-prerequisites--supported-platforms)
  - [5.2 Hardware Profiling & Compute Tiers](#52-hardware-profiling--compute-tiers)
  - [5.3 Clean Virtual Environment Setup](#53-clean-virtual-environment-setup)
  - [5.4 Step-by-Step Dependency Installation](#54-step-by-step-dependency-installation)
  - [5.5 Verification & Smoke Testing](#55-verification--smoke-testing)
- [Part VI: Configuration & Environment Variables Reference](#part-vi-configuration--environment-variables-reference)
  - [6.1 Configuration Philosophy](#61-configuration-philosophy)
  - [6.2 Complete Environment Variables Matrix](#62-complete-environment-variables-matrix)
  - [6.3 Offline vs Online Evaluation Configuration](#63-offline-vs-online-evaluation-configuration)
  - [6.4 Rate Limiting & Security Settings](#64-rate-limiting--security-settings)
- [Part VII: Production Web API Reference](#part-vii-production-web-api-reference)
  - [7.1 API Architecture & OpenAPI Specification](#71-api-architecture--openapi-specification)
  - [7.2 System Probes (`/api/v1/health`, `/api/v1/ready`)](#72-system-probes-apiv1health-apiv1ready)
  - [7.3 Legal Chat Engine (`/api/v1/chat`)](#73-legal-chat-engine-apiv1chat)
  - [7.4 Conversation Session Management (`/api/v1/conversations`)](#74-conversation-session-management-apiv1conversations)
  - [7.5 User & Advocate Feedback Loop (`/api/v1/feedback`)](#75-user--advocate-feedback-loop-apiv1feedback)
  - [7.6 HTTP Error Matrix & Status Codes](#76-http-error-matrix--status-codes)
- [Part VIII: Database Architecture & Data Storage Reference](#part-viii-database-architecture--data-storage-reference)
  - [8.1 Physical Segregation Principle](#81-physical-segregation-principle)
  - [8.2 Knowledge Base Schema (`data/legalmitra_kb.db`)](#82-knowledge-base-schema-datalegalmitra_kbdb)
  - [8.3 Full-Text Search Virtual Table (`legal_chunks_fts`)](#83-full-text-search-virtual-table-legal_chunks_fts)
  - [8.4 User Session & Feedback Schema (`data/conversations.db`)](#84-user-session--feedback-schema-dataconversationsdb)
  - [8.5 Performance Tuning, Indexes & Integrity Auditing](#85-performance-tuning-indexes--integrity-auditing)
- [Part IX: Legal Knowledge Ingestion & Corpus Engineering](#part-ix-legal-knowledge-ingestion--corpus-engineering)
  - [9.1 7-Stage State Machine Lifecycle](#91-7-stage-state-machine-lifecycle)
  - [9.2 Statutory Hierarchy & Provision Decomposition](#92-statutory-hierarchy--provision-decomposition)
  - [9.3 Judicial Document Structure & Coram Attribution](#93-judicial-document-structure--coram-attribution)
  - [9.4 Legal Text Normalization & Cleaners](#94-legal-text-normalization--cleaners)
  - [9.5 Content-Hash Deduplication & Anti-Tampering](#95-content-hash-deduplication--anti-tampering)
- [Part X: Retrieval-Augmented Generation (RAG) Architecture](#part-x-retrieval-augmented-generation-rag-architecture)
  - [10.1 Grounded RAG Inference Engine](#101-grounded-rag-inference-engine)
  - [10.2 Hybrid Lexical & Dense Retrieval Strategies](#102-hybrid-lexical--dense-retrieval-strategies)
  - [10.3 Authority Hierarchy & Precedent Weighting](#103-authority-hierarchy--precedent-weighting)
  - [10.4 Evidential Grounding & Abstention Logic](#104-evidential-grounding--abstention-logic)
  - [10.5 Negative Constraint Checking & Forbidden Terms](#105-negative-constraint-checking--forbidden-terms)
  - [10.6 Missing Facts Prompting Engine](#106-missing-facts-prompting-engine)
- [Part XI: Legal Scope, Jurisdiction & Statutory Coverage](#part-xi-legal-scope-jurisdiction--statutory-coverage)
  - [11.1 Central Statutory Coverage (The 33 Active Universe Acts)](#111-central-statutory-coverage-the-33-active-universe-acts)
  - [11.2 State & Union Territory Legislative Coverage](#112-state--union-territory-legislative-coverage)
  - [11.3 High Court & Supreme Court Jurisprudence](#113-high-court--supreme-court-jurisprudence)
  - [11.4 Subordinate Rules & Commencement Orders](#114-subordinate-rules--commencement-orders)
  - [11.5 Complete Source Registry Matrix (111 Tracked Sources)](#115-complete-source-registry-matrix-111-tracked-sources)
- [Part XII: Original Legal Language Model Research Track](#part-xii-original-legal-language-model-research-track)
  - [12.1 Motivation for an Original Indian Legal Foundation Model](#121-motivation-for-an-original-indian-legal-foundation-model)
  - [12.2 Causal Transformer Architecture & PyTorch Implementation](#122-causal-transformer-architecture--pytorch-implementation)
  - [12.3 Exact Parameter Accounting (1,069,824 Parameters)](#123-exact-parameter-accounting-1069824-parameters)
  - [12.4 Empirical Pretraining Metrics & Loss Curves](#124-empirical-pretraining-metrics--loss-curves)
  - [12.5 Chinchilla Scaling Heuristic & The 615x Token Deficit](#125-chinchilla-scaling-heuristic--the-615x-token-deficit)
- [Part XIII: Custom Bilingual Tokenizer (Tokenizer v2) Architecture](#part-xiii-custom-bilingual-tokenizer-tokenizer-v2-architecture)
  - [13.1 Limitations of Standard Tokenizers on Indian Legal Text](#131-limitations-of-standard-tokenizers-on-indian-legal-text)
  - [13.2 Byte-Pair Encoding Implementation & Byte Fallback](#132-byte-pair-encoding-implementation--byte-fallback)
  - [13.3 Vocabulary Construction & 1,811 Learned Merges](#133-vocabulary-construction--1811-learned-merges)
  - [13.4 Comparative Empirical Audit: Tokenizer v1 vs v2](#134-comparative-empirical-audit-tokenizer-v1-vs-v2)
- [Part XIV: Training Data Governance, Split Integrity & Quarantine](#part-xiv-training-data-governance-split-integrity--quarantine)
  - [14.1 Dataset Manifest v4 Architecture](#141-dataset-manifest-v4-architecture)
  - [14.2 Source-Grouped Partitioning & Zero-Leakage Guarantee](#142-source-grouped-partitioning--zero-leakage-guarantee)
  - [14.3 Authentic Hindi Data Integration](#143-authentic-hindi-data-integration)
  - [14.4 Strict Quarantine Architecture (`IND-JUD-DEL-2024-BAIL`)](#144-strict-quarantine-architecture-ind-jud-del-2024-bail)
- [Part XV: Evaluation Framework, Benchmark v1–v9 & Metric Contracts](#part-xv-evaluation-framework-benchmark-v1v9--metric-contracts)
  - [15.1 Evaluation Philosophy & The Benchmark Suite Evolution](#151-evaluation-philosophy--the-benchmark-suite-evolution)
  - [15.2 Benchmark v9 Specification (96 Cases)](#152-benchmark-v9-specification-96-cases)
  - [15.3 The 15 Legal Question Evaluation Categories](#153-the-15-legal-question-evaluation-categories)
  - [15.4 Metric Contracts & Quality Gates](#154-metric-contracts--quality-gates)
  - [15.5 Automated Failure Attribution Engine](#155-automated-failure-attribution-engine)
- [Part XVI: Security, Privacy & Compliance Architecture](#part-xvi-security-privacy--compliance-architecture)
  - [16.1 Threat Modeling & Adversarial Defense](#161-threat-modeling--adversarial-defense)
  - [16.2 SSRF Protection & Hop-by-Hop Redirect Inspection](#162-ssrf-protection--hop-by-hop-redirect-inspection)
  - [16.3 Rate Limiting, Payload Capping & Injection Prevention](#163-rate-limiting-payload-capping--injection-prevention)
  - [16.4 Privacy Compliance & POCSO Redaction Engine](#164-privacy-compliance--pocso-redaction-engine)
  - [16.5 Immutable Audit Logging & Telemetry](#165-immutable-audit-logging--telemetry)
- [Part XVII: Automated Testing & Continuous Verification Reference](#part-xvii-automated-testing--continuous-verification-reference)
  - [17.1 Test Strategy & Pytest Architecture](#171-test-strategy--pytest-architecture)
  - [17.2 Inventory of Test Suites (38 Test Modules)](#172-inventory-of-test-suites-38-test-modules)
  - [17.3 Freeze Integrity Test Suite (`verify_freeze.py`)](#173-freeze-integrity-test-suite-verify_freezepy)
  - [17.4 Review Package Verification Suite (`verify_review_packages.py`)](#174-review-package-verification-suite-verify_review_packagespy)
  - [17.5 Reproducing the Complete Test Suite (315 Passing Tests)](#175-reproducing-the-complete-test-suite-315-passing-tests)
- [Part XVIII: Operational Runbooks & Developer Workflows](#part-xviii-operational-runbooks--developer-workflows)
  - [18.1 Runbook 1: Ingesting a New Central or State Statute](#181-runbook-1-ingesting-a-new-central-or-state-statute)
  - [18.2 Runbook 2: Indexing High Court / Supreme Court Precedents](#182-runbook-2-indexing-high-court--supreme-court-precedents)
  - [18.3 Runbook 3: Executing Evaluation Benchmarks](#183-runbook-3-executing-evaluation-benchmarks)
  - [18.4 Runbook 4: Pretraining & Benchmarking the Original Model](#184-runbook-4-pretraining--benchmarking-the-original-model)
  - [18.5 Runbook 5: Generating & Verifying Advocate Review Packages](#185-runbook-5-generating--verifying-advocate-review-packages)
  - [18.6 Runbook 6: Database Maintenance & Vacuum Procedures](#186-runbook-6-database-maintenance--vacuum-procedures)
- [Part XIX: Comprehensive Troubleshooting & Diagnostics Playbook](#part-xix-comprehensive-troubleshooting--diagnostics-playbook)
  - [19.1 CUDA & PyTorch Hardware Diagnostics](#191-cuda--pytorch-hardware-diagnostics)
  - [19.2 Database Lock & SQLite Corruptions](#192-database-lock--sqlite-corruptions)
  - [19.3 FTS5 Search & Query Syntax Anomalies](#193-fts5-search--query-syntax-anomalies)
  - [19.4 SSRF False Positives & Network Timeouts](#194-ssrf-false-positives--network-timeouts)
  - [19.5 Tokenizer Encoding & Byte-Fallback Issues](#195-tokenizer-encoding--byte-fallback-issues)
  - [19.6 Freeze & Review Package SHA-256 Mismatches](#196-freeze--review-package-sha-256-mismatches)
  - [19.7 Windows Console Unicode & Encoding Errors](#197-windows-console-unicode--encoding-errors)
  - [19.8 30 Operational Issue Resolution Scenarios](#198-30-operational-issue-resolution-scenarios)
- [Part XX: Historical Milestone Log (Phases 1 through 36)](#part-xx-historical-milestone-log-phases-1-through-36)
  - [20.1 Inception & Foundation (Phases 1 to 8)](#201-inception--foundation-phases-1-to-8)
  - [20.2 Phase 9 Review Snapshot Freeze](#202-phase-9-review-snapshot-freeze)
  - [20.3 Knowledge Base & Structural Normalization (Phases 10 to 18)](#203-knowledge-base--structural-normalization-phases-10-to-18)
  - [20.4 National Corpus & Legislative Expansion (Phases 19 to 25)](#204-national-corpus--legislative-expansion-phases-19-to-25)
  - [20.5 High Court Precedents & Security Hardening (Phases 26 to 30)](#205-high-court-precedents--security-hardening-phases-26-to-30)
  - [20.6 Original Foundation Model Track (Phases 31 to 36)](#206-original-foundation-model-track-phases-31-to-36)
- [Part XXI: Governance, Legal Risk Register & Open Ambiguities](#part-xxi-governance-legal-risk-register--open-ambiguities)
  - [21.1 The 6 Phase 9 Frozen Legal Ambiguities](#211-the-6-phase-9-frozen-legal-ambiguities)
  - [21.2 The 40 Advocate Review Candidates Register](#212-the-40-advocate-review-candidates-register)
  - [21.3 Synthetic Scaffold Quarantine Protocol](#213-synthetic-scaffold-quarantine-protocol)
  - [21.4 Criminal Law Transition Governance (IPC/CrPC/IEA vs BNS/BNSS/BSA)](#214-criminal-law-transition-governance-ipccrpciea-vs-bnsbnssbsa)
- [Part XXII: Deployment, Operations & Production Readiness](#part-xxii-deployment-operations--production-readiness)
  - [22.1 Standalone Local Server Mode](#221-standalone-local-server-mode)
  - [22.2 High-Throughput Production Architecture](#222-high-throughput-production-architecture)
  - [22.3 PostgreSQL & Vector DB Migration Strategy](#223-postgresql--vector-db-migration-strategy)
  - [22.4 Monitoring, Alerting & Health Check Probes](#224-monitoring-alerting--health-check-probes)
- [Part XXIII: Complete Reference Tables & Appendices](#part-xxiii-complete-reference-tables--appendices)
  - [Appendix A: Complete API Endpoint Matrix](#appendix-a-complete-api-endpoint-matrix)
  - [Appendix B: Database Tables & Columns Master Catalog](#appendix-b-database-tables--columns-master-catalog)
  - [Appendix C: Environment Variables Master Catalog](#appendix-c-environment-variables-master-catalog)
  - [Appendix D: CLI Scripts & Utility Commands Master Catalog](#appendix-d-cli-scripts--utility-commands-master-catalog)
  - [Appendix E: HTTP Status Codes & Error Messages Catalog](#appendix-e-http-status-codes--error-messages-catalog)
  - [Appendix F: Exhaustive Indian Legal Terminology Glossary](#appendix-f-exhaustive-indian-legal-terminology-glossary)
- [Part XXIV: Contribution Guidelines, Code Style & Integrity Standards](#part-xxiv-contribution-guidelines-code-style--integrity-standards)
  - [24.1 Branching Strategy & Git Workflows](#241-branching-strategy--git-workflows)
  - [24.2 Commit Message Standards](#242-commit-message-standards)
  - [24.3 Coding Conventions & Linting](#243-coding-conventions--linting)
  - [24.4 Invariant Enforcement & Pre-Commit Checks](#244-invariant-enforcement--pre-commit-checks)
- [Part XXV: Intellectual Property, Team Attribution & Future Roadmap](#part-xxv-intellectual-property-team-attribution--future-roadmap)
  - [25.1 Team Shatrujeet Ownership & Authorship](#251-team-shatrujeet-ownership--authorship)
  - [25.2 Proprietary License Terms](#252-proprietary-license-terms)
  - [25.3 Third-Party Component Attributions](#253-third-party-component-attributions)
  - [25.4 Future Roadmap: Milestones B through E](#254-future-roadmap-milestones-b-through-e)

---
"""


def generate_part_01() -> str:
    return """## Part I: Project Identity, Governance & Ethical Scope

### 1.1 Mission Statement & Problem Formulation

LegalMitra represents an original, sovereign engineering initiative dedicated to resolving the profound reliability, provenance, and grounding challenges that plague artificial intelligence when applied to the Indian Legal System. 

The Indian legal landscape is uniquely complex:
1. **Statutory Scale & Heterogeneity**: Over 800 central acts, tens of thousands of state statutes across 28 States and 8 Union Territories, hundreds of thousands of subordinate rules, regulations, statutory orders, and gazette notifications.
2. **The 2024 Criminal Law Transition**: The simultaneous enactment of the Bharatiya Nyaya Sanhita, 2023 (BNS), the Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS), and the Bharatiya Sakshya Adhiniyam, 2023 (BSA), replacing the century-old Indian Penal Code, 1860 (IPC), Code of Criminal Procedure, 1973 (CrPC), and Indian Evidence Act, 1872 (IEA). Navigating non-retroactivity under Article 20(1) of the Constitution while referencing active provisions requires strict temporal discrimination.
3. **Bilingual Diglossia**: Under Article 394A of the Constitution and Section 5(1) of the Official Languages Act, 1963, authoritative legal texts exist in both English and Hindi. General commercial language models exhibit severe token fragmentation and hallucination when dealing with Devanagari legal formulations.
4. **Binding Precedent Hierarchy**: The constitutional mandate of Article 141 of the Constitution establishes Supreme Court rulings as binding law, while High Courts exercise supervisory and binding jurisdiction within their territorial borders under Articles 226 and 227.

Commercial generative models generate fluent but non-existent case citations, confuse repealed provisions with active law, and synthesize legally invalid premises. LegalMitra solves this through a dual-track architecture combining **strictly grounded evidential retrieval (RAG)** with an **original, randomly initialized bilingual causal transformer** trained directly on authenticated primary sources.

### 1.2 Institutional Background & Team Credits

LegalMitra was conceptualized, designed, implemented, and verified by **Team Shatrujeet**, an elite group of AI researchers, legal engineers, and software architects:

```text
+----------------------------------------------------------------------------------------------------------------------+
|                                            TEAM SHATRUJEET — CORE CREDITS                                            |
+----------------------+-----------------------------+-----------------------------------------------------------------+
| Member Name          | Institutional Role          | Primary Technical Focus Area                                    |
+----------------------+-----------------------------+-----------------------------------------------------------------+
| Amar Khera           | Team Lead / AI Systems      | Grounded RAG, Pretraining Transformer, Tokenizer v2, Chinchilla |
| Ananya Rout          | Senior Legal Data Architect | Statutory Hierarchy, Indian Code Schemas, Pydantic Gates        |
| Lucky Kumar          | Infrastructure Engineer     | FTS5 Knowledge Base, SSRF Hardening, DB Segregation, High Perf  |
| Omm Prakash Sahoo    | UI/UX & Review Operations   | Web Architecture, Advocate Review Pipelines, Verification QA    |
+----------------------+-----------------------------+-----------------------------------------------------------------+
| Project Repository   | https://github.com/DebugDroid-15/LegalMitra                                                   |
| Legal Classification | PROPRIETARY AND CONFIDENTIAL (Team Shatrujeet All Rights Reserved)                            |
| Operating System     | Windows / Linux / macOS (Cross-platform Python 3.11+)                                         |
+----------------------------------------------------------------------------------------------------------------------+
```

### 1.3 Legal Disclaimers & Statutory Boundaries

> [!WARNING]
> **NO LEGAL REPRESENTATION OR ADVICE**: LegalMitra is an AI research, information indexing, and evidential retrieval platform. It does not provide legal representation, legal opinions, legal advocacy, or formal legal advice. 

The software operates under strict statutory constraints:
1. **The Advocates Act, 1961**: Under Section 29 and Section 33 of the Advocates Act, 1961, only advocates enrolled on the roll of a State Bar Council are entitled to practice the profession of law in India. LegalMitra is an analytical tool designed to assist enrolled advocates and judicial scholars, not an autonomous legal entity.
2. **Absence of Attorney-Client Privilege**: Use of LegalMitra or interactions with its APIs does not create an attorney-client relationship, privileged communication, or fiduciary duty.
3. **Mandatory Human-in-the-Loop Verification**: LegalMitra requires all generated statutory analyses, caselaw syntheses, and citation references to be verified against certified copies or official Gazette publications by qualified advocates before reliance in judicial proceedings.

### 1.4 Statutory Public Edict Doctrine (Section 52(1)(q))

All legal source materials ingested, parsed, and utilized within LegalMitra are governed by the **Public Edict Doctrine** under Indian copyright law:

```text
Section 52(1)(q) of the Copyright Act, 1957 (Act No. 14 of 1957):
"The following acts shall not constitute an infringement of copyright, namely:—
(q) the reproduction or publication of—
    (i) any matter which has been published in any Official Gazette except an Act of a Legislature;
    (ii) any Act of a Legislature subject to the condition that such Act is reproduced or published together with any
         commentary thereon or other matter;
    (iii) the report of any committee, commission, council, board or other like body appointed by the Government if such
          report has been laid on the Table of the Legislature, unless the reproduction or publication of such report is
          prohibited by the Government;
    (iv) any judgment or order of a court, tribunal or other judicial authority, unless the reproduction or publication of
          such judgment or order is prohibited by the court, the tribunal or other judicial authority, as the case may be."
```

Furthermore, in *Eastern Book Company v. D.B. Modak (2008) 1 SCC 1*, the Supreme Court of India held that raw judicial orders, judgments, and statutory text reside firmly in the public domain, free from copyright monopoly, guaranteeing that the reproduction of official legal texts for research, retrieval, and automated analysis is lawful.

### 1.5 Bilingual Authenticity Mandate (Article 394A & Official Languages Act)

LegalMitra adheres to the constitutional and statutory framework governing multilingual legal documentation in the Republic of India:

1. **Article 394A of the Constitution of India**:
   - The President of India shall cause to be published under his authority the translation in the Hindi language of the Constitution, and every amendment thereof.
   - The translation shall have the same meaning as the original English text and shall be deemed to be the authoritative text thereof in the Hindi language.
2. **Section 5(1) of the Official Languages Act, 1963**:
   - A translation in Hindi published under the authority of the President in the Official Gazette of any Central Act or of any Ordinance promulgated by the President, or of any order, rule, regulation or by-law issued under any Central Act, shall be deemed to be the authoritative text thereof in Hindi.

Accordingly, LegalMitra's corpus engineering pipeline strictly rejects machine-translated Hindi text for pretraining or evidential citation, requiring authentic authoritative Hindi texts sourced directly from official government gazettes and India Code repositories.

### 1.6 Explicit Non-Goals & System Limitations

To preserve technical integrity and legal defensibility, LegalMitra enforces explicit negative boundaries:
- **No Hallucinated Citations**: The system will explicitly refuse to answer or output an abstention signal rather than fabricate a citation or synthesize a provision that does not exist in the primary knowledge base.
- **No Synthetic Training Bleed**: Synthetic scaffold fixtures (such as `IND-JUD-DEL-2024-BAIL`) are strictly quarantined and mathematically forbidden from entering the pretraining manifests or active RAG index.
- **No Unreviewed Auto-Approval**: The 40 candidate records in the advocate review register remain strictly in `pending_legal_review` status until physical, enrolled advocates inspect and sign off on each item.
- **No Cross-Split Leakage**: Pretraining, validation, and test datasets are partitioned at the document-family level, guaranteeing zero intra-document or cross-split contamination.

---
"""


def generate_part_02() -> str:
    return """## Part II: Executive Summary & Dual-Track System Architecture

### 2.1 The Dual-Track Technical Paradigm

LegalMitra implements a bifurcated engineering architecture designed to provide immediate, legally grounded operational utility while advancing long-term sovereign AI research:

```text
+----------------------------------------------------------------------------------------------------------------------+
|                                         LEGALMITRA DUAL-TRACK ARCHITECTURE                                           |
+----------------------------------------------------------+-----------------------------------------------------------+
| TRACK 1: PRODUCTION GROUNDED-RAG SYSTEM                  | TRACK 2: ORIGINAL FOUNDATION-MODEL RESEARCH               |
+----------------------------------------------------------+-----------------------------------------------------------+
| • High-precision evidential retrieval                    | • 100% Original decoder-only causal transformer           |
| • SQLite + FTS5 full-text search with BM25 ranking       | • Built from scratch in PyTorch (zero pretrained weights) |
| • Pydantic-validated statutory schemas                   | • Trained from random weight initialization (N(0, 0.02))  |
| • 8 Pre-indexing and post-retrieval Quality Gates        | • Custom bilingual Byte-Pair Encoding (BPE) Tokenizer v2  |
| • Explicit abstention on unanswerable/false premises     | • 2,048 Vocabulary size with Devanagari script merges     |
| • Strict temporal point-in-time applicability engine     | • Source-grouped splits guaranteeing zero leakage         |
| • Hardened FastAPI web interface with session isolation  | • Rigorous parameter accounting & Chinchilla scaling gate |
+----------------------------------------------------------+-----------------------------------------------------------+
```

### 2.2 Why Generic LLMs Fail on Indian Jurisprudence

Mainstream foundation models (e.g., Llama, GPT, Claude, Mistral) fail critically when applied to Indian law due to fundamental domain characteristics:

1. **Severe Token Fragmentation**: Standard tokenizers allocate less than 2% of their vocabulary to Indic scripts. A single Hindi legal word such as *'अधिनियम'* (Adhiniyam / Act) or *'न्यायालय'* (Nyayalaya / Court) is fragmented into 4 to 8 byte tokens, inflating sequence lengths, exhausting context windows, and inducing severe semantic drift.
2. **Temporal Confusion (2024 Criminal Transition)**: When asked about statutory bail or murder in 2025, generic models conflate Section 302 of the Indian Penal Code with Section 103 of the Bharatiya Nyaya Sanhita, or apply repealed CrPC procedural rules to offenses committed post-July 1, 2024.
3. **Phantom Citation Fabrication**: Generic models suffer from high hallucination rates on case citations, fabricating realistic-looking citations like *"AIR 2019 SC 4512"* or *"2021 SCC OnLine Del 3120"* that do not correspond to real judgments.
4. **Failure to Abstain**: Commercial models attempt to answer even when presented with factually incomplete or legally absurd premises (e.g., filing a writ under Article 32 before a Sessions Judge). LegalMitra's evidential grounding engine detects missing facts and actively prompts the user for clarification.

### 2.3 Core Performance & Scale Metrics (Phase 36 Verified)

All metrics reported herein have been independently reproduced and verified against the actual repository checkout at commit `db588a5` (Phase 36 baseline):

```text
+----------------------------------------------------------------------------------------------------------------------+
|                                   LEGALMITRA VERIFIED REPOSITORY BENCHMARK METRICS                                   |
+----------------------------------------------+---------------------------+-------------------------------------------+
| Dimension / Metric                           | Measured Value            | Verification Source / Script              |
+----------------------------------------------+---------------------------+-------------------------------------------+
| Automated Test Suite Status                  | 315 Passed, 2 Deselected  | `pytest -q` (48.15s runtime)               |
| Phase 9 Frozen Artifacts Integrity           | 6 of 6 Bitwise Identical  | `python scripts/verify_freeze.py`         |
| Advocate Review Candidates Status            | 40 Pending Legal Review   | `python scripts/verify_review_packages.py`|
| Total Indexed Knowledge Chunks               | 1,505 Stored Chunks       | `data/legalmitra_kb.db` (legal_chunks)    |
| Active Retrievable Chunks                    | 1,499 Active Chunks       | Excluding 6 quarantined scaffold chunks   |
| National Source Registry Coverage            | 111 Tracked Sources       | `unified_source_registry.json`            |
| Training-Eligible Primary Sources            | 33 Indexed Statutes       | Section 52(1)(q) Cleared Primary Texts    |
| Rights-Reviewed Catalog Backlog              | 67 Cataloged Instruments  | 0 chunks extracted (inventory phase)      |
| Priority Discovery Candidates                | 10 Instruments Pending    | State & Judicial acquisition queue        |
| Quarantined Synthetic Scaffolds              | 1 Scaffold (6 chunks)     | `IND-JUD-DEL-2024-BAIL` isolated          |
| Evaluation Benchmark v9 Scale                | 96 Cases / 15 Categories  | `data/20_evaluation/evaluation_cases_v9`  |
| Benchmark v8 Historical Accuracy             | 88 of 88 Passed (100%)    | `data/19_evaluation/manifest_v8.json`     |
| Golden Citation Recall                       | 100% Across Benchmark v8  | Zero fabricated legal citations           |
| Claim Grounding Support                      | 668 of 669 Claims (99.85%)| Grounding validation quality gate         |
| Original Transformer Parameters              | 1,069,824 Parameters      | `research/original_model/model.py`        |
| Pretraining Convergence (50 steps)           | Loss: 7.6468 -> 5.0069    | `phase35_1m_baseline_regression.pt`       |
| Validation Loss Delta                        | Val Loss: 7.6464 -> 5.6607| Loss delta: -1.9858 (Exact Match repro)   |
| Pretraining Training Throughput              | 82,671 Tokens / Second    | CUDA GeForce RTX 3050 Laptop GPU          |
| Tokenizer v2 Vocabulary Scale                | 2,048 Tokens / 1,811 Merges| `research/original_model/tokenizer_v2.json`|
| Tokenizer v2 vs v1 Compression Ratio         | 40.8% Token Reduction     | 2.11 tokens/word vs 3.56 tokens/word      |
| Tokenizer v2 Hindi Unique Token Activation   | 190 Unique Tokens (9.28%) | 13.5x Increase over v1 (14 tokens / 1.37%)|
| Usable Pretraining Tokens (Manifest v4)      | 342,965 Usable Tokens     | 334,348 English | 8,617 Authentic Hindi   |
| Chinchilla Scaling Deficit                   | 615x Token Deficit        | 21.5M tokens needed for 1.07M parameters  |
+----------------------------------------------+---------------------------+-------------------------------------------+
```

### 2.4 Technical Innovation Summary

1. **Constitutional Modernism Design**: The web interface employs an authoritative Google Stitch theme built around Deep Constitutional Navy (`#0A192F`), Antique Parchment Ivory (`#F8F9FA`), and Legal Saffron Gold (`#C5A059`), communicating institutional credibility.
2. **Complete Separation of State**: Absolute isolation between the read-only evidential knowledge base (`data/legalmitra_kb.db`) and the read-write user session database (`data/conversations.db`), eliminating race conditions and security contamination.
3. **SSRF-Hardened Ingestion**: Multi-tier security engine featuring recursive DNS resolution, private IP range blocking, loopback rejection, hop-by-hop redirect inspection, and strict payload size capping.
4. **Mathematical Zero-Leakage Splitting**: Custom deterministic source-grouped partitioner ensuring that entire acts, chapters, or judgment corams are assigned monolithically to either train, validation, or test sets.

---
"""


def generate_part_03() -> str:
    return """## Part III: Architectural Diagrams & Subsystem Boundaries

### 3.1 End-to-End Grounded-RAG Inference Architecture

The following sequence diagram outlines the exact execution flow of a user query submitted through the Web API down to the retrieval, evidential grounding, and response generation layers:

```mermaid
sequenceDiagram
    autonumber
    actor User as Legal Practitioner / Advocate
    participant Web as FastAPI Application (legalmitra.web.app)
    participant Sec as Security & Rate Limiter (InMemoryRateLimiter)
    participant Store as Session Store (data/conversations.db)
    participant RAG as RAG Retrieval Engine (legalmitra.rag.engine)
    participant KB as Knowledge Base (data/legalmitra_kb.db + FTS5)
    participant Val as Grounding & Quality Gate (legalmitra.validation)
    participant LLM as Legal Generation Provider (Mock / Nemotron)

    User->>Web: POST /api/v1/chat (query, act_filter, section_filter, limit)
    Web->>Sec: check_rate_limit(client_ip)
    alt Rate limit exceeded (> 30 req/min)
        Sec-->>Web: HTTP 429 Too Many Requests
        Web-->>User: Rate limit response JSON
    else Allowed
        Sec-->>Web: OK
    end

    Web->>Store: get_or_create_conversation(conv_id)
    Web->>Store: append_user_message(conv_id, query)

    Web->>RAG: answer_legal_query(query, act_filter, section_filter, limit)
    RAG->>KB: search_chunks_fts(normalized_query, limit)
    KB-->>RAG: List[LegalChunk] (verbatim text, authority, citations)

    RAG->>Val: evaluate_evidence_sufficiency(chunks, query)
    alt Insufficient Evidence or False Legal Premise
        Val-->>RAG: AbstentionSignal(reason="Insufficient primary evidence")
        RAG-->>Web: ChatResponse(answer="Abstaining...", sufficiency="insufficient")
    else Sufficient Primary Evidence
        Val-->>RAG: EvidenceSufficiencyReport(status="sufficient")
        RAG->>LLM: generate_grounded_answer(prompt, evidence_context)
        LLM-->>RAG: RawGeneratedAnswer
        RAG->>Val: validate_citations_and_claims(RawGeneratedAnswer, chunks)
        Val-->>RAG: ValidatedAnswer(citations_verified=True, claims_supported=True)
        RAG-->>Web: ChatResponse(answer, citations, evidence, telemetry)
    end

    Web->>Store: append_assistant_message(conv_id, response)
    Web-->>User: 200 OK (JSON with answer, evidence items, disclaimer)
```

### 3.2 7-State National Legal Ingestion & Parsing Pipeline

Every piece of legislation, gazette notification, and judicial precedent transitions through a strictly governed 7-stage finite state machine (FSM):

```mermaid
stateDiagram-v2
    [*] --> DISCOVERED: Portal Audit & Scraping Discovery
    DISCOVERED --> REGISTERED: Metadata Validation & Entry into Registry
    REGISTERED --> ACQUIRED: Cryptographic Retrieval & SHA-256 Hashing
    ACQUIRED --> PARSED: Structural Parsing (Section, Proviso, Explanation)
    PARSED --> AUTHENTICITY_VERIFIED: Cross-Reference with Official Gazette / Court Seal
    AUTHENTICITY_VERIFIED --> RIGHTS_REVIEWED: Section 52(1)(q) Copyright Act Audit
    RIGHTS_REVIEWED --> TRAINING_ELIGIBLE: Cleared for Active Pretraining & RAG Indexing
    
    DISCOVERED --> REJECTED: Malformed Metadata / Unofficial Source
    ACQUIRED --> QUARANTINED: Synthetic Scaffold / Test Fixture Detected
    PARSED --> REJECTED: Structural Extraction Failure / Corrupted PDF
    AUTHENTICITY_VERIFIED --> QUARANTINED: Unverified Text / Disputed Seal
    RIGHTS_REVIEWED --> QUARANTINED: Proprietary / Copyrighted Commentary Included
```

### 3.3 Bilingual Foundation Model Pretraining & Tokenizer Pipeline

The engineering workflow for developing, training, and evaluating LegalMitra's original decoder-only causal transformer:

```mermaid
flowchart TD
    subgraph SOURCEDATA["1. Sovereign Data Ingestion"]
        S1["India Code Central Acts (English)"]
        S2["Authoritative Gazette Acts (Hindi)"]
        S3["Supreme Court Landmark Judgments"]
        S4["High Court Division Bench Orders"]
    end

    subgraph PREPROCESSING["2. Tokenization & Partitioning"]
        CLEAN["Legal Text Normalization<br/>(Unicode NFKC, Devanagari Cleaners)"]
        TOK["IndianLegalTokenizerV2<br/>(2,048 Vocab, 1,811 Merges, Byte Fallback)"]
        SPLIT["Source-Grouped Partitioning<br/>(Zero Intra-Document Leakage)"]
        MANI["Dataset Manifest v4<br/>(Train: 304K tokens, Val: 3.9K, Test: 34.7K)"]
    end

    subgraph NEURAL["3. Causal Neural Architecture"]
        EMB["Token + Learned Positional Embeddings<br/>(d_model=128, max_seq_len=128/256)"]
        TRF["4x Transformer Decoder Blocks<br/>• Multi-Head Causal Self-Attention (4 heads)<br/>• MLP Expansion (d_ff=512)<br/>• LayerNorm & Residual Connections"]
        HEAD["Tied Output Projection Head<br/>(Vocab Size 2,048)"]
    end

    subgraph EVALUATION["4. Verification & Scaling Gate"]
        LOSS["Loss Tracking & Checkpointing<br/>(Train Loss: 5.0069, Val Loss: 5.6607)"]
        CHINCH["Chinchilla Scaling Heuristic Audit<br/>(Current: 342K tokens vs Needed: 21.5M tokens)"]
        GATE{"Scaling Gate Decision"}
        PROCEED["Approved for Scaling (Post-Corpus Expansion)"]
        HALT["Pretraining Scale Halted (615x Token Deficit)"]
    end

    SOURCEDATA --> CLEAN
    CLEAN --> TOK
    TOK --> SPLIT
    SPLIT --> MANI
    MANI --> EMB
    EMB --> TRF
    TRF --> HEAD
    HEAD --> LOSS
    LOSS --> CHINCH
    CHINCH --> GATE
    GATE -- "Corpus >= 21.5M Tokens" --> PROCEED
    GATE -- "Corpus < 21.5M Tokens" --> HALT
```

### 3.4 Two-Tier Advocate Review & Quarantine Boundary

The isolation protocol that separates unreviewed candidate examples and synthetic test fixtures from production models:

```mermaid
flowchart LR
    subgraph PRODUCTION_CORE["Production System Boundary"]
        KB[("Knowledge Base<br/>legalmitra_kb.db")]
        MANIFEST["Pretraining Manifest<br/>dataset_manifest_v4.json"]
        RAG_SERV["Active RAG Engine"]
    end

    subgraph REVIEW_ISOLATION["Advocate Review Boundary (Zero Model Bleed)"]
        REG["Review Tracking Register<br/>(40 Records: All pending_legal_review)"]
        PKGA["Package A: Pilot 20 Frozen Snapshot<br/>(SHA-256 Bitwise Locked)"]
        PKGB["Package B: Batch 01 Candidate Expansion<br/>(20 Real-World Examples)"]
    end

    subgraph STRICT_QUARANTINE["Strict Quarantine Vault"]
        SCAF["IND-JUD-DEL-2024-BAIL<br/>(6 Synthetic Scaffold Chunks)"]
        WALL["Mathematical Quarantine Filter<br/>(Strictly Excluded by UUID)"]
    end

    PKGA -.->|Pending Human Advocate Review| REG
    PKGB -.->|Pending Human Advocate Review| REG
    REG -- "BLOCKED: Requires Enrolled Advocate Sign-off" --> PRODUCTION_CORE
    
    SCAF --> WALL
    WALL -- "FORBIDDEN FROM INGESTION" --> KB
    WALL -- "FORBIDDEN FROM TRAINING" --> MANIFEST
```

### 3.5 Strict Physical Database Segregation

To guarantee absolute data isolation, prevent concurrency deadlocks, and defend against privilege escalation, LegalMitra enforces physical separation of databases:

```text
+-------------------------------------------------------+  +-------------------------------------------------------+
|            DATA / LEGALMITRA_KB.DB                    |  |               DATA / CONVERSATIONS.DB                 |
+-------------------------------------------------------+  +-------------------------------------------------------+
| • Access Mode : Strictly READ-ONLY in Web App         |  | • Access Mode : Read-Write in Web Application         |
| • Purpose     : Authoritative Legal Knowledge Storage |  | • Purpose     : User Sessions, History, Feedback Loops|
| • Security    : Immutable to client web requests      |  | • Security    : Isolated by generated UUID4 session ID|
| • Tables:                                             |  | • Tables:                                             |
|   - sources            (59 registered legal sources)  |  |   - conversations  (User session state tracking)      |
|   - legal_chunks       (1,505 structural text chunks) |  |   - messages       (User queries & assistant answers) |
|   - legal_chunks_fts   (FTS5 Virtual Full-Text Index) |  |   - feedback       (Advocate & user accuracy reviews) |
|   - cases              (16 judicial case records)     |  |                                                       |
|   - judicial_documents (Court orders & transcripts)   |  |                                                       |
|   - hearing_events     (Procedural event timeline)    |  |                                                       |
+-------------------------------------------------------+  +-------------------------------------------------------+
                           ^                                                          ^
                           |                                                          |
             [ RAG Retrieval Engine ]                                      [ Session Store Manager ]
                           \                                                          /
                            \                                                        /
                             +------------------------------------------------------+
                             |               FastAPI Web Application                |
                             +------------------------------------------------------+
```

---
"""
