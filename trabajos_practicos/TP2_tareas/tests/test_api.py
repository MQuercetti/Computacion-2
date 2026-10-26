import asyncio
import time
from typing import List
import httpx
import pytest

from src.app import app, lifespan
from src.models import EstadoTarea


@pytest.fixture
async def client():
    async with lifespan(app):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test"
        ) as c:
            yield c


async def test_encolar_tarea_responde_inmediatamente(client: httpx.AsyncClient):
    """Valida que POST /tareas responda 202 inmediatamente sin esperar a que la tarea termine."""
    payload = {
        "tipo": "esperar",
        "segundos": 3.0
    }
    inicio = time.perf_counter()
    response = await client.post("/tareas", json=payload)
    latencia = time.perf_counter() - inicio
    
    assert response.status_code == 202
    data = response.json()
    assert "id" in data
    assert data["tipo"] == "esperar"
    assert data["estado"] == "pendiente"
    assert latencia < 0.5


async def test_tarea_descargar_io_concurrente(client: httpx.AsyncClient):
    """Valida la tarea I/O-bound 'descargar' devolviendo estados y latencias."""
    urls = [
        "https://httpbin.org/status/200",
        "https://httpbin.org/status/201",
        "https://httpbin.org/status/204"
    ]
    payload = {
        "tipo": "descargar",
        "urls": urls
    }
    resp_post = await client.post("/tareas", json=payload)
    assert resp_post.status_code == 202
    tarea_id = resp_post.json()["id"]

    for _ in range(40):
        await asyncio.sleep(0.3)
        resp_get = await client.get(f"/tareas/{tarea_id}")
        data = resp_get.json()
        if data["estado"] in ["completada", "fallida"]:
            break
    
    assert data["estado"] == "completada"
    assert "descargas" in data["resultado"]
    assert len(data["resultado"]["descargas"]) == 3


async def test_cancelacion_descarga_en_vuelo(client: httpx.AsyncClient):
    """Valida cancelación limpia durante una descarga con múltiples URLs sin sockets zombies."""
    urls = [
        "https://httpbin.org/delay/5",
        "https://httpbin.org/delay/5"
    ]
    payload = {
        "tipo": "descargar",
        "urls": urls
    }
    resp_post = await client.post("/tareas", json=payload)
    tarea_id = resp_post.json()["id"]

    # Dar tiempo a que comience la conexión de red
    await asyncio.sleep(0.4)

    # Cancelar la tarea de red
    resp_del = await client.delete(f"/tareas/{tarea_id}")
    assert resp_del.status_code == 200
    assert resp_del.json()["estado"] == "cancelada"

    # Verificar estado
    resp_get = await client.get(f"/tareas/{tarea_id}")
    assert resp_get.json()["estado"] == "cancelada"


async def test_tarea_hashear_cpu_bound(client: httpx.AsyncClient):
    """Valida la ejecución de una tarea CPU-bound en ProcessPoolExecutor."""
    payload = {
        "tipo": "hashear",
        "texto": "computacion2",
        "iteraciones": 50000
    }
    resp_post = await client.post("/tareas", json=payload)
    assert resp_post.status_code == 202
    tarea_id = resp_post.json()["id"]

    for _ in range(40):
        await asyncio.sleep(0.2)
        resp_get = await client.get(f"/tareas/{tarea_id}")
        data = resp_get.json()
        if data["estado"] == "completada":
            break
    
    assert data["estado"] == "completada"
    assert "hash_final" in data["resultado"]
    assert data["resultado"]["iteraciones"] == 50000


async def test_cancelacion_tarea_en_vuelo(client: httpx.AsyncClient):
    """Valida DELETE /tareas/{id} cancelando una tarea que está en ejecución."""
    payload = {
        "tipo": "esperar",
        "segundos": 10.0
    }
    resp_post = await client.post("/tareas", json=payload)
    tarea_id = resp_post.json()["id"]

    await asyncio.sleep(0.3)
    
    resp_del = await client.delete(f"/tareas/{tarea_id}")
    assert resp_del.status_code == 200
    assert resp_del.json()["estado"] == "cancelada"

    resp_get = await client.get(f"/tareas/{tarea_id}")
    assert resp_get.json()["estado"] == "cancelada"


async def test_cancelar_tarea_pendiente_en_cola(client: httpx.AsyncClient):
    """Valida que una tarea cancelada antes de que un worker la tome se marque 'cancelada'."""
    # Encolamos varias tareas para ocupar los 4 workers
    for _ in range(4):
        await client.post("/tareas", json={"tipo": "esperar", "segundos": 2.0})

    # Esta 5ta tarea quedará pendiente en cola
    resp_cola = await client.post("/tareas", json={"tipo": "esperar", "segundos": 2.0})
    tarea_id_cola = resp_cola.json()["id"]

    # Inmediatamente cancelamos la que está pendiente
    resp_del = await client.delete(f"/tareas/{tarea_id_cola}")
    assert resp_del.status_code == 200
    assert resp_del.json()["estado"] == "cancelada"

    # Verificar que persiste cancelada
    resp_get = await client.get(f"/tareas/{tarea_id_cola}")
    assert resp_get.json()["estado"] == "cancelada"


async def test_timeout_tarea(client: httpx.AsyncClient):
    """Valida que una tarea con timeout específico pase a 'fallida' al expirar."""
    payload = {
        "tipo": "esperar",
        "segundos": 5.0,
        "timeout": 0.5
    }
    resp_post = await client.post("/tareas", json=payload)
    tarea_id = resp_post.json()["id"]

    await asyncio.sleep(1.2)

    resp_get = await client.get(f"/tareas/{tarea_id}")
    data = resp_get.json()
    assert data["estado"] == "fallida"
    assert "Timeout excedido" in data["error"]


async def test_tarea_inexistente_retorna_404(client: httpx.AsyncClient):
    """Valida que consultar o borrar un ID inexistente retorne 404."""
    resp_get = await client.get("/tareas/uuid-falso-1234")
    assert resp_get.status_code == 404

    resp_del = await client.delete("/tareas/uuid-falso-1234")
    assert resp_del.status_code == 404


async def test_validacion_parametros_invalidos(client: httpx.AsyncClient):
    """Valida que payload con datos inválidos sea rechazado con 422."""
    # Descargar sin URLs
    resp1 = await client.post("/tareas", json={"tipo": "descargar", "urls": []})
    assert resp1.status_code == 422

    # Hashear sin iteraciones
    resp2 = await client.post("/tareas", json={"tipo": "hashear", "texto": "test"})
    assert resp2.status_code == 422

    # Esperar con segundos negativos
    resp3 = await client.post("/tareas", json={"tipo": "esperar", "segundos": -5})
    assert resp3.status_code == 422


async def test_filtro_por_estado_y_estadisticas(client: httpx.AsyncClient):
    """Valida filtrado en GET /tareas?estado=... y métricas en /estadisticas."""
    # Encolar y completar una rápida
    await client.post("/tareas", json={"tipo": "esperar", "segundos": 0.05})
    await asyncio.sleep(0.2)

    resp_list_comp = await client.get("/tareas?estado=completada")
    assert resp_list_comp.status_code == 200
    for t in resp_list_comp.json():
        assert t["estado"] == "completada"

    resp_stats = await client.get("/estadisticas")
    assert resp_stats.status_code == 200
    stats = resp_stats.json()
    assert stats["total_tareas"] >= 1
    assert stats["workers_totales"] == 4
