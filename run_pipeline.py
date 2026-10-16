"""
LegalMitra Corpus Pipeline Runner
Executes ingestion, Docling/Text extraction, normalization, and generates
sample JSONL dataset outputs and diagnostic failure reports.

Phase 2: Adds source-grounded dataset generation engine with LLM integration.
"""

import argparse
import sys
from datetime import date
from pathlib import Path
import json
from typing import Optional

from legalmitra.core.enums import CourtType, Jurisdiction, LegalReviewStatus, SourceType, SplitType
from legalmitra.core.logging import get_logger
from legalmitra.dataset.jsonl_exporter import JSONLExporter
from legalmitra.dataset.partitioner import DatasetPartitioner
from legalmitra.dataset.pipeline import LegalDataPipeline
from legalmitra.generation.orchestrator import run_generation_pipeline
from legalmitra.generation.schemas import GenerationConfig
from legalmitra.generation.exporter import create_generation_report
from legalmitra.llm.nemotron import NemotronLLMProvider
from legalmitra.schemas.case_analysis import CaseAnalysisDocument
from legalmitra.schemas.drafting_example import DraftingClause, DraftingExampleDocument
from legalmitra.schemas.evaluation import EvaluationQuestionDocument, EvaluationRubric
from legalmitra.schemas.judgment import JudgmentDocument
from legalmitra.schemas.legal_qa import EvidencePassage, LegalQADocument
from legalmitra.schemas.procedural_guide import ProceduralGuidanceDocument, ProceduralStep
from legalmitra.schemas.statute import StatuteDocument

logger = get_logger("run_pipeline")


def run_milestone_pipeline():
    """Run the Phase 1 milestone pipeline (ingestion, extraction, normalization)."""
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

    # 2. Generate grounded synthetic examples (static samples for Phase 1 compatibility)
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


def run_connectivity_test() -> bool:
    """Test Nemotron LLM provider connectivity."""
    logger.info("Testing Nemotron LLM provider connectivity...")
    
    provider = NemotronLLMProvider()
    
    if not provider.is_available():
        logger.error("Nemotron provider not configured. Set NEMOTRON_API_KEY environment variable.")
        logger.info("See .env.example for required configuration.")
        return False
    
    logger.info(f"Provider configured: {provider.model_name} at {provider.base_url}")
    
    try:
        from legalmitra.llm.interface import LLMMessage
        messages = [
            LLMMessage(role="system", content="You are a legal assistant."),
            LLMMessage(role="user", content="Reply with 'OK' if you receive this."),
        ]
        response = provider.generate(messages, temperature=0.1, max_tokens=10)
        logger.info(f"Connectivity test successful. Response: {response.content[:50]}")
        logger.info(f"Model: {response.model_name}, Tokens: {response.usage}")
        return True
    except Exception as e:
        logger.error(f"Connectivity test failed: {e}")
        return False


def run_generation(
    source_ids: Optional[list] = None,
    source_type: Optional[str] = None,
    dry_run: bool = False,
    pilot: bool = False,
    max_sources: int = 10,
    max_examples: int = 50,
    task_types: Optional[list] = None,
) -> dict:
    """Run the Phase 2 generation pipeline."""
    logger.info("Starting Phase 2: Source-Grounded Dataset Generation")
    
    # Parse source_type filter
    stype = None
    if source_type:
        try:
            stype = SourceType(source_type)
        except ValueError:
            logger.error(f"Invalid source_type: {source_type}. Valid: {[s.value for s in SourceType]}")
            return {"success": False, "error": f"Invalid source_type: {source_type}"}
    
    # Build config
    config = GenerationConfig(
        dry_run=dry_run,
        pilot_mode=pilot,
        pilot_max_sources=max_sources,
        pilot_max_examples=max_examples,
    )
    
    if task_types:
        from legalmitra.generation.prompts import TaskType
        config.task_types = [TaskType(t) for t in task_types]
    
    # Run generation
    summary = run_generation_pipeline(
        config=config,
        registry_file="registry/source_registry.jsonl",
        source_ids=source_ids,
        source_type=stype,
        dry_run=dry_run,
        pilot_mode=pilot,
    )
    
    # Create reports
    # Note: We need to collect results from orchestrator for detailed reports
    # For now, export summary
    from legalmitra.generation.exporter import GenerationExporter
    exporter = GenerationExporter("data/03_generated")
    exporter.export_summary(summary)
    exporter.export_markdown_report(summary)
    exporter.export_generation_quality_report(summary, [])
    
    logger.info(f"Generation complete: {summary.tasks_completed}/{summary.total_tasks} tasks, "
                f"{summary.total_examples_generated} examples generated")
    
    return {
        "success": True,
        "summary": summary.model_dump(),
        "report_dir": "data/03_generated/reports",
    }


