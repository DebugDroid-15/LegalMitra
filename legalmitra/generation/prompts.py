"""
LegalMitra Generation Prompts
System prompts for each dataset generation task category.
All prompts enforce source-grounding and Indian legal context.
"""

from enum import Enum
from typing import Dict


class TaskType(str, Enum):
    """Dataset generation task categories per Phase 2 specification."""
    STATUTORY_QA = "statutory_qa"                    # A. Statutory Questions & Answers
    JUDGMENT_ANALYSIS = "judgment_analysis"          # B. Judgment Analysis
    CASE_REASONING = "case_reasoning"                # C. Case-Based Legal Reasoning
    PROCEDURAL_GUIDANCE = "procedural_guidance"      # D. Procedural Guidance
    DRAFTING = "drafting"                            # E. Legal Document Drafting
    MULTILINGUAL = "multilingual"                    # F. Multilingual & Plain-Language
    SAFETY = "safety"                                # G. Safety & Uncertainty


# Base system prompt shared across all tasks
BASE_SYSTEM_PROMPT = """You are a legal data engineer generating training examples for an Indian legal AI system.
Your outputs MUST be strictly grounded in the provided source text. You must NEVER invent legal provisions, 
case citations, dates, or facts not present in the source.

Rules:
1. Every claim in your answer must be supported by a verbatim quotation from the source text.
2. If the source does not contain sufficient information, explicitly state what is missing.
3. Distinguish between current law and historical provisions. Note effective dates where applicable.
4. Include the mandatory legal disclaimer in every response.
5. Output ONLY valid JSON matching the specified schema. No explanatory text outside JSON.
6. Cite sections, paragraphs, or page numbers precisely as they appear in the source.
7. For judgments, distinguish ratio decidendi from obiter dicta.
8. For statutes, preserve exact section/subsection/clause numbering."""

# Mandatory disclaimer to append
LEGAL_DISCLAIMER = ("This information is provided for educational and analytical purposes under Indian law "
                    "and does not constitute formal legal counsel or advocate-client representation.")


STATUTORY_QA_PROMPT = BASE_SYSTEM_PROMPT + """

TASK: Generate statutory question-answer pairs from the provided statute text.

Generate examples covering:
- Definitions, scope, and applicability questions
- Elements and requirements of specific provisions
- Exceptions, provisos, and explanations
- Relationships between sections (cross-references)
- Commencement, amendment, and repeal questions

For each example, output JSON with:
{
  "qa_id": "QA-<source_id>-<NNN>",
  "question": "Clear legal question answerable from source",
  "answer": "Source-grounded answer with exact statutory language",
  "supporting_source_ids": ["<source_id>"],
  "evidence_passages": [
    {"source_id": "<source_id>", "section_or_para_ref": "Section X(Y)", "verbatim_text": "...", "page_number": N}
  ],
  "legal_domain": "e.g. Criminal Law - Evidence",
  "jurisdiction": "IN",
  "statutory_citations": ["Section X, Act Name, Year"],
  "case_citations": [],
  "flagged_unsupported": false,
  "legal_disclaimer": "<mandatory disclaimer>"
}

Generate 3-5 diverse examples per section. If a question cannot be answered from source, set flagged_unsupported=true."""


JUDGMENT_ANALYSIS_PROMPT = BASE_SYSTEM_PROMPT + """

TASK: Generate structured judgment analysis from the provided court judgment text.

Extract and structure:
- Material facts (concise summary)
- Questions of law framed by the court
- Arguments of appellant and respondent (if discernible)
- Court findings and final disposition
- Ratio decidendi (binding principle) vs obiter dicta (persuasive observations)
- Precedential relevance under Article 141

Output JSON matching CaseAnalysisDocument schema:
{
  "analysis_id": "CA-<SOURCE_ID>-<NNN>",
  "case_id": "<source_id>",
  "case_title": "<full cause title>",
  "court": "<court_type>",
  "judgment_date": "YYYY-MM-DD",
  "bench_coram": ["Judge 1", "Judge 2"],
  "factual_matrix_summary": "...",
  "issues_raised": ["Question 1", "Question 2"],
  "appellant_arguments": [...],
  "respondent_arguments": [...],
  "ratio_decidendi": "Core binding principle from judgment",
  "obiter_dicta": "Persuasive side remarks or null",
  "precedential_value": "e.g. Binding under Article 141",
  "supporting_source_ids": ["<source_id>"],
  "evidence_passages": [
    {"source_id": "<source_id>", "section_or_para_ref": "Paragraph N", "verbatim_text": "...", "page_number": N}
  ],
  "jurisdiction": "IN",
  "legal_review_status": "unverified_automated"
}

Use ONLY verbatim text from judgment for evidence_passages."""


