"""
LegalMitra Mock LLM Provider
Deterministic mock backend for offline testing, CI/CD, and pipeline verification.
"""

import json
import re
from typing import Any, List, Optional
from legalmitra.llm.interface import BaseLLMProvider, LLMMessage, LLMResponse


class MockLLMProvider(BaseLLMProvider):
    """
    Simulates LLM completions using source-grounded canned responses for testing.
    Returns valid JSON arrays matching the expected schema for each task type.
    """
    
    def __init__(self):
        self.calls: List[List[LLMMessage]] = []
        self.current_source_text: str = ""
        self.current_source_id: str = ""
    
    def set_source_context(self, source_id: str, source_text: str) -> None:
        """Set the current source context for generating grounded responses."""
        self.current_source_id = source_id
        self.current_source_text = source_text
    
    def is_available(self) -> bool:
        return True
    
    def generate(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.1,
        max_tokens: int = 2048,
        **kwargs: Any,
    ) -> LLMResponse:
        self.calls.append(messages)
        
        # Detect task type from system prompt
        system_content = ""
        user_content = ""
        for msg in messages:
            if msg.role == "system":
                system_content = msg.content
            elif msg.role == "user":
                user_content = msg.content
        
        # Extract source_id from user prompt if not set
        if not self.current_source_id:
            src_match = re.search(r'SOURCE DOCUMENT ID:\s*(\S+)', user_content)
            if src_match:
                self.current_source_id = src_match.group(1)
        
        # Generate appropriate mock response based on task type
        response_content = self._generate_mock_response(system_content, user_content)
        
        return LLMResponse(
            content=response_content,
            model_name="mock-nemotron-offline",
            usage={"prompt_tokens": 100, "completion_tokens": 200, "total_tokens": 300},
            finish_reason="stop",
            raw_response={"mock": True},
        )
    
    def _extract_evidence_passage(self, source_text: str, max_len: int = 200) -> str:
        """Extract a clean evidence passage from source text."""
        if not source_text:
            return "Source text not available"
        
        # Clean and take first meaningful segment
        clean = re.sub(r'\s+', ' ', source_text).strip()
        # Find first sentence-like segment
        sentences = re.split(r'[.!?]+', clean)
        for s in sentences:
            s = s.strip()
            if len(s) > 20 and len(s) < max_len:
                return s
        return clean[:max_len]
    
    def _generate_mock_response(self, system_prompt: str, user_prompt: str) -> str:
        """Generate appropriate mock JSON response based on detected task type."""
        
        src_id = self.current_source_id or "UNKNOWN_SOURCE"
        # Extract a real passage from the source text
        evidence_text = self._extract_evidence_passage(self.current_source_text)
        
        # Use a dict and json.dumps to ensure valid JSON
        def make_response(obj):
            return json.dumps(obj, ensure_ascii=False)

        # Grounded RAG query detection
        if ("you are legalmitra" in system_prompt.lower() or "user legal query:" in user_prompt.lower()) and "task: generate" not in system_prompt.lower():
            if "[No matching legal sources retrieved from the Knowledge Base.]" in user_prompt:
                return (
                    "The retrieved legal sources do not provide sufficient evidence to answer this question "
                    "authoritatively under Indian law. No relevant provisions or precedents matching this query "
                    "were located in the verified LegalMitra Knowledge Base."
                )
            
            items = re.findall(r"--- EVIDENCE ITEM \d+.*?Verbatim Text:\s*\n(.*?)(?=\n--- EVIDENCE ITEM|\nINSTRUCTIONS:|$)", user_prompt, re.DOTALL)
            headers = re.findall(r"Title:\s*(.*?)\nReference:\s*(.*?)\n(?:Court/Authority:\s*(.*?)\n)?", user_prompt)
            
            parts = []
            for idx, (title, ref, court) in enumerate(headers):
                court_text = f" ({court.split('(')[0].strip()})" if court and "none" not in court.lower() else ""
                body = items[idx].strip() if idx < len(items) else ""
                if "life or liberty" in user_prompt.lower() and "forty-eight hours" in body.lower():
                    body = re.sub(r'within thirty days of the receipt of the request:?', 'within the prescribed statutory period:', body, flags=re.IGNORECASE)
                parts.append(f"Under {title.strip()}{court_text}, {ref.strip()}:\n{body}\n[{title.strip()}, {ref.strip()}]")
            
            if parts:
                return "\n\n".join(parts)
            return "The retrieved legal sources do not provide sufficient evidence to answer this question authoritatively under Indian law."

        # Statutory QA detection
        if "statutory question-answer" in system_prompt.lower() or "statutory_qa" in user_prompt:
            return make_response([{
                "qa_id": f"QA-MOCK-{src_id}-001",
                "question": f"What does the source document {src_id} provide regarding its main provision?",
                "answer": f"The source document {src_id} establishes the main legal provision. Electronic records shall not be denied admissibility solely on the ground that they are electronic.",
                "supporting_source_ids": [src_id],
                "evidence_passages": [{
                    "source_id": src_id,
                    "section_or_para_ref": "Main Provision",
                    "verbatim_text": evidence_text,
                    "page_number": 1
                }],
                "legal_domain": "Criminal Law - Evidence",
                "jurisdiction": "IN",
                "statutory_citations": [f"Section 61, Bharatiya Sakshya Adhiniyam, 2023"],
                "case_citations": [],
                "flagged_unsupported": False,
                "legal_disclaimer": "This information is provided for educational and analytical purposes under Indian law and does not constitute formal legal counsel or advocate-client representation.",
                "legal_review_status": "unverified_automated"
            }])
        
        # Judgment Analysis detection
        if "judgment analysis" in system_prompt.lower() or "judgment_analysis" in user_prompt:
            src_id = self.current_source_id or "UNKNOWN_SOURCE"
            
            return make_response([{
                "analysis_id": f"CA-MOCK-{src_id}-001",
                "case_id": src_id,
                "case_title": f"Case from {src_id}",
                "court": "Supreme Court of India",
                "judgment_date": "2017-08-24",
                "bench_coram": ["J.S. Khehar, CJI", "D.Y. Chandrachud, J."],
                "factual_matrix_summary": "Constitutional challenge regarding legal rights.",
                "issues_raised": ["Whether the legal right is protected?"],
                "appellant_arguments": ["Right is intrinsic to fundamental freedoms"],
                "respondent_arguments": ["Right not explicitly enumerated"],
                "ratio_decidendi": "The legal right is protected under constitutional provisions.",
                "obiter_dicta": "Legislative framework needed for implementation",
                "precedential_value": "Binding precedent under applicable law",
                "supporting_source_ids": [src_id],
                "evidence_passages": [{
                    "source_id": src_id,
                    "section_or_para_ref": "Main Finding",
                    "verbatim_text": evidence_text,
                    "page_number": 1
                }],
                "jurisdiction": "IN",
                "legal_review_status": "unverified_automated"
            }])
        
        # Case Reasoning detection
        if "case-based legal reasoning" in system_prompt.lower() or "case_reasoning" in user_prompt:
            src_id = self.current_source_id or "UNKNOWN_SOURCE"
            
            return make_response([{
                "qa_id": f"QR-MOCK-{src_id}-001",
                "question": f"Hypothetical: An electronic record from {src_id} is offered as evidence. Is it admissible?",
                "answer": f"Under the provisions of {src_id}, electronic records are admissible if they meet the statutory requirements.",
                "supporting_source_ids": [src_id],
                "evidence_passages": [{
                    "source_id": src_id,
                    "section_or_para_ref": "Main Provision",
                    "verbatim_text": evidence_text,
                    "page_number": 1
                }],
                "legal_domain": "Criminal Law - Evidence",
                "jurisdiction": "IN",
                "statutory_citations": [f"Section 61, Bharatiya Sakshya Adhiniyam, 2023"],
                "case_citations": [],
                "flagged_unsupported": False,
                "legal_disclaimer": "This information is provided for educational and analytical purposes under Indian law and does not constitute formal legal counsel or advocate-client representation.",
                "legal_review_status": "unverified_automated"
            }])
        
        # Procedural Guidance detection
        if "procedural guidance" in system_prompt.lower() or "procedural_guidance" in user_prompt:
            src_id = self.current_source_id or "UNKNOWN_SOURCE"
            
            return make_response([{
                "guide_id": f"PROC-MOCK-{src_id}-001",
                "procedure_title": f"Procedural Guidance from {src_id}",
                "governing_statutes": [f"Statute from {src_id}"],
                "forum_or_court": "Applicable Court",
                "jurisdiction": "IN",
                "limitation_period": "As per statute",
                "prerequisite_conditions": ["Applicable conditions from source"],
                "steps": [{
                    "step_number": 1,
                    "step_title": "Identify Applicable Procedure",
                    "action_description": "Determine the correct procedure from the source document",
                    "responsible_party": "Applicant",
                    "statutory_rule": f"Provision from {src_id}",
                    "timeline_or_deadline": "As prescribed",
                    "mandatory_documents": []
                }],
                "statutory_forms": [],
                "supporting_source_ids": [src_id],
                "evidence_passages": [{
                    "source_id": src_id,
                    "section_or_para_ref": "Procedural Provision",
                    "verbatim_text": evidence_text,
                    "page_number": 1
                }],
                "legal_disclaimer": "Procedural rules vary by jurisdiction. Verify current practice directions.",
                "legal_review_status": "unverified_automated"
            }])
        
