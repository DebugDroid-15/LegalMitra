"""
LegalMitra Judicial Precedent and Case Law Hierarchy Engine
Models Article 141 binding precedent hierarchy, bench strength rules,
precedent treatment relationships, and statutory provisions considered.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class BenchStrength(str, Enum):
    SINGLE_JUDGE = "single_judge"            # 1 Judge
    DIVISION_BENCH = "division_bench"        # 2 Judges
    FULL_BENCH = "full_bench"                # 3 Judges
    CONSTITUTION_BENCH_5 = "constitution_5"  # 5 Judges
    CONSTITUTION_BENCH_7 = "constitution_7"  # 7 Judges
    CONSTITUTION_BENCH_9 = "constitution_9"  # 9 Judges
    LARGEST_BENCH_13 = "constitution_13"     # 13 Judges (Kesavananda Bharati)


class PrecedentTreatment(str, Enum):
    CITED = "cited"
    FOLLOWED = "followed"
    APPLIED = "applied"
    APPROVED = "approved"
    AFFIRMED = "affirmed"
    DISTINGUISHED = "distinguished"
    DOUBTED = "doubted"
    REFERRED_LARGER_BENCH = "referred_to_larger_bench"
    OVERRULED = "overruled"
    PARTIALLY_OVERRULED = "partially_overruled"
    REVERSED = "reversed"
    SET_ASIDE = "set_aside"
    REMANDED = "remanded"
    MODIFIED = "modified"
    RECONSIDERED = "reconsidered_or_clarified"


@dataclass
class PrecedentRelationship:
    relationship_id: str
    citing_case_id: str
    cited_case_id: str
    treatment: PrecedentTreatment
    statutes_considered: List[str] = field(default_factory=list)
    provisions_considered: List[str] = field(default_factory=list)
    ratio_summary: str = ""
    is_human_reviewed: bool = False
    treatment_passage_ref: Optional[str] = None
    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["treatment"] = self.treatment.value
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PrecedentRelationship:
        d = dict(data)
        d["treatment"] = PrecedentTreatment(d["treatment"])
        return cls(**d)


@dataclass
class CaseLawMetadata:
    case_id: str
    case_title: str
    official_citation: str
    neutral_citation: Optional[str] = None
    court: str = "Supreme Court of India"
    bench_strength: BenchStrength = BenchStrength.DIVISION_BENCH
    judge_count: int = 2
    judges: List[str] = field(default_factory=list)
    decision_date: str = ""  # YYYY-MM-DD
    statutes_considered: List[str] = field(default_factory=list)
    provisions_considered: List[str] = field(default_factory=list)
    ratio_decidendi: str = ""
    is_overruled: bool = False
    overruled_by_case_id: Optional[str] = None
    is_human_verified: bool = False

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["bench_strength"] = self.bench_strength.value
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> CaseLawMetadata:
        d = dict(data)
        d["bench_strength"] = BenchStrength(d["bench_strength"])
        return cls(**d)


class PrecedentHierarchyManager:
    """Manages precedent relationships and computes precedent authority."""

    BENCH_RANKS = {
        BenchStrength.SINGLE_JUDGE: 1,
        BenchStrength.DIVISION_BENCH: 2,
        BenchStrength.FULL_BENCH: 3,
        BenchStrength.CONSTITUTION_BENCH_5: 5,
        BenchStrength.CONSTITUTION_BENCH_7: 7,
        BenchStrength.CONSTITUTION_BENCH_9: 9,
        BenchStrength.LARGEST_BENCH_13: 13,
    }

    def __init__(self):
        self._cases: Dict[str, CaseLawMetadata] = {}
        self._relationships: List[PrecedentRelationship] = []

    def register_case(self, case: CaseLawMetadata) -> None:
        self._cases[case.case_id] = case

    def add_relationship(self, rel: PrecedentRelationship) -> None:
        self._relationships.append(rel)
        # If treatment is overruled, automatically mark cited case
        if rel.treatment == PrecedentTreatment.OVERRULED and rel.cited_case_id in self._cases:
            self._cases[rel.cited_case_id].is_overruled = True
            self._cases[rel.cited_case_id].overruled_by_case_id = rel.citing_case_id

    def get_case(self, case_id: str) -> Optional[CaseLawMetadata]:
        return self._cases.get(case_id)

    def list_cases(self) -> List[CaseLawMetadata]:
        return list(self._cases.values())

    def get_relationships_for_case(self, case_id: str) -> List[PrecedentRelationship]:
        return [r for r in self._relationships if r.citing_case_id == case_id or r.cited_case_id == case_id]

    def evaluate_binding_authority(
        self,
        case_id: str,
        target_court: str = "High Court of Delhi",
    ) -> Dict[str, Any]:
        """
        Evaluates the binding authority of a precedent on a target court
        under Article 141 of the Constitution of India and bench strength doctrine.
        """
        case = self.get_case(case_id)
        if not case:
            return {"error": f"Case ID '{case_id}' not found."}

        if case.is_overruled:
            return {
                "case_id": case_id,
                "case_title": case.case_title,
                "authority_status": "OVERRULED",
                "is_binding": False,
                "overruled_by": case.overruled_by_case_id,
                "rationale": (
                    f"Precedent has been overruled by {case.overruled_by_case_id}. "
                    "It no longer constitutes binding law under Article 141."
                )
            }

        # Supreme Court precedents
        if "Supreme Court" in case.court:
            if "Supreme Court" in target_court:
                return {
                    "case_id": case_id,
                    "case_title": case.case_title,
                    "authority_status": "BINDING_SAME_TIER",
                    "bench_strength": case.bench_strength.value,
                    "judge_count": case.judge_count,
                    "is_binding": True,
                    "rationale": (
                        f"Supreme Court decision with bench strength of {case.judge_count} judges. "
                        "Binds benches of co-equal or smaller strength. May only be reconsidered by a larger bench."
                    )
                }
            else:
                return {
                    "case_id": case_id,
                    "case_title": case.case_title,
                    "authority_status": "ABSOLUTELY_BINDING",
                    "bench_strength": case.bench_strength.value,
                    "judge_count": case.judge_count,
                    "is_binding": True,
                    "rationale": (
                        "Supreme Court of India decision. Absolutely binding on all High Courts, "
                        "Tribunals, and Subordinate Courts under Article 141 of the Constitution of India."
                    )
                }
        else:
            # High Court precedents
            if case.court.lower() in target_court.lower():
                return {
                    "case_id": case_id,
                    "case_title": case.case_title,
                    "authority_status": "TERRITORIALLY_BINDING",
                    "bench_strength": case.bench_strength.value,
                    "judge_count": case.judge_count,
                    "is_binding": True,
                    "rationale": (
                        f"High Court ruling binding on all Subordinate Courts and Single Benches within {case.court}."
                    )
                }
            else:
                return {
                    "case_id": case_id,
                    "case_title": case.case_title,
                    "authority_status": "PERSUASIVE_PRECEDENT",
                    "bench_strength": case.bench_strength.value,
                    "judge_count": case.judge_count,
                    "is_binding": False,
                    "rationale": (
                        f"Ruling of {case.court} has strong persuasive value but is not binding outside its territorial jurisdiction."
                    )
                }


def build_default_precedent_manager() -> PrecedentHierarchyManager:
    """Configures landmark Indian Supreme Court precedents and treatment relationships."""
    mgr = PrecedentHierarchyManager()

    # 1. Kesavananda Bharati (1973) 4 SCC 225
    mgr.register_case(CaseLawMetadata(
        case_id="IND-JUD-SC-1973-KESAVANANDA",
        case_title="Kesavananda Bharati v. State of Kerala (1973) 4 SCC 225",
        official_citation="(1973) 4 SCC 225",
        court="Supreme Court of India",
        bench_strength=BenchStrength.LARGEST_BENCH_13,
        judge_count=13,
        decision_date="1973-04-24",
        statutes_considered=["The Constitution of India"],
        provisions_considered=["Article 368", "Article 13", "Article 31C"],
        ratio_decidendi="Parliament has wide power to amend the Constitution under Article 368, but this power does not extend to altering or destroying the Basic Structure or framework of the Constitution.",
        is_human_verified=True,
    ))

    # 2. Puttaswamy I (2017) 10 SCC 1
    mgr.register_case(CaseLawMetadata(
        case_id="IND-JUD-SC-2017-PUTTASWAMY",
        case_title="Justice K.S. Puttaswamy (Retd.) v. Union of India (2017) 10 SCC 1",
        official_citation="(2017) 10 SCC 1",
        neutral_citation="2017 INSC 650",
        court="Supreme Court of India",
        bench_strength=BenchStrength.CONSTITUTION_BENCH_9,
        judge_count=9,
        decision_date="2017-08-24",
        statutes_considered=["The Constitution of India"],
        provisions_considered=["Article 21", "Article 14", "Article 19"],
        ratio_decidendi="The right to privacy is a fundamental right guaranteed under Article 21 and Part III of the Constitution of India, subject to proportionality and legitimate state aim.",
        is_human_verified=True,
    ))

    # 3. M.P. Sharma v. Satish Chandra (1954) SCR 1077 (8-Judge Bench, overruled on privacy)
    mgr.register_case(CaseLawMetadata(
        case_id="IND-JUD-SC-1954-MPSHARMA",
        case_title="M.P. Sharma v. Satish Chandra (1954) SCR 1077",
        official_citation="(1954) SCR 1077",
        court="Supreme Court of India",
        bench_strength=BenchStrength.CONSTITUTION_BENCH_7,
        judge_count=8,
        decision_date="1954-03-15",
        ratio_decidendi="Held there was no fundamental right to privacy in the Constitution analogous to the Fourth Amendment of the US Constitution.",
        is_overruled=True,
        overruled_by_case_id="IND-JUD-SC-2017-PUTTASWAMY",
        is_human_verified=True,
    ))

    # 4. Kharak Singh v. State of U.P. (1964) 1 SCR 332 (6-Judge Bench, overruled on privacy)
    mgr.register_case(CaseLawMetadata(
        case_id="IND-JUD-SC-1963-KHARAK",
        case_title="Kharak Singh v. State of U.P. (1964) 1 SCR 332",
        official_citation="(1964) 1 SCR 332",
        court="Supreme Court of India",
        bench_strength=BenchStrength.CONSTITUTION_BENCH_5,
        judge_count=6,
        decision_date="1962-12-18",
        ratio_decidendi="Majority held privacy was not a guaranteed fundamental right under Part III.",
        is_overruled=True,
        overruled_by_case_id="IND-JUD-SC-2017-PUTTASWAMY",
        is_human_verified=True,
    ))

    # 5. ADM Jabalpur v. Shivkant Shukla (1976) 2 SCC 521 (Habeas Corpus Case, overruled)
    mgr.register_case(CaseLawMetadata(
        case_id="IND-JUD-SC-1976-ADMJABALPUR",
        case_title="ADM Jabalpur v. Shivkant Shukla (1976) 2 SCC 521",
        official_citation="(1976) 2 SCC 521",
        court="Supreme Court of India",
        bench_strength=BenchStrength.CONSTITUTION_BENCH_5,
        judge_count=5,
        decision_date="1976-04-28",
        ratio_decidendi="Majority held that during Emergency no person had locus standi to move writ petition for habeas corpus.",
        is_overruled=True,
        overruled_by_case_id="IND-JUD-SC-2017-PUTTASWAMY",
        is_human_verified=True,
    ))

    # 6. Navtej Singh Johar v. Union of India (2018) 10 SCC 1 (5-Judge Bench)
    mgr.register_case(CaseLawMetadata(
        case_id="IND-JUD-SC-2018-NAVTEJ",
        case_title="Navtej Singh Johar v. Union of India (2018) 10 SCC 1",
        official_citation="(2018) 10 SCC 1",
        court="Supreme Court of India",
        bench_strength=BenchStrength.CONSTITUTION_BENCH_5,
        judge_count=5,
        decision_date="2018-09-06",
        statutes_considered=["Indian Penal Code, 1860", "The Constitution of India"],
        provisions_considered=["Section 377 IPC", "Article 14", "Article 15", "Article 21"],
        ratio_decidendi="Section 377 of the IPC, insofar as it criminalises consensual sexual conduct between adults of the same sex in private, violates Articles 14, 15, 19, and 21 of the Constitution.",
        is_human_verified=True,
    ))

    # 7. Suresh Kumar Koushal v. Naz Foundation (2014) 1 SCC 1 (2-Judge Bench, overruled)
    mgr.register_case(CaseLawMetadata(
        case_id="IND-JUD-SC-2014-KOUSHAL",
        case_title="Suresh Kumar Koushal v. Naz Foundation (2014) 1 SCC 1",
        official_citation="(2014) 1 SCC 1",
        court="Supreme Court of India",
        bench_strength=BenchStrength.DIVISION_BENCH,
        judge_count=2,
        decision_date="2013-12-11",
        ratio_decidendi="Reversed the Delhi High Court decision and upheld the constitutional validity of Section 377 IPC.",
        is_overruled=True,
        overruled_by_case_id="IND-JUD-SC-2018-NAVTEJ",
        is_human_verified=True,
    ))

    # Register Relationships
    mgr.add_relationship(PrecedentRelationship(
        relationship_id="REL-PUTTASWAMY-OVERRULES-MPSHARMA",
        citing_case_id="IND-JUD-SC-2017-PUTTASWAMY",
        cited_case_id="IND-JUD-SC-1954-MPSHARMA",
        treatment=PrecedentTreatment.OVERRULED,
        statutes_considered=["The Constitution of India"],
        provisions_considered=["Article 21"],
        ratio_summary="Overruled M.P. Sharma to the extent it held privacy is not a fundamental right.",
        is_human_reviewed=True,
    ))

    mgr.add_relationship(PrecedentRelationship(
        relationship_id="REL-PUTTASWAMY-OVERRULES-KHARAK",
        citing_case_id="IND-JUD-SC-2017-PUTTASWAMY",
        cited_case_id="IND-JUD-SC-1963-KHARAK",
        treatment=PrecedentTreatment.OVERRULED,
        statutes_considered=["The Constitution of India"],
        provisions_considered=["Article 21"],
        ratio_summary="Overruled Kharak Singh majority to the extent it denied the right to privacy.",
        is_human_reviewed=True,
    ))

    mgr.add_relationship(PrecedentRelationship(
        relationship_id="REL-PUTTASWAMY-OVERRULES-ADMJABALPUR",
        citing_case_id="IND-JUD-SC-2017-PUTTASWAMY",
        cited_case_id="IND-JUD-SC-1976-ADMJABALPUR",
        treatment=PrecedentTreatment.OVERRULED,
        statutes_considered=["The Constitution of India"],
        provisions_considered=["Article 21"],
        ratio_summary="Expressly overruled the majority opinion in ADM Jabalpur, affirming Justice HR Khanna's dissent.",
        is_human_reviewed=True,
    ))

    # 8. Arjun Panditrao Khotkar v. Kailash Kushanrao Gorantyal (2020) 7 SCC 1 (3-Judge Bench)
    mgr.register_case(CaseLawMetadata(
        case_id="IND-JUD-SC-2020-ARJUN-KHOTKAR",
        case_title="Arjun Panditrao Khotkar v. Kailash Kushanrao Gorantyal (2020) 7 SCC 1",
        official_citation="(2020) 7 SCC 1",
        neutral_citation="2020 INSC 452",
        court="Supreme Court of India",
        bench_strength=BenchStrength.FULL_BENCH,
        judge_count=3,
        decision_date="2020-07-14",
        statutes_considered=["Bharatiya Sakshya Adhiniyam, 2023", "Indian Evidence Act, 1872"],
        provisions_considered=["Section 63 BSA", "Section 65B IEA", "Section 91 CrPC"],
        ratio_decidendi="Certificate under Section 65B(4) IEA / Section 63(4) BSA is an absolute condition precedent to the admissibility of electronic records as secondary evidence.",
        is_human_verified=True,
    ))

    # 9. Anvar P.V. v. P.K. Basheer (2014) 10 SCC 473 (3-Judge Bench)
    mgr.register_case(CaseLawMetadata(
        case_id="IND-JUD-SC-2014-ANVAR-PV",
        case_title="Anvar P.V. v. P.K. Basheer (2014) 10 SCC 473",
        official_citation="(2014) 10 SCC 473",
        neutral_citation="2014 INSC 650",
        court="Supreme Court of India",
        bench_strength=BenchStrength.FULL_BENCH,
        judge_count=3,
        decision_date="2014-09-18",
        statutes_considered=["Indian Evidence Act, 1872"],
        provisions_considered=["Section 65B IEA", "Sections 63 & 65 IEA"],
        ratio_decidendi="Electronic records are governed exclusively by Section 65B; oral evidence cannot substitute the required statutory certificate.",
        is_human_verified=True,
    ))

    # 10. Shafhi Mohammad v. State of H.P. (2018) 2 SCC 801 (2-Judge Bench, overruled)
    mgr.register_case(CaseLawMetadata(
        case_id="IND-JUD-SC-2018-SHAFHI-MOHAMMAD",
        case_title="Shafhi Mohammad v. State of H.P. (2018) 2 SCC 801",
        official_citation="(2018) 2 SCC 801",
        neutral_citation="2018 INSC 92",
        court="Supreme Court of India",
        bench_strength=BenchStrength.DIVISION_BENCH,
        judge_count=2,
        decision_date="2018-01-30",
        ratio_decidendi="Held certificate can be relaxed if party not in possession of device. (Overruled)",
        is_overruled=True,
        overruled_by_case_id="IND-JUD-SC-2020-ARJUN-KHOTKAR",
        is_human_verified=True,
    ))

    # 11. Satender Kumar Antil v. CBI (2022) 10 SCC 51 (2-Judge Bench)
    mgr.register_case(CaseLawMetadata(
        case_id="IND-JUD-SC-2022-ANTIL",
        case_title="Satender Kumar Antil v. Central Bureau of Investigation (2022) 10 SCC 51",
        official_citation="(2022) 10 SCC 51",
        neutral_citation="2022 INSC 690",
        court="Supreme Court of India",
        bench_strength=BenchStrength.DIVISION_BENCH,
        judge_count=2,
        decision_date="2022-07-11",
        statutes_considered=["Bharatiya Nagarik Suraksha Sanhita, 2023", "Code of Criminal Procedure, 1973"],
        provisions_considered=["Section 35 BNSS", "Section 479 BNSS", "Section 41 CrPC", "Section 437 CrPC"],
        ratio_decidendi="Bail is the rule, jail is the exception. Arrest is not mandatory where accused cooperates with notice under Section 41A / 35 BNSS.",
        is_human_verified=True,
    ))

    # 12. Perkins Eastman Architects DPC v. HSCC (2020) 20 SCC 760 (2-Judge Bench)
    mgr.register_case(CaseLawMetadata(
        case_id="IND-JUD-SC-2020-PERKINS-EASTMAN",
        case_title="Perkins Eastman Architects DPC v. HSCC (India) Ltd (2020) 20 SCC 760",
        official_citation="(2020) 20 SCC 760",
        neutral_citation="2019 INSC 1289",
        court="Supreme Court of India",
        bench_strength=BenchStrength.DIVISION_BENCH,
        judge_count=2,
        decision_date="2019-11-26",
        statutes_considered=["Arbitration and Conciliation Act, 1996"],
        provisions_considered=["Section 11(6)", "Section 12(5)", "Seventh Schedule"],
        ratio_decidendi="A person who is ineligible to act as an arbitrator under Section 12(5) is equally disqualified from unilaterally appointing a sole arbitrator.",
        is_human_verified=True,
    ))

    # 13. Satyabrata Ghose v. Mugneeram Bangur & Co. (1954) SCR 310 (3-Judge Bench)
    mgr.register_case(CaseLawMetadata(
        case_id="IND-JUD-SC-1954-SATYABRATA",
        case_title="Satyabrata Ghose v. Mugneeram Bangur & Co. (1954) SCR 310",
        official_citation="(1954) SCR 310",
        court="Supreme Court of India",
        bench_strength=BenchStrength.FULL_BENCH,
        judge_count=3,
        decision_date="1953-09-16",
        statutes_considered=["Indian Contract Act, 1872"],
        provisions_considered=["Section 56"],
        ratio_decidendi="Section 56 of the Contract Act is exhaustive on frustration in India; frustration occurs when an untoward event upsets the foundation of the bargain.",
        is_human_verified=True,
    ))

    # 14. Satyawati Sharma v. Union of India (2008) 5 SCC 287 (2-Judge Bench)
    mgr.register_case(CaseLawMetadata(
        case_id="IND-JUD-SC-2008-SATYAWATI",
        case_title="Satyawati Sharma v. Union of India (2008) 5 SCC 287",
        official_citation="(2008) 5 SCC 287",
        court="Supreme Court of India",
        bench_strength=BenchStrength.DIVISION_BENCH,
        judge_count=2,
        decision_date="2008-04-16",
        statutes_considered=["The Delhi Rent Control Act, 1958", "The Constitution of India"],
        provisions_considered=["Section 14(1)(e) DRC Act", "Article 14"],
        ratio_decidendi="Severed 'let for residential purposes' in Section 14(1)(e) DRC Act, permitting bona fide eviction for commercial premises under Article 14 equality.",
        is_human_verified=True,
    ))

    # Phase 17 Additional Relationships
    mgr.add_relationship(PrecedentRelationship(
        relationship_id="REL-ARJUN-AFFIRMS-ANVAR",
        citing_case_id="IND-JUD-SC-2020-ARJUN-KHOTKAR",
        cited_case_id="IND-JUD-SC-2014-ANVAR-PV",
        treatment=PrecedentTreatment.AFFIRMED,
        statutes_considered=["Indian Evidence Act, 1872", "Bharatiya Sakshya Adhiniyam, 2023"],
        provisions_considered=["Section 65B IEA", "Section 63 BSA"],
        ratio_summary="Reaffirmed the law declared in Anvar P.V. that Section 65B certificate is mandatory.",
        treatment_passage_ref="Paragraph 51 & 72",
        is_human_reviewed=True,
    ))

    mgr.add_relationship(PrecedentRelationship(
        relationship_id="REL-ARJUN-OVERRULES-SHAFHI",
        citing_case_id="IND-JUD-SC-2020-ARJUN-KHOTKAR",
        cited_case_id="IND-JUD-SC-2018-SHAFHI-MOHAMMAD",
        treatment=PrecedentTreatment.OVERRULED,
        statutes_considered=["Indian Evidence Act, 1872"],
        provisions_considered=["Section 65B(4)"],
        ratio_summary="Overruled Shafhi Mohammad for relaxing Section 65B(4) certificate requirement without statutory authority.",
        treatment_passage_ref="Paragraph 72",
        is_human_reviewed=True,
    ))

    mgr.add_relationship(PrecedentRelationship(
        relationship_id="REL-NAVTEJ-OVERRULES-KOUSHAL",
        citing_case_id="IND-JUD-SC-2018-NAVTEJ",
        cited_case_id="IND-JUD-SC-2014-KOUSHAL",
        treatment=PrecedentTreatment.OVERRULED,
        statutes_considered=["Indian Penal Code, 1860", "The Constitution of India"],
        provisions_considered=["Section 377 IPC", "Article 21", "Article 14"],
        ratio_summary="Overruled Suresh Kumar Koushal v. Naz Foundation regarding constitutional invalidity of Section 377 IPC.",
        is_human_reviewed=True,
    ))

    return mgr

