# Clase 9: Multiprocessing — Avanzado

Material de la novena clase de Computación II (2026) — `Pool`, `Manager`, memoria compartida con `Value`/`Array`, patrones Map-Reduce y Pipeline.

## Estructura

```
clase_09_multiprocessing_avanzado/
├── README.md                  ← este archivo
├── contenido.md               ← teoría: Pool, Manager, Value, Array, patrones
├── ejercicios.md              ← 7 ejercicios (5: procesador de imágenes obligatorio)
├── autoevaluacion.md          ← quiz
├── extra_manijas.md           ← material opcional
└── scripts/
    ├── pool_methods.py        ← ejercicio 1: map/imap/starmap/apply_async
    ├── speedup_cpu.py         ← ejercicio 2: speedup con tareas CPU-bound
    ├── value_array_lock.py    ← ejercicio 3: Value con get_lock, Array particionado
    ├── manager_dict_list.py   ← ejercicio 4: Manager.dict y Manager.list
    ├── procesador_imagenes.py ← ejercicio 5: Pool.map con blur 3x3 (OBLIGATORIO)
    ├── map_reduce_palabras.py ← ejercicio 6: Map-Reduce word count
    └── pipeline_3_etapas.py   ← ejercicio 7: pipeline con Queue
```

## Orden de lectura recomendado

1. **`contenido.md`** — entendé bien la diferencia entre métodos de Pool.
2. **`ejercicios.md`** — el 5 (procesador de imágenes) es **obligatorio**.
3. **`autoevaluacion.md`**.

## Métodos de Pool — cuándo usar cada uno

| Método | Devuelve | Orden | Bloquea | Args |
|--------|----------|-------|---------|------|
| `map` | Lista al final | Preservado | Sí | 1 arg |
| `map_async` | `AsyncResult` | Preservado | No | 1 arg |
| `imap` | Iterador | Preservado | Sobre cada item | 1 arg |
| `imap_unordered` | Iterador | Por terminación | Sobre cada item | 1 arg |
| `starmap` | Lista al final | Preservado | Sí | N args (tupla) |
| `apply_async` | `AsyncResult` | N/A (1 tarea) | No | N args |

**Regla práctica:**
- ¿Una tarea por elemento, espero todo? → `map`
- ¿Streaming, no me importa el orden? → `imap_unordered`
- ¿Una sola tarea asíncrona? → `apply_async`

## Memoria compartida: cuándo cada uno

| Primitiva | Velocidad | Sincronización | Uso |
|-----------|-----------|----------------|-----|
| `Value('i', 0)` | Muy rápida | `get_lock()` incluido | Contadores, flags |
| `Array('i', n)` | Muy rápida | Manual | Buffers numéricos |
| `Manager().dict()` | Lenta (serializa) | Automática | Estructuras complejas |
| `Manager().list()` | Lenta (serializa) | Automática | Listas heterogéneas |

## Patrones

### Map-Reduce
```
textos → [mapper, mapper, mapper] → [reduce, reduce] → resultado
```
Cada proceso cuenta palabras de un texto; después se combinan los conteos.

### Pipeline
```
entrada → [etapa1] → [etapa2] → [etapa3] → salida
```
Cada etapa es un proceso que se comunica con el siguiente por una `Queue`.

## Próxima clase

**Clase 10: Threading** — concurrencia dentro del proceso, GIL, race conditions y `Lock`.

---

*Computación II - 2026 - Clase 9*
