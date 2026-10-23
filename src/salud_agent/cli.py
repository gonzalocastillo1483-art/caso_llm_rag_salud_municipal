from __future__ import annotations

from pathlib import Path

from .agent import MunicipalHealthAgent
from .demo import print_result


ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    agent = MunicipalHealthAgent(ROOT / "data" / "source_documents", ROOT / "runtime")
    print("Agente municipal listo. Escriba 'salir' para terminar.")
    while True:
        query = input("\nConsulta> ").strip()
        if query.lower() in {"salir", "exit", "quit"}:
            break
        if query:
            print_result(query, agent.ask(query, thread_id="sesion-interactiva"))


if __name__ == "__main__":
    main()

