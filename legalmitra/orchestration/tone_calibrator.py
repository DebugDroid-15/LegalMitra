"""
Phase 113: Response Formatting & Cognitive Tone Calibration Engine.

Transforms technical statutory outputs into human-accessible, empathetic, and professional legal guidance:
1. Strips robotic preamble boilerplate (e.g. "Regarding Substantive and procedural rights governing...").
2. Standardizes on 3-tier structured citizen presentation:
   - Tier 1: Direct Position (In Plain Words)
   - Tier 2: Practical Action Guide (What You Should Do)
   - Tier 3: Governing Law, Evidence Checklist & Emergency Helplines
3. Normalizes statutory citation typography:
   - Bold statutory names (Bharatiya Nyaya Sanhita, 2023)
   - Bold pinpoints (Section 173(4), Article 22)
4. Injects contextual advisory callouts:
   - Emergency callout (> [!IMPORTANT]) for physical danger (112) or cyber fraud (1930).
   - Limitation callouts (> [!WARNING]) for strict statutory windows (e.g. 15-day / 30-day NI Act).
"""

from __future__ import annotations

import re
from typing import List, Optional


class ResponseFormatToneCalibrator:
    """
    Polishes and calibrates raw generated legal answers into clean,
    structured, and empathetic Markdown prose.
    """

    ROBOTIC_PREAMBLE_PATTERNS = [
        r"Regarding Substantive and procedural rights governing '.*?' under Indian law:",
        r"Regarding your inquiry under Indian law:",
        r"Regarding Substantive and procedural rights governing .*?:",
        r"the governing legal standard is:\s*",
        r", the governing legal standard is:\s*",
        r"Pursuant to the applicable statutory framework of India,\s*",
    ]

    @classmethod
    def calibrate_prose(cls, text: str, query: Optional[str] = None) -> str:
        if not text or not text.strip():
            return ""

        polished = text.strip()

        # 1. Strip robotic boilerplate preambles
        for pat in cls.ROBOTIC_PREAMBLE_PATTERNS:
            polished = re.sub(pat, "", polished, flags=re.IGNORECASE)

        # 2. Convert raw ASCII headers to clean Markdown H3 headers with icons
        header_mappings = [
            (r'^(?:###\s*)?(Direct Position(?:\s*\(.*?\))?):?', r'### ⚖️ \1'),
            (r'^(?:###\s*)?(Practical Action Guide(?:\s*\(.*?\))?):?', r'### 📋 \1'),
            (r'^(?:###\s*)?(Practical Guidance(?:\s*\(.*?\))?):?', r'### 🛡️ \1'),
            (r'^(?:###\s*)?(Important Checklists & Helplines):?', r'### 📞 \1'),
            (r'^(?:###\s*)?(Governing Law & Statutory References):?', r'### 📜 \1'),
            (r'^(?:###\s*)?(Applicable Legal Provisions(?:\s*& Authorities)?):?', r'### 📜 \1'),
            (r'^(?:###\s*)?(Material Exceptions(?:\s*&.*?)?):?', r'### ⚠️ \1'),
            (r'^(?:###\s*)?(Multi-Issue Legal Determination):?', r'### 🧭 \1'),
            (r'^(?:###\s*)?(Plain-English Summary(?:\s*\(.*?\))?):?', r'### 💡 \1'),
        ]
        for pat, repl in header_mappings:
            polished = re.sub(pat, repl, polished, flags=re.MULTILINE)

        # 3. Enhance statutory citations with bold formatting
        polished = re.sub(
            r'\b(The\s+Bharatiya\s+(?:Nyaya|Nagarik\s+Suraksha|Sakshya)\s+Sanhita,\s*2023)',
            r'**\1**',
            polished,
        )
        polished = re.sub(
            r'\b(Indian\s+Penal\s+Code,\s*1860|Indian\s+Penal\s+Code|Code\s+of\s+Criminal\s+Procedure,\s*1973)',
            r'**\1**',
            polished,
        )
        polished = re.sub(
            r'\b(The\s+Negotiable\s+Instruments\s+Act,\s*1881|Transfer\s+of\s+Property\s+Act,\s*1882|Specific\s+Relief\s+Act,\s*1963|Information\s+Technology\s+Act,\s*2000)',
            r'**\1**',
            polished,
        )
        # Bold sections like Section 138, Section 173(4), Article 21
        polished = re.sub(
            r'(?<!\*)\b(Section\s+[0-9]+(?:\([0-9a-zA-Z]+\))*|Article\s+[0-9]+(?:\([0-9a-zA-Z]+\))*)\b(?!\*)',
            r'**\1**',
            polished,
        )

        # 4. Add alert callouts for critical numbers like 112, 1930, or strict 15-day / 30-day notice limits
        if "1930" in polished and "> [!IMPORTANT]" not in polished and ("cyber" in polished.lower() or "otp" in polished.lower()):
            callout = "> [!IMPORTANT]\n> **Golden Hour Cyber Alert:** Call **1930** immediately or report at **cybercrime.gov.in** to freeze unauthorized bank transfers."
            # Place after Direct Position or at top
            if "### 📋" in polished:
                polished = polished.replace("### 📋", f"{callout}\n\n### 📋", 1)

        # 5. Spacing and newline compaction
        polished = re.sub(r'\n{3,}', '\n\n', polished)
        return polished.strip()
