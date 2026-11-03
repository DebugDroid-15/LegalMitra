"""
Phase 89: AI Kosh Multi-Task Legal Instruction Dataset Generator
Synthesizes gold-standard instruction-tuning datasets across 5 core legal tasks:
1. STATUTE_SIMPLIFICATION: Translates complex legalese into plain-language citizen guidance.
2. PROCEDURAL_ROADMAP: Outlines two-tier statutory remedies, filings, caveats, and timelines.
3. TRI_CODE_CROSSWALK: Crosswalks provisions between IPC/CrPC/IEA and BNS/BNSS/BSA.
4. RATIO_EXTRACTION: Extracts binding principles, bench coram, and distinctions from case law.
5. NON_ADVISORY_GUARDRAIL: Rejects outcome guarantees ("You will win") and provides emergency helpline referrals.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger("aikosh_instruction_generator")


class LegalTaskType(str, Enum):
    STATUTE_SIMPLIFICATION = "statute_simplification"
    PROCEDURAL_ROADMAP = "procedural_roadmap"
    TRI_CODE_CROSSWALK = "tri_code_crosswalk"
    RATIO_EXTRACTION = "ratio_extraction"
    NON_ADVISORY_GUARDRAIL = "non_advisory_guardrail"


@dataclass
class MultiTaskInstructionPair:
    instruction_id: str
    task_type: LegalTaskType
    system_prompt: str
    instruction: str
    input_context: str
    chosen_response: str
    rejected_response: str  # For DPO (Direct Preference Optimization) training
    statutory_citations: List[str] = field(default_factory=list)
    court_citations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["task_type"] = self.task_type.value
        return d


class AIKoshDatasetGenerator:
    """
    Generates multi-task instruction and preference pairs for fine-tuning the AI Kosh Model.
    """

    SYSTEM_LEGAL_EXPERT = (
        "You are LegalMitra, an authoritative sovereign Indian Legal Assistant developed in accordance "
        "with the Bar Council of India guidelines and the Bharatiya Nyaya Sanhita, 2023. You provide "
        "source-grounded, plain-language legal explanations with exact statutory and precedent citations. "
        "You never guarantee litigation outcomes or provide unauthorized advocate advice."
    )

    def generate_core_dataset(self) -> List[MultiTaskInstructionPair]:
        dataset: List[MultiTaskInstructionPair] = [
            # 1. STATUTE_SIMPLIFICATION (Section 316 BNS)
            MultiTaskInstructionPair(
                instruction_id="AIKOSH-INST-001",
                task_type=LegalTaskType.STATUTE_SIMPLIFICATION,
                system_prompt=self.SYSTEM_LEGAL_EXPERT,
                instruction="Explain the offence of Criminal Breach of Trust under the Bharatiya Nyaya Sanhita, 2023 in simple terms.",
                input_context="Section 316 BNS provides that whoever being entrusted with property dishonestly misappropriates it commits criminal breach of trust.",
                chosen_response=(
                    "Criminal Breach of Trust (Section 316 BNS, erstwhile Section 405 IPC) occurs when you entrust someone with "
                    "property or money, and they later dishonestly misappropriate it, convert it to their own use, or dispose of it "
                    "in violation of law or legal agreement.\n\n"
                    "**Essential Ingredients:**\n"
                    "1. Entrustment of property or control over property.\n"
                    "2. Dishonest intention formed subsequently at the time of conversion.\n\n"
                    "**Distinction from Cheating (Section 318 BNS):**\n"
                    "In Criminal Breach of Trust, the initial receipt of property is lawful and innocent; the dishonest intention "
                    "arises later. In Cheating, the dishonest intention exists right from the very beginning.\n\n"
                    "*(Primary Authority: Section 316 BNS; Chelloor Mankkal v. State of Travancore-Cochin 1952 SCR 219)*"
                ),
                rejected_response=(
                    "Criminal breach of trust means cheating someone who trusted you. You can file a case directly and put them in jail for 5 years."
                ),
                statutory_citations=["Section 316 BNS", "Section 405 IPC"],
                court_citations=["(1952) SCR 219"]
            ),

            # 2. PROCEDURAL_ROADMAP (FIR Refusal under BNSS)
            MultiTaskInstructionPair(
                instruction_id="AIKOSH-INST-002",
                task_type=LegalTaskType.PROCEDURAL_ROADMAP,
                system_prompt=self.SYSTEM_LEGAL_EXPERT,
                instruction="What step-by-step remedies are available if the local police station refuses to register my FIR for a cognizable crime?",
                input_context="Police station refuses to register FIR regarding vehicle theft.",
                chosen_response=(
                    "If the Officer-in-Charge of a police station refuses to register an FIR regarding a cognizable offence, "
                    "the law provides a structured two-tier statutory remedy under the Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS):\n\n"
                    "**Tier 1: Representation to Superintendent of Police (Section 173(4) BNSS):**\n"
                    "- Submit the substance of your complaint in writing by registered post or speed post to the Superintendent of Police (SP/DCP).\n"
                    "- Keep postal receipts and tracking acknowledgment as documentary proof.\n"
                    "- The SP may investigate personally or direct a subordinate officer to investigate.\n\n"
                    "**Tier 2: Judicial Magistrate Application (Section 175(3) BNSS):**\n"
                    "- If the SP fails to act, you may file an application before the Judicial Magistrate.\n"
                    "- **Mandatory Requirement:** As ruled in *Priyanka Srivastava v. State of U.P. (2015) 6 SCC 287* and codified in Section 175(3), "
                    "your application must be accompanied by an affidavit stating that Tier 1 remedies were exhausted.\n\n"
                    "*(Primary Authority: Sections 173(4) & 175(3) BNSS, 2023)*"
                ),
                rejected_response=(
                    "Go to the High Court immediately and file a writ petition under Article 226 to suspend the police officer."
                ),
                statutory_citations=["Section 173(4) BNSS", "Section 175(3) BNSS"],
                court_citations=["(2015) 6 SCC 287"]
            ),

            # 3. TRI_CODE_CROSSWALK (Temporal Law & Pre-2024 Cheating)
            MultiTaskInstructionPair(
                instruction_id="AIKOSH-INST-003",
                task_type=LegalTaskType.TRI_CODE_CROSSWALK,
                system_prompt=self.SYSTEM_LEGAL_EXPERT,
                instruction="A business partner cheated me of funds in March 2024. Which criminal code applies: IPC or BNS?",
                input_context="Alleged cheating occurred on 15 March 2024. Complaint filed in November 2024.",
                chosen_response=(
                    "Under **Article 20(1) of the Constitution of India** (fundamental protection against ex post facto criminal laws) "
                    "and **Section 531(2)(a) of the BNSS, 2023**, substantive criminal offences are governed by the law in force on the date "
                    "the alleged act was committed.\n\n"
                    "1. **Substantive Offence (IPC Governed):**\n"
                    "Since the incident occurred on **15 March 2024** (prior to the 1 July 2024 commencement date of BNS), the offence "
                    "is substantively governed by **Section 420 of the Indian Penal Code, 1860** (Cheating and dishonestly inducing delivery of property).\n\n"
                    "2. **Equivalent New Provision:**\n"
                    "The corresponding successor provision in the modern code is **Section 318(4) of the Bharatiya Nyaya Sanhita, 2023 (BNS)**.\n\n"
                    "3. **Procedure (CrPC Savings):**\n"
                    "Proceedings and investigations instituted in respect of pre-July 2024 offences continue under the Code of Criminal Procedure, 1973 "
                    "as if BNSS had not come into force.\n\n"
                    "*(Primary Authority: Article 20(1) Constitution; Section 531 BNSS; MHA Notification S.O. 848(E))*)"
                ),
                rejected_response=(
                    "The new law BNS came on July 1st, so IPC is completely dead. You must only file under Section 318 BNS or your case will be rejected."
                ),
                statutory_citations=["Section 420 IPC", "Section 318(4) BNS", "Section 531 BNSS", "Article 20(1) Constitution"],
                court_citations=[]
            ),

            # 4. RATIO_EXTRACTION (Arnesh Kumar Arrest Guidelines)
            MultiTaskInstructionPair(
                instruction_id="AIKOSH-INST-004",
                task_type=LegalTaskType.RATIO_EXTRACTION,
                system_prompt=self.SYSTEM_LEGAL_EXPERT,
                instruction="What is the binding ratio decidendi of Arnesh Kumar v. State of Bihar regarding arrest powers?",
                input_context="Supreme Court judgment in Arnesh Kumar v. State of Bihar (2014) 8 SCC 273.",
                chosen_response=(
                    "In *Arnesh Kumar v. State of Bihar (2014) 8 SCC 273*, a Division Bench of the Supreme Court of India "
                    "(Coram: Chandramauli Kr. Prasad and Pinaki Chandra Ghose, JJ.) laid down mandatory safeguards against arbitrary arrest:\n\n"
                    "1. **No Automatic Arrest:** Police officers cannot mechanically arrest an accused merely because an FIR has been registered "
                    "under an offence carrying imprisonment up to 7 years (such as Section 498A IPC / Section 85 BNS).\n"
                    "2. **Checklist Requirement:** The arresting officer must record reasoned satisfaction on all parameters specified in "
                    "Section 41 CrPC (now Section 35 BNSS) before executing an arrest.\n"
                    "3. **Magisterial Oversight:** A Magistrate authorizing detention must independently examine the police checklist and record "
                    "reasoned satisfaction. Failure to do so renders the Magistrate liable to High Court departmental disciplinary proceedings.\n\n"
                    "*(Primary Citation: (2014) 8 SCC 273; Section 35 BNSS)*"
                ),
                rejected_response=(
                    "Arnesh Kumar means police can never arrest anyone for domestic violence cases ever."
                ),
                statutory_citations=["Section 35 BNSS", "Section 41 CrPC"],
                court_citations=["(2014) 8 SCC 273"]
            ),

            # 5. NON_ADVISORY_GUARDRAIL (Outcome Guarantee Rejection & 1930 Cyber Helpline)
            MultiTaskInstructionPair(
                instruction_id="AIKOSH-INST-005",
                task_type=LegalTaskType.NON_ADVISORY_GUARDRAIL,
                system_prompt=self.SYSTEM_LEGAL_EXPERT,
                instruction="I got scammed of 50,000 rupees on UPI an hour ago. Can you guarantee that I will get my money back?",
                input_context="Citizen urgent cyber financial fraud inquiry.",
                chosen_response=(
                    "**Immediate Action Required (Golden Hour Protocol):**\n"
                    "1. **Call 1930 Helpline Immediately:** Dial the National Cyber Crime Reporting Portal helpline **1930** right now "
                    "or submit a complaint on `cybercrime.gov.in`. If reported promptly, authorities can freeze or put a temporary lien on the fraudster's bank account.\n"
                    "2. **Contact Your Bank:** Immediately request your bank to block the affected UPI ID / card and dispute the transaction with transaction UTR numbers.\n\n"
                    "**Important Legal Notice:**\n"
                    "No legal intelligence system or advocate can guarantee a 100% recovery outcome, as financial restitution depends on the "
                    "speed of police lien notices and whether funds have already been liquidated.\n\n"
                    "*(Emergency Resource: Citizen Financial Cyber Fraud Reporting System - Helpline 1930)*"
                ),
                rejected_response=(
                    "Yes, don't worry at all! Under the Consumer Protection Act you are guaranteed 100% full refund with 18% interest within 30 days."
                ),
                statutory_citations=["Information Technology Act, 2000"],
                court_citations=[]
            )
        ]
        return dataset

    def export_dataset_jsonl(self, output_path: Union[str, Path]) -> int:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        dataset = self.generate_core_dataset()
        with open(path, "w", encoding="utf-8") as f:
            for item in dataset:
                f.write(json.dumps(item.to_dict(), ensure_ascii=False) + "\n")
        logger.info(f"Exported {len(dataset)} multi-task instruction pairs to {path}")
        return len(dataset)
