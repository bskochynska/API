from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User

async def authenticate_user(db: AsyncSession, email: str, password: str):
    """
    Checks user data
    """
    try:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user:
            return None
        if user.hashed_password != password:
            return None

        return user
    except Exception:
        return None
