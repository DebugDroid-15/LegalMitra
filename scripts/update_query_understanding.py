"""
Update query_understanding.py for Phase 56:
- Add procedural_posture, material_unknowns, issue_dependencies, decomposed_issues, statutory_exceptions_identified.
- Extract procedural postures, multi-issue decompositions, material unknowns, and statutory exceptions.
"""

from pathlib import Path

file_path = Path("legalmitra/orchestration/query_understanding.py")
content = file_path.read_text(encoding="utf-8")

# 1. Update ParsedLegalQuery dataclass
old_dataclass_end = """    is_adversarial_injection: bool = False
    adversarial_notes: Optional[str] = None"""

new_dataclass_end = """    is_adversarial_injection: bool = False
    adversarial_notes: Optional[str] = None
    procedural_posture: Optional[str] = None
    material_unknowns: List[Dict[str, str]] = field(default_factory=list)
    issue_dependencies: List[Dict[str, Any]] = field(default_factory=list)
    decomposed_issues: List[Dict[str, Any]] = field(default_factory=list)
    statutory_exceptions_identified: List[str] = field(default_factory=list)"""

assert old_dataclass_end in content, "Could not find old_dataclass_end"
content = content.replace(old_dataclass_end, new_dataclass_end, 1)

# 2. Add HSA, SRA, NI, IBC checks to applicable_acts & provisions
acts_anchor = """        if any(term in q_lower for term in ["commercial court", "commercial courts act", "pre-institution mediation"]):
            acts.append("IND-STAT-COMMERCIAL_COURTS-2015")
            provisions.append("Section 12A")"""

new_acts = """        if any(term in q_lower for term in ["commercial court", "commercial courts act", "pre-institution mediation"]):
            acts.append("IND-STAT-COMMERCIAL_COURTS-2015")
            provisions.append("Section 12A")
        if any(term in q_lower for term in ["hindu succession", "coparcen", "daughter coparcener", "ancestral property"]):
            acts.append("IND-STAT-HSA-1956")
            provisions.append("Section 6")
        if any(term in q_lower for term in ["specific relief", "infrastructure project", "section 20a"]) and "IND-STAT-SRA-1963" not in acts:
            acts.append("IND-STAT-SRA-1963")
            if "20a" in q_lower or "infrastructure" in q_lower:
                provisions.append("Section 20A")
            if "10" in q_lower:
                provisions.append("Section 10")
        if any(term in q_lower for term in ["ibc", "insolvency and bankruptcy", "clean slate", "resolution plan"]) and "IND-STAT-IBC-2016" not in acts:
            acts.append("IND-STAT-IBC-2016")
            if "32a" in q_lower or "clean slate" in q_lower:
                provisions.append("Section 32A")"""

assert acts_anchor in content, "Could not find acts_anchor"
content = content.replace(acts_anchor, new_acts, 1)

# 3. Add procedural posture and multi-issue decomposition before `if not issues:`
issues_anchor = """        if not issues:
            issues.append(f"Substantive and procedural rights governing '{clean_q[:60]}...' under Indian law")"""

