import uuid
import io

from fastapi.testclient import TestClient

from app.core.security import hash_password
from app.database import SessionLocal
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.dossier import Dossier
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

    login = client.post(
        "/auth/login",
        json={"email": email, "password": "Test1234"},
    )

    token = login.json()["access_token"]

    return user_id, {"Authorization": f"Bearer {token}"}


def create_vehicle():
    db = SessionLocal()

    vehicle = Vehicle(
        brand="BMW",
        model="X1",
        price=30000,
        type="vente",
        mileage=40000,
        year=2022,
        engine="Essence",
        power=150,
        description="Test doc",
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
        request_type="vente",
        status="soumis",
        message="Test dossier",
    )

    db.add(dossier)
    db.commit()
    db.refresh(dossier)

    dossier_id = dossier.id
    db.close()

    return dossier_id


def test_get_documents_without_auth():
    response = client.get("/documents/1")

    assert response.status_code == 401


def test_upload_document_without_auth():
    response = client.post("/documents/1/documents")

    assert response.status_code == 401


def test_client_can_upload_document():
    user_id, headers = create_user("client")
    vehicle_id = create_vehicle()
    dossier_id = create_dossier(user_id, vehicle_id)

    file = io.BytesIO(b"fake file content")

    response = client.post(
        f"/documents/{dossier_id}/documents",
        files={"file": ("test.pdf", file, "application/pdf")},
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Document ajouté"
    assert "file_url" in data
    assert data["file_url"].endswith("test.pdf")


def test_client_can_get_documents():
    user_id, headers = create_user("client")
    vehicle_id = create_vehicle()
    dossier_id = create_dossier(user_id, vehicle_id)

    # upload fichier
    file = io.BytesIO(b"fake file content")

    client.post(
        f"/documents/{dossier_id}/documents",
        files={"file": ("test.pdf", file, "application/pdf")},
        headers=headers,
    )

    response = client.get(f"/documents/{dossier_id}", headers=headers)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1


def test_admin_can_access_all_documents():
    user_id, _ = create_user("client")
    _, admin_headers = create_user("admin")

    vehicle_id = create_vehicle()
    dossier_id = create_dossier(user_id, vehicle_id)

    file = io.BytesIO(b"fake file content")

    client.post(
        f"/documents/{dossier_id}/documents",
        files={"file": ("test.pdf", file, "application/pdf")},
        headers=admin_headers,
    )

    response = client.get(f"/documents/{dossier_id}", headers=admin_headers)

    assert response.status_code == 200