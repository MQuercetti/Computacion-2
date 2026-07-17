# mi_imagen - Ejercicio 3.1 de Docker Aplicado

Imagen Docker mínima con cowsay. Para construir y correr:

```bash
docker build -t mi-cowsay .
docker run mi-cowsay
docker run mi-cowsay "Docker es genial"
```

## Estructura

```
mi_imagen/
├── Dockerfile
├── requirements.txt
└── app.py
```
