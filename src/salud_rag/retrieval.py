from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import math
import re

from .documents import Chunk


TOKEN_RE = re.compile(r"[a-záéíóúñü0-9]+", re.IGNORECASE)

STOPWORDS = {
    "a", "al", "ante", "con", "de", "del", "el", "en", "es", "la", "las",
    "lo", "los", "para", "por", "que", "se", "si", "sin", "un", "una",
    "y", "o", "como", "cuando", "qué", "cual", "cuál", "debe", "puede",
}


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text) if token.lower() not in STOPWORDS]


@dataclass(frozen=True)
class RetrievalResult:
    chunk: Chunk
    score: float


class BM25Retriever:
    def __init__(self, chunks: list[Chunk], k1: float = 1.5, b: float = 0.75) -> None:
        self.chunks = chunks
        self.k1 = k1
        self.b = b
        self.chunk_terms = [Counter(tokenize(chunk.text)) for chunk in chunks]
        self.doc_lengths = [sum(terms.values()) for terms in self.chunk_terms]
        self.avg_doc_length = sum(self.doc_lengths) / max(len(self.doc_lengths), 1)
        self.document_frequency: dict[str, int] = defaultdict(int)
        for terms in self.chunk_terms:
            for term in terms:
                self.document_frequency[term] += 1

    def search(self, query: str, top_k: int = 4) -> list[RetrievalResult]:
        query_terms = tokenize(query)
        scores: list[RetrievalResult] = []
        for index, chunk in enumerate(self.chunks):
            score = self._score(query_terms, index)
            if score > 0:
                scores.append(RetrievalResult(chunk=chunk, score=score))
        scores.sort(key=lambda item: item.score, reverse=True)
        return scores[:top_k]

    def _score(self, query_terms: list[str], index: int) -> float:
        terms = self.chunk_terms[index]
        doc_length = self.doc_lengths[index] or 1
        total_docs = max(len(self.chunks), 1)
        score = 0.0
        for term in query_terms:
            frequency = terms.get(term, 0)
            if frequency == 0:
                continue
            doc_frequency = self.document_frequency.get(term, 0)
            idf = math.log(1 + (total_docs - doc_frequency + 0.5) / (doc_frequency + 0.5))
            numerator = frequency * (self.k1 + 1)
            denominator = frequency + self.k1 * (1 - self.b + self.b * doc_length / self.avg_doc_length)
            score += idf * numerator / denominator
        return score

