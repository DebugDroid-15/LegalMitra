# LegalMitra Phase 24 Temporal Law & Criminal Transition Validation Report
**Workspace:** `C:\PROJECTS\LegalMitra`  
**Repository:** `https://github.com/DebugDroid-15/LegalMitra`  
**Owner:** Team Shatrujeet — Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo  
**Date:** October 2026  
**Classification:** Proprietary and Confidential  

---

## 1. Executive Summary

Indian criminal and procedural jurisprudence underwent a fundamental transition on **1 July 2024**, when the three new criminal enactments came into force via Ministry of Home Affairs commencement notifications (S.O. 848(E), S.O. 849(E), and S.O. 850(E)).

LegalMitra's temporal engine enforces strict temporal regime boundaries to prevent anachronistic application of law.

---

## 2. Criminal Transition & Savings Statutory Grounding

### 2.1 Substantive Criminal Law: IPC vs BNS 2023
- **Article 20(1) Constitutional Protection:** No person shall be convicted of any offence except for violation of a law in force at the time of the commission of the act charged as an offence.
- **Offences Committed Prior to 1 July 2024:** Governed strictly by the Indian Penal Code, 1860 (e.g. Section 420 IPC for cheating, Section 302 IPC for murder).
- **Offences Committed on or after 1 July 2024:** Governed exclusively by the Bharatiya Nyaya Sanhita, 2023 (e.g. Section 318 BNS for cheating, Section 103 BNS for murder).
- **Enforcement in LegalMitra:** Queries anchored on dates prior to 2024-07-01 are flagged if BNS is cited as substantive law, and post-2024-07-01 offences are flagged if IPC is cited.

### 2.2 Criminal Procedure: CrPC 1973 vs BNSS 2023 (Section 531)
- **Section 531(2)(a) BNSS 2023:** Expressly provides that notwithstanding repeal of the Code of Criminal Procedure, 1973, any appeal, application, trial, inquiry or investigation pending immediately before the commencement date shall be disposed of, continued, held or conducted in accordance with the provisions of the CrPC 1973 as if BNSS had not come into force.
- **New FIRs / Inquiries Registered Post-July 2024 for Prior Incidents:** While substantive offence remains under IPC, procedural steps post-commencement follow judicial interpretation of Section 531 BNSS.

### 2.3 Law of Evidence: IEA 1872 vs BSA 2023 (Section 170)
- **Section 170(2) BSA 2023:** Mandates that any proceeding pending immediately before 1 July 2024 continues under the Indian Evidence Act, 1872.
- **Electronic Evidence Transition:** Certificates required under former Section 65B(4) IEA now correspond to Section 63(4) BSA 2023.

---

## 3. Temporal Validation Scenarios & Guardrails

| Test Scenario | Temporal Anchor | Expected Governing Law | Prohibited / Anachronistic Citation | Result |
| :--- | :---: | :--- | :--- | :---: |
| **Cheating incident on 15 August 2024** | 2024-08-15 | Section 318 BNS 2023 | Section 420 IPC | **PASS** |
| **Pending 2023 FIR investigation as of July 2024** | 2024-07-02 | CrPC 1973 (Sec 531 BNSS savings) | Retrospective application of BNSS | **PASS** |
| **Trial pending as of 30 June 2024** | 2024-06-30 | IEA 1872 (Sec 170 BSA savings) | BSA 2023 retroactivity | **PASS** |
| **Phased DPDP 2023 Commencement** | 2026-10-17 | Phased notifications (IT Act 43A remains operative) | Blanket unconditional repeal in 2023 | **PASS** |
