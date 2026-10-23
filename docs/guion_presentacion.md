# Guion de presentación (10 minutos)

## 1. Caso y objetivo - 1 minuto

“Continuamos el caso de la EP1: funcionarios municipales necesitan responder consultas administrativas sin improvisar ni exponer datos sensibles. Ahora implementamos un agente funcional que consulta protocolos, decide una ruta, conserva memoria y deja registro.”

## 2. Arquitectura - 2 minutos

“LangGraph coordina siete etapas. Primero se sanitiza y clasifica; luego se crea un plan. Las consultas normales recuperan documentos y evalúan evidencia. Las urgencias saltan directamente a escalamiento. Todo termina en un registro auditable.”

## 3. Herramientas y contexto - 1 minuto

“El agente tiene tres herramientas: buscar contexto, registrar casos y escalar. La recuperación usa TF-IDF y similitud coseno sobre protocolos divididos por secciones, por lo que cada respuesta muestra sus fuentes.”

## 4. Memoria - 1 minuto

“La memoria corta mantiene los últimos turnos de una conversación. La memoria larga guarda resúmenes anonimizados en SQLite y permite recuperar experiencias relacionadas incluso desde otro hilo.”

## 5. Planificación adaptativa - 1 minuto

“El plan cambia con el entorno: privacidad agrega validación, caída del sistema activa contingencia y una posible urgencia evita la respuesta automática para escalar.”

## 6. Demo - 3 minutos

Ejecutar `python -m src.salud_agent.demo`. Mostrar tres casos: administrativo, sistema caído y dolor de pecho. Señalar ruta, acción, plan, fuentes y auditoría. Después ejecutar `python -m unittest discover -s tests -v` y mostrar los seis casos aprobados.

## 7. Cierre - 1 minuto

“El prototipo demuestra consulta, escritura, razonamiento, memoria y adaptación. Su límite principal es que usa documentos simulados y reglas que necesitan validación institucional antes de un uso real.”

## Preguntas probables

- ¿Por qué LangGraph? Porque hace visibles las etapas y rutas condicionales.
- ¿Qué ocurre si no hay evidencia? El agente escala y registra la brecha.
- ¿Dónde está la memoria? Corto plazo en memoria por hilo y largo plazo en SQLite.
- ¿Requiere API key? No; la demo local es determinista. La integración LLM es opcional.
- ¿Qué evita una alucinación? Contexto restringido, umbral de evidencia, citas y escalamiento.

