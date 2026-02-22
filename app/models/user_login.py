from sqlalchemy import Column, String, DateTime, ForeignKey, text
from app.db.base import Base

class UserLogin(Base):
    __tablename__ = "user_logins"
    login_provider = Column(String(128), primary_key=True)
    provider_key = Column(String(128), primary_key=True)
    provider_display_name = Column(String(255), nullable=True)
    user_id = Column(String(450), ForeignKey("users.id"), nullable=False, index=True)
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
