from __future__ import annotations

from pathlib import Path

from langgraph.graph import END, StateGraph

from .guardrails import classify_query
from .knowledge import SemanticContextRetriever
from .llm import ResponseGenerator
from .memory import LongTermMemory, ShortTermMemory
from .models import AgentResponse, AgentState
from .planner import AdaptivePlanner
from .tools import ToolRegistry


class MunicipalHealthAgent:
    def __init__(self, source_dir: Path, runtime_dir: Path, minimum_score: float = 0.08) -> None:
        self.short_memory = ShortTermMemory()
        self.long_memory = LongTermMemory(runtime_dir / "agent_memory.sqlite3")
        self.planner = AdaptivePlanner()
        self.tools = ToolRegistry(SemanticContextRetriever(source_dir), runtime_dir / "records")
        self.generator = ResponseGenerator()
        self.minimum_score = minimum_score
        self.graph = self._build_graph()

    def _build_graph(self):
        builder = StateGraph(AgentState)
        builder.add_node("intake", self._intake)
        builder.add_node("plan", self._plan)
        builder.add_node("retrieve", self._retrieve)
        builder.add_node("decide", self._decide)
        builder.add_node("respond", self._respond)
        builder.add_node("escalate", self._escalate)
        builder.add_node("persist", self._persist)
        builder.set_entry_point("intake")
        builder.add_edge("intake", "plan")
        builder.add_conditional_edges("plan", self._after_plan, {"escalate": "escalate", "retrieve": "retrieve"})
        builder.add_edge("retrieve", "decide")
        builder.add_conditional_edges("decide", self._after_decision, {"respond": "respond", "escalate": "escalate"})
        builder.add_edge("respond", "persist")
        builder.add_edge("escalate", "persist")
        builder.add_edge("persist", END)
        return builder.compile()

    def ask(self, query: str, thread_id: str = "demo") -> AgentResponse:
        self.short_memory.add(thread_id, "usuario", query)
        result = self.graph.invoke(
            {"query": query, "thread_id": thread_id},
        )
        self.short_memory.add(thread_id, "agente", result["answer"])
        return AgentResponse(
            answer=result["answer"],
            route=result["route"],
            action=result["action"],
            citations=result.get("citations", []),
            plan=result.get("plan", []),
            memory_used=result.get("memory_context", []),
            audit_id=result.get("audit_id", ""),
        )

    def _intake(self, state: AgentState) -> AgentState:
        decision = classify_query(state["query"])
        return {
            "sanitized_query": decision.sanitized_query,
            "route": decision.route,
            "risk_reason": decision.reason,
            "memory_context": self.short_memory.context(state["thread_id"]) + self.long_memory.recall(decision.sanitized_query),
        }

    def _plan(self, state: AgentState) -> AgentState:
        return {"plan": self.planner.create_plan(state["route"], state["sanitized_query"])}

    @staticmethod
    def _after_plan(state: AgentState) -> str:
        return "escalate" if state["route"] == "emergencia" else "retrieve"

    def _retrieve(self, state: AgentState) -> AgentState:
        return {"evidence": self.tools.consultar_contexto(state["sanitized_query"])}

    def _decide(self, state: AgentState) -> AgentState:
        evidence = state.get("evidence", [])
        if not evidence or evidence[0].score < self.minimum_score:
            return {"action": "escalar_sin_evidencia", "risk_reason": "Contexto insuficiente para responder con seguridad."}
        if state["route"] == "contingencia":
            return {"action": "aplicar_contingencia"}
        return {"action": "responder_con_fuentes"}

    @staticmethod
    def _after_decision(state: AgentState) -> str:
        return "escalate" if state["action"].startswith("escalar") else "respond"

    def _respond(self, state: AgentState) -> AgentState:
        answer = self.generator.generate(
            state["sanitized_query"], state["route"], state.get("evidence", []), state.get("memory_context", [])
        )
        return {"answer": answer, "citations": [item.citation for item in state.get("evidence", [])]}

    def _escalate(self, state: AgentState) -> AgentState:
        route = state.get("route", "sin_evidencia")
        reason = state.get("risk_reason", "Se requiere revisión humana.")
        audit_id = self.tools.escalar_caso(route, reason, state.get("sanitized_query", state["query"]))
        if route == "emergencia":
            answer = "Active el protocolo humano de urgencia. Indique SAPU, servicio de urgencia o 131 según disponibilidad local."
            action = "escalar_urgencia"
        else:
            answer = "No existe evidencia suficiente para una respuesta segura. Derive a SOME o jefatura y registre la brecha documental."
            action = "escalar_sin_evidencia"
        return {"answer": answer, "action": action, "citations": [], "audit_id": audit_id}

    def _persist(self, state: AgentState) -> AgentState:
        record_id = state.get("audit_id") or self.tools.registrar_caso({
            "type": "respuesta",
            "route": state["route"],
            "action": state["action"],
            "query": state["sanitized_query"],
            "citations": state.get("citations", []),
        })
        memory_text = f"Consulta: {state['sanitized_query']} | Acción: {state['action']} | Fuentes: {', '.join(state.get('citations', []))}"
        self.long_memory.remember(state["thread_id"], memory_text, state["route"])
        return {"audit_id": record_id}

