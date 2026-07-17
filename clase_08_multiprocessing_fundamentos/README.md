# Clase 8: Multiprocessing — Fundamentos

Material de la octava clase de Computación II (2026) — La API de alto nivel: `Process`, `Queue`, `Pipe`, `set_start_method`.

## Estructura

```
clase_08_multiprocessing_fundamentos/
├── README.md                  ← este archivo
├── contenido.md               ← teoría: Process, Queue, Pipe, start methods
├── ejercicios.md              ← 5 ejercicios prácticos
├── autoevaluacion.md          ← quiz
├── extra_manijas.md           ← material opcional
└── scripts/
    ├── primer_process.py      ← ejercicio 1: Process básico
    ├── cinco_workers.py       ← ejercicio 2: 5 workers en paralelo
    ├── productor_consumidor.py← ejercicio 3: Queue productor/consumidor
    ├── pipe_pingpong.py       ← ejercicio 4: Pipe bidireccional
    └── fork_vs_spawn.py       ← ejercicio 5: comparar start methods
```

## Orden de lectura recomendado

1. **`contenido.md`** — base de toda la programación paralela en Python.
2. **`ejercicios.md`** — los 5 son cortos, hacelos todos.
3. **`autoevaluacion.md`**.

## Por qué `multiprocessing` y no `os.fork()`

| `os.fork()` puro | `multiprocessing` |
|------------------|-------------------|
| Solo Linux/macOS | Portable (Win/Mac/Linux) |
| Manejo manual de wait/zombies | Automático |
| IPC a mano | `Queue`/`Pipe` integrados |
| Sin sincronización | `Lock`/`Semaphore`/`Event` |

## `Process`: el bloque básico

```python
from multiprocessing import Process

def tarea(nombre):
    print(f"[{nombre}] PID={os.getpid()}")
    time.sleep(2)

if __name__ == "__main__":
    p = Process(target=tarea, args=("worker",))
    p.start()
    p.join()  # esperar
    print(f"exitcode={p.exitcode}")
```

## Por qué `if __name__ == "__main__":`

En Windows y macOS (con `spawn`) el proceso hijo **reimporta el módulo**. Sin el guard, se crean procesos infinitamente. Aunque en Linux con `fork` no hace falta, es buena práctica incluirlo.

## IPC: `Queue` vs `Pipe`

| | `Queue` | `Pipe` |
|-|---------|--------|
| Comunicación | Muchos↔muchos | Dos procesos (un par `Pipe` ↔ dos extremos) |
| Hilos/procesos | Sí | Sí |
| Thread-safe | Sí | No (cada extremo es seguro, pero ojo) |
| Uso típico | Pool de workers | Ping-pong padre↔hijo |

## Start methods

| Método | Disponible en | Costo inicial | Memoria |
|--------|--------------|---------------|---------|
| `fork` | Linux, macOS | Bajo (COW) | Comparte memoria |
| `spawn` | Todas | Alto (reimporta) | Independiente |
| `forkserver` | Linux, macOS | Medio | Comparte con servidor |

## Próxima clase

**Clase 9: Multiprocessing avanzado** — `Pool`, `Manager`, memoria compartida, Map-Reduce.

---

*Computación II - 2026 - Clase 8*
