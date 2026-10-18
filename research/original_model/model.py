"""
Original Decoder-Only Causal Transformer for Indian Legal Research.
Built from scratch in PyTorch. Zero pretrained weights, zero pretrained embeddings.
Strict random weight initialization (N(0, 0.02)).
"""

import math
from dataclasses import dataclass
from typing import Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class LegalTransformerConfig:
    """Hyperparameters for decoder-only causal legal language model."""
    vocab_size: int = 1024
    d_model: int = 128
    n_layers: int = 4
    n_heads: int = 4
    d_ff: int = 512
    max_seq_len: int = 256
    dropout: float = 0.1
    tie_word_embeddings: bool = True
    pad_token_id: int = 0


class CausalSelfAttention(nn.Module):
    """Multi-Head Causal Self-Attention with lower-triangular autoregressive mask."""

    def __init__(self, config: LegalTransformerConfig):
        super().__init__()
        assert config.d_model % config.n_heads == 0, "d_model must be divisible by n_heads"
        self.n_heads = config.n_heads
        self.head_dim = config.d_model // config.n_heads
        self.d_model = config.d_model

        self.q_proj = nn.Linear(config.d_model, config.d_model, bias=False)
        self.k_proj = nn.Linear(config.d_model, config.d_model, bias=False)
        self.v_proj = nn.Linear(config.d_model, config.d_model, bias=False)
        self.out_proj = nn.Linear(config.d_model, config.d_model, bias=False)

        self.attn_dropout = nn.Dropout(config.dropout)
        self.resid_dropout = nn.Dropout(config.dropout)

        # Causal mask buffer
        mask = torch.tril(torch.ones(config.max_seq_len, config.max_seq_len))
        self.register_buffer("causal_mask", mask.view(1, 1, config.max_seq_len, config.max_seq_len))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, T, C = x.size()

        # Project Q, K, V
        q = self.q_proj(x).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)  # (B, H, T, D)
        k = self.k_proj(x).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)
        v = self.v_proj(x).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)

        # Attention scores
        scale = 1.0 / math.sqrt(self.head_dim)
        scores = torch.matmul(q, k.transpose(-2, -1)) * scale

        # Apply causal mask
        causal_slice = self.causal_mask[:, :, :T, :T]
        scores = scores.masked_fill(causal_slice == 0, float("-inf"))

        weights = F.softmax(scores, dim=-1)
        weights = self.attn_dropout(weights)

        context = torch.matmul(weights, v)  # (B, H, T, D)
        context = context.transpose(1, 2).contiguous().view(B, T, C)

        out = self.out_proj(context)
        return self.resid_dropout(out)


class FeedForward(nn.Module):
    """Position-wise Feed-Forward Network with GELU activation."""

    def __init__(self, config: LegalTransformerConfig):
        super().__init__()
        self.w1 = nn.Linear(config.d_model, config.d_ff)
        self.act = nn.GELU()
        self.w2 = nn.Linear(config.d_ff, config.d_model)
        self.dropout = nn.Dropout(config.dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.dropout(self.w2(self.act(self.w1(x))))


class TransformerBlock(nn.Module):
    """Pre-LN Transformer Decoder Block."""

    def __init__(self, config: LegalTransformerConfig):
        super().__init__()
        self.ln_1 = nn.LayerNorm(config.d_model)
        self.attn = CausalSelfAttention(config)
        self.ln_2 = nn.LayerNorm(config.d_model)
        self.mlp = FeedForward(config)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.attn(self.ln_1(x))
        x = x + self.mlp(self.ln_2(x))
        return x


class LegalDecoderTransformer(nn.Module):
    """
    Pure decoder-only causal Transformer initialized completely from scratch.
    Contains zero external weights. All parameters initialized via normal_(0, 0.02).
    """

    def __init__(self, config: LegalTransformerConfig):
        super().__init__()
        self.config = config

        self.tok_embeddings = nn.Embedding(config.vocab_size, config.d_model)
        self.pos_embeddings = nn.Embedding(config.max_seq_len, config.d_model)
        self.drop = nn.Dropout(config.dropout)

        self.blocks = nn.ModuleList([TransformerBlock(config) for _ in range(config.n_layers)])
        self.ln_f = nn.LayerNorm(config.d_model)
        self.lm_head = nn.Linear(config.d_model, config.vocab_size, bias=False)

        if config.tie_word_embeddings:
            self.lm_head.weight = self.tok_embeddings.weight

        # Strictly initialize weights randomly
        self.apply(self._init_weights)

    def _init_weights(self, module: nn.Module) -> None:
        """Initialize weights from Gaussian distribution with mean 0.0 and std 0.02."""
        if isinstance(module, nn.Linear):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
        elif isinstance(module, nn.LayerNorm):
            torch.nn.init.zeros_(module.bias)
            torch.nn.init.ones_(module.weight)

    def count_parameters(self, non_embedding_only: bool = False) -> int:
        """Count total trainable parameters."""
        if non_embedding_only:
            return sum(p.numel() for n, p in self.named_parameters() if "embedding" not in n)
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def forward(
        self,
        input_ids: torch.Tensor,
        labels: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
        """
        Forward pass computing logits and causal cross-entropy loss if labels provided.
        """
        B, T = input_ids.size()
        assert T <= self.config.max_seq_len, f"Sequence length {T} exceeds max_seq_len {self.config.max_seq_len}"

        positions = torch.arange(0, T, dtype=torch.long, device=input_ids.device)

        # Token + positional embeddings
        x = self.tok_embeddings(input_ids) + self.pos_embeddings(positions)
        x = self.drop(x)

        # Transformer blocks
        for block in self.blocks:
            x = block(x)

        x = self.ln_f(x)
        logits = self.lm_head(x)  # (B, T, vocab_size)

        loss = None
        if labels is not None:
            # Shift labels for next token prediction
            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = labels[..., 1:].contiguous()
            loss = F.cross_entropy(
                shift_logits.view(-1, self.config.vocab_size),
                shift_labels.view(-1),
                ignore_index=self.config.pad_token_id,
            )
            if torch.isnan(loss) or torch.isinf(loss):
                raise FloatingPointError("Loss diverged to NaN or Inf during forward pass")

        return logits, loss
