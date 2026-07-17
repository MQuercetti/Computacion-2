# Clase 11: Sincronización — Avanzada

Material de la undécima clase de Computación II (2026) — `Condition`, `Semaphore`, `Barrier`, `Event`, `ReadWriteLock`, deadlocks.

## Estructura

```
clase_11_sincronizacion_1/
├── README.md                  ← este archivo
├── contenido.md               ← teoría: primitivas avanzadas, deadlocks, starvation
├── ejercicios.md              ← 6 ejercicios (5: Readers-Writers obligatorio)
├── autoevaluacion.md          ← quiz
├── extra_manijas.md           ← material opcional
├── demo_race_condition.py     ← demo empírica de race condition
└── scripts/
    ├── cuenta_insegura.py     ← ejercicio 1.1: race condition bancaria
    ├── cuenta_segura.py       ← ejercicio 1.2: Lock como solución
    ├── condition_pc.py        ← ejercicio 2: productor-consumidor con Condition
    ├── barrier_fases.py       ← ejercicio 3: Barrier para fases paralelas
    ├── connection_pool.py     ← ejercicio 4: Semaphore como pool de conexiones
    ├── read_write_lock.py     ← ejercicio 5: Readers-Writers Lock (OBLIGATORIO)
    └── deadlock_demo.py       ← ejercicio 6: demostrar y evitar deadlock
```

## Orden de lectura recomendado

1. **`contenido.md`** — todas las primitivas en detalle.
2. **`ejercicios.md`** — el 5 (Readers-Writers Lock) es **obligatorio**.
3. **`autoevaluacion.md`**.

## Tabla maestra de primitivas

| Primitiva | Caso de uso | Ejemplo típico |
|-----------|-------------|----------------|
| `Lock` | Exclusión mutua simple | `saldo += 1` |
| `RLock` | Lock re-entrante | Métodos que se llaman entre sí |
| `Condition` | Esperar a que se cumpla una condición | Cola limitada (prod/cons) |
| `Semaphore(N)` | Limitar N accesos simultáneos | Pool de conexiones |
| `Event` | Notificación one-shot | "Listo, empezá" |
| `Barrier(N)` | Sincronizar N hilos en un punto | Fin de fase de cómputo |
| `Queue` | Productor-consumidor | Cola de tareas |

## Patrones clave

### Productor-Consumidor con `Condition`
```python
cv = threading.Condition()
def put(item):
    with cv:
        while len(buffer) == MAX:
            cv.wait()       # libera el lock y duerme
        buffer.append(item)
        cv.notify()
```

### Pool de recursos con `Semaphore`
```python
sem = threading.Semaphore(3)  # máximo 3 conexiones
def usar():
    sem.acquire()
    try:
        # usar recurso
    finally:
        sem.release()
```

### Readers-Writers Lock
- Múltiples lectores simultáneos ✓
- Un solo escritor a la vez ✗ sin lectores
- Implementado con dos `Condition` y un contador de readers

## Deadlocks: las 4 condiciones (todas deben cumplirse)

1. **Exclusión mutua**: el recurso solo lo puede usar uno a la vez.
2. **Hold and wait**: un hilo agarra un lock y espera otro.
3. **No preemption**: nadie puede sacarle un lock a la fuerza.
4. **Circular wait**: A espera a B, B espera a A.

**Prevención más simple**: imponer un **orden global** de adquisición de locks.

---

*Computación II - 2026 - Clase 11*
