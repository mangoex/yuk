import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_service_info(client) -> None:
    response = client.get("/api/v1/system")

    assert response.status_code == 200
    assert response.json() == {
        "name": "antigravity-crm-api",
        "version": "0.2.0",
        "environment": "development",
        "status": "ok",
    }

def test_frontend_is_served_at_root(client) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert '<div id="root"></div>' in response.text

def test_liveness(client) -> None:
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "alive"}

def test_readiness(client) -> None:
    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}

def test_openapi_is_available(client) -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"]["title"] == "CRM Inteligente Antigravity"
