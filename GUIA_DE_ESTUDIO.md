# 📘 Guía de Estudio — Computación II (2026)

> Documento vivo, paso a paso, para que puedas recorrer **todo** el curso de forma autónoma.
> Leelo en orden. Cada bloque/clase tiene: objetivos, qué hacer, qué mirar en la salida, y un checklist de comprensión.
> **Marcá los checkboxes `[ ]` a medida que avances** — te sirve para ver cuánto te falta y para repasar.

---

## 🗺️ Mapa del curso

```
BLOQUE 0 — Autónomo (antes de la clase 1)
├── 0.1 Git
├── 0.2 Argparse
├── 0.3 Filesystem
└── 0.4 Python avanzado

CLASES (con material en este repo)
├── Clase 1  → Docker Intro
├── Clase 2  → Docker Aplicado (volúmenes, redes, Compose)
├── Clase 3  → Procesos: anatomía (PID, memoria, /proc)
├── Clase 4  → fork / exec / wait + mini-shell
├── Clase 5  → Pipes y redirección + mini-shell con >
├── Clase 6  → Señales + servidor con señales
├── Clase 7  → mmap y memoria compartida
├── Clase 8  → multiprocessing (Process, Queue, Pipe)
├── Clase 9  → multiprocessing avanzado (Pool, Manager, Map-Reduce)
├── Clase 10 → Threading (GIL, Lock, Queue, daemon)
└── Clase 11 → Sincronización avanzada (Condition, Semaphore, Barrier, RWLock)

TRABAJO PRÁCTICO
└── TP1 → Monitor de procesos y threads (estilo htop)
```

**Convención de la guía**: "leer" significa abrir el archivo, leerlo, y volver a la guía. "Correr" significa ejecutar el comando. "Mirar" significa leer la salida con criterio (te digo qué buscar).

---

# 🟦 BLOQUE 0 — Material autónomo

**Objetivo general**: tener las herramientas de base (Git, línea de comandos, Python de nivel medio) antes de empezar con Docker y procesos. Este bloque NO tiene clase — es para hacerlo solo.

**Dónde está el material propio**: `bloque_0/`
**Dónde está el material de la cátedra**: `bloque_0/argparse/contenido_remoto.md` y `ejercicios_remoto.md` (versión espejo del repo original).

---

## 0.1 — Git

### 📖 Qué leer primero

1. Abrí `bloque_0/git/` y mirá qué hay ahí. Si no tenés apuntes propios, leé el README de la cátedra que tengas a mano (o pedime que te lo traiga).

### 🎯 Qué tenés que poder hacer al terminar

- [ ] Crear un repo local con `git init`
- [ ] Hacer `add` / `commit` / `push`
- [ ] Clonar un repo (`git clone <url>`)
- [ ] Crear y cambiar de rama (`git branch`, `git checkout -b`)
- [ ] Ver el historial (`git log --oneline --graph`)
- [ ] Resolver un merge conflict simple

### 🧪 Ejercicio sugerido (5 min)

```bash
# Parado en la raíz del repo, jugá un poco
git log --oneline --graph --all
git status
git branch
```

Mirá la salida de cada uno. **¿Qué branches hay? ¿Cuántos commits? ¿Hay algo sin commitear?**

---

## 0.2 — Argparse

### 📖 Qué leer primero

1. `bloque_0/argparse/contenido.md` (tu versión local, si la tenés)
2. **Si no la tenés o querés ver la de la cátedra**: `bloque_0/argparse/contenido_remoto.md`

### 🧪 Scripts que tenés en este repo

```
bloque_0/argparse/
├── genpass.py       ← generador de contraseñas
├── listar.py        ← listar archivos con filtros
├── wc_simple.py     ← word/line/char counter
├── contar.py        ← contar archivos por extensión
├── buscar.py        ← buscar patrón en archivos
├── inspeccionar.py  ← inspeccionar un archivo
├── permisos.py      ← cambiar permisos
├── contenido.md
├── contenido_remoto.md
└── ejercicios_remoto.md
```

### 🎯 Paso a paso

#### Ejercicio A — `genpass.py`

```bash
cd bloque_0/argparse
python genpass.py --help
```

**Mirá**: la descripción, qué argumentos hay, cuáles son obligatorios vs opcionales, cuáles tienen default.

```bash
# Generá una contraseña de 20 caracteres
python genpass.py -n 20

# Generá 5 contraseñas solo con letras y números (sin símbolos)
python genpass.py -n 16 --no-symbols --count 5

# Generá 3 contraseñas cortas
python genpass.py -n 8 --count 3
```

**Preguntas para chequear comprensión**:
- [ ] ¿Qué hace `-n`? ¿Y `--no-symbols`?
- [ ] ¿Qué pasa si no pasás `-n`? ¿Y si no pasás `--count`?
- [ ] ¿El orden de los flags importa? Probá `python genpass.py --count 3 -n 12`.

#### Ejercicio B — `listar.py`

```bash
cd bloque_0/argparse
python listar.py --help
python listar.py ..          # lista el directorio padre con defaults
python listar.py . -a        # incluye ocultos
python listar.py . --extension .py   # solo .py
python listar.py ../../..    # tres directorios arriba
```

**Preguntas**:
- [ ] ¿Qué hace `nargs="?"` en el argumento posicional?
- [ ] ¿Qué hace `-a`?
- [ ] Si pasás dos paths, ¿qué pasa? ¿Por qué?

#### Ejercicio C — `wc_simple.py`

```bash
cd bloque_0/argparse
python wc_simple.py --help
python wc_simple.py genpass.py
echo "hola mundo" | python wc_simple.py
```

**Mirá**:
- Si le pasás un archivo, cuenta líneas/palabras/caracteres del archivo.
- Si NO le pasás nada, lee de stdin (probá con pipe).
- [ ] ¿Por qué se comporta diferente en cada caso? Pista: mirá si el código distingue entre `len(sys.argv) > 1` o si usa `sys.stdin.isatty()`.

#### Ejercicio D — `contar.py`, `buscar.py`, `inspeccionar.py`, `permisos.py`

Para cada uno: `--help` primero, después un caso de uso real.

```bash
python contar.py . py
python buscar.py . "def main" --extension .py
python inspeccionar.py listar.py
python permisos.py hola.txt   # o algún archivo de prueba
```

**Pregunta integradora**:
- [ ] ¿Cuál de todos estos scripts te parece el más "tipo herramienta Unix"? ¿Por qué?

---

## 0.3 — Filesystem

### 📖 Qué leer primero

1. `bloque_0/filesystem/contenido.md` (si lo tenés)
2. Después: scripts en `bloque_0/filesystem/`

### 🧪 Scripts disponibles

```
bloque_0/filesystem/
├── inspector.py        ← inodos, permisos, owner
├── listar.py           ← tree
├── buscar.py           ← find-like
├── comparar.py         ← diff
├── contenido.md        ← (si lo tenés)
└── contenido_remoto.md
```

### 🎯 Paso a paso

```bash
cd bloque_0/filesystem

# 1. Inspector: mirá los inodos de varios archivos
python inspector.py ../argparse/genpass.py
python inspector.py ./

# 2. Listar en formato árbol
python listar.py ../
python listar.py ../../ --maxdepth 2

# 3. Buscar archivos
python buscar.py ../argparse -name "*.py"
python buscar.py ../ -name "*.md" -type f

# 4. Comparar dos archivos
python comparar.py ../argparse/listar.py ../argparse/wc_simple.py
```

**Preguntas**:
- [ ] ¿Qué es un inodo? ¿Por qué dos archivos distintos pueden tener el mismo inodo? (Pista: hard links)
- [ ] ¿Qué diferencia hay entre un link simbólico y un hard link?
- [ ] En Windows, ¿qué pasa con el owner/group? (Mirá el script — debería tener un try/except para `pwd`/`grp`)

