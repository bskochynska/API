from sqlalchemy import select, and_, or_, asc, desc, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.actor import Actor
from app.schemas.actor import ActorFilterParams, ActorUpdate, ActorCreate

async def get_all(db: AsyncSession) -> list:
    """Gets all actors"""
    try:
        res = await db.execute(select(Actor))
        return res.scalars().all()
    except Exception:
        return []

async def get_filtered(db: AsyncSession, params: ActorFilterParams) -> list:
    """Filter actors"""
    try:
        query = select(Actor)
        if params.SearchTerms:
            term = f"%{params.SearchTerms}%"
            query = query.where(or_(Actor.first_name.ilike(term), Actor.last_name.ilike(term)))

        if params.HasPhoto is not None:
            if params.HasPhoto:
                query = query.where(Actor.photo_url.isnot(None))
            else:
                query = query.where(Actor.photo_url.is_(None))

        query = query.offset(params.PageIndex * params.pageSize).limit(params.pageSize)
        res = await db.execute(query)
        return res.scalars().all()
    except Exception:
        return []

async def get_actor(db: AsyncSession, actor_id: str):
    """Gets the actor"""
    res = await db.execute(select(Actor).where(Actor.id == actor_id))
    return res.scalar_one_or_none()

async def exists(db: AsyncSession, actor_id: str) -> bool:
    """Checks if the actor exists in database"""
    res = await db.execute(select(Actor).where(Actor.id == actor_id))
    return res.scalar_one_or_none() is not None


async def create(db: AsyncSession, obj_in: ActorCreate) -> Actor:
    """Creates new actor"""
    try:
        new_actor = Actor(**obj_in.model_dump())
        db.add(new_actor)
        await db.commit()
        await db.refresh(new_actor)
        return new_actor
    except Exception:
        await db.rollback()
        return None

async def update(db: AsyncSession, db_obj: Actor, obj_in: ActorUpdate):
    """Updated existing actor"""
    data = obj_in.model_dump(exclude_unset=True)
    try:
        if "first_name" in data: db_obj.first_name = data["first_name"]
        if "last_name" in data: db_obj.last_name = data["last_name"]
        if "biography" in data: db_obj.biography = data["biography"]

        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    except Exception:
        await db.rollback()
        return None

async def remove(db: AsyncSession, actor_id: str):
    """Actor removal"""
    try:
        await db.execute(delete(Actor).where(Actor.id == actor_id))
        await db.commit()
    except Exception:
        await db.rollback()
