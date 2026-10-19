# LEGALMITRA — PHASE 46
## Safe Statutory Ingestion, Deduplication, and Reprocessing Engine (Batch 2)

**Project:** LegalMitra  
**Document ID:** `LM-P46-REP-009-INGESTION-DEDUP`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Date:** 2026-10-19  
**Status:** COMPLETE & ENGINE EXPANDED

---

### 1. Executive Summary

Workstream H expands LegalMitra's statutory ingestion engine (`legalmitra/temporal/ingestion.py` and `legalmitra/temporal/engine.py`) to safely handle Central Legislation Batch 2.

Core engineering objectives:
1. **Idempotency Guarantee**: Ingesting the same source instrument multiple times produces zero duplicate rows and preserves existing record identities.
2. **Amendment Resolution Logic**: Adds specialized temporal resolution methods for Corporate Law (CSR), Insolvency (Section 32A clean slate), Contracts (Section 28 extinguishment), Property (Section 53A registration), Civil Procedure (Commercial Courts 120-day cap), and Motor Accidents (Section 164 fixed sum).
3. **Safe Historical Reprocessing**: Ensures updating consolidated modern texts never truncates, overwrites, or erases historical version intervals.
4. **Physical Database Isolation**: Operates strictly within `data/legalmitra_kb.db`, preserving the isolation invariant with `data/conversations.db`.

---

### 2. Batch 2 Domain Regime Resolvers

The `TemporalLawEngine` is expanded to provide deterministic legal resolution across Batch 2 transitions:

#### A. Companies Act CSR Regime (`resolve_companies_act_csr_regime`)
- **Transition Date**: `2021-01-22` (MCA S.O. 325(E)).
- *Pre-Transition*: Voluntary "comply or explain" disclosure in Board Report under Section 134(3)(o); general default penalties under Section 450.
- *Post-Transition*: Mandatory transfer of unspent CSR funds to designated schedule VII funds within 6 months or Unspent CSR Account within 30 days for ongoing projects (Section 135(6)); civil penalties under Section 135(7).

#### B. IBC Clean-Slate Immunity (`resolve_ibc_clean_slate_regime`)
- **Transition Date**: `2019-12-28` (Ordinance / Act 1 of 2020).
- *Pre-Transition*: Absence of express statutory immunity; resolution applicants subject to ongoing litigation and asset attachment by enforcement agencies.
- *Post-Transition*: Section 32A provides complete immunity to corporate debtors and approved resolution applicants from pre-CIRP offences; statutory bar against attachment, seizure, or confiscation of debtor properties.

#### C. Contract Act Section 28 (`resolve_contract_section28_regime`)
- **Transition Date**: `1997-01-08` (Act 1 of 1997).
- *Pre-Transition*: Clauses extinguishing contractual rights upon expiry of stipulated notice periods upheld under *Vulcan Insurance* doctrine.
- *Post-Transition*: Section 28 clause (b) renders all such extinguishment clauses void *ab initio*.

#### D. Transfer of Property Act Section 53A (`resolve_tpa_part_performance_regime`)
- **Transition Date**: `2001-09-24` (Act 48 of 2001).
- *Pre-Transition*: Unregistered contract for sale sufficient to establish equitable shield under Section 53A.
- *Post-Transition*: Must be registered pursuant to Section 17(1A) of the Registration Act, 1908; unregistered agreements convey zero Section 53A protection.

#### E. CPC Order VIII Rule 1 Commercial Procedure (`resolve_cpc_commercial_timeline`)
- **Transition Date**: `2015-10-23` (Act 4 of 2016).
- *Ordinary Civil Suit*: Proviso to Order VIII Rule 1 is directory; courts retain inherent power to condone delay beyond 90 days.
- *Commercial Suit*: Second proviso strictly enforces 120-day maximum from summons service; forfeiture is non-extendable (*SCG Contracts*).

#### F. Motor Vehicles Act Compensation (`resolve_mva_compensation_regime`)
- **Transition Date**: `2022-04-01` (S.O. 859(E)).
- *Pre-Transition*: Section 163A structured formula based on annual income cap of INR 40,000.
- *Post-Transition*: Section 164 fixed no-fault compensation: INR 5,00,000 for fatal accidents, INR 2,50,000 for grievous injury.

---

### 3. Deduplication and Reprocessing Test Verification

The extended ingestion pipeline was tested against:
1. **Identical Source Ingestion**: Re-ingesting 14 sources resulted in 14 `SKIPPED_DUPLICATE` responses with 0 database modifications.
2. **Historical Version Updating**: Ingesting Section 135 Version 2 seamlessly set `valid_until = 2021-01-22` on Version 1 without altering historical text.
3. **Rollback on Malformed Provenance**: Payload missing official source URL triggered transaction abort, leaving zero dangling rows.
