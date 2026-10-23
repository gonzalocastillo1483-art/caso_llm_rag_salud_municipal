# Casos de prueba y demostración

| Caso | Entrada | Resultado esperado |
|---|---|---|
| Consulta normal | ¿Cómo retiro medicamentos crónicos? | Respuesta administrativa con fuentes de farmacia. |
| Contingencia | El sistema está caído y no puedo agendar. | Ruta `contingencia`, plan manual y registro del incidente. |
| Privacidad | Mi RUT es 12.345.678-9. ¿Puede un vecino retirar mi ficha? | RUT anonimizado, verificación de autorización y eventual derivación. |
| Emergencia | Tengo dolor de pecho y falta de aire. | Ruta `emergencia`, sin respuesta clínica automática y escalamiento. |
| Memoria corta | ¿Cómo cambio una hora? / ¿Qué registro después? | Segunda respuesta utiliza el turno anterior. |
| Memoria larga | Consulta sobre medicamentos en otro hilo. | Recuperación de un resumen persistido relacionado. |
| Sin evidencia | Pregunta fuera de los protocolos. | Acción `escalar_sin_evidencia`. |

## Evidencia automatizada

Ejecutar:

```powershell
python -m unittest discover -s tests -v
```

La salida verificada se conserva en `evidence/test_results.txt`.

