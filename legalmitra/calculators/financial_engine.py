"""
Phase 101: Court Fee, MACT & RERA Compensation Estimator
Calculates accurate litigation costs, statutory court fees, and judicial compensation:
1. Ad-Valorem State Court Fees (Maharashtra Court Fees Act 1959, Delhi Court Fees Act)
2. Motor Accident Claims Tribunal (MACT) Statutory Multiplier Formula:
   - Sarla Verma v. DTC (2009) 6 SCC 121 (Multiplier Table based on Age)
   - National Insurance Co. Ltd. v. Pranay Sethi (2017) 16 SCC 680 (Future Prospects & Conventional Heads)
3. RERA Real Estate Delayed Possession Interest Calculator (Section 18 RERA: SBI MCLR + 2%)
4. Cheque Dishonour NI Act 138 Court Fee & Compensation limits (up to twice the cheque amount)
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("financial_compensation_engine")


class StateJurisdiction(str, Enum):
    MAHARASHTRA = "maharashtra"
    DELHI = "delhi"
    KARNATAKA = "karnataka"
    UTTAR_PRADESH = "uttar_pradesh"
    TAMIL_NADU = "tamil_nadu"
    ALL_INDIA_DEFAULT = "all_india_default"


class FinancialCalculatorType(str, Enum):
    CIVIL_COURT_FEE = "civil_court_fee"
    MACT_ACCIDENT_COMPENSATION = "mact_accident_compensation"
    RERA_DELAYED_POSSESSION = "rera_delayed_possession"
    CHEQUE_138_RECOVERY = "cheque_138_recovery"


@dataclass
class FinancialCalculationRequest:
    calc_type: FinancialCalculatorType
    state: StateJurisdiction = StateJurisdiction.MAHARASHTRA
    claim_amount: float = 0.0
    # MACT specific parameters
    victim_age: Optional[int] = None
    monthly_income: Optional[float] = None
    dependents_count: Optional[int] = None
    is_permanent_employed: Optional[bool] = True
    # RERA specific parameters
    total_amount_paid_to_builder: Optional[float] = None
    delay_months: Optional[int] = None
    sbi_mclr_rate_percent: float = 8.75


@dataclass
class CompensationHead:
    head_name: str
    amount_inr: float
    statutory_governance: str
    calculation_breakdown: str


@dataclass
class FinancialCalculationResult:
    success: bool
    calc_type: str
    state_jurisdiction: str
    total_estimated_amount: float
    formatted_total_inr: str
    primary_enactment: str
    landmark_precedent: Optional[str]
    breakdown_heads: List[CompensationHead]
    practical_guidance: str


class FinancialCompensationEngine:
    """
    Sovereign Indian Court Fee & Statutory Compensation Estimator.
    """

    # Sarla Verma (2009) 6 SCC 121 Age-Multiplier Table
    MACT_MULTIPLIER_TABLE = [
        (15, 20, 18),
        (21, 25, 18),
        (26, 30, 17),
        (31, 35, 16),
        (36, 40, 15),
        (41, 45, 14),
        (46, 50, 13),
        (51, 55, 11),
        (56, 60, 9),
        (61, 65, 7),
        (66, 120, 5)
    ]

    def calculate(self, req: FinancialCalculationRequest) -> FinancialCalculationResult:
        if req.calc_type == FinancialCalculatorType.MACT_ACCIDENT_COMPENSATION:
            return self._calculate_mact(req)
        elif req.calc_type == FinancialCalculatorType.RERA_DELAYED_POSSESSION:
            return self._calculate_rera(req)
        elif req.calc_type == FinancialCalculatorType.CHEQUE_138_RECOVERY:
            return self._calculate_cheque_138(req)
        else:
            return self._calculate_court_fee(req)

    def _get_mact_multiplier(self, age: int) -> int:
        for min_a, max_a, mult in self.MACT_MULTIPLIER_TABLE:
            if min_a <= age <= max_a:
                return mult
        return 5

    def _calculate_mact(self, req: FinancialCalculationRequest) -> FinancialCalculationResult:
        """
        Sarla Verma & Pranay Sethi Constitutional Multiplier Calculation.
        """
        age = req.victim_age or 30
        monthly = req.monthly_income or 30000.0
        annual_income = monthly * 12
        dependents = req.dependents_count or 3

        # 1. Future Prospects (Pranay Sethi)
        # Age < 40: 50% (permanent) / 40% (self-employed); Age 40-50: 30% / 25%; Age 50-60: 15% / 10%
        if age < 40:
            future_rate = 0.50 if req.is_permanent_employed else 0.40
        elif 40 <= age <= 50:
            future_rate = 0.30 if req.is_permanent_employed else 0.25
        elif 50 < age <= 60:
            future_rate = 0.15 if req.is_permanent_employed else 0.10
        else:
            future_rate = 0.0

        future_prospects_val = annual_income * future_rate
        gross_annual_income = annual_income + future_prospects_val

        # 2. Personal Living Expenses Deduction (Sarla Verma)
        # 2-3 dependents: 1/3rd deduction; 4-6 dependents: 1/4th deduction; 1 dependent: 1/2 deduction
        if dependents <= 1:
            deduction_factor = 0.50
        elif 2 <= dependents <= 3:
            deduction_factor = 1.0 / 3.0
        else:
            deduction_factor = 0.25

        net_annual_dependency = gross_annual_income * (1.0 - deduction_factor)
        multiplier = self._get_mact_multiplier(age)
        total_loss_of_dependency = round(net_annual_dependency * multiplier, 2)

        # 3. Conventional Heads (Pranay Sethi indexed)
        loss_of_consortium = 44000.0 * max(1, dependents)
        loss_of_estate = 16500.0
        funeral_expenses = 16500.0
        total_conventional = loss_of_consortium + loss_of_estate + funeral_expenses

        grand_total = round(total_loss_of_dependency + total_conventional, 2)

        heads = [
            CompensationHead(
                head_name="Loss of Financial Dependency",
                amount_inr=total_loss_of_dependency,
                statutory_governance="Section 166 Motor Vehicles Act, 1988 read with Sarla Verma (2009) 6 SCC 121",
                calculation_breakdown=f"Annual Income (INR {annual_income:,.0f}) + Future Prospects {future_rate*100:.0f}% (INR {future_prospects_val:,.0f}) - Personal Deduction ({deduction_factor*100:.1f}%) × Multiplier {multiplier}"
            ),
            CompensationHead(
                head_name="Loss of Consortium (Spousal / Parental / Filial)",
                amount_inr=loss_of_consortium,
                statutory_governance="Pranay Sethi (2017) 16 SCC 680 read with Magma General Insurance (2018) 18 SCC 130",
                calculation_breakdown=f"INR 44,000 per dependent for {dependents} legal dependents"
            ),
            CompensationHead(
                head_name="Loss of Estate & Funeral Expenses",
                amount_inr=loss_of_estate + funeral_expenses,
                statutory_governance="Constitution Bench guidelines in National Insurance Co. Ltd. v. Pranay Sethi",
                calculation_breakdown="Loss of Estate (INR 16,500) + Funeral Expenses (INR 16,500)"
            )
        ]

        guidance = (
            f"Under Section 166 of the Motor Vehicles Act, 1988, claims must be preferred before the Motor Accident Claims Tribunal (MACT) "
            f"having jurisdiction over the accident spot or claimant's residence. No limitation applies to motor accident claims (Section 166(3) repealed in 2019/2022). "
            f"Statutory interest @ 7.5% to 9% p.a. is payable from the date of filing petition till realization."
        )

        return FinancialCalculationResult(
            success=True,
            calc_type="MACT Fatal / Motor Accident Statutory Compensation",
            state_jurisdiction=req.state.value.title(),
            total_estimated_amount=grand_total,
            formatted_total_inr=f"INR {grand_total:,.2f}",
            primary_enactment="Motor Vehicles Act, 1988 (Section 166)",
            landmark_precedent="Sarla Verma (2009) 6 SCC 121 & Pranay Sethi (2017) 16 SCC 680",
            breakdown_heads=heads,
            practical_guidance=guidance
        )

    def _calculate_rera(self, req: FinancialCalculationRequest) -> FinancialCalculationResult:
        """Section 18 Real Estate (Regulation and Development) Act, 2016."""
        paid_amt = req.total_amount_paid_to_builder or 5000000.0
        months = req.delay_months or 24
        # SBI MCLR + 2% standard RERA rule
        applicable_rate = req.sbi_mclr_rate_percent + 2.0
        monthly_rate = (applicable_rate / 100.0) / 12.0

        total_interest = round(paid_amt * monthly_rate * months, 2)
        refund_total = round(paid_amt + total_interest, 2)

        heads = [
            CompensationHead(
                head_name="Principal Amount Paid to Promoter/Builder",
                amount_inr=paid_amt,
                statutory_governance="Section 18(1) Real Estate (Regulation and Development) Act, 2016",
                calculation_breakdown=f"Total payments made towards purchase of allottee apartment"
            ),
            CompensationHead(
                head_name="Statutory Delay Interest (SBI Highest MCLR + 2%)",
                amount_inr=total_interest,
                statutory_governance="Section 18(1) RERA read with Rule 18 State RERA Rules",
                calculation_breakdown=f"INR {paid_amt:,.0f} × {applicable_rate:.2f}% p.a. (SBI MCLR {req.sbi_mclr_rate_percent}% + 2%) for {months} months delay"
            )
        ]

        guidance = (
            "Under Section 18 of RERA, 2016 and Supreme Court ruling Newtech Promoters and Developers v. State of UP (2021), "
            "the homebuyer possesses an unconditional statutory right to seek either (1) Immediate monthly interest till possession is delivered, "
            "or (2) Complete refund of principal amount with interest without forfeiture of any booking deposit."
        )

        return FinancialCalculationResult(
            success=True,
            calc_type="RERA Delayed Flat Possession Compensation",
            state_jurisdiction=req.state.value.title(),
            total_estimated_amount=refund_total,
            formatted_total_inr=f"INR {refund_total:,.2f} (Refund + Interest)",
            primary_enactment="Real Estate (Regulation and Development) Act, 2016",
            landmark_precedent="Newtech Promoters and Developers v. State of U.P. (2021 INSC 732)",
            breakdown_heads=heads,
            practical_guidance=guidance
        )

    def _calculate_cheque_138(self, req: FinancialCalculationRequest) -> FinancialCalculationResult:
        """Section 138 NI Act Recovery Limits."""
        cheque_val = req.claim_amount or 100000.0
        max_fine = cheque_val * 2.0

        # Section 143A Interim Compensation (up to 20%)
        interim_comp_20 = round(cheque_val * 0.20, 2)

        heads = [
            CompensationHead(
                head_name="Cheque Face Value (Subsisting Debt)",
                amount_inr=cheque_val,
                statutory_governance="Section 138 Negotiable Instruments Act, 1881",
                calculation_breakdown="Principal cheque amount dishonoured by bank"
            ),
            CompensationHead(
                head_name="Interim Compensation at Trial Stage (Up to 20%)",
                amount_inr=interim_comp_20,
                statutory_governance="Section 143A Negotiable Instruments (Amendment) Act, 2018",
                calculation_breakdown=f"Court can order drawer to deposit 20% of cheque amount (INR {interim_comp_20:,.2f}) within 60 days of framing notice"
            ),
            CompensationHead(
                head_name="Maximum Penal Fine Awardable on Conviction",
                amount_inr=max_fine,
                statutory_governance="Section 138 substantive clause (Twice Cheque Amount)",
                calculation_breakdown=f"INR {cheque_val:,.0f} × 2 = INR {max_fine:,.0f} plus imprisonment up to 2 years"
            )
        ]

        guidance = (
            "In criminal proceedings under Section 138, the Magistrate can award compensation to the complainant out of the fine imposed "
            "under Section 357 CrPC / Section 395 BNSS. File an application under Section 143A NI Act as soon as the accused enters appearance."
        )

        return FinancialCalculationResult(
            success=True,
            calc_type="Section 138 NI Act Monetary Penalties & Compensation",
            state_jurisdiction=req.state.value.title(),
            total_estimated_amount=max_fine,
            formatted_total_inr=f"Up to INR {max_fine:,.2f} (2x Cheque Amount)",
            primary_enactment="Negotiable Instruments Act, 1881",
            landmark_precedent="Rakesh Ranjan Shrivastava v. State of Jharkhand (2024 INSC 206 - Sec 143A discretion)",
            breakdown_heads=heads,
            practical_guidance=guidance
        )

    def _calculate_court_fee(self, req: FinancialCalculationRequest) -> FinancialCalculationResult:
        """Ad-valorem civil court fees schedule."""
        suit_val = req.claim_amount or 500000.0

        # Maharashtra Court Fees Act 1959 Schedule I Article 1
        if req.state == StateJurisdiction.MAHARASHTRA:
            if suit_val <= 10000:
                fee = 200.0
            elif suit_val <= 50000:
                fee = 200.0 + (suit_val - 10000) * 0.05
            elif suit_val <= 100000:
                fee = 2200.0 + (suit_val - 50000) * 0.04
            elif suit_val <= 1000000:
                fee = 4200.0 + (suit_val - 100000) * 0.03
            else:
                fee = min(50000.0, 31200.0 + (suit_val - 1000000) * 0.02)
            act_name = "Maharashtra Court Fees Act, 1959 (Schedule I Article 1)"
            cap_note = "Maximum court fee in Maharashtra is capped at INR 50,000/- for most civil suits."

        # Delhi Court Fees Act
        elif req.state == StateJurisdiction.DELHI:
            if suit_val <= 10000:
                fee = suit_val * 0.075
            elif suit_val <= 100000:
                fee = 750.0 + (suit_val - 10000) * 0.06
            elif suit_val <= 500000:
                fee = 6150.0 + (suit_val - 100000) * 0.05
            else:
                fee = 26150.0 + (suit_val - 500000) * 0.04
            act_name = "Court Fees Act, 1870 (as applicable to the National Capital Territory of Delhi)"
            cap_note = "Ad-valorem scale without overall monetary ceiling in the Delhi High Court & District Courts."

        else:
            fee = min(suit_val * 0.05, 75000.0)
            act_name = f"State Court Fees & Suits Valuation Act ({req.state.value.title()})"
            cap_note = "Standard ad-valorem bracket subject to district civil court rules."

        fee = round(fee, 2)
        heads = [
            CompensationHead(
                head_name="Ad-Valorem Institution Court Fee",
                amount_inr=fee,
                statutory_governance=act_name,
                calculation_breakdown=f"Calculated upon suit valuation of INR {suit_val:,.2f}"
            )
        ]

        guidance = (
            f"Court fee stamps must be affixed or paid electronically via e-Courts GRAS / e-Challan portal before filing the plaint. "
            f"Under Section 16 of the Court Fees Act and Section 89 CPC, if the matter is settled through Lok Adalat or Mediation, "
            f"the court SHALL issue a certificate directing 100% refund of the full court fee paid."
        )

        return FinancialCalculationResult(
            success=True,
            calc_type="Civil Plaint Ad-Valorem Court Fee",
            state_jurisdiction=req.state.value.title(),
            total_estimated_amount=fee,
            formatted_total_inr=f"INR {fee:,.2f}",
            primary_enactment=act_name,
            landmark_precedent="Salem Advocate Bar Association v. Union of India (2005) 6 SCC 344",
            breakdown_heads=heads,
            practical_guidance=guidance
        )
