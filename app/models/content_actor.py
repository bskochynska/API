from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class ContentActor(Base):
    __tablename__ = "content_actors"
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)
    actor_id = Column(Integer, ForeignKey("actors.id"), nullable=False)
    role_name = Column(String(255), nullable=False)
    content = relationship("Content", back_populates="content_actors")
    actor = relationship("Actor", back_populates="content_actors")
