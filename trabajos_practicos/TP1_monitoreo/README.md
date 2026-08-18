# Trabajo Práctico Nº 1 — Monitor de Procesos y Threads

**Computación II — Universidad de Mendoza — 2026**
**Alumno:** Ignacio Quercetti

Monitor de sistema en tiempo real estilo `htop` que muestra la anatomía interna
de procesos y threads leyendo `/proc` directamente. Sistema multiproceso con
7 analizadores + TUI + manejo de 5 señales.

---

## Cómo arrancar

```bash
docker compose up --build
```

Esto levanta el contenedor, monta `config.json` como sólo-lectura y `dumps/`
para que SIGUSR1 pueda escribir snapshots. Dentro del container corre
`python -m src.main`, que arranca:

1. el **Recolector** (lista `/proc` cada 1s),
2. los **7 analizadores** en procesos separados (`spawn`),
3. el **Display TUI** (proceso principal, render con `rich`).

Para salir limpiamente: `q` (o `Ctrl+C` desde otra terminal con
`docker compose kill --signal=SIGTERM monitor`).

Probar las señales desde otra terminal:

```bash
PID=$(docker inspect -f '{{.State.Pid}}' monitor)
kill -SIGHUP  $PID    # recarga config.json
kill -SIGUSR1 $PID    # dump_<ts>.json en ./dumps/
kill -SIGUSR2 $PID    # toggle verbose
kill -SIGTERM $PID    # shutdown limpio
```

Tests sin Docker (los que pueden correr en Linux nativo):

```bash
python -m pytest tests/ -v
```

---

## Arquitectura

```
Recolector (lista /proc cada 1s)
   └──► mp.Queue(maxsize=2)  ──►  7 wrappers analizadores (uno por vista)
                                          │
                                          ▼
                                  Snapshot global (Manager.dict con 7 slots)
                                          │
                                          ▼
                                  Display TUI (rich, 4 fps)
```

Cada analizador es un **proceso independiente** (no thread). El wrapper
`_wrapper_analizador` (`src/main.py:70-90`) consume la `mp.Queue`,
drena los PIDs viejos con `get_nowait()` y llama al `target(pids, ...)` del
analizador.

### Decisiones de diseño (y por qué)

#### `spawn`, no `fork`

`src/main.py:199-203` fuerza `mp.set_start_method("spawn", force=True)`.
En Linux `fork` es el default y es más rápido al arrancar, pero hereda
todo el estado del padre: handlers de señales, locks tomados, threads
vivos, descriptores abiertos. `spawn` arranca un intérprete limpio y
picklea solo lo que recibe por argumento. Es más lento al levantar
pero hace imposible heredar estado raro que dispare races en los
analizadores. Para un sistema donde cada analizador vive durante
toda la sesión del monitor y toca primitivas IPC, el costo vale la pena.

#### `Manager.dict` para el snapshot, `Value('d')` para los intervalos

El snapshot compartido entre 7+1 procesos necesita reemplazo atómico
por entrada: cada analizador publica un dict completo en su slot
(`agregador.escribir_slot` hace `snapshot[slot] = {"ts": ..., "datos": ...}`
de una). El `Manager.dict` garantiza que la asignación es atómica vista
desde otro proceso (lock interno).

Los intervalos son un solo float por slot y se leen/escriben muy seguido
(la TUI los modifica con `+`/`-`). `Value('d')` con su lock interno es
más liviano que un `Manager.dict` para escalar a 60 Hz de updates.

#### Queue latest-only (`maxsize=2` + drain-before-put)

`recolector.py:40-46` drena la queue antes de publicar la nueva foto.
Si el analizador de señales (intervalo 10s) está durmiendo cuando el
recolector publica 10 lotes, al despertar consume el más reciente y
descarta los 9 rancios. Con `maxsize=2` el productor tampoco bloquea
más de un ciclo. Es el patrón clásico para fuentes de datos que
cambian rápido y consumidores lentos.

#### `Value('b')` para el flag verbose (toggled por SIGUSR2)

Un único byte compartido entre todos los procesos. SIGUSR2 lo flipa
desde el handler del proceso padre; los analizadores/display lo leen
cuando quieren. No necesita Manager porque es un solo escalar.

