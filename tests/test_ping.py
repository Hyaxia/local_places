from fastapi.testclient import TestClient

from my_api.main import app


def test_ping() -> None:
    client = TestClient(app)
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"message": "pong"}
