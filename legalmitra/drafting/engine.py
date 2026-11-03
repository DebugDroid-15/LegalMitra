"""
Phase 98: One-Click Statutory Notice & Representation Drafter
Generates legally authoritative, formal statutory notices and police representations
grounded in authentic Indian enactments (BNSS, NI Act, Consumer Protection, Transfer of Property).

Exports formatted Word (.docx) and PDF documents adhering to Indian Court and Advocate margin standards.
"""

from __future__ import annotations

import base64
import io
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

import docx
from docx.shared import Inches, Pt

logger = logging.getLogger("statutory_drafter")


class NoticeTemplateType(str, Enum):
    POLICE_FIR_REFUSAL_SP = "police_fir_refusal_sp"         # Sec 173(4) BNSS (erstwhile 154(3) CrPC)
    CHEQUE_DISHONOUR_138 = "cheque_dishonour_138"           # Sec 138 Negotiable Instruments Act
    CONSUMER_DEFICIENCY_NOTICE = "consumer_deficiency_notice" # Sec 35 Consumer Protection Act 2019
    TENANT_EVICTION_NOTICE = "tenant_eviction_notice"       # Sec 106 Transfer of Property Act 1882
    GENERAL_LEGAL_DEMAND = "general_legal_demand"           # Civil / Contractual Demand Notice


@dataclass
class NoticeDraftRequest:
    template_type: NoticeTemplateType
    sender_name: str
    sender_address: str
    recipient_name: str
    recipient_designation: str
    recipient_address: str
    incident_date: str
    cause_of_action_facts: str
    claim_amount: Optional[str] = None
    cheque_number: Optional[str] = None
    cheque_date: Optional[str] = None
    police_station_name: Optional[str] = None
    advocate_name: Optional[str] = "LegalMitra Sovereign Draft"
    advocate_enrollment: Optional[str] = "Enrolled under Advocates Act, 1961"


@dataclass
class NoticeDraftResult:
    success: bool
    template_type: NoticeTemplateType
    title: str
    full_text_markdown: str
    pdf_base64: Optional[str] = None
    docx_base64: Optional[str] = None
    statutory_provision: str = ""
    error_message: Optional[str] = None


