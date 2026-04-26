from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # "vente" ou "location"