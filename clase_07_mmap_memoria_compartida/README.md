# Clase 7: mmap y Memoria Compartida

Material de la séptima clase de Computación II (2026) — Memoria compartida de cero copias: `mmap`, `Value`, `Array`, `SharedMemory`.

## Estructura

```
clase_07_mmap_memoria_compartida/
├── README.md                  ← este archivo
├── contenido.md               ← teoría: mmap, memoria compartida, IPC
├── ejercicios.md              ← 6 ejercicios + ejercicio de síntesis (banco)
├── autoevaluacion.md          ← quiz
├── extra_manijas.md           ← material opcional
├── ejemplo.txt                ← archivo de ejemplo para los ejercicios
└── scripts/
    ├── mmap_archivo.py        ← ejercicio 1.1: mmap sobre archivo
    ├── mmap_readonly.py       ← ejercicio 1.2: mmap solo lectura
    ├── mmap_binario.py        ← ejercicio 2.1: mmap como struct
    ├── mmap_anonimo.py        ← ejercicio 3.1: mmap anónimo con fork
    ├── mmap_hijos.py          ← ejercicio 3.2: hijos en regiones separadas
    ├── mmap_multiprocessing.py← ejercicio 4.1: mmap con Process
    ├── value_race.py          ← ejercicio 5.1: race condition con Value
    ├── array_paralelo.py      ← ejercicio 5.2: Array compartido
    ├── shared_memory.py       ← ejercicio 6.1: SharedMemory
    ├── shareable_list.py      ← ejercicio 6.2: ShareableList
    └── banco_race.py          ← ejercicio de síntesis: transferencias sin lock
```

## Orden de lectura recomendado

1. **`contenido.md`** — la base conceptual (cero copias, race conditions).
2. **`ejercicios.md`** — el 5 (Value/Array) es **obligatorio**.
3. **`autoevaluacion.md`**.

## Cuándo usar cada mecanismo de IPC

| Mecanismo | Copias | Velocidad | Sincronización | Complejidad |
|-----------|--------|-----------|----------------|-------------|
| **Pipe / FIFO** | 2 | Moderada | Implícita | Baja |
| **Queue (multiprocessing)** | 2 + pickle | Moderada | Implícita | Baja |
| **Socket** | 2 | Moderada | Manual | Media |
| **mmap / SharedMemory** | 0 | Máxima | **Manual** (peligro) | Alta |

La velocidad viene con costo: **sos responsable** de sincronizar el acceso.

## Primitivas en `multiprocessing`

| Primitiva | Uso | Tipo |
|-----------|-----|------|
| `Value(typecode, val)` | Un valor compartido | Tiene `.get_lock()` |
| `Array(typecode, n)` | Array de un tipo fijo | Manual |
| `Manager().dict()` | Dict compartido entre procesos | Lento, serializa |
| `Manager().list()` | Lista compartida | Lento, serializa |
| `shared_memory.SharedMemory` | Bytes crudos | Manual, máxima velocidad |
| `shared_memory.ShareableList` | Lista de tipos básicos | Manual |

## Race condition típica

```python
contador = Value('i', 0)

def incrementar():
    for _ in range(100_000):
        contador.value += 1   # ¡NO atómico!

# 4 procesos → valor final: depende de la suerte, siempre < 400_000
# Solución: with contador.get_lock():
```

## Próxima clase

**Clase 8: Multiprocessing fundamentos** — la API de alto nivel `multiprocessing.Process`, `Queue`, `Pipe`.

---

*Computación II - 2026 - Clase 7*
