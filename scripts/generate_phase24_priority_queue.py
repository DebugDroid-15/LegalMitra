"""
Script: scripts/generate_phase24_priority_queue.py
Builds the Phase 24 National Acquisition Priority Queue across all 14 practical legal domains.
Outputs:
- data/09_national_corpus/phase24_acquisition_queue.json
"""

import json
from pathlib import Path
from typing import Any, Dict, List

from legalmitra.corpus.acquisition_queue import (
    AcquisitionPriorityScorer,
    AcquisitionTask,
    PriorityAcquisitionQueue,
    TaskStatus,
)
from legalmitra.corpus.legal_universe import DocumentFamily, LegalAuthorityLevel


def build_phase24_queue() -> List[Dict[str, Any]]:
    output_path = Path("data/09_national_corpus/phase24_acquisition_queue.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    candidates = [
        # 1. Police procedure, FIRs, and criminal procedure
        {
            "task_id": "ACQ-BNS-COMPLETION",
            "record_id": "IND-ACT-2023-BNS-EXP",
            "official_title": "The Bharatiya Nyaya Sanhita, 2023 (Act No. 45 of 2023) - Core Penal Provisions",
            "document_family": DocumentFamily.CENTRAL_ACT,
            "authority_level": LegalAuthorityLevel.BINDING_CENTRAL_STATUTE,
            "jurisdiction": "IN",
            "source_url": "https://www.indiacode.nic.in/handle/123456789/20062",
            "legal_domain": "Police procedure, FIRs, and criminal procedure",
            "is_coverage_gap": True,
            "chunks_indexed": 28,
        },
        {
            "task_id": "ACQ-BSA-COMPLETION",
            "record_id": "IND-ACT-2023-BSA-EXP",
            "official_title": "The Bharatiya Sakshya Adhiniyam, 2023 (Act No. 47 of 2023) - Evidence Provisions",
            "document_family": DocumentFamily.CENTRAL_ACT,
            "authority_level": LegalAuthorityLevel.BINDING_CENTRAL_STATUTE,
            "jurisdiction": "IN",
            "source_url": "https://www.indiacode.nic.in/handle/123456789/20064",
            "legal_domain": "Police procedure, FIRs, and criminal procedure",
            "is_coverage_gap": True,
            "chunks_indexed": 6,
        },
        # 2. Women's rights and protective legislation
        {
            "task_id": "ACQ-POCSO-COMPLETION",
            "record_id": "IND-ACT-2012-POCSO-EXP",
            "official_title": "Protection of Children from Sexual Offences Act, 2012 (Act No. 32 of 2012)",
            "document_family": DocumentFamily.CENTRAL_ACT,
            "authority_level": LegalAuthorityLevel.BINDING_CENTRAL_STATUTE,
            "jurisdiction": "IN",
            "source_url": "https://www.indiacode.nic.in/handle/123456789/2079",
            "legal_domain": "Women's rights and protective legislation",
            "is_coverage_gap": True,
            "chunks_indexed": 4,
        },
        # 3. Right to Information
        {
            "task_id": "ACQ-RTI-FOUNDATIONAL",
            "record_id": "IND-ACT-2005-RTI",
            "official_title": "The Right to Information Act, 2005 (Act No. 22 of 2005)",
            "document_family": DocumentFamily.CENTRAL_ACT,
            "authority_level": LegalAuthorityLevel.BINDING_CENTRAL_STATUTE,
            "jurisdiction": "IN",
            "source_url": "https://www.indiacode.nic.in/handle/123456789/2065",
            "legal_domain": "Right to Information",
            "is_coverage_gap": True,
            "chunks_indexed": 0,
        },
        # 4. Traffic and motor vehicle law
        {
            "task_id": "ACQ-MV-FOUNDATIONAL",
            "record_id": "IND-ACT-1988-MVA-EXP",
            "official_title": "The Motor Vehicles Act, 1988 (as amended by MV Amendment Act 2019)",
            "document_family": DocumentFamily.CENTRAL_ACT,
            "authority_level": LegalAuthorityLevel.BINDING_CENTRAL_STATUTE,
            "jurisdiction": "IN",
            "source_url": "https://www.indiacode.nic.in/handle/123456789/1798",
            "legal_domain": "Traffic and motor vehicle law",
            "is_coverage_gap": True,
            "chunks_indexed": 0,
        },
        # 5. Constitutional rights and remedies (Landmark Judgments)
        {
            "task_id": "ACQ-JUD-MANEKA-GANDHI",
            "record_id": "IND-JUD-SC-1978-MANEKA",
            "official_title": "Maneka Gandhi v. Union of India (1978) 1 SCC 248 [Article 21 Due Process]",
            "document_family": DocumentFamily.JUDGMENT_SUPREME_COURT,
            "authority_level": LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141,
            "jurisdiction": "IN",
            "source_url": "https://main.sci.gov.in/judgment/judis/1978_1_SCC_248.pdf",
            "legal_domain": "Constitutional rights and remedies",
            "is_coverage_gap": True,
            "chunks_indexed": 0,
        },
        {
            "task_id": "ACQ-JUD-KESAVANANDA",
            "record_id": "IND-JUD-SC-1973-KESAVANANDA",
            "official_title": "Kesavananda Bharati v. State of Kerala (1973) 4 SCC 225 [Basic Structure]",
            "document_family": DocumentFamily.JUDGMENT_SUPREME_COURT,
            "authority_level": LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141,
            "jurisdiction": "IN",
            "source_url": "https://main.sci.gov.in/judgment/judis/1973_4_SCC_225.pdf",
            "legal_domain": "Constitutional rights and remedies",
            "is_coverage_gap": True,
            "chunks_indexed": 0,
        },
        {
            "task_id": "ACQ-JUD-DK-BASU",
            "record_id": "IND-JUD-SC-1997-DKBASU",
            "official_title": "D.K. Basu v. State of West Bengal (1997) 1 SCC 416 [Arrest Guidelines]",
            "document_family": DocumentFamily.JUDGMENT_SUPREME_COURT,
            "authority_level": LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141,
            "jurisdiction": "IN",
            "source_url": "https://main.sci.gov.in/judgment/judis/1997_1_SCC_416.pdf",
            "legal_domain": "Police procedure, FIRs, and criminal procedure",
            "is_coverage_gap": True,
            "chunks_indexed": 0,
        },
        {
            "task_id": "ACQ-JUD-LALITA-KUMARI",
            "record_id": "IND-JUD-SC-2014-LALITA",
            "official_title": "Lalita Kumari v. Govt. of U.P. (2014) 2 SCC 1 [Mandatory FIR Registration]",
            "document_family": DocumentFamily.JUDGMENT_SUPREME_COURT,
            "authority_level": LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141,
            "jurisdiction": "IN",
            "source_url": "https://main.sci.gov.in/judgment/judis/2014_2_SCC_1.pdf",
            "legal_domain": "Police procedure, FIRs, and criminal procedure",
            "is_coverage_gap": True,
            "chunks_indexed": 0,
        },
        {
            "task_id": "ACQ-JUD-ARNESH-KUMAR",
            "record_id": "IND-JUD-SC-2014-ARNESH",
            "official_title": "Arnesh Kumar v. State of Bihar (2014) 8 SCC 273 [Arrest Regulation up to 7 Yrs]",
            "document_family": DocumentFamily.JUDGMENT_SUPREME_COURT,
            "authority_level": LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141,
            "jurisdiction": "IN",
            "source_url": "https://main.sci.gov.in/judgment/judis/2014_8_SCC_273.pdf",
            "legal_domain": "Police procedure, FIRs, and criminal procedure",
            "is_coverage_gap": True,
            "chunks_indexed": 0,
        },
        {
            "task_id": "ACQ-JUD-SHREYA-SINGHAL",
            "record_id": "IND-JUD-SC-2015-SHREYA",
            "official_title": "Shreya Singhal v. Union of India (2015) 5 SCC 1 [Section 66A IT Act Struck Down]",
            "document_family": DocumentFamily.JUDGMENT_SUPREME_COURT,
            "authority_level": LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141,
            "jurisdiction": "IN",
            "source_url": "https://main.sci.gov.in/judgment/judis/2015_5_SCC_1.pdf",
            "legal_domain": "Cybercrime and online fraud",
            "is_coverage_gap": True,
            "chunks_indexed": 0,
        },
        # 6. Consumer protection
        {
            "task_id": "ACQ-JUD-JACOB-MATHEW",
            "record_id": "IND-JUD-SC-2005-JACOB",
            "official_title": "Jacob Mathew v. State of Punjab (2005) 6 SCC 1 [Medical Negligence Bolam Test]",
            "document_family": DocumentFamily.JUDGMENT_SUPREME_COURT,
            "authority_level": LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141,
            "jurisdiction": "IN",
            "source_url": "https://main.sci.gov.in/judgment/judis/2005_6_SCC_1.pdf",
            "legal_domain": "Consumer protection",
            "is_coverage_gap": True,
            "chunks_indexed": 0,
        },
        # 7. Arbitration and dispute resolution
        {
            "task_id": "ACQ-JUD-VIDYA-DROLIA",
            "record_id": "IND-JUD-SC-2021-VIDYA",
            "official_title": "Vidya Drolia v. Durga Trading Corporation (2021) 2 SCC 1 [Arbitrability & Tenancy]",
            "document_family": DocumentFamily.JUDGMENT_SUPREME_COURT,
            "authority_level": LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141,
            "jurisdiction": "IN",
            "source_url": "https://main.sci.gov.in/judgment/judis/2021_2_SCC_1.pdf",
            "legal_domain": "Arbitration and dispute resolution",
            "is_coverage_gap": True,
            "chunks_indexed": 0,
        },
        # 8. Property, rental, and tenancy
        {
            "task_id": "ACQ-JUD-SURAJ-LAMP",
            "record_id": "IND-JUD-SC-2012-SURAJ",
            "official_title": "Suraj Lamp & Industries v. State of Haryana (2012) 1 SCC 656 [GPA / SA Invalidation]",
            "document_family": DocumentFamily.JUDGMENT_SUPREME_COURT,
            "authority_level": LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141,
            "jurisdiction": "IN",
            "source_url": "https://main.sci.gov.in/judgment/judis/2012_1_SCC_656.pdf",
            "legal_domain": "Property, rental, and tenancy",
            "is_coverage_gap": True,
            "chunks_indexed": 0,
        },
        # 9. Contract and commercial law
        {
            "task_id": "ACQ-JUD-ENERGY-WATCHDOG",
            "record_id": "IND-JUD-SC-2017-ENERGY",
            "official_title": "Energy Watchdog v. CERC (2017) 14 SCC 80 [Force Majeure & Frustration]",
            "document_family": DocumentFamily.JUDGMENT_SUPREME_COURT,
            "authority_level": LegalAuthorityLevel.BINDING_SUPREME_COURT_ART141,
            "jurisdiction": "IN",
            "source_url": "https://main.sci.gov.in/judgment/judis/2017_14_SCC_80.pdf",
            "legal_domain": "Contract and commercial law",
            "is_coverage_gap": True,
            "chunks_indexed": 0,
        },
    ]

    queue = PriorityAcquisitionQueue()
    scored_tasks = []

    for c in candidates:
        score, rationale = AcquisitionPriorityScorer.calculate_priority(
            authority_level=c["authority_level"],
            legal_domain=c["legal_domain"],
            is_coverage_gap=c["is_coverage_gap"],
            chunks_indexed=c["chunks_indexed"],
        )
        task = AcquisitionTask(
            task_id=c["task_id"],
            record_id=c["record_id"],
            official_title=c["official_title"],
            document_family=c["document_family"],
            authority_level=c["authority_level"],
            jurisdiction=c["jurisdiction"],
            source_url=c["source_url"],
            priority_score=score,
            priority_rationale=rationale,
            metadata={"domain": c["legal_domain"], "gap_size": "high" if c["chunks_indexed"] < 10 else "medium"},
        )
        queue.enqueue(task)
        scored_tasks.append(task.to_dict())

    # Sort descending by priority score
    scored_tasks.sort(key=lambda x: x["priority_score"], reverse=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(scored_tasks, f, indent=2, ensure_ascii=False)

    print(f"[OK] Generated Phase 24 Acquisition Priority Queue ({len(scored_tasks)} items) at {output_path}")
    for idx, t in enumerate(scored_tasks[:10], 1):
        print(f"  {idx}. [{t['priority_score']:.1f}] {t['official_title']} ({t['metadata']['domain']})")

    return scored_tasks


if __name__ == "__main__":
    build_phase24_queue()
