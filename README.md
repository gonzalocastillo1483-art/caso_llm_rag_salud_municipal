# Agente funcional para salud municipal - EP2

Continuación del caso de atención primaria municipal de la EP1. El prototipo orienta a funcionarios en consultas administrativas, recupera protocolos locales, conserva contexto, registra decisiones y cambia su plan ante urgencias, datos sensibles o caídas del sistema.

## Capacidades evaluadas

- Orquestación explícita con `LangGraph`.
- Consulta semántica de documentos con TF-IDF y similitud coseno.
- Herramientas de consulta, escritura de registros y escalamiento humano.
- Memoria de corto plazo por conversación y memoria de largo plazo en SQLite.
- Planificación adaptativa para rutas administrativa, sensible, contingencia y emergencia.
- Respuestas con fuentes, sanitización de datos personales y trazabilidad.
- Funcionamiento local sin API key; uso opcional de OpenAI si se configura una clave.

## Requisitos

- Python 3.10 o superior.
- Windows, macOS o Linux.
- No se requiere API key para ejecutar la demostración evaluada.

## Instalación en Windows

```powershell
git clone https://github.com/gonzalocastillo1483-art/caso_llm_rag_salud_municipal.git
cd caso_llm_rag_salud_municipal
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si PowerShell bloquea la activación, se puede ejecutar directamente:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Ejecutar la demo

Con el entorno activado:

```powershell
python -m src.salud_agent.demo
```

Sin activar el entorno:

```powershell
.\.venv\Scripts\python.exe -m src.salud_agent.demo
```

La demo recorre cinco casos: cambio de hora, caída del sistema, privacidad de ficha clínica, urgencia y una consulta de seguimiento que usa memoria.

## Conversación interactiva

```powershell
python -m src.salud_agent.cli
```

Escriba `salir` para terminar.

## Pruebas

```powershell
python -m unittest discover -s tests -v
```

Resultado esperado: `Ran 6 tests` y `OK`. Las pruebas cubren recuperación de fuentes, adaptación ante urgencia y contingencia, sanitización y memoria de corto y largo plazo.

## OpenAI opcional

El modo predeterminado usa un generador local determinista para que la evaluación sea reproducible. Para activar generación con un LLM:

```powershell
$env:OPENAI_API_KEY="su_clave"
$env:OPENAI_MODEL="gpt-4o-mini"
python -m src.salud_agent.demo
```

## Flujo del agente

```text
Consulta -> sanitizar/clasificar -> plan adaptativo
                |                       |
                | emergencia            | resto
                v                       v
          escalamiento humano     recuperar contexto
                                        |
                                  evaluar evidencia
                                   /            \
                             suficiente      insuficiente
                                 |                 |
                              responder       escalar
                                   \            /
                                    registrar
```

El detalle editable se encuentra en [`docs/arquitectura.mmd`](docs/arquitectura.mmd).

## Estructura

```text
src/salud_agent/       agente, memoria, planificación, herramientas y guardrails
data/source_documents/ protocolos simulados del caso
tests/                 pruebas automatizadas
docs/                  arquitectura, decisiones, casos y guía de exposición
prompts/                prompts optimizados
evidence/              resultados verificados
runtime/               memoria y registros creados al ejecutar (ignorado por Git)
```

## Alcance y seguridad

El agente no diagnostica, no prioriza clínicamente y no reemplaza a profesionales. Sanitiza RUT, correos y teléfonos antes de persistir; escala urgencias, ambigüedad y falta de evidencia; y registra fuentes y decisiones. Los documentos incluidos son simulados para fines académicos.

## Documentación de entrega

- [`docs/decisiones_diseno.md`](docs/decisiones_diseno.md): decisiones técnicas y limitaciones.
- [`docs/casos_prueba.md`](docs/casos_prueba.md): escenarios de demostración.
- [`docs/guion_presentacion.md`](docs/guion_presentacion.md): guion breve para la defensa.
- [`docs/uso_ia.md`](docs/uso_ia.md): declaración de uso responsable de IA.

