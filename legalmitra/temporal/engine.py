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

    return engine