#### Race conditions: cómo las evitamos

- **Snapshot**: cada analizador pisa su slot completo (`snapshot[slot] = {...}`),
  no mergeea in-place. El lector (`display.py`) copia a local antes de iterar.
- **CPU% previo**: el dict `prev` en `resumen.py`/`threads.py`/`sistema.py` es
  **local al proceso del analizador**, no compartido. Cada vuelta se calcula
  contra la lectura anterior del mismo proceso.
- **`top_cpu`/`top_mem`**: copio el `Manager.dict` a dict Python local
  (`dict(resumen_slot.get("datos", {}))`) antes de `sorted()`. El `Manager`
  puede mutar durante la ordenación y romper la iteración; copiar primero
  cierra esa ventana.
- **Self-pipe codificado en byte**: `senales.py:62-65` hace
  `os.write(w_fd, bytes([signum & 0xFF]))`. Una sola syscall,
  sin string formatting ni malloc en el handler — sigue siendo
  async-signal-safe.

---

## Qué leemos de `/proc`

Tabla archivo → campo → vista que lo consume. Es la parte que la cátedra
pondera 15%.

| Archivo | Campo(s) | Vista |
|---|---|---|
| `/proc/[pid]/stat` | `state, ppid, pgrp, session, minflt, majflt, utime, stime, priority, nice, policy, comm` | resumen, threads, scheduling, sistema |
| `/proc/[pid]/status` | `Threads, Uid, SigBlk, SigIgn, SigCgt, SigPnd, ShdPnd, voluntary_ctxt_switches, nonvoluntary_ctxt_switches, Cpus_allowed_list, VmSize, VmRSS, VmData, VmStk, VmExe, VmLib, VmHWM, VmSwap` | resumen, senales, memoria, scheduling |
| `/proc/[pid]/cmdline` | (argumentos concatenados) | resumen |
| `/proc/[pid]/fd/*` | symlinks a `socket:`, `pipe:`, archivos, `/dev/tty`... | fds |
| `/proc/[pid]/task/[tid]/stat` | `state, utime, stime, comm` | threads |
| `/proc/[pid]/maps` | regiones con permisos y etiquetas (`[heap]`, `[stack]`, `[vdso]`, paths) | memoria |
| `/proc/stat` | línea `cpu` (todos los jiffies) + `btime` | sistema |
| `/proc/meminfo` | MemTotal, MemFree, MemAvailable, Buffers, Cached, SwapTotal, SwapFree | sistema |
| `/proc/loadavg` | 1min/5min/15min, running/total | sistema |
| `/proc/uptime` | uptime_seg, idle_seg | sistema |

`procfs.py` centraliza todas las lecturas. Cada función tolera que el
proceso desaparezca entre `listar_pids()` y `leer_xxx(pid)` devolviendo
`{}` o `""` (los analizadores filtran con `if not stat: continue`).

---

## Keybindings

| Tecla | Acción |
|---|---|
| `1`–`7` o `r/m/f/t/s/p/g` | Cambiar de vista |
| `c` | Ciclar orden: `cpu_pct` → `vm_rss` → `pid` |
| `+` / `-` | Acelerar / desacelerar el intervalo de la vista activa |
| `↑` / `↓` | Mover la fila seleccionada |
| `Enter` | Pin / unpin del PID seleccionado |
| `Esc` | Soltar el pin (si hay) o cancelar input |
| `/` | Entrar en modo input: filtro por comando. Enter confirma, Esc cancela |
| `u` | Entrar en modo input: filtro por uid |
| `h` / `?` | Mostrar ayuda en el header |
| `q` (o `Ctrl+C`) | Salir limpio |

El thread de teclado (`display._teclado_thread`) pone `stdin` en
`tty.setcbreak` cuando es una TTY real, así las flechas llegan crudas
como secuencias `ESC [ A/B` y las decodificamos a tokens `KEY_UP` /
`KEY_DOWN`. Si stdin no es TTY (pipe/redir) cae al modo simple: las
flechas no andan pero el resto sí.

---

## 5 señales

