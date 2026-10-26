# Trabajo Práctico Nº 2: Plataforma de Tareas Distribuidas

**Cátedra de Computación II — Universidad de Mendoza — Ciclo 2026**  
**Alumno:** Manuel Quercetti  
**Plataforma de Ejecución:** Python 3.11+ / Docker & Docker Compose  

---

## 1. Descripción del Sistema y Modo de Uso

El presente trabajo práctico implementa una **plataforma asíncrona de procesamiento de tareas distribuidas** construida sobre **FastAPI** y el motor asíncrono **`asyncio`** de Python.

El servicio permite a múltiples clientes HTTP encolar tareas de distinta naturaleza (I/O intensivo, cómputo intensivo en CPU e I/O simulado), ejecutándolas concurrentemente a través de un **pool de workers asíncronos** desacoplados mediante una **`asyncio.Queue`**.

### Características Principales

1. **API REST Asíncrona con FastAPI:** Encolado inmediato con código de estado HTTP `202 Accepted` sin retener la conexión del cliente mientras la tarea se procesa.
2. **Pool de Workers Asíncronos:** Corrutinas consumidoras concurrentes que compiten cooperativamente por la cola de trabajo compartida.
3. **Desacoplamiento de Cómputo CPU-Bound:** Aislamiento de tareas intensivas de cómputo en un `concurrent.futures.ProcessPoolExecutor` para evitar el congelamiento del *event loop* y eludir la barrera del GIL (*Global Interpreter Lock*).
4. **Cancelación Limpia y Timeouts:** Soporte para cancelar tareas en cola o en plena ejecución vía `DELETE /tareas/{id}` y expiración automática mediante `asyncio.wait_for`.
5. **Apagado Ordenado (*Graceful Shutdown*):** Captura de señales de terminación (`SIGTERM`/`SIGINT`), finalización de tareas en curso con tiempo de gracia y persistencia del estado en disco (`dumps/estado_<timestamp>.json`).
6. **Dockerización Completa:** Ejecución estandarizada mediante `docker compose up --build`.

---

## 2. Diagrama de Arquitectura

```
                        Cliente HTTP (curl / navegador / benchmark)
                                            │
                                            ▼
               ┌────────────────────────────────────────────────────────┐
               │                   FastAPI Application                  │
               │   POST /tareas | GET /tareas | GET /tareas/{id}        │
               │   DELETE /tareas/{id} | GET /estadisticas              │
               └────────────────────────────┬───────────────────────────┘
                                            │
                                            ▼
                       ┌────────────────────────────────────────┐
                       │          TaskManager (Service)         │
                       │ - Almacén en memoria: Dict[UUID, Tarea]│
                       │ - Registro de asyncio.Task en curso    │
                       │ - Métricas y estadísticas agregadas    │
                       └──────────────┬──────────────────┬──────┘
                                      │                  │
                (Encolar Tarea)       ▼                  ▼ (Cancelar asyncio.Task)
                         ┌─────────────────┐      ┌─────────────┐
                         │  asyncio.Queue  │      │ cancel()    │
                         └────────┬────────┘      └─────────────┘
                                  │
                                  ▼ (consume)
               ┌────────────────────────────────────────────────────────┐
               │               Worker Pool (N Corrutinas)               │
               │                                                        │
               │  ┌─────────────────┐ ┌─────────────────┐ ┌──────────┐  │
               │  │    Worker 0     │ │    Worker 1     │ │ Worker N │  │
               │  └────────┬────────┘ └────────┬────────┘ └────┬─────┘  │
               └───────────┼───────────────────┼───────────────┼────────┘
                           │                   │               │
            ┌──────────────┴───────────────────┴───────────────┴────────┐
            │                     Dispatcher de Tareas                  │
            └───────┬──────────────────────────┬─────────────────┬──────┘
                    │                          │                 │
                    ▼                          ▼                 ▼
          ┌───────────────────┐      ┌──────────────────┐  ┌─────────────┐
          │     descargar     │      │     hashear      │  │   esperar   │
          │    (I/O-bound)    │      │   (CPU-bound)    │  │(I/O simul.) │
          │  httpx.AsyncClient│      │run_in_executor   │  │asyncio.sleep│
          │  gather() URLs    │      │ProcessPoolExec   │  │             │
          └───────────────────┘      └──────────────────┘  └─────────────┘
```