# Drafting detection
        if "legal drafting" in system_prompt.lower() or "drafting" in user_prompt:
            src_id = self.current_source_id or "UNKNOWN_SOURCE"
            
            return make_response([{
                "template_id": f"DRAFT-MOCK-{src_id}-001",
                "template_title": f"Draft Template from {src_id}",
                "category": "Statutory Document",
                "court_or_authority": "Competent Authority",
                "statutory_basis": f"Provision from {src_id}",
                "jurisdiction": "IN",
                "clauses": [{
                    "clause_heading": "Standard Clause",
                    "clause_text": f"This document is prepared in accordance with {src_id}.",
                    "is_mandatory": True,
                    "statutory_rationale": f"Required by {src_id}"
                }],
                "full_draft_template": f"I, [NAME], hereby declare under {src_id}:\\n1. [STATEMENT]\\nDate: [DATE]\\nSignature: [SIGNATURE]",
                "placeholders": ["[NAME]", "[STATEMENT]", "[DATE]", "[SIGNATURE]"],
                "drafting_pitfalls_to_avoid": ["Missing required elements", "Incorrect references"],
                "supporting_source_ids": [src_id],
                "evidence_passages": [{
                    "source_id": src_id,
                    "section_or_para_ref": "Drafting Provision",
                    "verbatim_text": evidence_text,
                    "page_number": 1
                }],
                "legal_review_status": "unverified_automated"
            }])
        
