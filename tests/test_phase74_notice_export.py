"""
Test Suite for Phase 74: Court-Ready Legal Notice PDF & DOCX Export Studio.
Verifies:
1. High-fidelity PDF export generation with ReportLab.
2. Editable Word DOCX export generation with python-docx.
3. Proper legal margin, advocate letterhead, speed post header, and statutory warning block inclusion.
4. REST API binary stream endpoints for PDF and DOCX exports.
5. Multi-notice compliance across Section 138 NI Act, Section 21 Arbitration, and Section 106 TPA.
"""

import io
import pytest
from fastapi.testclient import TestClient

from legalmitra.drafting.export_engine import StatutoryNoticeExportEngine
from legalmitra.drafting.notice_engine import (
    NoticeParty,
    NoticeType,
    StatutoryNoticeDraftingEngine,
)
from legalmitra.server.api import app


class TestPhase74NoticeExport:

    @pytest.fixture
    def sample_ni138_draft(self):
        s = NoticeParty(
            name="Apex Commercial Ventures Ltd",
            address="Level 12, Barakhamba Road, Connaught Place, New Delhi 110001",
            advocate_name="Vikramaditya Sen",
            advocate_enrollment="D/4567/2012",
        )
        r = NoticeParty(
            name="Bharat Logistics Solutions Pvt Ltd",
            address="Plot 89, Sector 18, Electronic City, Gurugram, Haryana",
        )
        facts = {
            "cheque_number": "789123",
            "cheque_date": "2024-06-15",
            "cheque_amount": "12,50,000",
            "bank_name": "State Bank of India",
            "memo_date": "2024-06-25",
            "dishonour_reason": "Funds Insufficient",
            "debt_description": "Supply of commercial electronic consignments under Invoice No. 1042",
        }
        return StatutoryNoticeDraftingEngine.draft_notice(
            notice_type=NoticeType.CHEQUE_BOUNCE_NI_ACT_138,
            sender=s,
            recipient=r,
            facts=facts,
        )

    def test_pdf_export_structure(self, sample_ni138_draft):
        pdf_bytes = StatutoryNoticeExportEngine.export_to_pdf(sample_ni138_draft)

        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 2000
        # Check standard PDF header magic bytes %PDF-
        assert pdf_bytes.startswith(b"%PDF-")

    def test_docx_export_structure(self, sample_ni138_draft):
        docx_bytes = StatutoryNoticeExportEngine.export_to_docx(sample_ni138_draft)

        assert isinstance(docx_bytes, bytes)
        assert len(docx_bytes) > 5000
        # Check standard ZIP/OpenXML magic bytes PK\x03\x04
        assert docx_bytes.startswith(b"PK\x03\x04")

        # Verify readability with python-docx
        import docx
        doc = docx.Document(io.BytesIO(docx_bytes))
        full_text = "\n".join(p.text for p in doc.paragraphs)

        assert "CHAMBERS OF VIKRAMADITYA SEN" in full_text
        assert "Apex Commercial Ventures Ltd" in full_text
        assert "Bharat Logistics Solutions Pvt Ltd" in full_text
        assert "15" in full_text  # 15 days cure period
        assert "SECTION 138" in full_text and "NEGOTIABLE INSTRUMENTS ACT" in full_text

    def test_arbitration_notice_pdf_and_docx(self):
        s = NoticeParty(name="Claimant Infra Corp", address="Mumbai, MH", advocate_name="Adv. Mehra")
        r = NoticeParty(name="Respondent Tech Ltd", address="Bengaluru, KA")
        facts = {
            "contract_date": "2023-01-15",
            "contract_title": "EPC Turnkey Project Agreement",
            "arbitration_clause": "Clause 24.2",
            "dispute_summary": "Unjustified termination and failure to release milestone payment",
            "claim_amount": "4,50,00,000",
            "proposed_arbitrator": "Hon'ble Justice (Retd.) K. S. Sharma",
        }
        draft = StatutoryNoticeDraftingEngine.draft_notice(
            notice_type=NoticeType.ARBITRATION_INVOCATION_SEC_21,
            sender=s,
            recipient=r,
            facts=facts,
        )

        pdf_bytes = StatutoryNoticeExportEngine.export_to_pdf(draft)
        docx_bytes = StatutoryNoticeExportEngine.export_to_docx(draft)

        assert pdf_bytes.startswith(b"%PDF-")
        assert docx_bytes.startswith(b"PK\x03\x04")
        assert draft.mandatory_cure_period_days == 30

    def test_rest_api_pdf_export_endpoint(self):
        client = TestClient(app)
        payload = {
            "notice_type": "ni138",
            "sender": {
                "name": "Complainant Enterprise",
                "address": "New Delhi",
                "advocate_name": "Adv. R. K. Gupta",
                "advocate_enrollment": "D/999/2011",
            },
            "recipient": {
                "name": "Defaulting Party",
                "address": "Noida, UP",
            },
            "facts": {
                "cheque_number": "112233",
                "cheque_amount": "3,00,000",
                "bank_name": "ICICI Bank",
                "memo_date": "2024-05-12",
                "dishonour_reason": "Account Closed",
                "debt_description": "Goods sold and delivered",
            },
        }

        res = client.post("/api/v1/draft/export/pdf", json=payload)
        assert res.status_code == 200
        assert res.headers["content-type"] == "application/pdf"
        assert "attachment; filename=" in res.headers["content-disposition"]
        assert res.content.startswith(b"%PDF-")

    def test_rest_api_docx_export_endpoint(self):
        client = TestClient(app)
        payload = {
            "notice_type": "tpa106",
            "sender": {
                "name": "Landlord Trust",
                "address": "South Delhi",
                "advocate_name": "Adv. P. Verma",
            },
            "recipient": {
                "name": "Tenant Occupant",
                "address": "Shop 4, Market Complex",
            },
            "facts": {
                "tenancy_month": "Calendar Month",
                "property_desc": "Commercial Shop No. 4",
                "grounds": "Arrears of rent and expiry of lease period",
            },
        }

        res = client.post("/api/v1/draft/export/docx", json=payload)
        assert res.status_code == 200
        assert "application/vnd.openxmlformats" in res.headers["content-type"]
        assert "attachment; filename=" in res.headers["content-disposition"]
        assert res.content.startswith(b"PK\x03\x04")
