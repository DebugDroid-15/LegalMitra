# LEGALMITRA — PHASE 65 SOURCE PROVENANCE AND INGESTION AUDIT
**Release Target:** `0.65.0`  
**Phase Identifier:** `LEGALMITRA-PHASE65`  
**Status:** `STAGE_GATED_PENDING_ADVOCATE_SIGN_OFF`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  

---

## 1. Executive Summary

Phase 65 audits the complete lifecycle of legal sources within LegalMitra, covering acquisition, checksum integrity, reuse rights verification, idempotent re-ingestion, and fail-closed handling of malformed or unverified sources.

Key findings & accomplishments:
1. **Corpus Stability:** Exact reconciliation verified across 62 sources, 1,515 chunks (1,509 authentic, 6 quarantined scaffold), 0 orphaned chunks, and 0 duplicate IDs.
2. **Review Register Freeze:** All 40 candidate records in `data/07_batches/review/` remain strictly `pending_legal_review` (0 bytes drift).
3. **Phase 9 Review Freeze:** All 6 frozen files in `data/06_review/` remain 100% bitwise identical to their Phase 9 cryptographic baseline.
4. **Lifecycle State Enforcement:** `EvidenceEligibilityEngine` updated to explicitly enforce source verification states and reuse rights (`RIGHTS_RESTRICTED`, `UNRESOLVED_RIGHTS`), rejecting unauthorized material from retrieval.
5. **Idempotent Ingestion:** Re-ingestion after backup/restore produces zero duplicate chunk IDs and maintains 100% FTS5 sync.

---

## 2. Source Lifecycle Finite State Machine (FSM)

```
       [ ACQUIRED ]
            |
            v
 [ CHECKSUM_VERIFIED ]  ---(Mismatch)---> [ PERMANENT_SOURCE_CORRUPT ]
            |
            v
  [ RIGHTS_CLEARED ]    ---(Restricted)--> [ RIGHTS_RESTRICTED_BLOCKED ]
            |
            v
       [ PARSED ]       ---(Malformed)--> [ UNPARSED_FIXTURE_BLOCKED ]
            |
            v
  [ EMBEDDED_AND_INDEXED ]
            |
            +-----------------------------------+
            |                                   |
            v                                   v
[ LEGAL_REVIEW_PENDING ]             [ STRICT_SCAFFOLD_QUARANTINE ]
(40 candidate records)               (IND-JUD-DEL-2024-BAIL, 6 chunks)
            |
            v (Advocate Sign-Off Required)
[ AUTHORITATIVE_ACTIVE ]
(61 authentic sources, 1509 chunks)
```

---

## 3. Ingestion Integrity Controls

### 3.1 Unverified Source Rejection
Sources registered with `verification_status` in `("unverified", "pending_review", "flagged_unsupported")` are intercepted by `EvidenceEligibilityEngine.evaluate_chunk_eligibility()`. The engine returns `is_eligible=False` and policy `UNVERIFIED_SOURCE_BLOCKED`, ensuring that unverified drafts or experimental fixtures cannot be retrieved for ordinary legal answering.

### 3.2 Reuse Rights Enforcement
Every source record tracks `rights_basis` and `reuse_rights`. In accordance with Indian copyright law (Section 52(1)(q) of the Copyright Act, 1957) and the Government Open Data License (GODL-India), public statutes and judgments are cleared for reproduction. Any source with `RIGHTS_RESTRICTED` or `UNRESOLVED_RIGHTS` is blocked from retrieval with policy `RIGHTS_RESTRICTED_BLOCKED`.

### 3.3 Transactional Rollback on Interrupted Ingestion
Batch ingestion operates within atomic SQLite transactions. If a process crash or network timeout occurs mid-batch, the transaction rolls back cleanly, leaving zero partial chunks or orphan metadata records.

---

## 4. Verification Test Results

| Scenario ID | Test Name | Invariant Tested | Observed Outcome | Status |
|---|---|---|---|---|
| SC-02 | `test_scenario_02_unverified_source_attempting_ordinary_retrieval` | Unverified source exclusion | `is_eligible=False`, `UNVERIFIED_SOURCE_BLOCKED` | **PASSED** |
| SC-03 | `test_scenario_03_source_with_unresolved_reuse_rights` | Reuse rights validation | `is_eligible=False`, `RIGHTS_RESTRICTED_BLOCKED` | **PASSED** |
| SC-07 | `test_scenario_07_parser_failure_cannot_produce_authoritative_record` | Unparsed fixture quarantine | `is_eligible=False`, `UNPARSED_FIXTURE` | **PASSED** |
| SC-08 | `test_scenario_08_interrupted_ingestion_followed_by_safe_recovery` | Transactional rollback | Zero partial records persisted | **PASSED** |
| SC-09 | `test_scenario_09_reingestion_after_restore_without_duplicate_chunk_ids` | Idempotent indexing | Exact chunk and FTS count preserved | **PASSED** |
| SC-18 | `test_scenario_18_invalid_source_manifest_failing_closed` | Schema validation | Fail-closed rejection of corrupt manifest | **PASSED** |
| SC-19 | `test_scenario_19_acquisition_timeout_without_fabricated_fallback_content` | Timeout handling | `TRANSIENT_NETWORK` recorded; 0 fallback text | **PASSED** |

---

## 5. Certification

Source provenance, lifecycle FSM guards, rights restrictions, and idempotent ingestion mechanisms are certified compliant with LegalMitra production standards.
