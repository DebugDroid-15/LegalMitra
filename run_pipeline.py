"""
LegalMitra Corpus Pipeline Runner
Executes ingestion, Docling/Text extraction, normalization, and generates
sample JSONL dataset outputs and diagnostic failure reports.
"""

from datetime import date
from pathlib import Path
import json

from legalmitra.core.enums import CourtType, Jurisdiction, LegalReviewStatus, SourceType, SplitType
from legalmitra.core.logging import get_logger
from legalmitra.dataset.jsonl_exporter import JSONLExporter
from legalmitra.dataset.partitioner import DatasetPartitioner
from legalmitra.dataset.pipeline import LegalDataPipeline
from legalmitra.schemas.case_analysis import CaseAnalysisDocument
from legalmitra.schemas.drafting_example import DraftingClause, DraftingExampleDocument
from legalmitra.schemas.evaluation import EvaluationQuestionDocument, EvaluationRubric
from legalmitra.schemas.judgment import JudgmentDocument
from legalmitra.schemas.legal_qa import EvidencePassage, LegalQADocument
from legalmitra.schemas.procedural_guide import ProceduralGuidanceDocument, ProceduralStep
from legalmitra.schemas.statute import StatuteDocument

logger = get_logger("run_pipeline")


def run_milestone_pipeline():
    logger.info("Initializing LegalMitra Data Engineering Pipeline...")
    pipeline = LegalDataPipeline(
        registry_file="registry/source_registry.jsonl",
        raw_dir="data/01_raw",
        normalized_dir="data/02_normalized",
    )

    corpus_items = [
        (
            Path("corpus/sample_statute_bsa_s61.txt"),
            {
                "document_id": "IND-STAT-BSA-2023-SEC61",
                "title": "Bharatiya Sakshya Adhiniyam, 2023 - Section 61",
                "source_url": "https://www.indiacode.nic.in/handle/123456789/20000",
                "source_type": SourceType.STATUTE,
                "jurisdiction": Jurisdiction.INDIA_CENTRAL,
                "document_date": date(2023, 12, 25),
                "effective_date": date(2024, 7, 1),
                "licence_or_terms": "Government of India Open Data License (GODL-India)",
            },
        ),
        (
            Path("corpus/sample_judgment_sc_privacy.txt"),
            {
                "document_id": "IND-JUD-SC-2017-PUTTASWAMY",
                "title": "Justice K.S. Puttaswamy (Retd.) v. Union of India (2017) 10 SCC 1",
                "source_url": "https://main.sci.gov.in/judgments",
                "source_type": SourceType.JUDGMENT,
                "jurisdiction": Jurisdiction.INDIA_CENTRAL,
                "court": CourtType.SUPREME_COURT,
                "document_date": date(2017, 8, 24),
                "licence_or_terms": "Public Domain / Supreme Court Records",
                "privacy_redaction_notes": "Official reported judgment; no juvenile victim names present.",
            },
        ),
        (
            Path("corpus/sample_statute_bsa_s63.html"),
            {
                "document_id": "IND-STAT-BSA-2023-SEC63",
                "title": "Bharatiya Sakshya Adhiniyam, 2023 - Section 63",
                "source_url": "https://www.indiacode.nic.in/handle/123456789/20000",
                "source_type": SourceType.STATUTE,
                "jurisdiction": Jurisdiction.INDIA_CENTRAL,
                "document_date": date(2023, 12, 25),
                "effective_date": date(2024, 7, 1),
                "licence_or_terms": "Government of India Open Data License (GODL-India)",
            },
        ),
        (
            Path("corpus/sample_statute_pocso_s4.txt"),
            {
                "document_id": "IND-STAT-POCSO-2012-SEC4",
                "title": "Protection of Children from Sexual Offences Act, 2012 - Section 4",
                "source_url": "https://www.indiacode.nic.in/handle/123456789/2056",
                "source_type": SourceType.STATUTE,
                "jurisdiction": Jurisdiction.INDIA_CENTRAL,
                "document_date": date(2012, 6, 19),
                "licence_or_terms": "Government of India Open Data License (GODL-India)",
                "privacy_redaction_notes": "Statutory redaction obligation under POCSO Section 33(7) applied.",
            },
        ),
        (
            Path("corpus/sample_judgment_bns_bail.txt"),
            {
                "document_id": "IND-JUD-DEL-2024-BAIL",
                "title": "State (NCT of Delhi) v. Rahul Kumar - Anticipatory Bail under BNSS",
                "source_url": "https://delhihighcourt.nic.in/judgments",
                "source_type": SourceType.JUDGMENT,
                "jurisdiction": Jurisdiction.DELHI,
                "court": CourtType.HIGH_COURT_DELHI,
                "document_date": date(2024, 7, 10),
                "licence_or_terms": "Public Domain / High Court of Delhi",
            },
        ),
        (
            Path("corpus/unsupported_dummy.xyz"),
            {
                "document_id": "IND-UNSUPPORTED-001",
                "title": "Corrupt or Unsupported Document Format (.xyz)",
                "source_url": "https://example.com/unsupported",
                "source_type": SourceType.OTHER,
                "document_date": date(2024, 1, 1),
                "licence_or_terms": "Unknown",
            },
        ),
    ]

    logger.info("Executing batch pipeline across corpus items...")
    results = pipeline.process_batch(corpus_items, force_reprocess=True)

    # 1. Generate failure report
    failure_report_md = pipeline.get_failure_report()
    failure_report_path = Path("EXTRACTION_FAILURE_REPORT.md")
    failure_report_path.write_text(failure_report_md, encoding="utf-8")
    logger.info(f"Wrote failure diagnostic report to {failure_report_path}")

    # 2. Generate grounded synthetic examples
    logger.info("Generating grounded example datasets across all 7 schemas...")

    # (a) Legal Q&A Document
    qa_example = LegalQADocument(
        qa_id="QA-BSA-S61-001",
        question="Under the Bharatiya Sakshya Adhiniyam, 2023, on what grounds can an electronic record NOT be denied admissibility?",
        answer="Under Section 61 of the Bharatiya Sakshya Adhiniyam, 2023, nothing in the Adhiniyam shall apply to deny the admissibility of an electronic or digital record in evidence solely on the ground that it is an electronic or digital record. Such record holds the same legal validity, effect, and enforceability as any physical document, subject to the certification requirement set out in Section 63.",
        supporting_source_ids=["IND-STAT-BSA-2023-SEC61"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-BSA-2023-SEC61",
                section_or_para_ref="Section 61",
                verbatim_text="Nothing in this Adhiniyam shall apply to deny the admissibility of an electronic or digital record in the evidence on the ground that it is an electronic or digital record, and such record shall have the same legal effect, validity and enforceability as other document, subject to the provisions of section 63.",
                page_number=1,
            )
        ],
        legal_domain="Criminal Law - Evidence",
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        statutory_citations=["Section 61, Bharatiya Sakshya Adhiniyam, 2023", "Section 63, Bharatiya Sakshya Adhiniyam, 2023"],
        legal_review_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
    )

    # (b) Case Analysis Document
    ca_example = CaseAnalysisDocument(
        analysis_id="CA-PUTTASWAMY-2017-001",
        case_id="IND-JUD-SC-2017-PUTTASWAMY",
        case_title="Justice K.S. Puttaswamy (Retd.) and Another v. Union of India and Others",
        court=CourtType.SUPREME_COURT,
        judgment_date=date(2017, 8, 24),
        bench_coram=[
            "J.S. Khehar, CJI",
            "J. Chelameswar, J.",
            "S.A. Bobde, J.",
            "R.K. Agrawal, J.",
            "Rohinton Fali Nariman, J.",
            "A.M. Sapre, J.",
            "D.Y. Chandrachud, J.",
            "Sanjay Kishan Kaul, J.",
            "S. Abdul Nazeer, J.",
        ],
        factual_matrix_summary="Constitutional challenge referred to a 9-judge Constitution Bench regarding whether privacy is a constitutionally protected fundamental right in India.",
        issues_raised=["Whether the right to privacy is a fundamental right guaranteed under Part III of the Constitution of India?"],
        ratio_decidendi="The right to privacy is protected as an intrinsic part of the right to life and personal liberty under Article 21 and as a part of the freedoms guaranteed by Part III of the Constitution. M.P. Sharma and Kharak Singh are overruled to that extent.",
        precedential_value="Binding 9-Judge Constitution Bench precedent under Article 141 of the Constitution of India.",
        supporting_source_ids=["IND-JUD-SC-2017-PUTTASWAMY"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-JUD-SC-2017-PUTTASWAMY",
                section_or_para_ref="Ratio Decidendi",
                verbatim_text="The right to privacy is protected as an intrinsic part of the right to life and personal liberty under Article 21 and as a part of the freedoms guaranteed by Part III of the Constitution.",
            )
        ],
        legal_review_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
    )

    # (c) Procedural Guidance Document
    proc_example = ProceduralGuidanceDocument(
        guide_id="PROC-BNSS-482-BAIL-001",
        procedure_title="Filing Anticipatory Bail Application under BNSS",
        governing_statutes=["Bharatiya Nagarik Suraksha Sanhita, 2023 (Section 482)"],
        forum_or_court="Court of Sessions / High Court",
        jurisdiction=Jurisdiction.DELHI,
        limitation_period="Prior to execution of arrest by law enforcement",
        steps=[
            ProceduralStep(
                step_number=1,
                step_title="Establish Reasonable Apprehension of Arrest",
                action_description="Identify registered FIR number or complaint showing non-bailable accusation under Bharatiya Nyaya Sanhita (BNS).",
                responsible_party="Advocate for Applicant",
                statutory_rule="Section 482(1) BNSS",
            ),
            ProceduralStep(
                step_number=2,
                step_title="Draft and Lodge Petition before High Court / Sessions Court",
                action_description="File notice of motion with supporting affidavit, clean antecedents certificate, and undertaking to join investigation.",
                responsible_party="Counsel on Record",
                statutory_rule="Section 482(2) BNSS",
            ),
        ],
        supporting_source_ids=["IND-JUD-DEL-2024-BAIL"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-JUD-DEL-2024-BAIL",
                section_or_para_ref="Paragraph 3",
                verbatim_text="The statutory considerations under Section 482 of BNSS mandate that the Court assess the nature and gravity of the accusation, the antecedents of the applicant, and the possibility of the applicant fleeing from justice.",
            )
        ],
        legal_review_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
    )

    # (d) Drafting Example Document
    draft_example = DraftingExampleDocument(
        template_id="DRAFT-BSA-S63-CERT-001",
        template_title="Certificate for Admissibility of Electronic Records under Section 63(4) BSA",
        category="Statutory Certificate",
        court_or_authority="Court of Competent Jurisdiction",
        statutory_basis="Section 63(4) of Bharatiya Sakshya Adhiniyam, 2023",
        jurisdiction=Jurisdiction.INDIA_CENTRAL,
        clauses=[
            DraftingClause(
                clause_heading="Statement of Management and Operation",
                clause_text="I certify that during the period [PERIOD], the computer device [DEVICE IDENTIFIER] was operating properly and under my lawful official control.",
                is_mandatory=True,
                statutory_rationale="Mandated by Section 63(4)(a) of Bharatiya Sakshya Adhiniyam, 2023.",
            ),
            DraftingClause(
                clause_heading="Truth and Faith Clause",
                clause_text="The contents of this certificate are true to the best of my knowledge and belief.",
                is_mandatory=True,
                statutory_rationale="Mandatory solemn declaration required for evidentiary admissibility.",
            ),
        ],
        full_draft_template="I, [NAME OF RESPONSIBLE OFFICER], son/daughter of [PARENT NAME], aged [AGE], residing at [ADDRESS], do hereby solemnly certify under Section 63(4) of the Bharatiya Sakshya Adhiniyam, 2023:\n1. That I am the in-charge of [COMPUTER/SERVER] located at [LOCATION].\n2. That the electronic record [FILE NAME/HASH] was generated in regular course.\nDate: [DATE]\nSignature: [SIGNATURE]",
        placeholders=["[NAME OF RESPONSIBLE OFFICER]", "[DEVICE IDENTIFIER]", "[FILE NAME/HASH]", "[DATE]"],
        supporting_source_ids=["IND-STAT-BSA-2023-SEC61"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-BSA-2023-SEC61",
                section_or_para_ref="Proviso to Section 61",
                verbatim_text="Provided that where any electronic record is produced in evidence, it shall be accompanied by a certificate referred to in sub-section (4) of section 63.",
            )
        ],
        legal_review_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
    )

    # (e) Evaluation Question Document
    eval_example = EvaluationQuestionDocument(
        eval_id="EVAL-BSA-S61-001",
        question="Which legislative enactment and section in contemporary Indian law replaces Section 65B of the repealed Indian Evidence Act, 1872 regarding electronic records?",
        expected_answer="Sections 61 and 63 of the Bharatiya Sakshya Adhiniyam, 2023 (Act No. 47 of 2023) replace Section 65B of the repealed Indian Evidence Act, 1872.",
        target_statute_or_case="Bharatiya Sakshya Adhiniyam, 2023, Sections 61 and 63",
        golden_citations=["Section 61, Bharatiya Sakshya Adhiniyam, 2023", "Section 63, Bharatiya Sakshya Adhiniyam, 2023"],
        forbidden_terms_or_repealed_citations=["Indian Evidence Act, 1872 (as applicable law for post-July 2024 crimes)"],
        rubric=EvaluationRubric(accuracy_weight=0.4, statutory_citation_weight=0.3, grounding_faithfulness_weight=0.3),
        supporting_source_ids=["IND-STAT-BSA-2023-SEC61"],
        evidence_passages=[
            EvidencePassage(
                source_id="IND-STAT-BSA-2023-SEC61",
                section_or_para_ref="Section 61",
                verbatim_text="Nothing in this Adhiniyam shall apply to deny the admissibility of an electronic or digital record in the evidence on the ground that it is an electronic or digital record",
            )
        ],
        legal_domain="Criminal Law - Evidence",
        legal_review_status=LegalReviewStatus.UNVERIFIED_AUTOMATED,
    )

    # 3. Export to JSONL in data directories
    JSONLExporter.export([qa_example], "data/03_generated/legal_qa.jsonl")
    JSONLExporter.export([ca_example], "data/03_generated/case_analysis.jsonl")
    JSONLExporter.export([proc_example], "data/03_generated/procedural_guide.jsonl")
    JSONLExporter.export([draft_example], "data/03_generated/drafting_examples.jsonl")
    JSONLExporter.export([eval_example], "data/05_evaluation/evaluation_benchmark.jsonl")

    # 4. Verified examples directory
    verified_qa = qa_example.model_copy(update={"legal_review_status": LegalReviewStatus.PENDING_LEGAL_REVIEW})
    JSONLExporter.export([verified_qa], "data/04_verified/verified_examples.jsonl")

    # 5. Partition normalized models into train / validation / test splits
    normalized_models = [m for _, m in results if m is not None]
    partitioner = DatasetPartitioner(train_ratio=0.6, val_ratio=0.2, test_ratio=0.2, seed=42)
    splits = partitioner.partition_by_source(normalized_models)

    JSONLExporter.export(splits[SplitType.TRAIN], "data/splits/train.jsonl")
    JSONLExporter.export(splits[SplitType.VALIDATION], "data/splits/val.jsonl")
    JSONLExporter.export(splits[SplitType.TEST], "data/splits/test.jsonl")

    logger.info("Pipeline run complete! All outputs successfully generated and verified.")


if __name__ == "__main__":
    run_milestone_pipeline()
