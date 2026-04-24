from __future__ import annotations


def test_health_endpoint(client):
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["metadata"]["cache_status"] == "bypass"


def test_series_endpoint_returns_registry(client):
    response = client.get("/api/v1/series")

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] >= 10
    assert payload["items"][0]["source"] == "TCMB EVDS"
    assert "fetch_status" in payload["items"][0]
    assert payload["data"]


def test_series_detail_supports_alias(client):
    response = client.get("/api/v1/series/inflation")

    assert response.status_code == 200
    payload = response.json()
    assert payload["code"] == "CPI"
    assert payload["latest"]["value"] is not None


def test_observations_endpoint_returns_points(client):
    response = client.get("/api/v1/series/USDTRY/observations?limit=5")

    assert response.status_code == 200
    payload = response.json()
    assert payload["series_code"] == "USDTRY"
    assert payload["count"] == 5
    assert len(payload["data"]) == 5


def test_latest_endpoint_returns_latest_observation(client):
    response = client.get("/api/v1/series/USDTRY/latest")

    assert response.status_code == 200
    payload = response.json()
    assert payload["series_code"] == "USDTRY"
    assert payload["value"] is not None
    assert payload["data"]["value"] == payload["value"]


def test_invalid_series_code_returns_404(client):
    response = client.get("/api/v1/series/UNKNOWN")

    assert response.status_code == 404


def test_dashboard_summary_endpoint(client):
    response = client.get("/api/v1/dashboard/summary")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload["indicators"]) >= 8
    assert payload["data"]
    assert "Yatırım tavsiyesi" in payload["disclaimer"]


def test_compare_endpoint(client):
    response = client.get("/api/v1/compare?series=USDTRY,CPI&normalize=true")

    assert response.status_code == 200
    payload = response.json()
    assert payload["normalized"] is True
    assert len(payload["series"]) == 2
    assert payload["series"][0]["observations"][0]["value"] == 100


def test_compare_requires_at_least_two_series(client):
    response = client.get("/api/v1/compare?series=USDTRY")

    assert response.status_code == 400


def test_admin_fetch_data_falls_back_without_evds_key(client):
    response = client.post("/api/v1/admin/fetch-data")

    assert response.status_code == 200
    payload = response.json()
    assert payload["mode"] == "demo-seed"
    assert payload["source"] == "local-demo"
    assert payload["warnings"]

