from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class SourceDocument:
    doc_id: str
    title: str
    path: Path
    body: str


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    doc_id: str
    title: str
    section: str
    text: str
    path: str

    @property
    def citation(self) -> str:
        return f"{self.doc_id} - {self.section}"


HEADING_RE = re.compile(r"^(#{1,3})\s+(.+)$")


def load_documents(directory: Path) -> list[SourceDocument]:
    docs: list[SourceDocument] = []
    for path in sorted(directory.glob("*.md")):
        body = path.read_text(encoding="utf-8")
        title = path.stem.replace("_", " ").title()
        for line in body.splitlines():
            match = HEADING_RE.match(line.strip())
            if match and match.group(1) == "#":
                title = match.group(2).strip()
                break
        docs.append(SourceDocument(doc_id=path.stem.upper(), title=title, path=path, body=body))
    return docs


def chunk_document(document: SourceDocument, max_words: int = 130) -> list[Chunk]:
    chunks: list[Chunk] = []
    current_section = document.title
    buffer: list[str] = []

    def flush() -> None:
        if not buffer:
            return
        words = " ".join(buffer).split()
        while words:
            piece = words[:max_words]
            del words[:max_words]
            index = len(chunks) + 1
            chunks.append(
                Chunk(
                    chunk_id=f"{document.doc_id}-{index:03d}",
                    doc_id=document.doc_id,
                    title=document.title,
                    section=current_section,
                    text=" ".join(piece),
                    path=str(document.path),
                )
            )
        buffer.clear()

    for raw_line in document.body.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = HEADING_RE.match(line)
        if match:
            flush()
            current_section = match.group(2).strip()
            continue
        buffer.append(line)
    flush()
    return chunks


def load_chunks(directory: Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    for document in load_documents(directory):
        chunks.extend(chunk_document(document))
    return chunks

