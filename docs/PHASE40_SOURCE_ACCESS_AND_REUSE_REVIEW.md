# PHASE 40 — SOURCE ACCESS, COPYRIGHT, AND REUSE REVIEW

## 1. Statutory Context & Legal Authority

The acquisition, normalization, indexing, and serving of judicial judgments and legal materials in India is governed by specific statutory exemptions under the **Copyright Act, 1957 (India)**.

### Section 52(1)(q) Exemption
Under Section 52(1)(q)(iv) of the Copyright Act, 1957:
> *"The following acts shall not constitute an infringement of copyright, namely: ... the reproduction or publication of — (iv) any judgment or order of a court, tribunal or other judicial authority, unless the reproduction or publication of such judgment or order is prohibited by the court, the tribunal or other judicial authority, as the case may be."*

Judicial decisions delivered by the Supreme Court of India, High Courts, District Courts, and Tribunals are in the public domain as sovereign judicial acts, subject to court-ordered seals or statutory publication bars.

---

## 2. Eastern Book Company v. D.B. Modak (2008) 1 SCC 1

The Supreme Court of India in *Eastern Book Company v. D.B. Modak* established the definitive standard on copyright in law reports and judicial judgments:
1. **Raw Judgments**: The text of the judgment delivered by the court is public property and cannot be subjected to copyright claims by any private publisher.
2. **Headnotes and Editorial Additions**: Private law reporters possess copyright only in their original editorial headnotes, footnotes, and paragraph arrangements that demonstrate "a minimum modicum of creativity" and exercise of judgment.
3. **LegalMitra Policy**: LegalMitra acquires only raw, official judgments and neutral citations directly from court registries, the Supreme Court of India (`sci.gov.in`), Delhi High Court (`delhihighcourt.nic.in`), Bombay High Court (`bombayhighcourt.nic.in`), and official eCourts portals. LegalMitra never ingests third-party proprietary headnotes, digests, or commercial editorial annotations.

---

## 3. Terms of Service, Rate Limiting, and Access Etiquette

1. **Lawful Access**: Egress to government portals is polite and respectful of server capacity.
2. **No CAPTCHA Circumvention**: Where court portals (such as eCourts Services public search) utilize visual CAPTCHA verification, LegalMitra strictly forbids automated CAPTCHA-breaking algorithms. Instead, District Court records are ingested via authorized local data dumps or authenticated eCommittee API credentials.
3. **SSRF Guard**: All connectors are physically barred from accessing non-approved domains or internal network nodes.
4. **Permanent Audit Logging**: Every acquired document records timestamp, source URL, SHA-256 digest, and responsible process ID.