decomposition_logic = """        # Procedural Posture Extraction (Phase 56)
        posture = "GENERAL_LEGAL_INQUIRY"
        if any(t in q_lower for t in ["statutory demand notice", "notice under section 138", "demand notice", "legal notice"]):
            posture = "STATUTORY_PRE_SUIT_NOTICE"
        elif any(t in q_lower for t in ["pre-institution mediation", "section 12a", "mediation non-starter"]):
            posture = "COMMERCIAL_PRE_INSTITUTION_MEDIATION"
        elif any(t in q_lower for t in ["fir", "investigation", "arrest", "police custody", "remand"]):
            posture = "INVESTIGATION_STAGE"
        elif any(t in q_lower for t in ["anticipatory bail", "regular bail", "bail application"]):
            posture = "BAIL_APPLICATION"
        elif any(t in q_lower for t in ["quashing", "section 482", "section 528"]):
            posture = "QUASHING_PETITION"
        elif any(t in q_lower for t in ["mandate extension", "extension of mandate", "section 29a"]):
            posture = "ARBITRAL_MANDATE_EXTENSION"
        elif any(t in q_lower for t in ["setting aside award", "section 34", "challenge award"]):
            posture = "AWARD_CHALLENGE"
        elif any(t in q_lower for t in ["suit for specific performance", "injunction", "civil suit"]):
            posture = "ORIGINAL_CIVIL_SUIT"
        elif any(t in q_lower for t in ["retrenchment", "industrial tribunal", "conciliation"]):
            posture = "LABOUR_TRIBUNAL_PROCEEDING"
        elif any(t in q_lower for t in ["appeal", "revision", "special leave petition", "slp"]):
            posture = "APPELLATE_PROCEEDING"

        # Multi-Issue Decomposition & Rule Dependency Identification (Phase 56)
        decomposed_issues = []
        issue_dependencies = []
        statutory_exceptions = []
        material_unknowns = []

        # Compound Pattern 1: Specific Relief Act Sec 10 + Sec 20A Infrastructure Bar
        if ("specific relief" in q_lower or "specific performance" in q_lower or "contract" in q_lower) and ("infrastructure" in q_lower or "20a" in q_lower):
            decomposed_issues.append({
                "issue_id": "ISSUE-1",
                "statement": "Entitlement to specific performance of contract under Section 10 of Specific Relief Act, 1963",
                "governing_statute": "IND-STAT-SRA-1963 Section 10",
                "relationship_type": "PRIMARY_RULE",
                "prerequisite_issue_id": None,
            })
            decomposed_issues.append({
                "issue_id": "ISSUE-2",
                "statement": "Statutory bar on granting injunctions in infrastructure projects under Section 20A and Schedule of Specific Relief Act",
                "governing_statute": "IND-STAT-SRA-1963 Section 20A",
                "relationship_type": "STATUTORY_EXCEPTION",
                "prerequisite_issue_id": "ISSUE-1",
            })
            issue_dependencies.append({
                "dependent_issue_id": "ISSUE-2",
                "governing_issue_id": "ISSUE-1",
                "dependency_type": "STATUTORY_EXCEPTION_BAR",
                "description": "Section 20A operates as a statutory bar overriding general injunctive relief if project falls under infrastructure schedule."
            })
            statutory_exceptions.append("Section 20A(1) SRA: No injunction shall be granted in infrastructure project suits where it causes impediment or delay.")

        # Compound Pattern 2: Hindu Succession Act Sec 6 Coparcenary + Pre-2004 Partition Proviso
        elif ("hindu succession" in q_lower or "coparcen" in q_lower or "daughter" in q_lower) and ("partition" in q_lower or "proviso" in q_lower or "2004" in q_lower or "ancestral" in q_lower):
            decomposed_issues.append({
                "issue_id": "ISSUE-1",
                "statement": "Right of daughter as coparcener by birth under Section 6(1) of Hindu Succession Act as amended in 2005",
                "governing_statute": "IND-STAT-HSA-1956 Section 6(1)",
                "relationship_type": "PRIMARY_RULE",
                "prerequisite_issue_id": None,
            })
            decomposed_issues.append({
                "issue_id": "ISSUE-2",
                "statement": "Statutory exemption preserving registered partitions executed prior to 20 December 2004 under Section 6(1) proviso",
                "governing_statute": "IND-STAT-HSA-1956 Section 6(1) Proviso",
                "relationship_type": "STATUTORY_EXCEPTION",
                "prerequisite_issue_id": "ISSUE-1",
            })
            issue_dependencies.append({
                "dependent_issue_id": "ISSUE-2",
                "governing_issue_id": "ISSUE-1",
                "dependency_type": "STATUTORY_SAVINGS_PROVISO",
                "description": "Section 6(1) proviso saves partitions and dispositions executed before 20 December 2004 from being reopened."
            })
            statutory_exceptions.append("Section 6(1) Proviso HSA: Nothing contained in sub-section (1) shall affect or invalidate any disposition or alienation, including any partition, which took place before 20 December 2004.")
            material_unknowns.append({
                "unknown_fact": "Date and registration status of family partition",
                "governing_provision": "Section 6(1) Proviso, Hindu Succession Act, 1956",
                "legal_consequence": "If partition was registered before 20 Dec 2004, it is protected; if executed thereafter, daughter is entitled to reopen coparcenary share.",
            })

        # Compound Pattern 3: Cheque Bounce NI Act Sec 138 Notice + Sec 142 Limitation
        elif any(t in q_lower for t in ["cheque bounce", "section 138", "dishonour", "138 of ni act"]):
            decomposed_issues.append({
                "issue_id": "ISSUE-1",
                "statement": "Service of 15-day statutory demand notice within 30 days of dishonour memo under Section 138 proviso (b)",
                "governing_statute": "IND-STAT-NI-1881 Section 138",
                "relationship_type": "PROCEDURAL_PREREQUISITE",
                "prerequisite_issue_id": None,
            })
            decomposed_issues.append({
                "issue_id": "ISSUE-2",
                "statement": "Limitation period of 1 month for institution of criminal complaint under Section 142(1)(b) of Negotiable Instruments Act",
                "governing_statute": "IND-STAT-NI-1881 Section 142(1)(b)",
                "relationship_type": "PRIMARY_RULE",
                "prerequisite_issue_id": "ISSUE-1",
            })
            issue_dependencies.append({
                "dependent_issue_id": "ISSUE-2",
                "governing_issue_id": "ISSUE-1",
                "dependency_type": "PROCEDURAL_PREREQUISITE",
                "description": "Cause of action under Section 142 arises only upon failure of drawer to pay within 15 days of statutory notice under Section 138(c)."
            })
            statutory_exceptions.append("Section 142(1)(b) Proviso NI Act: Court may take cognizance of complaint after 1-month limitation period if complainant satisfies court of sufficient cause.")

        # Compound Pattern 4: Retrenchment under IDA Sec 25F + Uncommenced Labour Code
        elif ("retrenchment" in q_lower or "25f" in q_lower) and any(t in q_lower for t in ["labour code", "code on wages", "industrial relations code"]):
            decomposed_issues.append({
                "issue_id": "ISSUE-1",
                "statement": "Substantive validity and conditions precedent for retrenchment of workmen under Section 25F Industrial Disputes Act, 1947",
                "governing_statute": "IND-STAT-IDA-1947 Section 25F",
                "relationship_type": "PRIMARY_RULE",
                "prerequisite_issue_id": None,
            })
            decomposed_issues.append({
                "issue_id": "ISSUE-2",
                "statement": "Inapplicability of uncommenced Industrial Relations Code, 2020 pending Central Government Gazette commencement notification",
                "governing_statute": "IND-STAT-IRCODE-2020 Section 1(3)",
                "relationship_type": "UNCOMMENCED_REGIME",
                "prerequisite_issue_id": None,
            })
            issue_dependencies.append({
                "dependent_issue_id": "ISSUE-2",
                "governing_issue_id": "ISSUE-1",
                "dependency_type": "TEMPORAL_COEXISTENCE",
                "description": "Predecessor Act (IDA 1947) remains operative substantive law; uncommenced Code cannot be enforced."
            })

        # Compound Pattern 5: Commercial Courts Act Sec 12A Mediation + Urgent Interim Relief
        elif ("commercial court" in q_lower or "12a" in q_lower or "pre-institution mediation" in q_lower) and ("urgent" in q_lower or "interim" in q_lower or "suit" in q_lower):
            decomposed_issues.append({
                "issue_id": "ISSUE-1",
                "statement": "Mandatory nature of pre-institution mediation under Section 12A Commercial Courts Act, 2015",
                "governing_statute": "IND-STAT-COMMERCIAL_COURTS-2015 Section 12A",
                "relationship_type": "PRIMARY_RULE",
                "prerequisite_issue_id": None,
            })
            decomposed_issues.append({
                "issue_id": "ISSUE-2",
                "statement": "Statutory exemption from pre-institution mediation where urgent interim relief is contemplated",
                "governing_statute": "IND-STAT-COMMERCIAL_COURTS-2015 Section 12A(1)",
                "relationship_type": "STATUTORY_EXCEPTION",
                "prerequisite_issue_id": "ISSUE-1",
            })
            issue_dependencies.append({
                "dependent_issue_id": "ISSUE-2",
                "governing_issue_id": "ISSUE-1",
                "dependency_type": "STATUTORY_EXCEPTION",
                "description": "Section 12A(1) exempts suits that contemplate urgent interim relief from mandatory pre-institution mediation."
            })
            statutory_exceptions.append("Section 12A(1) Commercial Courts Act: Suit which does not contemplate any urgent interim relief shall not be instituted unless plaintiff exhausts pre-institution mediation.")

        # Compound Pattern 6: IBC Sec 32A Clean Slate + Promoter Liability Proviso
        elif ("ibc" in q_lower or "clean slate" in q_lower or "resolution plan" in q_lower) and ("promoter" in q_lower or "director" in q_lower or "offence" in q_lower or "32a" in q_lower):
            decomposed_issues.append({
                "issue_id": "ISSUE-1",
                "statement": "Cessation of liability of corporate debtor for prior offences upon approval of resolution plan under Section 32A(1) IBC",
                "governing_statute": "IND-STAT-IBC-2016 Section 32A(1)",
                "relationship_type": "PRIMARY_RULE",
                "prerequisite_issue_id": None,
            })
            decomposed_issues.append({
                "issue_id": "ISSUE-2",
                "statement": "Continuation of liability and prosecution of erstwhile promoters/directors under Section 32A(1) proviso",
                "governing_statute": "IND-STAT-IBC-2016 Section 32A(1) Proviso",
                "relationship_type": "STATUTORY_EXCEPTION",
                "prerequisite_issue_id": "ISSUE-1",
            })
            issue_dependencies.append({
                "dependent_issue_id": "ISSUE-2",
                "governing_issue_id": "ISSUE-1",
                "dependency_type": "STATUTORY_EXCEPTION",
                "description": "Section 32A(1) proviso explicitly preserves criminal liability of designated partner, promoter, or key managerial personnel."
            })
            statutory_exceptions.append("Section 32A(1) Proviso IBC: Every person who was a designated partner or officer in default shall continue to be liable to be prosecuted and punished.")

        # If decomposed issues identified, update candidate_issues
        if decomposed_issues:
            issues = [d["statement"] for d in decomposed_issues]

        if not issues:
            issues.append(f"Substantive and procedural rights governing '{clean_q[:60]}...' under Indian law")"""

