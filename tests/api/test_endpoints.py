from __future__ import annotations

from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_health_returns_200():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_model_info_returns_200():
    response = client.get("/model-info")
    assert response.status_code == 200
    assert "model_version" in response.json()


def test_predict_returns_503_without_loaded_model():
    """Until a real model artifact is loaded at startup, /predict
    should fail loudly (503) rather than silently returning junk."""
    payload = {
        "agency": "DSNY",
        "complaint_type": "Missed Collection",
        "borough": "BROOKLYN",
        "open_data_channel_type": "MOBILE",
        "hour_of_day": 14,
        "day_of_week": "Tuesday",
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 503


def test_predict_invalid_schema_returns_422():
    response = client.post("/predict", json={"agency": "DSNY"})  # missing required fields
    assert response.status_code == 422
