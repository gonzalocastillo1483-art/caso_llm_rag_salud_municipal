from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from uuid import uuid4

from .knowledge import SemanticContextRetriever
from .models import Evidence


class ToolRegistry:
    """Herramientas de consulta, escritura y escalamiento usadas por el grafo."""

    def __init__(self, retriever: SemanticContextRetriever, output_dir: Path) -> None:
        self.retriever = retriever
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def consultar_contexto(self, query: str, top_k: int = 4) -> list[Evidence]:
        return self.retriever.search(query, top_k=top_k)

    def registrar_caso(self, payload: dict) -> str:
        record_id = str(uuid4())
        record = {"id": record_id, "timestamp": datetime.now(timezone.utc).isoformat(), **payload}
        with (self.output_dir / "casos.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
        return record_id

    def escalar_caso(self, route: str, reason: str, query: str) -> str:
        return self.registrar_caso({"type": "escalamiento", "route": route, "reason": reason, "query": query})

