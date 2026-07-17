"""
experimentos_repaso.py — 5 experimentos cortos para entender IPC desde cero.

Pensado para correr en Windows (usa la API de multiprocessing que funciona
en todas las plataformas).

Cómo correr cada uno:
    python experimentos_repaso.py 1
    python experimentos_repaso.py 2
    ...

Cada experimento está pensado para que lo mires correr, leas la salida, y
después leas el bloque "QUE VAS A VER" más abajo. NO leas la explicación
antes — perdés la mitad del aprendizaje.

Convención: "PADRE" es el proceso principal (el que corre este script).
"HIJO" es cualquier proceso que se crea con multiprocessing.
"""

import multiprocessing as mp
import os
import time
import sys


# ============================================================
# EXPERIMENTO 1 — Dos procesos son dos cajas aisladas
# ============================================================
def exp1_hijo(compartido_desde_padre):
    print(f"  [HIJO]  PID={os.getpid()}, mi variable local x=99")
    print(f"  [HIJO]  recibí por arg: {compartido_desde_padre}")
    print(f"  [HIJO]  el PID del padre era: {os.getppid()}")
    time.sleep(0.3)
    print(f"  [HIJO]  termino. La variable local x se va con migo.")


def experimento_1():
    print("\n" + "=" * 60)
    print("EXPERIMENTO 1: dos procesos son dos cajas aisladas")
    print("=" * 60)
    x = 42  # variable local del PADRE
    print(f"[PADRE] PID={os.getpid()}, x={x}")
    p = mp.Process(target=exp1_hijo, args=(x,))
    p.start()
    time.sleep(0.1)
    x = 999  # cambio x en el padre DESPUÉS de arrancar el hijo
    print(f"[PADRE] cambié x a {x} mientras el hijo corría")
    p.join()
    print(f"[PADRE] x final = {x}")


# ============================================================
# EXPERIMENTO 2 — Una Queue es un buzón entre procesos
# ============================================================
def exp2_hijo(q, nombre):
    while True:
        msg = q.get()
        if msg == "FIN":
            print(f"  [HIJO {nombre}] recibí FIN, salgo")
            break
        print(f"  [HIJO {nombre}] recibí: {msg!r}")


def experimento_2():
    print("\n" + "=" * 60)
    print("EXPERIMENTO 2: Queue es un buzón entre procesos")
    print("=" * 60)
    q = mp.Queue()
    p1 = mp.Process(target=exp2_hijo, args=(q, "A"))
    p2 = mp.Process(target=exp2_hijo, args=(q, "B"))
    p1.start(); p2.start()

    for i in range(4):
        q.put(f"mensaje {i}")
        time.sleep(0.2)
    q.put("FIN"); q.put("FIN")  # uno para cada hijo
    p1.join(); p2.join()
    print("[PADRE] terminé de enviar")


# ============================================================
# EXPERIMENTO 3 — Un Value es UNA variable compartida
# ============================================================
def exp3_hijo(counter, lock, nombre):
    for _ in range(3):
        with lock:                       # sin lock, esto se rompe
            v = counter.value
            time.sleep(0.05)             # simulo que "pienso"
            counter.value = v + 1
        print(f"  [HIJO {nombre}] counter.value = {counter.value}")


def experimento_3():
    print("\n" + "=" * 60)
    print("EXPERIMENTO 3: Value es UNA variable compartida")
    print("=" * 60)
    counter = mp.Value("i", 0)            # "i" = signed int
    lock = mp.Lock()
    p1 = mp.Process(target=exp3_hijo, args=(counter, lock, "A"))
    p2 = mp.Process(target=exp3_hijo, args=(counter, lock, "B"))
    p1.start(); p2.start(); p1.join(); p2.join()
    print(f"[PADRE] counter final = {counter.value}")
    print("[PADRE] (si ves 6, el lock funcionó. Si ves otra cosa, corré de nuevo)")


# ============================================================
# EXPERIMENTO 4 — Manager: el cartero con casillero
# ============================================================
def exp4_hijo(snap, mi_nombre, mi_slot):
    for i in range(3):
        snap[mi_slot] = {"ts": time.time(), "quien": mi_nombre, "n": i}
        time.sleep(0.3)
    print(f"  [HIJO {mi_nombre}] terminé de escribir en {mi_slot}")


def experimento_4():
    print("\n" + "=" * 60)
    print("EXPERIMENTO 4: Manager — un casillero compartido")
    print("=" * 60)
    mgr = mp.Manager()
    snap = mgr.dict()                     # ← esto NO es un dict normal
    print(f"[PADRE] type(snap) = {type(snap).__name__}")
    p1 = mp.Process(target=exp4_hijo, args=(snap, "A", "slot_A"))
    p2 = mp.Process(target=exp4_hijo, args=(snap, "B", "slot_B"))
    p1.start(); p2.start()

    for _ in range(5):
        time.sleep(0.4)
        # el PADRE lee el casillero que los hijos están escribiendo
        print(f"[PADRE] veo: {dict(snap)}")

    p1.join(); p2.join()
    print(f"[PADRE] snap final: {dict(snap)}")
    print("[PADRE] si guardás 'mgr' en una variable, el casillero sigue vivo")


# ============================================================
# EXPERIMENTO 5 — Si soltás el Manager, los hijos se quedan sin casillero
# ============================================================
def exp5_hijo(snap, mi_nombre):
    for i in range(3):
        try:
            snap[f"msg_{mi_nombre}_{i}"] = i
            time.sleep(0.3)
        except Exception as e:
            print(f"  [HIJO {mi_nombre}] ERROR: {type(e).__name__}: {e}")
            return


def experimento_5():
    print("\n" + "=" * 60)
    print("EXPERIMENTO 5: si perdés el Manager, el casillero muere")
    print("=" * 60)
    mgr = mp.Manager()
    snap = mgr.dict()
    p = mp.Process(target=exp5_hijo, args=(snap, "A"))
    p.start()

    time.sleep(0.1)
    print("[PADRE] suelto el manager (lo borro)")
    del mgr                                # ← acá "matás" el casillero

    p.join()
    # el padre intenta usar snap
    try:
        print(f"[PADRE] snap después de soltar el mgr: {dict(snap)}")
    except Exception as e:
        print(f"[PADRE] ERROR leyendo snap: {type(e).__name__}: {e}")


# ============================================================
# Dispatcher
# ============================================================
EXPERIMENTOS = {
    "1": experimento_1,
    "2": experimento_2,
    "3": experimento_3,
    "4": experimento_4,
    "5": experimento_5,
}


if __name__ == "__main__":
    # En Windows, multiprocessing necesita esto sí o sí para crear procesos.
    mp.set_start_method("spawn", force=True)
    if len(sys.argv) < 2 or sys.argv[1] not in EXPERIMENTOS:
        print("Uso: python experimentos_repaso.py [1-5]")
        print()
        for k in EXPERIMENTOS:
            print(f"  {k} → {EXPERIMENTOS[k].__doc__.splitlines()[0]}")
        sys.exit(1)
    EXPERIMENTOS[sys.argv[1]]()
