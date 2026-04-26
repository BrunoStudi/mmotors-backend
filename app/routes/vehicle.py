from typing import Optional, Annotated
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.dependencies import get_db, require_admin
from app.models.user import User
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleResponse
from app.models.vehicle_image import VehicleImage
import os
import shutil


router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


@router.post("/", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    new_vehicle = Vehicle(
        brand=vehicle.brand,
        model=vehicle.model,
        price=vehicle.price,
        type=vehicle.type.lower()
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
    current_user: User = Depends(require_admin)
):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Véhicule introuvable"
        )

    if not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seuls les fichiers image sont autorisés"
        )

    upload_dir = f"uploads/vehicles/{vehicle_id}"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = f"{upload_dir}/{image.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    image_url = f"/uploads/vehicles/{vehicle_id}/{image.filename}"

    vehicle_image = VehicleImage(
        vehicle_id=vehicle_id,
        image_url=image_url
    )

    db.add(vehicle_image)
    db.commit()

    return {
        "message": "Image ajoutée avec succès",
        "image": image_url
    }

@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

@router.get("/", response_model=list[VehicleResponse])
def get_vehicles(type: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Vehicle)

    if type:
        query = query.filter(Vehicle.type == type.lower())

    return query.all()