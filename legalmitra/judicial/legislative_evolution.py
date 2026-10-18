"""LegalMitra Judicial Knowledge Infrastructure — Judicial-Legislative Evolution Engine.

Traces the bidirectional relationship between Indian case law and legislation with strict
evidentiary causation standards:
- Judicial impact on statutes (struck down, read down, expanded, guideline gap-filling)
- Legislative responses to judgments (codification, nullification, amendment)
- Evidentiary causation classification (Direct Response, Express Reference, Law Commission,
  Documented Policy, Mere Temporal Sequence, Doctrinal Interaction).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class JudicialActionOnStatute(str, Enum):
    UPHELD = "UPHELD"
    STRUCK_DOWN_UNCONSTITUTIONAL = "STRUCK_DOWN_UNCONSTITUTIONAL"
    READ_DOWN = "READ_DOWN"
    DOCTRINE_OF_SEVERABILITY_APPLIED = "DOCTRINE_OF_SEVERABILITY_APPLIED"
    INTERPRETED_EXPANSIVELY = "INTERPRETED_EXPANSIVELY"
    INTERPRETED_RESTRICTIVELY = "INTERPRETED_RESTRICTIVELY"
    GAP_FILLED_BY_GUIDELINES = "GAP_FILLED_BY_GUIDELINES"


class LegislativeCausationLevel(str, Enum):
    """Rigorous classification of causal link between judgment and legislative change."""
    DIRECT_LEGISLATIVE_RESPONSE = "DIRECT_LEGISLATIVE_RESPONSE"       # Proven by Statement of Objects & Reasons / Debates
    EXPRESS_STATUTORY_REFERENCE = "EXPRESS_STATUTORY_REFERENCE"       # Statute explicitly names or references case doctrine
    OFFICIAL_REFORM_RECOMMENDATION = "OFFICIAL_REFORM_RECOMMENDATION" # Law Commission Report explicitly recommends change
    DOCUMENTED_POLICY_INFLUENCE = "DOCUMENTED_POLICY_INFLUENCE"       # Committee/White paper citations
    DOCTRINAL_INTERACTION = "DOCTRINAL_INTERACTION"                   # Ongoing iterative refinement between courts and Parliament
    MERE_TEMPORAL_SEQUENCE = "MERE_TEMPORAL_SEQUENCE"                 # Non-causal: law changed after judgment, no official proof


class LegislativeActionType(str, Enum):
    CODIFIED_JUDICIAL_DOCTRINE = "CODIFIED_JUDICIAL_DOCTRINE"
    SUPERSEDED_OR_NULLIFIED_EFFECT = "SUPERSEDED_OR_NULLIFIED_EFFECT"
    AMENDED_PROSPECTIVELY = "AMENDED_PROSPECTIVELY"
    ENACTED_NEW_ACT = "ENACTED_NEW_ACT"
    REPLACED_HISTORIC_STATUTE = "REPLACED_HISTORIC_STATUTE"


@dataclass
class JudicialStatuteInteraction:
    case_id: str
    case_citation: str
    statute_name: str
    statute_section: Optional[str]
    judicial_action: JudicialActionOnStatute
    constitutional_ground: Optional[str]
    holding_summary: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "case_id": self.case_id,
            "case_citation": self.case_citation,
            "statute_name": self.statute_name,
            "statute_section": self.statute_section,
            "judicial_action": self.judicial_action.value,
            "constitutional_ground": self.constitutional_ground,
            "holding_summary": self.holding_summary,
        }


@dataclass
class LegislativeResponseToCase:
    response_id: str
    prior_case_id: str
    prior_case_citation: str
    enacted_statute_or_amendment: str
    year_of_enactment: int
    legislative_action: LegislativeActionType
    causation_level: LegislativeCausationLevel
    official_evidentiary_citation: str  # Must cite official document, SOR, Law Commission report, or debate
    detailed_evolution_notes: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "response_id": self.response_id,
            "prior_case_id": self.prior_case_id,
            "prior_case_citation": self.prior_case_citation,
            "enacted_statute_or_amendment": self.enacted_statute_or_amendment,
            "year_of_enactment": self.year_of_enactment,
            "legislative_action": self.legislative_action.value,
            "causation_level": self.causation_level.value,
            "official_evidentiary_citation": self.official_evidentiary_citation,
            "detailed_evolution_notes": self.detailed_evolution_notes,
        }


class LegislativeEvolutionEngine:
    """Manages the bidirectional graph of judicial-legislative interactions."""

    def __init__(self) -> None:
        self._judicial_actions: List[JudicialStatuteInteraction] = []
        self._legislative_responses: Dict[str, LegislativeResponseToCase] = {}
        self._populate_canonical_interactions()

    def record_judicial_action(self, action: JudicialStatuteInteraction) -> None:
        self._judicial_actions.append(action)

    def record_legislative_response(self, response: LegislativeResponseToCase) -> None:
        # Enforce evidentiary invariant: If claiming DIRECT_LEGISLATIVE_RESPONSE or OFFICIAL_REFORM,
        # an official evidentiary citation must be present.
        if response.causation_level in [
            LegislativeCausationLevel.DIRECT_LEGISLATIVE_RESPONSE,
            LegislativeCausationLevel.OFFICIAL_REFORM_RECOMMENDATION,
            LegislativeCausationLevel.EXPRESS_STATUTORY_REFERENCE,
        ]:
            if not response.official_evidentiary_citation or len(response.official_evidentiary_citation.strip()) < 5:
                raise ValueError(
                    f"Evidentiary Invariant Violation: Causation level '{response.causation_level.value}' "
                    f"for response {response.response_id} requires specific official citation (SOR, Law Commission Report, or Gazetted Act)."
                )

        self._legislative_responses[response.response_id] = response

    def get_judicial_actions_for_case(self, case_id: str) -> List[JudicialStatuteInteraction]:
        return [ja for ja in self._judicial_actions if ja.case_id == case_id]

    def get_legislative_responses_for_case(self, case_id: str) -> List[LegislativeResponseToCase]:
        return [lr for lr in self._legislative_responses.values() if lr.prior_case_id == case_id]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_judicial_actions": len(self._judicial_actions),
            "total_legislative_responses": len(self._legislative_responses),
            "judicial_actions": [ja.to_dict() for ja in self._judicial_actions],
            "legislative_responses": [lr.to_dict() for lr in self._legislative_responses.values()],
        }

    def _populate_canonical_interactions(self) -> None:
        # 1. Shreya Singhal (2015) -> Section 66A IT Act struck down
        self.record_judicial_action(JudicialStatuteInteraction(
            case_id="SHREYA-SINGHAL-2015",
            case_citation="AIR 2015 SC 1523",
            statute_name="Information Technology Act 2000",
            statute_section="Section 66A",
            judicial_action=JudicialActionOnStatute.STRUCK_DOWN_UNCONSTITUTIONAL,
            constitutional_ground="Article 19(1)(a) & not saved under Article 19(2)",
            holding_summary="Section 66A invalidated in entirety for being vague and overbroad, creating a chilling effect on speech.",
        ))

        # 2. Vishaka (1997) -> POSH Act 2013 (Direct Legislative Response)
        self.record_judicial_action(JudicialStatuteInteraction(
            case_id="VISHAKA-1997",
            case_citation="AIR 1997 SC 3011",
            statute_name="Gender Equality at Workplace",
            statute_section=None,
            judicial_action=JudicialActionOnStatute.GAP_FILLED_BY_GUIDELINES,
            constitutional_ground="Articles 14, 19(1)(g), 21 read with CEDAW under Article 51(c)",
            holding_summary="Supreme Court formulated binding guidelines to operate as law under Article 141 until statutory enactment.",
        ))

        self.record_legislative_response(LegislativeResponseToCase(
            response_id="RESP-VISHAKA-POSH-2013",
            prior_case_id="VISHAKA-1997",
            prior_case_citation="AIR 1997 SC 3011",
            enacted_statute_or_amendment="Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013",
            year_of_enactment=2013,
            legislative_action=LegislativeActionType.CODIFIED_JUDICIAL_DOCTRINE,
            causation_level=LegislativeCausationLevel.DIRECT_LEGISLATIVE_RESPONSE,
            official_evidentiary_citation="Statement of Objects and Reasons, POSH Act 2013 (Bill No. 144 of 2010), citing Vishaka v. State of Rajasthan.",
            detailed_evolution_notes="Parliament expressly cited the Vishaka guidelines and international commitments in the Statement of Objects and Reasons, codifying internal complaints committees and inquiries into comprehensive statute.",
        ))

        # 3. Shah Bano (1985) -> Muslim Women (Protection of Rights on Divorce) Act 1986 (Superseded/Nullified)
        self.record_judicial_action(JudicialStatuteInteraction(
            case_id="SHAH-BANO-1985",
            case_citation="AIR 1985 SC 945",
            statute_name="Code of Criminal Procedure 1973",
            statute_section="Section 125",
            judicial_action=JudicialActionOnStatute.INTERPRETED_EXPANSIVELY,
            constitutional_ground="Article 44 / Secular application of Section 125 CrPC",
            holding_summary="Section 125 CrPC applies universally to all divorced women irrespective of personal religion.",
        ))

        self.record_legislative_response(LegislativeResponseToCase(
            response_id="RESP-SHAH-BANO-1986",
            prior_case_id="SHAH-BANO-1985",
            prior_case_citation="AIR 1985 SC 945",
            enacted_statute_or_amendment="Muslim Women (Protection of Rights on Divorce) Act, 1986",
            year_of_enactment=1986,
            legislative_action=LegislativeActionType.SUPERSEDED_OR_NULLIFIED_EFFECT,
            causation_level=LegislativeCausationLevel.DIRECT_LEGISLATIVE_RESPONSE,
            official_evidentiary_citation="Statement of Objects and Reasons, Muslim Women Act 1986, specifically addressing the aftermath of Mohd. Ahmed Khan v. Shah Bano Begum.",
            detailed_evolution_notes="Enacted to supersede the direct operation of Section 125 CrPC regarding Muslim divorced women, later harmoniously construed in Danial Latifi (2001).",
        ))

        # 4. Joseph Shine (2018) -> Decriminalization of Adultery
        self.record_judicial_action(JudicialStatuteInteraction(
            case_id="JOSEPH-SHINE-2018",
            case_citation="AIR 2018 SC 4898",
            statute_name="Indian Penal Code 1860",
            statute_section="Section 497",
            judicial_action=JudicialActionOnStatute.STRUCK_DOWN_UNCONSTITUTIONAL,
            constitutional_ground="Articles 14, 15, and 21",
            holding_summary="Struck down Section 497 IPC for violating dignity and autonomy of women, treating wife as chattel of husband.",
        ))

        self.record_legislative_response(LegislativeResponseToCase(
            response_id="RESP-JOSEPH-SHINE-BNS-2023",
            prior_case_id="JOSEPH-SHINE-2018",
            prior_case_citation="AIR 2018 SC 4898",
            enacted_statute_or_amendment="Bharatiya Nyaya Sanhita 2023",
            year_of_enactment=2023,
            legislative_action=LegislativeActionType.REPLACED_HISTORIC_STATUTE,
            causation_level=LegislativeCausationLevel.DIRECT_LEGISLATIVE_RESPONSE,
            official_evidentiary_citation="Parliamentary Standing Committee on Home Affairs Report No. 246 (2023) on Bharatiya Nyaya Sanhita, affirming omission of adultery pursuant to Joseph Shine.",
            detailed_evolution_notes="Adultery provision Section 497 was omitted completely from BNS 2023 in line with the Supreme Court constitutional bench decision in Joseph Shine.",
        ))

        # 5. Navtej Singh Johar (2018) -> Reading down Section 377 IPC
        self.record_judicial_action(JudicialStatuteInteraction(
            case_id="NAVTEJ-JOHAR-2018",
            case_citation="AIR 2018 SC 4321",
            statute_name="Indian Penal Code 1860",
            statute_section="Section 377",
            judicial_action=JudicialActionOnStatute.READ_DOWN,
            constitutional_ground="Articles 14, 15, 19(1)(a), 21",
            holding_summary="Read down Section 377 IPC to exclude consensual sexual acts between consenting adults in private.",
        ))

        # 6. D.K. Basu (1997) -> Section 41A-41D CrPC (Direct Legislative Codification via 2008/2010 Amendments)
        self.record_judicial_action(JudicialStatuteInteraction(
            case_id="DK-BASU-1997",
            case_citation="AIR 1997 SC 610",
            statute_name="Code of Criminal Procedure 1973 (Arrest & Custodial Safeguards)",
            statute_section="Sections 41, 46, 50, 54",
            judicial_action=JudicialActionOnStatute.GAP_FILLED_BY_GUIDELINES,
            constitutional_ground="Articles 21 and 22",
            holding_summary="Formulated 11 mandatory procedural guidelines for arrest and detention to prevent custodial violence.",
        ))

        self.record_legislative_response(LegislativeResponseToCase(
            response_id="RESP-DK-BASU-CRPC-2008",
            prior_case_id="DK-BASU-1997",
            prior_case_citation="AIR 1997 SC 610",
            enacted_statute_or_amendment="Code of Criminal Procedure (Amendment) Act, 2008 (Act 5 of 2009)",
            year_of_enactment=2009,
            legislative_action=LegislativeActionType.CODIFIED_JUDICIAL_DOCTRINE,
            causation_level=LegislativeCausationLevel.DIRECT_LEGISLATIVE_RESPONSE,
            official_evidentiary_citation="Law Commission of India 177th Report on Law Relating to Arrest (2001) and Statement of Objects & Reasons of CrPC Amendment Act 2008, citing D.K. Basu.",
            detailed_evolution_notes="Insertion of Sections 41A, 41B, 41C, and 41D into CrPC directly codifying D.K. Basu arrest memo, notice of appearance, and right to meet advocate.",
        ))
