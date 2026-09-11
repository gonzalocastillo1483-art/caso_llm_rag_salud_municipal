from __future__ import annotations

from dataclasses import dataclass

from .retrieval import RetrievalResult


SYSTEM_PROMPT = """Eres un asistente interno para personal administrativo de una red de salud municipal.
Tu tarea es responder solo con información respaldada por documentos recuperados.
No diagnostiques, no indiques tratamientos, no inventes horarios y no uses datos personales.
Si falta evidencia, deriva a un referente humano.
"""


ANSWER_PROMPT_TEMPLATE = """Pregunta del funcionario:
{query}

Contexto recuperado:
{context}

Instrucciones:
1. Responde en español chileno formal y claro.
2. Distingue información segura, restricciones y derivación.
3. Cita las fuentes usadas con el formato [FUENTE].
4. Si la pregunta pide consejo clínico personalizado, limita la respuesta a orientación administrativa.
"""


@dataclass(frozen=True)
class BuiltPrompt:
    system: str
    user: str


def build_context(results: list[RetrievalResult]) -> str:
    lines: list[str] = []
    for result in results:
        citation = result.chunk.citation
        lines.append(f"[{citation}] {result.chunk.text}")
    return "\n\n".join(lines)


def build_answer_prompt(query: str, results: list[RetrievalResult]) -> BuiltPrompt:
    return BuiltPrompt(
        system=SYSTEM_PROMPT,
        user=ANSWER_PROMPT_TEMPLATE.format(query=query, context=build_context(results)),
    )