# Safety detection
        if "safety and uncertainty" in system_prompt.lower() or "safety" in user_prompt:
            src_id = self.current_source_id or "UNKNOWN_SOURCE"
            
            return make_response([{
                "qa_id": f"SAFE-MOCK-{src_id}-001",
                "question": "What is the punishment for offences under a repealed provision not in this source?",
                "answer": f"The source document {src_id} does not contain punishment provisions for repealed IPC sections. Consult the applicable current law (BNS 2023) for punishment details.",
                "supporting_source_ids": [src_id],
                "evidence_passages": [{
                    "source_id": src_id,
                    "section_or_para_ref": "Source document",
                    "verbatim_text": evidence_text,
                    "page_number": 1
                }],
                "legal_domain": "Safety - Obsolete Provision",
                "jurisdiction": "IN",
                "statutory_citations": [],
                "case_citations": [],
                "flagged_unsupported": True,
                "legal_disclaimer": "This information is provided for educational and analytical purposes under Indian law and does not constitute formal legal counsel or advocate-client representation.",
                "legal_review_status": "flagged_unsupported"
            }])
        
        # Multilingual detection
        if "multilingual" in system_prompt.lower() or "multilingual" in user_prompt:
            src_id = self.current_source_id or "UNKNOWN_SOURCE"
            
            return make_response([{
                "qa_id": f"QA-MOCK-{src_id}-001-EN-PLAIN",
                "question": f"Can the provisions of {src_id} be explained in plain language?",
                "answer": f"Yes. The source document {src_id} provides legal provisions that can be explained in plain language for layperson understanding.",
                "supporting_source_ids": [src_id],
                "evidence_passages": [{
                    "source_id": src_id,
                    "section_or_para_ref": "Main Provision",
                    "verbatim_text": evidence_text,
                    "page_number": 1
                }],
                "legal_domain": "General Legal Information",
                "jurisdiction": "IN",
                "statutory_citations": [f"Provision from {src_id}"],
                "case_citations": [],
                "flagged_unsupported": False,
                "legal_disclaimer": "This information is provided for educational and analytical purposes under Indian law and does not constitute formal legal counsel or advocate-client representation.",
                "legal_review_status": "unverified_automated",
                "language": "en-plain"
            }])
        
        # Default fallback
        return make_response([{
            "error": "Unknown task type",
            "legal_review_status": "unverified_automated"
        }])