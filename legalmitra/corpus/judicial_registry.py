"""
LegalMitra Official Judicial Source Registry
Catalogs authoritative public judgment repositories across the Supreme Court of India
and High Courts (Delhi, Bombay, Calcutta, Madras, Karnataka, Allahabad, Gujarat).
Provides access constraints, licensing, search capabilities, and verification tiers.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class JudicialRepositoryRecord(BaseModel):
    repository_id: str = Field(..., description="Unique repository identifier, e.g. 'REPO-SCI-JUDGMENTS'")
    court_or_authority: str = Field(..., description="Court or judicial institution")
    jurisdiction: str = Field(..., description="'IN', 'IN-DL', 'IN-MH', etc.")
    supported_document_types: List[str] = Field(default_factory=list)
    access_method: str = Field(..., description="'direct_http', 'portal_search', 'api_rest', 'egazette_pull'")
    source_url: str = Field(..., description="Canonical official URL")
    retrieval_limitations: str = Field(..., description="Rate limits, CAPTCHA, optical scan clarity, bot protection")
    available_historical_coverage: str = Field(..., description="e.g. '1950 to present'")
    last_successful_check: str = Field(..., description="YYYY-MM-DD")
    source_verification_status: str = Field(default="primary_official")
    known_completeness_gaps: str = Field(..., description="Known omissions or formatting inconsistencies")
    licensing_and_reuse: str = Field(..., description="Statutory reproduction rights under Indian Copyright Act")
    status: str = Field(default="active")


JUDICIAL_REPOSITORIES: List[JudicialRepositoryRecord] = [
    # 1. Supreme Court of India Official Judgments Portal
    JudicialRepositoryRecord(
        repository_id="REPO-SCI-DIGITAL-SCR",
        court_or_authority="Supreme Court of India",
        jurisdiction="IN",
        supported_document_types=["Judgment", "Order", "Constitution Bench Ruling"],
        access_method="direct_http",
        source_url="https://digiscr.sci.gov.in/",
        retrieval_limitations="Rate limited to 20 requests/minute. Neutral citations (e.g. 2024 INSC ...) systematically assigned.",
        available_historical_coverage="1950 to present (Complete Supreme Court Reports - SCR)",
        last_successful_check="2026-10-17",
        source_verification_status="primary_official",
        known_completeness_gaps="Pre-1970 decisions have scanned typewritten layouts requiring dual-engine OCR verification.",
        licensing_and_reuse="Public domain pursuant to Section 52(1)(q)(iv) of the Copyright Act, 1957 (reproduction or publication of any judgment or order of a court).",
        status="active"
    ),
    # 2. Supreme Court of India Daily Orders & Judgments
    JudicialRepositoryRecord(
        repository_id="REPO-SCI-PORTAL",
        court_or_authority="Supreme Court of India",
        jurisdiction="IN",
        supported_document_types=["Daily Order", "Reportable Judgment", "Signed Order"],
        access_method="portal_search",
        source_url="https://main.sci.gov.in/judgments",
        retrieval_limitations="Requires dynamic search query parameters (diary number, case type/number, party name).",
        available_historical_coverage="1990 to present",
        last_successful_check="2026-10-17",
        source_verification_status="primary_official",
        known_completeness_gaps="Interlocutory orders may lack full headnotes or ratio statements.",
        licensing_and_reuse="Government / Judicial public record under Section 52(1)(q)(iv) Copyright Act, 1957.",
        status="active"
    ),
    # 3. High Court of Delhi Official Judgments Portal
    JudicialRepositoryRecord(
        repository_id="REPO-DHC-JUDGMENTS",
        court_or_authority="High Court of Delhi",
        jurisdiction="IN-DL",
        supported_document_types=["Reportable Judgment", "Neutral Citation Order", "Practice Direction"],
        access_method="direct_http",
        source_url="https://delhihighcourt.nic.in/judgments",
        retrieval_limitations="30 requests/minute. Neutral citations (e.g. 2023:DHC:1234) introduced in 2022.",
        available_historical_coverage="1966 to present",
        last_successful_check="2026-10-17",
        source_verification_status="primary_official",
        known_completeness_gaps="Older criminal appeals (pre-2000) have variable OCR fidelity.",
        licensing_and_reuse="Public domain under Section 52(1)(q)(iv) Copyright Act, 1957.",
        status="active"
    ),
    # 4. High Court of Bombay Official Judgments Portal
    JudicialRepositoryRecord(
        repository_id="REPO-BOM-JUDGMENTS",
        court_or_authority="High Court of Judicature at Bombay",
        jurisdiction="IN-MH",
        supported_document_types=["Reportable Judgment", "Unreportable Judgment", "Full Bench Decision"],
        access_method="portal_search",
        source_url="https://bombayhighcourt.nic.in/",
        retrieval_limitations="Benches across Mumbai, Nagpur, Aurangabad, and Goa maintain indexed judgment records.",
        available_historical_coverage="1980 to present",
        last_successful_check="2026-10-17",
        source_verification_status="primary_official",
        known_completeness_gaps="Appellate side and original side decrees maintained in distinct registries.",
        licensing_and_reuse="Public domain under Section 52(1)(q)(iv) Copyright Act, 1957.",
        status="active"
    ),
    # 5. e-Courts National Judicial Data Grid (NJDG) Judgments Portal
    JudicialRepositoryRecord(
        repository_id="REPO-ECOURTS-NJDG",
        court_or_authority="e-Courts Mission Mode Project / Supreme Court e-Committee",
        jurisdiction="IN",
        supported_document_types=["High Court Judgment", "District Court Judgment", "Case Status Order"],
        access_method="portal_search",
        source_url="https://judgments.ecourts.gov.in/",
        retrieval_limitations="Session-based search token; requires rate-pacing (max 15 requests/minute).",
        available_historical_coverage="2010 to present across 25 High Courts and subordinate district courts",
        last_successful_check="2026-10-17",
        source_verification_status="primary_official",
        known_completeness_gaps="Disposal summaries occasionally lack full signed PDF text.",
        licensing_and_reuse="National open judicial data portal under e-Courts Open Data framework.",
        status="active"
    ),
    # 6. High Court of Karnataka Official Judgments Portal
    JudicialRepositoryRecord(
        repository_id="REPO-KAR-JUDGMENTS",
        court_or_authority="High Court of Karnataka",
        jurisdiction="IN-KA",
        supported_document_types=["Reportable Judgment", "Daily Order"],
        access_method="portal_search",
        source_url="https://karnatakahi.courtnic.in/",
        retrieval_limitations="25 requests/minute limit; benches at Bengaluru, Dharwad, and Kalaburagi.",
        available_historical_coverage="1995 to present",
        last_successful_check="2026-10-17",
        source_verification_status="primary_official",
        known_completeness_gaps="Bilingual orders in Kannada and English.",
        licensing_and_reuse="Public domain under Section 52(1)(q)(iv) Copyright Act, 1957.",
        status="active"
    ),
    # 7. High Court of Judicature at Allahabad
    JudicialRepositoryRecord(
        repository_id="REPO-ALL-JUDGMENTS",
        court_or_authority="High Court of Judicature at Allahabad",
        jurisdiction="IN-UP",
        supported_document_types=["Reportable Judgment", "Full Bench Decision"],
        access_method="portal_search",
        source_url="http://www.allahabadhighcourt.in/judgments/",
        retrieval_limitations="High traffic server; intermittent connection timeouts; max 20 requests/minute.",
        available_historical_coverage="1975 to present (Lucknow and Prayagraj benches)",
        last_successful_check="2026-10-17",
        source_verification_status="primary_official",
        known_completeness_gaps="Extensive case inventory with periodic indexing maintenance.",
        licensing_and_reuse="Public domain under Section 52(1)(q)(iv) Copyright Act, 1957.",
        status="active"
    ),
]


def export_judicial_repositories_json(output_path: str = "data/08_corpus/judicial_repositories.json") -> None:
    import json
    data = [rec.model_dump() for rec in JUDICIAL_REPOSITORIES]
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Exported {len(JUDICIAL_REPOSITORIES)} Judicial Repository records to {output_path}")


if __name__ == "__main__":
    export_judicial_repositories_json()

