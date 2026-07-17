# Clase 2: Docker Aplicado

Material de la segunda clase de Computación II (2026) — Volúmenes, redes, Dockerfiles y Docker Compose.

## Estructura

```
clase_02_docker_aplicado/
├── README.md                  ← este archivo
├── contenido.md               ← teoría: volúmenes, redes, Dockerfile, Compose
├── ejercicios.md              ← 5 ejercicios prácticos + proyecto integrador
├── autoevaluacion.md          ← quiz de 20 preguntas
├── extra_manijas.md           ← material opcional
└── scripts/
    ├── contador.py            ← ejercicio 1.1: persistencia con bind mount
    ├── red_basica.py          ← ejercicio 2.1: comunicación entre contenedores
    └── mi_imagen/             ← ejercicio 3.1: Dockerfile, app.py, requirements
```

## Orden de lectura recomendado

1. **`contenido.md`** — leelo completo antes de la clase si podés.
2. **`ejercicios.md`** — hacé los 5 ejercicios en orden.
3. **`autoevaluacion.md`** — verificá tu comprensión (20 preguntas).
4. **`extra_manijas.md`** — opcional.

## Comandos clave de la clase

| Comando | Para qué |
|---------|----------|
| `docker volume create` / `ls` / `inspect` / `rm` | Gestión de volúmenes nombrados |
| `docker network create` / `ls` / `inspect` | Redes personalizadas con DNS automático |
| `docker build -t nombre .` | Construir imagen desde Dockerfile |
| `docker compose up` / `down` / `logs` | Orquestar múltiples contenedores |
| `docker compose -d` | Levantar en background |
| `docker compose down -v` | Detener y eliminar volúmenes |

## Diferencia clave: `EXPOSE` vs `-p`

| | `EXPOSE` (Dockerfile) | `-p` (runtime) |
|-|----------------------|----------------|
| **Abre el puerto?** | No, es solo metadata | Sí, mapea host↔contenedor |
| **Uso** | Documentar | Publicar |

## Tipos de volúmenes

| Tipo | Uso típico | Ejemplo |
|------|-----------|---------|
| Bind mount | Código fuente, config | `-v $(pwd):/app` |
| Named volume | Bases de datos, persistencia | `-v mis-datos:/data` |

---

*Computación II - 2026 - Clase 2*
