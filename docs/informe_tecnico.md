# Diseño de solución con LLM y RAG para atención primaria municipal

## Resumen ejecutivo

Se propone un asistente interno para funcionarios de una red de atención primaria municipal. La solución usa recuperación aumentada de información para responder consultas administrativas con evidencia documental, disminuir inconsistencias y bloquear respuestas clínicas inseguras. El caso se contextualiza en la Dirección de Salud Municipal de Santa Isabel, organización ficticia basada en procesos reales de CESFAM, SAPU, SOME, farmacia y lista de espera.

## Problema organizacional

La red administra tres CESFAM, un SAPU y un call center comunal. La información operativa se encuentra fragmentada en protocolos, correos, planillas y circulares. Esto produce demoras, respuestas distintas entre funcionarios, dependencia de personas expertas y riesgo de entregar orientación sin respaldo.

## Objetivos de intervención

- Centralizar el acceso a documentos vigentes.
- Responder consultas administrativas con citas a fuentes.
- Reducir alucinaciones mediante RAG y verificación de evidencia.
- Resguardar datos personales y ficha clínica.
- Derivar a responsables humanos cuando la pregunta no tenga respaldo o involucre riesgo clínico.

## Fuentes de datos

Las fuentes internas consideradas son protocolos de agenda, farmacia, derivaciones, confidencialidad y continuidad operativa. No se ingesta ficha clínica ni datos personales reales. Cada documento debe tener responsable, versión, fecha de vigencia y clasificación de sensibilidad.

## Diseño RAG

El pipeline normaliza documentos, divide por secciones, crea chunks, calcula índice de recuperación y construye un contexto con las mejores evidencias. El generador redacta una respuesta breve y obligatoriamente citada. Antes de entregar la respuesta, un verificador revisa si hay evidencia suficiente y si la consulta requiere escalamiento.

## Agentes

El diseño lógico separa cinco agentes: clasificador de intención, recuperador documental, generador de respuesta, verificador de seguridad y auditor. Esta separación permite controlar permisos, registrar decisiones y reemplazar componentes sin rediseñar todo el sistema.

## Restricciones

La solución no diagnostica, no prescribe, no prioriza clínicamente, no entrega ficha clínica a terceros y no responde cuando la evidencia recuperada sea insuficiente. En esos casos deriva a SOME, jefatura de sector, farmacia o profesional clínico.

## Métricas de evaluación

Se propone medir precisión de recuperación, porcentaje de respuestas con cita, tasa de derivación correcta, tiempo promedio de respuesta, satisfacción del funcionario y número de incidentes por respuesta sin respaldo.

## Referencias

Las referencias APA completas se incluyen en el informe DOCX final.

