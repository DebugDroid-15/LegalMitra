import re
from pathlib import Path

file_path = Path("legalmitra/temporal/engine.py")
content = file_path.read_text(encoding="utf-8")

# 1. Add normalize_calendar_date and update ProvisionTemporalVersion
old_version_block = """@dataclass
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
        \"\"\"Determines if this version of the provision was legally operative on the given date.\"\"\"
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

        return True"""

new_version_block = """def normalize_calendar_date(date_str: Optional[str]) -> Optional[datetime.date]:
    \"\"\"
    Normalizes a legal date string to a calendar date (YYYY-MM-DD) in Indian Standard Time context.
    Safely strips time and timezone information without calendar-day displacement.
    \"\"\"
    if not date_str or not isinstance(date_str, str):
        return None
    cleaned = date_str.strip()
    if "T" in cleaned:
        cleaned = cleaned.split("T")[0]
    elif " " in cleaned:
        cleaned = cleaned.split(" ")[0]
    try:
        return datetime.date.fromisoformat(cleaned)
    except ValueError:
        return None


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
    is_retrospective: bool = False
    retrospective_basis: Optional[str] = None
    conflicting_notifications: List[str] = field(default_factory=list)

    def is_operative_on(self, query_date_str: str) -> bool:
        \"\"\"Determines if this version of the provision was legally operative on the given date.\"\"\"
        q_date = normalize_calendar_date(query_date_str)
        if not q_date:
            return False

        # If uncommenced
        if self.commencement_date:
            c_date = normalize_calendar_date(self.commencement_date)
            if c_date and q_date < c_date:
                return False
        else:
            # If no commencement date is specified, it has not commenced unless explicitly active
            if self.is_phased_commencement:
                return False

        # Check effective window
        if self.version_effective_from:
            ef_date = normalize_calendar_date(self.version_effective_from)
            if ef_date and q_date < ef_date:
                if not (self.is_retrospective and self.retrospective_basis):
                    return False

        if self.version_effective_until:
            until_date = normalize_calendar_date(self.version_effective_until)
            if until_date and q_date > until_date:
                return False

        # Check repeal
        if self.repeal_date:
            r_date = normalize_calendar_date(self.repeal_date)
            if r_date and q_date >= r_date:
                # If repealed, it is not currently operative as primary law, unless saved for pending matters
                return False

        return True"""

if old_version_block in content:
    content = content.replace(old_version_block, new_version_block)
    print("Replaced ProvisionTemporalVersion block")
else:
    print("WARNING: old_version_block not found directly, trying normalized newlines")
    content = content.replace(old_version_block.replace("\n", "\r\n"), new_version_block.replace("\n", "\r\n"))

