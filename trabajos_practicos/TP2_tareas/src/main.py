import uvicorn
from src.app import app

if __name__ == "__main__":
    # La guarda __name__ == '__main__' es mandatoria para evitar bucles de spawn en Windows y macOS
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=False)
