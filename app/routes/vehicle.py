from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db, require_admin
from app.models.user import User
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleResponse

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



@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

@router.get("/", response_model=list[VehicleResponse])
def get_vehicles(type: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Vehicle)

    if type:
        query = query.filter(Vehicle.type == type.lower())

    return query.all()