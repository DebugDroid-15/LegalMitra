# RUNBOOK 54: SOURCE INTEGRITY & PROVENANCE AUDIT

**Project:** LegalMitra  
**Classification:** PROPRIETARY AND CONFIDENTIAL  
**Team:** Shatrujeet  
**Date:** October 2026  

---

## 1. Procedure

To audit the authenticity and Gazette provenance of new legal acquisitions:
1. Ensure the source is acquired from official repositories (`indiacode.nic.in`, `egazette.gov.in`, `sci.gov.in`, or official High Court portals).
2. Calculate the SHA-256 checksum of the primary document.
3. Verify that the enactment commencement notification is published in the Gazette of India.
4. Record whether the enactment has unnotified provisions or prospective amendments.
5. Ingest into `sources` table with appropriate `verification_status` and run `SourceAuthenticityVerifier`.
