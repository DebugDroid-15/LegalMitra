"""
LegalMitra Historical and Temporal Law Engine
Models statutory lifecycles, section-wise phased commencements, amendment versioning,
repeal-with-savings transitions, and historical point-in-time querying.
"""

from __future__ import annotations

import datetime
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class TemporalStatus(str, Enum):
    ACTIVE = "active"
    UNCOMMENCED = "uncommenced"
    REPEALED_WITH_SAVINGS = "repealed_with_savings"
    REPEALED_WITHOUT_SAVINGS = "repealed_without_savings"
    AMENDED_HISTORICAL = "amended_historical"


@dataclass
class ProvisionTemporalVersion:
    provision_id: str
    statute_id: str
    section_number: str
    version_number: int
    text: str
    version_effective_from: Optional[str] = None  # YYYY-MM-DD
    version_effective_until: Optional[str] = None  # YYYY-MM-DD (None = currently in force)
    commencement_date: Optional[str] = None
    commencement_notification: Optional[str] = None
    repeal_date: Optional[str] = None
    repealing_enactment_id: Optional[str] = None
    savings_clause_ref: Optional[str] = None
    amendment_act_id: Optional[str] = None
    temporal_status: TemporalStatus = TemporalStatus.ACTIVE
    is_phased_commencement: bool = False
    savings_applies_to_pending: bool = False

    def is_operative_on(self, query_date_str: str) -> bool:
        """Determines if this version of the provision was legally operative on the given date."""
        try:
            q_date = datetime.date.fromisoformat(query_date_str)
        except ValueError:
            return False

        # If uncommenced
        if self.commencement_date:
            try:
                c_date = datetime.date.fromisoformat(self.commencement_date)
                if q_date < c_date:
                    return False
            except ValueError:
                return False
        else:
            # If no commencement date is specified, it has not commenced unless explicitly active
            if self.is_phased_commencement:
                return False

        # Check effective window
        if self.version_effective_from:
            try:
                from_date = datetime.date.fromisoformat(self.version_effective_from)
                if q_date < from_date:
                    return False
            except ValueError:
                return False

        if self.version_effective_until:
            try:
                until_date = datetime.date.fromisoformat(self.version_effective_until)
                if q_date > until_date:
                    return False
            except ValueError:
                return False

        # Check repeal
        if self.repeal_date:
            try:
                r_date = datetime.date.fromisoformat(self.repeal_date)
                if q_date >= r_date:
                    # If repealed, it is not currently operative as primary law, unless saved for pending matters
                    return False
            except ValueError:
                pass

        return True

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["temporal_status"] = self.temporal_status.value
        return d


@dataclass
class StatuteLifecycle:
    statute_id: str
    title: str
    enactment_date: Optional[str] = None
    assent_date: Optional[str] = None
    publication_date: Optional[str] = None
    commencement_date: Optional[str] = None
    commencement_notification: Optional[str] = None
    repeal_date: Optional[str] = None
    repealing_enactment_id: Optional[str] = None
    savings_clause_ref: Optional[str] = None
    is_fully_commenced: bool = True


