from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base

class CinemaHall(Base):
    __tablename__ = "cinema_halls"

    id = Column(Integer, primary_key=True, index=True)
    total_capacity = Column(Integer, nullable=False)
    number_of_rows = Column(Integer, nullable=False)
    name = Column(String(512), nullable=False)
    seats_per_row = Column(JSON, nullable=False)
    sessions = relationship("Session", back_populates="cinema_hall")
