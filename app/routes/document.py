import os
import shutil

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.document import Document
from app.models.dossier import Dossier
from app.models.user import User

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/{dossier_id}/documents")
def upload_document(
    dossier_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    dossier = db.query(Dossier).filter(Dossier.id == dossier_id).first()

    if not dossier:
        raise HTTPException(status_code=404, detail="Dossier introuvable")

    if dossier.status == "refusé":
        raise HTTPException(status_code=400, detail="Dossier refusé")

    if dossier.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Accès interdit")

    upload_dir = f"uploads/dossiers/{dossier_id}"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = f"{upload_dir}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    doc = Document(
        dossier_id=dossier_id,
        file_url=f"/{file_path}",
    )

    db.add(doc)
    db.commit()

    return {"message": "Document ajouté", "file_url": doc.file_url}


@router.get("/{dossier_id}")
def get_documents(
    dossier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    dossier = db.query(Dossier).filter(Dossier.id == dossier_id).first()

    if not dossier:
        raise HTTPException(status_code=404, detail="Dossier introuvable")

    if dossier.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Accès interdit")

    documents = db.query(Document).filter(Document.dossier_id == dossier_id).all()

    return [
        {
            "id": doc.id,
            "file_url": doc.file_url,
            "filename": doc.file_url.split("/")[-1],
        }
        for doc in documents
    ]
