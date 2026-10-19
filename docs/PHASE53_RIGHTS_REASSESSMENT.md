# PHASE 53: RIGHTS REASSESSMENT & MODEL-TRAINING PROHIBITION

**Project:** LegalMitra  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Phase:** 53  

---

## 1. Legal Basis for Internal Knowledge Ingestion

Ingestion and chunking of official Indian legal enactments and judicial decisions are legally grounded in:
1. **Section 52(1)(q) of the Indian Copyright Act, 1957**: Specifically exempts the reproduction or publication of any matter published in any Official Gazette, judicial decisions, or parliamentary enactments.
2. **Government Open Data License (GODL-India)**: Grants permission to use and index public domain statutory texts for algorithmic retrieval.

## 2. Non-Negotiable Invariant: Foundation Model Training Prohibited

```
+----------------------------------------------------------------------------------+
|                     CRITICAL ARCHITECTURAL BOUNDARY                              |
|                                                                                  |
|  [PERMITTED]  Internal Knowledge-Base Retrieval (RAG)                            |
|  [PERMITTED]  Claim Validation & Verification Against Authentic Source Text      |
|  [PERMITTED]  Temporal & Jurisdictional Disentanglement                          |
|                                                                                  |
|  [STRICT NO-GO] Pretraining Foundation Large Language Models                    |
|  [STRICT NO-GO] Fine-Tuning Weights on Ingested Judgments/Statutes               |
|  [STRICT NO-GO] Commercial Re-Licensing of Primary Judicial Opinions             |
+----------------------------------------------------------------------------------+
```

All 62 registered sources in `data/22_central_legislation/source_rights_registry.json` have `foundation_model_training_prohibited = True`.
