from __future__ import annotations

from dataclasses import dataclass
import re


RUT_RE = re.compile(r"\b\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]\b")
EMAIL_RE = re.compile(r"\b[\w.-]+@[\w.-]+\.\w+\b")
PHONE_RE = re.compile(r"\b(?:\+?56)?\s?(?:9\s?)?\d{4}\s?\d{4}\b")

EMERGENCY_TERMS = {
    "dolor de pecho", "falta de aire", "convulsion", "convulsión",
    "sangrado abundante", "perdida de conciencia", "pérdida de conciencia",
    "intento suicida", "accidente cerebrovascular",
}

SENSITIVE_TERMS = {"ficha clinica", "ficha clínica", "vecino", "rut", "diagnostico", "diagnóstico"}


@dataclass(frozen=True)
class SafetyDecision:
    route: str
    reason: str
    sanitized_query: str


def sanitize_text(text: str) -> str:
    text = RUT_RE.sub("[RUT]", text)
    text = EMAIL_RE.sub("[EMAIL]", text)
    return PHONE_RE.sub("[TELEFONO]", text)


def classify_query(query: str) -> SafetyDecision:
    lowered = query.lower()
    sanitized = sanitize_text(query)
    if any(term in lowered for term in EMERGENCY_TERMS):
        return SafetyDecision("emergencia", "Se detectaron signos de posible urgencia.", sanitized)
    if "caida" in lowered or "caído" in lowered or "sin sistema" in lowered:
        return SafetyDecision("contingencia", "Se detectó una interrupción operacional.", sanitized)
    if any(term in lowered for term in SENSITIVE_TERMS):
        return SafetyDecision("sensible", "La consulta puede involucrar información clínica o personal.", sanitized)
    return SafetyDecision("administrativa", "Consulta administrativa dentro del alcance.", sanitized)

