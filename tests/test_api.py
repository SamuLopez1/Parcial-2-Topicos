from fastapi.testclient import TestClient
from app.adapters.http.fastapi_app import app

client = TestClient(app)

def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_create_and_list_tasks():
    r = client.post("/tasks", json={"title": "Tarea 1", "status": "pending"})
    assert r.status_code == 201
    data = r.json()
    assert data["id"] >= 1
    assert data["title"] == "Tarea 1"
    assert data["status"] == "pending"

    r2 = client.get("/tasks")
    assert r2.status_code == 200
    items = r2.json()
    assert any(x["title"] == "Tarea 1" for x in items)
