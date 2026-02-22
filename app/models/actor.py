from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.db.base import Base
class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    photo_url = Column(String(512), nullable=True)
    content_actors = relationship("ContentActor", back_populates="actor")