# 2. Update resolve_point_in_time_applicability
old_resolve = """    def resolve_point_in_time_applicability(
        self,
        provision_id: str,
        query_date_str: Optional[str] = None,
        jurisdiction: str = "IN",
        pending_proceeding_commenced_prior: bool = False,
    ) -> Dict[str, Any]:
        \"\"\"
        Determines the precise statutory applicability of a provision at a specified date
        using half-open interval semantics [effective_from, effective_until) and savings clauses.
        \"\"\"
        if not query_date_str:
            return {
                "provision_id": provision_id,
                "query_date": None,
                "jurisdiction": jurisdiction,
                "applicability_state": StatutoryApplicabilityState.INSUFFICIENT_EVIDENCE,
                "applicable_version": None,
                "is_applicable": False,
                "savings_applied": False,
                "rationale": "No query date provided; temporal applicability cannot be definitively established.",
            }

        try:
            q_date = datetime.date.fromisoformat(query_date_str)
        except ValueError:
            return {
                "provision_id": provision_id,
                "query_date": query_date_str,
                "jurisdiction": jurisdiction,
                "applicability_state": StatutoryApplicabilityState.CONFLICTING_TEMPORAL_EVIDENCE,
                "applicable_version": None,
                "is_applicable": False,
                "savings_applied": False,
                "rationale": f"Invalid ISO date format: '{query_date_str}'.",
            }

        versions = self._versions.get(provision_id, [])
        if not versions:
            return {
                "provision_id": provision_id,
                "query_date": query_date_str,
                "jurisdiction": jurisdiction,
                "applicability_state": StatutoryApplicabilityState.INSUFFICIENT_EVIDENCE,
                "applicable_version": None,
                "is_applicable": False,
                "savings_applied": False,
                "rationale": f"No temporal versions registered for provision ID '{provision_id}'.",
            }

        # Check parent statute lifecycle
        statute_id = versions[0].statute_id
        statute = self.get_statute(statute_id)

        # 1. Check if uncommenced / partially commenced statute
        if statute and not statute.is_fully_commenced:
            if not statute.commencement_date:
                return {
                    "provision_id": provision_id,
                    "statute_id": statute_id,
                    "query_date": query_date_str,
                    "jurisdiction": jurisdiction,
                    "applicability_state": StatutoryApplicabilityState.PARTIALLY_COMMENCED,
                    "applicable_version": None,
                    "is_applicable": False,
                    "savings_applied": False,
                    "rationale": f"Parent statute '{statute.title}' is uncommenced or subject to phased notification; provision not generally in force.",
                }

        # 2. Check each version
        # Find version operative on query_date
        matched_version: Optional[ProvisionTemporalVersion] = None
        for v in versions:
            # Check commencement
            if v.commencement_date:
                try:
                    c_date = datetime.date.fromisoformat(v.commencement_date)
                    if q_date < c_date:
                        continue
                except ValueError:
                    pass
            elif v.is_phased_commencement:
                continue

            # Effective from [
            if v.version_effective_from:
                try:
                    ef_date = datetime.date.fromisoformat(v.version_effective_from)
                    if q_date < ef_date:
                        continue
                except ValueError:
                    pass

            # Effective until boundary check
            if v.version_effective_until:
                try:
                    eu_date = datetime.date.fromisoformat(v.version_effective_until)
                    # If version_effective_until is given as the final day of validity,
                    # q_date > eu_date means it has expired.
                    if q_date > eu_date:
                        continue
                except ValueError:
                    pass

            # Repeal check
            if v.repeal_date:
                try:
                    r_date = datetime.date.fromisoformat(v.repeal_date)
                    if q_date >= r_date:
                        if pending_proceeding_commenced_prior and v.savings_applies_to_pending:
                            matched_version = v
                            break
                        continue
                except ValueError:
                    pass

            matched_version = v
            break

        if matched_version:
            # Check if this matched version is historical or currently operative
            is_current = (matched_version.version_effective_until is None) and (matched_version.repeal_date is None)
            state = StatutoryApplicabilityState.CONFIRMED_APPLICABLE if is_current else StatutoryApplicabilityState.CONFIRMED_HISTORICAL
            
            savings_active = False
            if matched_version.repeal_date:
                try:
                    r_date = datetime.date.fromisoformat(matched_version.repeal_date)
                    if q_date >= r_date and pending_proceeding_commenced_prior:
                        savings_active = True
                        state = StatutoryApplicabilityState.CONFIRMED_HISTORICAL
                except ValueError:
                    pass

            return {
                "provision_id": provision_id,
                "statute_id": statute_id,
                "query_date": query_date_str,
                "jurisdiction": jurisdiction,
                "applicability_state": state,
                "applicable_version": matched_version.to_dict(),
                "version_number": matched_version.version_number,
                "is_applicable": True,
                "savings_applied": savings_active,
                "rationale": f"Version {matched_version.version_number} was in force on {query_date_str} (effective from {matched_version.version_effective_from}).",
            }

        # If not matched, determine why (not yet in force vs repealed/superseded)
        first_version = versions[0]
        if first_version.commencement_date or first_version.version_effective_from:
            earliest_str = first_version.commencement_date or first_version.version_effective_from
            try:
                earliest_date = datetime.date.fromisoformat(earliest_str)
                if q_date < earliest_date:
                    return {
                        "provision_id": provision_id,
                        "statute_id": statute_id,
                        "query_date": query_date_str,
                        "jurisdiction": jurisdiction,
                        "applicability_state": StatutoryApplicabilityState.NOT_YET_IN_FORCE,
                        "applicable_version": None,
                        "is_applicable": False,
                        "savings_applied": False,
                        "rationale": f"Provision '{provision_id}' was not yet in force on {query_date_str} (earliest commencement: {earliest_str}).",
                    }
            except ValueError:
                pass

        # Otherwise provision is superseded or repealed
        return {
            "provision_id": provision_id,
            "statute_id": statute_id,
            "query_date": query_date_str,
            "jurisdiction": jurisdiction,
            "applicability_state": StatutoryApplicabilityState.SUPERSEDED_OR_REPEALED,
            "applicable_version": None,
            "is_applicable": False,
            "savings_applied": False,
            "rationale": f"Provision '{provision_id}' has been repealed or superseded prior to query date {query_date_str}.",
        }"""