### ⚠️ Nota sobre Windows

Los scripts de esta sección usan partes de POSIX (`/proc`, `pwd`, `grp`). En Windows algunos fallarán o devolverán información parcial. **Eso es esperable** — para los ejercicios de la materia, todos van a correr dentro de un contenedor Docker con Linux.

---

## 0.4 — Python avanzado

### 📖 Qué leer primero

1. `bloque_0/python_avanzado/contenido.md` (si lo tenés)

### 🎯 Temas que deberías manejar

- **Decoradores** (con y sin argumentos)
- **Context managers** (`with` + `__enter__`/`__exit__`)
- **Generadores** (`yield`)
- **Closures**
- **Dataclasses** (`@dataclass`)
- **Type hints** básicos

### 🧪 Ejercicio sugerido

Si tenés scripts propios de esta sección, corré los ejemplos. Si no, probá esto en un REPL:

```python
# Decorador básico
def medir_tiempo(func):
    import time
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        resultado = func(*args, **kwargs)
        print(f"{func.__name__} tardó {time.perf_counter() - t0:.4f}s")
        return resultado
    return wrapper

@medir_tiempo
def lento():
    sum(range(10_000_000))

lento()

# Context manager
class Timer:
    def __enter__(self):
        import time
        self.t0 = time.perf_counter()
    def __exit__(self, *args):
        import time
        print(f"Transcurrido: {time.perf_counter() - self.t0:.4f}s")

with Timer():
    sum(range(10_000_000))
```

**Checklist de comprensión**:
- [ ] ¿Qué devuelve un decorador? ¿Qué recibe?
- [ ] ¿Por qué `__enter__` no recibe args pero `__exit__` sí?
- [ ] ¿Qué ventaja tiene un generador sobre una lista para secuencias grandes?
- [ ] ¿Cuándo usar `dataclass` y cuándo un dict normal?

---

# 🟩 CLASE 1 — Docker Intro

### 🎯 Objetivo

Que puedas correr un contenedor, explorar Docker, y ejecutar Python dentro de un contenedor.

### 📂 Dónde está el material

```
clase_01_docker_intro/
├── README.md
├── contenido.md
├── ejercicios.md
├── autoevaluacion.md
├── extra_manijas.md
└── scripts/
    ├── hola.py
    ├── con_dependencias.py
    └── info_sistema.py
```

### 🎯 Paso a paso

#### 1. Leé la teoría

- Abrí `clase_01_docker_intro/contenido.md` y leélo completo.
- Si te trabás con algún término, mirá `extra_manijas.md`.

#### 2. Prerrequisito: ¿tenés Docker?

```bash
docker --version
docker run hello-world
```

Si NO tenés Docker: instalalo (Docker Desktop en Windows/macOS, docker.io en Linux).
Si lo tenés pero `hello-world` falla: hay un problema de permisos o el daemon no está corriendo. Buscá el error específico.

- [ ] `docker run hello-world` imprime el mensaje de bienvenida

#### 3. Ejercicios del archivo `ejercicios.md`

Andá en orden. Cada ejercicio tiene una verificación al final.

##### Ejercicio 1 — Explorando contenedores

```bash
docker run -it ubuntu bash
# Dentro:
cat /etc/os-release
whoami
ps aux
ls /
apt update && apt install -y cowsay
/usr/games/cowsay "Hola desde Docker"
exit
```

- [ ] Ubuntu corrió dentro de un contenedor

Después:

```bash
docker run -it ubuntu bash
# Intentá correr cowsay
/usr/games/cowsay "Hola"
# No existe → confirma que el contenedor es efímero
exit
```

- [ ] Entendiste que cada `docker run` crea un contenedor NUEVO

```bash
docker ps
docker ps -a
```

- [ ] Viste los contenedores detenidos con `docker ps -a`

##### Ejercicio 2 — Python en Docker

```bash
docker run -it python
```

Adentro, en el REPL:
```python
import sys
print(f"Python {sys.version}")
import os
print(f"Sistema: {os.uname()}")
exit()
```

Después, sin entrar al REPL:
```bash
docker run python python -c "print('Hola desde contenedor')"
docker run python python -c "import platform; print(platform.platform())"
```

Versiones diferentes:
```bash
docker run python:3.11 python --version
docker run python:3.9 python --version
docker run python:3.8-slim python --version
```

- [ ] Viste cómo cambia la versión de Python según el tag
- [ ] Viste el "Sistema" del contenedor (Linux aunque estés en Windows/macOS)

##### Ejercicio 3 — Ejecutar scripts locales

Usá los scripts que ya tenés en `scripts/`:

```bash
cd clase_01_docker_intro/scripts
docker run -v $(pwd):/app -w /app python python hola.py
```

- [ ] Viste que el `hostname` es un ID corto (ID del contenedor)
- [ ] El `directorio actual` es `/app`
- [ ] Los archivos listados son los de tu máquina local

**Probalo desde otra terminal** (mismo directorio):
```bash
docker run -v $(pwd):/app -w /app python python -c "
with open('prueba_desde_docker.txt', 'w') as f:
    f.write('Creado desde contenedor')
print('Listo')
"
ls prueba_desde_docker.txt
cat prueba_desde_docker.txt
```

- [ ] El archivo existe en tu máquina → confirmaste que el bind mount es bidireccional

##### Ejercicio 4 — Gestión de contenedores

```bash
docker run -d --name mi-python python sleep 300
docker ps
docker logs mi-python
docker exec -it mi-python python -c "print('Adentro del contenedor')"
docker stop mi-python
docker rm mi-python
```

- [ ] Levantar en background con `-d`
- [ ] `docker exec` para correr algo en un contenedor que ya está corriendo
- [ ] Limpieza con `stop` + `rm`

Limpieza general:
```bash
docker container prune    # respondé "y"
docker image prune
```

##### Ejercicio 5 — Script con dependencias

```bash
cd clase_01_docker_intro/scripts
docker run -v $(pwd):/app -w /app python python con_dependencias.py
# Falla: no está requests
```

```bash
docker run -v $(pwd):/app -w /app python sh -c "pip install requests && python con_dependencias.py"
# Anda, pero instala cada vez
```

- [ ] Viste que la imagen base de Python no trae `requests`
- [ ] Viste que se puede instalar on-the-fly con `sh -c "..."`

#### 4. Ejercicio de síntesis

El script `scripts/info_sistema.py` se corre en tres lugares:

```bash
# 1. Local
cd clase_01_docker_intro/scripts
python info_sistema.py > salida_local.txt

# 2. En contenedor con Python 3.11
docker run -v $(pwd):/app -w /app python:3.11 python info_sistema.py > salida_py311.txt

# 3. En contenedor con Python 3.9
docker run -v $(pwd):/app -w /app python:3.9 python info_sistema.py > salida_py39.txt
```

Después compará los archivos:
```bash
diff salida_local.txt salida_py311.txt
diff salida_local.txt salida_py39.txt
```

- [ ] Las **variables de entorno** son distintas (Docker vs tu shell)
- [ ] La **memoria disponible** es distinta (el contenedor tiene límites)
- [ ] El **sistema operativo** dice "Linux" en los tres casos, pero la versión puede cambiar

#### 5. Autoevaluación

Abrí `clase_01_docker_intro/autoevaluacion.md` y respondé las 15 preguntas **sin mirar las respuestas**. Después chequeá.

- [ ] Saqué al menos 12/15

### 🧠 Preguntas de comprensión de la Clase 1

Respondé en tu cabeza (o en papel) antes de seguir:

1. ¿Por qué un contenedor es "efímero"? ¿Cómo se rompe eso?
2. ¿Qué hace `-v $(pwd):/app` exactamente?
3. ¿Por qué `docker run python:3.9` no es lo mismo que `docker run python`?
4. ¿Qué pasa si instalás algo en un contenedor y después lo borrás?

