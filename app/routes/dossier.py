from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user, require_admin
from app.models.dossier import Dossier
from app.models.vehicle import Vehicle
from app.models.user import User
from app.schemas.dossier import DossierCreate, DossierResponse, DossierUpdate

router = APIRouter(prefix="/dossiers", tags=["Dossiers"])


@router.post("/", response_model=DossierResponse)
def create_dossier(
    dossier: DossierCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vehicle = db.query(Vehicle).filter(Vehicle.id == dossier.vehicle_id).first()

    if not vehicle:
        raise HTTPException(status_code=404, detail="Véhicule introuvable")

    new_dossier = Dossier(
        user_id=current_user.id,
        vehicle_id=vehicle.id,
        request_type=vehicle.type,
        message=dossier.message
    )

    db.add(new_dossier)
    db.commit()
    db.refresh(new_dossier)

    return new_dossier


@router.get("/me", response_model=list[DossierResponse])
def get_my_dossiers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Dossier).filter(Dossier.user_id == current_user.id).all()


@router.get("/", response_model=list[DossierResponse])
def get_all_dossiers(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return db.query(Dossier).all()


@router.put("/{dossier_id}", response_model=DossierResponse)
def update_dossier(
    dossier_id: int,
    data: DossierUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    dossier = db.query(Dossier).filter(Dossier.id == dossier_id).first()

    if not dossier:
        raise HTTPException(status_code=404, detail="Dossier introuvable")

    dossier.status = data.status
    dossier.admin_comment = data.admin_comment

    db.commit()
    db.refresh(dossier)

    return dossier