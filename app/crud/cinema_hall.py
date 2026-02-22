from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, exists
from app.models.cinema_hall import CinemaHall
from app.schemas.cinema_hall import CinemaHallCreate, CinemaHallUpdate

async def get_all(db: AsyncSession):
    result = await db.execute(select(CinemaHall))
    return result.scalars().all()

async def get_by_id(db: AsyncSession, hall_id: int):
    result = await db.execute(select(CinemaHall).where(CinemaHall.id == hall_id))
    return result.scalar_one_or_none()

async def check_exists(db: AsyncSession, hall_id: int) -> bool:
    stmt = select(exists().where(CinemaHall.id == hall_id))
    result = await db.execute(stmt)
    return result.scalar() or False

async def create(db: AsyncSession, obj_in: CinemaHallCreate):
    db_obj = CinemaHall(**obj_in.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def update(db: AsyncSession, db_obj: CinemaHall, obj_in: CinemaHallUpdate):
    update_data = obj_in.model_dump(exclude_unset=True)
    try:
        if "name" in update_data: db_obj.name = update_data["name"]
        if "rows_count" in update_data: db_obj.rows_count = update_data["rows_count"]
        if "seats_per_row" in update_data: db_obj.seats_per_row = update_data["seats_per_row"]

        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    except Exception:
        await db.rollback()
        return None

async def remove(db: AsyncSession, hall_id: int):
    await db.execute(delete(CinemaHall).where(CinemaHall.id == hall_id))
    await db.commit()
