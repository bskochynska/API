from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class FavoriteContent(Base):
    __tablename__ = "favorite_contents"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(450), ForeignKey("users.id"), nullable=False)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)
    user = relationship("User", back_populates="favorite_contents")
    content = relationship("Content", back_populates="favorite_contents")
