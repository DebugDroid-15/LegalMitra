"""
LegalMitra Custom Exceptions
"""


class LegalMitraError(Exception):
    """Base exception for all LegalMitra errors."""
    pass


class SourceRegistryError(LegalMitraError):
    """Raised when there is an issue registering or updating a source document."""
    pass


class DuplicateDocumentError(LegalMitraError):
    """Raised when a duplicate document is encountered and duplicate handling is strict."""
    pass


class ExtractionError(LegalMitraError):
    """Raised when extraction of document content fails."""
    pass


class UnsupportedDocumentError(LegalMitraError):
    """Raised when encountering an unsupported file type or corrupted structure."""
    pass


class NormalizationError(LegalMitraError):
    """Raised when normalizer cannot parse structure from extracted text."""
    pass


class SchemaValidationError(LegalMitraError):
    """Raised when an object fails Pydantic schema validation."""
    pass


class GroundingValidationError(LegalMitraError):
    """Raised when a generated answer references unsupported or ungrounded assertions."""
    pass


class LLMProviderError(LegalMitraError):
    """Raised when an LLM provider fails to generate or authenticate."""
    pass

