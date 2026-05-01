from typing import Optional, Annotated
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.dependencies import get_db, require_admin
from app.models.user import User
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleResponse
from app.models.vehicle_image import VehicleImage
from app.models.dossier import Dossier
from app.models.document import Document
from app.models.vehicle_image import VehicleImage
import os
import shutil

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


@router.post("/", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    new_vehicle = Vehicle(
        brand=vehicle.brand,
        model=vehicle.model,
        price=vehicle.price,
        type=vehicle.type.lower(),
        mileage=vehicle.mileage,
        year=vehicle.year,
        engine=vehicle.engine,
        power=vehicle.power,
        description=vehicle.description,
    )

    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)

    return new_vehicle


@router.post("/{vehicle_id}/images")
def upload_vehicle_image(
    vehicle_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Véhicule introuvable"
        )

    if not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seuls les fichiers image sont autorisés",
        )

    upload_dir = f"uploads/vehicles/{vehicle_id}"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = f"{upload_dir}/{image.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    image_url = f"/uploads/vehicles/{vehicle_id}/{image.filename}"

    vehicle_image = VehicleImage(vehicle_id=vehicle_id, image_url=image_url)

    db.add(vehicle_image)
    db.commit()

    return {"message": "Image ajoutée avec succès", "image": image_url}


@router.put("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(
    vehicle_id: int,
    vehicle_data: VehicleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Véhicule introuvable"
        )

    update_data = vehicle_data.model_dump(exclude_unset=True)

    if "type" in update_data and update_data["type"]:
        update_data["type"] = update_data["type"].lower()

    for field, value in update_data.items():
        setattr(vehicle, field, value)

    db.commit()
    db.refresh(vehicle)

    return vehicle


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Véhicule introuvable"
        )

    dossiers = db.query(Dossier).filter(Dossier.vehicle_id == vehicle_id).all()

    for dossier in dossiers:
        documents = db.query(Document).filter(Document.dossier_id == dossier.id).all()

        for document in documents:
            file_path = document.file_url.lstrip("/")
            if os.path.exists(file_path):
                os.remove(file_path)

            db.delete(document)

        db.delete(dossier)

    images = db.query(VehicleImage).filter(VehicleImage.vehicle_id == vehicle_id).all()

    for image in images:
        file_path = image.image_url.lstrip("/")
        if os.path.exists(file_path):
            os.remove(file_path)

        db.delete(image)

    db.delete(vehicle)
    db.commit()

    return


@router.delete("/images/{image_id}", status_code=204)
def delete_vehicle_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    image = db.query(VehicleImage).filter(VehicleImage.id == image_id).first()

    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image introuvable"
        )

    file_path = image.image_url.lstrip("/")

    if os.path.exists(file_path):
        os.remove(file_path)

    db.delete(image)
    db.commit()

    return


@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Véhicule introuvable"
        )

    return vehicle

@router.get("/", response_model=list[VehicleResponse])
def get_vehicles(type: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Vehicle)

    if type:
        query = query.filter(Vehicle.type == type.lower())

    return query.all()