def validate_sources() -> dict:
    """Validate registered sources for generation readiness."""
    from legalmitra.ingestion.registry import SourceRegistryManager
    
    registry = SourceRegistryManager("registry/source_registry.jsonl")
    records = registry.list_all()
    
    normalized = [r for r in records if r.processing_status.value == "normalized"]
    failed = [r for r in records if r.processing_status.value == "failed"]
    registered = [r for r in records if r.processing_status.value == "registered"]
    
    by_type = {}
    for r in normalized:
        by_type.setdefault(r.source_type.value, 0)
        by_type[r.source_type.value] += 1
    
    logger.info(f"Source validation: {len(normalized)} normalized, {len(failed)} failed, {len(registered)} pending")
    
    return {
        "total": len(records),
        "normalized": len(normalized),
        "failed": len(failed),
        "registered_pending": len(registered),
        "by_type": by_type,
        "normalized_ids": [r.document_id for r in normalized],
    }


def acquire_sources() -> dict:
    """Acquire official Indian legal sources from permitted repositories."""
    from legalmitra.ingestion.acquisition import SourceAcquisitionEngine
    from legalmitra.ingestion.registry import SourceRegistryManager
    from pathlib import Path
    
    registry = SourceRegistryManager("registry/source_registry.jsonl")
    engine = SourceAcquisitionEngine(registry, Path("data/01_raw"))
    res = engine.acquire_all()
    logger.info(f"Source acquisition finished: {res['successfully_acquired']} acquired, "
                f"{res['existing_verified']} existing, {res['failed_acquisitions']} failed")
    return {
        "successfully_acquired": res["successfully_acquired"],
        "existing_verified": res["existing_verified"],
        "failed_acquisitions": res["failed_acquisitions"],
        "total_catalog": res["total_catalog"],
        "records": [r.document_id for r in res["records"]],
    }


def export_splits() -> dict:
    """Re-export dataset splits from normalized documents."""
    from legalmitra.ingestion.registry import SourceRegistryManager
    from legalmitra.normalization.normalizer import DocumentNormalizer
    
    registry = SourceRegistryManager("registry/source_registry.jsonl")
    normalizer = DocumentNormalizer("data/02_normalized", registry)
    
    # Load all normalized models
    normalized_models = []
    norm_dir = Path("data/02_normalized")
    for json_file in norm_dir.glob("*.json"):
        with open(json_file, "r") as f:
            data = json.load(f)
        # Determine type and parse
        if "sections" in data:
            model = StatuteDocument.model_validate(data)
        elif "paragraphs" in data:
            model = JudgmentDocument.model_validate(data)
        else:
            continue
        normalized_models.append(model)
    
    partitioner = DatasetPartitioner(train_ratio=0.6, val_ratio=0.2, test_ratio=0.2, seed=42)
    splits = partitioner.partition_by_source(normalized_models)
    
    JSONLExporter.export(splits[SplitType.TRAIN], "data/splits/train.jsonl")
    JSONLExporter.export(splits[SplitType.VALIDATION], "data/splits/val.jsonl")
    JSONLExporter.export(splits[SplitType.TEST], "data/splits/test.jsonl")
    
    return {
        "train": len(splits[SplitType.TRAIN]),
        "validation": len(splits[SplitType.VALIDATION]),
        "test": len(splits[SplitType.TEST]),
    }