---

# 🟩 CLASE 2 — Docker Aplicado

### 🎯 Objetivo

Saber crear tus propias imágenes, manejar volúmenes nombrados, redes personalizadas, y orquestar con docker-compose.

### 📂 Material

```
clase_02_docker_aplicado/
├── README.md
├── contenido.md
├── ejercicios.md
├── autoevaluacion.md
├── extra_manijas.md
└── scripts/
    ├── contador.py
    ├── red_basica.py
    └── mi_imagen/
        ├── Dockerfile
        ├── app.py
        ├── requirements.txt
        └── README.md
```

### 🎯 Paso a paso

#### 1. Leé la teoría

`clase_02_docker_aplicado/contenido.md` — prestá atención a la sección "EXPOSE vs `-p`" y "Tipos de redes".

#### 2. Ejercicio 1 — Volúmenes

##### 1.1 Bind mount para desarrollo

```bash
cd clase_02_docker_aplicado/scripts
mkdir -p datos
docker run -v $(pwd):/app -v $(pwd)/datos:/datos -w /app python python contador.py
docker run -v $(pwd):/app -v $(pwd)/datos:/datos -w /app python python contador.py
docker run -v $(pwd):/app -v $(pwd)/datos:/datos -w /app python python contador.py
cat datos/contador.txt
```

- [ ] El contador se incrementa entre ejecuciones
- [ ] El archivo `datos/contador.txt` existe en tu máquina

Probalo SIN el segundo `-v`:
```bash
docker run -v $(pwd):/app -w /app python python contador.py
# Falla: no existe /datos/contador.txt
```

- [ ] Entendiste que cada `-v` es un bind mount independiente

##### 1.2 Named volume

```bash
docker volume create contador-data
docker run -v $(pwd):/app -v contador-data:/datos -w /app python python contador.py
docker run -v $(pwd):/app -v contador-data:/datos -w /app python python contador.py
docker volume inspect contador-data
```

- [ ] El contador persiste
- [ ] No podés ver el archivo desde tu host (está en el área de Docker)

#### 3. Ejercicio 2 — Redes

##### 2.1 Comunicación entre contenedores

```bash
docker network create ejercicio-red
docker run -d --name servidor --network ejercicio-red python:3.11 python -m http.server 8000

# En otra terminal:
docker run --rm --network ejercicio-red python:3.11 \
    python -c "import urllib.request; print(urllib.request.urlopen('http://servidor:8000').read()[:100])"

# Limpieza
docker stop servidor && docker rm servidor
docker network rm ejercicio-red
```

- [ ] El cliente encontró al servidor por **nombre** (`servidor:8000`), no por IP

##### 2.2 Redis (opcional, requiere internet)

```bash
docker network create redis-net
docker run -d --name redis --network redis-net redis:alpine
docker run -it --rm --network redis-net python bash
# Dentro:
pip install redis
python -c "
import redis
r = redis.Redis(host='redis', port=6379)
r.set('prueba', 'funciona')
print(r.get('prueba'))
"
exit
```

- [ ] Funcionó la conexión por nombre
- [ ] Si salís y volvés a entrar con `docker run -it --network redis-net python bash`, los datos siguen

#### 4. Ejercicio 3 — Dockerfile

##### 3.1 Tu primera imagen

El material del repo ya viene armado en `scripts/mi_imagen/`:

```bash
cd clase_02_docker_aplicado/scripts/mi_imagen
docker build -t mi-cowsay .
docker run mi-cowsay
docker run mi-cowsay "Docker es genial"
docker images mi-cowsay
docker history mi-cowsay
```

- [ ] `mi-cowsay` se construyó y corrió
- [ ] `docker history` muestra las capas del build

##### 3.3 Cache de capas

Modificá `app.py` (cambiá el mensaje default), rebuild:
```bash
docker build -t mi-cowsay .
```
- Mirá las líneas: dice "Using cache" para `pip install` y solo rehace las últimas capas.

Después agregá otro paquete a `requirements.txt`:
```bash
docker build -t mi-cowsay .
```
- Ahora `pip install` SÍ se re-ejecuta porque cambió el archivo de dependencias.

- [ ] Entendiste el orden de las instrucciones en el Dockerfile (lo que cambia menos va primero)

#### 5. Ejercicio 4 — Docker Compose

Creá una carpeta para esto (no la pongas en el repo):

```bash
mkdir ~/compose-app
cd ~/compose-app
# Copiá los archivos de clase_02_docker_aplicado o recrealos
```

Estructura:
```
compose-app/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── app.py
```

`requirements.txt`:
```
redis==5.0.0
```

`app.py`:
```python
import redis
import os
import time

redis_host = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=redis_host, port=6379)
print(f"Conectando a Redis en {redis_host}...")
while True:
    visitas = r.incr('visitas')
    print(f"Visitas: {visitas}")
    time.sleep(2)
```

`Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
CMD ["python", "-u", "app.py"]
```

`docker-compose.yml`:
```yaml
services:
  app:
    build: .
    environment:
      - REDIS_HOST=redis
    depends_on:
      - redis
  redis:
    image: redis:alpine
```

Levantá:
```bash
docker compose up
# Verás: "Visitas: 1", "Visitas: 2", ...
```

En otra terminal:
```bash
docker compose ps
docker compose logs redis
```

- [ ] El counter sube cada 2 segundos

Probá con persistencia. Modificá `docker-compose.yml`:
```yaml
services:
  ...
  redis:
    image: redis:alpine
    volumes:
      - redis-data:/data
    command: redis-server --appendonly yes

volumes:
  redis-data:
```

```bash
docker compose down
docker compose up -d
# Esperar 10 segundos
docker compose down
docker compose up
# El counter NO empezó de 0 (persiste)
```

- [ ] Confirmaste que el volumen `redis-data` sobrevive a `docker compose down`

#### 6. Autoevaluación

20 preguntas en `clase_02_docker_aplicado/autoevaluacion.md`. Hacé las 4 secciones (Volúmenes, Redes, Dockerfile, Compose).

- [ ] Saqué al menos 16/20

### 🧠 Preguntas de comprensión Clase 2

1. ¿Cuándo usar bind mount vs named volume?
2. ¿Qué diferencia hay entre `EXPOSE` en el Dockerfile y `-p` en runtime?
3. ¿Por qué los contenedores en una red personalizada se ven por nombre?
4. ¿Por qué el orden de las instrucciones del Dockerfile importa?
5. ¿Qué hace `depends_on`? ¿Espera a que el servicio esté "listo" o solo a que el contenedor arranque?

---

# 🟧 CLASES 3-7 — Procesos, pipes, señales, memoria compartida

> Estas cinco clases son la parte central de la materia. Todas se ejecutan dentro de un **contenedor Docker con Linux** porque usan `os.fork()`, señales, `/proc`, etc., que no funcionan en Windows.

### 🐳 Setup obligatorio

Una vez, antes de empezar la clase 3:

```bash
# Creá un directorio de trabajo para los ejercicios de la materia
mkdir ~/compu2_ejercicios
cd ~/compu2_ejercicios

# Bajá una imagen de Linux con Python y herramientas
docker pull python:3.11-slim

# Verificá
docker run -it --rm python:3.11-slim bash
# Dentro:
ls /
cat /etc/os-release
which python
python --version
exit
```

Ahora cada vez que quieras correr algo, montás tu repo dentro del contenedor:

```bash
# Ejemplo genérico (ajustá el path):
docker run -it --rm \
    -v /ruta/a/tu/repo:/repo \
    -w /repo \
    python:3.11-slim \
    bash
```

⚠️ **Si estás en Windows**: el `$(pwd)` se reemplaza por la ruta completa de Windows. Usá siempre la flag `-v /ruta/absoluta/con/forward/slashes:/repo` y montá la carpeta correcta.

