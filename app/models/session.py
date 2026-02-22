from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.enums import SessionStatus

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)
    cinema_hall_id = Column(Integer, ForeignKey("cinema_halls.id"), nullable=False)
    status = Column(Enum(SessionStatus), nullable=False)
    ticket_price = Column(Numeric(18, 2), nullable=False)
    content = relationship("Content", back_populates="sessions")
    cinema_hall = relationship("CinemaHall", back_populates="sessions")
    bookings = relationship("Booking", back_populates="session")
