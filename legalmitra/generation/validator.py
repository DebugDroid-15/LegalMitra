"""
LegalMitra Generation Validator
Validates LLM-generated outputs against schemas and grounding requirements.
"""

import json
import re
from typing import Any, Dict, List, Optional, Tuple, Type, Union
from pydantic import BaseModel, ValidationError

from legalmitra.core.enums import LegalReviewStatus
from legalmitra.core.logging import get_logger
from legalmitra.schemas.legal_qa import EvidencePassage, LegalQADocument
from legalmitra.schemas.registry import SourceRegistryRecord
from legalmitra.validation.grounding_validator import GroundingValidator
from legalmitra.validation.pydantic_validator import SchemaValidator
from legalmitra.validation.quality_gate import DataQualityGate
from legalmitra.generation.schemas import GeneratedDocument, task_type_to_schema, TaskType

logger = get_logger("generation_validator")


class GenerationValidationError(Exception):
    """Raised when generated output fails validation."""
    pass


class GenerationValidator:
    """
    Validates LLM-generated legal examples for schema compliance and source grounding.
    """
    
    def __init__(self, registry_manager=None):
        self.grounding_validator = GroundingValidator(registry_manager)
        self.schema_validator = SchemaValidator()
        self.registry = registry_manager
    
    def validate_generation_output(
        self,
        raw_output: str,
        task_type: TaskType,
        source_texts: Dict[str, str],
        source_records: Dict[str, SourceRegistryRecord],
    ) -> Tuple[List[GeneratedDocument], List[str]]:
        """
        Parse and validate raw LLM output.
        
        Returns:
            Tuple of (validated_documents, validation_errors)
        """
        errors = []
        documents = []
        
        # Parse JSON output
        try:
            parsed = json.loads(raw_output)
        except json.JSONDecodeError as e:
            salvaged = self._salvage_json_objects(raw_output)
            if salvaged:
                parsed = salvaged
            else:
                errors.append(f"Invalid JSON output: {e}")
                return [], errors
        
        # Accept single dict or array of examples
        if isinstance(parsed, dict):
            parsed = [parsed]
        elif not isinstance(parsed, list):
            errors.append("Output must be a JSON array of examples or a JSON object")
            return [], errors
        
        # Get target schema
        target_schema = task_type_to_schema(task_type)
        
        for idx, item in enumerate(parsed):
            try:
                # Validate schema
                is_valid, validated_doc, schema_error = self.schema_validator.validate(target_schema, item)
                if not is_valid or validated_doc is None:
                    errors.append(f"Example {idx}: Schema validation failed: {schema_error}")
                    continue
                
                # Validate grounding if enabled
                if task_type in (TaskType.STATUTORY_QA, TaskType.CASE_REASONING, 
                                TaskType.MULTILINGUAL, TaskType.SAFETY, 
                                TaskType.JUDGMENT_ANALYSIS, TaskType.PROCEDURAL_GUIDANCE, 
                                TaskType.DRAFTING):
                    grounded, grounding_issues = self._validate_document_grounding(
                        validated_doc, source_texts, source_records
                    )
                    if not grounded:
                        for issue in grounding_issues:
                            errors.append(f"Example {idx}: {issue}")
                        # Mark as flagged
                        if hasattr(validated_doc, 'flagged_unsupported'):
                            validated_doc.flagged_unsupported = True
                        if hasattr(validated_doc, 'legal_review_status'):
                            validated_doc.legal_review_status = LegalReviewStatus.FLAGGED_UNSUPPORTED
                
                # Enforce complete DataQualityGate for LegalQADocument instances
                if isinstance(validated_doc, LegalQADocument):
                    gate = DataQualityGate(registry_manager=self.registry, source_texts=source_texts)
                    qg_res = gate.validate_record(validated_doc)
                    if not qg_res.is_valid:
                        for qg_issue in qg_res.issues:
                            errors.append(f"Example {idx} QualityGate: {qg_issue}")
                        validated_doc.flagged_unsupported = True
                        validated_doc.legal_review_status = LegalReviewStatus.FLAGGED_UNSUPPORTED

                documents.append(validated_doc)
                
            except Exception as e:
                errors.append(f"Example {idx}: Unexpected validation error: {e}")
                logger.error(f"Validation error for example {idx}: {e}")
        
        return documents, errors
    
    def _validate_document_grounding(
        self,
        doc: GeneratedDocument,
        source_texts: Dict[str, str],
        source_records: Dict[str, SourceRegistryRecord],
    ) -> Tuple[bool, List[str]]:
        """Validate grounding for a generated document."""
        issues = []
        
        # Extract supporting source IDs
        supporting_ids = getattr(doc, 'supporting_source_ids', [])
        if not supporting_ids:
            issues.append("No supporting_source_ids provided")
            return False, issues
        
        # Check all source IDs exist in registry
        for s_id in supporting_ids:
            if s_id not in source_records:
                issues.append(f"Supporting source ID '{s_id}' not found in registry")
        
        # Check evidence passages
        evidence_passages = getattr(doc, 'evidence_passages', [])
        if not evidence_passages:
            issues.append("No evidence_passages provided")
            return False, issues
        
        for ep_idx, passage in enumerate(evidence_passages):
            if not isinstance(passage, EvidencePassage):
                issues.append(f"Evidence passage {ep_idx}: Invalid format")
                continue
            
            if passage.source_id not in supporting_ids:
                issues.append(
                    f"Evidence passage {ep_idx} references source '{passage.source_id}' "
                    f"not in supporting_source_ids"
                )
            
            # Verify verbatim text exists in source
            if passage.source_id in source_texts:
                source_text = source_texts[passage.source_id]
                if not self.grounding_validator.verify_evidence_passage(passage, source_text):
                    issues.append(
                        f"Evidence passage {ep_idx} ('{passage.section_or_para_ref}') "
                        f"not found verbatim in source {passage.source_id}"
                    )
        
        # Check statutory citations in answer against evidence
        answer = getattr(doc, 'answer', '') or getattr(doc, 'ratio_decidendi', '') or ''
        if answer:
            cited_sections = re.findall(r"\bSection\s+(\d+[A-Z]?)\b", answer, re.IGNORECASE)
            for sec in cited_sections:
                mentioned = any(
                    f"section {sec.lower()}" in p.verbatim_text.lower() or 
                    f"{sec.lower()}" in p.section_or_para_ref.lower()
                    for p in evidence_passages if isinstance(p, EvidencePassage)
                )
                if not mentioned:
                    issues.append(
                        f"Answer cites 'Section {sec}' but this section not found in evidence passages"
                    )
        
        return len(issues) == 0, issues
    
    def validate_single_document(
        self,
        doc: BaseModel,
        source_texts: Dict[str, str],
    ) -> Tuple[bool, List[str]]:
        """Validate a single document instance."""
        if isinstance(doc, LegalQADocument):
            return self.grounding_validator.validate_grounding(doc, source_texts)
        
        # For other types, basic validation
        issues = []
        supporting_ids = getattr(doc, 'supporting_source_ids', [])
        if not supporting_ids:
            issues.append("No supporting_source_ids")
        
        evidence = getattr(doc, 'evidence_passages', [])
        if not evidence:
            issues.append("No evidence_passages")
        
        for ep in evidence:
            if isinstance(ep, EvidencePassage) and ep.source_id in source_texts:
                if not self.grounding_validator.verify_evidence_passage(ep, source_texts[ep.source_id]):
                    issues.append(f"Evidence passage not found in source: {ep.section_or_para_ref}")
        
        return len(issues) == 0, issues

    def _salvage_json_objects(self, text: str) -> List[Dict[str, Any]]:
        """Extract all self-contained valid JSON objects from a truncated array or text."""
        results = []
        bracket_count = 0
        start = -1
        in_str = False
        escape = False
        for i, c in enumerate(text):
            if escape:
                escape = False
                continue
            if c == '\\' and in_str:
                escape = True
                continue
            if c == '"' and not escape:
                in_str = not in_str
                continue
            if not in_str:
                if c == '{':
                    if bracket_count == 0:
                        start = i
                    bracket_count += 1
                elif c == '}':
                    bracket_count -= 1
                    if bracket_count == 0 and start != -1:
                        chunk = text[start:i+1]
                        try:
                            obj = json.loads(chunk)
                            if isinstance(obj, dict):
                                results.append(obj)
                        except Exception:
                            pass
                        start = -1
        return results


