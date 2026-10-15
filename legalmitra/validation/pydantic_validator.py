"""
LegalMitra Schema Validator
Validates dataset entities against Pydantic schemas and enforces explicit legal review tagging.
"""

from typing import Any, Dict, Optional, Tuple, Type, Union
from pydantic import BaseModel, ValidationError

from legalmitra.core.enums import LegalReviewStatus
from legalmitra.core.errors import SchemaValidationError
from legalmitra.core.logging import get_logger

logger = get_logger("schema_validator")


class SchemaValidator:
    """
    Enforces strict Pydantic validation across all Indian legal dataset schemas.
    """

    @staticmethod
    def validate(model_class: Type[BaseModel], data: Union[Dict[str, Any], BaseModel]) -> Tuple[bool, Optional[BaseModel], Optional[str]]:
        """
        Validates data against the given Pydantic model.
        Returns: (is_valid, validated_model_instance, error_message)
        """
        try:
            if isinstance(data, model_class):
                validated = data
            else:
                validated = model_class.model_validate(data)

            # Ensure legal review status is explicit
            if hasattr(validated, "legal_review_status"):
                status = getattr(validated, "legal_review_status")
                if status not in LegalReviewStatus:
                    return False, None, f"Invalid legal review status: {status}"

            return True, validated, None
        except ValidationError as ve:
            error_msg = f"Schema validation failed for {model_class.__name__}:\n{ve}"
            logger.warning(error_msg)
            return False, None, error_msg
        except Exception as e:
            error_msg = f"Unexpected error during validation for {model_class.__name__}: {e}"
            logger.error(error_msg)
            return False, None, error_msg

    @classmethod
    def validate_or_raise(cls, model_class: Type[BaseModel], data: Union[Dict[str, Any], BaseModel]) -> BaseModel:
        """Validates or raises SchemaValidationError."""
        is_valid, model, err = cls.validate(model_class, data)
        if not is_valid or model is None:
            raise SchemaValidationError(err)
        return model
