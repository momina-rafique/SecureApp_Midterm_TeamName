from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_notes_crud():
    r = client.post("/api/notes/", json={"title": "Test", "content": "Hello"})
    assert r.status_code == 201
    note_id = r.json()["id"]

    r = client.get(f"/api/notes/{note_id}")
    assert r.status_code == 200

    r = client.put(f"/api/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    assert r.json()["title"] == "Updated"

    r = client.delete(f"/api/notes/{note_id}")
    assert r.status_code == 204
