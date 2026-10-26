FROM python:3.11-slim

# Evitar buffers en stdout/stderr para que los logs se vean inmediatamente
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY src/ ./src/
COPY benchmarks/ ./benchmarks/

# Crear carpeta para dumps de persistencia
RUN mkdir -p /app/dumps

EXPOSE 8000

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
