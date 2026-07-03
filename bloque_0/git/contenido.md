# Git y GitHub

## ¿Por qué empezamos con esto?

Git es la herramienta base que vas a usar para registrar, revisar y compartir todo el trabajo de la materia. Antes de procesos, sockets o hilos, necesitás dominar cómo guardar la historia de tu código y cómo volver atrás cuando algo sale mal.

## ¿Qué es Git?

Git es un sistema de control de versiones distribuido. En lugar de guardar solo diferencias, trabaja con snapshots: cada commit representa un estado completo del proyecto.

## Las tres áreas de Git

- Working directory: los archivos que editás.
- Staging area: lo que preparás con `git add`.
- Repository: la historia que se crea con `git commit`.

## Lo esencial del flujo

```bash
git status
git add archivo
git commit -m "mensaje"
```

## Branches y merges

Los branches sirven para trabajar en paralelo sin romper `main`. `git merge` integra esos cambios cuando la rama ya está lista.

## GitHub

GitHub es el servicio remoto donde hospedás repositorios y colaborás con otras personas. `git push` sube cambios y `git pull` los baja e integra.

## Buenas prácticas

- Commits pequeños y frecuentes.
- Mensajes descriptivos.
- `.gitignore` para archivos que no deben versionarse.

## Resumen

Si entendés staging, commits, branches, merge y sincronización con GitHub, ya tenés la base para el resto del curso.
