from __future__ import annotations

from dataclasses import dataclass
import re


RUT_RE = re.compile(r"\b\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]\b")
EMAIL_RE = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b")
PHONE_RE = re.compile(r"\b(?:\+?56)?\s?(?:9\s?)?\d{4}\s?\d{4}\b")

EMERGENCY_TERMS = {
    "dolor de pecho",
    "falta de aire",
    "convulsión",
    "convulsion",
    "sangrado abundante",
    "pérdida de conciencia",
    "perdida de conciencia",
    "intento suicida",
    "accidente cerebrovascular",
}

CLINICAL_ADVICE_TERMS = {
    "diagnóstico",
    "diagnostico",
    "receta",
    "dosis",
    "antibiótico",
    "antibiotico",
    "tratamiento",
    "medicamento me tomo",
}


@dataclass(frozen=True)
class SafetyDecision:
    allowed: bool
    reason: str
    sanitized_query: str
    route: str


def sanitize_text(text: str) -> str:
    sanitized = RUT_RE.sub("[RUT]", text)
    sanitized = EMAIL_RE.sub("[EMAIL]", sanitized)
    sanitized = PHONE_RE.sub("[TELEFONO]", sanitized)
    return sanitized


def classify_query(query: str) -> SafetyDecision:
    lowered = query.lower()
    sanitized = sanitize_text(query)

    if any(term in lowered for term in EMERGENCY_TERMS):
        return SafetyDecision(
            allowed=False,
            reason="La consulta contiene signos de urgencia o emergencia.",
            sanitized_query=sanitized,
            route="emergencia",
        )

    if any(term in lowered for term in CLINICAL_ADVICE_TERMS):
        return SafetyDecision(
            allowed=True,
            reason="La consulta puede requerir control de alcance para evitar consejo clínico personalizado.",
            sanitized_query=sanitized,
            route="clinica_restringida",
        )

    return SafetyDecision(
        allowed=True,
        reason="Consulta administrativa o informativa.",
        sanitized_query=sanitized,
        route="administrativa",
    )

