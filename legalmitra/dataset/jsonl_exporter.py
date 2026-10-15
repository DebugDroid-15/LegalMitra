"""
LegalMitra JSONL Exporter
Handles high-throughput, schema-validated JSONL serialization and deserialization.
"""

import json
from pathlib import Path
from typing import Iterator, List, Type, Union
from pydantic import BaseModel

from legalmitra.core.logging import get_logger

logger = get_logger("jsonl_exporter")


class JSONLExporter:
    """
    Exports and imports schema-validated records in JSONL format.
    """

    @staticmethod
    def export(items: List[BaseModel], output_path: Union[str, Path], append: bool = False) -> int:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        mode = "a" if append else "w"
        written = 0
        with path.open(mode, encoding="utf-8") as f:
            for item in items:
                line = item.model_dump_json()
                f.write(line + "\n")
                written += 1

        logger.info(f"Exported {written} records to {path}")
        return written

    @staticmethod
    def load(file_path: Union[str, Path], model_class: Type[BaseModel]) -> List[BaseModel]:
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {path}")

        records = []
        with path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                clean = line.strip()
                if not clean:
                    continue
                try:
                    data = json.loads(clean)
                    records.append(model_class.model_validate(data))
                except Exception as e:
                    logger.error(f"Error parsing line {line_no} in {path}: {e}")
                    raise

        return records

