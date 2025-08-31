import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def signup_and_login(email="user@example.com", password="secret123"):
    r = client.post("/auth/signup", json={"email": email, "password": password})
    assert r.status_code in (201, 400)
    r = client.post("/auth/login", data={"username": email, "password": password})
    assert r.status_code == 200
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_auth_and_notes_flow():
    headers = signup_and_login()
    # Create
    r = client.post("/api/notes/", json={"title": "Alpha", "content": "one", "tags": ["fastapi", "Tech"]}, headers=headers)
    assert r.status_code == 201
    note_id = r.json()["id"]

    # List with search
    r = client.get("/api/notes/?q=alp", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) >= 1

    # Filter by tag
    r = client.get("/api/notes/?tag=fastapi", headers=headers)
    assert r.status_code == 200
    assert any(n["id"] == note_id for n in r.json())

    # Update
    r = client.put(f"/api/notes/{note_id}", json={"title": "Beta", "is_archived": True, "tags": ["fastapi"]}, headers=headers)
    assert r.status_code == 200
    assert r.json()["title"] == "Beta"
    assert r.json()["is_archived"] is True
    assert [t["name"] for t in r.json()["tags"]] == ["fastapi"]

    # Get one
    r = client.get(f"/api/notes/{note_id}", headers=headers)
    assert r.status_code == 200

    # Delete
    r = client.delete(f"/api/notes/{note_id}", headers=headers)
    assert r.status_code == 204
