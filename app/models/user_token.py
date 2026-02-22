from sqlalchemy import Column, String, DateTime, ForeignKey, text
from app.db.base import Base

class UserToken(Base):
    __tablename__ = "user_tokens"
    user_id = Column(String(450), ForeignKey("users.id"), primary_key=True)
    login_provider = Column(String(128), primary_key=True)
    name = Column(String(128), primary_key=True)
    value = Column(String(2048), nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False
    )
