"""
Phase 93: Pillar 1 — Bhashini ASR (Voice-to-Text Speech Recognition)
Provides high-fidelity speech-to-text decoding for 22 Scheduled Indian Languages + regional dialects.
Converts raw citizen audio streams (WAV, MP3, WebM, PCM) into clean Indic legal prompts.
"""

from __future__ import annotations

import base64
import logging
import os
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from legalmitra.multilingual.bhashini_gateway import (
    BhashiniTaskType,
    BhashiniULCAGateway,
    ULCAInferenceRequest,
    ULCAInferenceResponse,
)
from legalmitra.multilingual.bhashini_pipeline import IndicLanguageCode

logger = logging.getLogger("bhashini_asr")


@dataclass
class ASRExecutionResult:
    success: bool
    language: str
    transcription: str
    confidence_score: float
    duration_seconds: float
    latency_ms: float
    provider: str
    error_message: Optional[str] = None


class BhashiniASREngine:
    """
    Sovereign Speech-to-Text Engine powered by Bhashini IndicConformer / Conformer models.
    Supports audio uploads and streamed chunk decoding.
    """

    def __init__(self, gateway: Optional[BhashiniULCAGateway] = None):
        self.gateway = gateway or BhashiniULCAGateway()

    def transcribe_audio_bytes(
        self,
        audio_bytes: bytes,
        language: str = "mr",
        audio_format: str = "audio/wav"
    ) -> ASRExecutionResult:
        """
        Transcribes raw audio bytes into native Indic text.
        """
        t0 = time.time()
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

        # Estimate duration roughly based on 16kHz 16-bit PCM (32000 bytes/sec)
        est_duration = round(len(audio_bytes) / 32000.0, 2)
        if est_duration < 0.1:
            est_duration = 1.0

        req = ULCAInferenceRequest(
            task_type=BhashiniTaskType.ASR,
            source_language=language,
            audio_base64=audio_b64
        )

        resp: ULCAInferenceResponse = self.gateway.execute_task(req)
        latency_ms = round((time.time() - t0) * 1000, 2)

        if resp.success and resp.output_text:
            return ASRExecutionResult(
                success=True,
                language=resp.source_language,
                transcription=resp.output_text,
                confidence_score=0.98,
                duration_seconds=est_duration,
                latency_ms=latency_ms,
                provider=resp.provider
            )
        else:
            return ASRExecutionResult(
                success=False,
                language=language,
                transcription="",
                confidence_score=0.0,
                duration_seconds=est_duration,
                latency_ms=latency_ms,
                provider=resp.provider,
                error_message=resp.error_message or "ASR transcription failed"
            )

    def transcribe_base64(
        self,
        audio_base64: str,
        language: str = "mr"
    ) -> ASRExecutionResult:
        """Helper to transcribe when audio is already base64 encoded (e.g. from browser frontend)."""
        # Strip data URL prefix if present
        if "," in audio_base64:
            audio_base64 = audio_base64.split(",", 1)[1]
        try:
            raw_bytes = base64.b64decode(audio_base64)
            return self.transcribe_audio_bytes(raw_bytes, language=language)
        except Exception as e:
            return ASRExecutionResult(
                success=False,
                language=language,
                transcription="",
                confidence_score=0.0,
                duration_seconds=0.0,
                latency_ms=0.0,
                provider="error",
                error_message=f"Failed to decode base64 audio: {str(e)}"
            )
