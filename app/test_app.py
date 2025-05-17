import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200

def test_predict_valid():
    response = client.post("/predict", json={"features": [5.1, 3.5, 1.4, 0.2]})
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert data["prediction"] == "setosa"
    assert "confidence" in data
    assert "all_probabilities" in data
    assert "features" in data
    assert data["features"] == [5.1, 3.5, 1.4, 0.2]

def test_predict_form():
    response = client.post(
        "/predict-form",
        data={
            "feature1": 5.1,
            "feature2": 3.5,
            "feature3": 1.4,
            "feature4": 0.2
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert data["prediction"] == "setosa"
    assert "confidence" in data
    assert "all_probabilities" in data
    assert "features" in data
    assert data["features"] == [5.1, 3.5, 1.4, 0.2]

def test_predict_invalid_features():
    # Too few features
    response = client.post("/predict", json={"features": [1.0, 2.0]})
    assert response.status_code in (400, 422)
    # Too many features
    response = client.post("/predict", json={"features": [1.0, 2.0, 3.0, 4.0, 5.0]})
    assert response.status_code in (400, 422)

def test_history():
    response = client.get("/history")
    assert response.status_code == 200
    data = response.json()
    assert "prediction_history" in data
