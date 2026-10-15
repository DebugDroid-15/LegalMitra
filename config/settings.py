"""
LegalMitra Configuration Settings
Centralizes project paths, pipeline controls, and LLM credentials.
"""

import os
from pathlib import Path
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PipelineSettings(BaseSettings):
    """
    Settings for paths, extraction, normalization, deduplication, and LLM connection.
    Values can be overridden by environment variables or .env file.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Base Project Paths
    base_dir: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent)
    raw_dir: Path = Field(default_factory=lambda: Path("data/01_raw"))
    normalized_dir: Path = Field(default_factory=lambda: Path("data/02_normalized"))
    generated_dir: Path = Field(default_factory=lambda: Path("data/03_generated"))
    verified_dir: Path = Field(default_factory=lambda: Path("data/04_verified"))
    evaluation_dir: Path = Field(default_factory=lambda: Path("data/05_evaluation"))
    splits_dir: Path = Field(default_factory=lambda: Path("data/splits"))
    registry_file: Path = Field(default_factory=lambda: Path("registry/source_registry.jsonl"))

    # Extraction Settings
    allowed_extensions: List[str] = Field(default=[".pdf", ".docx", ".html", ".txt", ".md"])
    enable_ocr: bool = Field(default=False, description="Enable OCR in Docling if scanned PDF")
    max_file_size_mb: float = Field(default=100.0)

    # NVIDIA Nemotron LLM Provider Configuration
    # Store credentials in environment variables (NEMOTRON_API_KEY, NEMOTRON_BASE_URL, etc.)
    nemotron_api_key: Optional[str] = Field(
        default=None,
        validation_alias="NEMOTRON_API_KEY",
        description="NVIDIA API key for Nemotron"
    )
    nemotron_base_url: str = Field(
        default="https://integrate.api.nvidia.com/v1",
        validation_alias="NEMOTRON_BASE_URL",
        description="Base URL for NVIDIA NIM or OpenAI-compatible endpoint"
    )
    nemotron_model_name: str = Field(
        default="nvidia/llama-3.1-nemotron-70b-instruct",
        validation_alias="NEMOTRON_MODEL_NAME",
        description="Model name/id to query"
    )
    nemotron_api_format: str = Field(
        default="openai_compatible",
        validation_alias="NEMOTRON_API_FORMAT",
        description="API protocol format ('openai_compatible' or 'nvidia_nim')"
    )
    nemotron_timeout_seconds: float = Field(
        default=60.0,
        validation_alias="NEMOTRON_TIMEOUT_SECONDS"
    )

    def resolve_paths(self) -> None:
        """Resolve all relative paths against base_dir and ensure directories exist."""
        for attr in [
            "raw_dir",
            "normalized_dir",
            "generated_dir",
            "verified_dir",
            "evaluation_dir",
            "splits_dir",
        ]:
            val: Path = getattr(self, attr)
            if not val.is_absolute():
                setattr(self, attr, (self.base_dir / val).resolve())
            getattr(self, attr).mkdir(parents=True, exist_ok=True)

        if not self.registry_file.is_absolute():
            self.registry_file = (self.base_dir / self.registry_file).resolve()
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)


# Global settings singleton
settings = PipelineSettings()
settings.resolve_paths()

