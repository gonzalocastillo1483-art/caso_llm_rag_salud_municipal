from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .models import Evidence


HEADING_RE = re.compile(r"^(#{1,3})\s+(.+)$")

CONCEPT_ALIASES = {
    "hora": "agenda cita reserva cupo",
    "medicamento": "farmacia receta retiro stock",
    "remedio": "farmacia medicamento receta retiro",
    "ficha": "privacidad acceso autorizacion datos clinicos",
    "sistema": "contingencia continuidad caida operacion manual",
    "derivacion": "referencia traslado especialidad red",
}


@dataclass(frozen=True)
class KnowledgeChunk:
    source_id: str
    title: str
    section: str
    text: str


def _normalize_concepts(text: str) -> str:
    lowered = text.lower()
    additions = [expansion for term, expansion in CONCEPT_ALIASES.items() if term in lowered]
    return f"{text} {' '.join(additions)}".strip()


def load_chunks(directory: Path) -> list[KnowledgeChunk]:
    chunks: list[KnowledgeChunk] = []
    for path in sorted(directory.glob("*.md")):
        title = path.stem.replace("_", " ").title()
        section = title
        buffer: list[str] = []

        def flush() -> None:
            if not buffer:
                return
            chunks.append(KnowledgeChunk(path.stem.upper(), title, section, " ".join(buffer)))
            buffer.clear()

        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            match = HEADING_RE.match(line)
            if match:
                flush()
                section = match.group(2).strip()
                if match.group(1) == "#":
                    title = section
            elif line:
                buffer.append(line)
        flush()
    return chunks


class SemanticContextRetriever:
    """Recuperación vectorial local con TF-IDF normalizado por conceptos del dominio."""

    def __init__(self, source_dir: Path) -> None:
        self.chunks = load_chunks(source_dir)
        self.vectorizer = TfidfVectorizer(strip_accents="unicode", ngram_range=(1, 2), sublinear_tf=True)
        corpus = [_normalize_concepts(chunk.text) for chunk in self.chunks]
        self.matrix = self.vectorizer.fit_transform(corpus)

    def search(self, query: str, top_k: int = 4) -> list[Evidence]:
        query_vector = self.vectorizer.transform([_normalize_concepts(query)])
        scores = cosine_similarity(query_vector, self.matrix)[0]
        ranked = sorted(enumerate(scores), key=lambda item: item[1], reverse=True)
        results: list[Evidence] = []
        for index, score in ranked[:top_k]:
            if score <= 0:
                continue
            chunk = self.chunks[index]
            results.append(Evidence(chunk.source_id, chunk.title, chunk.section, chunk.text, float(score)))
        return results

