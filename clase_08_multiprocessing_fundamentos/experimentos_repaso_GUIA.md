# Guía de los 5 experimentos de repaso (IPC)

## Cómo usar este material

1. Andá a la carpeta: `clase_08_multiprocessing_fundamentos/scripts/`
2. Abrí una terminal ahí.
3. Corré **un experimento por vez**: `python experimentos_repaso.py 1`
4. Mirá la salida.
5. **Recién ahora** leé la sección "Qué vas a ver" más abajo para ese experimento.
6. Cuando lo entendiste, pasá al siguiente.

No leas todas las explicaciones de corrido. Pierde la mitad del valor.

---

## Experimento 1 — "Dos procesos son dos cajas aisladas"

**Qué vas a ver**:

- El padre y el hijo tienen **PIDs distintos**.
- El padre cambia `x` a 999 **después** de arrancar el hijo. El hijo ya recibió su copia de `x` (que era 42) por el pipe de `spawn`. La variable `x` del padre no es la misma que la del hijo, ni siquiera cuando "se llama igual".
- Cuando el hijo termina, su `x` local **muere con él**. No vuelve al padre.

**Conceptos que mete**:

- Cada proceso tiene su **propia memoria**. Cambiar una variable en el padre **no afecta** al hijo.
- Los argumentos que se le pasan al hijo son **pickleados** (serializados) y enviados por un pipe. El hijo recibe una **copia**.

**Por qué importa para tu TP**:

En `main.py`, cuando hacés `mp.Process(target=algo, args=(snapshot, ...))`, el `snapshot` que le llega al hijo **no es el mismo objeto** que está en el padre. Es una copia por valor. Pero — ojo — eso no es todo, y es lo que el experimento 4 viene a romper.

---

## Experimento 2 — "Una Queue es un buzón entre procesos"

**Qué vas a ver**:

- El padre mete mensajes en la Queue.
- **Cualquier** hijo que esté escuchando con `q.get()` puede recibirlos. No hay un "dueño" del mensaje.
- Cuando metés 4 mensajes, los hijos los van sacando en orden (FIFO).
- Metés dos `"FIN"` porque cada `get()` saca uno solo. Si metés uno solo, **un hijo se queda colgado esperando**.

**Conceptos que mete**:

- `mp.Queue` es un buzón **compartido** entre procesos. No es un objeto del padre ni del hijo: vive en un sistema de IPC del SO.
- `put()` no bloquea si hay lugar. `get()` bloquea si está vacío.
- Cada `get()` saca **un solo** mensaje.

**Por qué importa para tu TP**:

En `main.py` línea 102: `q_pids = mp.Queue(maxsize=2)`. El recolector `put()` los PIDs, los 7 analizadores compiten por `get()`. Si un analizador es lento, **el otro se queda con el siguiente mensaje** — el primero ya no está. Por eso en `_wrapper_analizador` (línea 81) hay un `while not q_pids.empty(): pids = q_pids.get_nowait()`: para que cada analizador se quede con el **último** mensaje disponible, no con uno viejo.

---

## Experimento 3 — "Un Value es UNA variable compartida (con cuidado)"

**Qué vas a ver**:

- Hay UN solo `counter` (`mp.Value("i", 0)`).
- Los dos hijos leen, suman 1, escriben. El resultado debería ser 6 (2 hijos × 3 incrementos).
- El `with lock:` es lo que hace que funcione. Sin lock, los dos pueden leer 0, sumar 1, escribir 1 — y "pisarse".

**Conceptos que mete**:

- `mp.Value("i", 0)` es **una variable compartida** entre procesos. A diferencia de las variables comunes, todos ven el mismo valor.
- Pero "compartida" no es "mágica": dos procesos pueden leer y escribir al mismo tiempo y **corromper** el valor.
- `mp.Lock` es un semáforo binario: garantiza que **solo un proceso a la vez** esté en la sección crítica.

**Por qué importa para tu TP**:

En `agregador.py` línea 76: `crear_lock_global()`. Y en el `agregador.py` línea 5-15 el comentario lo explica: el Manager.dict ya sincroniza **a nivel de operación simple** (`d["x"] = y` es atómico), pero si querés hacer operaciones más grandes (leer-modificar-escribir varias claves juntas), necesitás el Lock a mano.

---

## Experimento 4 — "Manager: el cartero con casillero"

**Qué vas a ver**:

- `type(snap)` te dice `DictProxy`, no `dict`. Eso ya te avisa que algo raro pasa.
- Los dos hijos escriben en claves distintas. El padre las lee **en vivo** desde otro proceso.
- Si guardaras `mgr = Manager()` en una variable local que se va de scope, el casillero **se cierra**.

**Conceptos que mete**:

- `Manager()` arranca un **proceso servidor** (otro PID) que tiene un dict **real** adentro.
- `mgr.dict()` te devuelve un **proxy**: una "dirección" para hablar con ese dict remoto.
- Cuando hacés `snap["x"] = y`, tu proxy manda un mensaje al servidor: "poné y en la clave x". El servidor lo hace. Tu variable local no tiene el dict, solo la dirección.
- Por eso el padre y los hijos **ven lo mismo**: todos están hablando con el mismo servidor.
- El `mgr` (la referencia al Manager) tiene **el pipe abierto** al servidor. Si lo soltás, el servidor se queda sin clientes y se cierra.

**Por qué importa para tu TP**:

En `main.py` línea 98: `mgr_snap, snapshot = crear_snapshot()`. **Devuelve dos cosas** justamente por esto: una es el casillero (snapshot, el proxy) y la otra es la referencia al Manager (mgr_snap) que mantiene vivo al servidor. Por eso en `agregador.py` línea 30-31 el comentario dice "hay que mantenerlo vivo en el proceso padre".

---

## Experimento 5 — "Si soltás el Manager, los hijos se quedan sin casillero"

**Qué vas a ver**:

- El padre crea el Manager, arranca un hijo, **borra** su referencia con `del mgr`.
- El hijo, cuando intenta escribir, **tira error** (o el padre tira error al leer).
- El proceso servidor del Manager **murió** porque no le quedó ningún cliente con la conexión abierta.

**Conceptos que mete**:

- El Manager no es un objeto "decorativo". Es un **proceso vivo**.
- La conexión (pipe) al servidor la tiene cada referencia al Manager. Si nadie la tiene, el servidor se cierra.

**Por qué importa para tu TP**:

En `main.py` el `mgr_snap` y el `mgr_int` se guardan como variables locales de `main()`. Mientras `main()` no retorne, viven. Por eso `_shutdown()` los maneja **al final** (línea 173), después de matar a los hijos. Si los mataras antes, los hijos verían errores de "server died".

---

## Después de los 5

Cuando termines los 5, volvé a `main.py` y mirá:

- Línea 98-103: cada IPC que creás. ¿Cuál es un buzón (Queue)? ¿Cuál es un casillero (Manager.dict)? ¿Cuál es un switch (Event)? ¿Cuál es una variable compartida (Value)?
- Línea 203: `mp.set_start_method("spawn", force=True)`. ¿Por qué? Por las cosas que viste en el experimento 1: spawn arranca **limpio**, fork copiaría memoria del padre que puede traer problemas (locks, archivos abiertos, etc.).

Si alguno de los experimentos no te quedó claro, decímelo **antes** de seguir. Mejor frenar acá que acumular dudas para el `main.py`.
