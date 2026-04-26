from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleResponse
from typing import Optional

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=VehicleResponse)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
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