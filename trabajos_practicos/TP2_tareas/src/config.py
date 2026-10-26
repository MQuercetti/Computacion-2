import os
from pathlib import Path

# Cantidad de workers concurrentes consumiendo de la cola
WORKER_COUNT: int = int(os.getenv("WORKER_COUNT", "4"))

# Timeout por defecto para las tareas (en segundos)
DEFAULT_TASK_TIMEOUT: float = float(os.getenv("DEFAULT_TASK_TIMEOUT", "60.0"))

# Tiempo máximo de espera para tareas en curso durante el graceful shutdown (en segundos)
SHUTDOWN_TIMEOUT: float = float(os.getenv("SHUTDOWN_TIMEOUT", "10.0"))

# Directorio base para los volcados de estado en apagado
BASE_DIR: Path = Path(__file__).resolve().parent.parent
DUMP_DIR: Path = Path(os.getenv("DUMP_DIR", str(BASE_DIR / "dumps")))
DUMP_DIR.mkdir(parents=True, exist_ok=True)
