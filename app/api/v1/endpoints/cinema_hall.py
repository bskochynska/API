from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.cinema_hall import CinemaHallResponse, CinemaHallCreate, CinemaHallUpdate
from app.crud import cinema_hall as crud

router = APIRouter(prefix="/api/v1/cinema-halls", tags=["CinemaHall"])

@router.get("/filter", response_model=list[CinemaHallResponse])
async def filter_halls(db: AsyncSession = Depends(get_db)):
    """Retrieves cinema hall items based on filter, pagination, and ordering criteria."""
    return await crud.get_all(db)

@router.get("/{id}/exists")
async def check_hall_exists(id: int, db: AsyncSession = Depends(get_db)):
    """Checks if a CinemaHall entity with the specified ID exists."""
    return await crud.check_exists(db, id)

@router.get("/", response_model=list[CinemaHallResponse])
async def get_all_halls(db: AsyncSession = Depends(get_db)):
    """Retrieves a list of all CinemaHall entities."""
    return await crud.get_all(db)

@router.post("/", response_model=CinemaHallResponse)
async def create_hall(obj_in: CinemaHallCreate, db: AsyncSession = Depends(get_db)):
    """Creates a new CinemaHall entity."""
    return await crud.create(db, obj_in)

@router.get("/{id}", response_model=CinemaHallResponse)
async def get_hall(id: int, db: AsyncSession = Depends(get_db)):
    """Retrieves a specific CinemaHall entity by its unique identifier."""
    res = await crud.get_by_id(db, id)
    if not res: raise HTTPException(404, "Hall not found")
    return res

@router.put("/{id}", response_model=CinemaHallResponse)
async def update_hall(id: int, obj_in: CinemaHallUpdate, db: AsyncSession = Depends(get_db)):
    """Updates an existing CinemaHall entity."""
    db_obj = await crud.get_by_id(db, id)
    if not db_obj: raise HTTPException(404)
    return await crud.update(db, db_obj, obj_in)

@router.delete("/{id}")
async def delete_hall(id: int, db: AsyncSession = Depends(get_db)):
    """Deletes a specific CinemaHall entity by its unique identifier."""
    await crud.remove(db, id)
    return {"status": "deleted"}
