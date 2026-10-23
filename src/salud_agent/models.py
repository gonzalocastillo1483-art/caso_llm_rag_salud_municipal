from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypedDict


@dataclass(frozen=True)
class Evidence:
    source_id: str
    title: str
    section: str
    text: str
    score: float

    @property
    def citation(self) -> str:
        return f"{self.title} - {self.section}"


@dataclass(frozen=True)
class PlanStep:
    order: int
    action: str
    reason: str
    priority: str


@dataclass(frozen=True)
class AgentResponse:
    answer: str
    route: str
    action: str
    citations: list[str] = field(default_factory=list)
    plan: list[PlanStep] = field(default_factory=list)
    memory_used: list[str] = field(default_factory=list)
    audit_id: str = ""


class AgentState(TypedDict, total=False):
    query: str
    thread_id: str
    sanitized_query: str
    route: str
    risk_reason: str
    plan: list[PlanStep]
    evidence: list[Evidence]
    memory_context: list[str]
    action: str
    answer: str
    citations: list[str]
    audit_id: str

