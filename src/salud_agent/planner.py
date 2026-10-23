from __future__ import annotations

from .models import PlanStep


class AdaptivePlanner:
    def create_plan(self, route: str, query: str) -> list[PlanStep]:
        steps = [
            PlanStep(1, "sanitizar", "Evitar que datos personales entren al flujo.", "alta"),
            PlanStep(2, "recuperar_contexto", "Combinar memoria de sesión, memoria persistente y documentos.", "alta"),
        ]
        if route == "emergencia":
            steps.append(PlanStep(3, "escalar_urgencia", "La seguridad clínica tiene prioridad sobre la respuesta automática.", "critica"))
            return steps
        if route == "contingencia":
            steps.extend([
                PlanStep(3, "consultar_contingencia", "Aplicar el protocolo de continuidad operativa.", "critica"),
                PlanStep(4, "registrar_incidente", "Dejar trazabilidad de la interrupción y la acción tomada.", "alta"),
            ])
            return steps
        steps.append(PlanStep(3, "evaluar_evidencia", "Responder solo si el contexto supera el umbral definido.", "alta"))
        if route == "sensible":
            steps.append(PlanStep(4, "verificar_privacidad", "Restringir acceso y derivar cuando falte autorización.", "critica"))
        steps.extend([
            PlanStep(len(steps) + 1, "redactar", "Construir una respuesta breve con fuentes.", "media"),
            PlanStep(len(steps) + 2, "registrar", "Persistir la decisión para continuidad y auditoría.", "media"),
        ])
        return steps

