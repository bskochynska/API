from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, exists
from sqlalchemy.orm import joinedload
from app.models.session import Session
from app.schemas.session import SessionCreate, SessionUpdate

async def get_all(db: AsyncSession):
    result = await db.execute(select(Session))
    return result.scalars().all()

async def get_with_content(db: AsyncSession):
    """Отримує сесії разом із деталями контенту (JOIN)."""
    result = await db.execute(select(Session).options(joinedload(Session.content)))
    return result.scalars().all()

async def get_by_id(db: AsyncSession, session_id: int):
    result = await db.execute(select(Session).where(Session.id == session_id))
    return result.scalar_one_or_none()

async def check_exists(db: AsyncSession, session_id: int) -> bool:
    stmt = select(exists().where(Session.id == session_id))
    result = await db.execute(stmt)
    return result.scalar() or False

async def create(db: AsyncSession, obj_in: SessionCreate):
    db_obj = Session(**obj_in.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def update(db: AsyncSession, db_obj: Session, obj_in: SessionUpdate):
    update_data = obj_in.model_dump(exclude_unset=True)
    try:
        if "content_id" in update_data: db_obj.content_id = update_data["content_id"]
        if "cinema_hall_id" in update_data: db_obj.cinema_hall_id = update_data["cinema_hall_id"]
        if "start_time" in update_data: db_obj.start_time = update_data["start_time"]
        if "price" in update_data: db_obj.price = update_data["price"]

        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    except Exception:
        await db.rollback()
        return None

async def remove(db: AsyncSession, session_id: int):
    await db.execute(delete(Session).where(Session.id == session_id))
    await db.commit()
