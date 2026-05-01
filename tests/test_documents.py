from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_documents_without_auth():
    response = client.get("/documents/1")

    assert response.status_code == 401

def test_upload_document_without_auth():
    response = client.post("/documents/1/documents")

    assert response.status_code == 401