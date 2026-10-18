# Phase 29: Precedent Knowledge Graph Integrity & Overruling Analysis
**Project:** LegalMitra — Indian Legal Research and Assistance Platform  
**Owner:** Team Shatrujeet (Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo)  
**Classification:** Proprietary and Confidential  
**Date:** October 2026  
**Phase:** 29  

---

## 1. Graph Architecture & Precedent Modeling

The LegalMitra National Judicial Knowledge Graph links Constitution Articles, Statutes, Sections, Judicial Precedents, Orders, and Legal Concepts. It models directed, typed relationships with propositional accuracy to prevent citing overruled authorities.

---

## 2. Precedent Treatment Graph Verifications

All relationships in `data/08_corpus/precedent_relationships.json` and `precedent_edge_audit_register.json` have been audited and anchored to exact proposition paragraph references:

| Relationship ID | Citing Case | Cited Case | Treatment | Proposition / Passage Anchor |
|---|---|---|---|---|
| `REL-PUTTASWAMY-OVERRULES-MPSHARMA` | *K.S. Puttaswamy (Retd.) v. UOI* | *M.P. Sharma v. Satish Chandra* | Overruled | Paragraph 262 (Chandrachud, J.) & Para 3 (Chelameswar, J.): Privacy is a fundamental right under Art 21. |
| `REL-PUTTASWAMY-OVERRULES-KHARAK` | *K.S. Puttaswamy (Retd.) v. UOI* | *Kharak Singh v. State of U.P.* | Overruled | Paragraph 262 & Para 319 (Chandrachud, J.): Overruled majority opinion denying fundamental right to privacy. |
| `REL-PUTTASWAMY-OVERRULES-ADMJABALPUR` | *K.S. Puttaswamy (Retd.) v. UOI* | *ADM Jabalpur v. Shivkant Shukla* | Overruled | Paragraph 136 & Para 137 (Chandrachud, J.): Overruled majority; affirmed Justice H.R. Khanna's dissent. |
| `REL-ARJUN-AFFIRMS-ANVAR` | *Arjun Panditrao Khotkar v. Kailash Gorantyal* | *Anvar P.V. v. P.K. Basheer* | Affirmed | Paragraph 51 & 72: Section 65B(4) certificate is a mandatory condition precedent for electronic records. |
| `REL-ARJUN-OVERRULES-SHAFHI` | *Arjun Panditrao Khotkar v. Kailash Gorantyal* | *Shafhi Mohammad v. State of H.P.* | Overruled | Paragraph 72: Overruled Shafhi Mohammad for relaxing Section 65B(4) certificate requirement. |
| `REL-NAVTEJ-OVERRULES-KOUSHAL` | *Navtej Singh Johar v. UOI* | *Suresh Kumar Koushal v. Naz Foundation* | Overruled | Paragraph 267 (Misra, C.J.) & Para 156 (Nariman, J.): Overruled Koushal, decriminalizing consensual adult relationships under Section 377 IPC. |
| `E-OVERRULE-STAMP-NNGLOBAL` | *In Re: Arbitration Agreements & Stamp Act* | *N.N. Global Mercantile* | Overruled | 7-Judge Bench overruled *N.N. Global* (5-Judge) holding unstamped arbitration agreements are not void ab initio. |
| `E-OVERRULE-VIDYA-HIMANGNI` | *Vidya Drolia v. Durga Trading* | *Himangni Enterprises* | Overruled | Overruled *Himangni Enterprises*; held tenancy disputes under Transfer of Property Act are arbitrable. |

---

## 3. High Court Precedent Graph Integration

In addition to Supreme Court overruling edges, High Court interpretive edges are verified in `legalmitra/caselaw/knowledge_graph.py`:
- `CASE-DHC-LOUBOUTIN` ──`[interprets]`──> `SEC-IT-79` (Active marketplace loses safe harbor).
- `CASE-DHC-TATA-GREENPEACE` ──`[interprets]`──> `ART-CONST-19` (Parody and critique protected under Article 19(1)(a)).