class StatutoryNoticeDrafter:
    """
    Automated Legal Drafting Engine conforming to Indian statutory notice requirements.
    """

    def generate_draft(self, req: NoticeDraftRequest) -> NoticeDraftResult:
        today_str = datetime.now().strftime("%d-%m-%Y")

        if req.template_type == NoticeTemplateType.POLICE_FIR_REFUSAL_SP:
            title = "WRITTEN REPRESENTATION UNDER SECTION 173(4) OF THE BHARATIYA NAGARIK SURAKSHA SANHITA, 2023"
            statutory_provision = "Section 173(4) BNSS, 2023 (Corresponding to Section 154(3) CrPC, 1973)"
            content_md = f"""# {title}

**Date:** {today_str}  
**Mode of Service:** Registered Post with Acknowledgment Due (RPAD) / Speed Post  

**TO:**  
**The {req.recipient_designation} ({req.recipient_name})**,  
Office of the Superintendent of Police / Deputy Commissioner of Police,  
{req.recipient_address}  

**FROM:**  
**{req.sender_name}**,  
{req.sender_address}  

---

### SUBJECT:
**Representation under Section 173(4) of the Bharatiya Nagarik Suraksha Sanhita, 2023 regarding refusal by Officer-in-Charge, {req.police_station_name or 'Local Police Station'} to record Information of a Cognizable Offence.**

---

**RESPECTED SIR / MADAM,**

1. The Applicant/Complainant named above respectfully submits this written representation to bring to your urgent official notice the arbitrary and unlawful refusal by the Station House Officer (SHO), {req.police_station_name or 'concerned Police Station'}, to record an FIR disclosing the commission of serious cognizable offences.

2. **STATEMENT OF COGNIZABLE FACTS:**  
On {req.incident_date}, at the location described herein, the following cognizable offences were committed against the Applicant:  
"{req.cause_of_action_facts}"

3. **MANDATE OF LAW UNDER SECTION 173 BNSS:**  
The Applicant approached the Station House Officer on {req.incident_date} with a written complaint. However, in direct violation of the mandatory dictum laid down by the Constitution Bench of the Supreme Court of India in **Lalita Kumari v. Government of U.P. [(2014) 2 SCC 1]** and the express statutory command of **Section 173(1) of the Bharatiya Nagarik Suraksha Sanhita, 2023**, the concerned officer arbitrarily refused to register the First Information Report (FIR).

4. **PRAYER & STATUTORY RELIEF SOUGHT:**  
In light of the aforesaid facts and by virtue of the supervisory powers vested in your high office under **Section 173(4) of the Bharatiya Nagarik Suraksha Sanhita, 2023**, the Applicant respectfully prays that:  
(a) Your office may kindly examine the substance of the information disclosing a cognizable offence;  
(b) Direct the immediate registration of an FIR at the competent Police Station; and  
(c) Either investigate the offence yourself or direct an officer subordinate to you to conduct an impartial investigation in accordance with the provisions of the BNSS, 2023.

Yours faithfully,  

_____________________________  
**{req.sender_name}**  
(Complainant / Applicant)  
Contact & Address: {req.sender_address}  
"""

        elif req.template_type == NoticeTemplateType.CHEQUE_DISHONOUR_138:
            title = "FORMAL STATUTORY DEMAND NOTICE UNDER SECTION 138 OF THE NEGOTIABLE INSTRUMENTS ACT, 1881"
            statutory_provision = "Section 138 read with Section 142 of Negotiable Instruments Act, 1881"
            content_md = f"""# {title}

**Date:** {today_str}  
**Mode of Service:** Speed Post / Registered Post with A.D.  

**TO:**  
**{req.recipient_name}**,  
{req.recipient_address}  

**FROM (Through Legal Counsel):**  
**Advocate {req.advocate_name}**,  
{req.advocate_enrollment}  
On behalf of Client: **{req.sender_name}**, {req.sender_address}  

---

### SUBJECT:
**Statutory Demand Notice under Clause (b) of the Proviso to Section 138 of the Negotiable Instruments Act, 1881 for Dishonour of Cheque No. {req.cheque_number or '[Cheque No]'} for Amount INR {req.claim_amount or '[Amount]'}/-.**

---

**SIR / MADAM,**

Under instructions from and on behalf of my client **{req.sender_name}**, I hereby serve upon you this mandatory Statutory Legal Demand Notice:

1. That in discharge of your legally enforceable debt and subsisting liability towards my client, you issued Cheque bearing No. **{req.cheque_number or '[Cheque No]'}** dated **{req.cheque_date or req.incident_date}** for a sum of **INR {req.claim_amount or '[Amount]'}/-** drawn on your bank account.

2. That upon presentation by my client through their banker within its period of validity, the said cheque was returned dishonoured and unpaid with the official bank return memo stating the reason: "Funds Insufficient / Exceeds Arrangement".

3. **CAUSE OF ACTION & CIRCUMSTANCES:**  
"{req.cause_of_action_facts}"

4. **15-DAY STATUTORY DEMAND:**  
In terms of **Section 138(c) of the Negotiable Instruments Act, 1881**, you are hereby formally called upon to make payment of the said cheque amount of **INR {req.claim_amount or '[Amount]'}/-** to my client within **fifteen (15) days** from the date of receipt of this notice.

5. **NOTICE OF PROSECUTION:**  
Please take note that in the event you fail to liquidate the aforesaid amount within the stipulated statutory period of 15 days, my client shall be constrained to initiate criminal proceedings against you under **Section 138 read with Section 142 of the Negotiable Instruments Act, 1881** and **Section 318(4) of the Bharatiya Nyaya Sanhita, 2023 (Cheating)** before the competent Judicial Magistrate, holding you liable for imprisonment up to two years, fine up to twice the cheque amount, and all costs of litigation.

Yours faithfully,  

_____________________________  
**Advocate {req.advocate_name}**  
Counsel for {req.sender_name}  
"""

        elif req.template_type == NoticeTemplateType.CONSUMER_DEFICIENCY_NOTICE:
            title = "PRE-LITIGATION LEGAL NOTICE UNDER SECTION 35 OF THE CONSUMER PROTECTION ACT, 2019"
            statutory_provision = "Section 2(11), Section 2(47) & Section 35 Consumer Protection Act, 2019"
            content_md = f"""# {title}

**Date:** {today_str}  
**TO:**  
**{req.recipient_name} ({req.recipient_designation})**,  
{req.recipient_address}  

**FROM:**  
**{req.sender_name}**,  
{req.sender_address}  

---

### SUBJECT:
**Legal Notice for Deficiency of Service, Defective Goods, and Unfair Trade Practice under Consumer Protection Act, 2019.**

---

**SIR / MADAM,**

1. That the Complainant is a 'Consumer' within the statutory meaning of **Section 2(7) of the Consumer Protection Act, 2019**, having availed your services / purchased goods on {req.incident_date} for valuable consideration amounting to **INR {req.claim_amount or '[Amount]'}/-**.

2. **STATEMENT OF GRIEVANCE & DEFICIENCY:**  
"{req.cause_of_action_facts}"

3. That your aforesaid conduct constitutes gross 'Deficiency of Service' under **Section 2(11)** and an 'Unfair Trade Practice' under **Section 2(47)** of the Consumer Protection Act, 2019, causing severe financial loss and mental harassment to the Complainant.

4. **FINAL REQUISITION:**  
You are hereby called upon to refund the full amount of **INR {req.claim_amount or '[Amount]'}/-** along with interest @ 18% p.a. and compensation of INR 25,000/- for harassment within **15 days** of receiving this notice, failing which a formal Consumer Complaint shall be filed before the competent District Consumer Disputes Redressal Commission under **Section 35 of the Consumer Protection Act, 2019** at your sole risk and costs.

Yours faithfully,  

_____________________________  
**{req.sender_name}**  
"""

        else:
            title = "FORMAL STATUTORY LEGAL DEMAND NOTICE"
            statutory_provision = "Indian Contract Act, 1872 / Specific Relief Act, 1963"
            content_md = f"""# {title}

**Date:** {today_str}  
**TO:** {req.recipient_name}, {req.recipient_address}  
**FROM:** {req.sender_name}, {req.sender_address}  

### SUBJECT: Demand Notice for Redressal of Grievance.

**SIR / MADAM,**  
Please take notice that regarding the dispute of {req.incident_date}:  
"{req.cause_of_action_facts}"

You are formally called upon to perform your legal obligations and redress the aforesaid grievance within 15 days of this notice, failing which legal proceedings shall be initiated before competent courts.

Yours faithfully,  
**{req.sender_name}**
"""

        # Generate Binary Artifacts (PDF & DOCX)
        pdf_b64 = self._render_pdf(title, content_md)
        docx_b64 = self._render_docx(title, content_md)

        return NoticeDraftResult(
            success=True,
            template_type=req.template_type,
            title=title,
            full_text_markdown=content_md,
            pdf_base64=pdf_b64,
            docx_base64=docx_b64,
            statutory_provision=statutory_provision
        )

    def _render_pdf(self, title: str, markdown_text: str) -> str:
        """Renders formal legal PDF document with court standard 1-inch margins."""
        buf = io.BytesIO()
        doc = SimpleDocTemplate(
            buf,
            pagesize=letter,
            rightMargin=inch,
            leftMargin=inch,
            topMargin=inch,
            bottomMargin=inch
        )
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'LegalTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=15,
            alignment=1, # Center
            spaceAfter=14
        )
        body_style = ParagraphStyle(
            'LegalBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            spaceAfter=7
        )

        story = []
        story.append(Paragraph(f"<b>{title}</b>", title_style))
        story.append(Spacer(1, 8))

        lines = markdown_text.split("\n")
        for line in lines:
            if line.startswith("#"):
                continue
            elif line.startswith("---"):
                story.append(Spacer(1, 6))
            elif line.strip():
                clean_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                clean_line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', clean_line)
                clean_line = re.sub(r'\*(.*?)\*', r'<i>\1</i>', clean_line)
                story.append(Paragraph(clean_line, body_style))

        doc.build(story)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode("utf-8")

    def _render_docx(self, title: str, markdown_text: str) -> str:
        """Renders formal Microsoft Word (.docx) file with court formatting."""
        doc = docx.Document()
        for section in doc.sections:
            section.top_margin = Inches(1)
            section.bottom_margin = Inches(1)
            section.left_margin = Inches(1)
            section.right_margin = Inches(1)

        # Title
        p_title = doc.add_paragraph()
        run_title = p_title.add_run(title)
        run_title.bold = True
        run_title.font.size = Pt(13)
        run_title.font.name = "Times New Roman"
        p_title.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER

        for line in markdown_text.split("\n"):
            if line.startswith("#"):
                continue
            elif line.startswith("###"):
                p = doc.add_paragraph()
                r = p.add_run(line.replace("###", "").strip())
                r.bold = True
                r.font.size = Pt(11)
                r.font.name = "Times New Roman"
            elif line.strip():
                p = doc.add_paragraph()
                clean = line.replace("**", "")
                r = p.add_run(clean)
                r.font.size = Pt(10.5)
                r.font.name = "Times New Roman"

        buf = io.BytesIO()
        doc.save(buf)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode("utf-8")
