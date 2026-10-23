from __future__ import annotations

from collections import defaultdict, deque
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path
import sqlite3
from threading import Lock


@dataclass(frozen=True)
class MemoryItem:
    content: str
    score: float


class ShortTermMemory:
    def __init__(self, max_turns: int = 8) -> None:
        self._turns: dict[str, deque[str]] = defaultdict(lambda: deque(maxlen=max_turns))

    def add(self, thread_id: str, role: str, content: str) -> None:
        self._turns[thread_id].append(f"{role}: {content}")

    def context(self, thread_id: str) -> list[str]:
        return list(self._turns[thread_id])


class LongTermMemory:
    def __init__(self, database_path: Path) -> None:
        database_path.parent.mkdir(parents=True, exist_ok=True)
        self.database_path = database_path
        self._lock = Lock()
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_path)

    def _initialize(self) -> None:
        with closing(self._connect()) as connection:
            with connection:
                connection.execute(
                    "CREATE TABLE IF NOT EXISTS memories (id INTEGER PRIMARY KEY, thread_id TEXT, content TEXT, route TEXT)"
                )

    def remember(self, thread_id: str, content: str, route: str) -> None:
        with self._lock, closing(self._connect()) as connection:
            with connection:
                connection.execute(
                    "INSERT INTO memories(thread_id, content, route) VALUES (?, ?, ?)",
                    (thread_id, content, route),
                )

    def recall(self, query: str, limit: int = 3) -> list[str]:
        terms = {term.lower() for term in re_tokenize(query) if len(term) > 3}
        with closing(self._connect()) as connection:
            rows = connection.execute("SELECT content FROM memories ORDER BY id DESC LIMIT 100").fetchall()
        scored = []
        for (content,) in rows:
            overlap = len(terms.intersection(re_tokenize(content)))
            if overlap:
                scored.append((overlap, content))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [content for _, content in scored[:limit]]


def re_tokenize(text: str) -> set[str]:
    return {token.strip(".,:;!?¿¡()[]").lower() for token in text.split() if token.strip()}

