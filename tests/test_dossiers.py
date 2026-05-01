from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_my_dossiers_without_token():
    response = client.get("/dossiers/me")

    assert response.status_code == 401


def test_get_admin_dossiers_without_token():
    response = client.get("/dossiers/")

    assert response.status_code == 401

def test_create_dossier_without_auth():
    response = client.post(
        "/dossiers/",
        json={
            "vehicle_id": 1,
            "message": "test"
        }
    )

    assert response.status_code == 401

def test_admin_access_without_token():
    response = client.get("/dossiers/")

    assert response.status_code == 401