"""
Batch 0 Workflow Validation Script
Tests schema validation, provenance checks, duplicate detection, export,
review import, rollback, and audit logging on a small 3-example validation batch.
Operates strictly in data/07_batches/batch_00_validation without modifying the frozen pilot.
"""

import csv
import json
from datetime import date
from pathlib import Path

from legalmitra.core.enums import (
    LawStatusLabel,
    LegalReviewStatus,
    ProvisionCommencementStatus,
    TemporalValidationStatus,
)
from legalmitra.review.import_review import ReviewImporter, ReviewImportError
from legalmitra.schemas.legal_qa import EvidencePassage, LegalQADocument
from legalmitra.validation.quality_gate import DataQualityGate


def run_batch_00_validation() -> bool:
    print("=== Running Batch 0 Workflow Validation ===")
    out_dir = Path("data/07_batches/batch_00_validation")
    out_dir.mkdir(parents=True, exist_ok=True)
    batch_file = out_dir / "batch_00_examples.jsonl"
    csv_file = out_dir / "batch_00_review_sheet.csv"

    # 1. Create 3 validation candidates
    examples = [
        LegalQADocument(
            qa_id="QA-BATCH0-001",
            question="Under the enacted statutory text of Section 8(6) of the Digital Personal Data Protection Act, 2023 (scheduled to commence on 13 May 2027 under G.S.R. 843(E)), who must be notified by the Data Fiduciary in the event of a personal data breach?",
            answer="Under Section 8(6) of the Digital Personal Data Protection Act, 2023 (enacted and appointed to commence on 13 May 2027 under Notification G.S.R. 843(E), hence uncommenced as of 16 October 2026), in the event of a personal data breach, the Data Fiduciary shall give intimation of such breach to both the Data Protection Board of India and each affected Data Principal, in such form and manner as may be prescribed.",
            supporting_source_ids=["IND-STAT-DPDP-2023"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-DPDP-2023",
                    section_or_para_ref="Section 8(6)",
                    verbatim_text="(6) In the event of a personal data breach, the Data Fiduciary shall give the Board and each affected Data Principal, intimation of such breach in such form and manner as may be prescribed.",
                )
            ],
            legal_domain="Data Protection",
            statutory_citations=["Section 8(6), Digital Personal Data Protection Act, 2023"],
            legal_as_of_date=date(2026, 10, 16),
            commencement_source_id="IND-NOTIF-MEITY-GSR-843E-2025",
            commencement_date=date(2027, 5, 13),
            law_status_label=LawStatusLabel.ENACTED_NOT_YET_IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.UNCOMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_FUTURE_COMMENCEMENT,
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
        ),
        LegalQADocument(
            qa_id="QA-BATCH0-002",
            question="Can electronic records be admitted in evidence under Section 61 of the Bharatiya Sakshya Adhiniyam, 2023?",
            answer="Under Section 61 of the Bharatiya Sakshya Adhiniyam, 2023 (in force since 1 July 2024 under S.O. 849(E)), nothing in this Adhiniyam shall apply to deny the admissibility of an electronic or digital record in the evidence on the ground that it is an electronic or digital record, and such record shall have the same legal effect, validity and enforceability as other document, subject to the provisions of section 63.",
            supporting_source_ids=["IND-STAT-BSA-2023-SEC61"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-BSA-2023-SEC61",
                    section_or_para_ref="Section 61",
                    verbatim_text="Nothing in this Adhiniyam shall apply to deny the admissibility of an electronic or digital record in the evidence on the ground that it is an electronic or digital record, and such record shall have the same legal effect, validity and enforceability as other document, subject to the provisions of section 63.",
                )
            ],
            legal_domain="Evidence Law",
            statutory_citations=["Section 61, Bharatiya Sakshya Adhiniyam, 2023"],
            legal_as_of_date=date(2026, 10, 16),
            commencement_source_id="IND-NOTIF-MHA-SO-849E-2024",
            commencement_date=date(2024, 7, 1),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
        ),
        LegalQADocument(
            qa_id="QA-BATCH0-003",
            question="What is the inherent power of the High Court preserved under Section 528 of the Bharatiya Nagarik Suraksha Sanhita, 2023?",
            answer="Under Section 528 of the BNSS 2023, the inherent powers of the High Court are preserved to make such orders as necessary to prevent abuse of the process of any court or secure the ends of justice.",
            supporting_source_ids=["IND-STAT-BNSS-2023"],
            evidence_passages=[
                EvidencePassage(
                    source_id="IND-STAT-BNSS-2023",
                    section_or_para_ref="Section 528",
                    verbatim_text="Nothing in this Sanhita shall be deemed to limit or affect the inherent powers of the High Court to make such orders as may be necessary to give effect to any order under this Sanhita, or to prevent abuse of the process of any court or otherwise to secure the ends of justice.",
                )
            ],
            legal_domain="Criminal Procedure",
            statutory_citations=["Section 528, Bharatiya Nagarik Suraksha Sanhita, 2023"],
            legal_as_of_date=date(2026, 10, 16),
            commencement_source_id="IND-NOTIF-MHA-SO-848E-2024",
            commencement_date=date(2024, 7, 1),
            law_status_label=LawStatusLabel.IN_FORCE,
            provision_commencement_status=ProvisionCommencementStatus.COMMENCED,
            temporal_validation_status=TemporalValidationStatus.VERIFIED_CURRENT,
            legal_review_status=LegalReviewStatus.PENDING_LEGAL_REVIEW,
        ),
    ]

    # Save candidates
    with open(batch_file, "w", encoding="utf-8") as f:
        for ex in examples:
            f.write(ex.model_dump_json() + "\n")
    print(f"[OK] Saved 3 candidate examples to {batch_file}")

    # 2. Run DataQualityGate
    from legalmitra.generation.orchestrator import GenerationOrchestrator
    from legalmitra.generation.schemas import GenerationConfig
    from legalmitra.ingestion.registry import SourceRegistryManager

    reg = SourceRegistryManager("registry/source_registry.jsonl")
    orch = GenerationOrchestrator(GenerationConfig(dry_run=True), reg)
    source_ids = [
        "IND-STAT-DPDP-2023",
        "IND-STAT-IT-2000",
        "IND-STAT-BSA-2023-SEC61",
        "IND-STAT-BSA-2023-SEC63",
        "IND-STAT-BNSS-2023",
    ]
    source_texts = {sid: orch.load_source_text(sid) for sid in source_ids}
    gate = DataQualityGate(registry_manager=reg, source_texts=source_texts)
    all_passed, results = gate.validate_batch(examples)
    if not all_passed:
        for r in results:
            if not r.is_valid:
                print(f"[FAIL] Quality gate rejected {r.qa_id}: {r.issues}")
        return False
    print("[OK] All 3 candidate examples passed DataQualityGate")

    # 3. Create review sheet CSV
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "record_id", "question", "review_decision", "legal_accuracy_score_1_to_5",
            "temporal_accuracy_score_1_to_5", "grounding_accuracy_score_1_to_5",
            "reviewer_comments", "reviewer_name_initials", "review_date"
        ])
        writer.writeheader()
        for ex in examples:
            writer.writerow({
                "record_id": ex.qa_id,
                "question": ex.question,
                "review_decision": "",  # Blank by default!
                "legal_accuracy_score_1_to_5": "",
                "temporal_accuracy_score_1_to_5": "",
                "grounding_accuracy_score_1_to_5": "",
                "reviewer_comments": "",
                "reviewer_name_initials": "",
                "review_date": "",
            })
    print(f"[OK] Generated blank review sheet at {csv_file}")

    # 4. Test atomic rollback on bad review decision
    importer = ReviewImporter(audit_dir=out_dir / "audit")
    bad_csv = out_dir / "bad_review.csv"
    with open(bad_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["record_id", "review_decision", "reviewer_comments"])
        writer.writeheader()
        writer.writerow({"record_id": "QA-BATCH0-001", "review_decision": "ILLEGAL_STATUS", "reviewer_comments": "x"})

    try:
        importer.import_reviews(bad_csv, batch_file)
        print("[FAIL] Importer failed to reject invalid review decision!")
        return False
    except ReviewImportError:
        print("[OK] Importer correctly rejected invalid review decision with atomic rollback")

    # 5. Verify batch file remains unmodified after failed import
    with open(batch_file, "r", encoding="utf-8") as f:
        for line in f:
            doc = LegalQADocument(**json.loads(line))
            assert doc.legal_review_status == LegalReviewStatus.PENDING_LEGAL_REVIEW
    print("[OK] Verified batch candidates remain strictly pending_legal_review")
    print("=== Batch 0 Workflow Validation Succeeded ===")
    return True


if __name__ == "__main__":
    success = run_batch_00_validation()
    if not success:
        exit(1)
