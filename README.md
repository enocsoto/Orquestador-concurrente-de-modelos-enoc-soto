# Orquestador concurrente de modelos

Simula un backend que consulta tres modelos de IA al mismo tiempo. Si la tanda supera 2 segundos, registra el error y sigue. Después dispara 10 llamadas y deja correr solo 2 a la vez.

## Cómo correrlo

Requiere Python 3.12 o superior.

```bash
python3.12 -m venv .venv
.venv/bin/python -m orchestrator.orchestrator
```

En el log las tres llamadas arrancan juntas. `local_llama` no alcanza a terminar: aparece `TimeoutError` y el programa continúa con las simulaciones, de a dos.

## Qué hace

| Pieza | Comportamiento |
| --- | --- |
| `query_models` | Dispara `gpt_4_call`, `claude_3_call` y `local_llama_call` con `asyncio.gather` |
| Timeout | 2 segundos sobre la ejecución total. Captura `TimeoutError` y no detiene el proceso |
| `simulate_calls` | 10 llamadas con un `asyncio.Semaphore` de 2 |
| Espera | Solo `asyncio.sleep`. No usa `time.sleep` |

El código está en inglés. Los mensajes del logger están en español.

## Tests

```bash
.venv/bin/python -m unittest discover -s tests -v
```
