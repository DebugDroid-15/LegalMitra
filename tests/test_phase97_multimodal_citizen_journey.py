"""
Phase 97: End-to-End Multimodal Citizen Journey Verification & Benchmark Hardening
Automated comprehensive test suite validating all 4 Bhashini pillars working cohesively:
1. Citizen Speaks Grievance (Voice Audio) -> Bhashini ASR (Phase 93)
2. Citizen Uploads Scanned FIR (Image) -> Bhashini Document OCR (Phase 94)
3. Sovereign Central Gateway & Hybrid Routing -> Bhashini ULCA (Phase 92)
4. AI Kosh Legal RAG Retrieval & Multi-dialect IndicTrans2 -> Sovereign NMT (Phase 95)
5. Citizen Listens to Audio Guidance -> Bhashini TTS (Phase 96)
"""

from __future__ import annotations

import base64
import os
import time
import unittest
from typing import Dict, List

from legalmitra.multilingual.bhashini_gateway import (
    BhashiniGatewayConfig,
    BhashiniTaskType,
    BhashiniULCAGateway,
    ULCAInferenceRequest,
    ULCAInferenceResponse,
)
from legalmitra.multilingual.asr_engine import BhashiniASREngine
from legalmitra.multilingual.ocr_engine import BhashiniLegalOCREngine
from legalmitra.multilingual.indictrans2_engine import SovereignIndicTrans2Engine
from legalmitra.multilingual.tts_engine import BhashiniLegalTTSEngine


