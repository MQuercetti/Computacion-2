# Filesystem de Linux - Ejercicios

## Cómo abordar estos ejercicios

El filesystem de Linux no se aprende solo leyendo. Tenés que mirarlo con tus propios ojos desde la terminal y después automatizar lo que observaste con Python.

## Parte 1: Exploración desde la terminal

### Ejercicio 1.1: Investigando tu sistema

Respondé usando solo comandos de terminal:

1. ¿Cuántos archivos hay directamente en `/etc`?
2. ¿Cuál es el tamaño exacto de `/etc/passwd`?
3. ¿Qué tipo de archivo es `/dev/null` y por qué es especial?
4. ¿A dónde apunta `/bin` si es symlink?
5. ¿Cuál es el número de inodo de tu `.bashrc` o `.zshrc`?
6. ¿Cuántos enlaces duros tiene `/home`?

Comandos útiles:

- `ls -l`
- `ls -i`
- `stat`
- `file`
- `readlink`
- `wc -l`

### Ejercicio 1.2: Entendiendo permisos

Creá un script simple, intentá ejecutarlo sin permisos, revisá `ls -l`, aplicá `chmod +x` y volvilo a ejecutar.

Después probá:

- diferencia entre `chmod +x` y `chmod 755`
- qué usuarios leen un archivo `644`
- por qué los directorios necesitan permiso `x`

### Ejercicio 1.3: Enlaces duros vs simbólicos

Creá un archivo original, un enlace duro y un symlink. Observá:

- inodos con `ls -li`
- contador de enlaces con `stat`
- qué pasa al borrar el archivo original

## Parte 2: Herramientas en Python

### Ejercicio 2.1: Inspector de archivos (OBLIGATORIO)

Creá `inspector.py`, una herramienta que muestre información detallada de un archivo o directorio.

Debe mostrar:

- tipo de archivo
- tamaño
- permisos legibles y octales
- propietario y grupo
- inodo
- enlaces duros
- timestamps
- para directorios, cuántos elementos contienen
- para symlinks, a dónde apuntan

### Ejercicio 2.2: Buscador de archivos grandes

Creá `find_large.py` para buscar archivos o directorios grandes de forma recursiva.

Debe aceptar:

- directorio a analizar
- `--min-size`
- `--type`
- `--top`
- búsqueda recursiva

### Ejercicio 2.3: Detector de enlaces rotos

Creá `broken_links.py` para encontrar symlinks rotos.

Debe aceptar:

- directorio a buscar
- `--delete`
- `--quiet`

## Parte 3: Herramientas avanzadas

### Ejercicio 3.1: Comparador de directorios

Creá `diffdir.py` para comparar dos directorios.

Debe mostrar:

- solo en un lado
- archivos modificados por tamaño
- archivos modificados por fecha
- opción `--recursive`
- opción `--checksum`

### Ejercicio 3.2: Analizador de uso de disco

Creá `diskusage.py` como una versión simplificada de `du`, con profundidad, top y exclusiones.

### Ejercicio 3.3: Sincronizador de directorios

Creá `sync.py` como una versión simplificada de `rsync`.

Debe poder:

- comparar origen y destino
- simular con `--dry-run`
- borrar extras con `--delete`
- excluir patrones
- preservar metadatos al copiar

## Parte 4: Para los que quieren más

### Ejercicio 4.1: Monitor de cambios en tiempo real

Creá `watch.py` para reportar cambios en un directorio.

### Ejercicio 4.2: Normalizador de permisos

Creá `fixperms.py` para normalizar permisos de archivos, directorios y scripts.

### Ejercicio 4.3: Deduplicador de archivos

Creá `dedup.py` para encontrar archivos duplicados por contenido.

## Checklist de entrega

Para el Bloque 0:

- 1.1 respuestas escritas: recomendado
- 1.2 demostración de chmod: recomendado
- 1.3 experimento de enlaces: recomendado
- 2.1 `inspector.py`: obligatorio
- 2.2 `find_large.py`: recomendado
- 2.3 `broken_links.py`: recomendado
- 3.1 o 3.2: uno de los avanzados, recomendado

## Ubicación en tu repositorio

```text
computacion2-2026/
└── bloque_0/
    └── filesystem/
        ├── ejercicio_1_1_respuestas.txt
        ├── inspector.py
        ├── find_large.py
        ├── broken_links.py
        └── diffdir.py
```

## Errores comunes

- confundir nombre con inodo
- pensar que `ctime` es creación
- olvidar que `x` en directorios significa poder entrar
- romper symlinks al borrar el destino