---

## 🟧 CLASE 3 — Procesos: anatomía

### 🎯 Objetivo

Entender qué es un proceso, cómo se organiza la memoria, qué es PID/PPID, cómo es la jerarquía.

### 📂 Material

```
clase_03_procesos_fundamentos/
├── contenido.md
├── ejercicios.md
├── autoevaluacion.md
└── scripts/inspeccionar_proceso.py
```

### 🎯 Paso a paso

#### 1. Leé la teoría

`contenido.md` completo. La sección de "Anatomía del proceso" (memoria: text/data/BSS/heap/stack) es la más importante.

#### 2. Ejercicio 1 — Explorar tu propio proceso

Adentro del contenedor Linux:

```bash
# Si todavía no estás en el contenedor, entrá:
docker run -it --rm -v /ruta/a/tu/repo:/repo -w /repo python:3.11-slim bash

cd /repo/clase_03_procesos_fundamentos/scripts
python inspeccionar_proceso.py
```

**Mirá la salida con criterio**:
- [ ] Tu PID
- [ ] Tu PPID (el PID del shell que te lanzó)
- [ ] Los FDs: debería haber al menos 0, 1, 2
- [ ] El mapa de memoria: buscá líneas con permisos `r-xp` (text) y `[heap]` y `[stack]`

#### 3. Ejercicio 2 — Árbol de procesos

En el contenedor:

```bash
apt update && apt install -y psmisc procps
pstree -p $$
ps -ef --forest
ps -o pid,ppid,comm -p $$ $(pgrep -P $$)
```

- [ ] Encontraste el PID 1 (debería ser algo así como `bash` si entraste directo, o `tini`/similar)
- [ ] Tu shell tiene como padre a PID 1

#### 4. Ejercicio 3 — Memoria virtual

```bash
# Lanzá un proceso de larga vida
python3 -c "import time; time.sleep(60)" &
PID=$!
cat /proc/$PID/maps | head -40
wait
```

**Mirá**:
- [ ] Líneas con `r-xp` → text segment (código)
- [ ] Línea con `[heap]` → heap
- [ ] Línea con `[stack]` → stack
- [ ] Líneas con `.so` → librerías compartidas

**Pregunta para chequear**:
- ¿Por qué hay tantas líneas `.so`? ¿Qué representan?

#### 5. Ejercicio 4 — PIDs y reciclado

```bash
cat /proc/sys/kernel/pid_max
for i in $(seq 1 20); do sh -c 'echo "PID=$$"'; done
```

- [ ] Viste que los PIDs van creciendo
- [ ] Entendiste que se reciclan cuando llegan a `pid_max`

#### 6. Autoevaluación

12 preguntas en `autoevaluacion.md`.

- [ ] 9+/12

### 🧠 Comprensión Clase 3

1. ¿Diferencia entre programa y proceso?
2. ¿Qué pasa si el padre termina antes que el hijo? (Anticipo de la clase 4)
3. ¿En qué segmento están las variables globales inicializadas a 0?
4. ¿Por qué el heap crece hacia arriba y el stack hacia abajo?
5. ¿Qué hace la MMU?

---

## 🟧 CLASE 4 — fork, exec, wait

### 🎯 Objetivo

Aprender a crear procesos en Unix: `fork`, `exec`, `wait`, y el patrón fork-exec.

### 📂 Material

```
clase_04_procesos_fork_exec_wait/
├── contenido.md
├── ejercicios.md
├── autoevaluacion.md
├── ej_fork_exec.py
└── scripts/
    ├── primer_fork.py
    ├── n_hijos.py
    ├── fork_exec_launcher.py
    ├── zombie_demo.py
    └── minish.py
```

### 🎯 Paso a paso

#### 1. Leé la teoría

`contenido.md` — **toda la clase 4 se sostiene sobre la teoría**. Si no leíste esto, los ejercicios no van a tener sentido.

#### 2. Ejercicio 1 — Primer fork

```bash
cd /repo/clase_04_procesos_fork_exec_wait/scripts
python primer_fork.py
```

- [ ] Viste dos líneas: una del padre, una del hijo
- [ ] El padre esperó al hijo (última línea: "Programa terminado")

**Pregunta**: ¿Por qué se imprime "Soy el padre" ANTES que "Soy el hijo" en algunas ejecuciones, y al revés en otras?

#### 3. Ejercicio 2 — N hijos

```bash
python n_hijos.py
```

- [ ] Viste 5 hijos crearse
- [ ] Los "códigos" de salida son 0, 1, 2, 3, 4 (en algún orden)
- [ ] El padre esperó a todos

**Mirá el código**: cada hijo duerme un tiempo random. ¿Por qué el orden de terminación es distinto del orden de creación?

#### 4. Ejercicio 3 — Patrón fork-exec

```bash
python fork_exec_launcher.py ls -la /tmp
python fork_exec_launcher.py echo "Hola desde mi launcher"
python fork_exec_launcher.py nonexistent-command    # exit 127
```

- [ ] `ls` y `echo` se ejecutaron (el launcher los "lanzó")
- [ ] `nonexistent-command` dio código 127 (comando no encontrado)

#### 5. Ejercicio 4 — Zombies

```bash
python zombie_demo.py
# En otra terminal (en el mismo host o en otra conexión al contenedor):
ps aux | grep -E 'Z|defunct'
```

- [ ] Viste un proceso zombie (estado `Z` o marcado como `defunct`)

Ahora, modificá `zombie_demo.py`: descomentá el `os.wait()` y la línea siguiente. Volvé a correr. El zombie ya no aparece.

- [ ] Confirmaste que `wait()` recoge el estado del hijo y elimina el zombie

#### 6. Ejercicio 5 (OBLIGATORIO) — Mini-shell

```bash
python minish.py
```

Probá estos comandos dentro del minish:
```
minish$ pwd
minish$ ls
minish$ cd /tmp
minish$ pwd
minish$ echo "hola"
minish$ ls -la /etc | head
minish$ exit
```

- [ ] `cd` cambió el directorio del shell mismo (sin fork)
- [ ] Los demás comandos se ejecutaron en procesos hijos
- [ ] El shell mostró el código de salida cuando fue != 0

**Extensión opcional** (sin bonus de nota, para entender): agregale soporte de pipes con `|`. Vas a usar lo que vas a ver en la clase 5.

#### 7. Autoevaluación

15 preguntas. Sección 1 (fork), 2 (exec), 3 (wait), 4 (patrón fork-exec).

- [ ] 11+/15

### 🧠 Comprensión Clase 4

1. ¿Por qué `os.fork()` retorna dos veces? ¿Qué retorna en cada lado?
2. ¿Qué significa Copy-on-Write?
3. Si `exec` falla, ¿qué pasa con el proceso?
4. ¿Por qué `cd` se hace sin fork en un shell?
5. ¿Qué pasaría si NUNCA llamamos a `wait()`?

---

## 🟧 CLASE 5 — Pipes y redirección

### 🎯 Objetivo

Entender file descriptors, redirección (`>`, `<`), pipes anónimos y named pipes (FIFOs).

### 📂 Material

```
clase_05_pipes/
├── contenido.md
├── ejercicios.md
├── autoevaluacion.md
├── fd_playground.py
├── pipe_playground.py
└── scripts/
    ├── explorar_fds.py
    ├── redireccionar_stdout.py
    ├── separar_stdout_stderr.py
    ├── pipe_padre_hijo.py
    ├── pipe_bidireccional.py
    ├── pipeline_dos.py
    ├── pipeline_tres.py
    ├── minish_redir.py      ← OBLIGATORIO
    ├── mayusculas.py
    ├── pipeline_subprocess.py
    ├── escritor_fifo.py
    └── lector_fifo.py
```

