# Decisiones de diseño

> Guía de estudio: este archivo reúne evidencia objetiva del prototipo. El estudiante debe redactar en palabras propias la justificación técnica que presentará y entregará.

## Continuidad del caso

La EP1 propuso un RAG para orientar al call center y SOME de una red municipal. La EP2 convierte esa propuesta en un agente ejecutable: además de recuperar información, decide una ruta, construye un plan, usa herramientas, conserva memoria y deja trazabilidad.

## Framework y orquestación

Se usa `LangGraph` porque permite representar el proceso como nodos con estado compartido y transiciones condicionales. El grafo separa intake, planificación, recuperación, decisión, respuesta, escalamiento y persistencia. Esta separación facilita explicar y probar cada responsabilidad.

## Recuperación de contexto

Los protocolos Markdown se dividen por encabezados. Cada fragmento se vectoriza con TF-IDF y se ordena por similitud coseno. Se agregan equivalencias de dominio, por ejemplo `hora -> agenda/cita/cupo`, para mejorar consultas breves. La respuesta solo se genera cuando el mejor resultado supera un umbral; de lo contrario se deriva a una persona.

## Herramientas

1. `consultar_contexto`: recupera evidencia documental.
2. `registrar_caso`: escribe una línea JSON auditable con fecha, ruta y fuentes.
3. `escalar_caso`: registra la derivación cuando existe riesgo o falta evidencia.

Las herramientas están encapsuladas en un registro único para mantener bajo acoplamiento entre el grafo y las implementaciones.

## Memoria

La memoria corta conserva hasta ocho mensajes por `thread_id` y permite comprender seguimientos. La memoria larga almacena resúmenes anonimizados en SQLite y recupera experiencias relacionadas por coincidencia de términos. No se guarda la ficha clínica ni identificadores personales.

## Planificación adaptativa

El plan no es fijo. Una consulta administrativa usa recuperación, evaluación, redacción y registro. Una consulta sensible agrega verificación de privacidad. Una caída del sistema prioriza contingencia y registro de incidente. Una posible urgencia omite la respuesta documental y escala de inmediato.

## Generación

El modo local determinista permite evaluar el agente sin servicios externos. Si existe `OPENAI_API_KEY`, se habilita `ChatOpenAI` con temperatura cero y un prompt restringido a las fuentes. En ambos modos se conservan guardrails y trazabilidad.

## Limitaciones

- La base documental es simulada y pequeña; no representa políticas de una municipalidad específica.
- TF-IDF no comprende todos los sinónimos ni contradicciones documentales.
- Las reglas de riesgo son demostrativas y requieren validación clínica, legal y organizacional.
- Antes de un uso real se necesitan control de acceso, cifrado, monitoreo, evaluación con usuarios y aprobación institucional.

## Correspondencia con la rúbrica

| Indicador | Evidencia |
|---|---|
| IE1 | `ToolRegistry` integra consulta, escritura y escalamiento. |
| IE2 | `StateGraph` orquesta siete nodos y rutas condicionales. |
| IE3 | `ShortTermMemory` conserva contexto por conversación. |
| IE4 | `LongTermMemory` persiste y recupera casos en SQLite. |
| IE5 | `SemanticContextRetriever` recupera contexto relevante. |
| IE6 | `AdaptivePlanner` modifica pasos según riesgo y operación. |
| IE7 | Estado tipado, módulos separados y sanitización previa. |
| IE8 | Demo, pruebas y evidencias reproducibles. |
| IE9 | Informe, diagramas, README y referencias. |
| IE10 | Código y documentación organizados para la defensa individual. |

## Conclusión

El proyecto permitió transformar la propuesta RAG de la EP1 en un agente funcional capaz de consultar protocolos, planificar según el riesgo, usar herramientas, conservar memoria y registrar trazabilidad. Su funcionamiento se verificó con una demo reproducible y nueve pruebas automatizadas aprobadas. El principal aporte es que, ante falta de evidencia o una posible urgencia, el sistema deriva la atención a una persona. La principal limitación es el tamaño simulado de la base documental y el uso de reglas de demostración. Como siguiente mejora se propone incorporar documentos institucionales validados, evaluación con usuarios y controles de seguridad para realizar un piloto real.

