"""
Dataset management and versioned governance loader for LegalMitra evaluations.
Loads benchmark cases, validates schemas, verifies partition splits, and computes manifest checksums.
"""

import hashlib
import json
from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from legalmitra.evaluation.models import EvaluationCase, EvaluationCategory


class DatasetManifest(BaseModel):
    version: str = "1.0.0"
    created_date: str = "2026-10-17"
    author: str = "Team Shatrujeet (Amar Khera, Ananya Rout, Lucky Kumar, Omm Prakash Sahoo)"
    total_cases: int
    category_counts: Dict[str, int] = Field(default_factory=dict)
    sha256_checksum: str


class EvaluationDataset:
    """
    Manages loading, filtering, and partitioning of legal evaluation benchmark cases.
    """

    def __init__(self, cases: List[EvaluationCase], version: str = "1.0.0"):
        self.cases = cases
        self.version = version

    @classmethod
    def load_from_json(cls, file_path: str) -> "EvaluationDataset":
        """Load evaluation dataset from a JSON file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Evaluation dataset not found at {file_path}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        cases = [EvaluationCase(**item) for item in data]
        return cls(cases=cases)

    def filter_by_category(self, category: EvaluationCategory) -> List[EvaluationCase]:
        """Return cases matching a specific EvaluationCategory."""
        return [c for c in self.cases if c.category == category]

    def generate_manifest(self, raw_content_bytes: bytes) -> DatasetManifest:
        """Generate a versioned manifest with SHA-256 integrity checksum."""
        sha = hashlib.sha256(raw_content_bytes).hexdigest()
        counts: Dict[str, int] = {}
        for c in self.cases:
            counts[c.category.value] = counts.get(c.category.value, 0) + 1

        return DatasetManifest(
            version=self.version,
            total_cases=len(self.cases),
            category_counts=counts,
            sha256_checksum=sha,
        )

    def save(self, json_path: str, manifest_path: Optional[str] = None) -> None:
        """Persist evaluation cases and corresponding manifest."""
        data = [c.model_dump(mode="json") for c in self.cases]
        content_str = json.dumps(data, indent=2, ensure_ascii=False)
        content_bytes = content_str.encode("utf-8")

        p = Path(json_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content_str)

        if manifest_path:
            manifest = self.generate_manifest(content_bytes)
            mp = Path(manifest_path)
            mp.parent.mkdir(parents=True, exist_ok=True)
            with open(mp, "w", encoding="utf-8") as f:
                f.write(json.dumps(manifest.model_dump(mode="json"), indent=2))

