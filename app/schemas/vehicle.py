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
    mileage: int | None = None
    year: int | None = None
    engine: str | None = None
    power: int | None = None
    description: str | None = None


class VehicleResponse(BaseModel):
    id: int
    brand: str
    model: str
    price: float
    type: str
    mileage: int | None = None
    year: int | None = None
    engine: str | None = None
    power: int | None = None
    description: str | None = None
    images: list[VehicleImageResponse] = []

    class Config:
        from_attributes = True


class VehicleUpdate(BaseModel):
    brand: str | None = None
    model: str | None = None
    price: float | None = None
    type: str | None = None
    mileage: int | None = None
    year: int | None = None
    engine: str | None = None
    power: int | None = None
    description: str | None = None