# Argumentos de Línea de Comandos - Autoevaluación

## Parte 1: sys.argv

1. ¿Qué problema tiene usar `sys.argv` directamente para CLIs no triviales?
2. ¿Cómo detectás si faltan argumentos obligatorios?
3. ¿Qué devuelve `sys.argv[0]`?
4. ¿Qué ventaja tiene juntar `sys.argv[1:]` cuando querés un nombre con espacios?

## Parte 2: argparse básico

5. ¿Para qué sirve `argparse.ArgumentParser`?
6. ¿Qué diferencia hay entre argumento posicional y opción?
7. ¿Cómo marcás una opción como obligatoria?
8. ¿Qué hace `choices` en un argumento?
9. ¿Para qué sirve `nargs='*'`?
10. ¿Qué hace `action='store_true'`?
11. ¿Qué agrega `--help` automáticamente?

## Parte 3: herramientas de terminal

12. ¿Cómo se lee desde `stdin` cuando no se pasan archivos?
13. ¿Qué hace `git` con `stderr` frente a `stdout` en una CLI bien diseñada?
14. ¿Cuándo conviene usar `Path.iterdir()` en lugar de `os.listdir()`?
15. ¿Por qué `--count` cambia la forma de salida de un buscador tipo grep?

## Parte 4: subcomandos

16. ¿Para qué sirve `add_subparsers()`?
17. ¿Qué ventaja tienen los subcomandos para un programa como un gestor de tareas?
18. ¿Cómo modelarías una base de datos simple en JSON para persistir tareas?
19. ¿Qué hace un `mutually_exclusive_group`?
20. ¿Qué diferencia hay entre `print()` normal y `print(..., file=sys.stderr)`?

## Parte 5: buenas prácticas

21. ¿Por qué es importante validar tipos en argumentos de línea de comandos?
22. ¿Qué problema resuelve `Path.home()`?
23. ¿Por qué conviene separar el parseo de argumentos de la lógica de negocio?
24. ¿Qué error común aparece si no se maneja un archivo inexistente?
25. ¿Qué significa usar códigos de salida `0` y `1` correctamente?

## Respuestas

Completá esta parte vos mismo. La idea es que puedas justificar cada respuesta con un ejemplo del bloque.
