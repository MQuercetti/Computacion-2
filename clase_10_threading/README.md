# Clase 10: Threading

Material de la décima clase de Computación II (2026) — Hilos, GIL, race conditions, `Lock`, `Queue`, `threading.local()`.

## Estructura

```
clase_10_threading/
├── README.md                  ← este archivo
├── contenido.md               ← teoría: threads, GIL, Lock, daemon
├── ejercicios.md              ← 9 ejercicios (9: descargador paralelo obligatorio)
├── autoevaluacion.md          ← quiz
├── extra_manijas.md           ← material opcional
└── scripts/
    ├── primer_hilo.py         ← ejercicio 1: 3 hilos con pausas
    ├── io_bound_compare.py    ← ejercicio 2: secuencial vs threading (descargas)
    ├── gil_cpu_bound.py       ← ejercicio 3: demostrar que GIL bloquea CPU-bound
    ├── contador_hilo_subclase.py← ejercicio 4: clase Thread personalizada
    ├── race_y_lock.py         ← ejercicio 5: race condition + Lock
    ├── daemons.py             ← ejercicio 6: hilo daemon vs no-daemon
    ├── productor_consumidor.py← ejercicio 7: Queue productor/consumidor
    ├── threading_local.py     ← ejercicio 8: threading.local() por request
    └── descargador_paralelo.py← ejercicio 9: pool de threads para HTTP (OBLIGATORIO)
```

## Orden de lectura recomendado

1. **`contenido.md`** — fundamental entender el GIL.
2. **`ejercicios.md`** — el 9 (descargador paralelo) es **obligatorio**.
3. **`autoevaluacion.md`**.

## Thread vs Proceso

| Característica | Proceso | Hilo |
|----------------|---------|------|
| Memoria | Separada (COW) | Compartida |
| Comunicación | IPC explícito | Variables directas |
| Costo de creación | Alto (~ms) | Bajo (~µs) |
| Aislamiento | Alto | Bajo |
| Paralelismo real (CPU-bound) | **Sí** | **No** (GIL) |
| Paralelismo real (I/O-bound) | Sí | **Sí** |

## El GIL en una línea

El **Global Interpreter Lock** (GIL) garantiza que **solo un hilo ejecuta bytecode Python a la vez**. Esto significa:

- **CPU-bound** (cálculo, procesamiento): threading no acelera (o empeora).
- **I/O-bound** (red, disco, sleep): threading sí acelera.

Para CPU-bound → `multiprocessing`. Para I/O-bound → `threading`.

## Race condition clásica

```python
import threading

saldo = 1000

def retirar(monto):
    global saldo
    if saldo >= monto:    # 1. Lee saldo
        time.sleep(0.001) # 2. Ventana de vulnerabilidad
        saldo -= monto    # 3. Escribe saldo
```

10 hilos retirando $200 cada uno → saldo final puede ser **negativo**. Solución: `with threading.Lock():`.

## Cuándo usar cada primitiva

| Primitiva | Caso de uso |
|-----------|-------------|
| `Lock` | Exclusión mutua básica |
| `RLock` | Lock re-entrante (la misma thread puede adquirirlo varias veces) |
| `Event` | Notificar a uno o varios hilos de que algo ocurrió |
| `Condition` | Productor-consumidor con espera condicional |
| `Semaphore` | Limitar acceso a N recursos |
| `Barrier` | Sincronizar N hilos en un punto común |
| `Queue` | Productor-consumidor (thread-safe por diseño) |

## Próxima clase

**Clase 11: Sincronización avanzada** — `Condition`, `Semaphore`, `Barrier`, `Event`, `ReadWriteLock`, deadlocks.

---

*Computación II - 2026 - Clase 10*
