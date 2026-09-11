from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .documents import load_chunks
from .guardrails import classify_query
from .prompts import build_answer_prompt
from .retrieval import BM25Retriever, RetrievalResult


@dataclass(frozen=True)
class RagAnswer:
    answer: str
    route: str
    sources: list[str]
    retrieval_scores: list[tuple[str, float]]
    prompt_preview: str


class RagPipeline:
    def __init__(self, source_dir: Path, minimum_score: float = 1.2) -> None:
        self.chunks = load_chunks(source_dir)
        self.retriever = BM25Retriever(self.chunks)
        self.minimum_score = minimum_score

    def ask(self, query: str, top_k: int = 4) -> RagAnswer:
        safety = classify_query(query)
        if not safety.allowed:
            answer = (
                "No corresponde responder esta consulta con el asistente. "
                f"Motivo: {safety.reason} "
                "Indique a la persona que contacte atención de urgencia local, SAPU o 131 según disponibilidad, "
                "y active el protocolo humano definido por la red."
            )
            return RagAnswer(answer=answer, route=safety.route, sources=[], retrieval_scores=[], prompt_preview="")

        results = self.retriever.search(safety.sanitized_query, top_k=top_k)
        prompt = build_answer_prompt(safety.sanitized_query, results)
        if not results or results[0].score < self.minimum_score:
            answer = (
                "No encontré respaldo documental suficiente para responder con seguridad. "
                "Derive la consulta al referente SOME o a la jefatura de sector y registre la brecha documental."
            )
            return RagAnswer(
                answer=answer,
                route="sin_evidencia",
                sources=[],
                retrieval_scores=[(item.chunk.chunk_id, round(item.score, 3)) for item in results],
                prompt_preview=prompt.user,
            )

        answer = self._deterministic_generate(safety.sanitized_query, results, safety.route)
        return RagAnswer(
            answer=answer,
            route=safety.route,
            sources=[item.chunk.citation for item in results],
            retrieval_scores=[(item.chunk.chunk_id, round(item.score, 3)) for item in results],
            prompt_preview=prompt.user,
        )

    def _deterministic_generate(self, query: str, results: list[RetrievalResult], route: str) -> str:
        top_sources = ", ".join(f"[{item.chunk.citation}]" for item in results[:3])
        evidence_lines = []
        for item in results[:3]:
            text = item.chunk.text
            if len(text) > 360:
                text = text[:357].rstrip() + "..."
            evidence_lines.append(f"- {text} [{item.chunk.citation}]")

        scope_note = ""
        if route == "clinica_restringida":
            scope_note = (
                "\n\nAlcance: la respuesta no debe indicar diagnóstico, dosis ni tratamiento. "
                "Si la persona solicita orientación clínica personalizada, derive a profesional clínico."
            )

        return (
            f"Respuesta sugerida para el funcionario:\n\n"
            f"Según la base documental recuperada, entregue la orientación usando estas fuentes: {top_sources}.\n\n"
            f"Evidencia relevante:\n" + "\n".join(evidence_lines) + scope_note +
            "\n\nCierre operativo: confirme identidad solo cuando el procedimiento lo exija, no solicite datos sensibles "
            "por canales no autorizados y deje registro de la respuesta entregada."
        )