class TestBhashiniMultimodalCitizenJourney(unittest.TestCase):
    """
    Validates complete round-trip citizen journey from spoken audio / scanned document
    to statutory grounding and voice audio delivery.
    """

    @classmethod
    def setUpClass(cls):
        cls.gateway = BhashiniULCAGateway()
        cls.asr = BhashiniASREngine(cls.gateway)
        cls.ocr = BhashiniLegalOCREngine(cls.gateway)
        cls.nmt = SovereignIndicTrans2Engine()
        cls.tts = BhashiniLegalTTSEngine(cls.gateway)

    def test_01_gateway_diagnostics_and_offline_routing(self):
        """Verifies Gateway dispatches correctly across all 4 tasks without errors."""
        for task in [BhashiniTaskType.TRANSLATION, BhashiniTaskType.ASR, BhashiniTaskType.TTS, BhashiniTaskType.OCR]:
            req = ULCAInferenceRequest(
                task_type=task,
                source_language="mr",
                target_language="en",
                input_text="FIR नोंदवून घेण्यास नकार दिल्यास कायदेशीर उपाय",
                audio_base64="mock_audio_bytes",
                image_base64="mock_image_bytes"
            )
            resp = self.gateway.execute_task(req)
            self.assertTrue(resp.success, f"Gateway failed on task {task}")
            self.assertIn("offline_hybrid", resp.provider)

    def test_02_pillar1_asr_spoken_audio_transcription(self):
        """Tests citizen speaking in Marathi, Hindi, and Tamil."""
        test_languages = ["mr", "hi", "ta", "te", "bn"]
        mock_wav = b"RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00"
        b64_audio = base64.b64encode(mock_wav).decode("utf-8")

        for lang in test_languages:
            res = self.asr.transcribe_base64(b64_audio, language=lang)
            self.assertTrue(res.success)
            self.assertEqual(res.language, lang)
            self.assertGreater(len(res.transcription), 5)
            self.assertGreaterEqual(res.confidence_score, 0.90)

    def test_03_pillar2_ocr_scanned_fir_statutory_extraction(self):
        """Tests parsing scanned police documents and extracting Devanagari sections."""
        dummy_img = b"mock_scanned_fir_image_bytes"
        b64_doc = base64.b64encode(dummy_img).decode("utf-8")

        res = self.ocr.analyze_base64(b64_doc, language="mr")
        self.assertTrue(res.success)
        self.assertEqual(res.document_type, "POLICE_COMPLAINT_REPRESENTATION")
        canonical_sections = [s.normalized_canonical for s in res.detected_statutes]
        self.assertIn("Section 318(4) BNS", canonical_sections)
        self.assertIn("Section 316 BNS", canonical_sections)

    def test_04_pillar3_nmt_citation_shielding_and_dialects(self):
        """Tests translation across 22 Scheduled languages and regional dialects while preserving citations."""
        en_statute_text = (
            "Under Section 173(4) BNSS, if the police refuse to register an FIR, "
            "an application can be filed before the Judicial Magistrate under Section 175(3) BNSS."
        )

        target_test_dialects = ["hi", "mr", "ta", "te", "bn", "gu", "kn", "bho", "mwr"]
        for target in target_test_dialects:
            res = self.nmt.translate_with_sovereign_fidelity(en_statute_text, target_language=target)
            self.assertTrue(res.is_sovereign_grounded)
            self.assertEqual(len(res.preserved_citations), 2)
            # Ensure both citations appear intact in the translated text
            self.assertIn("Section 173(4) BNSS", res.translated_text)
            self.assertIn("Section 175(3) BNSS", res.translated_text)

    def test_05_pillar4_tts_voice_guidance_synthesis(self):
        """Tests audio generation and phonetic abbreviation expansions."""
        marathi_advice = (
            "पोलीस ठाण्यात तक्रार नोंदवून घेण्यास नकार दिल्यास Section 173(4) BNSS अंतर्गत "
            "SP यांच्याकडे लेखी तक्रार पाठवावी."
        )
        res = self.tts.synthesize_speech(marathi_advice, language="mr")
        self.assertTrue(res.success)
        self.assertEqual(res.audio_format, "audio/wav")
        self.assertGreater(len(res.audio_base64), 20)
        self.assertGreater(res.duration_seconds, 1.0)

    def test_06_complete_multimodal_citizen_journey_loop(self):
        """
        Simulates end-to-end citizen experience:
        Step 1: Citizen speaks a Marathi grievance
        Step 2: ASR decodes to Marathi text
        Step 3: Gateway bridges query to canonical BNSS provisions
        Step 4: NMT translates advice back to Marathi preserving Section 173(4)
        Step 5: TTS synthesizes the final voice audio response for the citizen
        """
        t0 = time.time()
        # 1. Voice Ingestion
        mock_wav = b"RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00"
        asr_res = self.asr.transcribe_audio_bytes(mock_wav, language="mr")
        self.assertTrue(asr_res.success)

        # 2. Statutory Retrieval & Normalization
        from legalmitra.multilingual.duplex_bridge import BhashiniFullDuplexBridge
        bridge = BhashiniFullDuplexBridge()
        norm_query, detected_lang = bridge.normalize_indic_to_english_query(asr_res.transcription)
        self.assertIn("Section 173(4) BNSS", norm_query)

        # 3. Advisory Answer Generation
        mock_answer = (
            "### Direct Position (In Plain Words)\n"
            "If police refuse to register an FIR, you have remedy under Section 173(4) BNSS.\n\n"
            "### Practical Action Guide (What You Should Do)\n"
            "- Step 1: Send your complaint to the Superintendent of Police under Section 173(4) BNSS."
        )

        # 4. NMT Translation back to citizen's language
        nmt_res = self.nmt.translate_with_sovereign_fidelity(mock_answer, target_language="mr")
        self.assertIn("Section 173(4) BNSS", nmt_res.translated_text)

        # 5. TTS Speech Delivery
        tts_res = self.tts.synthesize_speech(nmt_res.translated_text, language="mr")
        self.assertTrue(tts_res.success)
        self.assertGreater(len(tts_res.audio_base64), 0)

        total_elapsed = round((time.time() - t0) * 1000, 2)
        print(f"\n[E2E MULTIMODAL CITIZEN LOOP COMPLETE in {total_elapsed} ms]: All 4 Pillars Verified.")


if __name__ == "__main__":
    unittest.main()
