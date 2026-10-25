# LegalMitra Phase 59 — Proposition Provenance Model Specification

**Release Version:** `0.59.0`  
**Phase Identifier:** `LEGALMITRA-PHASE59`  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Module:** `legalmitra.evaluation.provenance_model`  
**Timestamp:** `2026-10-25T17:35:00Z`

---

## 1. Executive Summary & Objective

In Phase 59, LegalMitra establishes an auditable, proposition-level provenance model that eliminates boolean collapse. Previously, retrieval and claim validation evaluated whether a claim was "supported" without maintaining the distinct lifecycle stages of the legal source document. 

The Phase 59 provenance model explicitly models twelve (12) discrete, non-collapsible evidence states across the evidentiary chain, connecting user propositions back to verified gazettes, official acts, and reported court judgments.

---

## 2. The 12 Non-Collapsible Evidence Lifecycle States

Every material legal assertion synthesized by LegalMitra must progress through sequential validation states:

| State Index | State Name | Legal Operational Definition | Invariant Constraint |
|:---:|:---|:---|:---|
| 1 | `SOURCE_REGISTERED` | Source entry exists in legal source catalog | Must have official enactment or citation identifier |
| 2 | `SOURCE_ACQUIRED` | Full text or gazette artifact acquired via authenticated ingest | Acquired from official legislative portal or law reporter |
| 3 | `SOURCE_PARSED` | Structure segmented into sections, sub-sections, schedules, orders | Zero parsing truncation; hierarchy preserved |
| 4 | `SOURCE_STRUCTURE_VALIDATED` | Cross-validated against official gazette or certified court copy | Hash and text structure match official publishing |
| 5 | `SOURCE_AUTHENTICITY_VERIFIED` | Cryptographic SHA-256 and publishing source verified | Rejects unverified or fabricated source identities |
| 6 | `SOURCE_INDEXED` | Chunked and embedded in verified `legalmitra_kb.db` | Strictly isolated from conversational database |
| 7 | `PASSAGE_RETRIEVABLE` | Relevant verbatim statutory or judicial passage located | Pinpoint section/sub-section or paragraph cited |
| 8 | `TEMPORALLY_APPLICABLE` | In force on inquiry evaluation date under closed interval | Evaluated under canonical `[effective_from, effective_until]` |
| 9 | `JURISDICTIONALLY_APPLICABLE` | Operative within territorial and forum boundaries | National or State jurisdiction verified |
| 10 | `SUBSTANTIVELY_SUPPORTS` | Proposition logically entailed by verbatim legal text | Prohibits contradiction or uncalibrated overstatement |
| 11 | `RIGHTS_CLEARED` | Public domain statute (Sec 52(1)(q)) or fair dealing | Precludes copyrighted third-party commercial synthesis |
| 12 | `ADVOCATE_REVIEWED` | Verified and signed off by advocate enrolled under Advocates Act, 1961 | Cannot be automated; human sign-off required |

---

## 3. Data Architecture: `LegalPropositionProvenance`

```python
@dataclass
class LegalPropositionProvenance:
    proposition_id: str
    issue_id: str
    user_query: str
    proposition_text: str
    source_id: str
    source_type: str  # CENTRAL_ACT, STATE_ACT, DELEGATED_RULES, JUDICIAL_PRECEDENT, CONSTITUTIONAL_PROVISION
    authority_title: str
    pinpoint_reference: str  # e.g., "Section 20A(1)", "Paragraph 42", "Article 226"
    evidence_states: List[EvidenceLifecycleState]
    highest_verified_state: EvidenceLifecycleState
    authenticity_status: AuthenticityStatus
    passage_locator: str
    verbatim_passage: str
    jurisdiction: str
    effective_from: Optional[str]
    effective_until: Optional[str]
    evaluation_date: Optional[str]
    temporal_applicability: bool
    legislative_status: str
    precedent_status: AuthorityLevel
    substantive_relation: SubstantiveRelation
    material_exceptions: List[str]
    prerequisite_dependencies: List[str]
    dependencies_satisfied: bool
    rights_status: RightsStatus
    human_review_required: bool
    review_notes: str
    audit_hash: str
```

---

## 4. Auditor Rules & Failure Mechanisms

The `PropositionProvenanceAuditor` enforces strict fail-closed constraints:
1. **Quarantine Isolation:** If `source_id` contains `IND-JUD-DEL-2024-BAIL` or synthetic scaffold markers, authenticity is forced to `SYNTHETIC_QUARANTINED` and the audit fails immediately.
2. **Prerequisite Sequentiality:** `SUBSTANTIVELY_SUPPORTS` cannot be claimed unless `PASSAGE_RETRIEVABLE`, `SOURCE_AUTHENTICITY_VERIFIED`, and `TEMPORALLY_APPLICABLE` are satisfied.
3. **Contradiction Alignment:** If `substantive_relation` is `CONTRADICTS`, `SUBSTANTIVELY_SUPPORTS` is disallowed.
4. **Pinpoint Precision:** Missing pinpoint references are flagged as audit defects.
