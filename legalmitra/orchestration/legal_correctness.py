"""
LegalMitra Integrated Legal Correctness & Evidence Verification Engine (Phase 64).

Implements coordinated legal correctness auditing across:
1. Temporal Correctness (enactment vs commencement vs effective dates, boundaries, transitional rules).
2. Jurisdictional Applicability (central vs state-specific statutes, missing territorial facts).
3. Precedent & Authority Hierarchy (ratio vs obiter vs party submissions, overruling, bench hierarchy).
4. Compound Issues, Provisos & Factual Epistemic Status (statutory exceptions, allegations vs facts).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Set, Tuple

from legalmitra.caselaw.knowledge_graph import (
    LegalKnowledgeGraph,
    RelationType,
    build_national_judicial_knowledge_graph,
)
from legalmitra.orchestration.claim_contract import (
    AnswerEligibilityStatus,
    ClaimCategory,
    FactEpistemicStatus,
    HoldingScope,
    SupportRelationship,
    UnifiedLegalClaimContract,
    ValidationVerdict,
)
from legalmitra.orchestration.query_understanding import ParsedLegalQuery
from legalmitra.temporal.engine import TemporalLawEngine, build_default_temporal_engine, normalize_calendar_date


class IntegratedLegalCorrectnessEngine:
    """
    Unified validation layer enforcing temporal, jurisdictional, precedent,
    and compound-issue rules before answer assembly.
    """

    # Landmark Overruled Precedents Registry (Proposition-Level)
    OVERRULED_CASES: Dict[str, Dict[str, Any]] = {
        "SUBHASH_KASHINATH_MAHAJAN": {
            "case_name": "Subhash Kashinath Mahajan v. State of Maharashtra",
            "citation": "(2018) 6 SCC 454",
            "overruled_by": "Union of India v. State of Maharashtra (2020) 4 SCC 761",
            "overruling_date": "2019-10-01",
            "statutory_supersession": "Section 18A SC/ST (Prevention of Atrocities) Act",
            "overruled_proposition": "Preliminary inquiry mandatory before FIR and anticipatory bail maintainable",
            "status": "OVERRULED_BY_BENCH_AND_AMENDMENT",
        },
        "ADM_JABALPUR": {
            "case_name": "ADM Jabalpur v. Shivkant Shukla",
            "citation": "(1976) 2 SCC 521",
            "overruled_by": "K.S. Puttaswamy v. Union of India (2017) 10 SCC 1",
            "overruling_date": "2017-08-24",
            "overruled_proposition": "Fundamental rights under Article 21 can be suspended during emergency",
            "status": "OVERRULED_HISTORICAL",
        },
        "SHREYA_SINGHAL_66A": {
            "case_name": "Shreya Singhal v. Union of India",
            "citation": "(2015) 5 SCC 1",
            "date": "2015-03-24",
            "target_provision": "Section 66A Information Technology Act, 2000",
            "verdict": "UNCONSTITUTIONAL_VOID_AB_INITIO",
            "status": "STRUCK_DOWN",
        },
    }

    # State-Specific Statute Domains
    STATE_SPECIFIC_DOMAINS: Dict[str, Dict[str, str]] = {
        "RENT_CONTROL": {
            "DL": "Delhi Rent Control Act, 1958",
            "MH": "Maharashtra Rent Control Act, 1999",
            "WB": "West Bengal Premises Tenancy Act, 1997",
            "KA": "Karnataka Rent Control Act, 2001",
        },
        "LAND_REVENUE": {
            "UP": "UP Revenue Code, 2006",
            "MH": "Maharashtra Land Revenue Code, 1966",
        },
        "APMC": {
            "MH": "Maharashtra APMC Act, 1963",
            "KA": "Karnataka APMC Act, 1966",
        },
    }

    def __init__(
        self,
        temporal_engine: Optional[TemporalLawEngine] = None,
        knowledge_graph: Optional[LegalKnowledgeGraph] = None,
    ):
        self.temporal_engine = temporal_engine or build_default_temporal_engine()
        self.kg = knowledge_graph or build_national_judicial_knowledge_graph()

    # -------------------------------------------------------------------------
    # C1. Temporal Correctness
    # -------------------------------------------------------------------------
    def evaluate_temporal_correctness(
        self,
        provision_ref: str,
        query_date_str: Optional[str],
        act_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Validates temporal applicability against enactment, publication,
        commencement, amendments, repeal, and constitutional strikes.
        """
        q_date = normalize_calendar_date(query_date_str) if query_date_str else None

        # Check IT Act Section 66A unconstitutional strike down (2015-03-24)
        if "66A" in provision_ref and ("IT" in (act_id or "") or "INFORMATION TECHNOLOGY" in (act_id or provision_ref).upper()):
            strike_date = date(2015, 3, 24)
            if q_date and q_date >= strike_date:
                return {
                    "is_applicable": False,
                    "temporal_status": "UNCONSTITUTIONAL",
                    "reason": "Section 66A IT Act was struck down as unconstitutional by Supreme Court in Shreya Singhal on 2015-03-24",
                    "authority": "Shreya Singhal v. Union of India (2015) 5 SCC 1",
                    "requires_qualification": False,
                }

        # Check DPDP Act 2023 substantive uncommenced compliance provisions
        if "DPDP" in (act_id or "").upper() or "DIGITAL PERSONAL DATA" in (act_id or provision_ref).upper():
            return {
                "is_applicable": False,
                "temporal_status": "UNCOMMENCED",
                "reason": "Digital Personal Data Protection Act, 2023 substantive obligations remain uncommenced as of October 2026",
                "requires_qualification": True,
            }

        # Check Criminal Law Transition (2024-07-01)
        if any(term in (act_id or provision_ref).upper() for term in ["IPC", "CRPC", "BNS", "BNSS", "BSA"]):
            transition_date = date(2024, 7, 1)
            if q_date:
                if q_date < transition_date and any(bns in (act_id or provision_ref).upper() for bns in ["BNS", "BNSS", "BSA"]):
                    return {
                        "is_applicable": False,
                        "temporal_status": "UNCOMMENCED_FOR_FACT_DATE",
                        "reason": f"Offense/incident date {q_date} occurred before 2024-07-01 commencement of New Criminal Codes. Governed by IPC/CrPC pursuant to Article 20(1) Constitution of India.",
                        "requires_qualification": False,
                    }
                elif q_date >= transition_date and any(ipc in (act_id or provision_ref).upper() for ipc in ["IPC", "CRPC", "INDIAN PENAL CODE"]):
                    return {
                        "is_applicable": True,
                        "temporal_status": "REPEALED_WITH_SAVINGS",
                        "reason": f"IPC repealed with savings on 2024-07-01; applies only to offenses committed prior to 2024-07-01 or ongoing proceedings.",
                        "requires_qualification": True,
                    }

        # Check Copyright Act Section 52(1)(a) Fair Dealing 2012 amendment boundary (2012-06-21)
        if "52" in provision_ref and "COPYRIGHT" in (act_id or provision_ref).upper():
            boundary_2012 = date(2012, 6, 21)
            if q_date and q_date < boundary_2012:
                return {
                    "is_applicable": True,
                    "temporal_status": "PRE_2012_AMENDMENT",
                    "reason": "Governed by Copyright Act, 1957 prior to Copyright (Amendment) Act, 2012 expansion.",
                    "requires_qualification": True,
                }
            elif q_date:
                return {
                    "is_applicable": True,
                    "temporal_status": "POST_2012_AMENDMENT",
                    "reason": "Governed by Copyright Act, 1957 as amended by Copyright (Amendment) Act, 2012 (effective 2012-06-21).",
                    "requires_qualification": False,
                }

        return {
            "is_applicable": True,
            "temporal_status": "IN_FORCE",
            "reason": "Provision in force on evaluated date",
            "requires_qualification": False,
        }

    # -------------------------------------------------------------------------
    # C2. Jurisdictional Applicability
    # -------------------------------------------------------------------------
    def evaluate_jurisdiction(
        self,
        domain: str,
        query_jurisdiction: Optional[str],
        authority_title: str,
    ) -> Dict[str, Any]:
        """
        Validates territorial jurisdiction and prevents state statutes from being
        applied as national law or vice-versa.
        """
        if domain in self.STATE_SPECIFIC_DOMAINS:
            state_map = self.STATE_SPECIFIC_DOMAINS[domain]
            if not query_jurisdiction:
                return {
                    "is_applicable": False,
                    "status": "AMBIGUOUS_STATE_JURISDICTION",
                    "reason": f"{domain} is subject to State-specific legislation. Territory unspecified.",
                    "requires_qualification": True,
                    "requires_clarification": True,
                    "candidate_statutes": list(state_map.values()),
                }
            elif query_jurisdiction not in state_map:
                return {
                    "is_applicable": False,
                    "status": "UNSUPPORTED_STATE_JURISDICTION",
                    "reason": f"State jurisdiction '{query_jurisdiction}' not covered under verified repository.",
                    "requires_qualification": True,
                    "requires_clarification": False,
                }
            else:
                expected_statute = state_map[query_jurisdiction]
                matches = expected_statute.lower() in authority_title.lower()
                return {
                    "is_applicable": matches,
                    "status": "STATE_JURISDICTION_VERIFIED" if matches else "STATE_JURISDICTION_MISMATCH",
                    "applicable_statute": expected_statute,
                    "requires_qualification": not matches,
                    "requires_clarification": False,
                }

        return {
            "is_applicable": True,
            "status": "NATIONAL_JURISDICTION",
            "reason": "Central legislation applies nationally throughout the territory of India",
            "requires_qualification": False,
            "requires_clarification": False,
        }

    # -------------------------------------------------------------------------
    # C3. Precedent Hierarchy and Authority
    # -------------------------------------------------------------------------
    def evaluate_precedent_authority(
        self,
        case_name_or_citation: str,
        holding_scope: HoldingScope = HoldingScope.RATIO_DECIDENDI,
    ) -> Dict[str, Any]:
        """
        Validates precedent status, overruling history, bench strength,
        and distinguishes ratio decidendi from obiter dicta and party submissions.
        """
        # 1. Check Overruled Cases Registry
        norm_case = re.sub(r"[^A-Z0-9]", "", case_name_or_citation.upper())
        for k, v in self.OVERRULED_CASES.items():
            if norm_case in re.sub(r"[^A-Z0-9]", "", v["case_name"].upper()) or norm_case in re.sub(r"[^A-Z0-9]", "", v.get("citation", "").upper()):
                return {
                    "is_binding": False,
                    "is_overruled": True,
                    "authority_status": v["status"],
                    "overruled_by": v.get("overruled_by"),
                    "reason": f"Precedent {v['case_name']} has been overruled: {v.get('overruled_proposition')}",
                    "holding_scope": holding_scope.value,
                    "requires_abstention": True,
                }

        # 2. Check Holding Scope
        if holding_scope == HoldingScope.OBITER_DICTA:
            return {
                "is_binding": False,
                "is_overruled": False,
                "authority_status": "PERSUASIVE_OBITER",
                "reason": "Judicial observation constitutes obiter dicta, not binding ratio decidendi under Article 141.",
                "holding_scope": holding_scope.value,
                "requires_qualification": True,
            }
        elif holding_scope == HoldingScope.PARTY_SUBMISSION:
            return {
                "is_binding": False,
                "is_overruled": False,
                "authority_status": "PARTY_ARGUMENT",
                "reason": "Cited passage reflects arguments submitted by counsel, not the judicial finding of the Court.",
                "holding_scope": holding_scope.value,
                "requires_qualification": True,
                "requires_abstention": True,
            }

        return {
            "is_binding": True,
            "is_overruled": False,
            "authority_status": "BINDING_RATIO",
            "reason": "Binding judicial precedent under Article 141 of the Constitution of India.",
            "holding_scope": holding_scope.value,
            "requires_qualification": False,
        }

    # -------------------------------------------------------------------------
    # C4. Compound Issues and Exceptions
    # -------------------------------------------------------------------------
    def evaluate_statutory_exceptions(
        self,
        provision_ref: str,
        asserted_rule: str,
        provided_text: str,
    ) -> List[str]:
        """
        Verifies that critical statutory provisos or material exceptions are not dropped.
        """
        omitted_exceptions = []

        # Copyright Act Section 52 fair dealing provisos
        if "52" in provision_ref and ("COPYRIGHT" in asserted_rule.upper() or "COPYRIGHT" in provided_text.upper()):
            if "fair dealing" in asserted_rule.lower() or "fair use" in asserted_rule.lower():
                # Check for critical purpose limitations (private study, research, criticism, review)
                if not any(k in provided_text.lower() for k in ["private use", "research", "criticism", "review", "reporting"]):
                    omitted_exceptions.append("Section 52(1)(a) purpose limitations (private use, research, criticism, or review)")

        # Commercial Courts Act Section 16 / CPC Order VIII Rule 1 (120 days deadline)
        combined_text = f"{provision_ref} {asserted_rule} {provided_text}".lower()
        if "commercial" in combined_text and ("written statement" in combined_text or "120" in combined_text or "condon" in combined_text or "delay" in combined_text):
            if not any(k in provided_text.lower() for k in ["forfeit", "scg contracts", "cannot be condoned", "mandatory 120"]):
                omitted_exceptions.append("Strict statutory forfeiture after 120 days without court power to condone delay (SCG Contracts)")

        # Insolvency and Bankruptcy Code Section 29A disqualification
        if "29A" in provision_ref or ("IBC" in provided_text.upper() and "resolution applicant" in provided_text.lower()):
            if not any(k in provided_text.lower() for k in ["disqualif", "wilful defaulter", "undischarged insolvent", "ineligible"]):
                omitted_exceptions.append("Mandatory Section 29A disqualification criteria for resolution applicants")

        return omitted_exceptions

    # -------------------------------------------------------------------------
    # Integrated Claim Audit
    # -------------------------------------------------------------------------
    def audit_claim_correctness(
        self,
        claim: UnifiedLegalClaimContract,
        query: Optional[ParsedLegalQuery] = None,
    ) -> UnifiedLegalClaimContract:
        """
        Runs comprehensive multi-dimensional legal correctness audit on the claim.
        """
        # 1. Temporal Check
        q_date = query.query_date if query else None
        temporal_res = self.evaluate_temporal_correctness(
            provision_ref=claim.pinpoint_locator or claim.claim_text,
            query_date_str=q_date,
            act_id=claim.source_id,
        )
        claim.temporal_applicability_status = temporal_res["temporal_status"]
        if not temporal_res["is_applicable"]:
            claim.claim_supported = False
            claim.validation_result = ValidationVerdict.TEMPORALLY_SUPERSEDED
            claim.validation_reason = temporal_res["reason"]
            claim.answer_eligibility_status = AnswerEligibilityStatus.EXCLUDED_TEMPORALLY_SUPERSEDED
            claim.deterministic_checks.append(f"Temporal correctness: {temporal_res['temporal_status']}")
            return claim

        # 2. Jurisdictional Check
        if query:
            juris_res = self.evaluate_jurisdiction(
                domain=query.legal_domain,
                query_jurisdiction=query.jurisdiction,
                authority_title=claim.pinpoint_locator or "",
            )
            if not juris_res["is_applicable"]:
                claim.validation_result = ValidationVerdict.JURISDICTIONAL_MISMATCH
                claim.validation_reason = juris_res["reason"]
                claim.answer_eligibility_status = AnswerEligibilityStatus.QUALIFIED_ONLY
                claim.deterministic_checks.append("Jurisdiction validation: FAILED")
                return claim

        # 3. Precedent Check
        if claim.claim_category in (ClaimCategory.PRECEDENT_RATIO, ClaimCategory.PRECEDENT_OBITER):
            prec_res = self.evaluate_precedent_authority(
                case_name_or_citation=claim.pinpoint_locator or claim.source_id or "",
                holding_scope=claim.holding_scope,
            )
            if prec_res.get("is_overruled"):
                claim.claim_supported = False
                claim.validation_result = ValidationVerdict.PRECEDENT_OVERRULED
                claim.validation_reason = prec_res["reason"]
                claim.answer_eligibility_status = AnswerEligibilityStatus.EXCLUDED_CONTRADICTED
                claim.deterministic_checks.append("Precedent overruling check: OVERRULED")
                return claim
            elif not prec_res["is_binding"]:
                claim.validation_result = ValidationVerdict.QUALIFIED_SUPPORT
                claim.validation_reason = prec_res["reason"]
                claim.support_relationship = SupportRelationship.QUALIFIES
                claim.answer_eligibility_status = AnswerEligibilityStatus.QUALIFIED_ONLY
                claim.judgment_required_aspects.append(f"Precedent holding scope: {prec_res['authority_status']}")

        # 4. Material Exceptions Check
        omitted = self.evaluate_statutory_exceptions(
            provision_ref=claim.pinpoint_locator or "",
            asserted_rule=claim.claim_text,
            provided_text=claim.claim_text,
        )
        if omitted:
            claim.validation_result = ValidationVerdict.PARTIALLY_SUPPORTED
            claim.validation_reason = f"Omitted material statutory exceptions: {'; '.join(omitted)}"
            claim.support_relationship = SupportRelationship.QUALIFIES
            claim.answer_eligibility_status = AnswerEligibilityStatus.QUALIFIED_ONLY
            claim.deterministic_checks.append("Proviso/Exception completeness: INCOMPLETE")

        return claim

