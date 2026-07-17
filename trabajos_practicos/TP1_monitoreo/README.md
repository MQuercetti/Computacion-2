# Trabajo Práctico Nº 1 — Monitor de Procesos y Threads

**Computación II — Universidad de Mendoza — 2026**

Monitor de sistema en tiempo real estilo `htop` que muestra la anatomía interna de procesos y threads leyendo `/proc` directamente. Sistema multiproceso con 7 analizadores + TUI + manejo de señales.

## Estructura de la consigna

```
trabajos_practicos/TP1_monitoreo/
├── README.md              ← este archivo
├── consigna.md            ← especificación completa del TP
├── consigna_macos.md      ← instrucciones específicas para macOS
└── prompt_tutor_ia.md     ← prompt para usar una IA como tutor
```

## Resumen ejecutivo

| | |
|-|-|
| **Entrega** | Clase 11 (02/06/2026) |
| **Modalidad** | Individual |
| **Plataforma** | Linux (en Docker) |
| **Lenguaje** | Python 3.11+ |
| **Entrega** | Repositorio público en GitHub |

## Objetivos pedagógicos

1. Inspeccionar procesos de Linux leyendo `/proc` directamente (sin `psutil`).
2. Diseñar un sistema multiproceso (7 analizadores paralelos + TUI).
3. Comunicar procesos con `Queue`, `Pipe`, `Manager`, `Value`, `Array`.
4. Manejar señales (SIGINT, SIGTERM, SIGHUP, SIGUSR1, SIGUSR2) con shutdown limpio.
5. Identificar y resolver race conditions con primitivas de sincronización.
6. Conectar la teoría del curso con un sistema vivo.

## Arquitectura mínima obligatoria

```
Recolector (lista procesos /proc)
    │
    ├──► Analizador Resumen  (cada 2s)
    ├──► Analizador Memoria  (cada 3s)
    ├──► Analizador FDs      (cada 5s)
    ├──► Analizador Threads  (cada 2s)
    ├──► Analizador Señales  (cada 10s)
    ├──► Analizador Scheduling (cada 10s)
    └──► Analizador Sistema  (cada 2s)
            │
            ▼
      Snapshot global (Manager dict compartido)
            │
            ▼
      Display TUI (7 vistas alternables, teclas 1-7 / r,m,f,t,s,p,g)
```

## 7 vistas obligatorias

| Tecla | Vista | Refresh default |
|-------|-------|-----------------|
| `1` / `r` | Resumen | 2s |
| `2` / `m` | Memoria | 3s |
| `3` / `f` | File descriptors | 5s |
| `4` / `t` | Threads | 2s |
| `5` / `s` | Señales | 10s |
| `6` / `p` | Scheduling | 10s |
| `7` / `g` | Sistema global | 2s |

## Keybindings

| Tecla | Acción |
|-------|--------|
| `1`–`7` o `r/m/f/t/s/p/g` | Cambiar de vista |
| `↑` `↓` | Navegar por la lista |
| `Enter` | Pin del proceso seleccionado |
| `/` | Filtrar por comando |
| `u` | Filtrar por usuario |
| `c` | Toggle ordenamiento (CPU% / RSS / PID) |
| `+` / `-` | Ajustar intervalo de la vista activa |
| `q` | Salir limpiamente |
| `h` / `?` | Ayuda |

## 5 señales que el monitor debe manejar

| Señal | Acción |
|-------|--------|
| `SIGINT` (Ctrl+C) | Shutdown limpio |
| `SIGTERM` | Shutdown limpio |
| `SIGHUP` | Recargar config desde `config.json` |
| `SIGUSR1` | Dump del snapshot a `dump_<timestamp>.json` |
| `SIGUSR2` | Toggle modo verbose |

## Restricciones

- ❌ No usar `psutil` ni equivalentes
- ❌ No usar `subprocess` para `ps`/`top`
- ❌ No usar redes, bases de datos, `asyncio`
- ✅ Solo stdlib + `rich` o `curses` para TUI

## Cómo arrancar

1. **Leé la consigna completa** (`consigna.md`).
2. **Usá el prompt de tutor** (`prompt_tutor_ia.md`) si vas a apoyarte en una IA.
3. Si estás en macOS, leé primero `consigna_macos.md` (igual corre en Docker).
4. Armá la estructura mínima:

```
.
├── README.md
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── config.json
├── src/
│   ├── main.py
│   ├── recolector.py
│   ├── analizadores/{resumen,memoria,fds,threads,senales,scheduling,sistema}.py
│   ├── display.py
│   ├── procfs.py
│   └── senales.py
└── tests/
```

5. `docker compose up --build` y a jugar.

## Cronograma sugerido

| Semana | Tarea |
|--------|-------|
| 1 (post-clase 5) | Recolector + lectura de `/proc/<pid>/stat` |
| 2 (post-clase 6) | Vistas Resumen, Memoria, Sistema + señales básicas |
| 3 (post-clase 7) | Memoria compartida con `Manager` + agregador |
| 4 (post-clase 8-9) | Los 7 analizadores en paralelo |
| 5 (post-clase 10) | Vista Threads, intervalos diferenciados |
| 6 (post-clase 11) | Polishing, README, entrega |

## Clases relacionadas

- **Clase 3**: Procesos - Fundamentos (anatomía, /proc, memoria virtual)
- **Clase 4**: fork, exec, wait (zombies, COW)
- **Clase 5**: Pipes (file descriptors, IPC básico)
- **Clase 6**: Señales (handlers, máscaras, async-signal-safe, self-pipe)
- **Clase 7**: mmap y memoria compartida
- **Clase 8**: Multiprocessing fundamentos
- **Clase 9**: Multiprocessing avanzado (Pool, Manager, Value, Array)
- **Clase 10**: Threading (GIL, threads como LWPs en `/proc/<pid>/task`)
- **Clase 11**: Sincronización

## Criterios de evaluación

| Ítem | Peso |
|------|------|
| Funcionalidad (7 vistas, navegación) | 30% |
| Arquitectura multiproceso, IPC, sin race conditions | 25% |
| 5 señales funcionando | 10% |
| Lectura correcta de /proc | 15% |
| README con justificación y conexión a la teoría | 15% |
| Código limpio | 5% |
| Bonus (extensiones) | +10% |

> ⚠️ **Si no podés explicar tu propio código, no aprueba** — aunque el código funcione.

---

*Trabajo Práctico Nº 1 — Computación II — 2026*
