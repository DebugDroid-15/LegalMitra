# LegalMitra Phase 42 — Source Permission & Access Rights Register

**Date:** October 19, 2026  
**Auditor:** Senior Legal Infrastructure & Compliance Lead  
**Scope:** Comprehensive review of digital source access permissions for all judicial and statutory repositories  

---

## 1. Statutory & Institutional Permission Matrix

| Source Authority | Repository Domain | Permitted Access Mode | Operational Safeguards Required | LegalMitra Status |
|:---|:---|:---|:---|:---:|
| **eCourts Services** | `services.ecourts.gov.in` | Authorized Institutional API via SC eCommittee MOU | Bearer Token, Client ID, rate limiting. Scraping & CAPTCHA bypass strictly prohibited. | **BLOCKED_PENDING_ECOMMITTEE_CREDENTIALS** (Staging Fallback Active) |
| **High Court of Delhi** | `delhihighcourt.nic.in` | Public Web Portal / Case History Query | Manual web access permitted; automated bulk scraping requires Registrar General written authorization. | **FIXTURE_VALIDATED_GATED** (Live unauthenticated crawling blocked) |
| **High Court of Bombay** | `bombayhighcourt.nic.in` | Public Case Status & Orders Portal | Manual query permitted; automated harvesting subject to NIC WAF rate limits. | **FIXTURE_VALIDATED_GATED** (Live unauthenticated crawling blocked) |
| **Supreme Court of India** | `main.sci.gov.in` / `judis.nic.in` | Open Access Judgments & Neutral Citations | Permitted for public non-commercial legal research under Open Judicial Data initiatives. | **VERIFIED_PUBLIC_DOMAIN** |
| **Gazette of India** | `egazette.gov.in` | Official Central Government Gazette | Central statutory enactments (BNS, BNSS, BSA) are sovereign public domain legal texts. | **AUTHENTIC_PUBLIC_DOMAIN** |
| **High Court Hindi Releases** | State HC Portals (Allahabad, Rajasthan, MP) | Certified Public Vernacular Judgments | Published under Article 348(2) & Official Languages Act for open public dissemination. | **VERIFIED_BENCHMARK_STAGED** |

---

## 2. Access Governance Policies

1. **No Circumvention Rule:** No module in LegalMitra may contain routines for breaking CAPTCHAs, spoofing browser finger-prints, rotating residential proxies to evade IP bans, or forging authorization tokens.
2. **Pretraining Quarantine:** No district court case file or unreviewed advocate pilot candidate may be routed to neural foundation model pretraining pipelines.
3. **Idempotent Ingestion:** All network-acquired artifacts must be hashed via SHA-256 upon reception and compared against existing inventories before processing.
