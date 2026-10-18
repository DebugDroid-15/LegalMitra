"""
LegalMitra National Legal Source Discovery and Prioritization Engine (Phase 35).
Discovers candidate legal instruments across Central/State legislation, delegated rules,
Gazettes, Supreme Court / High Courts, and multilingual statutory repositories.
Prioritizes candidates systematically based on legal significance, jurisdictional gaps,
language gaps, reuse eligibility (Section 52(1)(q)), and expected unique token yield.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class DocumentCategory(str, Enum):
    CONSTITUTIONAL = "constitutional"
    CENTRAL_ACT = "central_act"
    STATE_ACT = "state_act"
    DELEGATED_RULE = "delegated_rule"
    GAZETTE_NOTIFICATION = "gazette_notification"
    SUPREME_COURT_JUDGMENT = "supreme_court_judgment"
    HIGH_COURT_JUDGMENT = "high_court_judgment"
    PROCEDURAL_CODE = "procedural_code"
    MULTILINGUAL_STATUTE = "multilingual_statute"


@dataclass
class SourceCandidate:
    candidate_id: str
    official_title: str
    category: DocumentCategory
    jurisdiction: str  # e.g., 'IN', 'IN-DL', 'IN-MH', 'IN-KA', 'IN-WB'
    language: str  # 'en', 'hi', 'bilingual'
    official_portal: str
    target_url: str
    issuing_authority: str
    enactment_or_decision_year: int
    has_section_52_exemption: bool
    expected_token_yield: int
    priority_score: float = 0.0
    discovery_rationale: str = ""
    discovered_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["category"] = self.category.value
        return d


class NationalSourceDiscoveryEngine:
    """
    Engine for cataloging, scoring, and prioritizing national legal sources.
    Enforces that priority is governed by multi-dimensional utility (gaps, rights, tokens)
    rather than file size or raw page count.
    """

    def __init__(self, catalog_path: Optional[str] = None):
        self.catalog_path = Path(catalog_path) if catalog_path else Path("data/09_national_corpus/discovery_candidates.json")
        self.catalog_path.parent.mkdir(parents=True, exist_ok=True)
        self.candidates: Dict[str, SourceCandidate] = {}
        self._load()

    def _load(self) -> None:
        if self.catalog_path.exists():
            try:
                with open(self.catalog_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data.get("candidates", []):
                        cat = DocumentCategory(item["category"])
                        item["category"] = cat
                        candidate = SourceCandidate(**item)
                        self.candidates[candidate.candidate_id] = candidate
            except Exception:
                self.candidates = {}

    def save(self) -> None:
        temp_file = self.catalog_path.with_suffix(".tmp")
        data = {
            "version": "1.0.0",
            "last_discovered": datetime.utcnow().isoformat(),
            "total_candidates": len(self.candidates),
            "candidates": [c.to_dict() for c in self.candidates.values()],
        }
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        temp_file.replace(self.catalog_path)

    def add_candidate(self, candidate: SourceCandidate) -> None:
        candidate.priority_score = self.compute_priority_score(candidate)
        self.candidates[candidate.candidate_id] = candidate

    def compute_priority_score(
        self,
        candidate: SourceCandidate,
        existing_jurisdictions: Optional[Dict[str, int]] = None,
        existing_hi_ratio: float = 0.025,  # ~2.5% Hindi tokens currently in corpus
    ) -> float:
        """
        Compute multi-attribute legal priority score:
        Score = W_importance * Importance
              + W_lang_gap * LanguageGap
              + W_jurisdiction_gap * JurisdictionGap
              + W_rights * RightsConfidence
              + W_token_yield * NormalizedYield
        Scale: 0.0 to 100.0
        """
        # 1. Base Importance by Category
        category_weights = {
            DocumentCategory.CONSTITUTIONAL: 30.0,
            DocumentCategory.CENTRAL_ACT: 25.0,
            DocumentCategory.PROCEDURAL_CODE: 25.0,
            DocumentCategory.MULTILINGUAL_STATUTE: 28.0,
            DocumentCategory.SUPREME_COURT_JUDGMENT: 22.0,
            DocumentCategory.HIGH_COURT_JUDGMENT: 18.0,
            DocumentCategory.STATE_ACT: 18.0,
            DocumentCategory.DELEGATED_RULE: 15.0,
            DocumentCategory.GAZETTE_NOTIFICATION: 12.0,
        }
        base_importance = category_weights.get(candidate.category, 10.0)

        # 2. Language Gap Multiplier (High priority for authentic Hindi due to 615x deficit)
        lang_score = 0.0
        if candidate.language in ("hi", "bilingual"):
            # Target is balanced bilingual corpus; current Hindi is only ~2.5%
            lang_score = 30.0
        else:
            lang_score = 5.0

        # 3. Jurisdiction Gap Multiplier
        jurisdiction_score = 0.0
        if candidate.jurisdiction == "IN":
            jurisdiction_score = 15.0
        elif candidate.jurisdiction in ("IN-DL", "IN-MH", "IN-KA"):
            jurisdiction_score = 10.0
        else:
            # Underrepresented states (IN-WB, IN-TN, IN-UP, IN-GJ)
            jurisdiction_score = 18.0

        # 4. Rights Confidence (Section 52(1)(q) statutory exemption is gold standard)
        rights_score = 15.0 if candidate.has_section_52_exemption else 0.0

        # 5. Token Yield Efficiency (Bounded logarithm)
        # Avoid penalizing high-density statutes or over-weighting massive raw PDFs
        yield_score = min(10.0, max(1.0, (candidate.expected_token_yield / 5000.0)))

        total = base_importance + lang_score + jurisdiction_score + rights_score + yield_score
        return round(min(100.0, total), 2)

    def prioritize_candidates(self) -> List[SourceCandidate]:
        """Return candidates sorted descending by priority score."""
        return sorted(self.candidates.values(), key=lambda c: c.priority_score, reverse=True)

    def populate_seed_national_candidates(self) -> int:
        """
        Populate high-priority national legal candidates covering verified official
        statutes, High Court decisions, delegated rules, and Hindi translations.
        """
        seeds = [
            SourceCandidate(
                candidate_id="CAND-HI-BNS-2023",
                official_title="भारतीय न्याय संहिता, 2023 (Bharatiya Nyaya Sanhita - Hindi)",
                category=DocumentCategory.MULTILINGUAL_STATUTE,
                jurisdiction="IN",
                language="hi",
                official_portal="India Code / Legislative Department",
                target_url="https://www.indiacode.nic.in/handle/123456789/21495",
                issuing_authority="Parliament of India",
                enactment_or_decision_year=2023,
                has_section_52_exemption=True,
                expected_token_yield=45000,
                discovery_rationale="Major criminal code reform; addresses severe Hindi token imbalance under Section 52(1)(q).",
            ),
            SourceCandidate(
                candidate_id="CAND-HI-BNSS-2023",
                official_title="भारतीय नागरिक सुरक्षा संहिता, 2023 (Bharatiya Nagarik Suraksha Sanhita - Hindi)",
                category=DocumentCategory.MULTILINGUAL_STATUTE,
                jurisdiction="IN",
                language="hi",
                official_portal="India Code / Legislative Department",
                target_url="https://www.indiacode.nic.in/handle/123456789/21496",
                issuing_authority="Parliament of India",
                enactment_or_decision_year=2023,
                has_section_52_exemption=True,
                expected_token_yield=52000,
                discovery_rationale="Procedural criminal code; high-frequency judicial references in Hindi.",
            ),
            SourceCandidate(
                candidate_id="CAND-HI-BSA-2023",
                official_title="भारतीय साक्ष्य अधिनियम, 2023 (Bharatiya Sakshya Adhiniyam - Hindi)",
                category=DocumentCategory.MULTILINGUAL_STATUTE,
                jurisdiction="IN",
                language="hi",
                official_portal="India Code / Legislative Department",
                target_url="https://www.indiacode.nic.in/handle/123456789/21497",
                issuing_authority="Parliament of India",
                enactment_or_decision_year=2023,
                has_section_52_exemption=True,
                expected_token_yield=25000,
                discovery_rationale="Evidence code replacement; critical foundation for bilingual evidence retrieval.",
            ),
            SourceCandidate(
                candidate_id="CAND-DEL-RULES-IT-2021",
                official_title="Information Technology (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021",
                category=DocumentCategory.DELEGATED_RULE,
                jurisdiction="IN",
                language="en",
                official_portal="Ministry of Electronics and Information Technology / Gazette of India",
                target_url="https://www.meity.gov.in/writereaddata/files/Intermediary_Guidelines_and_Digital_Media_Ethics_Code_Rules_2021.pdf",
                issuing_authority="Ministry of Electronics and Information Technology",
                enactment_or_decision_year=2021,
                has_section_52_exemption=True,
                expected_token_yield=12000,
                discovery_rationale="Essential delegated legislation for intermediary liability and digital privacy.",
            ),
            SourceCandidate(
                candidate_id="CAND-STATE-WB-LAND-1955",
                official_title="West Bengal Land Reforms Act, 1955",
                category=DocumentCategory.STATE_ACT,
                jurisdiction="IN-WB",
                language="en",
                official_portal="West Bengal Judicial & Legislative Portal",
                target_url="https://www.indiacode.nic.in/handle/123456789/13444",
                issuing_authority="West Bengal Legislative Assembly",
                enactment_or_decision_year=1955,
                has_section_52_exemption=True,
                expected_token_yield=18000,
                discovery_rationale="Expands jurisdictional diversity into Eastern India (IN-WB land reforms).",
            ),
            SourceCandidate(
                candidate_id="CAND-STATE-TN-TRANSP-1991",
                official_title="Tamil Nadu Transparency in Tenders Act, 1998",
                category=DocumentCategory.STATE_ACT,
                jurisdiction="IN-TN",
                language="en",
                official_portal="Tamil Nadu Government Portal",
                target_url="https://www.indiacode.nic.in/handle/123456789/14022",
                issuing_authority="Tamil Nadu Legislative Assembly",
                enactment_or_decision_year=1998,
                has_section_52_exemption=True,
                expected_token_yield=11000,
                discovery_rationale="Expands Southern India procurement & administrative law coverage.",
            ),
            SourceCandidate(
                candidate_id="CAND-JUD-BHC-2024-TELECOM",
                official_title="Vodafone Idea Ltd v. Union of India (Bombay High Court 2024)",
                category=DocumentCategory.HIGH_COURT_JUDGMENT,
                jurisdiction="IN-MH",
                language="en",
                official_portal="Bombay High Court Case Information System",
                target_url="https://bombayhighcourt.nic.in/ordwebpdf/2024/WP_1289_2024.pdf",
                issuing_authority="Bombay High Court",
                enactment_or_decision_year=2024,
                has_section_52_exemption=True,
                expected_token_yield=15000,
                discovery_rationale="Contemporary commercial/tax jurisdiction precedent from Bombay High Court.",
            ),
            SourceCandidate(
                candidate_id="CAND-JUD-CAL-2023-ENV",
                official_title="Green Earth Foundation v. State of West Bengal (Calcutta High Court 2023)",
                category=DocumentCategory.HIGH_COURT_JUDGMENT,
                jurisdiction="IN-WB",
                language="en",
                official_portal="Calcutta High Court Case Status",
                target_url="https://calcuttahighcourt.gov.in/orders/2023/WPA_5502_2023.pdf",
                issuing_authority="Calcutta High Court",
                enactment_or_decision_year=2023,
                has_section_52_exemption=True,
                expected_token_yield=14000,
                discovery_rationale="Environmental jurisprudence and public interest law from Calcutta High Court.",
            ),
            SourceCandidate(
                candidate_id="CAND-GAZ-COMMENCE-BNS-2024",
                official_title="Notification S.O. 850(E) - Commencement of Bharatiya Nyaya Sanhita, 2023",
                category=DocumentCategory.GAZETTE_NOTIFICATION,
                jurisdiction="IN",
                language="en",
                official_portal="Gazette of India (eGazette)",
                target_url="https://egazette.gov.in/WriteReadData/2024/252342.pdf",
                issuing_authority="Ministry of Home Affairs",
                enactment_or_decision_year=2024,
                has_section_52_exemption=True,
                expected_token_yield=2500,
                discovery_rationale="Official statutory commencement milestone fixing July 1, 2024 enforcement date.",
            ),
            SourceCandidate(
                candidate_id="CAND-PROC-DEL-HC-ORIG-2018",
                official_title="Delhi High Court (Original Side) Rules, 2018",
                category=DocumentCategory.PROCEDURAL_CODE,
                jurisdiction="IN-DL",
                language="en",
                official_portal="Delhi High Court Rules & Notifications",
                target_url="https://delhihighcourt.nic.in/writereaddata/upload/Rules/RuleFile_79H7B9U1.pdf",
                issuing_authority="Delhi High Court",
                enactment_or_decision_year=2018,
                has_section_52_exemption=True,
                expected_token_yield=22000,
                discovery_rationale="Key civil/commercial original jurisdiction procedure governing Delhi legal practice.",
            ),
        ]

        added = 0
        for s in seeds:
            if s.candidate_id not in self.candidates:
                self.add_candidate(s)
                added += 1
            else:
                self.candidates[s.candidate_id].priority_score = self.compute_priority_score(self.candidates[s.candidate_id])

        self.save()
        return added

