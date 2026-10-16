"""
LegalMitra Amendment History & Statutory Modification Engine
Models amendment relationships, amending Acts, insertion, substitution, omission,
and repeal with exact commencement dates and gazette references.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class AmendmentAction(str, Enum):
    INSERTION = "insertion"
    SUBSTITUTION = "substitution"
    OMISSION = "omission"
    REPEAL = "repeal"
    RENUMBERING = "renumbering"
    SAVINGS_TRANSITION = "savings_transition"


@dataclass
class AmendmentInstrument:
    instrument_id: str
    official_title: str
    act_number: str
    year: int
    assent_date: str
    publication_date: str
    commencement_date: str
    commencement_notification: Optional[str] = None
    issuing_authority: str = "Parliament of India"
    source_url: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AmendmentInstrument:
        return cls(**data)


@dataclass
class AmendmentRelationship:
    relationship_id: str
    principal_act_id: str
    amending_instrument_id: str
    target_provision: str  # e.g., "Section 10", "Section 20A"
    action: AmendmentAction
    effective_date: str
    commencement_notification: Optional[str] = None
    prior_text_summary: Optional[str] = None
    amended_text_summary: Optional[str] = None
    statutory_rationale: str = ""
    is_complete: bool = True

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["action"] = self.action.value
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AmendmentRelationship:
        d = dict(data)
        d["action"] = AmendmentAction(d["action"])
        return cls(**d)


class AmendmentHistoryManager:
    """Manages the graph of statutory amendments across Indian central enactments."""

    def __init__(self):
        self._instruments: Dict[str, AmendmentInstrument] = {}
        self._relationships: List[AmendmentRelationship] = []

    def register_instrument(self, inst: AmendmentInstrument) -> None:
        self._instruments[inst.instrument_id] = inst

    def add_relationship(self, rel: AmendmentRelationship) -> None:
        self._relationships.append(rel)

    def get_instrument(self, inst_id: str) -> Optional[AmendmentInstrument]:
        return self._instruments.get(inst_id)

    def list_instruments(self) -> List[AmendmentInstrument]:
        return list(self._instruments.values())

    def list_relationships(self) -> List[AmendmentRelationship]:
        return list(self._relationships)

    def get_amendments_for_act(self, act_id: str) -> List[AmendmentRelationship]:
        return [r for r in self._relationships if r.principal_act_id == act_id]

    get_relationships_for_act = get_amendments_for_act


    def get_amendments_for_provision(self, act_id: str, provision: str) -> List[AmendmentRelationship]:
        return [
            r for r in self._relationships
            if r.principal_act_id == act_id and r.target_provision.lower() == provision.lower()
        ]

    def export_json(self, target_path: Path) -> None:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": "1.0.0",
            "total_instruments": len(self._instruments),
            "total_amendment_relationships": len(self._relationships),
            "instruments": [i.to_dict() for i in self._instruments.values()],
            "amendment_relationships": [r.to_dict() for r in self._relationships],
        }
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    @classmethod
    def load_json(cls, source_path: Path) -> AmendmentHistoryManager:
        with open(source_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        mgr = cls()
        for i_data in payload.get("instruments", []):
            mgr.register_instrument(AmendmentInstrument.from_dict(i_data))
        for r_data in payload.get("amendment_relationships", []):
            mgr.add_relationship(AmendmentRelationship.from_dict(r_data))
        return mgr


def build_default_amendment_history() -> AmendmentHistoryManager:
    """Builds authoritative amendment relationships for Indian central legislation."""
    mgr = AmendmentHistoryManager()

    # 1. Specific Relief (Amendment) Act, 2018 (Act No. 18 of 2018)
    inst_sra_2018 = AmendmentInstrument(
        instrument_id="IND-AMEND-SRA-2018",
        official_title="The Specific Relief (Amendment) Act, 2018",
        act_number="Act No. 18 of 2018",
        year=2018,
        assent_date="2018-08-01",
        publication_date="2018-08-01",
        commencement_date="2018-10-01",
        commencement_notification="S.O. 4888(E) dated 19 September 2018",
        source_url="https://www.indiacode.nic.in/handle/123456789/1583",
    )
    mgr.register_instrument(inst_sra_2018)

    mgr.add_relationship(AmendmentRelationship(
        relationship_id="REL-SRA-SEC10-SUBSTITUTION",
        principal_act_id="IND-STAT-SRA-1963",
        amending_instrument_id="IND-AMEND-SRA-2018",
        target_provision="Section 10",
        action=AmendmentAction.SUBSTITUTION,
        effective_date="2018-10-01",
        commencement_notification="S.O. 4888(E)",
        prior_text_summary="Specific performance was discretionary with the court under former Section 20.",
        amended_text_summary="Specific performance of a contract shall be enforced by the court subject to sections 11(2), 14, and 16 (mandatory).",
        statutory_rationale="Transforms specific performance from an equitable discretionary remedy into the primary statutory rule."
    ))

    mgr.add_relationship(AmendmentRelationship(
        relationship_id="REL-SRA-SEC20A-INSERTION",
        principal_act_id="IND-STAT-SRA-1963",
        amending_instrument_id="IND-AMEND-SRA-2018",
        target_provision="Section 20A",
        action=AmendmentAction.INSERTION,
        effective_date="2018-10-01",
        commencement_notification="S.O. 4888(E)",
        prior_text_summary="No special provisions existed barring injunctions in infrastructure contracts.",
        amended_text_summary="No injunction shall be granted by court in a suit where granting injunction would cause impediment or delay in infrastructure projects specified in Schedule.",
        statutory_rationale="Prevents judicial injunctions from stalling vital national infrastructure projects."
    ))

    # 2. Arbitration and Conciliation (Amendment) Act, 2015 (Act No. 3 of 2016)
    inst_arb_2015 = AmendmentInstrument(
        instrument_id="IND-AMEND-ARB-2015",
        official_title="The Arbitration and Conciliation (Amendment) Act, 2015",
        act_number="Act No. 3 of 2016",
        year=2015,
        assent_date="2015-12-31",
        publication_date="2016-01-01",
        commencement_date="2015-10-23",  # Retrospective from ordinance date
        commencement_notification="Ordinance promulgated 23 October 2015",
        source_url="https://www.indiacode.nic.in/handle/123456789/1978",
    )
    mgr.register_instrument(inst_arb_2015)

    mgr.add_relationship(AmendmentRelationship(
        relationship_id="REL-ARB-SEC34-SUBSTITUTION",
        principal_act_id="IND-STAT-ARB-1996",
        amending_instrument_id="IND-AMEND-ARB-2015",
        target_provision="Section 34",
        action=AmendmentAction.SUBSTITUTION,
        effective_date="2015-10-23",
        prior_text_summary="Broad interpretation of public policy permitted merits review under ONGC v. Saw Pipes.",
        amended_text_summary="Patent illegality appearing on the face of the award restricted to domestic arbitrations, excluding international commercial arbitrations, with express bar on review on merits.",
        statutory_rationale="Narrows grounds for challenging arbitral awards and establishes pro-arbitration enforcement regime."
    ))

    mgr.add_relationship(AmendmentRelationship(
        relationship_id="REL-ARB-SEC29A-INSERTION",
        principal_act_id="IND-STAT-ARB-1996",
        amending_instrument_id="IND-AMEND-ARB-2015",
        target_provision="Section 29A",
        action=AmendmentAction.INSERTION,
        effective_date="2015-10-23",
        prior_text_summary="No statutory timeline existed for concluding arbitral proceedings.",
        amended_text_summary="Award must be made within 12 months from the date the arbitral tribunal enters upon reference (later amended to completion of pleadings in 2019).",
        statutory_rationale="Introduces strict statutory deadlines to ensure speedy resolution of commercial disputes."
    ))

    # 3. Information Technology (Amendment) Act, 2008 (Act No. 10 of 2009)
    inst_it_2008 = AmendmentInstrument(
        instrument_id="IND-AMEND-IT-2008",
        official_title="The Information Technology (Amendment) Act, 2008",
        act_number="Act No. 10 of 2009",
        year=2008,
        assent_date="2009-02-05",
        publication_date="2009-02-06",
        commencement_date="2009-10-27",
        commencement_notification="S.O. 2689(E) dated 27 October 2009",
        source_url="https://www.indiacode.nic.in/handle/123456789/496511",
    )
    mgr.register_instrument(inst_it_2008)

    mgr.add_relationship(AmendmentRelationship(
        relationship_id="REL-IT-SEC43A-INSERTION",
        principal_act_id="IND-STAT-IT-2000",
        amending_instrument_id="IND-AMEND-IT-2008",
        target_provision="Section 43A",
        action=AmendmentAction.INSERTION,
        effective_date="2009-10-27",
        commencement_notification="S.O. 2689(E)",
        prior_text_summary="IT Act 2000 lacked specific corporate compensation for sensitive personal data leaks.",
        amended_text_summary="Introduced corporate liability to pay compensation for failure to protect sensitive personal data or information.",
        statutory_rationale="Established statutory foundation for corporate data protection in India prior to DPDP Act."
    ))

    mgr.add_relationship(AmendmentRelationship(
        relationship_id="REL-IT-SEC79-SUBSTITUTION",
        principal_act_id="IND-STAT-IT-2000",
        amending_instrument_id="IND-AMEND-IT-2008",
        target_provision="Section 79",
        action=AmendmentAction.SUBSTITUTION,
        effective_date="2009-10-27",
        commencement_notification="S.O. 2689(E)",
        prior_text_summary="Limited network service provider exemption under original Section 79.",
        amended_text_summary="Comprehensive intermediary safe harbor immunity subject to due diligence and take-down compliance.",
        statutory_rationale="Intermediary protection calibrated with Shreya Singhal (2015) judicial reading."
    ))

    # 4. Constitution (106th Amendment) Act, 2023 (Nari Shakti Vandan Adhiniyam)
    inst_const_106 = AmendmentInstrument(
        instrument_id="IND-AMEND-CONST-106",
        official_title="The Constitution (One Hundred and Sixth Amendment) Act, 2023",
        act_number="Act No. 20 of 2023",
        year=2023,
        assent_date="2023-09-28",
        publication_date="2023-09-28",
        commencement_date="2023-09-28",
        commencement_notification="Official Gazette Extraordinary 28 September 2023",
        source_url="https://legislative.gov.in/constitution-of-india/",
    )
    mgr.register_instrument(inst_const_106)

    mgr.add_relationship(AmendmentRelationship(
        relationship_id="REL-CONST-ART330A-INSERTION",
        principal_act_id="IND-CONST-1950",
        amending_instrument_id="IND-AMEND-CONST-106",
        target_provision="Article 330A",
        action=AmendmentAction.INSERTION,
        effective_date="2023-09-28",
        prior_text_summary="No reservation for women in the House of the People (Lok Sabha).",
        amended_text_summary="Reserves one-third of total seats in Lok Sabha for women, effective following census delimitation.",
        statutory_rationale="Affirmative action ensuring 33% representation for women in Parliament."
    ))

    # 5. Bharatiya Nyaya Sanhita, 2023 (Repeal and Replacement of IPC 1860)
    inst_bns_repeal = AmendmentInstrument(
        instrument_id="IND-AMEND-BNS-2023",
        official_title="The Bharatiya Nyaya Sanhita, 2023 (Section 358 Repeal & Savings)",
        act_number="Act No. 45 of 2023",
        year=2023,
        assent_date="2023-12-25",
        publication_date="2023-12-25",
        commencement_date="2024-07-01",
        commencement_notification="S.O. 849(E)",
        source_url="https://indiacode.gov.in/handle/123456789/601738",
    )
    mgr.register_instrument(inst_bns_repeal)

    mgr.add_relationship(AmendmentRelationship(
        relationship_id="REL-IPC-REPEAL-SAVINGS",
        principal_act_id="IND-STAT-IPC-1860",
        amending_instrument_id="IND-AMEND-BNS-2023",
        target_provision="Whole Act (IPC 1860)",
        action=AmendmentAction.REPEAL,
        effective_date="2024-07-01",
        commencement_notification="S.O. 849(E)",
        prior_text_summary="Indian Penal Code 1860 was the primary substantive criminal enactment.",
        amended_text_summary="Repealed under Section 358(1) of BNS 2023; pending cases and offences committed prior to 01.07.2024 saved under Section 358(2).",
        statutory_rationale="Transition from colonial penal code to Bharatiya Nyaya Sanhita."
    ))

    # 6. Consumer Protection Act, 2019 (Repeal and Replacement of CPA 1986)
    inst_cpa_repeal = AmendmentInstrument(
        instrument_id="IND-AMEND-CPA-2019",
        official_title="The Consumer Protection Act, 2019 (Section 107 Repeal & Savings)",
        act_number="Act No. 35 of 2019",
        year=2019,
        assent_date="2019-08-09",
        publication_date="2019-08-09",
        commencement_date="2020-07-20",
        commencement_notification="S.O. 2351(E) dated 15 July 2020",
        source_url="https://www.indiacode.nic.in/handle/123456789/15256",
    )
    mgr.register_instrument(inst_cpa_repeal)

    mgr.add_relationship(AmendmentRelationship(
        relationship_id="REL-CPA-REPEAL-SAVINGS",
        principal_act_id="IND-STAT-CPA-1986",
        amending_instrument_id="IND-AMEND-CPA-2019",
        target_provision="Whole Act (CPA 1986)",
        action=AmendmentAction.REPEAL,
        effective_date="2020-07-20",
        commencement_notification="S.O. 2351(E)",
        prior_text_summary="Consumer Protection Act 1986 lacked product liability and central regulator (CCPA).",
        amended_text_summary="Repealed by Section 107 of CPA 2019, with pending complaints saved.",
        statutory_rationale="Modernizes consumer rights to include e-commerce, misleading advertisements, and product liability."
    ))

    return mgr


build_default_amendment_manager = build_default_amendment_history
