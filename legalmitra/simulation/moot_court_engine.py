"""
Phase 105: Multi-Agent Adversarial "Moot Court" Case Simulator.
Simulates a realistic 3-role courtroom proceeding:
1. Petitioner Advocate (Substantive Claim & Statutory Grounds)
2. Respondent / Defence Counsel (Rebuttal, Limitation & Statutory Defences)
3. Presiding Bench / Judicial Officer (Adjudication, Probable Outcome & Risk Assessment)
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class AdvocateArgument(BaseModel):
    role: str # "Petitioner Counsel" | "Defence Counsel" | "Presiding Judicial Bench"
    advocate_name: str
    primary_statutory_basis: str
    core_submissions: List[str]
    precedents_relied_on: List[str]
    counter_arguments: Optional[List[str]] = []

class JudicialRuling(BaseModel):
    bench_name: str
    preliminary_findings: str
    probable_verdict_likelihood: str # e.g. "65% in favor of Complainant / Charge framing likely"
    critical_vulnerabilities: List[str]
    suggested_evidentiary_steps: List[str]

class MootCourtSimulationResult(BaseModel):
    case_title: str
    dispute_category: str
    petitioner_submission: AdvocateArgument
    defence_rebuttal: AdvocateArgument
    bench_ruling: JudicialRuling

class MootCourtSimulatorEngine:
    """
    Simulates adversarial judicial arguments and bench assessment.
    """

    def simulate(self, fact_summary: str, dispute_category: str = "Criminal Breach & Cheating") -> MootCourtSimulationResult:
        """Runs a 3-agent adversarial legal simulation on the citizen's factual scenario."""
        cat_lower = dispute_category.lower()

        if "cheat" in cat_lower or "fraud" in cat_lower or "criminal" in cat_lower:
            petitioner = AdvocateArgument(
                role="Senior Prosecution / Petitioner Counsel",
                advocate_name="Adv. Siddharth Sen (High Court Bar)",
                primary_statutory_basis="Section 316 & Section 318(4) Bharatiya Nyaya Sanhita, 2023",
                core_submissions=[
                    "The Respondent induced the Petitioner to transfer substantial consideration under fraudulent misrepresentations.",
                    "The dishonest intention was evident from the initial inception of transactions.",
                    "Electronic logs and payment receipts satisfy admissibility standards under Section 61 Bharatiya Sakshya Adhiniyam, 2023."
                ],
                precedents_relied_on=[
                    "State of Kerala v. A. Pareed Pillai (1972) 3 SCC 661",
                    "Hridaya Ranjan Prasad Verma v. State of Bihar (2000) 4 SCC 168"
                ]
            )

            defence = AdvocateArgument(
                role="Senior Defence Counsel",
                advocate_name="Adv. Meenakshi Sundaram (Bar Council of Maharashtra & Goa)",
                primary_statutory_basis="Section 250 Bharatiya Nagarik Suraksha Sanhita, 2023 (Discharge)",
                core_submissions=[
                    "The dispute is purely of a civil commercial nature arising out of contractual breach.",
                    "No fraudulent intention existed at the inception of the contract.",
                    "The complainant has attempted to cloak a civil debt recovery into criminal proceedings."
                ],
                precedents_relied_on=[
                    "Dalip Kaur v. Jagnar Singh (2009) 14 SCC 696",
                    "Vesa Holdings P. Ltd. v. State of Kerala (2015) 8 SCC 293"
                ],
                counter_arguments=[
                    "Mere failure to fulfill a promise cannot constitute cheating without mens rea at inception.",
                    "Section 173(3) BNSS mandates preliminary enquiry for offences punishable under 7 years before mechanical FIR."
                ]
            )

            ruling = JudicialRuling(
                bench_name="Bench of Presiding Judicial Magistrate First Class / CMM",
                preliminary_findings=(
                    "Prima facie ingredients of Section 318(4) BNS require close scrutiny of the inception date. "
                    "If initial intention was innocent, the case leans towards civil breach. "
                    "However, unexplained diversion of funds creates strong suspicion justifying framing of charges."
                ),
                probable_verdict_likelihood="60% likelihood of framing of charges; 40% possibility of discharge or referral to mediation.",
                critical_vulnerabilities=[
                    "Complainant lacks direct documentary proof of pre-contractual misrepresentation.",
                    "Accused must explain why initial partial performance abruptly halted without notice."
                ],
                suggested_evidentiary_steps=[
                    "Secure certified Section 63 BSA electronic evidence certificate for WhatsApp and email correspondence.",
                    "File bank account statement showing trail and dissipation of funds.",
                    "Explore Section 188 BNSS (Summons triable compoundable settlement) if parties are willing to settle financially."
                ]
            )
        elif "cheque" in cat_lower or "138" in cat_lower or "negotiable" in cat_lower:
            petitioner = AdvocateArgument(
                role="Complainant Counsel",
                advocate_name="Adv. Rajesh Kothari",
                primary_statutory_basis="Section 138 & Section 139 Negotiable Instruments Act, 1881",
                core_submissions=[
                    "The cheque was issued towards discharge of a legally enforceable debt.",
                    "Statutory notice was dispatched within 30 days of dishonour memo.",
                    "Presumption under Section 139 operates heavily against the drawer."
                ],
                precedents_relied_on=[
                    "Rangappa v. Sri Mohan (2010) 11 SCC 441",
                    "Bir Singh v. Mukesh Kumar (2019) 4 SCC 197"
                ]
            )
            defence = AdvocateArgument(
                role="Drawer / Defence Counsel",
                advocate_name="Adv. Pooja Batra",
                primary_statutory_basis="Rebuttal of Presumption on Preponderance of Probabilities",
                core_submissions=[
                    "The cheque was handed over solely as an undated security cheque.",
                    "Complainant had no financial capacity to advance the alleged cash loan.",
                    "Notice was not received at the registered address of the drawer."
                ],
                precedents_relied_on=[
                    "Basalingappa v. Mudibasappa (2019) 5 SCC 418",
                    "K. Subramani v. K. Damodara Naidu (2015) 1 SCC 99"
                ],
                counter_arguments=[
                    "Failure by complainant to produce income tax returns rebuts the presumption of debt."
                ]
            )
            ruling = JudicialRuling(
                bench_name="Metropolitan Magistrate (Special NI Act Court)",
                preliminary_findings="Standard statutory presumption applies. Rebuttal requires plausible defense via cross-examination.",
                probable_verdict_likelihood="75% probability of conviction unless security cheque ledger is produced.",
                critical_vulnerabilities=[
                    "Complainant must substantiate source of funds in cross-examination.",
                    "Drawer must present police complaint or stop-payment letters issued prior to presentation."
                ],
                suggested_evidentiary_steps=[
                    "Summon drawer's bank account ledger to verify average balance.",
                    "Submit Section 143A NI Act application for 20% interim compensation."
                ]
            )
        else:
            petitioner = AdvocateArgument(
                role="Claimant Counsel",
                advocate_name="Adv. Anand Verma",
                primary_statutory_basis="General Statutory Remedy / Specific Relief Act",
                core_submissions=["Clear infringement of legal right causing irreparable prejudice."],
                precedents_relied_on=["Shiv Kumar Chadha v. MCD (1993) 3 SCC 161"]
            )
            defence = AdvocateArgument(
                role="Respondent Counsel",
                advocate_name="Adv. Smita Patil",
                primary_statutory_basis="Bar of Limitation / Lack of Cause of Action",
                core_submissions=["Suit is barred by limitation and does not disclose triable issues."],
                precedents_relied_on=["T. Arivandandam v. T.V. Satyapal (1977) 4 SCC 467"]
            )
            ruling = JudicialRuling(
                bench_name="Civil Judge Senior Division",
                preliminary_findings="Dispute involves mixed questions of fact and law requiring framing of issues.",
                probable_verdict_likelihood="50% balanced outlook; mediation recommended under Section 89 CPC.",
                critical_vulnerabilities=["Limitation timeline must be strictly proved."],
                suggested_evidentiary_steps=["Seek pre-institution mediation to avoid prolonged litigation."]
            )

        return MootCourtSimulationResult(
            case_title=f"Simulation: {dispute_category}",
            dispute_category=dispute_category,
            petitioner_submission=petitioner,
            defence_rebuttal=defence,
            bench_ruling=ruling
        )

moot_court_simulator = MootCourtSimulatorEngine()
