"""
Original Indian Legal Tokenizer for LegalMitra Research.
Trained from scratch from Indian legal statutory and judicial texts.
Zero pretrained weights or tokenizers.
Provides custom legal tokens and full Unicode / Devanagari character support.
"""

from collections import Counter
import json
from pathlib import Path
import re
from typing import Dict, Iterable, List, Optional, Tuple, Union


SPECIAL_TOKENS = [
    "<pad>",   # 0: Padding token
    "<s>",     # 1: Start of sequence
    "</s>",    # 2: End of sequence
    "<unk>",   # 3: Unknown token
    "<sec>",   # 4: Section delimiter
    "<court>", # 5: Court delimiter
    "<prov>",  # 6: Proviso / provision delimiter
    "<act>",   # 7: Act delimiter
]


class IndianLegalTokenizer:
    """
    Subword / Byte-Pair tokenizer trained from scratch on Indian legal corpus text.
    Maintains clean separation from pretrained HuggingFace tokenizers.
    """

    def __init__(self, vocab: Optional[Dict[str, int]] = None, merges: Optional[List[Tuple[str, str]]] = None):
        if vocab is not None:
            self.vocab = vocab
            self.id_to_token = {v: k for k, v in vocab.items()}
        else:
            self.vocab = {tok: idx for idx, tok in enumerate(SPECIAL_TOKENS)}
            self.id_to_token = {idx: tok for idx, tok in enumerate(SPECIAL_TOKENS)}
        self.merges: List[Tuple[str, str]] = merges or []
        self.bpe_ranks: Dict[Tuple[str, str], int] = {tuple(m): i for i, m in enumerate(self.merges)}
        self._cache: Dict[str, List[str]] = {}
        self._special_token_set = set(SPECIAL_TOKENS)

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

    def _pre_tokenize(self, text: str) -> List[List[str]]:
        """Split text into words preserving punctuation, digits, and Indian legal citations."""
        # Clean whitespaces
        text = text.strip()
        if not text:
            return []
        # Pattern handles legal abbreviations, words, numbers, symbols, and Devanagari characters
        pattern = r"[\u0900-\u097F]+|[A-Za-z]+|\d+|[^\s\w]"
        words = re.findall(pattern, text)
        return [[char for char in word] for word in words]

    def train_from_texts(self, texts: Iterable[str], target_vocab_size: int = 1024) -> "IndianLegalTokenizer":
        """Train BPE subword merges from scratch using word-frequency aggregation."""
        # 1. Reset vocabulary to special tokens
        self.vocab = {tok: idx for idx, tok in enumerate(SPECIAL_TOKENS)}
        self.merges = []

        # 2. Extract base character frequencies from sample texts
        word_freqs = Counter()
        char_counts = Counter()
        for text in texts:
            pattern = r"[\u0900-\u097F]+|[A-Za-z]+|\d+|[^\s\w]"
            for word in re.findall(pattern, text):
                word_chars = tuple(word)
                word_freqs[word_chars] += 1
                for char in word:
                    char_counts[char] += 1

        # Pre-seed standard ASCII printable characters and Devanagari Unicode block (0x0900-0x097F)
        for codepoint in range(32, 127):
            ch = chr(codepoint)
            if ch not in self.vocab:
                self.vocab[ch] = len(self.vocab)
        for codepoint in range(0x0900, 0x0980):
            ch = chr(codepoint)
            if ch not in self.vocab:
                self.vocab[ch] = len(self.vocab)

        # Add single characters from corpus text
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

            # Update word_freqs with the new merged pair
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
        """Apply learned BPE merges to a single word using rank lookup and memoization."""
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
            word = tuple(new_word)
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

        # Pre-tokenize words
        words = re.findall(r"[\u0900-\u097F]+|[A-Za-z]+|\d+|[^\s\w]", text)
        for word in words:
            subwords = self._bpe(word)
            for sub in subwords:
                tokens.append(self.vocab.get(sub, self.unk_token_id))

        if add_special_tokens:
            tokens.append(self.eos_token_id)
        return tokens

    def decode(self, token_ids: List[int], skip_special_tokens: bool = True) -> str:
        """Convert token IDs back to human-readable text."""
        pieces = []
        for tid in token_ids:
            tok = self.id_to_token.get(tid, "<unk>")
            if skip_special_tokens and tok in self._special_token_set:
                continue
            pieces.append(tok)
        return "".join(pieces)

    def save(self, file_path: Union[str, Path]) -> None:
        """Serialize tokenizer to disk as JSON."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "vocab": self.vocab,
            "merges": self.merges,
            "special_tokens": SPECIAL_TOKENS,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, file_path: Union[str, Path]) -> "IndianLegalTokenizer":
        """Deserialize tokenizer from disk."""
        path = Path(file_path)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        merges = [tuple(m) for m in data.get("merges", [])]
        return cls(vocab=data.get("vocab"), merges=merges)
