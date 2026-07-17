# Clase 4: Procesos — fork, exec, wait

Material de la cuarta clase de Computación II (2026) — Las llamadas al sistema para crear procesos y el patrón fork-exec.

## Estructura

```
clase_04_procesos_fork_exec_wait/
├── README.md                  ← este archivo
├── contenido.md               ← teoría: fork, exec, wait, fork-exec
├── ejercicios.md              ← 6 ejercicios (último = mini-shell obligatorio)
├── autoevaluacion.md          ← quiz de 15 preguntas
├── extra_manijas.md           ← material opcional
├── ej_fork_exec.py            ← ejemplo de fork-exec del contenido
└── scripts/
    ├── primer_fork.py         ← ejercicio 1: doble flujo padre/hijo
    ├── n_hijos.py             ← ejercicio 2: 5 hijos con exit codes
    ├── fork_exec_launcher.py  ← ejercicio 3: ejecutar comando externo
    ├── zombie_demo.py         ← ejercicio 4: observar un zombie
    └── minish.py              ← ejercicio 5: mini-shell obligatorio
```

## Orden de lectura recomendado

1. **`contenido.md`** — la pieza central. Sin esto, el resto no cierra.
2. **`ejercicios.md`** — el 5 (mini-shell) es **obligatorio**.
3. **`autoevaluacion.md`** — 15 preguntas, varias sobre race conditions y zombies.

## Las 3 llamadas al sistema

| Llamada | Qué hace | Dónde se ejecuta |
|---------|----------|------------------|
| `os.fork()` | Crea una copia del proceso actual | Padre e hijo corren en paralelo |
| `os.execvp()` | Reemplaza el programa del proceso | Solo en el hijo (rama `pid == 0`) |
| `os.wait()` / `os.waitpid()` | Recoge el estado de un hijo terminado | Solo en el padre |

## El patrón fork-exec

Es lo que hace un shell cada vez que escribís un comando:

```
1. fork()           → duplica el shell
2. (en el hijo) exec() → reemplaza por el comando
3. (en el padre) wait() → espera y recoge el exit code
```

## Por qué `cd` no se hace con fork+exec

`cd` debe cambiar el directorio del **shell mismo**, no de un hijo. Por eso se ejecuta directamente en el proceso del shell, sin fork.

## Prerequisito para los ejercicios

Los ejercicios 1-6 usan `os.fork()`, que **no existe en Windows**. Para correrlos necesitás:
- Linux o macOS nativo, **o**
- Un contenedor Docker (recomendado: `docker run -it --rm python:3.11 bash`)

## Próxima clase

**Clase 5: Pipes** — cómo conectar procesos vía file descriptors para construir pipelines.

---

*Computación II - 2026 - Clase 4*
