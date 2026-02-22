from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.session import SessionResponse, SessionWithContentResponse, SessionCreate, SessionUpdate
from app.crud import session as crud
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

router = APIRouter(
    prefix="/api/v1/sessions",
    tags=["Session"],
    dependencies=[Depends(oauth2_scheme)]
)

@router.get("/filter", response_model=list[SessionResponse])
async def filter_sessions(db: AsyncSession = Depends(get_db)):
    """Retrieves session items based on filter, pagination, and ordering criteria."""
    return await crud.get_all(db)

@router.get("/filter-with-content", response_model=list[SessionWithContentResponse])
async def filter_with_content(db: AsyncSession = Depends(get_db)):
    """Retrieves session items along with their associated content details."""
    return await crud.get_with_content(db)

@router.get("/{id}/exists")
async def check_session_exists(id: int, db: AsyncSession = Depends(get_db)):
    """Checks if a Session entity with the specified ID exists."""
    return await crud.check_exists(db, id)

@router.get("/", response_model=list[SessionResponse])
async def get_sessions(db: AsyncSession = Depends(get_db)):
    """Retrieves a list of all Session entities."""
    return await crud.get_all(db)

@router.post("/", response_model=SessionResponse)
async def create_session(obj_in: SessionCreate, db: AsyncSession = Depends(get_db)):
    """Creates a new Session entity."""
    return await crud.create(db, obj_in)

@router.get("/{id}", response_model=SessionResponse)
async def get_session(id: int, db: AsyncSession = Depends(get_db)):
    """Retrieves a specific Session entity by its unique identifier."""
    res = await crud.get_by_id(db, id)
    if not res: raise HTTPException(404, "Session not found")
    return res

@router.put("/{id}", response_model=SessionResponse)
async def update_session(id: int, obj_in: SessionUpdate, db: AsyncSession = Depends(get_db)):
    """Updates an existing Session entity."""
    db_obj = await crud.get_by_id(db, id)
    if not db_obj: raise HTTPException(404)
    return await crud.update(db, db_obj, obj_in)

@router.delete("/{id}")
async def delete_session(id: int, db: AsyncSession = Depends(get_db)):
    """Deletes a specific Session entity by its unique identifier."""
    await crud.remove(db, id)
    return {"status": "deleted"}
