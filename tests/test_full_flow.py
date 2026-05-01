from fastapi.testclient import TestClient
from main import app
from app.database import SessionLocal
from app.models.user import User

client = TestClient(app)


def register_user(email: str, password: str = "Test1234"):
    client.post(
        "/auth/register",
        json={"email": email, "password": password},
    )


def promote_admin(email: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    user.role = "admin"
    db.commit()
    db.close()


def get_token(email: str, password: str = "Test1234"):
    response = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )
    return response.json()["access_token"]


def test_full_vehicle_dossier_document_flow():
    admin_email = "admin_test_flow@mmotors.fr"
    user_email = "client_test_flow@mmotors.fr"

    register_user(admin_email)
    register_user(user_email)
    promote_admin(admin_email)

    admin_token = get_token(admin_email)
    user_token = get_token(user_email)

    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    user_headers = {"Authorization": f"Bearer {user_token}"}

    vehicle_response = client.post(
        "/vehicles/",
        json={
            "brand": "TestBrand",
            "model": "TestModel",
            "price": 15000,
            "type": "vente",
            "mileage": 120000,
            "year": 2020,
            "engine": "Essence",
            "power": 150,
            "description": "Véhicule de test",
        },
        headers=admin_headers,
    )

    assert vehicle_response.status_code == 201

    vehicle_id = vehicle_response.json()["id"]

    update_response = client.put(
        f"/vehicles/{vehicle_id}",
        json={"price": 16000, "type": "location"},
        headers=admin_headers,
    )

    assert update_response.status_code == 200
    assert update_response.json()["price"] == 16000

    image_response = client.post(
        f"/vehicles/{vehicle_id}/images",
        files={"image": ("car.jpg", b"fake-image-content", "image/jpeg")},
        headers=admin_headers,
    )

    assert image_response.status_code == 200

    dossier_response = client.post(
        "/dossiers/",
        json={
            "vehicle_id": vehicle_id,
            "message": "Demande de test",
        },
        headers=user_headers,
    )

    assert dossier_response.status_code == 200

    dossier_id = dossier_response.json()["id"]

    my_dossiers_response = client.get("/dossiers/me", headers=user_headers)
    assert my_dossiers_response.status_code == 200
    assert isinstance(my_dossiers_response.json(), list)

    admin_dossiers_response = client.get("/dossiers/", headers=admin_headers)
    assert admin_dossiers_response.status_code == 200

    update_dossier_response = client.put(
        f"/dossiers/{dossier_id}",
        json={
            "status": "en_cours",
            "admin_comment": "Dossier en analyse",
        },
        headers=admin_headers,
    )

    assert update_dossier_response.status_code == 200
    assert update_dossier_response.json()["status"] == "en_cours"

    document_response = client.post(
        f"/documents/{dossier_id}/documents",
        files={"file": ("document.pdf", b"fake-pdf-content", "application/pdf")},
        headers=user_headers,
    )

    assert document_response.status_code == 200

    documents_list_response = client.get(
        f"/documents/{dossier_id}",
        headers=user_headers,
    )

    assert documents_list_response.status_code == 200
    assert isinstance(documents_list_response.json(), list)