new_resolve = """    def resolve_point_in_time_applicability(
        self,
        provision_id: str,
        query_date_str: Optional[str] = None,
        jurisdiction: str = "IN",
        pending_proceeding_commenced_prior: bool = False,
    ) -> Dict[str, Any]:
        \"\"\"
        Determines the precise statutory applicability of a provision at a specified date
        using inclusive boundary semantics [effective_from, effective_until] and savings clauses.
        Enforces:
        - Parent enactment commencement barrier (enacted/published != in force).
        - Explicit uncertainty for overlapping intervals without legislative resolution.
        - Unresolved conflicting gazette notifications.
        - Authoritative retrospective application (e.g. Vineeta Sharma).
        - Historical query availability after repeal.
        - Timezone/timestamp normalization preserving calendar day.
        \"\"\"
        if not query_date_str:
            return {
                "provision_id": provision_id,
                "query_date": None,
                "jurisdiction": jurisdiction,
                "applicability_state": StatutoryApplicabilityState.INSUFFICIENT_EVIDENCE,
                "applicable_version": None,
                "is_applicable": False,
                "savings_applied": False,
                "rationale": "No query date provided; temporal applicability cannot be definitively established.",
            }

        q_date = normalize_calendar_date(query_date_str)
        if not q_date:
            return {
                "provision_id": provision_id,
                "query_date": query_date_str,
                "jurisdiction": jurisdiction,
                "applicability_state": StatutoryApplicabilityState.CONFLICTING_TEMPORAL_EVIDENCE,
                "applicable_version": None,
                "is_applicable": False,
                "savings_applied": False,
                "rationale": f"Invalid ISO date format: '{query_date_str}'.",
            }

        versions = self._versions.get(provision_id, [])
        if not versions:
            return {
                "provision_id": provision_id,
                "query_date": query_date_str,
                "jurisdiction": jurisdiction,
                "applicability_state": StatutoryApplicabilityState.INSUFFICIENT_EVIDENCE,
                "applicable_version": None,
                "is_applicable": False,
                "savings_applied": False,
                "rationale": f"No temporal versions registered for provision ID '{provision_id}'.",
            }

        # Check parent statute lifecycle
        statute_id = versions[0].statute_id
        statute = self.get_statute(statute_id)

        # 1. Check if uncommenced / partially commenced statute
        if statute:
            if not statute.is_fully_commenced and not statute.commencement_date:
                return {
                    "provision_id": provision_id,
                    "statute_id": statute_id,
                    "query_date": query_date_str,
                    "jurisdiction": jurisdiction,
                    "applicability_state": StatutoryApplicabilityState.PARTIALLY_COMMENCED,
                    "applicable_version": None,
                    "is_applicable": False,
                    "savings_applied": False,
                    "rationale": f"Parent statute '{statute.title}' is uncommenced or subject to phased notification; provision not generally in force.",
                }
            if statute.commencement_date:
                s_cdate = normalize_calendar_date(statute.commencement_date)
                if s_cdate and q_date < s_cdate:
                    return {
                        "provision_id": provision_id,
                        "statute_id": statute_id,
                        "query_date": query_date_str,
                        "jurisdiction": jurisdiction,
                        "applicability_state": StatutoryApplicabilityState.NOT_YET_IN_FORCE,
                        "applicable_version": None,
                        "is_applicable": False,
                        "savings_applied": False,
                        "rationale": f"Parent statute '{statute.title}' had not yet commenced on {query_date_str} (appointed commencement date: {statute.commencement_date}). Promulgation or publication prior to appointed commencement date does not bring provisions into force.",
                    }

        # Check if provision versions have conflicting gazette notifications
        for v in versions:
            if v.conflicting_notifications:
                return {
                    "provision_id": provision_id,
                    "statute_id": statute_id,
                    "query_date": query_date_str,
                    "jurisdiction": jurisdiction,
                    "applicability_state": StatutoryApplicabilityState.CONFLICTING_TEMPORAL_EVIDENCE,
                    "applicable_version": None,
                    "is_applicable": False,
                    "savings_applied": False,
                    "conflicting_notifications": v.conflicting_notifications,
                    "rationale": f"Conflicting commencement notifications in Official Gazette ({v.conflicting_notifications}) create unresolved temporal ambiguity on {query_date_str}.",
                }

        # 2. Check each version
        # Find all versions operative on query_date
        matching_versions = []
        for v in versions:
            # Check commencement
            if v.commencement_date:
                c_date = normalize_calendar_date(v.commencement_date)
                if c_date and q_date < c_date:
                    continue
            elif v.is_phased_commencement:
                continue

            # Effective from [
            if v.version_effective_from:
                ef_date = normalize_calendar_date(v.version_effective_from)
                if ef_date and q_date < ef_date:
                    if not (v.is_retrospective and v.retrospective_basis):
                        continue

            # Effective until boundary check
            if v.version_effective_until:
                eu_date = normalize_calendar_date(v.version_effective_until)
                if eu_date and q_date > eu_date:
                    continue

            # Repeal check
            if v.repeal_date:
                r_date = normalize_calendar_date(v.repeal_date)
                if r_date and q_date >= r_date:
                    if pending_proceeding_commenced_prior and v.savings_applies_to_pending:
                        matching_versions.append((v, True))
                    continue

            matching_versions.append((v, False))

        if len(matching_versions) > 1:
            # Check for explicit retrospective resolution
            retro_versions = [v for v, sav in matching_versions if v.is_retrospective]
            if len(retro_versions) == 1:
                matched_version, savings_active = next((v, sav) for v, sav in matching_versions if v.is_retrospective)
            else:
                return {
                    "provision_id": provision_id,
                    "statute_id": statute_id,
                    "query_date": query_date_str,
                    "jurisdiction": jurisdiction,
                    "applicability_state": StatutoryApplicabilityState.CONFLICTING_TEMPORAL_EVIDENCE,
                    "applicable_version": None,
                    "is_applicable": False,
                    "savings_applied": False,
                    "matching_version_numbers": [v.version_number for v, _ in matching_versions],
                    "rationale": f"Multiple conflicting temporal versions ({[v.version_number for v, _ in matching_versions]}) are concurrently operative on {query_date_str} without verified legislative resolution.",
                }
        elif len(matching_versions) == 1:
            matched_version, savings_active = matching_versions[0]
        else:
            matched_version = None
            savings_active = False

        if matched_version:
            is_current = (matched_version.version_effective_until is None) and (matched_version.repeal_date is None)
            state = StatutoryApplicabilityState.CONFIRMED_APPLICABLE if is_current else StatutoryApplicabilityState.CONFIRMED_HISTORICAL
            
            if matched_version.repeal_date:
                r_date = normalize_calendar_date(matched_version.repeal_date)
                if r_date and q_date >= r_date and pending_proceeding_commenced_prior:
                    savings_active = True
                    state = StatutoryApplicabilityState.CONFIRMED_HISTORICAL

            ret_dict = {
                "provision_id": provision_id,
                "statute_id": statute_id,
                "query_date": query_date_str,
                "jurisdiction": jurisdiction,
                "applicability_state": state,
                "applicable_version": matched_version.to_dict(),
                "version_number": matched_version.version_number,
                "is_applicable": True,
                "savings_applied": savings_active,
                "rationale": f"Version {matched_version.version_number} was in force on {query_date_str} (effective from {matched_version.version_effective_from}).",
            }
            if matched_version.is_retrospective:
                ret_dict["is_retrospective"] = True
                ret_dict["retrospective_basis"] = matched_version.retrospective_basis
            return ret_dict

        # If not matched, determine why (not yet in force vs repealed/superseded)
        first_version = versions[0]
        earliest_str = first_version.commencement_date or first_version.version_effective_from
        if earliest_str:
            earliest_date = normalize_calendar_date(earliest_str)
            if earliest_date and q_date < earliest_date:
                return {
                    "provision_id": provision_id,
                    "statute_id": statute_id,
                    "query_date": query_date_str,
                    "jurisdiction": jurisdiction,
                    "applicability_state": StatutoryApplicabilityState.NOT_YET_IN_FORCE,
                    "applicable_version": None,
                    "is_applicable": False,
                    "savings_applied": False,
                    "rationale": f"Provision '{provision_id}' was not yet in force on {query_date_str} (earliest commencement: {earliest_str}).",
                }

        # Otherwise provision is superseded or repealed
        return {
            "provision_id": provision_id,
            "statute_id": statute_id,
            "query_date": query_date_str,
            "jurisdiction": jurisdiction,
            "applicability_state": StatutoryApplicabilityState.SUPERSEDED_OR_REPEALED,
            "applicable_version": None,
            "is_applicable": False,
            "savings_applied": False,
            "rationale": f"Provision '{provision_id}' has been repealed or superseded prior to query date {query_date_str}.",
        }"""

