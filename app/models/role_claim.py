from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, text # 1. Імпортуємо text
from app.db.base import Base

class RoleClaim(Base):
    __tablename__ = "role_claims"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(String(450), ForeignKey("roles.id"), nullable=False)
    claim_type = Column(String(256), nullable=True)
    claim_value = Column(String(256), nullable=True)

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
