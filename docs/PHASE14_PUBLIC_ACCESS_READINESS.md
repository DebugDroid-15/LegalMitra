# LegalMitra Public-Benefit Product Readiness & Access Guidelines

**Specification Document — Phase 14J**  
**Version:** 1.0.0  
**Classification:** Public Access, Legal Aid Integration & Ethical Boundaries

---

## 1. Mission: Affordable Legal Research & Public Assistance

LegalMitra is designed to reduce unnecessary legal research costs for citizens, students, and small enterprises while assisting legal practitioners with instant, source-traceable statutory lookup.

### Explicit Professional Boundaries:
- **No Replacement for Advocates:** LegalMitra provides legal information, statutory cross-referencing, and precedent tracking. It does not provide legal advice, represent parties in litigation, or replace licensed advocates enrolled under the Advocates Act, 1961.
- **Escalation Recommendations:** The application automatically advises users to consult an advocate when queries involve:
  1. Active criminal arrests, police summons, or non-bailable warrants.
  2. Imminent statutory limitation deadlines under the Limitation Act, 1963.
  3. Disputed questions of fact, cross-examination, or evidence admissibility.
  4. Commercial disputes exceeding pecuniary jurisdiction thresholds.

---

## 2. Verified Free Legal Aid Resources

Under the Legal Services Authorities Act, 1987, eligible citizens (including women, children, members of SC/ST communities, and persons with annual income below statutory thresholds) are entitled to free legal assistance:

| Institution | Level | Jurisdiction | Official Portal |
|---|---|---|---|
| **National Legal Services Authority (NALSA)** | National | Supreme Court & Central Oversight | `https://nalsa.gov.in/` |
| **Supreme Court Legal Services Committee (SCLSC)** | Apex Court | Supreme Court Matters | `https://sclsc.gov.in/` |
| **State Legal Services Authorities (SLSAs)** | State | High Courts & State Matters | Respective State High Court Portals |
| **District Legal Services Authorities (DLSAs)** | District | District & Taluk Courts | Respective District Court Complexes |
| **Tele-Law (Department of Justice)** | Panchayats / CSCs | Pre-litigation Legal Advice | `https://www.tele-law.in/` |

---

## 3. UI, Privacy, and Accessibility Standards

1. **Constitutional Modernism Design Tokens:** Deep Navy (`#172B4D`) and Constitutional Ivory (`#FAF8F2`) with clean, legible typography optimized for mobile devices and low-bandwidth connections.
2. **Session Privacy:** User queries and conversations are maintained in a separate SQLite database (`conversations.db`) with zero telemetry or unconsented cross-session indexing.
3. **Multilingual Architecture:** The taxonomy and inventory support standard Indian languages, preparing for Hindi and regional vernacular translation modules in subsequent phases.