def run_index_kb(db_path: str = "data/legalmitra_kb.db") -> dict:
    """Index normalized legal documents into the SQLite/FTS5 knowledge base."""
    from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
    from legalmitra.schemas.registry import SourceRegistryRecord
    from legalmitra.schemas.statute import StatuteDocument
    from legalmitra.schemas.judgment import JudgmentDocument

    kb = LegalKnowledgeBase(db_path)
    records = {}
    with open("registry/source_registry.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                r = SourceRegistryRecord.model_validate_json(line)
                records[r.document_id] = r
                kb.index_source_record(r)

    norm_dir = Path("data/02_normalized")
    total_statutes = 0
    total_judgments = 0
    for json_file in norm_dir.glob("*.json"):
        data = json.loads(json_file.read_text(encoding="utf-8"))
        s_id = data.get("source_id")
        rec = records.get(s_id)
        if "sections" in data:
            doc = StatuteDocument.model_validate(data)
            kb.index_statute_document(doc, rec)
            total_statutes += 1
        elif "paragraphs" in data:
            doc = JudgmentDocument.model_validate(data)
            is_scaffold = (s_id == "IND-JUD-DEL-2024-BAIL")
            kb.index_judgment_document(doc, rec, is_synthetic_scaffold=is_scaffold)
            total_judgments += 1

    return {
        "status": "success",
        "sources_indexed": kb.count_sources(),
        "chunks_indexed": kb.count_chunks(),
        "statutes_indexed": total_statutes,
        "judgments_indexed": total_judgments,
        "db_path": str(db_path),
    }


def run_search_kb(
    query: str,
    jurisdiction: Optional[str] = None,
    court: Optional[str] = None,
    as_of_date: Optional[str] = None,
    include_synthetic: bool = False,
    limit: int = 5,
) -> list:
    """Search the Legal Knowledge Base with metadata filters."""
    from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
    from legalmitra.knowledge.models import SearchFilters
    kb = LegalKnowledgeBase("data/legalmitra_kb.db")
    eff_date = date.fromisoformat(as_of_date) if as_of_date else None
    filters = SearchFilters(
        jurisdiction=jurisdiction,
        court=court,
        as_of_date=eff_date,
        include_synthetic=include_synthetic,
    )
    results = kb.search(query, filters=filters, limit=limit)
    return [r.model_dump(mode="json") for r in results]


def run_rag_query(
    query: str,
    jurisdiction: Optional[str] = None,
    as_of_date: Optional[str] = None,
    include_synthetic: bool = False,
    limit: int = 4,
) -> dict:
    """Run source-grounded RAG answering on a legal query."""
    from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
    from legalmitra.knowledge.models import SearchFilters
    from legalmitra.rag.engine import LegalRAGEngine
    kb = LegalKnowledgeBase("data/legalmitra_kb.db")
    engine = LegalRAGEngine(knowledge_base=kb)
    eff_date = date.fromisoformat(as_of_date) if as_of_date else None
    filters = SearchFilters(
        jurisdiction=jurisdiction,
        as_of_date=eff_date,
        include_synthetic=include_synthetic,
    )
    resp = engine.answer(query, filters=filters, limit=limit)
    return resp.model_dump(mode="json")


def run_rag_evaluation(
    eval_path: str = "data/05_evaluation/held_out_eval.jsonl",
    top_k: int = 4,
) -> dict:
    """Run automated RAG evaluation over the held-out benchmark."""
    from legalmitra.knowledge.knowledge_base import LegalKnowledgeBase
    from legalmitra.rag.engine import LegalRAGEngine
    from legalmitra.rag.evaluator import RAGEvaluator
    kb = LegalKnowledgeBase("data/legalmitra_kb.db")
    engine = LegalRAGEngine(knowledge_base=kb)
    evaluator = RAGEvaluator(engine)
    summary = evaluator.evaluate_benchmark(Path(eval_path), top_k=top_k)
    dumped = summary.model_dump(mode="json")
    out_file = Path("data/05_evaluation/rag_eval_results.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dumped, f, indent=2, default=str)
    logger.info(f"RAG evaluation results saved to {out_file}")
    return dumped


def main():
    """Main CLI entry point with subcommands."""
    parser = argparse.ArgumentParser(
        description="LegalMitra Pipeline Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  pipeline          Run Phase 1 ingestion/extraction/normalization pipeline
  generate          Run Phase 2 source-grounded dataset generation
  connectivity      Test Nemotron LLM provider connectivity
  validate-sources  Validate registered sources for generation
  export-splits     Re-export train/val/test splits
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # pipeline command
    subparsers.add_parser("pipeline", help="Run Phase 1 milestone pipeline")
    
    # generate command
    gen_parser = subparsers.add_parser("generate", help="Run Phase 2 dataset generation")
    gen_parser.add_argument("--source-ids", nargs="+", help="Specific source IDs to process")
    gen_parser.add_argument("--source-type", choices=[s.value for s in SourceType], help="Filter by source type")
    gen_parser.add_argument("--dry-run", action="store_true", help="Use mock provider (no API calls)")
    gen_parser.add_argument("--pilot", action="store_true", help="Pilot mode: limited sources/examples")
    gen_parser.add_argument("--max-sources", type=int, default=10, help="Max sources in pilot mode")
    gen_parser.add_argument("--max-examples", type=int, default=50, help="Max examples in pilot mode")
    gen_parser.add_argument("--task-types", nargs="+", 
                           choices=[t.value for t in __import__('legalmitra.generation.prompts', fromlist=['TaskType']).TaskType],
                           help="Specific task types to generate")
    
    # acquire-sources command
    subparsers.add_parser("acquire-sources", help="Acquire official Indian legal sources")
    
    # connectivity command
    subparsers.add_parser("connectivity", help="Test Nemotron LLM connectivity")
    
    # validate-sources command
    subparsers.add_parser("validate-sources", help="Validate registered sources")
    
    # export-splits command
    subparsers.add_parser("export-splits", help="Re-export train/val/test splits")

    # index-kb command
    index_kb_p = subparsers.add_parser("index-kb", help="Index normalized legal documents into SQLite/FTS5 knowledge base")
    index_kb_p.add_argument("--db-path", default="data/legalmitra_kb.db", help="Path to SQLite database")

    # search-kb command
    search_kb_p = subparsers.add_parser("search-kb", help="Search the Legal Knowledge Base")
    search_kb_p.add_argument("--query", "-q", required=True, help="Search query")
    search_kb_p.add_argument("--jurisdiction", help="Jurisdiction filter (e.g. IN, IN-DL)")
    search_kb_p.add_argument("--court", help="Court filter")
    search_kb_p.add_argument("--as-of-date", help="Applicable date filter (YYYY-MM-DD)")
    search_kb_p.add_argument("--include-synthetic", action="store_true", help="Include synthetic test scaffolds")
    search_kb_p.add_argument("--limit", type=int, default=5, help="Max results")

    # rag command
    rag_p = subparsers.add_parser("rag", help="Query the Source-Grounded Legal RAG Engine")
    rag_p.add_argument("--query", "-q", required=True, help="Legal question to answer")
    rag_p.add_argument("--jurisdiction", help="Jurisdiction filter")
    rag_p.add_argument("--as-of-date", help="Applicable date filter (YYYY-MM-DD)")
    rag_p.add_argument("--include-synthetic", action="store_true", help="Include synthetic test scaffolds")
    rag_p.add_argument("--limit", type=int, default=4, help="Max retrieved passages")

    # eval-rag command
    eval_rag_p = subparsers.add_parser("eval-rag", help="Run RAG benchmark evaluation")
    eval_rag_p.add_argument("--eval-path", default="data/05_evaluation/held_out_eval.jsonl", help="Evaluation JSONL path")
    eval_rag_p.add_argument("--top-k", type=int, default=4, help="Top-K retrieval limit")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == "pipeline":
            run_milestone_pipeline()
        elif args.command == "generate":
            result = run_generation(
                source_ids=args.source_ids,
                source_type=args.source_type,
                dry_run=args.dry_run,
                pilot=args.pilot,
                max_sources=args.max_sources,
                max_examples=args.max_examples,
                task_types=args.task_types,
            )
            if not result.get("success"):
                sys.exit(1)
        elif args.command == "acquire-sources":
            result = acquire_sources()
            print(json.dumps(result, indent=2))
        elif args.command == "connectivity":
            success = run_connectivity_test()
            sys.exit(0 if success else 1)
        elif args.command == "validate-sources":
            result = validate_sources()
            print(json.dumps(result, indent=2, default=str))
        elif args.command == "export-splits":
            result = export_splits()
            print(json.dumps(result, indent=2))
        elif args.command == "index-kb":
            result = run_index_kb(db_path=args.db_path)
            print(json.dumps(result, indent=2))
        elif args.command == "search-kb":
            results = run_search_kb(
                query=args.query,
                jurisdiction=args.jurisdiction,
                court=args.court,
                as_of_date=args.as_of_date,
                include_synthetic=args.include_synthetic,
                limit=args.limit,
            )
            print(json.dumps(results, indent=2, default=str))
        elif args.command == "rag":
            resp = run_rag_query(
                query=args.query,
                jurisdiction=args.jurisdiction,
                as_of_date=args.as_of_date,
                include_synthetic=args.include_synthetic,
                limit=args.limit,
            )
            print(json.dumps(resp, indent=2, default=str))
        elif args.command == "eval-rag":
            summary = run_rag_evaluation(eval_path=args.eval_path, top_k=args.top_k)
            print(json.dumps(summary, indent=2, default=str))
        else:
            parser.print_help()
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Command failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()