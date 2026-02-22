from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.genre import GenreResponse, GenreCreate, GenreUpdate
from app.crud import genre as crud
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

router = APIRouter(
    prefix="/api/v1/genres",
    tags=["Genre"],
    dependencies=[Depends(oauth2_scheme)]
)

@router.get("/{id}/exists")
async def check_genre_exists(id: int, db: AsyncSession = Depends(get_db)):
    """Checks if a Genre entity with the specified ID exists."""
    return await crud.check_exists(db, id)

@router.get("/", response_model=list[GenreResponse])
async def get_genres(db: AsyncSession = Depends(get_db)):
    """Retrieves a list of all Genre entities."""
    return await crud.get_all(db)

@router.post("/", response_model=GenreResponse, status_code=status.HTTP_201_CREATED)
async def create_genre(obj_in: GenreCreate, db: AsyncSession = Depends(get_db)):
    """Creates a new Genre entity."""
    return await crud.create(db, obj_in)

@router.get("/{id}", response_model=GenreResponse)
async def get_genre(id: int, db: AsyncSession = Depends(get_db)):
    """Retrieves a specific Genre entity by its unique identifier."""
    res = await crud.get_by_id(db, id)
    if not res: raise HTTPException(404, "Genre not found")
    return res

@router.put("/{id}", response_model=GenreResponse)
async def update_genre(id: int, obj_in: GenreUpdate, db: AsyncSession = Depends(get_db)):
    """Updates an existing Genre entity."""
    db_obj = await crud.get_by_id(db, id)
    if not db_obj: raise HTTPException(404, "Genre not found")
    return await crud.update(db, db_obj, obj_in)

@router.delete("/{id}")
async def delete_genre(id: int, db: AsyncSession = Depends(get_db)):
    """Deletes a specific Genre entity by its unique identifier."""
    await crud.remove(db, id)
    return {"status": "deleted"}
