# Phase 35 Source Registry Design & Lifecycle FSM Specification

**Project:** LegalMitra  
**Phase:** 35 — National Legal Data Engine, Source Verification & Corpus Scaling Infrastructure  
**Author:** Team Shatrujeet  
**Date:** 2026-10-18  
**Status:** VERIFIED  

---

## 1. Executive Summary

Phase 35 implements an auditable, deterministic Finite State Machine (FSM) governing the entire lifecycle of Indian legal sources in `legalmitra/corpus/source_registry_engine.py`. The fundamental design principle is that **a legal document does not become eligible for model pretraining merely because it was discovered, acquired, or indexed into a retrieval database**.

Instead, every document must progress through strict, verifiable state transitions, with immutable transition logs, SHA-256 content verification, and legal rights clearance under Section 52(1)(q) of the Indian Copyright Act, 1957.

---

## 2. FSM State Definitions & Transition Matrix

The registry implements the `SourceLifecycleState` enumeration:

```
DISCOVERED
   │
   ▼
REGISTERED
   │
   ▼
ACQUIRED ──────────► PARSE_FAILED (Terminal / Recovery)
   │                      │
   ▼                      ▼
 PARSED ◄─────────────────┘ (Upon parser patch)
   │
   ▼
AUTHENTICITY_VERIFIED
   │
   ▼
RIGHTS_REVIEWED ────► RIGHTS_UNRESOLVED
   │                      │
   ▼                      ▼
TRAINING_ELIGIBLE ◄───────┘ (Upon advocate rights review)
```

### Exceptional and Terminal States:
- **`QUARANTINED`**: Reserved for synthetic test fixtures (e.g. `IND-JUD-DEL-2024-BAIL`), corrupted files, or security anomalies. Strictly excludes records from pretraining and user retrieval.
- **`BLOCKED`**: Prohibited content, private records, non-authoritative commentary, or third-party proprietary materials.
- **`DUPLICATE`**: Identical legal instruments pointing to an established primary canonical entry.

### Enforced State Transitions Table

| Current State | Permitted Next States | Validation Enforcement |
|---|---|---|
| `DISCOVERED` | `REGISTERED`, `BLOCKED`, `DUPLICATE`, `QUARANTINED` | Rejects direct jumps to `ACQUIRED` or `TRAINING_ELIGIBLE` |
| `REGISTERED` | `ACQUIRED`, `BLOCKED`, `QUARANTINED` | Validates target URL syntax and issuing authority |
| `ACQUIRED` | `PARSED`, `PARSE_FAILED`, `QUARANTINED`, `BLOCKED` | Checks HTTP response size (<= 50MB) and content type |
| `PARSED` | `AUTHENTICITY_VERIFIED`, `BLOCKED`, `QUARANTINED` | Requires absence of FATAL parsing defects |
| `AUTHENTICITY_VERIFIED` | `RIGHTS_REVIEWED`, `RIGHTS_UNRESOLVED`, `BLOCKED` | Cross-references Gazette of India or certified court report |
| `RIGHTS_REVIEWED` | `TRAINING_ELIGIBLE`, `RIGHTS_UNRESOLVED`, `BLOCKED` | Confirms Section 52(1)(q) public edict exemption |
| `TRAINING_ELIGIBLE` | `RIGHTS_UNRESOLVED`, `QUARANTINED`, `BLOCKED` | Eligibility can be revoked if legal defects emerge |

Any attempt to execute an unauthorized transition raises `IllegalStateTransitionError` and halts execution.

---

## 3. Data Schema & Persistence

The registry is persisted in `data/09_national_corpus/unified_source_registry.json`. Each entry contains:

- `source_id`: Stable alphanumeric identifier (e.g., `IND-STAT-BNS-2023`).
- `official_title`: Canonical title of the Act, Rule, or Judgment.
- `issuing_authority`: Parliament of India, State Legislature, Supreme Court, or High Court.
- `source_url`: Validated URL from official government portal (e.g., `indiacode.nic.in`, `egazette.gov.in`).
- `source_type`: `statute`, `judgment`, `delegated_rule`, `gazette_notification`, `procedural_code`.
- `jurisdiction`: ISO-based legal jurisdiction code (`IN`, `IN-DL`, `IN-MH`, `IN-WB`, `IN-TN`, `IN-KA`).
- `language`: `en`, `hi`, or `bilingual`.
- `document_family`: `criminal_law`, `civil_procedure`, `constitutional_law`, `commercial`, etc.
- `current_state`: `SourceLifecycleState` enum value.
- `pretraining_eligible`: Boolean flag set to `True` strictly when `current_state == TRAINING_ELIGIBLE`.
- `rights_basis`: Legal foundation for reproduction (e.g. `Section 52(1)(q) Copyright Act 1957`).
- `content_hash`: SHA-256 digest of original raw text.
- `history`: Sequential list of state transition logs (timestamp, from_state, to_state, reason, actor).

---

## 4. Current Registry Verification Metrics

Audit of `data/09_national_corpus/unified_source_registry.json`:
- **Total Tracked Legal Sources:** 111 records.
- **Training Eligible Sources:** 33 records (fully indexed with verified chunks).
- **Discovered & Registered Candidates:** 10 national priority candidates.
- **Quarantined Sources:** Exactly 1 (`UNIV-SCAFFOLD-DEL-2024-BAIL`).
- **Expected / Historical Universe Records:** 67 records.
- **FSM State Transition Integrity:** 100% verified across all unit tests (`test_fsm_source_lifecycle_transitions`, `test_fsm_illegal_transition_rejection`, `test_fsm_quarantine_isolation`).
