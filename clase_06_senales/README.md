# Clase 6: Señales

Material de la sexta clase de Computación II (2026) — Comunicación asíncrona entre procesos vía señales, handlers, y self-pipe.

## Estructura

```
clase_06_senales/
├── README.md                  ← este archivo
├── contenido.md               ← teoría: señales, kill, handlers, self-pipe
├── ejercicios.md              ← 6 ejercicios (5: servidor con señales obligatorio)
├── autoevaluacion.md          ← quiz
├── extra_manijas.md           ← material opcional
└── scripts/
    ├── ctrl_c_handler.py      ← ejercicio 2.1: capturar SIGINT
    ├── shutdown_limpio.py     ← ejercicio 2.2: SIGTERM graceful
    ├── padre_envia_al_hijo.py ← ejercicio 3.1: os.kill() + handlers
    ├── sigchld_recoger.py     ← ejercicio 3.2: detectar hijos terminados
    ├── timeout_decorador.py   ← ejercicio 4.1: SIGALRM como timeout
    ├── timer_periodico.py     ← ejercicio 4.2: setitimer
    ├── servidor_signals.py    ← ejercicio 5: servidor obligatorio
    └── pool_supervisado.py    ← ejercicio 6: pool de workers con SIGCHLD
```

## Orden de lectura recomendado

1. **`contenido.md`** — incluye self-pipe y async-signal-safe (clave para TP1).
2. **`ejercicios.md`** — el 5 (servidor con señales) es **obligatorio**.
3. **`autoevaluacion.md`**.

## Señales más usadas

| Señal | Default | Uso típico |
|-------|---------|-----------|
| `SIGTERM` (15) | Terminar | Shutdown amable — **capturable** |
| `SIGKILL` (9) | Terminar | Matar sin vuelta — **NO capturable** |
| `SIGINT` (2) | Terminar | Ctrl+C |
| `SIGHUP` (1) | Terminar | Terminal colgada, reload config |
| `SIGUSR1` (10) | Terminar | Definida por usuario |
| `SIGUSR2` (12) | Terminar | Definida por usuario |
| `SIGCHLD` (17) | Ignorar | Un hijo cambió de estado |
| `SIGALRM` (14) | Terminar | Timer expiró |
| `SIGSTOP` (19) | Detener | Pausa forzada — **NO capturable** |
| `SIGCONT` (18) | Continuar | Reanuda un proceso detenido |

## Regla de oro

**`SIGKILL` y `SIGSTOP` no se pueden capturar, bloquear ni ignorar.** Son la herramienta del kernel para casos extremos.

## Patrón self-pipe (clave para TP1)

En los handlers de señales **no podés hacer casi nada** (no es async-signal-safe). El patrón self-pipe resuelve esto:

1. Creás un pipe (anónimo) al inicio
2. El handler solo escribe un byte en el pipe
3. El loop principal lee del pipe y ahí sí hace el trabajo pesado

```python
read_fd, write_fd = os.pipe()

def handler(sig, frame):
    os.write(write_fd, b'x')  # lo único async-signal-safe

signal.signal(signal.SIGUSR1, handler)

# Loop principal: bloquea en read, no en signal
while True:
    data = os.read(read_fd, 1)
    print("Recibí SIGUSR1, ahora sí puedo hacer cosas")
```

## Prerequisito

`signal`, `os.kill` y `os.pipe` funcionan en Linux/macOS/WSL. En Windows solo lo básico de `signal`.

## Próxima clase

**Clase 7: mmap y memoria compartida** — la forma más rápida de comunicar procesos.

---

*Computación II - 2026 - Clase 6*