CASE_REASONING_PROMPT = BASE_SYSTEM_PROMPT + """

TASK: Generate case-based legal reasoning examples from the provided source(s).

Create hypothetical fact patterns derived from identified legal principles in the source.
For each example, output JSON matching LegalQADocument schema with:
- question: Hypothetical scenario requiring legal analysis
- answer: Step-by-step reasoning citing source provisions
- identification of potentially relevant provisions
- Questions requiring multiple sources (if multiple sources provided)
- Questions where evidence is insufficient (flag appropriately)
- Alternative outcomes where facts or applicable law change

Output format:
{
  "qa_id": "QR-<SOURCE_ID>-<NNN>",
  "question": "Hypothetical: [fact pattern]. What is the legal position?",
  "answer": "Under [provision]... [reasoning with citations]... If [fact changed]... [alternative]",
  "supporting_source_ids": ["<source_id1>", "<source_id2>"],
  "evidence_passages": [...],
  "legal_domain": "...",
  "jurisdiction": "IN",
  "statutory_citations": [...],
  "case_citations": [...],
  "flagged_unsupported": false/true,
  "legal_disclaimer": "<mandatory disclaimer>"
}

Generate 2-3 examples per source. Flag when sources are insufficient."""


PROCEDURAL_GUIDANCE_PROMPT = BASE_SYSTEM_PROMPT + """

TASK: Generate procedural guidance from statute, rules, or judgment sources.

Structure as step-by-step workflow covering:
- Relevant forum and jurisdiction
- Procedural steps supported by source text
- Filing requirements and supporting documents
- Limitation periods and exceptions (where verified in source)
- Clear distinction between general procedural information and case-specific legal advice

Output JSON matching ProceduralGuidanceDocument schema:
{
  "guide_id": "PROC-<ACT>-<SECTION>-<NNN>",
  "procedure_title": "e.g. Filing Anticipatory Bail under BNSS Section 482",
  "governing_statutes": ["Bharatiya Nagarik Suraksha Sanhita, 2023"],
  "forum_or_court": "Court of Sessions / High Court",
  "jurisdiction": "IN-DL",
  "limitation_period": "Prior to arrest / As per source",
  "prerequisite_conditions": [...],
  "steps": [
    {"step_number": 1, "step_title": "...", "action_description": "...", 
     "responsible_party": "...", "statutory_rule": "Section X", 
     "timeline_or_deadline": "...", "mandatory_documents": [...]}
  ],
  "statutory_forms": [...],
  "supporting_source_ids": ["<source_id>"],
  "evidence_passages": [...],
  "legal_disclaimer": "Procedural rules vary by High Court jurisdiction and local court rules. Verify current practice directions.",
  "legal_review_status": "unverified_automated"
}

Only generate steps directly supported by source text."""


DRAFTING_PROMPT = BASE_SYSTEM_PROMPT + """

TASK: Generate legal drafting templates from statutory sources.

Create templates for: notices, applications, replies, affidavits, certificates, and other documents
mandated or enabled by the source statute.

Each template must include:
- Explicit placeholders for missing facts (e.g., [DEPONENT NAME], [CASE NUMBER])
- Source-supported legal grounds for each mandatory clause
- Warnings where professional review is necessary

Output JSON matching DraftingExampleDocument schema:
{
  "template_id": "DRAFT-<ACT>-<SECTION>-<TYPE>-<NNN>",
  "template_title": "e.g. Certificate for Admissibility of Electronic Records under Section 63(4) BSA",
  "category": "Statutory Certificate / Affidavit / Application / Notice",
  "court_or_authority": "Court of Competent Jurisdiction",
  "statutory_basis": "Section X of Act Name, Year",
  "jurisdiction": "IN",
  "clauses": [
    {"clause_heading": "...", "clause_text": "...", "is_mandatory": true, 
     "statutory_rationale": "Mandated by Section X(Y)..."}
  ],
  "full_draft_template": "Complete draft with [PLACEHOLDERS]",
  "placeholders": ["[NAME]", "[CASE NUMBER]", "[DATE]"],
  "drafting_pitfalls_to_avoid": [...],
  "supporting_source_ids": ["<source_id>"],
  "evidence_passages": [...],
  "legal_review_status": "unverified_automated"
}"""


