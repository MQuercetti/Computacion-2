# Python Avanzado

## ¿Por qué este bloque?

Estos conceptos aparecen una y otra vez cuando escribís Python real: control de recursos con context managers, modificación de comportamiento con decoradores, procesamiento incremental con generadores, y técnicas de introspección y validación.

## Context managers

Un context manager controla la entrada y salida de un bloque `with`. Se usa para abrir y cerrar recursos de forma segura, incluso si ocurre una excepción.

## Decoradores

Un decorador recibe una función y devuelve otra función que la envuelve. Sirve para agregar comportamiento transversal como logging, retries o memoización sin repetir código.

## Generadores

Un generador produce valores bajo demanda con `yield`. Es la forma natural de trabajar con secuencias grandes o infinitas sin cargar todo en memoria.

## Closures y funciones de orden superior

Una closure recuerda variables del entorno donde fue creada. Las funciones de orden superior reciben o devuelven funciones, y son la base de muchos patrones avanzados.

## Excepciones y estructuras útiles

Python ofrece herramientas muy prácticas como `try/except/else/finally`, `collections.Counter`, `deque`, `functools.partial`, `dataclasses` e introspección con `inspect` y `typing`.

## Resumen

La idea central del bloque es aprender a combinar estas herramientas para construir soluciones pequeñas, expresivas y seguras.
