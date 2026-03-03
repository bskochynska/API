from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, exists
from app.models.content import Content
from app.schemas.content import ContentCreate, ContentUpdate

async def get_all(db: AsyncSession):
    """
    Gets all movies
    """
    result = await db.execute(select(Content))
    return result.scalars().all()

async def get_by_id(db: AsyncSession, content_id: int):
    """Gets movie by ID"""
    result = await db.execute(select(Content).where(Content.id == content_id))
    return result.scalar_one_or_none()

async def check_exists(db: AsyncSession, content_id: int) -> bool:
    """Checks if movie exists"""
    stmt = select(exists().where(Content.id == content_id))
    result = await db.execute(stmt)
    return result.scalar() or False

async def create(db: AsyncSession, obj_in: ContentCreate):
    """Creates new movie"""
    db_obj = Content(**obj_in.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def update(db: AsyncSession, db_obj: Content, obj_in: ContentUpdate):
    """
    Updates movie
    """
    update_data = obj_in.model_dump(exclude_unset=True)
    try:
        if "title" in update_data:
            db_obj.title = update_data["title"]
        if "description" in update_data:
            db_obj.description = update_data["description"]
        if "release_date" in update_data:
            db_obj.release_date = update_data["release_date"]

        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    except Exception:
        await db.rollback()
        return None

async def remove(db: AsyncSession, content_id: int):
    """Movie removal"""
    try:
        await db.execute(delete(Content).where(Content.id == content_id))
        await db.commit()
    except Exception:
        await db.rollback()
