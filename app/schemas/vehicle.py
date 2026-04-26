from pydantic import BaseModel


class VehicleCreate(BaseModel):
    brand: str
    model: str
    price: float
    type: str


class VehicleResponse(BaseModel):
    id: int
    brand: str
    model: str
    price: float
    type: str

    class Config:
        from_attributes = True