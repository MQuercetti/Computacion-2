# El sistema de archivos de Linux

## ¿Por qué necesitás entender esto?

Linux organiza casi todo alrededor del sistema de archivos. Vas a usarlo para leer configuración, guardar temporales, revisar permisos, inspeccionar procesos y comunicar programas entre sí. Si entendés cómo funciona, vas a depurar mejor y vas a escribir scripts más confiables.

## "Todo es un archivo"

En Linux, muchas cosas se representan como archivos:

- documentos de texto
- ejecutables
- directorios
- dispositivos de hardware
- información de procesos
- conexiones de red en algunos contextos

La idea importante no es memorizar casos aislados, sino entender que las mismas herramientas sirven para casi todo.

## La estructura del árbol de directorios

Linux tiene una única raíz: `/`.

Algunos directorios importantes:

- `/home`: carpetas personales de los usuarios.
- `/etc`: configuración del sistema.
- `/tmp`: archivos temporales.
- `/var`: datos variables como logs.
- `/dev`: dispositivos representados como archivos.
- `/proc`: filesystem virtual con información del kernel y procesos.

## Inodos: la verdad sobre los archivos

El nombre de un archivo no es el archivo. El archivo real está representado por un inodo, que guarda metadatos como permisos, tamaño, propietario, timestamps y punteros a los datos.

El nombre es solo una entrada de directorio que apunta a ese inodo.

### ¿Por qué importa esto?

Esto explica varias cosas que parecen mágicas:

1. Un archivo puede tener varios nombres si se crean enlaces duros.
2. Renombrar un archivo es rápido porque solo cambia la entrada del directorio.
3. Un archivo borrado puede seguir existiendo si algún proceso lo tiene abierto.

### ¿Qué contiene un inodo?

- tipo de archivo
- permisos
- propietario y grupo
- tamaño
- timestamps
- referencias a bloques de datos

### Los tres timestamps

- atime: último acceso de lectura
- mtime: última modificación de contenido
- ctime: último cambio de metadatos

### Ver información del inodo

El comando `stat` muestra metadatos detallados.

## Permisos: quién puede hacer qué

Cada archivo tiene permisos para tres categorías:

- usuario (u)
- grupo (g)
- otros (o)

Y tres tipos de permiso:

- lectura (r)
- escritura (w)
- ejecución (x)

### Interpretando los permisos

`ls -l` muestra algo como `-rwxr-xr--`.

- el primer carácter indica el tipo
- los tres siguientes son permisos del usuario
- los tres siguientes son permisos del grupo
- los últimos tres son permisos de otros

### Notación octal

Los permisos también se expresan como números:

- r = 4
- w = 2
- x = 1

Por eso `rwxr-xr--` equivale a `754`.

### Cambiando permisos

`chmod` permite cambiar permisos con notación octal o simbólica.

### Permisos en directorios

- `r`: listar contenido
- `w`: crear o borrar archivos
- `x`: entrar al directorio

### El problema de /tmp y el sticky bit

`/tmp` es escribible por todos, pero el sticky bit evita que un usuario borre archivos ajenos.

### Permisos desde Python

Con `os.stat()` y `os.chmod()` podés inspeccionar y modificar permisos desde Python.

## Enlaces: múltiples caminos al mismo archivo

### Enlaces duros

Un enlace duro es otro nombre para el mismo inodo. No es una copia.

### Enlaces simbólicos

Un symlink guarda una ruta a otro archivo. Tiene su propio inodo y puede romperse si el destino desaparece.

### ¿Cuándo usar cada uno?

- enlace duro: mismo filesystem, mismo archivo real
- enlace simbólico: más flexible, apunta a archivos o directorios

## Trabajando con archivos desde Python

La forma moderna de manejar rutas es `pathlib`.

También existen `os`, `os.path` y `shutil`, que siguen siendo útiles para tareas de sistema.

### pathlib: el enfoque moderno

`Path` permite crear rutas, leer archivos, listar directorios y construir caminos con `/`.

### os y os.path: el enfoque clásico

Siguen apareciendo mucho en código existente, pero para código nuevo suele preferirse `pathlib`.

### shutil: operaciones de alto nivel

Sirve para copiar, mover o borrar árboles de directorios.

## Juntando todo: un ejemplo práctico

Un script de limpieza de temporales combina:

- `pathlib` para recorrer rutas
- `stat()` para leer metadatos
- `argparse` para parámetros de línea de comandos

## Resumen

Lo esencial del bloque es entender:

- qué es un inodo
- cómo funcionan permisos y timestamps
- diferencia entre enlaces duros y simbólicos
- cómo usar `pathlib`, `os` y `shutil`
