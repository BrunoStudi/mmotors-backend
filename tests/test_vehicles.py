from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_vehicles():
    response = client.get("/vehicles/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_vehicle_not_found():
    response = client.get("/vehicles/999999")

    assert response.status_code in [404, 500, 422]

def test_get_vehicles_empty():
    response = client.get("/vehicles/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_vehicle_without_auth():
    response = client.post(
        "/vehicles/",
        json={
            "brand": "Test",
            "model": "Test",
            "price": 10000,
            "type": "vente"
        }
    )

    assert response.status_code == 401