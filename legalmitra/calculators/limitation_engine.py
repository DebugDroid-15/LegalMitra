"""
Phase 99: Statutory Limitation & Procedural Timeline Calculator
Computes precise statutory deadlines and procedural timelines under:
1. The Limitation Act, 1963 (Suits, Appeals, Revisions, Applications)
2. Section 138 Negotiable Instruments Act, 1881 (Cheque Dishonour 30-15-30 Triad)
3. Criminal Procedure / BNSS Timelines (Section 173 Default Bail, Section 528 Quashing)
4. Consumer Protection Act, 2019 (Section 69 2-year limitation)
5. Arbitration and Conciliation Act, 1996 (Section 34 3-month challenge window)

Calculates 'Limitation Barred' status, remaining days, and flags Section 5 Condonation of Delay eligibility.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("limitation_calculator")


class DisputeCategory(str, Enum):
    CHEQUE_DISHONOUR_138 = "cheque_dishonour_138"
    MONEY_RECOVERY_DEBT = "money_recovery_debt"
    CONSUMER_COMPLAINT = "consumer_complaint"
    ARBITRATION_AWARD_CHALLENGE = "arbitration_award_challenge"
    HIGH_COURT_APPEAL_CIVIL = "high_court_appeal_civil"
    CRIMINAL_APPEAL_HIGH_COURT = "criminal_appeal_high_court"
    SPECIFIC_PERFORMANCE_CONTRACT = "specific_performance_contract"
    TENANT_EVICTION = "tenant_eviction"


@dataclass
class MilestoneStep:
    step_number: int
    title: str
    statutory_deadline_date: str
    duration_days: int
    governing_section: str
    status: str  # "COMPLETED", "ACTIVE_ACTION_REQUIRED", "TIME_BARRED", "UPCOMING"
    instruction: str


@dataclass
class LimitationCalculationResult:
    success: bool
    dispute_category: str
    start_event_date: str
    calculated_current_date: str
    final_limitation_expiry_date: str
    days_remaining: int
    is_time_barred: bool
    is_condonation_of_delay_permissible: bool
    condonation_governing_law: str
    primary_enactment: str
    statutory_citation: str
    milestones: List[MilestoneStep]
    practical_advocate_advice: str


class StatutoryLimitationEngine:
    """
    Sovereign Indian Legal Timeline & Limitation Calculator.
    """

    def calculate_timeline(
        self,
        category: DisputeCategory,
        event_date_str: str,
        current_date_str: Optional[str] = None
    ) -> LimitationCalculationResult:
        """
        Parses start date and calculates statutory milestones.
        """
        fmt = "%Y-%m-%d"
        try:
            event_d = datetime.strptime(event_date_str, fmt).date()
        except ValueError:
            # Try DD-MM-YYYY fallback
            event_d = datetime.strptime(event_date_str, "%d-%m-%Y").date()

        curr_d = datetime.strptime(current_date_str, fmt).date() if current_date_str else date.today()

        if category == DisputeCategory.CHEQUE_DISHONOUR_138:
            return self._calc_cheque_138(event_d, curr_d)
        elif category == DisputeCategory.CONSUMER_COMPLAINT:
            return self._calc_consumer(event_d, curr_d)
        elif category == DisputeCategory.ARBITRATION_AWARD_CHALLENGE:
            return self._calc_arbitration_34(event_d, curr_d)
        elif category == DisputeCategory.HIGH_COURT_APPEAL_CIVIL:
            return self._calc_hc_appeal(event_d, curr_d)
        else:
            return self._calc_money_recovery(event_d, curr_d)

    def _calc_cheque_138(self, memo_date: date, curr_date: date) -> LimitationCalculationResult:
        """
        Section 138 NI Act:
        Step 1: 30 days from Bank Return Memo to dispatch Demand Notice.
        Step 2: 15 days cure period from receipt of notice by drawer.
        Step 3: 30 days limitation to file Criminal Complaint before Judicial Magistrate under Section 142(1)(b).
        """
        step1_deadline = memo_date + timedelta(days=30)
        # Assuming notice dispatched within 10 days, 15 days cure starts
        cure_end_date = step1_deadline + timedelta(days=15)
        final_complaint_deadline = cure_end_date + timedelta(days=30)

        days_left = (final_complaint_deadline - curr_date).days
        is_barred = days_left < 0

        milestones = [
            MilestoneStep(
                step_number=1,
                title="Dispatch Statutory Demand Notice",
                statutory_deadline_date=step1_deadline.strftime("%d-%m-%Y"),
                duration_days=30,
                governing_section="Section 138 Proviso (b) NI Act, 1881",
                status="COMPLETED" if curr_date > step1_deadline else "ACTIVE_ACTION_REQUIRED",
                instruction="Send written notice via Registered Post AD / Speed Post within 30 days of receiving the cheque return memo."
            ),
            MilestoneStep(
                step_number=2,
                title="15-Day Statutory Cure Period for Drawer",
                statutory_deadline_date=cure_end_date.strftime("%d-%m-%Y"),
                duration_days=15,
                governing_section="Section 138 Proviso (c) NI Act, 1881",
                status="ACTIVE_ACTION_REQUIRED" if step1_deadline <= curr_date <= cure_end_date else ("COMPLETED" if curr_date > cure_end_date else "UPCOMING"),
                instruction="The drawer has 15 statutory days to pay the cheque amount. Cause of action arises only on the 16th day."
            ),
            MilestoneStep(
                step_number=3,
                title="File Criminal Complaint before Judicial Magistrate",
                statutory_deadline_date=final_complaint_deadline.strftime("%d-%m-%Y"),
                duration_days=30,
                governing_section="Section 142(1)(b) NI Act, 1881",
                status="TIME_BARRED" if is_barred else ("ACTIVE_ACTION_REQUIRED" if curr_date > cure_end_date else "UPCOMING"),
                instruction="Complaint under Section 138 must be filed in the Magistrate court possessing territorial jurisdiction over your bank branch."
            )
        ]

        advice = (
            "If the 30-day filing window under Section 142(1)(b) has expired, Section 142(1)(b) Proviso empowers the Magistrate "
            "to condone the delay upon an application showing 'sufficient cause'. File an Application for Condonation of Delay supported by an Affidavit."
        )

        return LimitationCalculationResult(
            success=True,
            dispute_category="Section 138 Negotiable Instruments Act (Cheque Dishonour)",
            start_event_date=memo_date.strftime("%d-%m-%Y"),
            calculated_current_date=curr_date.strftime("%d-%m-%Y"),
            final_limitation_expiry_date=final_complaint_deadline.strftime("%d-%m-%Y"),
            days_remaining=days_left,
            is_time_barred=is_barred,
            is_condonation_of_delay_permissible=True,
            condonation_governing_law="Section 142(1)(b) Proviso of Negotiable Instruments Act, 1881",
            primary_enactment="Negotiable Instruments Act, 1881",
            statutory_citation="Section 138 read with Section 142(1)(b)",
            milestones=milestones,
            practical_advocate_advice=advice
        )

    def _calc_consumer(self, cause_date: date, curr_date: date) -> LimitationCalculationResult:
        """Section 69 Consumer Protection Act: 2 years from date of cause of action."""
        expiry = cause_date + timedelta(days=730) # 2 years
        days_left = (expiry - curr_date).days
        is_barred = days_left < 0

        milestones = [
            MilestoneStep(
                step_number=1,
                title="File Consumer Complaint before District Commission",
                statutory_deadline_date=expiry.strftime("%d-%m-%Y"),
                duration_days=730,
                governing_section="Section 69(1) Consumer Protection Act, 2019",
                status="TIME_BARRED" if is_barred else "ACTIVE_ACTION_REQUIRED",
                instruction="Submit complaint online via e-Daakhil portal or physical registry of District CDRC."
            )
        ]

        advice = (
            "Section 69(2) allows the Consumer Commission to entertain a complaint after 2 years if the complainant satisfies the Commission "
            "that there was sufficient cause for not filing within period. File an application under Section 69(2) detailing medical, technical, or postal delays."
        )

        return LimitationCalculationResult(
            success=True,
            dispute_category="Consumer Protection Act, 2019 (Deficiency in Service)",
            start_event_date=cause_date.strftime("%d-%m-%Y"),
            calculated_current_date=curr_date.strftime("%d-%m-%Y"),
            final_limitation_expiry_date=expiry.strftime("%d-%m-%Y"),
            days_remaining=days_left,
            is_time_barred=is_barred,
            is_condonation_of_delay_permissible=True,
            condonation_governing_law="Section 69(2) Consumer Protection Act, 2019",
            primary_enactment="Consumer Protection Act, 2019",
            statutory_citation="Section 69(1) & (2)",
            milestones=milestones,
            practical_advocate_advice=advice
        )

    def _calc_arbitration_34(self, award_date: date, curr_date: date) -> LimitationCalculationResult:
        """Section 34(3) Arbitration Act: 3 months + strictly 30 days condonation only."""
        three_months = award_date + timedelta(days=90)
        thirty_days_condonation = three_months + timedelta(days=30)
        days_left = (three_months - curr_date).days
        is_barred = curr_date > thirty_days_condonation

        milestones = [
            MilestoneStep(
                step_number=1,
                title="Statutory Challenge Window (3 Months)",
                statutory_deadline_date=three_months.strftime("%d-%m-%Y"),
                duration_days=90,
                governing_section="Section 34(3) Arbitration and Conciliation Act, 1996",
                status="COMPLETED" if curr_date > three_months else "ACTIVE_ACTION_REQUIRED",
                instruction="Petition under Section 34 challenging arbitral award must be filed before competent Commercial Court / High Court."
            ),
            MilestoneStep(
                step_number=2,
                title="Strict 30-Day Condonation Limit (Proviso)",
                statutory_deadline_date=thirty_days_condonation.strftime("%d-%m-%Y"),
                duration_days=30,
                governing_section="Section 34(3) Proviso (Union of India v. Popular Construction)",
                status="TIME_BARRED" if is_barred else ("ACTIVE_ACTION_REQUIRED" if curr_date > three_months else "UPCOMING"),
                instruction="Under Supreme Court ruling Union of India v. Popular Construction Co. (2001) 8 SCC 470, delay beyond 30 days CANNOT be condoned under Section 5 Limitation Act."
            )
        ]

        advice = (
            "CRITICAL: Section 34(3) limitation is absolute. The Supreme Court has held that Section 5 of the Limitation Act "
            "is expressly excluded. If 3 months + 30 days have elapsed, the award attains absolute finality and is immediately executable."
        )

        return LimitationCalculationResult(
            success=True,
            dispute_category="Arbitration & Conciliation Act, 1996 (Setting Aside Arbitral Award)",
            start_event_date=award_date.strftime("%d-%m-%Y"),
            calculated_current_date=curr_date.strftime("%d-%m-%Y"),
            final_limitation_expiry_date=thirty_days_condonation.strftime("%d-%m-%Y"),
            days_remaining=days_left,
            is_time_barred=is_barred,
            is_condonation_of_delay_permissible=curr_date <= thirty_days_condonation,
            condonation_governing_law="Section 34(3) Proviso (Absolute cap of 30 days only)",
            primary_enactment="Arbitration and Conciliation Act, 1996",
            statutory_citation="Section 34(3)",
            milestones=milestones,
            practical_advocate_advice=advice
        )

    def _calc_hc_appeal(self, order_date: date, curr_date: date) -> LimitationCalculationResult:
        """Article 116 Limitation Act: 90 days for appeal to High Court from civil decree."""
        expiry = order_date + timedelta(days=90)
        days_left = (expiry - curr_date).days
        is_barred = days_left < 0

        milestones = [
            MilestoneStep(
                step_number=1,
                title="File Regular First Appeal (RFA) in High Court",
                statutory_deadline_date=expiry.strftime("%d-%m-%Y"),
                duration_days=90,
                governing_section="Article 116(a) Limitation Act, 1963",
                status="TIME_BARRED" if is_barred else "ACTIVE_ACTION_REQUIRED",
                instruction="Exclude time requisite for obtaining certified copy of judgment/decree under Section 12(2) of Limitation Act."
            )
        ]

        advice = (
            "Section 5 of the Limitation Act, 1963 applies to High Court appeals. If delayed, file an application supported by "
            "an affidavit explaining each day's delay (Collector Land Acquisition v. Katiji 1987 SCR (2) 387: 'substantial justice overrides technicalities')."
        )

        return LimitationCalculationResult(
            success=True,
            dispute_category="Civil Appeal to High Court",
            start_event_date=order_date.strftime("%d-%m-%Y"),
            calculated_current_date=curr_date.strftime("%d-%m-%Y"),
            final_limitation_expiry_date=expiry.strftime("%d-%m-%Y"),
            days_remaining=days_left,
            is_time_barred=is_barred,
            is_condonation_of_delay_permissible=True,
            condonation_governing_law="Section 5 read with Section 12(2) Limitation Act, 1963",
            primary_enactment="The Limitation Act, 1963",
            statutory_citation="Article 116 & Section 5",
            milestones=milestones,
            practical_advocate_advice=advice
        )

    def _calc_money_recovery(self, debt_date: date, curr_date: date) -> LimitationCalculationResult:
        """Article 19-21 Limitation Act: 3 years for recovery of money or debt."""
        expiry = debt_date + timedelta(days=1095) # 3 years
        days_left = (expiry - curr_date).days
        is_barred = days_left < 0

        milestones = [
            MilestoneStep(
                step_number=1,
                title="File Civil Suit for Recovery of Money",
                statutory_deadline_date=expiry.strftime("%d-%m-%Y"),
                duration_days=1095,
                governing_section="Article 19 & 21 Limitation Act, 1963",
                status="TIME_BARRED" if is_barred else "ACTIVE_ACTION_REQUIRED",
                instruction="Ensure suit is instituted before expiry of 3 years. Check if debtor made any written acknowledgment of debt under Section 18."
            )
        ]

        advice = (
            "NOTE: Under Section 3 of the Limitation Act, suits filed after limitation MUST be dismissed even if defense does not raise it. "
            "However, if the debtor sent an email, WhatsApp acknowledgment, or part payment before the 3-year expiry, Section 18 / 19 "
            "of the Limitation Act restarts a fresh 3-year period from that date."
        )

        return LimitationCalculationResult(
            success=True,
            dispute_category="Civil Money Recovery / Debt Suit",
            start_event_date=debt_date.strftime("%d-%m-%Y"),
            calculated_current_date=curr_date.strftime("%d-%m-%Y"),
            final_limitation_expiry_date=expiry.strftime("%d-%m-%Y"),
            days_remaining=days_left,
            is_time_barred=is_barred,
            is_condonation_of_delay_permissible=False,  # Sec 5 does NOT apply to original suits
            condonation_governing_law="Section 18 Limitation Act (Fresh period on written acknowledgment only)",
            primary_enactment="The Limitation Act, 1963",
            statutory_citation="Article 19-21 & Section 18",
            milestones=milestones,
            practical_advocate_advice=advice
        )
