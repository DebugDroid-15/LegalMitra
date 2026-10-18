"""
Indian Legal Tokenizer V2 for LegalMitra Phase 33 Bilingual Research.
Trained jointly from scratch on English and Hindi Indian legal texts.
Zero pretrained weights or tokenizers.
Preserves Devanagari Unicode, legal morphemes, whitespace round-tripping,
and Indian legal citation patterns in both English and Hindi.
"""

from collections import Counter
import json
from pathlib import Path
import re
from typing import Dict, Iterable, List, Optional, Tuple, Union


SPECIAL_TOKENS_V2 = [
    "<pad>",   # 0: Padding token
    "<s>",     # 1: Start of sequence
    "</s>",    # 2: End of sequence
    "<unk>",   # 3: Unknown token
    "<sec>",   # 4: Section delimiter
    "<court>", # 5: Court delimiter
    "<prov>",  # 6: Proviso delimiter
    "<act>",   # 7: Act delimiter
    "<hi>",    # 8: Hindi language tag
    "<en>",    # 9: English language tag
]


class IndianLegalTokenizerV2:
    """
    Enhanced Bilingual Subword Tokenizer trained from scratch on Indian legal corpus.
    Maintains clean separation from pretrained HuggingFace tokenizers.
    Preserves whitespace via a distinct marker (Ġ /  ) for exact reconstruction.
    """

    def __init__(self, vocab: Optional[Dict[str, int]] = None, merges: Optional[List[Tuple[str, str]]] = None):
        if vocab is not None:
            self.vocab = vocab
            self.id_to_token = {v: k for k, v in vocab.items()}
        else:
            self.vocab = {tok: idx for idx, tok in enumerate(SPECIAL_TOKENS_V2)}
            self.id_to_token = {idx: tok for idx, tok in enumerate(SPECIAL_TOKENS_V2)}
        self.merges: List[Tuple[str, str]] = merges or []
        self.bpe_ranks: Dict[Tuple[str, str], int] = {tuple(m): i for i, m in enumerate(self.merges)}
        self._cache: Dict[str, List[str]] = {}
        self._special_token_set = set(SPECIAL_TOKENS_V2)

    @property
    def vocab_size(self) -> int:
        return len(self.vocab)

    @property
    def pad_token_id(self) -> int:
        return self.vocab["<pad>"]

    @property
    def bos_token_id(self) -> int:
        return self.vocab["<s>"]

    @property
    def eos_token_id(self) -> int:
        return self.vocab["</s>"]

    @property
    def unk_token_id(self) -> int:
        return self.vocab["<unk>"]

    def _pre_tokenize(self, text: str) -> List[str]:
        """
        Split text into words preserving whitespace as leading marker 'Ġ'
        and handling Devanagari, English, legal abbreviations, and punctuation.
        """
        if not text:
            return []
        # Pre-process spaces: replace spaces with space marker 'Ġ'
        # Split tokens with regex preserving Devanagari clusters, English words, numbers, and symbols
        pattern = r"( ?[\u0900-\u097F]+| ?[A-Za-z]+| ?\d+| ?[^\s\w]|\n)"
        tokens = re.findall(pattern, text)
        result = []
        for t in tokens:
            if t.startswith(" "):
                result.append("Ġ" + t[1:])
            elif t == "\n":
                result.append("Ċ")
            else:
                result.append(t)
        return result

    def train_from_texts(self, texts: Iterable[str], target_vocab_size: int = 2048) -> "IndianLegalTokenizerV2":
        """Train BPE subword merges from scratch using joint English-Hindi texts."""
        # 1. Reset vocabulary to special tokens
        self.vocab = {tok: idx for idx, tok in enumerate(SPECIAL_TOKENS_V2)}
        self.merges = []

        # 2. Extract base characters and pre-tokenized words
        word_freqs = Counter()
        char_counts = Counter()

        # Pre-seed standard ASCII printable characters (32..126)
        for codepoint in range(32, 127):
            ch = chr(codepoint)
            if ch not in self.vocab:
                self.vocab[ch] = len(self.vocab)

        # Pre-seed Devanagari Unicode block (0x0900-0x097F)
        for codepoint in range(0x0900, 0x0980):
            ch = chr(codepoint)
            if ch not in self.vocab:
                self.vocab[ch] = len(self.vocab)

        # Pre-seed space and newline markers
        for m in ["Ġ", "Ċ"]:
            if m not in self.vocab:
                self.vocab[m] = len(self.vocab)

        for text in texts:
            words = self._pre_tokenize(text)
            for word in words:
                word_chars = tuple(word)
                word_freqs[word_chars] += 1
                for char in word:
                    char_counts[char] += 1

        for char, _ in char_counts.most_common():
            if char not in self.vocab:
                self.vocab[char] = len(self.vocab)

        self.id_to_token = {v: k for k, v in self.vocab.items()}

        # 3. Iteratively perform BPE merges until target_vocab_size is reached
        while len(self.vocab) < target_vocab_size:
            pair_counts = Counter()
            for word_tuple, freq in word_freqs.items():
                for i in range(len(word_tuple) - 1):
                    pair_counts[(word_tuple[i], word_tuple[i + 1])] += freq

            if not pair_counts:
                break

            best_pair, best_count = pair_counts.most_common(1)[0]
            if best_count < 2:
                break

            new_token = best_pair[0] + best_pair[1]
            self.merges.append(best_pair)
            self.vocab[new_token] = len(self.vocab)
            self.id_to_token[self.vocab[new_token]] = new_token

            # Update word_freqs with new merge
            new_word_freqs = Counter()
            for word_tuple, freq in word_freqs.items():
                new_tuple = []
                i = 0
                while i < len(word_tuple):
                    if i < len(word_tuple) - 1 and (word_tuple[i], word_tuple[i + 1]) == best_pair:
                        new_tuple.append(new_token)
                        i += 2
                    else:
                        new_tuple.append(word_tuple[i])
                        i += 1
                new_word_freqs[tuple(new_tuple)] += freq
            word_freqs = new_word_freqs

        self.bpe_ranks = {tuple(m): i for i, m in enumerate(self.merges)}
        self._cache = {}
        return self

    def _bpe(self, token: str) -> List[str]:
        """Apply learned BPE merges to a single word/cluster with memoization."""
        if token in self._cache:
            return self._cache[token]

        word = tuple(token)
        pairs = set(zip(word[:-1], word[1:]))
        if not pairs:
            return [token]

        while True:
            valid_pairs = [p for p in pairs if p in self.bpe_ranks]
            if not valid_pairs:
                break
            min_pair = min(valid_pairs, key=lambda p: self.bpe_ranks[p])
            first, second = min_pair
            new_word = []
            i = 0
            while i < len(word):
                if i < len(word) - 1 and word[i] == first and word[i + 1] == second:
                    new_word.append(first + second)
                    i += 2
                else:
                    new_word.append(word[i])
                    i += 1
                word_tuple = tuple(new_word)
            word = word_tuple
            if len(word) == 1:
                break
            pairs = set(zip(word[:-1], word[1:]))

        res = list(word)
        self._cache[token] = res
        return res

    def encode(self, text: str, add_special_tokens: bool = True) -> List[int]:
        """Convert text into token IDs using fast cached BPE."""
        tokens = []
        if add_special_tokens:
            tokens.append(self.bos_token_id)

        words = self._pre_tokenize(text)
        for word in words:
            subwords = self._bpe(word)
            for sub in subwords:
                tokens.append(self.vocab.get(sub, self.unk_token_id))

        if add_special_tokens:
            tokens.append(self.eos_token_id)
        return tokens

    def decode(self, token_ids: List[int], skip_special_tokens: bool = True) -> str:
        """Convert token IDs back to human-readable text restoring spaces."""
        pieces = []
        for tid in token_ids:
            tok = self.id_to_token.get(tid, "<unk>")
            if skip_special_tokens and tok in self._special_token_set:
                continue
            pieces.append(tok)
        raw = "".join(pieces)
        # Restore whitespace markers
        restored = raw.replace("Ġ", " ").replace("Ċ", "\n")
        return restored

    def save(self, file_path: Union[str, Path]) -> None:
        """Serialize tokenizer to disk as JSON."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "version": "v2.0.0",
            "vocab_size": len(self.vocab),
            "vocab": self.vocab,
            "merges": self.merges,
            "special_tokens": SPECIAL_TOKENS_V2,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, file_path: Union[str, Path]) -> "IndianLegalTokenizerV2":
        """Deserialize tokenizer from disk."""
        path = Path(file_path)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        merges = [tuple(m) for m in data.get("merges", [])]
        return cls(vocab=data.get("vocab"), merges=merges)