---

## 3. Guía de Ejecución y Ejemplos de Uso (`curl`)

### Opción A: Ejecución en Docker (Recomendada)

```bash
# Levantar el servicio y compilar la imagen
docker compose up --build

# El servicio queda expuesto en http://localhost:8000
```

### Opción B: Ejecución Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor Uvicorn
python src/main.py
```

### Ejemplos de `curl`

#### 1. Encolar tarea I/O-bound (`descargar`)
```bash
curl -X POST http://localhost:8000/tareas \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "descargar",
    "urls": [
      "https://httpbin.org/status/200",
      "https://httpbin.org/status/201",
      "https://httpbin.org/delay/1"
    ]
  }'
```

#### 2. Encolar tarea CPU-bound (`hashear`)
```bash
curl -X POST http://localhost:8000/tareas \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "hashear",
    "texto": "Computacion-II-2026",
    "iteraciones": 500000
  }'
```

#### 3. Encolar tarea I/O simulado (`esperar`) con timeout
```bash
curl -X POST http://localhost:8000/tareas \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "esperar",
    "segundos": 10.0,
    "timeout": 5.0
  }'
```

#### 4. Consultar estado y resultado de una tarea
```bash
curl http://localhost:8000/tareas/<ID_DE_LA_TAREA>
```

#### 5. Cancelar una tarea en cola o en ejecución
```bash
curl -X DELETE http://localhost:8000/tareas/<ID_DE_LA_TAREA>
```

#### 6. Listar todas las tareas (con filtro opcional)
```bash
# Todas
curl http://localhost:8000/tareas

