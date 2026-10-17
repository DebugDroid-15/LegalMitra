# PHASE 21 — END-TO-END CASE RESEARCH & RETRIEVAL VERIFICATION
## Grounded Passage Retrieval, Dated Procedural Timelines & Statutory Continuity

**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Repository:** `https://github.com/DebugDroid-15/LegalMitra`  
**Workspace:** `C:\PROJECTS\LegalMitra`  
**Owner:** Team Shatrujeet — Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo  
**Classification:** Proprietary and Confidential  
**Date:** October 2026  
**Status:** Ingested & Verified  

---

## 1. Executive Summary

Workstream Q mandates building and verifying an end-to-end legal research workflow across the judicial corpus. Given a case identifier, statutory citation, or legal question, LegalMitra resolves:
1. The court and case entity.
2. The exact judicial documents (final judgment, interim orders, notices).
3. Exact verbatim passages and numbered paragraphs without hallucination.
4. The dated chronological procedural timeline.
5. Linked statutory provisions and whether later decisions modified or overruled propositions.
6. Explicit identification of unavailable or unverified records.

---

## 2. End-to-End Test Scenarios

### Scenario 1: Cheque Dishonour Presumption & Standard of Proof
- **Query**: *Section 139 Negotiable Instruments Act reverse onus presumption*
- **Retrieved Decision**: `IND-JUD-SC-2010-RANGAPPA` (*Rangappa v. Sri Mohan*, (2010) 11 SCC 441).
- **Exact Passages**:
  - Para 26: Section 139 presumption includes existence of legally enforceable debt; *Krishna Janardhan Bhat* overruled to that extent.
  - Para 27: Reverse onus clause regulatory purpose.
  - Para 28: Standard of proof is preponderance of probabilities.
- **Precedent Graph Linkage**: Identifies `CASE-RANGAPPA` $\rightarrow$ `OVERRULES` $\rightarrow$ `CASE-KRISHNA-BHAT`.

### Scenario 2: Unstamped Arbitration Clause at Section 11 Referral Stage
- **Query**: *Arbitration agreement in unstamped contract enforceable Section 11*
- **Retrieved Decision**: `IND-JUD-SC-2023-ARBITRATION-STAMP` (*In Re: Interplay Between Arbitration Agreements & Stamp Act*, (2024) 6 SCC 1).
- **Exact Passages**:
  - Para 162: Deficiency in stamping is a curable defect; unstamped contract is not void ab initio.
  - Para 175: Competence-competence under Section 16 mandates referral court confine scrutiny to prima facie existence.
  - Para 224: Overrules *NN Global* (2023) 7 SCC 1 and *SMS Tea Estates* (2011) 14 SCC 66.

### Scenario 3: Procedural Timeline Reconstruction for Civil Appeal
- **Target Case**: `IN-SC-CA-2082-2018` (*Arjun Panditrao Khotkar v. Kailash Kushanrao Gorantyal*)
- **Reconstructed Timeline**:
  1. `2018-02-23`: Notice Order (`IND-ORD-SC-2018-CA2082-NOTICE`) issued on prayer for interim relief.
  2. `2018-02-23`: Hearing Event (`EVT-SC-2018-02-23`) admission hearing before Nariman & Sinha, JJ.
  3. `2019-07-26`: Reference Order (`IND-ORD-SC-2019-CA2082-REFERENCE`) referring conflict between *Shafhi Mohammad* and *Anvar P.V.* to larger bench.
  4. `2020-07-14`: Final Judgment (`IND-JUD-SC-2020-ARJUN-KHOTKAR`, 3-Judge Bench, 7 indexed chunks).

---

## 3. Privacy, Sensitive Matters & Quarantine Safeguards

1. **Synthetic Scaffold Exclusion**: `IND-JUD-DEL-2024-BAIL` remains strictly quarantined with `is_synthetic_scaffold = 1`. All RAG and case searches enforce `WHERE is_synthetic_scaffold = 0`.
2. **POCSO and Sensitive Family Disputes**: The schema includes `is_sensitive: bool` and `redaction_reason: Optional[str]`. Records involving sexual offences or minors anonymize parties to "Victim / Child / State" pursuant to Section 33(7) POCSO Act and Supreme Court guidelines in *Nipun Saxena v. Union of India*.
3. **Database Separation**: Zero leakage into `data/conversations.db`. Authentication and user session data remain fully segregated from the judicial knowledge base.

