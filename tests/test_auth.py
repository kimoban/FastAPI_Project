from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_login_wrong_credentials():
    r = client.post("/api/v1/auth/login", json={"email": "none@example.com", "password": "bad"})
    assert r.status_code == 401
