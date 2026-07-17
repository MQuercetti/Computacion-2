# Clase 3: Procesos — Fundamentos

Material de la tercera clase de Computación II (2026) — Anatomía del proceso: jerarquía, PID/PPID, memoria virtual, file descriptors.

## Estructura

```
clase_03_procesos_fundamentos/
├── README.md                  ← este archivo
├── contenido.md               ← teoría: programa vs proceso, jerarquía, /proc, memoria
├── ejercicios.md              ← 4 ejercicios prácticos + adicionales
├── autoevaluacion.md          ← quiz de 12 preguntas
├── extra_manijas.md           ← material opcional
└── scripts/
    └── inspeccionar_proceso.py ← ejercicio 1: ver PID, FDs, mapa de memoria
```

## Orden de lectura recomendado

1. **`contenido.md`** — la base teórica de toda la materia.
2. **`ejercicios.md`** — los 4 ejercicios son cortos pero fundamentales.
3. **`autoevaluacion.md`** — 12 preguntas sobre conceptos clave.

## Conceptos centrales

| Concepto | Definición |
|----------|------------|
| **Proceso** | Instancia activa de un programa con su propio contexto (memoria, FDs, estado) |
| **PID** | Process ID — número único que identifica al proceso |
| **PPID** | Parent PID — el PID del proceso que lo creó |
| **PID 1** | `init` / `systemd` — ancestro de todos los procesos |
| **Zombie** | Proceso terminado cuyo padre no llamó `wait()` |
| **Huérfano** | Proceso cuyo padre murió; es adoptado por init |

## Segmentos de memoria

```
Direcciones altas
┌──────────────────────┐
│       Stack          │  Crece hacia abajo
├──────────────────────┤
│       Heap           │  Crece hacia arriba
├──────────────────────┤
│       BSS            │  Variables globales no inicializadas
├──────────────────────┤
│       Data           │  Variables globales inicializadas
├──────────────────────┤
│       Text           │  Código (solo lectura)
└──────────────────────┘
Direcciones bajas
```

## Comandos para explorar

| Comando | Para qué |
|---------|----------|
| `pstree -p` | Árbol de procesos con PIDs |
| `ps -ef --forest` | Todos los procesos en formato árbol |
| `cat /proc/<pid>/status` | Estado del proceso |
| `cat /proc/<pid>/maps` | Mapa de memoria |
| `cat /proc/<pid>/stat` | Estadísticas del proceso |
| `ls -l /proc/<pid>/fd` | File descriptors abiertos |
| `cat /proc/sys/kernel/pid_max` | Máximo de PIDs posibles |

## Próxima clase

**Clase 4: fork, exec, wait** — cómo crear procesos en Linux y el patrón fork-exec que usa todo shell.

---

*Computación II - 2026 - Clase 3*
