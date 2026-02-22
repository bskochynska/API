from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, exists
from app.models.genre import Genre
from app.schemas.genre import GenreCreate, GenreUpdate

async def get_all(db: AsyncSession):
    result = await db.execute(select(Genre))
    return result.scalars().all()

async def get_by_id(db: AsyncSession, genre_id: int):
    result = await db.execute(select(Genre).where(Genre.id == genre_id))
    return result.scalar_one_or_none()

async def check_exists(db: AsyncSession, genre_id: int) -> bool:
    stmt = select(exists().where(Genre.id == genre_id))
    result = await db.execute(stmt)
    return result.scalar() or False

async def create(db: AsyncSession, obj_in: GenreCreate):
    db_obj = Genre(**obj_in.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def update(db: AsyncSession, db_obj: Genre, obj_in: GenreUpdate):
    update_data = obj_in.model_dump(exclude_unset=True)
    try:
        if "name" in update_data:
            db_obj.name = update_data["name"]

        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    except Exception:
        await db.rollback()
        return None

async def remove(db: AsyncSession, genre_id: int):
    try:
        await db.execute(delete(Genre).where(Genre.id == genre_id))
        await db.commit()
    except Exception:
        await db.rollback()
