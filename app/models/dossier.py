from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Dossier(Base):
    __tablename__ = "dossiers"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)

    request_type = Column(String, nullable=False)  # achat ou location
    status = Column(String, default="soumis")

    message = Column(Text, nullable=True)
    admin_comment = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    vehicle = relationship("Vehicle")