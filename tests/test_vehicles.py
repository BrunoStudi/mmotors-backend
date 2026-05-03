import uuid

from fastapi.testclient import TestClient

from app.core.security import hash_password
from app.database import SessionLocal
from app.models.user import User
from app.models.vehicle import Vehicle
from main import app


client = TestClient(app)


def create_admin_user():
    db = SessionLocal()

    email = f"admin_{uuid.uuid4().hex}@test.com"

    admin = User(
        email=email,
        password=hash_password("Admin1234"),
        role="admin",
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)
    db.close()

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "Admin1234",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


def create_vehicle_in_db():
    db = SessionLocal()

    vehicle = Vehicle(
        brand="Peugeot",
        model="308",
        price=18000,
        type="vente",
        mileage=85000,
        year=2020,
        engine="Diesel",
        power=130,
        description="Véhicule de test injecté en base",
    )

    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)

    vehicle_id = vehicle.id

    db.close()

    return vehicle_id


def test_get_vehicles_returns_list():
    create_vehicle_in_db()

    response = client.get("/vehicles/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_get_existing_vehicle_by_injected_id():
    vehicle_id = create_vehicle_in_db()

    response = client.get(f"/vehicles/{vehicle_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == vehicle_id
    assert data["brand"] == "Peugeot"
    assert data["model"] == "308"


def test_get_vehicle_not_found():
    response = client.get("/vehicles/999999999")

    assert response.status_code == 404


def test_create_vehicle_without_auth():
    response = client.post(
        "/vehicles/",
        json={
            "brand": "Test",
            "model": "Test",
            "price": 10000,
            "type": "vente",
        },
    )

    assert response.status_code == 401


def test_create_vehicle_with_admin_auth():
    headers = create_admin_user()

    response = client.post(
        "/vehicles/",
        json={
            "brand": "Renault",
            "model": "Clio",
            "price": 12000,
            "type": "location",
            "mileage": 60000,
            "year": 2021,
            "engine": "Essence",
            "power": 90,
            "description": "Véhicule créé pendant le test",
        },
        headers=headers,
    )

    assert response.status_code in [200, 201]

    data = response.json()

    assert data["brand"] == "Renault"
    assert data["model"] == "Clio"
    assert data["type"] == "location"