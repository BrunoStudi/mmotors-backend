from pydantic import BaseModel


class VehicleImageResponse(BaseModel):
    id: int
    image_url: str

    class Config:
        from_attributes = True


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
    images: list[VehicleImageResponse] = []

    class Config:
        from_attributes = True