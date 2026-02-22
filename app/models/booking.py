from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, text
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.schemas.booking import BookingStatus

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    row_number = Column(Integer, nullable=False)
    seat_number = Column(Integer, nullable=False)
    status = Column(Enum(BookingStatus), nullable=False, default=BookingStatus.Pending)

    created_at = Column(
        DateTime(timezone=True),
        server_default=text('CURRENT_TIMESTAMP')
    )

    session = relationship("Session", back_populates="bookings")
    user = relationship("User", back_populates="bookings")
