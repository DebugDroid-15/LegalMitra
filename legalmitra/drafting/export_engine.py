"""Document Exporter Studio for LegalMitra Statutory Notices (Phase 74).

Generates court-ready PDF and editable Microsoft Word (DOCX) files from
StatutoryNoticeDraft objects, adhering strictly to Indian legal drafting
conventions:
1. Formal Advocate Letterhead & Bar Enrollment Block
2. Registered AD / Speed Post Tracking Header
3. Mandatory Statutory Grace/Cure Period Callouts
4. Numbered Legal Recitals & Operative Demands
5. Place & Date Block, Verification & Signature Blocks
"""

from __future__ import annotations

import io
import re
from typing import Optional, Union

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from legalmitra.drafting.notice_engine import StatutoryNoticeDraft


class StatutoryNoticeExportEngine:
    """Exports structured StatutoryNoticeDraft payloads into PDF and DOCX formats."""

    @staticmethod
    def export_to_docx(draft: StatutoryNoticeDraft) -> bytes:
        """Generates an editable, court-ready .docx file representation of the legal notice."""
        doc = docx.Document()

        # Set standard legal margins (1 inch all around)
        for section in doc.sections:
            section.top_margin = Inches(1.0)
            section.bottom_margin = Inches(1.0)
            section.left_margin = Inches(1.0)
            section.right_margin = Inches(1.0)

        # 1. Advocate Letterhead
        adv_name = draft.complainant_or_sender.advocate_name or "LEGAL COUNSEL / ADVOCATE"
        adv_enr = draft.complainant_or_sender.advocate_enrollment or "Enrolment No. D/XXXX/XXXX"
        adv_addr = draft.complainant_or_sender.address

        p_header = doc.add_paragraph()
        p_header.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_name = p_header.add_run(f"CHAMBERS OF {adv_name.upper()}\n")
        run_name.bold = True
        run_name.font.size = Pt(14)
        run_name.font.name = "Times New Roman"

        run_sub = p_header.add_run(f"Advocate & Legal Consultant | {adv_enr}\nOffice: {adv_addr}\n")
        run_sub.font.size = Pt(9.5)
        run_sub.font.italic = True
        run_sub.font.color.rgb = RGBColor(80, 80, 80)
        run_sub.font.name = "Times New Roman"

        # Horizontal Divider
        p_div = doc.add_paragraph()
        p_div.paragraph_format.space_after = Pt(14)
        r_div = p_div.add_run("_______________________________________________________________________________")
        r_div.font.size = Pt(8)
        r_div.font.color.rgb = RGBColor(160, 160, 160)

        # 2. Dispatch Mode Header & Date
        p_meta = doc.add_paragraph()
        run_mode = p_meta.add_run("SPEED POST A.D. / REGISTERED POST WITH ACK. DUE / LEGAL TRANSMISSION\n")
        run_mode.bold = True
        run_mode.font.size = Pt(9)
        run_mode.font.name = "Times New Roman"

        run_date = p_meta.add_run(f"Date: {draft.created_at[:10]}\nRef: LM/STAT-NOT/{draft.notice_type.value}/{draft.mandatory_cure_period_days}D")
        run_date.font.size = Pt(10)
        run_date.font.name = "Times New Roman"

        # 3. Addressee (Opposite Party) Block
        doc.add_paragraph().paragraph_format.space_before = Pt(6)
        p_to = doc.add_paragraph()
        r_to_label = p_to.add_run("TO,\n")
        r_to_label.bold = True
        r_to_label.font.name = "Times New Roman"

        r_to = p_to.add_run(f"1. {draft.recipient.name}\n   {draft.recipient.address}\n")
        r_to.font.name = "Times New Roman"
        r_to.font.size = Pt(11)

        # 4. Notice Subject / Title
        p_subj = doc.add_paragraph()
        p_subj.paragraph_format.space_before = Pt(12)
        p_subj.paragraph_format.space_after = Pt(14)
        p_subj.alignment = WD_ALIGN_PARAGRAPH.CENTER

        r_subj = p_subj.add_run(f"LEGAL NOTICE UNDER {draft.statutory_governing_section.upper()}\n")
        r_subj.bold = True
        r_subj.font.size = Pt(12)
        r_subj.font.underline = True
        r_subj.font.name = "Times New Roman"

        r_title = p_subj.add_run(f"{draft.title.upper()}")
        r_title.bold = True
        r_title.font.size = Pt(10.5)
        r_title.font.name = "Times New Roman"

        # 5. Introductory Representation Clause
        p_intro = doc.add_paragraph()
        p_intro.paragraph_format.space_after = Pt(10)
        r_sir = p_intro.add_run("SIR / MADAM,\n\n")
        r_sir.bold = True
        r_sir.font.name = "Times New Roman"

        r_intro = p_intro.add_run(
            f"Under instructions from and on behalf of my client, {draft.complainant_or_sender.name}, "
            f"having address at {draft.complainant_or_sender.address} (hereinafter referred to as the 'Client'), "
            f"I hereby address you with this formal Statutory Demand Notice as under:\n"
        )
        r_intro.font.name = "Times New Roman"
        r_intro.font.size = Pt(11)

        # 6. Factual Recitals
        p_rec_h = doc.add_paragraph()
        r_rec_h = p_rec_h.add_run("I. FACTUAL RECITALS & GROUNDS OF DEMAND:")
        r_rec_h.bold = True
        r_rec_h.font.name = "Times New Roman"

        for idx, rec in enumerate(draft.factual_recitals, start=1):
            p_rec = doc.add_paragraph()
            p_rec.paragraph_format.left_indent = Inches(0.25)
            p_rec.paragraph_format.space_after = Pt(6)
            r_num = p_rec.add_run(f"{idx}. ")
            r_num.bold = True
            r_num.font.name = "Times New Roman"
            r_txt = p_rec.add_run(rec)
            r_txt.font.name = "Times New Roman"
            r_txt.font.size = Pt(10.5)

        # 7. Demands & Requisitions
        p_dem_h = doc.add_paragraph()
        p_dem_h.paragraph_format.space_before = Pt(10)
        r_dem_h = p_dem_h.add_run("II. FORMAL REQUISITIONS & STATUTORY CURE DEMAND:")
        r_dem_h.bold = True
        r_dem_h.font.name = "Times New Roman"

        for idx, dem in enumerate(draft.demands_and_requisitions, start=1):
            p_dem = doc.add_paragraph()
            p_dem.paragraph_format.left_indent = Inches(0.25)
            p_dem.paragraph_format.space_after = Pt(6)
            r_dnum = p_dem.add_run(f"{idx}. ")
            r_dnum.bold = True
            r_dnum.font.name = "Times New Roman"
            r_dtxt = p_dem.add_run(dem)
            r_dtxt.font.name = "Times New Roman"
            r_dtxt.font.size = Pt(10.5)

        # 8. Statutory Warning Callout Box
        p_warn = doc.add_paragraph()
        p_warn.paragraph_format.space_before = Pt(14)
        p_warn.paragraph_format.space_after = Pt(14)
        r_wtitle = p_warn.add_run("STATUTORY CONSEQUENCES & WARNING OF LEGAL PROCEEDINGS:\n")
        r_wtitle.bold = True
        r_wtitle.font.name = "Times New Roman"
        r_wtitle.font.color.rgb = RGBColor(160, 0, 0)

        r_warn = p_warn.add_run(draft.statutory_warning)
        r_warn.font.italic = True
        r_warn.font.name = "Times New Roman"
        r_warn.font.size = Pt(10)

        # 9. Verification & Signature Block
        p_sig = doc.add_paragraph()
        p_sig.paragraph_format.space_before = Pt(18)
        p_sig.paragraph_format.keep_with_next = True

        r_place = p_sig.add_run(f"Place: New Delhi\nDate: {draft.created_at[:10]}\n\n\n\n")
        r_place.font.name = "Times New Roman"
        r_place.font.size = Pt(10)

        r_sign = p_sig.add_run(f"_____________________________________\n({adv_name})\nAdvocate for the Client / Complainant\n{adv_enr}\n")
        r_sign.bold = True
        r_sign.font.name = "Times New Roman"
        r_sign.font.size = Pt(10.5)

        # 10. Copy Retained Note
        p_copy = doc.add_paragraph()
        p_copy.paragraph_format.space_before = Pt(10)
        r_copy = p_copy.add_run("Note: A verified duplicate copy of this Statutory Notice is retained in my chambers for record and future court production.")
        r_copy.font.italic = True
        r_copy.font.size = Pt(8.5)
        r_copy.font.color.rgb = RGBColor(100, 100, 100)
        r_copy.font.name = "Times New Roman"

        bio = io.BytesIO()
        doc.save(bio)
        return bio.getvalue()

    @staticmethod
    def export_to_pdf(draft: StatutoryNoticeDraft) -> bytes:
        """Generates a court-ready, print-formatted PDF document of the statutory legal notice."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=0.75 * inch,
            rightMargin=0.75 * inch,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch,
        )

        styles = getSampleStyleSheet()

        # Custom typography styles
        style_letterhead_name = ParagraphStyle(
            name="LetterheadName",
            fontName="Times-Bold",
            fontSize=14,
            leading=18,
            alignment=1,  # Center
            textColor=colors.HexColor("#1A202C"),
        )
        style_letterhead_sub = ParagraphStyle(
            name="LetterheadSub",
            fontName="Times-Italic",
            fontSize=9.5,
            leading=13,
            alignment=1,  # Center
            textColor=colors.HexColor("#4A5568"),
        )
        style_mode = ParagraphStyle(
            name="NoticeMode",
            fontName="Times-Bold",
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#2B6CB0"),
        )
        style_meta = ParagraphStyle(
            name="NoticeMeta",
            fontName="Times-Roman",
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#2D3748"),
        )
        style_subject = ParagraphStyle(
            name="NoticeSubject",
            fontName="Times-Bold",
            fontSize=11.5,
            leading=15,
            alignment=1,  # Center
            textColor=colors.HexColor("#1A202C"),
        )
        style_body = ParagraphStyle(
            name="NoticeBody",
            fontName="Times-Roman",
            fontSize=10,
            leading=14.5,
            textColor=colors.HexColor("#2D3748"),
            alignment=4,  # Justified
        )
        style_heading = ParagraphStyle(
            name="NoticeHeading",
            fontName="Times-Bold",
            fontSize=10.5,
            leading=14,
            textColor=colors.HexColor("#1A202C"),
            spaceBefore=8,
            spaceAfter=4,
        )
        style_warning = ParagraphStyle(
            name="NoticeWarning",
            fontName="Times-Italic",
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#742A2A"),
        )
        style_sign = ParagraphStyle(
            name="NoticeSign",
            fontName="Times-Roman",
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#1A202C"),
        )
        style_footer = ParagraphStyle(
            name="NoticeFooter",
            fontName="Times-Italic",
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#718096"),
        )

        adv_name = draft.complainant_or_sender.advocate_name or "LEGAL COUNSEL / ADVOCATE"
        adv_enr = draft.complainant_or_sender.advocate_enrollment or "Enrolment No. D/XXXX/XXXX"
        adv_addr = draft.complainant_or_sender.address

        elements = []

        # 1. Chambers Letterhead
        elements.append(Paragraph(f"CHAMBERS OF {adv_name.upper()}", style_letterhead_name))
        elements.append(Paragraph(f"Advocate & Legal Consultant | {adv_enr}<br/>Office: {adv_addr}", style_letterhead_sub))
        elements.append(Spacer(1, 6))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E0"), spaceAfter=10))

        # 2. Dispatch Mode Header
        elements.append(Paragraph("<u>BY SPEED POST A.D. / REGISTERED POST WITH ACKNOWLEDGEMENT DUE</u>", style_mode))
        elements.append(Spacer(1, 4))
        elements.append(Paragraph(f"<b>Date:</b> {draft.created_at[:10]} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Ref:</b> LM/NOT/{draft.notice_type.value}/{draft.mandatory_cure_period_days}D", style_meta))
        elements.append(Spacer(1, 8))

        # 3. Addressee Block
        elements.append(Paragraph("<b>TO,</b>", style_heading))
        elements.append(Paragraph(f"<b>1. {draft.recipient.name}</b><br/>{draft.recipient.address}", style_body))
        elements.append(Spacer(1, 10))

        # 4. Subject Heading
        elements.append(Paragraph(f"<u>LEGAL NOTICE UNDER {draft.statutory_governing_section.upper()}</u><br/><b>{draft.title.upper()}</b>", style_subject))
        elements.append(Spacer(1, 10))

        # 5. Introductory Formal Narrative
        elements.append(Paragraph("<b>SIR / MADAM,</b>", style_body))
        elements.append(Spacer(1, 4))
        elements.append(Paragraph(
            f"Under instructions from and on behalf of my client, <b>{draft.complainant_or_sender.name}</b>, "
            f"residing/having office at {draft.complainant_or_sender.address} (hereinafter referred to as my <i>'Client'</i>), "
            f"I hereby serve upon you this formal Statutory Notice under {draft.statutory_governing_section} on the following factual and legal terms:",
            style_body,
        ))
        elements.append(Spacer(1, 8))

        # 6. Recitals
        elements.append(Paragraph("<b>I. FACTUAL RECITALS & GROUNDS OF DEMAND:</b>", style_heading))
        for idx, rec in enumerate(draft.factual_recitals, start=1):
            elements.append(Paragraph(f"<b>{idx}.</b> {rec}", style_body))
            elements.append(Spacer(1, 4))

        # 7. Demands
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(f"<b>II. FORMAL REQUISITIONS & {draft.mandatory_cure_period_days}-DAY STATUTORY CURE DEMAND:</b>", style_heading))
        for idx, dem in enumerate(draft.demands_and_requisitions, start=1):
            elements.append(Paragraph(f"<b>{idx}.</b> {dem}", style_body))
            elements.append(Spacer(1, 4))

        # 8. Statutory Warning Box
        elements.append(Spacer(1, 10))
        warning_table_data = [
            [Paragraph("<b>STATUTORY WARNING & LEGAL PROCEEDINGS:</b>", ParagraphStyle(name="WarnH", fontName="Times-Bold", fontSize=9, textColor=colors.HexColor("#742A2A")))],
            [Paragraph(draft.statutory_warning, style_warning)],
        ]
        warning_table = Table(warning_table_data, colWidths=[6.8 * inch])
        warning_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF5F5")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#FEB2B2")),
            ("PADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
        ]))
        elements.append(warning_table)
        elements.append(Spacer(1, 14))

        # 9. Sign-off block
        sign_block = []
        sign_block.append(Paragraph(f"<b>Place:</b> New Delhi<br/><b>Date:</b> {draft.created_at[:10]}", style_meta))
        sign_block.append(Spacer(1, 16))
        sign_block.append(Paragraph(f"_____________________________________<br/><b>({adv_name})</b><br/>Advocate for the Client / Complainant<br/>{adv_enr}", style_sign))
        elements.append(KeepTogether(sign_block))

        # 10. Copy Note
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("<i>Note: A verified duplicate copy of this Statutory Notice is retained in my chambers for record and future court production.</i>", style_footer))

        doc.build(elements)
        return buffer.getvalue()
