"""
LegalMitra Legal Knowledge Base
SQLite and FTS5 based full-text and metadata-filtered retrieval engine.
Maintains exact statutory hierarchies (sections, subsections, provisos, explanations)
and case law authorities (coram, ratio, holdings, paragraphs) with strict temporal
and synthetic-scaffold boundaries.
"""

import json
import re
import sqlite3
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from legalmitra.core.enums import CourtType, Jurisdiction, LegalReviewStatus, SourceType
from legalmitra.core.logging import get_logger
from legalmitra.knowledge.models import AuthorityLevel, ChunkHierarchy, SearchFilters, SearchResult
from legalmitra.schemas.judgment import JudgmentDocument
from legalmitra.schemas.registry import SourceRegistryRecord
from legalmitra.schemas.statute import StatuteDocument, StatuteSection

logger = get_logger("knowledge_base")


class LegalKnowledgeBase:
    """
    Local SQLite + FTS5 Legal Knowledge Base.
    Provides structured, auditable storage and high-precision BM25 legal retrieval.
    """

    def __init__(
        self,
        db_path: Union[str, Path] = "data/legalmitra_kb.db",
        must_exist: bool = False,
    ):
        self.db_path = Path(db_path)
        if must_exist and not self.db_path.exists():
            raise FileNotFoundError(
                f"Configured Legal Knowledge Base does not exist at {self.db_path}. "
                "Refusing to initialize a silent empty database."
            )
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self) -> None:
        """Create tables, indexes, and FTS5 virtual tables."""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sources (
                document_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                source_url TEXT NOT NULL,
                source_type TEXT NOT NULL,
                jurisdiction TEXT NOT NULL,
                court TEXT NOT NULL,
                document_date TEXT NOT NULL,
                effective_date TEXT,
                is_historical INTEGER NOT NULL DEFAULT 0,
                is_synthetic_scaffold INTEGER NOT NULL DEFAULT 0,
                repeal_status TEXT NOT NULL DEFAULT 'active',
                checksum TEXT NOT NULL,
                verification_status TEXT NOT NULL,
                metadata_json TEXT NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS legal_chunks (
                chunk_id TEXT PRIMARY KEY,
                source_id TEXT NOT NULL REFERENCES sources(document_id),
                doc_type TEXT NOT NULL,
                act_or_case_title TEXT NOT NULL,
                provision_or_para_ref TEXT NOT NULL,
                hierarchy_level TEXT NOT NULL,
                section_number TEXT,
                paragraph_number INTEGER,
                jurisdiction TEXT NOT NULL,
                court TEXT NOT NULL,
                document_date TEXT NOT NULL,
                effective_date TEXT,
                is_historical INTEGER NOT NULL DEFAULT 0,
                is_synthetic_scaffold INTEGER NOT NULL DEFAULT 0,
                authority_level TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata_json TEXT NOT NULL
            );
        """)

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_source ON legal_chunks(source_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_sec_num ON legal_chunks(section_number);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_para_num ON legal_chunks(paragraph_number);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_doc_type ON legal_chunks(doc_type);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_jurisdiction ON legal_chunks(jurisdiction);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_authority ON legal_chunks(authority_level);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_scaffold ON legal_chunks(is_synthetic_scaffold);")

        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS legal_chunks_fts USING fts5(
                chunk_id UNINDEXED,
                content,
                title,
                act_or_case_title,
                provision_or_para_ref,
                tokenize = 'porter unicode61'
            );
        """)

        self.conn.commit()

    def close(self) -> None:
        """Close database connection."""
        if self.conn:
            self.conn.close()

    def index_source_record(self, record: SourceRegistryRecord) -> None:
        """Store or update source metadata record in the Knowledge Base."""
        cursor = self.conn.cursor()

        is_synthetic = 1 if (
            record.verification_status == LegalReviewStatus.FLAGGED_UNSUPPORTED
            or "IND-JUD-DEL-2024-BAIL" in record.document_id
            or (record.privacy_redaction_notes and "SYNTHETIC" in record.privacy_redaction_notes.upper())
        ) else 0

        repeal_status = "active"
        if "IT-2000" in record.document_id:
            repeal_status = "prospective_repeal"
        elif "DPDP-2023" in record.document_id:
            repeal_status = "partially_in_force"

        cursor.execute("""
            INSERT OR REPLACE INTO sources (
                document_id, title, source_url, source_type, jurisdiction,
                court, document_date, effective_date, is_historical,
                is_synthetic_scaffold, repeal_status, checksum,
                verification_status, metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            record.document_id,
            record.title,
            record.source_url,
            record.source_type.value if hasattr(record.source_type, 'value') else str(record.source_type),
            record.jurisdiction.value if hasattr(record.jurisdiction, 'value') else str(record.jurisdiction),
            record.court.value if hasattr(record.court, 'value') else str(record.court),
            record.document_date.isoformat(),
            record.effective_date.isoformat() if record.effective_date else None,
            0,
            is_synthetic,
            repeal_status,
            record.checksum,
            record.verification_status.value if hasattr(record.verification_status, 'value') else str(record.verification_status),
            json.dumps(record.model_dump(mode="json"))
        ))
        self.conn.commit()

    def _insert_chunk(
        self,
        chunk_id: str,
        source_id: str,
        doc_type: str,
        act_or_case_title: str,
        title: str,
        provision_or_para_ref: str,
        hierarchy_level: str,
        section_number: Optional[str],
        paragraph_number: Optional[int],
        jurisdiction: str,
        court: str,
        document_date: str,
        effective_date: Optional[str],
        is_historical: int,
        is_synthetic_scaffold: int,
        authority_level: str,
        content: str,
        metadata: Dict[str, Any],
    ) -> None:
        """Insert or replace a legal chunk and update the FTS5 index."""
        cursor = self.conn.cursor()

        # Remove existing chunk from FTS if present
        cursor.execute("DELETE FROM legal_chunks_fts WHERE chunk_id = ?", (chunk_id,))

        cursor.execute("""
            INSERT OR REPLACE INTO legal_chunks (
                chunk_id, source_id, doc_type, act_or_case_title,
                provision_or_para_ref, hierarchy_level, section_number,
                paragraph_number, jurisdiction, court, document_date,
                effective_date, is_historical, is_synthetic_scaffold,
                authority_level, content, metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            chunk_id, source_id, doc_type, act_or_case_title,
            provision_or_para_ref, hierarchy_level, section_number,
            paragraph_number, jurisdiction, court, document_date,
            effective_date, is_historical, is_synthetic_scaffold,
            authority_level, content, json.dumps(metadata)
        ))

        # Insert into FTS index
        cursor.execute("""
            INSERT INTO legal_chunks_fts (
                chunk_id, content, title, act_or_case_title, provision_or_para_ref
            ) VALUES (?, ?, ?, ?, ?);
        """, (chunk_id, content, title, act_or_case_title, provision_or_para_ref))

    def index_statute_document(
        self,
        doc: StatuteDocument,
        source_rec: Optional[SourceRegistryRecord] = None
    ) -> int:
        """
        Index a StatuteDocument into the knowledge base.
        Preserves section, subsection, proviso, and explanation structures.
        """
        if source_rec:
            self.index_source_record(source_rec)
        elif not self._source_exists(doc.source_id):
            # Create stub source record if missing
            stub_rec = SourceRegistryRecord(
                document_id=doc.source_id,
                title=doc.act_title,
                source_url=f"https://www.indiacode.nic.in/handle/{doc.source_id}",
                source_type=SourceType.STATUTE,
                jurisdiction=doc.jurisdiction,
                court=CourtType.NONE,
                document_date=doc.enactment_date,
                effective_date=doc.effective_date,
                licence_or_terms="Government of India Open Data License (GODL-India)",
                checksum="0000000000000000000000000000000000000000000000000000000000000000",
                raw_file_path="",
                file_format=".txt",
                byte_size=0,
            )
            self.index_source_record(stub_rec)

        jurisdiction = doc.jurisdiction.value if hasattr(doc.jurisdiction, 'value') else str(doc.jurisdiction)
        doc_date = doc.enactment_date.isoformat()
        eff_date = doc.effective_date.isoformat() if doc.effective_date else None
        
        # Determine appropriate doc_type (e.g. statute, rules_regulation, notification)
        if source_rec and hasattr(source_rec.source_type, 'value'):
            doc_type_val = source_rec.source_type.value
        elif source_rec and isinstance(source_rec.source_type, str):
            doc_type_val = source_rec.source_type
        elif "RULE" in doc.source_id:
            doc_type_val = "rules_regulation"
        elif "NOTIF" in doc.source_id:
            doc_type_val = "notification"
        else:
            doc_type_val = "statute"

        chunks_indexed = 0

        for sec in doc.sections:
            sec_num = sec.section_number
            sec_title = f"{doc.act_title} - Section {sec_num}"
            ref_str = f"Section {sec_num}"

            # 1. Full section chunk
            sec_chunk_id = f"{doc.source_id}:SEC:{sec_num}"
            self._insert_chunk(
                chunk_id=sec_chunk_id,
                source_id=doc.source_id,
                doc_type=doc_type_val,
                act_or_case_title=doc.act_title,
                title=sec_title,
                provision_or_para_ref=ref_str,
                hierarchy_level=ChunkHierarchy.SECTION.value,
                section_number=sec_num,
                paragraph_number=None,
                jurisdiction=jurisdiction,
                court="None (Statutory / Executive)",
                document_date=doc_date,
                effective_date=eff_date,
                is_historical=0,
                is_synthetic_scaffold=0,
                authority_level=AuthorityLevel.BINDING_STATUTE.value,
                content=sec.full_verbatim_text,
                metadata={
                    "section_title": sec.section_title,
                    "chapter_number": sec.chapter_number,
                    "chapter_title": sec.chapter_title,
                    "act_number": doc.act_number,
                }
            )
            chunks_indexed += 1

            # 2. Subsections
            for sub in sec.subsections:
                sub_num = sub.sub_section_number
                sub_chunk_id = f"{doc.source_id}:SEC:{sec_num}:SUB:{sub_num.strip('()')}"
                sub_ref = f"Section {sec_num}{sub_num}"
                self._insert_chunk(
                    chunk_id=sub_chunk_id,
                    source_id=doc.source_id,
                    doc_type=doc_type_val,
                    act_or_case_title=doc.act_title,
                    title=f"{sec_title} {sub_num}",
                    provision_or_para_ref=sub_ref,
                    hierarchy_level=ChunkHierarchy.SUBSECTION.value,
                    section_number=sec_num,
                    paragraph_number=None,
                    jurisdiction=jurisdiction,
                    court="None (Statutory / Executive)",
                    document_date=doc_date,
                    effective_date=eff_date,
                    is_historical=0,
                    is_synthetic_scaffold=0,
                    authority_level=AuthorityLevel.BINDING_STATUTE.value,
                    content=sub.text,
                    metadata={"section_number": sec_num, "subsection_number": sub_num}
                )
                chunks_indexed += 1

            # 3. Provisos
            for idx, proviso in enumerate(sec.provisos, start=1):
                p_chunk_id = f"{doc.source_id}:SEC:{sec_num}:PROVISO:{idx}"
                p_ref = f"Section {sec_num} Proviso {idx}"
                self._insert_chunk(
                    chunk_id=p_chunk_id,
                    source_id=doc.source_id,
                    doc_type=doc_type_val,
                    act_or_case_title=doc.act_title,
                    title=f"{sec_title} Proviso {idx}",
                    provision_or_para_ref=p_ref,
                    hierarchy_level=ChunkHierarchy.PROVISO.value,
                    section_number=sec_num,
                    paragraph_number=None,
                    jurisdiction=jurisdiction,
                    court="None (Statutory / Executive)",
                    document_date=doc_date,
                    effective_date=eff_date,
                    is_historical=0,
                    is_synthetic_scaffold=0,
                    authority_level=AuthorityLevel.BINDING_STATUTE.value,
                    content=proviso.text,
                    metadata={"section_number": sec_num, "proviso_index": idx}
                )
                chunks_indexed += 1

            # 4. Explanations
            for exp in sec.explanations:
                exp_chunk_id = f"{doc.source_id}:SEC:{sec_num}:EXP:{exp.explanation_identifier.replace(' ', '_')}"
                exp_ref = f"Section {sec_num} {exp.explanation_identifier}"
                self._insert_chunk(
                    chunk_id=exp_chunk_id,
                    source_id=doc.source_id,
                    doc_type=doc_type_val,
                    act_or_case_title=doc.act_title,
                    title=f"{sec_title} {exp.explanation_identifier}",
                    provision_or_para_ref=exp_ref,
                    hierarchy_level=ChunkHierarchy.EXPLANATION.value,
                    section_number=sec_num,
                    paragraph_number=None,
                    jurisdiction=jurisdiction,
                    court="None (Statutory / Executive)",
                    document_date=doc_date,
                    effective_date=eff_date,
                    is_historical=0,
                    is_synthetic_scaffold=0,
                    authority_level=AuthorityLevel.BINDING_STATUTE.value,
                    content=exp.text,
                    metadata={"section_number": sec_num, "identifier": exp.explanation_identifier}
                )
                chunks_indexed += 1

        self.conn.commit()
        logger.info(f"Indexed statute '{doc.act_title}' ({doc.source_id}): {chunks_indexed} chunks.")
        return chunks_indexed

    def index_judgment_document(
        self,
        doc: JudgmentDocument,
        source_rec: Optional[SourceRegistryRecord] = None,
        is_synthetic_scaffold: bool = False,
    ) -> int:
        """
        Index a JudgmentDocument into the knowledge base.
        Preserves court, coram, ratio decidendi, holdings, and numbered paragraphs.
        """
        if source_rec:
            self.index_source_record(source_rec)
        elif not self._source_exists(doc.source_id):
            stub_rec = SourceRegistryRecord(
                document_id=doc.source_id,
                title=doc.case_title,
                source_url=f"https://main.sci.gov.in/judgments/{doc.source_id}",
                source_type=SourceType.JUDGMENT,
                jurisdiction=doc.jurisdiction,
                court=doc.court,
                document_date=doc.judgment_date,
                effective_date=None,
                licence_or_terms="Public Domain / Judicial Decisions",
                checksum="0000000000000000000000000000000000000000000000000000000000000000",
                raw_file_path="",
                file_format=".txt",
                byte_size=0,
            )
            self.index_source_record(stub_rec)

        is_scaffold = 1 if (
            is_synthetic_scaffold
            or "IND-JUD-DEL-2024-BAIL" in doc.source_id
            or "IND-JUD-DEL-2024-BAIL" in doc.judgment_id
            or doc.legal_review_status == LegalReviewStatus.FLAGGED_UNSUPPORTED
        ) else 0

        # Authority Level determination under Article 141 of Indian Constitution
        court_name = doc.court.value if hasattr(doc.court, 'value') else str(doc.court)
        if is_scaffold:
            authority = AuthorityLevel.UNVERIFIED_SCAFFOLD.value
        elif "Supreme Court" in court_name:
            authority = AuthorityLevel.BINDING_PRECEDENT.value
        else:
            authority = AuthorityLevel.PERSUASIVE_PRECEDENT.value

        jurisdiction = doc.jurisdiction.value if hasattr(doc.jurisdiction, 'value') else str(doc.jurisdiction)
        doc_date = doc.judgment_date.isoformat()
        chunks_indexed = 0

        # Prepare citations string for metadata and indexing
        citations_str = " | ".join(c.citation_text for c in doc.citations) if doc.citations else ""

        # 1. Ratio Decidendi
        if doc.ratio_decidendi:
            ratio_chunk_id = f"{doc.source_id}:RATIO"
            self._insert_chunk(
                chunk_id=ratio_chunk_id,
                source_id=doc.source_id,
                doc_type="judgment",
                act_or_case_title=doc.case_title,
                title=f"{doc.case_title} - Ratio Decidendi",
                provision_or_para_ref="Ratio Decidendi",
                hierarchy_level=ChunkHierarchy.RATIO.value,
                section_number=None,
                paragraph_number=None,
                jurisdiction=jurisdiction,
                court=court_name,
                document_date=doc_date,
                effective_date=None,
                is_historical=0,
                is_synthetic_scaffold=is_scaffold,
                authority_level=authority,
                content=f"{doc.ratio_decidendi}\n[Citations: {citations_str}]" if citations_str else doc.ratio_decidendi,
                metadata={"coram": doc.bench_coram, "case_number": doc.case_number, "citations": citations_str}
            )
            chunks_indexed += 1

        # 2. Holdings
        for holding in doc.holdings:
            h_chunk_id = f"{doc.source_id}:HOLDING:{holding.issue_number}"
            self._insert_chunk(
                chunk_id=h_chunk_id,
                source_id=doc.source_id,
                doc_type="judgment",
                act_or_case_title=doc.case_title,
                title=f"{doc.case_title} - Holding on Issue {holding.issue_number}",
                provision_or_para_ref=f"Holding {holding.issue_number}",
                hierarchy_level=ChunkHierarchy.HOLDING.value,
                section_number=None,
                paragraph_number=None,
                jurisdiction=jurisdiction,
                court=court_name,
                document_date=doc_date,
                effective_date=None,
                is_historical=0,
                is_synthetic_scaffold=is_scaffold,
                authority_level=authority,
                content=f"Issue: {holding.issue_text}\nHolding: {holding.holding_summary}",
                metadata={
                    "issue_number": holding.issue_number,
                    "supporting_paras": holding.supporting_paragraph_numbers,
                    "citations": citations_str
                }
            )
            chunks_indexed += 1

        # 3. Numbered Paragraphs
        for para in doc.paragraphs:
            p_chunk_id = f"{doc.source_id}:PARA:{para.paragraph_number}"
            p_ref = f"Paragraph {para.paragraph_number}"
            self._insert_chunk(
                chunk_id=p_chunk_id,
                source_id=doc.source_id,
                doc_type="judgment",
                act_or_case_title=doc.case_title,
                title=f"{doc.case_title} - Para {para.paragraph_number}",
                provision_or_para_ref=p_ref,
                hierarchy_level=ChunkHierarchy.PARAGRAPH.value,
                section_number=None,
                paragraph_number=para.paragraph_number,
                jurisdiction=jurisdiction,
                court=court_name,
                document_date=doc_date,
                effective_date=None,
                is_historical=0,
                is_synthetic_scaffold=is_scaffold,
                authority_level=authority,
                content=para.verbatim_text,
                metadata={"page_number": para.page_number, "citations": citations_str}
            )
            chunks_indexed += 1

        self.conn.commit()
        logger.info(f"Indexed judgment '{doc.case_title}' ({doc.source_id}): {chunks_indexed} chunks.")
        return chunks_indexed

    def _source_exists(self, document_id: str) -> bool:
        cursor = self.conn.cursor()
        res = cursor.execute("SELECT 1 FROM sources WHERE document_id = ?", (document_id,)).fetchone()
        return res is not None

    def search(
        self,
        query: str,
        filters: Optional[SearchFilters] = None,
        limit: int = 5,
    ) -> List[SearchResult]:
        """
        Execute full-text and metadata-filtered search over legal chunks.
        Supports query preprocessing, BM25 ranking, and section number boosting.
        """
        filters = filters or SearchFilters()
        cursor = self.conn.cursor()

        # Sanitize query for FTS5
        fts_query = self._sanitize_fts_query(query)

        # Detect statutory section mention in query (e.g. "Section 61", "Section 63", "s. 482")
        explicit_sec = filters.section_number
        if not explicit_sec:
            sec_match = re.search(r"\b(?:section|sec\.?|s\.)\s*(\d+[A-Z]?)\b", query, re.IGNORECASE)
            if sec_match:
                explicit_sec = sec_match.group(1).upper()

        results_dict: Dict[str, SearchResult] = {}

        # 1. Exact Section Boost Query (if section number is present)
        if explicit_sec:
            sec_sql = """
                SELECT c.*, s.source_url
                FROM legal_chunks c
                JOIN sources s ON c.source_id = s.document_id
                WHERE (c.section_number = :sec_num OR c.provision_or_para_ref = :sec_exact OR c.provision_or_para_ref LIKE :sec_like)
                  AND (:act_title_like IS NULL OR c.act_or_case_title LIKE :act_title_like)
                  AND (:jurisdiction IS NULL OR c.jurisdiction = :jurisdiction)
                  AND (:court IS NULL OR c.court = :court)
                  AND (:doc_type IS NULL OR c.doc_type = :doc_type)
                  AND (:include_synthetic = 1 OR c.is_synthetic_scaffold = 0)
                  AND (:is_historical IS NULL OR c.is_historical = :is_historical)
                  AND (:as_of_date IS NULL OR (c.effective_date IS NOT NULL AND c.effective_date <= :as_of_date))
                ORDER BY CASE 
                    WHEN c.section_number = :sec_num AND c.hierarchy_level = 'section' THEN 0 
                    WHEN c.section_number = :sec_num THEN 1
                    ELSE 2 
                END
                LIMIT :limit;
            """
            params = {
                "sec_num": explicit_sec,
                "sec_exact": f"Section {explicit_sec}",
                "sec_like": f"Section {explicit_sec} (%",
                "act_title_like": f"%{filters.act_title}%" if filters.act_title else None,
                "jurisdiction": filters.jurisdiction,
                "court": filters.court,
                "doc_type": filters.doc_type,
                "include_synthetic": 1 if filters.include_synthetic else 0,
                "is_historical": 1 if filters.is_historical else (0 if filters.is_historical is False else None),
                "as_of_date": filters.as_of_date.isoformat() if filters.as_of_date else None,
                "limit": limit * 2,
            }
            q_tokens = {t.lower() for t in re.findall(r'\w+', query)}
            for row in cursor.execute(sec_sql, params).fetchall():
                title_tokens = {t.lower() for t in re.findall(r'\w+', row["act_or_case_title"])}
                overlap = len(q_tokens.intersection(title_tokens))
                match_score = -100.0 - (overlap * 10.0)
                res = self._row_to_result(row, score=match_score)
                results_dict[res.chunk_id] = res

        # 2. Exact Citation or Case Lookup (if citation provided)
        if filters.case_citation:
            cit_sql = """
                SELECT c.*, s.source_url
                FROM legal_chunks c
                JOIN sources s ON c.source_id = s.document_id
                WHERE (c.act_or_case_title LIKE :cit_like OR c.content LIKE :cit_like)
                  AND (:jurisdiction IS NULL OR c.jurisdiction = :jurisdiction)
                  AND (:court IS NULL OR c.court = :court)
                  AND (:doc_type IS NULL OR c.doc_type = :doc_type)
                  AND (:include_synthetic = 1 OR c.is_synthetic_scaffold = 0)
                  AND (:hierarchy_level IS NULL OR c.hierarchy_level = :hierarchy_level)
                LIMIT :limit;
            """
            cit_params = {
                "cit_like": f"%{filters.case_citation}%",
                "jurisdiction": filters.jurisdiction,
                "court": filters.court,
                "doc_type": filters.doc_type,
                "include_synthetic": 1 if filters.include_synthetic else 0,
                "hierarchy_level": filters.hierarchy_level,
                "limit": limit * 2,
            }
            for row in cursor.execute(cit_sql, cit_params).fetchall():
                res = self._row_to_result(row, score=-120.0)
                results_dict[res.chunk_id] = res

        # 3. Full-Text Search Query using FTS5
        if fts_query:
            fts_sql = """
                SELECT c.*, s.source_url, fts.rank
                FROM legal_chunks_fts fts
                JOIN legal_chunks c ON fts.chunk_id = c.chunk_id
                JOIN sources s ON c.source_id = s.document_id
                WHERE legal_chunks_fts MATCH :query
                  AND (:act_title_like IS NULL OR c.act_or_case_title LIKE :act_title_like)
                  AND (:jurisdiction IS NULL OR c.jurisdiction = :jurisdiction)
                  AND (:court IS NULL OR c.court = :court)
                  AND (:doc_type IS NULL OR c.doc_type = :doc_type)
                  AND (:include_synthetic = 1 OR c.is_synthetic_scaffold = 0)
                  AND (:is_historical IS NULL OR c.is_historical = :is_historical)
                  AND (:as_of_date IS NULL OR (c.effective_date IS NOT NULL AND c.effective_date <= :as_of_date))
                  AND (:hierarchy_level IS NULL OR c.hierarchy_level = :hierarchy_level)
                  AND (:para_num IS NULL OR c.paragraph_number = :para_num)
                ORDER BY fts.rank
                LIMIT :limit;
            """
            params = {
                "query": fts_query,
                "act_title_like": f"%{filters.act_title}%" if filters.act_title else None,
                "jurisdiction": filters.jurisdiction,
                "court": filters.court,
                "doc_type": filters.doc_type,
                "include_synthetic": 1 if filters.include_synthetic else 0,
                "is_historical": 1 if filters.is_historical else (0 if filters.is_historical is False else None),
                "as_of_date": filters.as_of_date.isoformat() if filters.as_of_date else None,
                "hierarchy_level": filters.hierarchy_level,
                "para_num": filters.paragraph_number,
                "limit": limit * 2,
            }

            try:
                for row in cursor.execute(fts_sql, params).fetchall():
                    chunk_id = row["chunk_id"]
                    if chunk_id not in results_dict:
                        results_dict[chunk_id] = self._row_to_result(row, score=float(row["rank"]))
            except sqlite3.OperationalError as oe:
                logger.warning(f"FTS search syntax error on query '{fts_query}': {oe}")

        # Sort results: negative scores (direct match) first, then BM25 rank ascending
        sorted_results = sorted(results_dict.values(), key=lambda r: r.score)
        return sorted_results[:limit]

    def _sanitize_fts_query(self, query: str) -> str:
        """Sanitize query string into safe FTS5 query tokens."""
        # Remove characters with special FTS syntax meaning
        cleaned = re.sub(r'[^\w\s]', ' ', query)
        tokens = [t.strip() for t in cleaned.split() if len(t.strip()) > 1]
        if not tokens:
            return ""
        # Return boolean OR of all tokens for broad recall, BM25 handles ranking
        return " OR ".join(f'"{t}"' for t in tokens[:12])

    def _row_to_result(self, row: sqlite3.Row, score: float) -> SearchResult:
        """Convert a database row into a structured SearchResult."""
        meta = json.loads(row["metadata_json"]) if row["metadata_json"] else {}
        doc_date = date.fromisoformat(row["document_date"])
        eff_date = date.fromisoformat(row["effective_date"]) if row["effective_date"] else None

        return SearchResult(
            chunk_id=row["chunk_id"],
            source_id=row["source_id"],
            doc_type=row["doc_type"],
            act_or_case_title=row["act_or_case_title"],
            provision_or_para_ref=row["provision_or_para_ref"],
            hierarchy_level=row["hierarchy_level"],
            section_number=row["section_number"],
            paragraph_number=row["paragraph_number"],
            jurisdiction=row["jurisdiction"],
            court=row["court"],
            document_date=doc_date,
            effective_date=eff_date,
            is_historical=bool(row["is_historical"]),
            is_synthetic_scaffold=bool(row["is_synthetic_scaffold"]),
            authority_level=AuthorityLevel(row["authority_level"]),
            content=row["content"],
            source_url=row["source_url"],
            score=score,
            metadata=meta,
        )

    def count_chunks(self) -> int:
        """Count total legal chunks stored in the knowledge base."""
        cursor = self.conn.cursor()
        res = cursor.execute("SELECT COUNT(*) FROM legal_chunks").fetchone()
        return res[0] if res else 0

    def count_sources(self) -> int:
        """Count total sources stored in the knowledge base."""
        cursor = self.conn.cursor()
        res = cursor.execute("SELECT COUNT(*) FROM sources").fetchone()
        return res[0] if res else 0

    def get_chunks_for_source(self, source_id: str) -> List[Dict[str, Any]]:
        """Retrieve all indexed chunks belonging to a specific source document."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM legal_chunks WHERE source_id = ?", (source_id,))
        return [dict(row) for row in cursor.fetchall()]

    def get_source(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve source document record by document ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sources WHERE document_id = ?", (document_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def clear_source_chunks(self, source_id: str) -> int:
        """Deletes all chunks and FTS index entries for a source to allow clean re-indexing."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM legal_chunks_fts WHERE chunk_id IN (SELECT chunk_id FROM legal_chunks WHERE source_id = ?)", (source_id,))
        cursor.execute("DELETE FROM legal_chunks WHERE source_id = ?", (source_id,))
        count = cursor.rowcount
        self.conn.commit()
        return count


