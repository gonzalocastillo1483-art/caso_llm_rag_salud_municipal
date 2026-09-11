from __future__ import annotations

from pathlib import Path

from .pipeline import RagPipeline


EXAMPLES = [
    "¿Qué debe responder el call center si una persona pide cambiar una hora de morbilidad?",
    "¿Cómo se informa el retiro de medicamentos crónicos?",
    "Un paciente dice que tiene dolor de pecho y falta de aire, ¿qué hago?",
    "¿Puedo entregar la ficha clínica de una persona a su vecino?",
]


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    pipeline = RagPipeline(root / "data" / "source_documents")
    for question in EXAMPLES:
        print("=" * 88)
        print(f"Pregunta: {question}")
        result = pipeline.ask(question)
        print(f"Ruta: {result.route}")
        print(result.answer)
        if result.sources:
            print("\nFuentes:", "; ".join(result.sources))
        if result.retrieval_scores:
            print("Scores:", result.retrieval_scores)


if __name__ == "__main__":
    main()

