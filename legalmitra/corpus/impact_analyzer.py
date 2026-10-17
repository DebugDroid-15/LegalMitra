"""
Source Change Impact & Evaluation Regression Analyzer (Phase 23)
Maps statutory amendments, substitutions, and repeals to:
1. Affected database knowledge chunks (legal_chunks table)
2. Affected benchmark evaluation cases (data/13_evaluation/evaluation_cases_v2.json)
3. Evaluates regression impact severity and generates recommended test scopes.
"""

from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
import json
from pathlib import Path
import sqlite3
from typing import Any, Dict, List, Optional, Set, Union

from legalmitra.core.logging import get_logger

logger = get_logger("impact_analyzer")


class ChangeType(str, Enum):
    AMENDMENT = "amendment"
    SUBSTITUTION = "substitution"
    INSERTION = "insertion"
    REPEAL = "repeal"
    COMMENCEMENT = "commencement"


class ImpactSeverity(str, Enum):
    CRITICAL = "critical"  # Affects benchmark cases directly or active golden citations
    HIGH = "high"          # Affects provisions with active citations in review queue
    MEDIUM = "medium"      # Affects indexed chunks without active eval case
    LOW = "low"            # Affects unindexed or catalogued-only inventory


@dataclass
class ImpactReport:
    act_title: str
    sections_affected: List[str]
    change_type: ChangeType
    effective_date: Optional[str]
    affected_chunk_ids: List[str]
    affected_chunk_count: int
    affected_eval_cases: List[str]
    affected_eval_count: int
    severity: ImpactSeverity
    rationale: str
    recommended_regression_tests: List[str]
    generated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class SourceChangeImpactAnalyzer:
    """
    Analyzes how legal source modifications ripple through the corpus and evaluation benchmarks.
    """

    def __init__(
        self,
        db_path: Union[str, Path] = "data/legalmitra_kb.db",
        eval_cases_path: Union[str, Path] = "data/13_evaluation/evaluation_cases_v2.json",
    ):
        self.db_path = Path(db_path)
        self.eval_cases_path = Path(eval_cases_path)
        self.eval_cases: List[Dict[str, Any]] = []
        if self.eval_cases_path.exists():
            with open(self.eval_cases_path, "r", encoding="utf-8") as f:
                self.eval_cases = json.load(f)

    def analyze_change(
        self,
        act_title: str,
        sections_affected: List[str],
        change_type: ChangeType = ChangeType.AMENDMENT,
        effective_date: Optional[str] = None,
    ) -> ImpactReport:
        """
        Analyze the impact of a change to an act and set of sections.
        """
        affected_chunk_ids: List[str] = []

        # 1. Query matching chunks in DB
        if self.db_path.exists():
            conn = sqlite3.connect(str(self.db_path))
            c = conn.cursor()
            try:
                # Find chunks matching act title
                act_pattern = f"%{act_title.strip()}%"
                c.execute(
                    "SELECT chunk_id, provision_or_para_ref FROM legal_chunks WHERE act_or_case_title LIKE ?",
                    (act_pattern,),
                )
                rows = c.fetchall()
                for chunk_id, ref in rows:
                    if not sections_affected:
                        affected_chunk_ids.append(chunk_id)
                    else:
                        for s in sections_affected:
                            s_clean = s.strip().lower()
                            if s_clean in (ref or "").lower():
                                affected_chunk_ids.append(chunk_id)
                                break
            finally:
                conn.close()

        # 2. Query affected evaluation cases
        affected_eval_cases: List[str] = []
        for ec in self.eval_cases:
            target_act = ec.get("target_act_or_case", "").lower()
            if act_title.lower() in target_act or target_act in act_title.lower():
                # If specific sections provided, check section overlap
                if sections_affected:
                    target_sections = [s.lower() for s in ec.get("target_sections_or_paras", [])]
                    goldens = [g.lower() for g in ec.get("golden_citations", [])]
                    match = False
                    for s in sections_affected:
                        s_clean = s.strip().lower()
                        if any(s_clean in ts for ts in target_sections) or any(s_clean in g for g in goldens):
                            match = True
                            break
                    if match:
                        affected_eval_cases.append(ec.get("eval_id"))
                else:
                    affected_eval_cases.append(ec.get("eval_id"))

        # 3. Determine severity
        if affected_eval_cases:
            severity = ImpactSeverity.CRITICAL
            rationale = (
                f"Change directly impacts {len(affected_eval_cases)} benchmark evaluation cases: "
                f"{', '.join(affected_eval_cases)}."
            )
        elif affected_chunk_ids:
            severity = ImpactSeverity.HIGH
            rationale = f"Change impacts {len(affected_chunk_ids)} indexed corpus chunks."
        else:
            severity = ImpactSeverity.LOW
            rationale = "No directly indexed chunks or evaluation cases impacted."

        # 4. Generate recommendations
        recommended_tests = ["tests/test_phase23_metric_contracts.py"]
        if affected_eval_cases:
            recommended_tests.append("tests/test_phase22_evaluation.py")
            recommended_tests.append("legalmitra/evaluation/runner.py")

        return ImpactReport(
            act_title=act_title,
            sections_affected=sections_affected,
            change_type=change_type,
            effective_date=effective_date,
            affected_chunk_ids=list(set(affected_chunk_ids)),
            affected_chunk_count=len(set(affected_chunk_ids)),
            affected_eval_cases=affected_eval_cases,
            affected_eval_count=len(affected_eval_cases),
            severity=severity,
            rationale=rationale,
            recommended_regression_tests=recommended_tests,
        )

