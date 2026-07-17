# Clase 1: Docker Intro

Material de la primera clase de Computación II (2026) — Introducción a Docker.

## Estructura

```
clase_01_docker_intro/
├── README.md                  ← este archivo
├── contenido.md               ← teoría: qué es Docker, por qué lo usamos, comandos básicos
├── ejercicios.md              ← 5 ejercicios prácticos + ejercicio de síntesis
├── autoevaluacion.md          ← quiz de 15 preguntas para verificar comprensión
├── extra_manijas.md           ← material opcional (namespaces, cgroups, Podman, etc.)
├── docker_intro.pptx          ← slides de la clase
└── scripts/
    ├── hola.py                ← script de ejemplo (ejercicio 3.1)
    ├── con_dependencias.py    ← script con requests (ejercicio 5.1)
    └── info_sistema.py        ← ejercicio de síntesis final
```

## Orden de lectura recomendado

1. **`contenido.md`** — leelo completo antes de la clase si podés.
2. **`ejercicios.md`** — hacé los 5 ejercicios. Requisito: Docker instalado (`docker run hello-world` tiene que funcionar).
3. **`autoevaluacion.md`** — verificá tu comprensión con el quiz.
4. **`extra_manijas.md`** — opcional, para los que quieren profundizar.

## Comandos clave de la clase

| Comando | Para qué |
|---------|----------|
| `docker run -it ubuntu bash` | Contenedor interactivo |
| `docker run python python -c "..."` | Ejecutar comando one-shot |
| `docker run -v $(pwd):/app -w /app python python script.py` | Montar dir local y correr script |
| `docker run python:3.9 python --version` | Versión específica de imagen |
| `docker ps` / `docker ps -a` | Ver contenedores corriendo / todos |
| `docker images` | Ver imágenes descargadas |
| `docker stop` / `docker rm` / `docker rmi` | Detener / borrar contenedor / borrar imagen |
| `docker container prune` | Limpiar contenedores detenidos |
| `docker exec -it <nombre> bash` | Entrar a contenedor ya corriendo |

## Ejercicio de síntesis

El archivo `scripts/info_sistema.py` se usa para comparar la salida en:
- tu máquina local
- un contenedor con `python:3.11`
- un contenedor con `python:3.9`

Mismas preguntas, distintos ambientes. Eso es la idea de Docker.

---

*Computación II - 2026 - Clase 1*
