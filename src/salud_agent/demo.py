from __future__ import annotations

from pathlib import Path

from .agent import MunicipalHealthAgent


ROOT = Path(__file__).resolve().parents[2]


def print_result(question: str, result) -> None:
    print("=" * 88)
    print(f"Pregunta: {question}")
    print(f"Ruta: {result.route} | Acción: {result.action}")
    print("Plan adaptativo:")
    for step in result.plan:
        print(f"  {step.order}. [{step.priority}] {step.action}: {step.reason}")
    print("Respuesta:")
    print(result.answer)
    if result.citations:
        print("Fuentes:", "; ".join(result.citations))
    print("Auditoría:", result.audit_id)


def main() -> None:
    agent = MunicipalHealthAgent(ROOT / "data" / "source_documents", ROOT / "runtime")
    scenarios = [
        "¿Cómo cambio una hora de morbilidad?",
        "El sistema de agenda está caído, ¿cómo seguimos atendiendo?",
        "Mi RUT es 12.345.678-9. ¿Puede mi vecino retirar mi ficha clínica?",
        "Tengo dolor de pecho y falta de aire, ¿qué hago?",
        "En relación con la consulta anterior, ¿qué debe quedar registrado?",
    ]
    for question in scenarios:
        print_result(question, agent.ask(question, thread_id="demo-en-vivo"))


if __name__ == "__main__":
    main()

