from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert "message" in response.json()


def test_register_user_invalid_email():
    response = client.post(
        "/auth/register",
        json={
            "email": "email-invalide",
            "password": "Test1234"
        }
    )

    assert response.status_code == 422

def test_login_invalid_user():
    response = client.post(
        "/auth/login",
        json={
            "email": "fake@test.com",
            "password": "wrong"
        }
    )

    assert response.status_code == 401

def test_register_valid_user():
    unique_email = f"testuser_{uuid.uuid4().hex}@test.com"

    response = client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "password": "Test1234"
        }
    )

    assert response.status_code in [200, 201]