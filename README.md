# Asistente RAG para atención primaria municipal

Caso propuesto para la Evaluación Parcial N°1: diseño de una solución con LLM, agentes inteligentes y RAG para una red de centros de salud familiar municipal.

## Resumen del caso

La Dirección de Salud Municipal de una comuna ficticia llamada Santa Isabel administra tres CESFAM, un SAPU y una unidad de atención telefónica. El personal administrativo responde consultas repetitivas sobre toma de horas, derivaciones, farmacia, derechos de pacientes y continuidad de atención. La información está distribuida en protocolos PDF, circulares internas, planillas y mensajes enviados por correo. Esto genera respuestas inconsistentes, demoras y riesgo de entregar orientación clínica sin respaldo.

La solución propuesta es un asistente interno basado en LLM y RAG. El asistente recupera evidencia desde una base documental controlada, redacta respuestas con citas, bloquea consultas clínicas peligrosas y deriva a un funcionario humano cuando la pregunta no tiene respaldo suficiente.

## Qué incluye este repositorio

- `src/salud_rag`: implementación autocontenida del pipeline RAG.
- `data/source_documents`: documentos de ejemplo que simulan fuentes internas.
- `prompts`: prompts optimizados y separados por rol.
- `docs`: informe en Markdown, arquitectura y casos de prueba.
- `tests`: pruebas unitarias básicas para recuperación y guardrails.

## Ejecución rápida

No requiere servicios externos ni llaves de API.

```powershell
cd outputs/caso_llm_rag_salud_municipal
python -m src.salud_rag.demo
```

Para correr pruebas:

```powershell
python -m unittest discover -s tests
```

## Preguntas de demostración

```text
¿Qué debe responder el call center si una persona pide cambiar una hora de morbilidad?
¿Cómo se informa el retiro de medicamentos crónicos?
Un paciente dice que tiene dolor de pecho y falta de aire, ¿qué hago?
¿Puedo entregar la ficha clínica de una persona a su vecino?
```

## Decisiones técnicas principales

- Recuperación local con BM25 para que la demo funcione sin infraestructura externa.
- Chunking por secciones para conservar trazabilidad.
- Guardrails antes y después de recuperar evidencia.
- Respuestas con fuentes obligatorias.
- Separación entre documentos, recuperación, prompts, generación y auditoría.
- Diseño preparado para cambiar el generador determinístico por un LLM real.

## Alcance de la demo

La demo no diagnostica, no entrega indicaciones clínicas personalizadas y no procesa fichas clínicas reales. Usa documentos ficticios para demostrar el flujo técnico. En una implementación productiva se reemplazaría el motor BM25 por búsqueda híbrida, se integraría un modelo LLM aprobado por la institución y se conectaría un repositorio documental con control de versiones.