def extract_json_from_response(response: str) -> str:
    """Extract JSON array or object from LLM response, handling markdown code blocks and nested structures."""
    # Try to find JSON in markdown code blocks first
    code_block_match = re.search(r"```(?:json)?\s*([\[\{][\s\S]*?[\]\}])\s*```", response)
    if code_block_match:
        return code_block_match.group(1).strip()
    
    # Find the outermost JSON array or object by bracket matching
    start_bracket = None
    start_idx = -1
    for i, c in enumerate(response):
        if c in ('[', '{'):
            start_bracket = c
            start_idx = i
            break
            
    if start_idx == -1:
        return response.strip()
    
    end_bracket = ']' if start_bracket == '[' else '}'
    bracket_count = 0
    in_string = False
    escape_next = False
    
    for i, char in enumerate(response[start_idx:], start=start_idx):
        if escape_next:
            escape_next = False
            continue
        
        if char == '\\' and in_string:
            escape_next = True
            continue
        
        if char == '"' and not escape_next:
            in_string = not in_string
            continue
        
        if not in_string:
            if char == start_bracket:
                bracket_count += 1
            elif char == end_bracket:
                bracket_count -= 1
                if bracket_count == 0:
                    return response[start_idx:i+1]
    
    # Return as-is if no balanced brackets found
    return response.strip()