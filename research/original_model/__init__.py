"""
Original Indian Legal Foundation Model Research Namespace.
Independent experimental research modules for pretraining an Indian legal LLM from scratch.
Zero external pretrained weights.
"""

from research.original_model.tokenizer import IndianLegalTokenizer
from research.original_model.model import LegalDecoderTransformer, LegalTransformerConfig
from research.original_model.dataset import LegalDataset, build_train_val_datasets

__all__ = [
    "IndianLegalTokenizer",
    "LegalDecoderTransformer",
    "LegalTransformerConfig",
    "LegalDataset",
    "build_train_val_datasets",
]
