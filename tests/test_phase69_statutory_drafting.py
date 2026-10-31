"""Phase 69 Test Suite: Statutory Legal Notice & Document Drafting Engine."""

import pytest
from legalmitra.drafting import (
    NoticeParty,
    NoticeType,
    StatutoryNoticeDraft,
    StatutoryNoticeDraftingEngine,
)


class TestPhase69StatutoryNoticeDrafting:
    """Verifies statutory compliance, mandatory cure windows, and Markdown formatting of drafted legal notices."""

    def test_section_138_ni_act_statutory_cure_and_warning(self):
        """Test Section 138 NI Act draft enforces 15-day cure period and criminal penalty warning."""
        sender = NoticeParty(
            name="Apex Enterprises Ltd",
            address="Nehru Place, New Delhi",
            advocate_name="Advocate Vikram Sen",
            advocate_enrollment="D/998/2010"
        )
        recipient = NoticeParty(name="Sun Traders Pvt Ltd", address="Okhla Phase 3, New Delhi")
        facts = {
            "cheque_number": "112233",
            "cheque_date": "2024-04-01",
            "cheque_amount": "8,50,000",
            "bank_name": "Axis Bank",
            "return_memo_date": "2024-04-10",
            "dishonour_reason": "Funds Insufficient"
        }

        draft = StatutoryNoticeDraftingEngine.draft_notice(
            NoticeType.CHEQUE_BOUNCE_NI_ACT_138, sender, recipient, facts, as_of_date="2024-04-15"
        )

        assert isinstance(draft, StatutoryNoticeDraft)
        assert draft.notice_type == NoticeType.CHEQUE_BOUNCE_NI_ACT_138
        assert draft.mandatory_cure_period_days == 15
        assert "fifteen (15) days" in draft.full_notice_markdown
        assert "Section 138" in draft.full_notice_markdown
        assert "Section 141" in draft.full_notice_markdown
        assert "Advocate Vikram Sen" in draft.full_notice_markdown
        assert "INR 8,50,000" in draft.full_notice_markdown

    def test_section_21_arbitration_notice_30_days_cure(self):
        """Test Section 21 Arbitration notice enforces statutory 30-day nomination window."""
        sender = NoticeParty(name="Infra Construtora Inc", address="Bandra Kurla Complex, Mumbai")
        recipient = NoticeParty(name="Metro Rail Authority", address="Nariman Point, Mumbai")
        facts = {
            "contract_title": "Concession Agreement for Metro Line 4",
            "contract_date": "2020-02-15",
            "arbitration_clause": "Clause 22.3 (Arbitration)",
            "nature_of_disputes": "Prolongation costs and delay damages",
            "claim_amount": "45,00,00,000",
            "proposed_arbitrator": "Justice (Retd.) S.K. Kaul"
        }

        draft = StatutoryNoticeDraftingEngine.draft_notice(
            NoticeType.ARBITRATION_INVOCATION_SEC_21, sender, recipient, facts, as_of_date="2024-07-01"
        )

        assert draft.mandatory_cure_period_days == 30
        assert "Section 21" in draft.full_notice_markdown
        assert "Section 11(6)" in draft.full_notice_markdown
        assert "thirty (30) days" in draft.full_notice_markdown
        assert "Justice (Retd.) S.K. Kaul" in draft.full_notice_markdown

    def test_section_106_tpa_tenancy_termination(self):
        """Test Section 106 Transfer of Property Act 15-day notice to quit."""
        sender = NoticeParty(name="Ramesh Chandra", address="Civil Lines, Jaipur")
        recipient = NoticeParty(name="Tenant Suresh Kumar", address="Shop 4, MI Road, Jaipur")
        facts = {
            "property_address": "Commercial Shop 4, MI Road, Jaipur",
            "lease_date": "2021-01-01",
            "monthly_rent": "35,000",
            "ground_for_eviction": "Non-payment of rent for 6 consecutive months"
        }

        draft = StatutoryNoticeDraftingEngine.draft_notice(
            NoticeType.TENANCY_TERMINATION_TPA_106, sender, recipient, facts
        )

        assert draft.mandatory_cure_period_days == 15
        assert "SECTION 106" in draft.full_notice_markdown or "Section 106" in draft.full_notice_markdown
        assert "Transfer of Property Act, 1882" in draft.full_notice_markdown
        assert "Shop 4, MI Road, Jaipur" in draft.full_notice_markdown

    def test_section_8_ibc_demand_notice_10_days_statutory_window(self):
        """Test Section 8 IBC Form 3 operational creditor demand notice with 10-day timeline."""
        sender = NoticeParty(name="Steel Suppliers LLP", address="Peenya, Bengaluru")
        recipient = NoticeParty(name="Buildwell Projects Ltd", address="MG Road, Bengaluru")
        facts = {
            "debt_amount": "1,20,00,000",
            "default_date": "2024-01-15",
            "invoices": "INV-101, INV-102, INV-108"
        }

        draft = StatutoryNoticeDraftingEngine.draft_notice(
            NoticeType.IBC_OPERATIONAL_CREDITOR_SEC_8, sender, recipient, facts
        )

        assert draft.mandatory_cure_period_days == 10
        assert "Section 8" in draft.full_notice_markdown
        assert "Section 9" in draft.full_notice_markdown
        assert "NCLT" in draft.full_notice_markdown
        assert "ten (10) days" in draft.full_notice_markdown

    def test_general_demand_notice_custom_days(self):
        """Test general demand notice supports customized cure timelines."""
        sender = NoticeParty(name="Author A", address="Delhi")
        recipient = NoticeParty(name="Publisher B", address="Mumbai")
        facts = {
            "subject": "Infringement of Copyright and Royalty Non-Payment",
            "grievance": "Unauthorized printing of 5,000 copies",
            "demand_text": "Cease distribution and account for profits",
            "cure_days": 7
        }

        draft = StatutoryNoticeDraftingEngine.draft_notice(
            NoticeType.GENERAL_LEGAL_DEMAND, sender, recipient, facts
        )

        assert draft.mandatory_cure_period_days == 7
        assert "7 days" in draft.full_notice_markdown
        assert "Infringement of Copyright" in draft.full_notice_markdown
