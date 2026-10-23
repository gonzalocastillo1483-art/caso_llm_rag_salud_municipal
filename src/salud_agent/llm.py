from __future__ import annotations

import os

from .models import Evidence


class ResponseGenerator:
    def __init__(self) -> None:
        self._llm = None
        if os.getenv("OPENAI_API_KEY"):
            try:
                from langchain_openai import ChatOpenAI

                self._llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0)
            except ImportError:
                self._llm = None

    def generate(self, query: str, route: str, evidence: list[Evidence], memory: list[str]) -> str:
        if self._llm is not None:
            context = "\n".join(f"[{item.citation}] {item.text}" for item in evidence)
            prompt = (
                "Eres un asistente administrativo de salud municipal. Usa solo el contexto entregado, "
                "cita las fuentes entre corchetes, no diagnostiques y deriva si falta respaldo.\n"
                f"Ruta: {route}\nConsulta: {query}\nMemoria: {memory}\nContexto:\n{context}"
            )
            return str(self._llm.invoke(prompt).content)
        return self._deterministic(query, route, evidence)

    @staticmethod
    def _deterministic(query: str, route: str, evidence: list[Evidence]) -> str:
        lines = ["Respuesta sugerida para el funcionario:"]
        for item in evidence[:3]:
            text = item.text if len(item.text) <= 280 else item.text[:277].rstrip() + "..."
            lines.append(f"- {text} [{item.citation}]")
        if route == "sensible":
            lines.append("Aplique verificación de identidad y autorización. Si falta respaldo, derive a jefatura.")
        lines.append("Registre la orientación entregada sin almacenar RUT, teléfonos ni contenido de ficha clínica.")
        return "\n".join(lines)

