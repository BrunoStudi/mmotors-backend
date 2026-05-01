from datetime import datetime
from pydantic import BaseModel


class DossierCreate(BaseModel):
    vehicle_id: int
    message: str | None = None


class DossierResponse(BaseModel):
    id: int
    request_type: str
    status: str
    message: str | None
    admin_comment: str | None
    user_email: str
    vehicle_name: str
    vehicle_image: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class DossierUpdate(BaseModel):
    status: str
    admin_comment: str | None = None