# Filtrar por estado completada
curl "http://localhost:8000/tareas?estado=completada"
```

#### 7. Consultar estadísticas globales del sistema
```bash
curl http://localhost:8000/estadisticas
```

---

## 4. Decisiones de Diseño Fundamentadas

### ¿Por qué `asyncio.Queue` y no `queue.Queue`?
`queue.Queue` de la biblioteca estándar de Python está diseñada para concurrencia basada en hilos (`threading`). Sus métodos `get()` y `put()` bloquean el hilo del sistema operativo mediante primitivas de sincronización pesadas (`threading.Condition`). Si una corrutina invoca `queue.Queue.get()`, **congelaría por completo el único hilo del event loop**, impidiendo que cualquier otro cliente o corrutina continúe su ejecución.  
En cambio, `asyncio.Queue` es puramente asíncrona: `await cola.get()` cede cooperativamente el control del loop hasta que un ítem esté disponible, permitiendo atender cientos de peticiones simultáneas.

### ¿Por qué el pool de workers no necesita un `Lock`?
A diferencia de los hilos de sistema donde el planificador del kernel puede interrumpir la ejecución en cualquier instrucción en código máquina (generando *race conditions*), en `asyncio` la concurrencia es **cooperativa**. El cambio de contexto solo puede ocurrir en puntos de suspensión explícitos marcados con la palabra clave `await`.  
Como las operaciones de extracción de tareas, actualización de contadores y mutación de diccionarios en memoria no contienen `await` intermedio, se ejecutan de manera atómica respecto del event loop, eliminando la necesidad de `threading.Lock` o `asyncio.Lock` para proteger las estructuras internas del pool.

### ¿Cómo evitamos que una tarea CPU-bound congele la API?
Python tradicional (CPython) cuenta con el GIL (*Global Interpreter Lock*), el cual restringe la ejecución de bytecode a un único hilo a la vez. Incluso si ejecutáramos la función `hashear` en un thread mediante `asyncio.to_thread` o `ThreadPoolExecutor`, la saturación de CPU degradaría severamente el event loop y no aprovecharía múltiples núcleos.  
Por esta razón, empleamos `concurrent.futures.ProcessPoolExecutor` invocado con `await loop.run_in_executor(...)`. Esto delega el cálculo matemático a procesos hijos del sistema operativo independientes, con su propio espacio de memoria e intérprete Python libre del GIL, manteniendo la latencia del event loop en el rango de los milisegundos.

### ¿Cómo implementamos la cancelación limpia y qué pasa con los recursos?
Mantenemos un registro de las corrutinas en vuelo (`dict[str, asyncio.Task]`). Cuando el usuario envía `DELETE /tareas/{id}`:
1. Si la tarea está aún en la cola (`pendiente`), se marca directamente como `cancelada` para que el worker la ignore al extraerla.
2. Si está en ejecución, se llama a `task.cancel()`. Esto inyecta una excepción `asyncio.CancelledError` en el punto de suspensión del worker.
3. La tarea de descarga (`httpx.AsyncClient`) y la de espera manejan context managers asíncronos (`async with`), garantizando el cierre inmediato y ordenado de sockets TCP y conexiones sin dejar descriptores de archivo huérfanos.

### ¿Qué pasa si un worker lanza una excepción no capturada?
Cada iteración del `_worker_loop` está envuelta en un bloque `try ... except Exception as e`. Si una tarea falla de manera imprevista (por ejemplo, error de sintaxis, caída imprevista de red no controlada, etc.), el worker captura la excepción, marca la tarea como `fallida`, registra el detalle en el campo `error`, notifica a la cola con `task_done()` y continúa ejecutando la siguiente tarea. El worker nunca muere.

---

## 5. Mediciones Obligatorias y Análisis

Las siguientes mediciones fueron obtenidas ejecutando el script [`benchmarks/benchmark_mediciones.py`](file:///c:/Users/mquer/OneDrive/Documentos/Proyectos/Escuela/Computacion-2/trabajos_practicos/TP2_tareas/benchmarks/benchmark_mediciones.py).

### Medición 1: Concurrencia I/O (20 descargas de red)

Se ejecutaron 20 peticiones HTTP a endpoints de prueba de red, comparando el enfoque secuencial tradicional contra el concurrente con `asyncio.gather`.

| Modo de Ejecución | Tiempo Total (s) | Speedup Obtenido |
|-------------------|------------------|------------------|
| **Secuencial** (`for` + `await`) | **4.086 s** | 1.00x (base) |
| **Concurrente** (`asyncio.gather`) | **1.138 s** | **3.59x** |

**Interpretación:** En el modo secuencial, cada petición debe esperar el *Round Trip Time* (RTT) de la anterior (suma de tiempos individuales). En el modo concurrente, todas las solicitudes vuelan simultáneamente por la red; el tiempo total está acotado por la latencia de la descarga más lenta más el overhead de multiplexación, logrando una aceleración de **3.59x**.

---

### Medición 2: Event Loop Bloqueado por Tarea CPU-Bound

Se midió la latencia máxima experimentada por el event loop para responder a eventos del sistema mientras se ejecutaba un cálculo iterativo pesado de SHA-256 (1.500.000 iteraciones, ~1.1 segundos de cómputo neto):

| Estrategia de Cómputo CPU | Duración Cómputo | Latencia Máxima del Event Loop | Impacto en la API |
|---------------------------|------------------|--------------------------------|-------------------|
| **Directo en el Event Loop** (Sin executor) | 1.0982 s | **1.0983 s** | **API Congelada**: No responde a peticiones HTTP |
| **ProcessPoolExecutor** (`run_in_executor`) | 1.0982 s | **0.0394 s** | **Totalmente Fluida**: Latencia menor a 40 ms |

**Interpretación:** Cuando una función CPU-bound corre directo en el loop, monopoliza el hilo y ninguna otra corrutina (incluyendo el servidor HTTP de FastAPI/Uvicorn) puede recibir tiempo de CPU. Al derivarla al `ProcessPoolExecutor`, el cálculo corre en un proceso separado del SO, permitiendo que el event loop atienda tráfico de red en menos de 40 milisegundos.

---

### Medición 3: Techo del Pool de Workers y Análisis de Saturación

Se encolaron ráfagas crecientes de tareas en un pool configurado con **4 workers**:

| Tareas encoladas ($N$) | Tiempo de cada tarea | Tiempo Total de Procesamiento | Throughput Real (tareas/s) |
|------------------------|----------------------|-------------------------------|-----------------------------|
| **10 tareas** | 0.1 s | 0.323 s | **30.9 tareas/s** |
| **20 tareas** | 0.1 s | 0.484 s | **41.3 tareas/s** |
| **50 tareas** | 0.1 s | 1.286 s | **38.9 tareas/s** |
| **100 tareas** | 0.1 s | 2.412 s | **41.5 tareas/s** |

**Interpretación del límite:**  
Teóricamente, 4 workers procesando tareas de $0.1\text{ s}$ rinden un techo máximo ideal de:
$$\text{Throughput teórico} = \frac{4\text{ workers}}{0.1\text{ s}} = 40\text{ tareas/segundo}$$
Los resultados empíricos muestran que el sistema alcanza de forma consistente entre **38 y 41.5 tareas/s**.  
**¿Dónde está el límite y qué se satura?** El límite lo impone el número de workers concurrentes ($W=4$). Cuando $N$ supera a $W$, las tareas excedentes deben esperar en la `asyncio.Queue` su turno de ejecución. Si se incrementara la carga a 100.000 tareas instantáneas, la memoria RAM requerida para albergar los objetos en cola y el tiempo de despacho en memoria se convertirían en el primer cuello de botella antes de que el event loop sufra degradación.

---

## 6. Conceptos del Curso Aplicados

1. **Clase 11 (Sincronización):** Se implementó el patrón **Productor-Consumidor**. Los endpoints HTTP actúan como productores encolando en `asyncio.Queue`, y las corrutinas del pool actúan como consumidores. No se requieren cerrojos (*locks*) porque el cambio de contexto es puramente cooperativo.
2. **Clase 17 (I/O Multiplexing - `select`/`epoll`):** Base fundamental del event loop de asyncio. En lugar de bloquear un hilo por cada socket de red en `descargar`, el loop registra los descriptores de archivo en el mecanismo de multiplexación del kernel y solo despierta cuando hay datos listos para leer.
3. **Clase 18 (De yield a asyncio):** Comprensión profunda de cómo las corrutinas operan como generadores cooperativos con delegación de control mediante `await`, suspendiendo su estado sin consumir ciclos de CPU mientras esperan I/O.
4. **Clase 19 (HTTP y FastAPI):** Diseño de la API REST, inyección de dependencias, tipado con Pydantic y gestión del ciclo de vida de la aplicación con `lifespan`.
5. **Clase 21 y 22 (Asyncio Avanzado y `concurrent.futures`):** Uso de `run_in_executor` acoplado a un `ProcessPoolExecutor` para eludir las restricciones del GIL en Python y ejecución de pruebas de cancelación con propagación limpia de `asyncio.CancelledError`.

---

## 7. Limitaciones Conocidas

- **Almacenamiento en Memoria:** Las tareas activas y finalizadas se mantienen en el heap del proceso. Ante millones de tareas completadas acumuladas, la memoria crecería de forma no acotada (en un entorno productivo requeriría paginación con TTL o expulsión por política LRU).
- **Persistencia en Apagado No Transaccional:** El volcado a JSON ocurre durante el shutdown; si el proceso sufre un fallo catastrófico instantáneo (`kill -9`), las tareas encoladas que no se hayan volcado se perderán.
- **Límite de Procesos de CPU:** El pool de procesos hijos está acotado por la cantidad de cores físicos del procesador host. Encolar cientos de tareas CPU-bound formará una fila de espera en el executor.

---

## 8. Conclusiones y Aprendizaje Personal

La realización de este trabajo práctico permitió consolidar de forma práctica la diferencia fundamental entre concurrencia de entrada/salida (I/O-bound) y paralelismo de cómputo (CPU-bound). Durante el cursado se estudiaron sockets, multiplexado con `select`/`epoll` y el funcionamiento interno de las corrutinas; construir esta plataforma integró todos esos conceptos en una arquitectura sólida.

Comprobar empíricamente que una tarea CPU-bound sin executor puede congelar por completo un servidor asíncrono demostró por qué `asyncio` no es una solución mágica para todo problema de concurrencia, y por qué el uso de `ProcessPoolExecutor` o workers distribuidos externos resulta indispensable en arquitecturas de backend modernas.

Asimismo, dominar la cancelación limpia mediante `asyncio.CancelledError` y la sincronización sin locks a través de colas cooperativas reforzó la importancia del diseño arquitectónico por sobre la simple escritura de código.
