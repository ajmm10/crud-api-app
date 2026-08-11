from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
HEADERS = {"X-API-Key": "dev-secret-key"}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "1.2"}


def test_listar_sin_api_key():
    response = client.get("/productos")
    assert response.status_code == 401


def test_crud_completo():
    # Crear
    payload = {"nombre": "Piñata Estrella", "categoria": "Piñatas", "precio": 250.0, "stock": 15}
    response = client.post("/productos", json=payload, headers=HEADERS)
    assert response.status_code == 201
    producto = response.json()
    producto_id = producto["id"]
    assert producto["nombre"] == "Piñata Estrella"

    # Leer uno
    response = client.get(f"/productos/{producto_id}", headers=HEADERS)
    assert response.status_code == 200

    # Leer todos
    response = client.get("/productos", headers=HEADERS)
    assert response.status_code == 200
    assert len(response.json()) >= 1

    # Actualizar
    response = client.put(f"/productos/{producto_id}", json={"stock": 20}, headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["stock"] == 20

    # Eliminar
    response = client.delete(f"/productos/{producto_id}", headers=HEADERS)
    assert response.status_code == 204

    # Confirmar que ya no existe
    response = client.get(f"/productos/{producto_id}", headers=HEADERS)
    assert response.status_code == 404
