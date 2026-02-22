from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class ContentGenre(Base):
    __tablename__ = "content_genres"
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)
    content = relationship("Content", back_populates="content_genres")
    genre = relationship("Genre", back_populates="content_genres")
