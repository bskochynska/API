from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, exists
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

async def get_by_id(db: AsyncSession, user_id: int):
    """Gets user by ID"""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def check_exists(db: AsyncSession, user_id: int) -> bool:
    """Checks if user with ID exists"""
    try:
        stmt = select(exists().where(User.id == user_id))
        result = await db.execute(stmt)
        return result.scalar() or False
    except Exception:
        return False

async def update(db: AsyncSession, db_obj: User, obj_in: UserUpdate):
    """
    Updates existing user
    """
    update_data = obj_in.model_dump(exclude_unset=True)
    try:
        if "username" in update_data:
            db_obj.username = update_data["username"]
        if "email" in update_data:
            db_obj.email = update_data["email"]
        if "password" in update_data:
            db_obj.hashed_password = update_data["password"]

        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    except Exception:
        await db.rollback()
        return None

async def remove(db: AsyncSession, user_id: int):
    """
    User removal
    """
    try:
        await db.execute(delete(User).where(User.id == user_id))
        await db.commit()
    except Exception:
        await db.rollback()