### 🎯 Paso a paso

#### 1. Leé la teoría

`contenido.md` — sobre todo: la tabla de FDs estándar, `dup2`, `os.pipe()`, y named pipes.

#### 2. Ejercicio 1 — File descriptors

```bash
cd /repo/clase_05_pipes/scripts
python explorar_fds.py
```

- [ ] Viste que `stdin`/`stdout`/`stderr` son fds 0, 1, 2
- [ ] Al abrir un archivo, apareció un fd nuevo (probablemente 3)
- [ ] Al cerrar, desapareció

#### 3. Ejercicio 2 — Redirección

```bash
python redireccionar_stdout.py
cat /tmp/salida.txt    # debería tener los prints que "iban al archivo"

python separar_stdout_stderr.py
# Probalo con redirecciones:
python separar_stdout_stderr.py > solo_stdout.txt
cat solo_stdout.txt
python separar_stdout_stderr.py 2> solo_stderr.txt
cat solo_stderr.txt
python separar_stdout_stderr.py > todo.txt 2>&1
cat todo.txt
```

- [ ] `>` manda stdout al archivo, `2>` manda stderr
- [ ] `2>&1` hace que stderr vaya a donde vaya stdout

#### 4. Ejercicio 3 — Pipes básicos

```bash
python pipe_padre_hijo.py
python pipe_bidireccional.py
```

- [ ] En el primero: el hijo escribió 4 mensajes, el padre los leyó
- [ ] En el segundo: el padre preguntó, el hijo respondió con el cuadrado

**Mirá el código**: el orden de los `os.close()` es importante. ¿Por qué el padre cierra `write_fd` antes de leer? (Porque si no, el read del padre bloquearía esperando más datos.)

#### 5. Ejercicio 4 — Pipeline de comandos

```bash
python pipeline_dos.py     # equivalente a ls -la | grep .py
python pipeline_tres.py    # cat /etc/passwd | grep root | wc -l
```

- [ ] `pipeline_dos.py` lista archivos y filtra los `.py`
- [ ] `pipeline_tres.py` cuenta líneas con "root" en `/etc/passwd`

**Pregunta**: ¿por qué en `pipeline_tres.py` se crean **dos** pipes en lugar de uno?

#### 6. Ejercicio 5 (OBLIGATORIO) — Mini-shell con redirección

```bash
python minish_redir.py
```

Probá:
```
minish$ echo "hola mundo" > test.txt
minish$ cat test.txt
minish$ ls -la > listado.txt
minish$ wc -l < listado.txt
minish$ exit
```

- [ ] `>` crea el archivo y le manda la salida del comando
- [ ] `<` hace que el comando lea del archivo

#### 7. Ejercicio 6 — Filtro Unix

```bash
echo "hola mundo desde el filtro" | python mayusculas.py
echo -e "primera\nsegunda\ntercera" | python mayusculas.py
```

- [ ] Cada línea de entrada se imprimió en mayúsculas

#### 8. Ejercicio 7 — Named pipe (FIFO)

En **una** terminal:
```bash
python lector_fifo.py
```

En **otra** terminal (mismo contenedor, otra sesión o `&`):
```bash
python escritor_fifo.py
```

- [ ] El lector recibió los mensajes que fue escribiendo el escritor

**¿Por qué se llama "named pipe"?** Porque tiene un nombre en el filesystem (`/tmp/mi_canal`) pero funciona como un pipe (flujo de bytes, dos extremos).

#### 9. Autoevaluación

- [ ] Saqué 12+/15 o más

### 🧠 Comprensión Clase 5

1. ¿Por qué fd 0, 1, 2 son stdin/stdout/stderr?
2. ¿Qué hace `os.dup2(a, b)` exactamente?
3. ¿Por qué hay que cerrar el `write_fd` en el padre antes de hacer `read`?
4. ¿Qué es un named pipe y en qué se diferencia de un pipe anónimo?
5. ¿Cómo implementarías `cat archivo | grep palabra | wc -l` con `os.pipe` y `os.fork`?

---

## 🟧 CLASE 6 — Señales

### 🎯 Objetivo

Entender señales Unix: cómo se envían, cómo se manejan, y el patrón self-pipe.

### 📂 Material

```
clase_06_senales/
├── contenido.md
├── ejercicios.md
├── autoevaluacion.md
└── scripts/
    ├── ctrl_c_handler.py
    ├── shutdown_limpio.py
    ├── padre_envia_al_hijo.py
    ├── sigchld_recoger.py
    ├── timeout_decorador.py
    ├── timer_periodico.py
    ├── servidor_signals.py   ← OBLIGATORIO
    └── pool_supervisado.py
```

### 🎯 Paso a paso

#### 1. Leé la teoría

`contenido.md` — secciones "Señales estándar" y "Self-pipe" son las más importantes.

#### 2. Ejercicio 1 — Explorando señales

```bash
# Ver todas las señales
kill -l

# En una terminal:
sleep 1000
# En otra:
pgrep sleep
kill -STOP <pid>      # pausa
kill -CONT <pid>      # continúa
kill <pid>            # termina con SIGTERM
```

- [ ] Viste que `STOP` pausa sin matar
- [ ] Viste que `CONT` reanuda
- [ ] Viste que `SIGTERM` se puede capturar (no siempre mata)

#### 3. Ejercicio 2 — Manejadores básicos

```bash
python ctrl_c_handler.py
# Apretá Ctrl+C tres veces (la tercera sale)
```

- [ ] Las primeras dos veces no terminó (handler personalizado)
- [ ] A la tercera, salió

```bash
python shutdown_limpio.py
# En otra terminal: kill <pid>
```

- [ ] El proceso liberó los "recursos" antes de salir

#### 4. Ejercicio 3 — Padre → hijo

```bash
python padre_envia_al_hijo.py
```

- [ ] Viste que SIGUSR1 incrementó, SIGUSR2 mostró

**Pregunta**: ¿por qué el hijo tiene que `signal.pause()` en un loop? ¿Qué pasaría si no?

```bash
python sigchld_recoger.py
```

- [ ] El handler de SIGCHLD recogió los hijos a medida que terminaron

#### 5. Ejercicio 4 — Alarmas

```bash
python timeout_decorador.py
```

- [ ] La operación rápida terminó normal
- [ ] La operación lenta fue interrumpida a los 3 segundos

```bash
python timer_periodico.py
# Apretá Ctrl+C después de unos segundos
```

- [ ] El timer disparó cada 2 segundos
- [ ] Al hacer Ctrl+C, el timer se desactivó

#### 6. Ejercicio 5 (OBLIGATORIO) — Servidor con señales

```bash
python servidor_signals.py
# Anotá el PID que imprime
```

En **otra** terminal:
```bash
kill -HUP <PID>     # recarga config
kill -USR1 <PID>    # muestra stats
kill -USR2 <PID>    # rota logs
kill <PID>          # shutdown limpio
```

- [ ] Las 4 señales hicieron lo que tenían que hacer
- [ ] El servidor hizo cleanup antes de salir

**Mirá el código**: ¿qué signals fueron registrados? ¿Por qué SIGINT y SIGTERM hacen lo mismo?

#### 7. Ejercicio 6 — Pool supervisado

```bash
python pool_supervisado.py
# Esperá unos segundos — vas a ver que el supervisor re-lanza workers que "cayeron"
# Ctrl+C para salir
```

- [ ] El supervisor mantiene 3 workers vivos
- [ ] Cuando un worker muere, lo reemplaza

#### 8. Autoevaluación

- [ ] 12+/15

### 🧠 Comprensión Clase 6

1. ¿Qué señales no se pueden capturar?
2. ¿Por qué no podés hacer `print` dentro de un handler de señal?
3. ¿Qué es el patrón self-pipe y para qué sirve?
4. ¿Cómo diferenciás SIGUSR1 de SIGUSR2?
5. ¿Qué hace `signal.setitimer`?

