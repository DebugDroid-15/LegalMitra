"""
Tests for Phase 120: Production Semantic Cache, Health Monitoring & Live Telemetry.
"""

from __future__ import annotations

import os
import shutil
import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from legalmitra.server.api import app
from legalmitra.telemetry.production_cache import (
    CachedResponseEntry,
    LiveQueryTelemetryLogger,
    ProductionSemanticCache,
    get_live_telemetry,
    get_semantic_cache,
)


@pytest.fixture
def temp_cache_dir(tmp_path):
    db_file = tmp_path / "test_semantic_cache.db"
    telemetry_file = tmp_path / "test_telemetry.jsonl"
    cache = ProductionSemanticCache(db_path=db_file, max_memory_entries=10)
    telemetry = LiveQueryTelemetryLogger(log_path=telemetry_file)
    return cache, telemetry, tmp_path


class TestPhase120ProductionCachingAndTelemetry:
    def test_cache_put_and_get_latency(self, temp_cache_dir):
        cache, _, _ = temp_cache_dir
        query = "party ne cheque diya tha bounce ho gaya sign mismatch"
        answer = "### ⚖️ Direct Position\nUnder Section 138 Negotiable Instruments Act..."
        citations = ["Negotiable Instruments Act, 1881 (Section 138)"]
        provisions = ["Section 138 NI Act"]

        # 1. Put into cache
        cache.put(query, answer, citations, provisions, language="en")

        # 2. Measure retrieval latency (<5ms)
        t0 = time.perf_counter()
        entry = cache.get(query, language="en")
        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        assert entry is not None
        assert entry.answer_text == answer
        assert "138" in entry.citations[0]
        assert elapsed_ms < 15.0  # Under 15ms in test runner (normally <1ms in memory)

    def test_cache_normalization_word_order_and_punctuation(self, temp_cache_dir):
        cache, _, _ = temp_cache_dir
        q1 = "Police station complaint nahi le rahe? SHO bhaga raha hai!"
        q2 = "police station complaint nahi le rahe sho bhaga raha hai"
        answer = "### ⚖️ Direct Position\nSection 173(4) BNSS..."

        cache.put(q1, answer, ["BNSS 173(4)"], ["Section 173(4)"])
        entry = cache.get(q2)
        assert entry is not None
        assert entry.answer_text == answer

    def test_telemetry_event_logging(self, temp_cache_dir):
        _, telemetry, _ = temp_cache_dir
        ev = telemetry.record_query(
            raw_query="landlord locked flat",
            normalized_query="landlord locked flat",
            detected_language="en",
            cache_hit=False,
            latency_ms=12.4,
            has_recognized_intent=True,
            statutory_citations_count=2,
            is_unrecognized_slang=False,
        )

        assert ev.latency_ms == 12.4
        recent = telemetry.get_recent_events(limit=5)
        assert len(recent) >= 1
        assert recent[-1]["raw_query"] == "landlord locked flat"

    def test_unrecognized_slang_telemetry_flag(self, temp_cache_dir):
        _, telemetry, _ = temp_cache_dir
        telemetry.record_query(
            raw_query="random untracked slang jargon xyz123",
            normalized_query="random untracked slang jargon xyz123",
            detected_language="en",
            cache_hit=False,
            latency_ms=45.0,
            has_recognized_intent=False,
            statutory_citations_count=0,
            is_unrecognized_slang=True,
        )

        unrecognized = telemetry.get_unrecognized_slang_inputs()
        assert len(unrecognized) == 1
        assert "xyz123" in unrecognized[0]["raw_query"]

    def test_api_health_includes_cache_metrics(self):
        client = TestClient(app)
        resp = client.get("/api/v1/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert "semantic_cache_stats" in data
        assert "persistent_cache_entries" in data["semantic_cache_stats"]

    def test_api_telemetry_stats_endpoint(self):
        client = TestClient(app)
        resp = client.get("/api/v1/telemetry/stats")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "active"
        assert "cache" in data
        assert "recent_queries" in data
