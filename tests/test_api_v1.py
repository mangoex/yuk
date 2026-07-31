import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_get_deals_stages(client) -> None:
    response = client.get("/api/v1/deals/stages")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 4
    assert data[0]["title"] == "Nuevo"

def test_create_and_list_leads(client) -> None:
    # Create lead
    resp = client.post("/api/v1/leads", json={
        "company_name": "Industrias Prueba SpA",
        "contact_name": "Juan Pérez",
        "email": "jperez@pruebaspa.com",
        "industry": "Tecnología",
        "size_range": "51-200",
        "annual_revenue": 3500000.0,
    })
    assert resp.status_code == 200
    lead_data = resp.json()
    assert lead_data["company_name"] == "Industrias Prueba SpA"
    assert lead_data["score"] >= 70

    # List leads
    list_resp = client.get("/api/v1/leads")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 1

def test_apify_prospecting_endpoint(client) -> None:
    resp = client.post("/api/v1/prospecting/run", json={
        "search_query": "Construcción",
        "location": "Querétaro",
        "limit_count": 3,
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["items_scraped"] == 3
    assert len(data["leads"]) == 3

def test_calls_analyze_endpoint(client) -> None:
    resp = client.post("/api/v1/calls/analyze", json={
        "company_name": "Grupo Constructor del Bajío",
        "duration_seconds": 300,
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["company_name"] == "Grupo Constructor del Bajío"
    assert "talk_listen_ratio_pct" in data

def test_reports_forecast_endpoint(client) -> None:
    resp = client.get("/api/v1/reports/forecast")
    assert resp.status_code == 200
    data = resp.json()
    assert "total_pipeline_value_mxn" in data
    assert "weighted_forecast_value_mxn" in data