---

## 🟧 CLASE 7 — mmap y memoria compartida

### 🎯 Objetivo

Entender memoria compartida: `mmap` sobre archivos, mmap anónimo entre procesos, `Value`, `Array`, `SharedMemory`.

### 📂 Material

```
clase_07_mmap_memoria_compartida/
├── contenido.md
├── ejercicios.md
├── autoevaluacion.md
├── ejemplo.txt
└── scripts/
    ├── mmap_archivo.py
    ├── mmap_readonly.py
    ├── mmap_binario.py
    ├── mmap_anonimo.py
    ├── mmap_hijos.py
    ├── mmap_multiprocessing.py
    ├── value_race.py          ← OBLIGATORIO
    ├── array_paralelo.py
    ├── shared_memory.py
    ├── shareable_list.py
    └── banco_race.py
```

### 🎯 Paso a paso

#### 1. Leé la teoría

`contenido.md` — la tabla de "Cuándo usar cada mecanismo" (pipe vs queue vs memoria compartida) es clave.

#### 2. Ejercicio 1 — mmap sobre archivo

```bash
cd /repo/clase_07_mmap_memoria_compartida/scripts
python mmap_archivo.py
cat /tmp/mmap_test.txt     # el cambio se reflejó en disco
```

- [ ] Viste que modificando el mmap cambió el archivo en disco
- [ ] Viste cómo `find()` busca dentro del mmap

```bash
python mmap_readonly.py
```

- [ ] Viste que escribir en modo READ tira `TypeError`

#### 3. Ejercicio 2 — mmap como estructura binaria

```bash
python mmap_binario.py
```

- [ ] Viste que con `struct.pack_into` escribís enteros en posiciones fijas

#### 4. Ejercicio 3 — mmap anónimo entre procesos

```bash
python mmap_anonimo.py
python mmap_hijos.py
```

- [ ] En el primero: el hijo escribió, el padre leyó sin copiar nada
- [ ] En el segundo: 4 hijos escribieron en regiones distintas del mismo mmap

**Pregunta clave**: ¿por qué esto es más rápido que pipes? (Respuesta: cero copias)

#### 5. Ejercicio 4 — mmap con multiprocessing

```bash
python mmap_multiprocessing.py
```

- [ ] Viste que los procesos abrieron el mismo archivo y escribieron en distintos offsets

#### 6. Ejercicio 5 (OBLIGATORIO) — Value y Array

```bash
python value_race.py
# Ejecutalo varias veces, vas a ver números distintos
```

- [ ] El resultado siempre es **menor** que 400000 (algunos incrementos se "perdieron")

**Modificá el código**: agregale `with contador.get_lock():` alrededor de `contador.value += 1`. Volvé a correr. Ahora siempre da 400000.

- [ ] Confirmaste que `get_lock()` previene la race condition

```bash
python array_paralelo.py
```

- [ ] 4 procesos llenaron el array en paralelo
- [ ] Todos los `resultado[i] == i * i` (cero errores)

#### 7. Ejercicio 6 — SharedMemory

```bash
python shared_memory.py
python shareable_list.py
```

- [ ] Viste que `SharedMemory` comparte bytes crudos
- [ ] Viste que `ShareableList` permite tipos básicos pero el tamaño del string se fija al crear

#### 8. Ejercicio de síntesis — Banco

```bash
python banco_race.py
# Ejecutá varias veces — el total puede cambiar
```

- [ ] Viste race conditions: el total de dinero no se conservó
- [ ] Pensaste cómo arreglarlo (Lock, ¿verdad?)

#### 9. Autoevaluación

- [ ] 12+/15

### 🧠 Comprensión Clase 7

1. ¿Qué ventaja tiene memoria compartida sobre pipes?
2. ¿Qué desventaja?
3. ¿Cuándo usar `Value` vs `Array` vs `Manager().dict()`?
4. ¿Por qué `banco_race.py` pierde dinero? (Dibuja el flujo: leer saldo, decidir, escribir saldo)
5. ¿Qué hace `mmap(-1, n)`?

---

# 🟦 CLASES 8-11 — multiprocessing y threading

> A partir de acá los scripts usan `multiprocessing` y `threading`, que **funcionan también en Windows**. Si querés probar desde tu Windows directamente, podés. Para los ejercicios "clásicos" con `os.fork`, seguís necesitando el contenedor Linux.

---

## 🟦 CLASE 8 — Multiprocessing fundamentos

### 🎯 Objetivo

API de alto nivel para procesos: `Process`, `Queue`, `Pipe`, `set_start_method`.

### 📂 Material

```
clase_08_multiprocessing_fundamentos/
├── contenido.md
├── ejercicios.md
├── autoevaluacion.md
└── scripts/
    ├── primer_process.py
    ├── cinco_workers.py
    ├── productor_consumidor.py
    ├── pipe_pingpong.py
    └── fork_vs_spawn.py
```

### 🎯 Paso a paso

#### 1. Leé la teoría

`contenido.md` — sección "¿Por qué multiprocessing?" y la tabla Process vs os.fork.

#### 2. Ejercicio 1 — Tu primer Process

```bash
cd /repo/clase_08_multiprocessing_fundamentos/scripts
python primer_process.py
```

- [ ] Viste un proceso separado con su propio PID
- [ ] El `exitcode` fue 0

#### 3. Ejercicio 2 — 5 workers

```bash
python cinco_workers.py
```

- [ ] Los 5 workers arrancaron "a la vez" (sincronización con `time.perf_counter()`)
- [ ] El tiempo total ≈ la duración del más lento (no la suma)

#### 4. Ejercicio 3 — Productor-Consumidor

```bash
python productor_consumidor.py
```

- [ ] El productor puso 10 items, el consumidor los procesó

#### 5. Ejercicio 4 — Pipe ping-pong

```bash
python pipe_pingpong.py
```

- [ ] 5 mensajes en cada dirección
- [ ] No se cruzaron (cada extremo tiene su propio canal)

#### 6. Ejercicio 5 — fork vs spawn

```bash
# En Linux (contenedor):
python fork_vs_spawn.py

# En Windows (host):
python fork_vs_spawn.py
```

- [ ] En Linux, `fork` es más rápido que `spawn`
- [ ] En Windows, solo hay `spawn`

#### 7. Autoevaluación

- [ ] 10+/12

### 🧠 Comprensión Clase 8

1. ¿Por qué `if __name__ == "__main__":` es necesario?
2. ¿Cuándo usar `Queue` y cuándo `Pipe`?
3. ¿Qué significa "start method"?
4. ¿Por qué `multiprocessing` es portable y `os.fork` no?

---

## 🟦 CLASE 9 — Multiprocessing avanzado

### 🎯 Objetivo

`Pool` (map, imap, apply_async), `Manager`, `Value`/`Array` ya vistos, patrones Map-Reduce y Pipeline.

### 📂 Material

```
clase_09_multiprocessing_avanzado/
├── contenido.md
├── ejercicios.md
├── autoevaluacion.md
└── scripts/
    ├── pool_methods.py
    ├── speedup_cpu.py
    ├── value_array_lock.py
    ├── manager_dict_list.py
    ├── procesador_imagenes.py   ← OBLIGATORIO
    ├── map_reduce_palabras.py
    └── pipeline_3_etapas.py
```

### 🎯 Paso a paso

#### 1. Leé la teoría

`contenido.md` — la tabla de métodos de Pool es **lo más importante**.

#### 2. Ejercicio 1 — Métodos de Pool

```bash
cd /repo/clase_09_multiprocessing_avanzado/scripts
python pool_methods.py
```

- [ ] `map` → lista al final, ordenado
- [ ] `imap` → iterador, ordenado
- [ ] `imap_unordered` → iterador, por orden de terminación
- [ ] `starmap` → múltiples args