assert issues_anchor in content, "Could not find issues_anchor"
content = content.replace(issues_anchor, decomposition_logic, 1)

# 4. Update the return ParsedLegalQuery(...) statement
old_return = """        return ParsedLegalQuery(
            original_query=clean_q,
            legal_domain=primary_domain,
            sub_domains=sub_domains,
            candidate_issues=issues,
            events_and_dates=events_and_dates,
            query_date=query_date,
            user_supplied_facts=user_facts,
            alleged_facts_unverified=alleged_facts,
            implicit_assumptions=implicit_assumptions,
            parties_and_roles=parties,
            jurisdiction=detected_jurisdiction,
            applicable_acts=acts,
            candidate_provisions=provisions,
            delegated_instruments=delegated_instruments,
            candidate_precedents=precedents,
            ambiguous_terms=ambiguous_terms,
            missing_facts=missing_facts,
            clarification_necessary=clarification_necessary,
            clarification_prompt=clarification_prompt,
            source_coverage_requirements=acts + [f"Rule: {r}" for r in delegated_instruments],
            is_adversarial_injection=is_adversarial,
            adversarial_notes=adv_notes,
        )"""

new_return = """        return ParsedLegalQuery(
            original_query=clean_q,
            legal_domain=primary_domain,
            sub_domains=sub_domains,
            candidate_issues=issues,
            events_and_dates=events_and_dates,
            query_date=query_date,
            user_supplied_facts=user_facts,
            alleged_facts_unverified=alleged_facts,
            implicit_assumptions=implicit_assumptions,
            parties_and_roles=parties,
            jurisdiction=detected_jurisdiction,
            applicable_acts=acts,
            candidate_provisions=provisions,
            delegated_instruments=delegated_instruments,
            candidate_precedents=precedents,
            ambiguous_terms=ambiguous_terms,
            missing_facts=missing_facts,
            clarification_necessary=clarification_necessary,
            clarification_prompt=clarification_prompt,
            source_coverage_requirements=acts + [f"Rule: {r}" for r in delegated_instruments],
            is_adversarial_injection=is_adversarial,
            adversarial_notes=adv_notes,
            procedural_posture=posture,
            material_unknowns=material_unknowns,
            issue_dependencies=issue_dependencies,
            decomposed_issues=decomposed_issues,
            statutory_exceptions_identified=statutory_exceptions,
        )"""

assert old_return in content, "Could not find old_return"
content = content.replace(old_return, new_return, 1)

file_path.write_text(content, encoding="utf-8")
print(f"Successfully updated {file_path}")
