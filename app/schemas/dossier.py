from datetime import datetime
from pydantic import BaseModel


class DossierCreate(BaseModel):
    vehicle_id: int
    message: str | None = None


class DossierResponse(BaseModel):
    id: int
    user_id: int
    vehicle_id: int
    request_type: str
    status: str
    message: str | None
    admin_comment: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class DossierUpdate(BaseModel):
    status: str
    admin_comment: str | None = None