**Pregunta**: ¿en qué caso `imap_unordered` es más rápido que `imap`?

#### 3. Ejercicio 2 — Speedup

```bash
python speedup_cpu.py
```

- [ ] `Pool(1)` ≈ secuencial
- [ ] `Pool(N)` ≈ N× más rápido (hasta saturar cores)

#### 4. Ejercicio 3-4 — Memoria compartida

```bash
python value_array_lock.py
python manager_dict_list.py
```

- [ ] `Value` con `get_lock()` previene race conditions
- [ ] `Manager` permite dict/list compartidos pero es más lento

#### 5. Ejercicio 5 (OBLIGATORIO) — Procesador de imágenes

```bash
python procesador_imagenes.py
```

- [ ] Versión secuencial vs paralela (4 workers)
- [ ] Speedup > 1 (idealmente cerca de 4 si tenés 4+ cores)

**Modificá el código**: cambiá el `Pool(4)` por `Pool(1)`, `Pool(8)`. ¿Qué pasa?

#### 6. Ejercicio 6 — Map-Reduce

```bash
python map_reduce_palabras.py
```

- [ ] Viste el top 10 de palabras más frecuentes

#### 7. Ejercicio 7 — Pipeline

```bash
python pipeline_3_etapas.py
```

- [ ] 3 etapas conectadas por colas
- [ ] Input 0..9 → salida "resultado_010", "resultado_012", etc.

#### 8. Autoevaluación

- [ ] 12+/15

### 🧠 Comprensión Clase 9

1. ¿Cuándo usar `Pool` vs procesos manuales con `Process`?
2. ¿Por qué `imap_unordered` puede ser más rápido?
3. ¿Cuándo conviene `Manager` sobre `Value`/`Array`?
4. ¿Qué es el patrón Map-Reduce? ¿Y el Pipeline?
5. ¿Por qué `multiprocessing.Pool` es "el caballo de batalla"?

---

## 🟦 CLASE 10 — Threading

### 🎯 Objetivo

Threads, GIL, race conditions, `Lock`, `Queue`, `threading.local()`, daemons.

### 📂 Material

```
clase_10_threading/
├── contenido.md
├── ejercicios.md
├── autoevaluacion.md
└── scripts/
    ├── primer_hilo.py
    ├── io_bound_compare.py
    ├── gil_cpu_bound.py
    ├── contador_hilo_subclase.py
    ├── race_y_lock.py
    ├── daemons.py
    ├── productor_consumidor.py
    ├── threading_local.py
    └── descargador_paralelo.py   ← OBLIGATORIO
```

### 🎯 Paso a paso

#### 1. Leé la teoría

`contenido.md` — la sección del GIL es la más importante.

#### 2. Ejercicio 1 — Primer hilo

```bash
cd /repo/clase_10_threading/scripts
python primer_hilo.py
```

- [ ] Viste 3 hilos ejecutándose en paralelo (puede que el orden varie)
- [ ] "Listo" se imprime al final

#### 3. Ejercicio 2 — I/O-bound

```bash
python io_bound_compare.py
```

- [ ] Versión secuencial: ~5 segundos
- [ ] Versión con threads: ~1 segundo (5× más rápido)

#### 4. Ejercicio 3 — GIL (CPU-bound)

```bash
python gil_cpu_bound.py
```

- [ ] Los 4 threads NO son más rápidos que el secuencial (o incluso son más lentos)
- [ ] **Esto es el GIL**: solo un hilo ejecuta bytecode Python a la vez

**Pruebalo** reemplazando `threading.Thread` por `multiprocessing.Process`. Ahora sí vas a ver speedup.

#### 5. Ejercicio 4-5 — Clase Thread y Lock

```bash
python contador_hilo_subclase.py
python race_y_lock.py
```

- [ ] La versión "insegura" puede dar saldo negativo
- [ ] La versión con `Lock` siempre da saldo correcto (0)

#### 6. Ejercicio 6 — Daemons

```bash
python daemons.py
# Esperá 3 segundos y mirá: el programa termina aunque el thread esté "trabajando"
```

- [ ] El daemon murió cuando el main terminó

#### 7. Ejercicio 7 — Productor-Consumidor con Queue

```bash
python productor_consumidor.py
```

- [ ] 4 workers procesaron 20 imágenes en ~2.5s (vs ~10s secuencial)
- [ ] `queue.Queue` es thread-safe (no necesitás Lock explícito)

#### 8. Ejercicio 8 — threading.local()

```bash
python threading_local.py
```

- [ ] Cada hilo tuvo su propio contexto (usuario, ip, timestamp) sin interferir

#### 9. Ejercicio 9 (OBLIGATORIO) — Descargador paralelo

```bash
python descargador_paralelo.py
```

- [ ] 4 threads descargaron 5 URLs en paralelo
- [ ] Errores de red no crashearon el programa

#### 10. Autoevaluación

- [ ] 12+/15

### 🧠 Comprensión Clase 10

1. ¿Qué es el GIL y por qué existe?
2. ¿Cuándo threading ayuda? ¿Cuándo NO?
3. ¿Por qué `queue.Queue` es más segura que `list.append()` desde varios hilos?
4. ¿Qué ventaja tiene `threading.local()`?
5. ¿Diferencia entre thread daemon y no-daemon?

---

## 🟦 CLASE 11 — Sincronización avanzada

### 🎯 Objetivo

`Condition`, `Semaphore`, `Barrier`, `Event`, `ReadWriteLock`, prevención de deadlocks.

### 📂 Material

```
clase_11_sincronizacion_1/
├── contenido.md
├── ejercicios.md
├── autoevaluacion.md
├── demo_race_condition.py
└── scripts/
    ├── cuenta_insegura.py
    ├── cuenta_segura.py
    ├── condition_pc.py
    ├── barrier_fases.py
    ├── connection_pool.py
    ├── read_write_lock.py    ← OBLIGATORIO
    └── deadlock_demo.py
```

### 🎯 Paso a paso

#### 1. Leé la teoría

`contenido.md` — la tabla "Tabla maestra de primitivas" y "Las 4 condiciones de deadlock".

#### 2. Ejercicio 1 — Race condition y Lock

```bash
cd /repo/clase_11_sincronizacion_1/scripts
python cuenta_insegura.py    # saldo puede NO ser 1000
python cuenta_segura.py      # saldo SIEMPRE es 1000
python demo_race_condition.py --runs 10
```

- [ ] La versión insegura da resultados distintos en cada corrida
- [ ] La versión con Lock da siempre el resultado correcto

#### 3. Ejercicio 2 — Condition

```bash
python condition_pc.py
```

- [ ] Los productores esperaban cuando la cola estaba llena
- [ ] Los consumidores esperaban cuando la cola estaba vacía
- [ ] No se perdió ningún item

#### 4. Ejercicio 3 — Barrier

```bash
python barrier_fases.py
```

- [ ] Todos los workers terminaron la fase 1 antes de empezar la fase 2
- [ ] La `Barrier(N, action=imprimir_estado)` imprimió después de cada fase

#### 5. Ejercicio 4 — Semaphore

```bash
python connection_pool.py
```

- [ ] Máximo 3 clientes simultáneos
- [ ] Estadísticas finales: total_requests, esperas, tiempo promedio

#### 6. Ejercicio 5 (OBLIGATORIO) — Readers-Writers Lock

```bash
python read_write_lock.py
```

- [ ] Múltiples lectores leyeron a la vez
- [ ] Un escritor tuvo acceso exclusivo
- [ ] El valor final y los contadores son consistentes

**Mirá el código**:
- ¿Por qué `acquire_read` usa `while self.writers > 0` y no `if`?
- ¿Por qué `release_read` notifica a `can_write` y no a `can_read`?
- ¿Por qué `release_write` notifica a `can_read` con `notify_all`?

