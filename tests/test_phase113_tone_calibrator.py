"""
Unit tests for Phase 113: Response Formatting & Cognitive Tone Calibration.
"""

import pytest
from legalmitra.orchestration.tone_calibrator import ResponseFormatToneCalibrator


class TestPhase113ToneCalibrator:
    def test_strip_robotic_preamble(self):
        raw_text = (
            "Regarding Substantive and procedural rights governing 'how can you help me...' under Indian law:\n"
            "- 1. Review all primary agreements.\n"
            "Direct Position:\n"
            "Under The Bharatiya Nagarik Suraksha Sanhita, 2023, Section 150, the governing legal standard is: ..."
        )
        calibrated = ResponseFormatToneCalibrator.calibrate_prose(raw_text)
        assert "Regarding Substantive and procedural rights" not in calibrated
        assert "the governing legal standard is:" not in calibrated
        assert "### ⚖️ Direct Position" in calibrated
        assert "**The Bharatiya Nagarik Suraksha Sanhita, 2023**" in calibrated
        assert "**Section 150**" in calibrated

    def test_header_icon_standardization(self):
        raw_text = (
            "Direct Position (In Plain Words)\n"
            "You have full legal remedies.\n\n"
            "Practical Action Guide (What You Should Do)\n"
            "- Step 1: Send a notice.\n\n"
            "Governing Law & Statutory References\n"
            "Section 138 applies."
        )
        calibrated = ResponseFormatToneCalibrator.calibrate_prose(raw_text)
        assert "### ⚖️ Direct Position (In Plain Words)" in calibrated
        assert "### 📋 Practical Action Guide (What You Should Do)" in calibrated
        assert "### 📜 Governing Law & Statutory References" in calibrated
        assert "**Section 138**" in calibrated

    def test_cyber_fraud_callout_injection(self):
        raw_text = (
            "Direct Position (In Plain Words)\n"
            "Your money was stolen via unauthorized cyber fraud.\n\n"
            "Practical Action Guide (What You Should Do)\n"
            "- Step 1: Call 1930 immediately.\n"
        )
        calibrated = ResponseFormatToneCalibrator.calibrate_prose(raw_text)
        assert "> [!IMPORTANT]" in calibrated
        assert "Golden Hour Cyber Alert" in calibrated
        assert "**1930**" in calibrated
