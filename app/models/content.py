from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy import Text

class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(512), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    rating = Column(Numeric(3, 1), nullable=True)
    age_rating = Column(Integer, nullable=False)
    release_year = Column(Integer, nullable=False)
    director_full_name = Column(String(512), nullable=False)
    trailer_url = Column(String(2048), nullable=True)
    poster_url = Column(String(512), nullable=True)
    banner_url = Column(String(512), nullable=True)
    duration_minutes = Column(Integer, nullable=False)
    sessions = relationship("Session", back_populates="content")
    favorite_contents = relationship("FavoriteContent", back_populates="content")
    content_genres = relationship("ContentGenre", back_populates="content")
    content_actors = relationship("ContentActor", back_populates="content")