#### 7. Ejercicio 6 — Deadlock

```bash
python deadlock_demo.py
```

- [ ] La primera versión puede quedar colgada (deadlock)
- [ ] La segunda versión (orden global) termina siempre

**Mirá el código**: ¿en qué se diferencia la primera de la segunda?

#### 8. Autoevaluación

- [ ] 12+/15

### 🧠 Comprensión Clase 11

1. ¿Las 4 condiciones de deadlock? ¿Cómo se previene cada una?
2. ¿Cuándo usar `Condition` vs `Queue`?
3. ¿Cómo implementarías un rate limiter con `Semaphore`?
4. ¿Por qué en Readers-Writers, `release_read` notifica a `can_write` y no al revés?
5. ¿Qué es starvation? ¿Cómo evitarlo en Readers-Writers?

---

# 🟥 TP1 — Monitor de procesos y threads

### 🎯 Objetivo

**El trabajo integrador de toda la materia**. Construir un monitor estilo `htop` que:
- Lee `/proc` directamente (no `psutil`)
- Tiene 7 procesos analizadores paralelos
- Muestra 7 vistas diferentes
- Maneja 5 señales (SIGINT/TERM/HUP/USR1/USR2)
- TUI con teclas 1-7 para cambiar vista

### 📂 Material

```
trabajos_practicos/TP1_monitoreo/
├── README.md
├── consigna.md                ← leé esto completo
├── consigna_macos.md
└── prompt_tutor_ia.md
```

### 🎯 Cómo encarar el TP

#### 1. Antes de empezar

- Leé `consigna.md` de punta a punta. **No subestimes el README** — vale 15% de la nota.
- Leé `prompt_tutor_ia.md` si pensás usar IA como tutor.

#### 2. Estructura mínima sugerida

```
.
├── README.md                 ← informe
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── config.json
├── src/
│   ├── main.py
│   ├── recolector.py
│   ├── analizadores/
│   │   ├── resumen.py
│   │   ├── memoria.py
│   │   ├── fds.py
│   │   ├── threads.py
│   │   ├── senales.py
│   │   ├── scheduling.py
│   │   └── sistema.py
│   ├── display.py
│   ├── procfs.py
│   └── senales.py
└── tests/
```

#### 3. Cronograma sugerido (de la cátedra)

| Semana | Qué hacer |
|--------|-----------|
| 1 (post-clase 5) | Recolector que lista procesos y lee `/proc/<pid>/stat` |
| 2 (post-clase 6) | Vistas Resumen, Memoria, Sistema + señales básicas |
| 3 (post-clase 7) | Memoria compartida con `Manager` + agregador |
| 4 (post-clase 8-9) | Los 7 analizadores en paralelo |
| 5 (post-clase 10) | Vista Threads, intervalos diferenciados |
| 6 (post-clase 11) | Polishing, README, entrega |

#### 4. Clave del TP: entendé `/proc`

Antes de escribir código, pasá un rato explorando:

```bash
# Dentro del contenedor
cat /proc/self/status
cat /proc/self/maps | head
ls -la /proc/self/fd
cat /proc/self/stat
cat /proc/1/comm
ls /proc/1/task/    # threads del proceso 1
```

- [ ] Entendés qué hay en cada archivo de `/proc/<pid>/`
- [ ] Sabés parsear `/proc/<pid>/stat` (los campos están en `man proc`)

#### 5. Andá por capas

1. **Primero**: hacé un script que lea `/proc` y muestre info básica de 1 proceso.
2. **Segundo**: hacé que liste todos los procesos.
3. **Tercero**: separá en procesos analizadores.
4. **Cuarto**: agregá la TUI.
5. **Quinto**: agregá las señales.

#### 6. Cosas que van a preguntar al corregir

> "Si no podés explicar tu propio código, no aprueba" — `consigna.md`

Algunas preguntas típicas:
- "Mostrame dónde podría ocurrir una race condition en tu código. ¿Cómo la prevenís?"
- "¿Por qué tu agregador usa `Manager.dict` y no un `dict` regular?"
- "¿Cómo decodificás `SigBlk` para mostrar `SIGINT` legible?"
- "Diferencia entre PID y TID en `/proc`. ¿Cómo se ve en tu output?"

#### 7. Bonus (+10%)

Cuando lo obligatorio esté sólido:
- Histórico de CPU/MEM con mini-gráficos ASCII
- Detección de anomalías (picos de CPU, zombies)
- Modo daemon (sin TUI, solo log)
- Exportación a JSON/CSV
- Vista de jerarquía tipo `pstree`
- Tests del parseo de `/proc`

---

# 📊 Resumen: qué saber antes de cada examen

Si tuvieras que repasar en una noche, en este orden:

1. **Docker**: bind mount, named volume, EXPOSE vs -p, docker-compose, networks con DNS.
2. **Procesos**: PID, PPID, jerarquía, memoria (text/data/BSS/heap/stack), `/proc`.
3. **fork/exec/wait**: patrón fork-exec, copy-on-write, zombies, huérfanos.
4. **Pipes**: FDs (0,1,2), `os.pipe()`, `os.dup2()`, redirección, named pipes.
5. **Señales**: SIGTERM/INT/HUP/USR1/USR2, handlers, self-pipe, async-signal-safe.
6. **Memoria compartida**: mmap, `Value`, `Array`, `SharedMemory`, race conditions.
7. **multiprocessing**: `Process`, `Queue`, `Pipe`, `Pool` (map vs imap vs apply_async), `Manager`.
8. **Threading**: GIL, race conditions, `Lock`, `Queue`, `threading.local()`, daemon.
9. **Sincronización**: `Condition`, `Semaphore`, `Barrier`, `Event`, `ReadWriteLock`, deadlocks (4 condiciones).

---

# 🎓 Tips generales

- **Corré todo el código**. Leer no alcanza. La diferencia entre "creo que entendí" y "ya lo corrí y sé qué pasa" es enorme.
- **Modificalo**. Después de correr un script, cambiá algo (un número, un orden, un parámetro) y volvé a correr. Ver qué pasa es la mejor forma de aprender.
- **Dibujá**. Los diagramas ASCII de la guía son un punto de partida — copialos en papel y agregá flechas con lo que vos pensás que pasa.
- **Usá `print` para debuggear**. En el TP1 vas a usar `rich`/`curses`, pero `print` nunca falla.
- **Preguntate "¿qué pasa si...?"**. ¿Y si el archivo no existe? ¿Y si el hijo termina antes que el padre llame a wait? ¿Y si dos procesos escriben al mismo tiempo?
- **No te apures con el TP1**. Andá clase por clase, replicando lo que vimos.

---

# ✅ Checklist final del curso

- [ ] Bloque 0 completo (Git, Argparse, Filesystem, Python avanzado)
- [ ] Clase 1 (Docker Intro)
- [ ] Clase 2 (Docker Aplicado)
- [ ] Clase 3 (Procesos: anatomía)
- [ ] Clase 4 (fork, exec, wait, mini-shell)
- [ ] Clase 5 (Pipes, mini-shell con redirección)
- [ ] Clase 6 (Señales, servidor con señales)
- [ ] Clase 7 (mmap, memoria compartida)
- [ ] Clase 8 (multiprocessing fundamentos)
- [ ] Clase 9 (multiprocessing avanzado)
- [ ] Clase 10 (Threading, GIL)
- [ ] Clase 11 (Sincronización avanzada)
- [ ] TP1 entregado y con README completo

Cuando completes el checklist, **ya sabés lo que la materia te quería enseñar**. 🎉

---

*Guía de estudio generada para acompañarte en Computación II - 2026 - Universidad de Mendoza*
*Basada en el material de la cátedra del Ing. Gabriel Quintero*
