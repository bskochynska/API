import uuid
from sqlalchemy import Column, String
from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class Role(Base):
    __tablename__ = "roles"
    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    name = Column(String(256), nullable=True)
    normalized_name = Column(String(256), nullable=True)
    concurrency_stamp = Column(String(256), nullable=True, default=lambda: str(uuid.uuid4()))