if old_resolve in content:
    content = content.replace(old_resolve, new_resolve)
    print("Replaced resolve_point_in_time_applicability")
else:
    print("WARNING: old_resolve not found directly, trying normalized newlines")
    content = content.replace(old_resolve.replace("\n", "\r\n"), new_resolve.replace("\n", "\r\n"))

# 3. Update HSA-SEC-6 version 2 in build_default_temporal_engine
old_hsa2 = """    # Version 2 (Post-2005 Amendment Act No. 39 of 2005)
    engine.register_provision_version(ProvisionTemporalVersion(
        provision_id="HSA-SEC-6",
        statute_id="IND-STAT-HSA-1956",
        section_number="6",
        version_number=2,
        text="6. Devolution of interest in coparcenary property.(1) On and from the commencement of the Hindu Succession (Amendment) Act, 2005, in a Joint Hindu family governed by the Mitakshara law, the daughter of a coparcener shall,(a) by birth become a coparcener in her own right the same manner as the son...",
        version_effective_from="2005-09-09",
        version_effective_until=None,
        amendment_act_id="HSA-AMEND-2005",
        temporal_status=TemporalStatus.ACTIVE,
    ))"""

new_hsa2 = """    # Version 2 (Post-2005 Amendment Act No. 39 of 2005)
    engine.register_provision_version(ProvisionTemporalVersion(
        provision_id="HSA-SEC-6",
        statute_id="IND-STAT-HSA-1956",
        section_number="6",
        version_number=2,
        text="6. Devolution of interest in coparcenary property.(1) On and from the commencement of the Hindu Succession (Amendment) Act, 2005, in a Joint Hindu family governed by the Mitakshara law, the daughter of a coparcener shall,(a) by birth become a coparcener in her own right the same manner as the son...",
        version_effective_from="2005-09-09",
        version_effective_until=None,
        amendment_act_id="HSA-AMEND-2005",
        temporal_status=TemporalStatus.ACTIVE,
        is_retrospective=True,
        retrospective_basis="Supreme Court of India in Vineeta Sharma v. Rakesh Sharma (2020) 9 SCC 1 held that rights under amended Section 6 apply retroactively to daughters living on or after 2005-09-09 irrespective of date of birth or survival of coparcener father.",
    ))"""

if old_hsa2 in content:
    content = content.replace(old_hsa2, new_hsa2)
    print("Replaced HSA-SEC-6 version 2")
else:
    content = content.replace(old_hsa2.replace("\n", "\r\n"), new_hsa2.replace("\n", "\r\n"))

file_path.write_text(content, encoding="utf-8")
print("Saved patched legalmitra/temporal/engine.py")