class TemporalLawEngine:
    """Core engine for point-in-time legal queries and statutory lifecycle tracking."""

    def __init__(self):
        self._statutes: Dict[str, StatuteLifecycle] = {}
        self._versions: Dict[str, List[ProvisionTemporalVersion]] = {}

    def register_statute(self, statute: StatuteLifecycle) -> None:
        self._statutes[statute.statute_id] = statute

    def register_provision_version(self, version: ProvisionTemporalVersion) -> None:
        self._versions.setdefault(version.provision_id, []).append(version)
        # Keep versions ordered by version_number
        self._versions[version.provision_id].sort(key=lambda v: v.version_number)

    def get_statute(self, statute_id: str) -> Optional[StatuteLifecycle]:
        return self._statutes.get(statute_id)

    def query_provision_at_date(self, provision_id: str, query_date: str) -> Optional[ProvisionTemporalVersion]:
        """Returns the specific provision version operative on the requested date."""
        versions = self._versions.get(provision_id, [])
        for v in versions:
            if v.is_operative_on(query_date):
                return v
        return None

    def get_all_versions_for_provision(self, provision_id: str) -> List[ProvisionTemporalVersion]:
        return self._versions.get(provision_id, [])

    def resolve_criminal_law_regime(
        self,
        offence_date_str: str,
        proceedings_institute_date_str: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Resolves the substantive and procedural criminal regime based on the date of offence
        and the date of institution of proceedings under BNS/IPC and BNSS/CrPC.
        """
        TRANSITION_DATE = datetime.date(2024, 7, 1)

        try:
            offence_date = datetime.date.fromisoformat(offence_date_str)
        except ValueError:
            return {"error": f"Invalid offence_date: {offence_date_str}"}

        proc_date = None
        if proceedings_institute_date_str:
            try:
                proc_date = datetime.date.fromisoformat(proceedings_institute_date_str)
            except ValueError:
                return {"error": f"Invalid proceedings_institute_date: {proceedings_institute_date_str}"}

        # Substantive law (Article 20(1) Constitution of India: Ex post facto protection)
        if offence_date < TRANSITION_DATE:
            substantive_regime = "Indian Penal Code, 1860 (IPC)"
            substantive_rationale = (
                "Offence occurred prior to 1 July 2024. Governed by IPC under Article 20(1) "
                "of the Constitution and Section 358(2) of the Bharatiya Nyaya Sanhita, 2023."
            )
        else:
            substantive_regime = "Bharatiya Nyaya Sanhita, 2023 (BNS)"
            substantive_rationale = (
                "Offence occurred on or after 1 July 2024. Governed by BNS (Act No. 45 of 2023) "
                "commenced via S.O. 849(E)."
            )

        # Procedural law (BNSS s.531(2)(a) savings for pending investigations/trials)
        if proc_date and proc_date < TRANSITION_DATE:
            procedural_regime = "Code of Criminal Procedure, 1973 (CrPC)"
            procedural_rationale = (
                "Proceedings/investigation instituted prior to 1 July 2024. Continued under CrPC "
                "by virtue of the statutory savings clause in Section 531(2)(a) of the BNSS, 2023."
            )
            savings_applied = True
        elif proc_date and proc_date >= TRANSITION_DATE:
            procedural_regime = "Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)"
            procedural_rationale = (
                "Proceedings instituted on or after 1 July 2024. Governed by BNSS (Act No. 46 of 2023)."
            )
            savings_applied = False
        else:
            # If no proceeding date given, default based on offence date
            if offence_date < TRANSITION_DATE:
                procedural_regime = "Contingent on institution date: CrPC if instituted pre-01.07.2024; BNSS if post-01.07.2024"
                procedural_rationale = "Section 531(2)(a) of BNSS saves pending matters instituted before 1 July 2024."
                savings_applied = True
            else:
                procedural_regime = "Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)"
                procedural_rationale = "New proceedings for post-01.07.2024 offences fall under BNSS."
                savings_applied = False

        return {
            "offence_date": offence_date_str,
            "proceedings_institute_date": proceedings_institute_date_str,
            "substantive_law": substantive_regime,
            "substantive_rationale": substantive_rationale,
            "procedural_law": procedural_regime,
            "procedural_rationale": procedural_rationale,
            "bnss_s531_savings_applied": savings_applied,
        }

    def resolve_data_protection_regime(self, query_date_str: str) -> Dict[str, Any]:
        """
        Resolves whether IT Act Section 43A or DPDP Act substantive provisions apply
        at a given point in time.
        """
        try:
            q_date = datetime.date.fromisoformat(query_date_str)
        except ValueError:
            return {"error": f"Invalid query_date: {query_date_str}"}

        # DPDP Act was enacted 2023-08-11, but Section 1(2) stipulates phased commencement.
        # Substantive data protection provisions and Section 44(2) omission of Section 43A IT Act
        # remain unappointed as of early 2026.
        return {
            "query_date": query_date_str,
            "dpdp_enactment_date": "2023-08-11",
            "dpdp_status": "Enacted; substantive penalty and adjudication sections uncommenced pending s.1(2) notification",
            "it_act_s43a_status": "Operative in law (Compensation for failure to protect sensitive personal data)",
            "governing_remedy": "Section 43A of Information Technology Act, 2000 read with SPDI Rules, 2011",
            "legal_note": "DPDP Section 44(2) omits Section 43A of IT Act only when formally brought into force via Gazette notification."
        }

    def resolve_specific_relief_regime(self, contract_date_str: str) -> Dict[str, Any]:
        """
        Resolves whether Specific Relief Act 1963 pre-2018 (discretionary) or
        post-2018 (mandatory) regime applies based on date.
        """
        TRANSITION_DATE = datetime.date(2018, 10, 1)
        try:
            c_date = datetime.date.fromisoformat(contract_date_str)
        except ValueError:
            return {"error": f"Invalid date: {contract_date_str}"}

        if c_date < TRANSITION_DATE:
            return {
                "date": contract_date_str,
                "regime": "Specific Relief Act, 1963 (Pre-2018 Amendment)",
                "specific_performance_character": "Equitable and Discretionary (former Section 20)",
                "infrastructure_bar_active": False,
                "governing_provision": "Section 10 (as unamended, subject to court discretion under former s.20)",
                "notification_ref": "Prior to S.O. 4888(E)",
            }
        else:
            return {
                "date": contract_date_str,
                "regime": "Specific Relief Act, 1963 (Post-2018 Amendment by Act 18 of 2018)",
                "specific_performance_character": "Mandatory Statutory Rule ('shall be enforced')",
                "infrastructure_bar_active": True,
                "governing_provision": "Section 10 (substituted) read with Section 20A (statutory bar on infrastructure injunctions)",
                "notification_ref": "S.O. 4888(E) dated 19 September 2018, effective 1 October 2018",
            }

    def resolve_arbitration_regime(self, arbitration_commence_date_str: str) -> Dict[str, Any]:
        """
        Resolves whether Arbitration & Conciliation Act 1996 pre-2015 or post-2015
        amendment applies to arbitral proceedings.
        """
        TRANSITION_DATE = datetime.date(2015, 10, 23)
        try:
            a_date = datetime.date.fromisoformat(arbitration_commence_date_str)
        except ValueError:
            return {"error": f"Invalid date: {arbitration_commence_date_str}"}

        if a_date < TRANSITION_DATE:
            return {
                "date": arbitration_commence_date_str,
                "regime": "Arbitration and Conciliation Act, 1996 (Pre-2015 Amendment)",
                "s34_patent_illegality_scope": "Broad public policy review (ONGC v. Saw Pipes standard)",
                "s29a_timeline_mandate": False,
                "merits_review_expressly_barred": False,
            }
        else:
            return {
                "date": arbitration_commence_date_str,
                "regime": "Arbitration and Conciliation Act, 1996 (Post-2015 Amendment by Act 3 of 2016)",
                "s34_patent_illegality_scope": "Restricted patent illegality (domestic awards only; patent on the face of award)",
                "s29a_timeline_mandate": True,
                "merits_review_expressly_barred": True,
                "notification_ref": "Commenced 23 October 2015 via Ordinance / Act No. 3 of 2016",
            }

    def resolve_consumer_regime(self, cause_of_action_date_str: str) -> Dict[str, Any]:
        """
        Resolves whether Consumer Protection Act 1986 or 2019 applies based on date.
        """
        TRANSITION_DATE = datetime.date(2020, 7, 20)
        try:
            coa_date = datetime.date.fromisoformat(cause_of_action_date_str)
        except ValueError:
            return {"error": f"Invalid date: {cause_of_action_date_str}"}

        if coa_date < TRANSITION_DATE:
            return {
                "date": cause_of_action_date_str,
                "regime": "Consumer Protection Act, 1986",
                "repealed": True,
                "savings_applicable": True,
                "product_liability_statutory_claim": False,
                "central_regulator_ccpa": False,
                "savings_ref": "Consumer Protection Act, 2019 Section 107(2) saves pre-existing complaints",
            }
        else:
            return {
                "date": cause_of_action_date_str,
                "regime": "Consumer Protection Act, 2019 (Act No. 35 of 2019)",
                "repealed": False,
                "product_liability_statutory_claim": True,
                "central_regulator_ccpa": True,
                "commencement_notification": "S.O. 2351(E) dated 15 July 2020, effective 20 July 2020",
            }

    def resolve_companies_act_csr_regime(self, query_date_str: str) -> Dict[str, Any]:
        """Resolves whether Companies Act Section 135 CSR comply-or-explain (pre-2021)
        or mandatory unspent account transfer and civil penalties (post-2021) apply.
        """
        TRANSITION_DATE = datetime.date(2021, 1, 22)
        try:
            q_date = datetime.date.fromisoformat(query_date_str)
        except ValueError:
            return {"error": f"Invalid query_date: {query_date_str}"}

        if q_date < TRANSITION_DATE:
            return {
                "date": query_date_str,
                "regime": "Companies Act, 2013 (Pre-2020 Amendment)",
                "csr_character": "Comply or explain disclosure in Board report under Section 134(3)(o)",
                "penalty_type": "Criminal general penalty under Section 450",
                "unspent_transfer_mandate": False,
                "governing_provision": "Section 135 as enacted by Act 18 of 2013",
            }
        else:
            return {
                "date": query_date_str,
                "regime": "Companies Act, 2013 (Post-2020 Amendment by Act 29 of 2020)",
                "csr_character": "Mandatory spending and unspent account transfer under Section 135(6)",
                "penalty_type": "Civil monetary administrative penalty under Section 135(7)",
                "unspent_transfer_mandate": True,
                "governing_provision": "Section 135 as amended by Act 29 of 2020 w.e.f. 22 January 2021",
                "notification_ref": "Ministry of Corporate Affairs S.O. 325(E) dated 22 January 2021",
            }

    def resolve_ibc_clean_slate_regime(self, query_date_str: str) -> Dict[str, Any]:
        """Resolves whether Section 32A clean-slate immunity under IBC applies based on date."""
        TRANSITION_DATE = datetime.date(2019, 12, 28)
        try:
            q_date = datetime.date.fromisoformat(query_date_str)
        except ValueError:
            return {"error": f"Invalid query_date: {query_date_str}"}

        if q_date < TRANSITION_DATE:
            return {
                "date": query_date_str,
                "regime": "Insolvency and Bankruptcy Code, 2016 (Pre-Section 32A)",
                "clean_slate_statutory_immunity": False,
                "asset_attachment_bar": False,
                "governing_rule": "Absence of express statutory immunity; governed by general law and NCLT approval orders",
            }
        else:
            return {
                "date": query_date_str,
                "regime": "Insolvency and Bankruptcy Code, 2016 (Post-Section 32A Insertion)",
                "clean_slate_statutory_immunity": True,
                "asset_attachment_bar": True,
                "governing_rule": "Section 32A immunizes corporate debtor and new management from pre-CIRP offences; bars attachment of debtor properties",
                "notification_ref": "Inserted by Ordinance on 28 December 2019 / Act No. 1 of 2020",
            }

    def resolve_contract_section28_regime(self, agreement_date_str: str) -> Dict[str, Any]:
        """Resolves whether Contract Act Section 28 pre-1997 (Vulcan Insurance doctrine)
        or post-1997 (extinguishment clauses void) applies.
        """
        TRANSITION_DATE = datetime.date(1997, 1, 8)
        try:
            a_date = datetime.date.fromisoformat(agreement_date_str)
        except ValueError:
            return {"error": f"Invalid agreement_date: {agreement_date_str}"}

        if a_date < TRANSITION_DATE:
            return {
                "date": agreement_date_str,
                "regime": "Indian Contract Act, 1872 (Pre-1997 Amendment)",
                "extinguishment_clause_valid": True,
                "doctrine": "Vulcan Insurance doctrine: contractual clauses extinguishing rights after stipulated period were lawful",
                "clause_b_active": False,
            }
        else:
            return {
                "date": agreement_date_str,
                "regime": "Indian Contract Act, 1872 (Post-1997 Amendment by Act 1 of 1997)",
                "extinguishment_clause_valid": False,
                "doctrine": "Section 28 clause (b) renders void any clause extinguishing rights on expiry of period",
                "clause_b_active": True,
                "statutory_ref": "Indian Contract (Amendment) Act, 1997 (Act No. 1 of 1997) w.e.f. 8 January 1997",
            }

    def resolve_tpa_part_performance_regime(self, agreement_date_str: str) -> Dict[str, Any]:
        """Resolves whether Transfer of Property Act Section 53A requires mandatory registration."""
        TRANSITION_DATE = datetime.date(2001, 9, 24)
        try:
            a_date = datetime.date.fromisoformat(agreement_date_str)
        except ValueError:
            return {"error": f"Invalid agreement_date: {agreement_date_str}"}

        if a_date < TRANSITION_DATE:
            return {
                "date": agreement_date_str,
                "regime": "Transfer of Property Act, 1882 (Pre-2001 Amendment)",
                "mandatory_registration": False,
                "s53a_protection_unregistered": True,
                "registration_act_s17_1a_required": False,
            }
        else:
            return {
                "date": agreement_date_str,
                "regime": "Transfer of Property Act, 1882 (Post-2001 Amendment by Act 48 of 2001)",
                "mandatory_registration": True,
                "s53a_protection_unregistered": False,
                "registration_act_s17_1a_required": True,
                "governing_rule": "Contract for transfer of immoveable property must be registered to claim Section 53A defense",
                "notification_ref": "Act No. 48 of 2001 w.e.f. 24 September 2001",
            }

    def resolve_cpc_commercial_timeline(self, is_commercial_dispute: bool, days_elapsed: int) -> Dict[str, Any]:
        """Resolves written statement filing deadlines under CPC Order VIII Rule 1
        distinguishing ordinary civil suits from commercial suits.
        """
        if not is_commercial_dispute:
            condonable = True
            forfeited = False
            rationale = "In ordinary civil suits, the 30-90 day timeline under Order VIII Rule 1 is directory (Kailash v. Nanhku)."
        else:
            condonable = days_elapsed <= 120
            forfeited = days_elapsed > 120
            rationale = "In commercial disputes of Specified Value, Order VIII Rule 1 second proviso strictly forfeits the right after 120 days (SCG Contracts)."

        return {
            "is_commercial_dispute": is_commercial_dispute,
            "days_elapsed": days_elapsed,
            "within_initial_period": days_elapsed <= 30,
            "within_extended_period": days_elapsed <= (120 if is_commercial_dispute else 90),
            "delay_condonable": condonable,
            "right_to_file_forfeited": forfeited,
            "procedural_rationale": rationale,
        }

    def resolve_mva_compensation_regime(self, accident_date_str: str) -> Dict[str, Any]:
        """Resolves whether Motor Vehicles Act Section 163A (structured formula)
        or Section 164 (fixed no-fault sum) applies based on accident date.
        """
        TRANSITION_DATE = datetime.date(2022, 4, 1)
        try:
            a_date = datetime.date.fromisoformat(accident_date_str)
        except ValueError:
            return {"error": f"Invalid accident_date: {accident_date_str}"}

        if a_date < TRANSITION_DATE:
            return {
                "date": accident_date_str,
                "regime": "Motor Vehicles Act, 1988 (Pre-2019 Amendment Chapter XI / Section 163A)",
                "governing_section": "Section 163A read with Second Schedule",
                "basis": "Structured formula compensation with annual income cap of INR 40,000",
                "fixed_no_fault_sum": None,
            }
        else:
            return {
                "date": accident_date_str,
                "regime": "Motor Vehicles Act, 1988 (Post-2019 Amendment Section 164)",
                "governing_section": "Section 164 substituted by Act 32 of 2019",
                "basis": "Fixed no-fault statutory compensation: INR 5,00,000 for death, INR 2,50,000 for grievous hurt",
                "fixed_sum_death": 500000,
                "fixed_sum_grievous_hurt": 250000,
                "notification_ref": "Ministry of Road Transport and Highways S.O. 859(E) dated 25 February 2022, effective 1 April 2022",
            }




def build_default_temporal_engine() -> TemporalLawEngine:
    """Pre-configures known statutory timelines for Indian law."""
    engine = TemporalLawEngine()

    # 1. Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)
    engine.register_statute(StatuteLifecycle(
        statute_id="IND-STAT-BNSS-2023",
        title="Bharatiya Nagarik Suraksha Sanhita, 2023",
        enactment_date="2023-12-25",
        assent_date="2023-12-25",
        publication_date="2023-12-25",
        commencement_date="2024-07-01",
        commencement_notification="S.O. 848(E) dated 23 February 2024",
        repealing_enactment_id=None,
        is_fully_commenced=True,
    ))

    # 2. Code of Criminal Procedure, 1973 (CrPC)
    engine.register_statute(StatuteLifecycle(
        statute_id="IND-STAT-CRPC-1973",
        title="Code of Criminal Procedure, 1973",
        enactment_date="1974-01-25",
        commencement_date="1974-04-01",
        repeal_date="2024-07-01",
        repealing_enactment_id="IND-STAT-BNSS-2023",
        savings_clause_ref="BNSS Section 531(2)(a)",
        is_fully_commenced=True,
    ))

    # 3. Bharatiya Sakshya Adhiniyam, 2023 (BSA)
    engine.register_statute(StatuteLifecycle(
        statute_id="IND-STAT-BSA-2023",
        title="Bharatiya Sakshya Adhiniyam, 2023",
        enactment_date="2023-12-25",
        assent_date="2023-12-25",
        commencement_date="2024-07-01",
        commencement_notification="S.O. 850(E) dated 23 February 2024",
        is_fully_commenced=True,
    ))

    # 4. Indian Evidence Act, 1872 (IEA)
    engine.register_statute(StatuteLifecycle(
        statute_id="IND-STAT-IEA-1872",
        title="Indian Evidence Act, 1872",
        enactment_date="1872-03-15",
        commencement_date="1872-09-01",
        repeal_date="2024-07-01",
        repealing_enactment_id="IND-STAT-BSA-2023",
        savings_clause_ref="BSA Section 170(2)",
        is_fully_commenced=True,
    ))

    # 5. Digital Personal Data Protection Act, 2023 (DPDP)
    engine.register_statute(StatuteLifecycle(
        statute_id="IND-STAT-DPDP-2023",
        title="Digital Personal Data Protection Act, 2023",
        enactment_date="2023-08-11",
        assent_date="2023-08-11",
        publication_date="2023-08-11",
        commencement_date=None,  # Phased
        is_fully_commenced=False,
    ))

    # 6. Information Technology Act, 2000 (IT Act)
    engine.register_statute(StatuteLifecycle(
        statute_id="IND-STAT-IT-2000",
        title="Information Technology Act, 2000",
        enactment_date="2000-06-09",
        commencement_date="2000-10-17",
        commencement_notification="S.O. 934(E)",
        is_fully_commenced=True,
    ))

    # 7. Specific Relief Act, 1963 (SRA)
    engine.register_statute(StatuteLifecycle(
        statute_id="IND-STAT-SRA-1963",
        title="Specific Relief Act, 1963",
        enactment_date="1963-12-13",
        commencement_date="1964-03-01",
        is_fully_commenced=True,
    ))

    # 8. Arbitration and Conciliation Act, 1996 (ARB)
    engine.register_statute(StatuteLifecycle(
        statute_id="IND-STAT-ARB-1996",
        title="Arbitration and Conciliation Act, 1996",
        enactment_date="1996-08-16",
        commencement_date="1996-08-22",
        is_fully_commenced=True,
    ))

    # 9. Consumer Protection Act, 1986 (CPA 1986)
    engine.register_statute(StatuteLifecycle(
        statute_id="IND-STAT-CPA-1986",
        title="Consumer Protection Act, 1986",
        enactment_date="1986-12-24",
        commencement_date="1987-04-15",
        repeal_date="2020-07-20",
        repealing_enactment_id="IND-STAT-CPA-2019",
        savings_clause_ref="CPA 2019 Section 107(2)",
        is_fully_commenced=True,
    ))

    # 10. Consumer Protection Act, 2019 (CPA 2019)
    engine.register_statute(StatuteLifecycle(
        statute_id="IND-STAT-CPA-2019",
        title="Consumer Protection Act, 2019",
        enactment_date="2019-08-09",
        assent_date="2019-08-09",
        commencement_date="2020-07-20",
        commencement_notification="S.O. 2351(E) dated 15 July 2020",
        is_fully_commenced=True,
    ))

    # 11. Indian Penal Code, 1860 (IPC)
    engine.register_statute(StatuteLifecycle(
        statute_id="IND-STAT-IPC-1860",
        title="Indian Penal Code, 1860",
        enactment_date="1860-10-06",
        commencement_date="1862-01-01",
        repeal_date="2024-07-01",
        repealing_enactment_id="IND-STAT-BNS-2023",
        savings_clause_ref="BNS Section 358(2)",
        is_fully_commenced=True,
    ))

    # 12. Bharatiya Nyaya Sanhita, 2023 (BNS)
    engine.register_statute(StatuteLifecycle(
        statute_id="IND-STAT-BNS-2023",
        title="Bharatiya Nyaya Sanhita, 2023",
        enactment_date="2023-12-25",
        assent_date="2023-12-25",
        commencement_date="2024-07-01",
        commencement_notification="S.O. 849(E)",
        is_fully_commenced=True,
    ))

    # 13. Constitution of India (CONST)
    engine.register_statute(StatuteLifecycle(
        statute_id="IND-CONST-1950",
        title="The Constitution of India",
        enactment_date="1949-11-26",
        commencement_date="1950-01-26",
        is_fully_commenced=True,
    ))

    # Register Provision Versions:
    # IT Act Section 43A (Operative from 2009-10-27 to Present)
    engine.register_provision_version(ProvisionTemporalVersion(
        provision_id="IT-ACT-SEC-43A",
        statute_id="IND-STAT-IT-2000",
        section_number="43A",
        version_number=1,
        text="Compensation for failure to protect data: Where a body corporate possessing, dealing or handling any sensitive personal data or information in a computer resource which it owns, controls or operates, is negligent in implementing and maintaining reasonable security practices and procedures and thereby causes wrongful loss or wrongful gain to any person, such body corporate shall be liable to pay damages by way of compensation to the person so affected.",
        version_effective_from="2009-10-27",
        version_effective_until=None,  # Remains operative until DPDP s.44(2) notification
        commencement_date="2009-10-27",
        commencement_notification="IT (Amendment) Act 2008 Notification",
        temporal_status=TemporalStatus.ACTIVE,
    ))

    # BNSS Section 531 (Operative from 2024-07-01 to Present)
    engine.register_provision_version(ProvisionTemporalVersion(
        provision_id="BNSS-SEC-531",
        statute_id="IND-STAT-BNSS-2023",
        section_number="531",
        version_number=1,
        text="531. (1) The Code of Criminal Procedure, 1973 is hereby repealed. (2) Notwithstanding such repeal,— (a) if, immediately before the date on which this Sanhita comes into force, there is any appeal, application, trial, inquiry or investigation pending, then, such appeal, application, trial, inquiry or investigation shall be disposed of, continued, held or made, as the case may be, in accordance with the provisions of the Code of Criminal Procedure, 1973, as in force immediately before such commencement, as if this Sanhita had not come into force;",
        version_effective_from="2024-07-01",
        version_effective_until=None,
        commencement_date="2024-07-01",
        commencement_notification="S.O. 848(E)",
        temporal_status=TemporalStatus.ACTIVE,
        savings_applies_to_pending=True,
    ))

    # BSA Section 63 (Operative from 2024-07-01 to Present)
    engine.register_provision_version(ProvisionTemporalVersion(
        provision_id="BSA-SEC-63",
        statute_id="IND-STAT-BSA-2023",
        section_number="63",
        version_number=1,
        text="63. (1) Notwithstanding anything contained in this Adhiniyam, any information contained in an electronic record which is printed on a paper, stored, recorded or copied in optical or magnetic media or each or other form of electronic device shall be deemed to be also a document... (4) In any proceeding where it is desired to give a statement in evidence by virtue of this section, a certificate doing any of the following things, that is to say,— (a) identifying the electronic record containing the statement...",
        version_effective_from="2024-07-01",
        version_effective_until=None,
        commencement_date="2024-07-01",
        commencement_notification="S.O. 850(E)",
        temporal_status=TemporalStatus.ACTIVE,
    ))

    # IEA Section 65B (Historical Version: 2000-10-17 to 2024-06-30)
    engine.register_provision_version(ProvisionTemporalVersion(
        provision_id="IEA-SEC-65B",
        statute_id="IND-STAT-IEA-1872",
        section_number="65B",
        version_number=1,
        text="65B. Admissibility of electronic records.— (1) Notwithstanding anything contained in this Act, any information contained in an electronic record which is printed on a paper, stored, recorded or copied in optical or magnetic media produced by a computer shall be deemed to be also a document... (4) In any proceedings where it is desired to give a statement in evidence by virtue of this section, a certificate doing any of the following things...",
        version_effective_from="2000-10-17",
        version_effective_until="2024-06-30",
        commencement_date="2000-10-17",
        repeal_date="2024-07-01",
        repealing_enactment_id="IND-STAT-BSA-2023",
        savings_clause_ref="BSA Section 170(2)",
        temporal_status=TemporalStatus.REPEALED_WITH_SAVINGS,
        savings_applies_to_pending=True,
    ))

    # SRA Section 10 (Historical Discretionary Version: 1964-03-01 to 2018-09-30)
    engine.register_provision_version(ProvisionTemporalVersion(
        provision_id="SRA-SEC-10",
        statute_id="IND-STAT-SRA-1963",
        section_number="10",
        version_number=1,
        text="10. Cases in which specific performance of contract enforceable.—Except as otherwise provided in this Chapter, the specific performance of any contract may, in the discretion of the court, be enforced...",
        version_effective_from="1964-03-01",
        version_effective_until="2018-09-30",
        commencement_date="1964-03-01",
        temporal_status=TemporalStatus.AMENDED_HISTORICAL,
    ))

    # SRA Section 10 (Current Mandatory Version: 2018-10-01 to Present)
    engine.register_provision_version(ProvisionTemporalVersion(
        provision_id="SRA-SEC-10",
        statute_id="IND-STAT-SRA-1963",
        section_number="10",
        version_number=2,
        text="10. Specific performance in respect of contracts.—The specific performance of a contract shall be enforced by the court subject to the provisions contained in sub-section (2) of section 11, section 14 and section 16.",
        version_effective_from="2018-10-01",
        version_effective_until=None,
        commencement_date="2018-10-01",
        commencement_notification="S.O. 4888(E) dated 19 September 2018",
        amendment_act_id="IND-AMEND-SRA-2018",
        temporal_status=TemporalStatus.ACTIVE,
    ))

    # SRA Section 20A (Inserted by Act 18 of 2018: 2018-10-01 to Present)
    engine.register_provision_version(ProvisionTemporalVersion(
        provision_id="SRA-SEC-20A",
        statute_id="IND-STAT-SRA-1963",
        section_number="20A",
        version_number=1,
        text="20A. Special provisions for contract relating to infrastructure project.—(1) No injunction shall be granted by court in a suit under this Act where granting injunction would cause impediment or delay in the progress or completion of such infrastructure project.",
        version_effective_from="2018-10-01",
        version_effective_until=None,
        commencement_date="2018-10-01",
        commencement_notification="S.O. 4888(E)",
        amendment_act_id="IND-AMEND-SRA-2018",
        temporal_status=TemporalStatus.ACTIVE,
    ))

    # ARB Section 34 (Historical Version: 1996-08-22 to 2015-10-22)
    engine.register_provision_version(ProvisionTemporalVersion(
        provision_id="ARB-SEC-34",
        statute_id="IND-STAT-ARB-1996",
        section_number="34",
        version_number=1,
        text="34. Application for setting aside arbitral award.—(1) Recourse to a Court against an arbitral award may be made only by an application for setting aside such award in accordance with sub-section (2) and sub-section (3)...",
        version_effective_from="1996-08-22",
        version_effective_until="2015-10-22",
        commencement_date="1996-08-22",
        temporal_status=TemporalStatus.AMENDED_HISTORICAL,
    ))

    # ARB Section 34 (Current Version post-2015 Amendment: 2015-10-23 to Present)
    engine.register_provision_version(ProvisionTemporalVersion(
        provision_id="ARB-SEC-34",
        statute_id="IND-STAT-ARB-1996",
        section_number="34",
        version_number=2,
        text="34. Application for setting aside arbitral award.—... (2A) An arbitral award arising out of an arbitration other than an international commercial arbitration, may also be set aside by the Court, if the Court finds that the award is vitiated by patent illegality appearing on the face of the award: Provided that an award shall not be set aside merely on the ground of an erroneous application of the law or by reappreciation of evidence.",
        version_effective_from="2015-10-23",
        version_effective_until=None,
        commencement_date="2015-10-23",
        amendment_act_id="IND-AMEND-ARB-2015",
        temporal_status=TemporalStatus.ACTIVE,
    ))

    # ARB Section 29A (Inserted by Act 3 of 2016: 2015-10-23 to Present)
    engine.register_provision_version(ProvisionTemporalVersion(
        provision_id="ARB-SEC-29A",
        statute_id="IND-STAT-ARB-1996",
        section_number="29A",
        version_number=1,
        text="29A. Time limit for arbitral award.—(1) The award in matters other than international commercial arbitration shall be made by the arbitral tribunal within a period of twelve months from the date of completion of pleadings under sub-section (4) of section 23...",
        version_effective_from="2015-10-23",
        version_effective_until=None,
        commencement_date="2015-10-23",
        amendment_act_id="IND-AMEND-ARB-2015",
        temporal_status=TemporalStatus.ACTIVE,
    ))

    # CONST Article 330A (Inserted by 106th Amendment: 2023-09-28 to Present)
    engine.register_provision_version(ProvisionTemporalVersion(
        provision_id="CONST-ART-330A",
        statute_id="IND-CONST-1950",
        section_number="330A",
        version_number=1,
        text="330A. Reservation of seats for women in the House of the People.—(1) Seats shall be reserved for women in the House of the People. (2) As nearly as may be, one-third of the total number of seats reserved under clause (2) of article 330 shall be reserved for women...",
        version_effective_from="2023-09-28",
        version_effective_until=None,
        commencement_date="2023-09-28",
        amendment_act_id="IND-AMEND-CONST-106",
        temporal_status=TemporalStatus.ACTIVE,
    ))

    # --- BATCH 2 STATUTES & PROVISIONS ---
    # 14. Companies Act, 2013
    engine.register_statute(StatuteLifecycle(
        statute_id="IND-STAT-COMP-2013",
        title="Companies Act, 2013",
        enactment_date="2013-08-29",
        assent_date="2013-08-29",
        commencement_date="2013-09-12",
        commencement_notification="Phased enforcement via MCA notifications",
        is_fully_commenced=True,
    ))

    # 15. Insolvency and Bankruptcy Code, 2016
    engine.register_statute(StatuteLifecycle(
        statute_id="IND-STAT-IBC-2016",
        title="Insolvency and Bankruptcy Code, 2016",
        enactment_date="2016-05-28",
        assent_date="2016-05-28",
        commencement_date="2016-08-05",
        commencement_notification="S.O. 2618(E)",
        is_fully_commenced=True,
    ))

    # 16. Indian Contract Act, 1872
    engine.register_statute(StatuteLifecycle(
        statute_id="IND-STAT-CONTRACT-1872",
        title="Indian Contract Act, 1872",
        enactment_date="1872-04-25",
        commencement_date="1872-09-01",
        is_fully_commenced=True,
    ))

    # 17. Transfer of Property Act, 1882
    engine.register_statute(StatuteLifecycle(
        statute_id="IND-STAT-TPA-1882",
        title="Transfer of Property Act, 1882",
        enactment_date="1882-02-17",
        commencement_date="1882-07-01",
        is_fully_commenced=True,
    ))

    # 18. Code of Civil Procedure, 1908
    engine.register_statute(StatuteLifecycle(
        statute_id="IND-STAT-CPC-1908",
        title="Code of Civil Procedure, 1908",
        enactment_date="1908-03-21",
        commencement_date="1909-01-01",
        is_fully_commenced=True,
    ))

    # 19. Motor Vehicles Act, 1988
    engine.register_statute(StatuteLifecycle(
        statute_id="IND-STAT-MVA-1988",
        title="Motor Vehicles Act, 1988",
        enactment_date="1988-10-14",
        commencement_date="1989-07-01",
        is_fully_commenced=True,
    ))

    # Batch 2 Provision Versions:
    # Companies Act Section 135 (Pre-2020: Comply or Explain)
    engine.register_provision_version(ProvisionTemporalVersion(
        provision_id="COMP-SEC-135",
        statute_id="IND-STAT-COMP-2013",
        section_number="135",
        version_number=1,
        text="135. (5) The Board of every company referred to in sub-section (1), shall ensure that the company spends, in every financial year, at least two per cent. of the average net profits of the company made during the three immediately preceding financial years... Provided further that if the company fails to spend such amount, the Board shall, in its report made under clause (o) of sub-section (3) of section 134, specify the reasons for not spending the amount.",
        version_effective_from="2014-04-01",
        version_effective_until="2021-01-21",
        commencement_date="2014-04-01",
        temporal_status=TemporalStatus.AMENDED_HISTORICAL,
    ))

    # Companies Act Section 135 (Post-2020: Mandatory Unspent Transfer & Civil Penalty)
    engine.register_provision_version(ProvisionTemporalVersion(
        provision_id="COMP-SEC-135",
        statute_id="IND-STAT-COMP-2013",
        section_number="135",
        version_number=2,
        text="135. (6) Any amount remaining unspent under sub-section (5), pursuant to any ongoing project... shall be transferred by the company within a period of thirty days from the end of the financial year to a special account to be opened by the company... (7) If a company is in default in complying with the provisions of sub-section (5) or sub-section (6), the company shall be liable to a penalty of twice the amount required to be transferred...",
        version_effective_from="2021-01-22",
        version_effective_until=None,
        commencement_date="2021-01-22",
        commencement_notification="S.O. 325(E) dated 22 January 2021",
        amendment_act_id="IND-AMEND-COMP-2020",
        temporal_status=TemporalStatus.ACTIVE,
    ))

    # IBC Section 29A (Disqualification of Resolution Applicants)
    engine.register_provision_version(ProvisionTemporalVersion(
        provision_id="IBC-SEC-29A",
        statute_id="IND-STAT-IBC-2016",
        section_number="29A",
        version_number=1,
        text="29A. Persons not eligible to be resolution applicant.—A person shall not be eligible to submit a resolution plan, if such person, or any other person acting jointly or in concert with such person— (a) is an undischarged insolvent; (b) is a wilful defaulter in accordance with the guidelines of the Reserve Bank of India...",
        version_effective_from="2017-11-23",
        version_effective_until=None,
        commencement_date="2017-11-23",
        amendment_act_id="IND-AMEND-IBC-2018",
        temporal_status=TemporalStatus.ACTIVE,
    ))

    # IBC Section 32A (Clean-Slate Immunity)
    engine.register_provision_version(ProvisionTemporalVersion(
        provision_id="IBC-SEC-32A",
        statute_id="IND-STAT-IBC-2016",
        section_number="32A",
        version_number=1,
        text="32A. Liability for prior offences, etc.—(1) Notwithstanding anything to the contrary contained in this Code or any other law for the time being in force, the liability of a corporate debtor for an offence committed prior to the commencement of the corporate insolvency resolution process shall cease, and the corporate debtor shall not be prosecuted for such an offence from the date the resolution plan has been approved by the Adjudicating Authority under section 31...",
        version_effective_from="2019-12-28",
        version_effective_until=None,
        commencement_date="2019-12-28",
        amendment_act_id="IND-AMEND-IBC-2020",
        temporal_status=TemporalStatus.ACTIVE,
    ))

    # Contract Act Section 28 (Historical Pre-1997 Version)
    engine.register_provision_version(ProvisionTemporalVersion(
        provision_id="CONTRACT-SEC-28",
        statute_id="IND-STAT-CONTRACT-1872",
        section_number="28",
        version_number=1,
        text="28. Agreements in restraint of legal proceedings, void.—Every agreement, by which any party thereto is restricted absolutely from enforcing his rights under or in respect of any contract, by the usual legal proceedings in the ordinary tribunals, or which limits the time within which he may thus enforce his rights, is void to that extent.",
        version_effective_from="1872-09-01",
        version_effective_until="1997-01-07",
        commencement_date="1872-09-01",
        temporal_status=TemporalStatus.AMENDED_HISTORICAL,
    ))

    # Contract Act Section 28 (Current Post-1997 Version)
    engine.register_provision_version(ProvisionTemporalVersion(
        provision_id="CONTRACT-SEC-28",
        statute_id="IND-STAT-CONTRACT-1872",
        section_number="28",
        version_number=2,
        text="28. Agreements in restraint of legal proceedings, void.—Every agreement,— (a) by which any party thereto is restricted absolutely from enforcing his rights under or in respect of any contract, by the usual legal proceedings in the ordinary tribunals, or which limits the time within which he may thus enforce his rights; or (b) which extinguishes the rights of any party thereto, or discharges any party thereto, from any liability, under or in respect of any contract on the expiry of a specified period so as to restrict any party from enforcing his rights, is void to that extent.",
        version_effective_from="1997-01-08",
        version_effective_until=None,
        commencement_date="1997-01-08",
        amendment_act_id="IND-AMEND-CONTRACT-1997",
        temporal_status=TemporalStatus.ACTIVE,
    ))

    # Transfer of Property Act Section 53A (Historical: 1929 to 2001)
    engine.register_provision_version(ProvisionTemporalVersion(
        provision_id="TPA-SEC-53A",
        statute_id="IND-STAT-TPA-1882",
        section_number="53A",
        version_number=1,
        text="53A. Part performance.—Where any person contracts to transfer for consideration any immoveable property by writing signed by him... and the transferee has, in part performance of the contract, taken possession of the property... then, notwithstanding that the contract, though required to be registered, has not been registered... the transferor or any person claiming under him shall be debarred from enforcing against the transferee...",
        version_effective_from="1929-04-01",
        version_effective_until="2001-09-23",
        commencement_date="1929-04-01",
        temporal_status=TemporalStatus.AMENDED_HISTORICAL,
    ))

    # Transfer of Property Act Section 53A (Current Post-2001 Amendment)
    engine.register_provision_version(ProvisionTemporalVersion(
        provision_id="TPA-SEC-53A",
        statute_id="IND-STAT-TPA-1882",
        section_number="53A",
        version_number=2,
        text="53A. Part performance.—Where any person contracts to transfer for consideration any immoveable property by writing signed by him... and the transferee has, in part performance of the contract, taken possession of the property... then, notwithstanding that there is an instrument of transfer, that the transfer has not been completed in the manner prescribed therefor by the law for the time being in force, the transferor or any person claiming under him shall be debarred from enforcing against the transferee...",
        version_effective_from="2001-09-24",
        version_effective_until=None,
        commencement_date="2001-09-24",
        amendment_act_id="IND-AMEND-TPA-2001",
        temporal_status=TemporalStatus.ACTIVE,
    ))

    # Motor Vehicles Act Section 163A (Historical Formula)
    engine.register_provision_version(ProvisionTemporalVersion(
        provision_id="MVA-SEC-163A",
        statute_id="IND-STAT-MVA-1988",
        section_number="163A",
        version_number=1,
        text="163A. Special provisions as to payment of compensation on structured formula basis.—(1) Notwithstanding anything contained in this Act or in any other law for the time being in force or instrument having the force of law, the owner of the motor vehicle or the authorised insurer shall be liable to pay in the case of death or permanent disablement due to accident arising out of the use of motor vehicle, compensation, as indicated in the Second Schedule...",
        version_effective_from="1994-11-14",
        version_effective_until="2022-03-31",
        commencement_date="1994-11-14",
        temporal_status=TemporalStatus.AMENDED_HISTORICAL,
    ))

    # Motor Vehicles Act Section 164 (Current Fixed No-Fault Compensation)
    engine.register_provision_version(ProvisionTemporalVersion(
        provision_id="MVA-SEC-164",
        statute_id="IND-STAT-MVA-1988",
        section_number="164",
        version_number=1,
        text="164. Payment of compensation in case of death or grievous hurt, etc.—(1) Notwithstanding anything contained in this Act or in any other law for the time being in force or instrument having the force of law, the owner of the motor vehicle or the authorised insurer shall be liable to pay in the case of death or grievous hurt due to any accident arising out of the use of motor vehicle, a compensation, of a sum of five lakh rupees in case of death or of two and a half lakh rupees in case of grievous hurt to the legal heirs or the victim, as the case may be.",
        version_effective_from="2022-04-01",
        version_effective_until=None,
        commencement_date="2022-04-01",
        commencement_notification="S.O. 859(E) dated 25 February 2022",
        amendment_act_id="IND-AMEND-MVA-2019",
        temporal_status=TemporalStatus.ACTIVE,
    ))

    return engine


