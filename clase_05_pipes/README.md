# Clase 5: Pipes y Redirección

Material de la quinta clase de Computación II (2026) — File descriptors, redirección, pipes anónimos y named pipes (FIFOs).

## Estructura

```
clase_05_pipes/
├── README.md                  ← este archivo
├── contenido.md               ← teoría: FDs, dup2, pipe(), FIFO
├── ejercicios.md              ← 7 ejercicios (5: mini-shell con > y <)
├── autoevaluacion.md          ← quiz
├── extra_manijas.md           ← material opcional
├── fd_playground.py           ← explorar FDs del proceso actual
├── pipe_playground.py         ← pipe básico padre↔hijo
└── scripts/
    ├── explorar_fds.py        ← ejercicio 1.2: FDs en Python
    ├── redireccionar_stdout.py← ejercicio 2.1: dup2 manual
    ├── separar_stdout_stderr.py← ejercicio 2.2: stdout vs stderr
    ├── pipe_padre_hijo.py     ← ejercicio 3.1: pipe unidireccional
    ├── pipe_bidireccional.py  ← ejercicio 3.2: dos pipes ping-pong
    ├── pipeline_dos.py        ← ejercicio 4.1: `ls | grep`
    ├── pipeline_tres.py       ← ejercicio 4.2: `cat | grep | wc`
    ├── minish_redir.py        ← ejercicio 5: mini-shell con > y < (OBLIGATORIO)
    ├── mayusculas.py          ← ejercicio 6.1: filtro Unix
    ├── pipeline_subprocess.py ← ejercicio 6.2: pipeline con Popen
    ├── escritor_fifo.py       ← ejercicio 7.1: escritor a FIFO
    └── lector_fifo.py         ← ejercicio 7.1: lector de FIFO
```

## Orden de lectura recomendado

1. **`contenido.md`** — los conceptos de file descriptor son la base de todo lo demás.
2. **`ejercicios.md`** — el 5 (mini-shell con redirección) es **obligatorio**.
3. **`autoevaluacion.md`**.

## Conceptos centrales

| Concepto | Significado |
|----------|-------------|
| **fd 0** | `stdin` (entrada estándar) |
| **fd 1** | `stdout` (salida estándar) |
| **fd 2** | `stderr` (errores) |
| **`dup2(a, b)`** | Hace que `b` apunte al mismo archivo que `a` |
| **`os.pipe()`** | Devuelve `(read_fd, write_fd)` para comunicar procesos |
| **FIFO / named pipe** | Un archivo en disco que es un pipe: `os.mkfifo()` |

## Mini-shell: el ejercicio integrador

Tu mini-shell debe soportar:

```bash
minish$ echo "hola" > test.txt    # redirección de salida
minish$ wc -l < test.txt          # redirección de entrada
minish$ ls -la                    # comando normal
minish$ exit                      # salir
```

## Prerequisito

Esta clase usa `os.fork()`, `os.pipe()`, `os.dup2()` y `os.mkfifo()`. **No funcionan en Windows**. Usá Linux/macOS o un contenedor Docker.

## Próxima clase

**Clase 6: Señales** — comunicación asíncrona, handlers y self-pipe.

---

*Computación II - 2026 - Clase 5*