| Señal | Acción |
|---|---|
| `SIGINT` (Ctrl+C) | Shutdown limpio: setea `stop_event`, `_shutdown` mata hijos |
| `SIGTERM` | Idem |
| `SIGHUP` | Recarga `config.json` (los `Value('d')` de intervalos se actualizan sin reiniciar) |
| `SIGUSR1` | Dump del snapshot a `dump_<timestamp>.json` en `./dumps/` (el volumen montado) |
| `SIGUSR2` | Toggle del flag `verbose` (Manager Value compartido) |

Implementación: `src/senales.py` con el patrón self-pipe. El handler
es mínimo (1 byte), el procesamiento real corre en el loop de señales
del proceso padre (`main.py:147-170`).

---

## Limitaciones

Las mismas que detecté durante el desarrollo. Sería mala idea no
documentarlas:

- **Primer sample de CPU% siempre es 0.0.** No hay delta posible
  hasta la segunda vuelta. Comportamiento esperado y documentado en
  el código (`resumen.py:analizar`).
- **`/proc/[pid]/maps` se parsea entero cada 3s.** En procesos
  pesados (postgres, java) puede ser miles de líneas y unos pocos MB.
  Para reducir overhead habría que cachear por `(pid, mtime)` o usar
  `smaps_rollup` si está disponible. No lo implementé por scope.
- **El segmento `[heap]` puede ser muy grande** y aparece mezclado con
  paths de archivos anónimos. La agregación es por etiqueta, no por
  permisos (rwx) ni por tipo de mapping (text/data/bss). Para algo más
  fino se necesita `/proc/[pid]/smaps` con sus campos `Size`, `Rss`,
  `Pss`, `Swap`.
- **El thread de teclado cae al modo simple si stdin no es TTY.**
  En `docker compose logs`, `docker attach`, o cualquier pipe, las
  flechas no funcionan (se mandan como 3 bytes literales). Decisión
  consciente: las flechas son para uso interactivo.
- **El PID del propio monitor aparece en la lista de procesos.** No
  lo filtramos — es lo que `listar_pids()` devuelve. Es decisión de
  diseño (queremos ver el monitor en el monitor).
- **El `verbose` flag lo togglean SIGUSR2 y nada más.** No hay tecla
  `v` desde la TUI para alternarlo sin mandar señal. Mejora futura.
- **`instalar_manejadores(pid_display=...)` no se usa.** El parámetro
  existe para una idea original de que el display hiciera el dump
  él mismo, pero hoy el dump lo hace el proceso padre con
  `_dump_snapshot`. No es bug, es API no usada.

---

## Criterios de evaluación (conservados del README de la cátedra)

| Ítem | Peso |
|---|---|
| Funcionalidad (7 vistas, navegación) | 30% |
| Arquitectura multiproceso, IPC, sin race conditions | 25% |
| 5 señales funcionando | 10% |
| Lectura correcta de /proc | 15% |
| README con justificación y conexión a la teoría | 15% |
| Código limpio | 5% |
| Bonus (extensiones) | +10% |

---

## Estructura del proyecto

```
trabajos_practicos/TP1_monitoreo/
├── Dockerfile
├── docker-compose.yml
├── config.json
├── requirements.txt
├── README.md              ← este archivo
├── consigna.md            ← especificación completa del TP
├── consigna_macos.md      ← instrucciones específicas para macOS
├── prompt_tutor_ia.md     ← prompt para usar una IA como tutor
├── src/
│   ├── main.py            ← entry point, lanza 7 procesos + display
│   ├── recolector.py      ← lista /proc y publica en mp.Queue (latest-only)
│   ├── senales.py         ← self-pipe + handlers para 5 señales
│   ├── procfs.py          ← helpers de lectura de /proc (stat, status, maps, …)
│   ├── agregador.py       ← Manager.dict snapshot + Value('d') intervalos + lock
│   ├── display.py         ← TUI con rich + dispatcher de teclas
│   └── analizadores/
│       ├── resumen.py
│       ├── memoria.py
│       ├── fds.py
│       ├── threads.py
│       ├── senales.py
│       ├── scheduling.py
│       └── sistema.py
├── tests/
│   ├── test_procfs.py
│   ├── test_agregador.py
│   └── test_senales.py
└── dumps/                 ← donde SIGUSR1 escribe snapshots
```

---

*Trabajo Práctico Nº 1 — Computación II — 2026 — Ignacio Quercetti*