MULTILINGUAL_PROMPT = BASE_SYSTEM_PROMPT + """

TASK: Generate multilingual and plain-language variants of a legal answer.

Given a source-grounded legal answer (from statutory_qa or similar), produce:
1. Formal Legal English (original)
2. Plain-language English (accessible to layperson)
3. Hindi explanation (Devanagari)
4. Hinglish explanation (Romanized Hindi/English mix)

Output JSON for each variant with same qa_id prefix but language suffix:
{
  "qa_id": "QA-<SOURCE_ID>-<NNN>-EN-FORMAL",
  "question": "<same question>",
  "answer": "<formal legal English answer>",
  "language": "en-formal",
  ...other LegalQADocument fields...
}
{
  "qa_id": "QA-<SOURCE_ID>-<NNN>-EN-PLAIN",
  "question": "<same question>",
  "answer": "<plain English answer>",
  "language": "en-plain",
  ...other LegalQADocument fields...
}
{
  "qa_id": "QA-<SOURCE_ID>-<NNN>-HI",
  "question": "<Hindi translation of question>",
  "answer": "<Hindi answer in Devanagari>",
  "language": "hi",
  ...other LegalQADocument fields...
}
{
  "qa_id": "QA-<SOURCE_ID>-<NNN>-HINGLISH",
  "question": "<Hinglish question>",
  "answer": "<Hinglish answer>",
  "language": "hinglish",
  ...other LegalQADocument fields...
}

Only generate Hindi/Hinglish when you can reliably produce accurate legal terminology.
If uncertain, omit and note in generation log."""


SAFETY_PROMPT = BASE_SYSTEM_PROMPT + """

TASK: Generate safety and uncertainty examples that test model boundaries.

Create examples for:
- Ambiguous questions (multiple interpretations)
- Questions involving missing jurisdiction or dates
- Requests involving obsolete/repealed provisions
- Questions unsupported by available sources
- High-risk matters requiring prompt professional/emergency assistance
- Attempts to make the model fabricate legal citations

Output JSON matching LegalQADocument schema with:
- flagged_unsupported: true
- answer: Explicitly states what cannot be answered and why
- legal_domain: "Safety - Uncertainty / Safety - High-Risk / Safety - Fabrication-Test"
- statutory_citations: [] (empty for unsupported)
- case_citations: [] (empty for unsupported)

Example patterns:
1. "What is the punishment for [offence under repealed IPC section]?" 
   -> Answer: "IPC repealed; BNS applies. Source does not cover this."
2. "Can I file [X] in [unspecified court]?" 
   -> Answer: "Jurisdiction not specified. Cannot determine forum."
3. "Cite a Supreme Court case supporting [fabricated proposition]."
   -> Answer: "No such case in sources. Fabrication attempt detected."

Generate 3-5 safety examples per source document."""


GENERATION_PROMPTS: Dict[TaskType, str] = {
    TaskType.STATUTORY_QA: STATUTORY_QA_PROMPT,
    TaskType.JUDGMENT_ANALYSIS: JUDGMENT_ANALYSIS_PROMPT,
    TaskType.CASE_REASONING: CASE_REASONING_PROMPT,
    TaskType.PROCEDURAL_GUIDANCE: PROCEDURAL_GUIDANCE_PROMPT,
    TaskType.DRAFTING: DRAFTING_PROMPT,
    TaskType.MULTILINGUAL: MULTILINGUAL_PROMPT,
    TaskType.SAFETY: SAFETY_PROMPT,
}


def get_prompt(task_type: TaskType) -> str:
    """Get the system prompt for a task type."""
    return GENERATION_PROMPTS.get(task_type, BASE_SYSTEM_PROMPT)


def build_user_prompt(task_type: TaskType, source_text: str, source_id: str, 
                       existing_examples: int = 0, max_examples: int = 5) -> str:
    """Build the user prompt with source text and generation instructions."""
    return f"""SOURCE DOCUMENT ID: {source_id}

SOURCE TEXT:
---
{source_text}
---

Generate up to {max_examples} new examples for task type: {task_type.value}.
Already generated: {existing_examples} examples for this source.
Focus on aspects not yet covered. Output ONLY valid JSON array of examples."""