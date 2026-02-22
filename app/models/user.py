import uuid
from sqlalchemy import Column, String, Boolean, DateTime, text
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String(255), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(256), unique=True, index=True, nullable=False)
    username = Column(String(256), unique=True, index=True)
    hashed_password = Column(String(1024), nullable=False)
    role = Column(String(255), default="Customer")

    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_blocked = Column(Boolean, default=False)

    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)

    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    bookings = relationship("Booking", back_populates="user")
    favorite_contents = relationship("FavoriteContent", back_populates="user")
