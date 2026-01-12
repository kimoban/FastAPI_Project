from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_and_me():
    payload = {"email": "user@example.com", "password": "secret123"}
    r = client.post("/api/v1/users/", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["email"] == payload["email"]
    assert "id" in data

    login = client.post("/api/v1/auth/login", json=payload)
    assert login.status_code == 200
    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    me = client.get("/api/v1/users/me", headers=headers)
    assert me.status_code == 200
    me_data = me.json()
    assert me_data["email"] == payload["email"]
