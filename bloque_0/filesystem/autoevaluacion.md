# Filesystem Linux - Autoevaluación

## Parte 1: Inodos y estructura

1. ¿Qué información NO almacena un inodo?
2. ¿Qué representa `nlinks`?
3. ¿Qué significa que dos archivos tengan el mismo inodo?
4. ¿Qué timestamp se actualiza al leer un archivo?
5. ¿Qué timestamp se actualiza al cambiar permisos?
6. ¿Qué indica `l` al inicio de `ls -l`?
7. ¿Qué directorio contiene archivos de dispositivos?
8. ¿Qué comando muestra información detallada del inodo?

## Parte 2: Permisos

9. ¿Qué permisos representa 755?
10. ¿Qué significa `x` en un directorio?
11. ¿Quién puede leer un archivo `rw-r-----`?
12. ¿Qué comando cambia el propietario de un archivo?
13. ¿Qué hace `chmod u+x script.sh`?
14. ¿Qué es el SUID bit?
15. ¿Para qué sirve el sticky bit en `/tmp`?
16. ¿Qué permisos suele producir umask `022`?

## Parte 3: Enlaces

17. ¿Cuál es la diferencia principal entre enlace duro y simbólico?
18. ¿Qué pasa si borrás el original de un enlace duro?
19. ¿Qué pasa si borrás el original de un enlace simbólico?
20. ¿Pueden los enlaces duros cruzar sistemas de archivos?
21. ¿Pueden los symlinks apuntar a directorios?
22. ¿Qué comando crea un enlace simbólico?

## Parte 4: Python y filesystem

23. ¿Qué módulo es recomendado para rutas modernas?
24. ¿Qué retorna `st_size` en `os.stat()`?
25. ¿Cómo verificás si un path es un symlink?
26. ¿Qué función de `shutil` preserva metadatos al copiar?
27. ¿Cómo leés el destino de un symlink?
28. ¿Qué atributo de `Path` da la extensión de un archivo?

## Respuestas

1. Nombre del archivo.
2. Cantidad de enlaces duros.
3. Son el mismo archivo.
4. `atime`.
5. `ctime`.
6. Enlace simbólico.
7. `/dev`.
8. `stat`.
9. `rwxr-xr-x`.
10. Poder entrar/atravesar el directorio.
11. El propietario y el grupo.
12. `chown`.
13. Agrega ejecución al usuario.
14. Ejecuta con permisos del propietario.
15. Evita que otros borren archivos ajenos.
16. `644`.
17. El duro comparte inodo, el simbólico apunta a una ruta.
18. Los datos siguen si queda otro enlace duro.
19. El enlace queda roto.
20. No.
21. Sí.
22. `ln -s`.
23. `pathlib`.
24. Bytes.
25. `os.path.islink(path)`.
26. `shutil.copy2()`.
27. `os.readlink()`.
28. `suffix`.
