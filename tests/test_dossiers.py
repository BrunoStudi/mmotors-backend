import uuid

from fastapi.testclient import TestClient

from app.core.security import hash_password
from app.database import SessionLocal
from app.models.dossier import Dossier
from app.models.user import User
from app.models.vehicle import Vehicle
from main import app


client = TestClient(app)


def create_user(role="client"):
    db = SessionLocal()

    email = f"{role}_{uuid.uuid4().hex}@test.com"

    user = User(
        email=email,
        password=hash_password("Test1234"),
        role=role,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    user_id = user.id
    db.close()

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "Test1234",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return user_id, {"Authorization": f"Bearer {token}"}


def create_vehicle():
    db = SessionLocal()

    vehicle = Vehicle(
        brand="Mercedes",
        model="Classe A",
        price=25000,
        type="location",
        mileage=50000,
        year=2021,
        engine="Essence",
        power=136,
        description="Véhicule injecté pour test dossier",
    )

    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)

    vehicle_id = vehicle.id
    db.close()

    return vehicle_id


def create_dossier(user_id, vehicle_id):
    db = SessionLocal()

    dossier = Dossier(
        user_id=user_id,
        vehicle_id=vehicle_id,
        request_type="location",
        status="soumis",
        message="Dossier injecté pour test",
    )

    db.add(dossier)
    db.commit()
    db.refresh(dossier)

    dossier_id = dossier.id
    db.close()

    return dossier_id


def test_get_my_dossiers_without_token():
    response = client.get("/dossiers/me")

    assert response.status_code == 401


def test_get_admin_dossiers_without_token():
    response = client.get("/dossiers/")

    assert response.status_code == 401


def test_create_dossier_without_auth():
    vehicle_id = create_vehicle()

    response = client.post(
        "/dossiers/",
        json={
            "vehicle_id": vehicle_id,
            "message": "test",
        },
    )

    assert response.status_code == 401


def test_client_can_create_dossier_with_injected_vehicle():
    _, client_headers = create_user("client")
    vehicle_id = create_vehicle()

    response = client.post(
        "/dossiers/",
        json={
            "vehicle_id": vehicle_id,
            "message": "Demande de location test",
        },
        headers=client_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] is not None
    assert data["message"] == "Demande de location test"
    assert data["request_type"] == "location"


def test_client_can_get_only_his_dossiers():
    user_id, client_headers = create_user("client")
    vehicle_id = create_vehicle()
    dossier_id = create_dossier(user_id, vehicle_id)

    response = client.get("/dossiers/me", headers=client_headers)

    assert response.status_code == 200

    dossiers = response.json()

    assert isinstance(dossiers, list)
    assert any(dossier["id"] == dossier_id for dossier in dossiers)


def test_admin_can_get_all_dossiers():
    user_id, _ = create_user("client")
    _, admin_headers = create_user("admin")

    vehicle_id = create_vehicle()
    dossier_id = create_dossier(user_id, vehicle_id)

    response = client.get("/dossiers/", headers=admin_headers)

    assert response.status_code == 200

    dossiers = response.json()

    assert isinstance(dossiers, list)
    assert any(dossier["id"] == dossier_id for dossier in dossiers)


def test_admin_can_update_dossier_status():
    user_id, _ = create_user("client")
    _, admin_headers = create_user("admin")

    vehicle_id = create_vehicle()
    dossier_id = create_dossier(user_id, vehicle_id)

    response = client.put(
        f"/dossiers/{dossier_id}",
        json={
            "status": "validé",
            "admin_comment": "Dossier accepté",
        },
        headers=admin_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == dossier_id
    assert data["status"] == "validé"
    assert data["admin_comment"] == "Dossier accepté"