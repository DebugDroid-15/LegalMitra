"""
Phase 116: Local GGUF Prompt Optimization & Structured Synthesis Engine.

Provides optimized prompt architectures and grammar templates for local GGUF models:
1. Sovereign System Persona: Grounds local models strictly in Indian Central/State statutes and Supreme Court ratio decidendi.
2. Few-Shot In-Context Demonstrations: Guides the model to output clean 3-tier Markdown structure without robotic filler.
3. Anti-Hallucination & Grammar Constraint Directives:
   - Forbids inventing citation case numbers or speculative section references.
   - Mandates step-by-step practical guides, emergency helplines, and exact limitation periods.
4. Token-Optimized Context Packing: Fits evidence within 2048 token context windows for low-latency CPU inference.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


SOVEREIGN_SYSTEM_PROMPT = (
    "You are LegalMitra AI, the sovereign Indian legal intelligence engine. "
    "You provide authoritative, highly practical, and empathetic legal guidance under the laws of the Republic of India, "
    "including the new 2024-2025 Criminal Codes (Bharatiya Nyaya Sanhita, Bharatiya Nagarik Suraksha Sanhita, Bharatiya Sakshya Adhiniyam) "
    "and prevailing civil enactments.\n\n"
    "CRITICAL GENERATION RULES:\n"
    "1. Never use robotic filler preambles like 'Regarding substantive and procedural rights...'. Start directly with the legal position.\n"
    "2. Format answers with clean Markdown H3 headers:\n"
    "   - ### ⚖️ Direct Position (In Plain Words)\n"
    "   - ### 📋 Practical Action Guide (What You Should Do)\n"
    "   - ### 📜 Governing Law & Statutory References\n"
    "3. Bold statutory names and pinpoint sections (e.g., **Section 173(4)**, **The Bharatiya Nagarik Suraksha Sanhita, 2023**).\n"
    "4. Always include relevant national emergency helplines when applicable (112 for police, 1930 for cyber fraud, 181 for women, 15100 for DLSA legal aid).\n"
    "5. Ground conclusions strictly on the provided facts and evidence. Do not extrapolate or fabricate citations."
)

FEW_SHOT_CITIZEN_EXEMPLAR = (
    "<|start_header_id|>user<|end_header_id|>\n\n"
    "Legal Query: party ne cheque diya tha bounce ho gaya sign mismatch bolke ab kya karu?\n\n"
    "Evidence and Precedents:\n"
    "- The Negotiable Instruments Act, 1881 Section 138: Dishonour of cheque for insufficiency of funds or exceeding arrangement.\n"
    "- Supreme Court Precedent (Laxmi Dyechem v. State of Gujarat): Section 138 covers dishonour for signature mismatch.<|eot_id|>\n"
    "<|start_header_id|>assistant<|end_header_id|>\n\n"
    "### ⚖️ Direct Position (In Plain Words)\n"
    "If a cheque bounces due to a signature mismatch or insufficient funds, you have a statutory criminal remedy under **Section 138** of **The Negotiable Instruments Act, 1881**.\n\n"
    "### 📋 Practical Action Guide (What You Should Do)\n"
    "- **Step 1:** Collect the original bounced cheque and the Bank Return Memo showing 'Signature Differs'.\n"
    "- **Step 2:** Issue a formal Statutory Demand Notice in writing to the drawer within 30 days of receiving the memo, giving a mandatory 15-day cure period to pay.\n"
    "- **Step 3:** If unpaid within 15 days, file a Criminal Complaint before the Judicial Magistrate within 30 days thereafter.\n\n"
    "### 📜 Governing Law & Statutory References\n"
    "Under **Section 138** and Supreme Court ruling in *Laxmi Dyechem v. State of Gujarat*, dishonour on grounds of signature mismatch is fully prosecutable.<|eot_id|>"
)


class GGUFStructuredPromptBuilder:
    """
    Constructs token-optimized Llama-3.1 prompts with structured few-shot guidance.
    """

    @classmethod
    def build_optimized_prompt(
        cls,
        query: str,
        provisions: List[Dict[str, Any]],
        precedents: List[Dict[str, Any]],
        temporal_context: Optional[str] = None,
        dialogue_history: Optional[str] = None,
        include_few_shot: bool = True
    ) -> str:
        evidence_lines = []
        if temporal_context:
            evidence_lines.append(f"Temporal Context: {temporal_context}")

        if provisions:
            evidence_lines.append("Statutory Provisions:")
            for p in provisions[:4]:  # Top 4 provisions
                act = p.get("act", "Statute")
                sec = p.get("section", "")
                text = (p.get("text") or "")[:180]
                evidence_lines.append(f"- {act} {sec}: {text}".strip())

        if precedents:
            evidence_lines.append("Judicial Precedents:")
            for prec in precedents[:3]:  # Top 3 precedents
                title = prec.get("case_title", "Precedent")
                cit = prec.get("citation", "")
                ratio = (prec.get("ratio") or "")[:180]
                evidence_lines.append(f"- {title} ({cit}): {ratio}".strip())

        evidence_str = "\n".join(evidence_lines) if evidence_lines else "General Indian Statutory Framework applies."

        dialogue_block = f"Prior Conversation History:\n{dialogue_history}\n\n" if dialogue_history else ""

        user_content = (
            f"{dialogue_block}"
            f"Legal Query: {query}\n\n"
            f"Evidence and Precedents:\n{evidence_str}\n\n"
            f"Provide an authoritative, structured legal answer using the 3-tier format."
        )

        parts = [
            f"<|start_header_id|>system<|end_header_id|>\n\n{SOVEREIGN_SYSTEM_PROMPT}<|eot_id|>\n"
        ]

        if include_few_shot:
            parts.append(f"{FEW_SHOT_CITIZEN_EXEMPLAR}\n")

        parts.append(f"<|start_header_id|>user<|end_header_id|>\n\n{user_content}<|eot_id|>\n")
        parts.append("<|start_header_id|>assistant<|end_header_id|>\n\n")

        return "".join(parts)
