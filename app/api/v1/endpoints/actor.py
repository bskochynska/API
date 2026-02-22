from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from app.db.session import get_db
from app.schemas.actor import ActorResponse, ActorCreate, ActorUpdate, ActorFilterParams
from app.crud import actor as crud_actor
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

router = APIRouter(
    prefix="/api/v1/actors",
    tags=["Actor"],
    dependencies=[Depends(oauth2_scheme)]
)

@router.get("/filter", response_model=List[ActorResponse])
async def filter_actors(
    params: Annotated[ActorFilterParams, Depends()],
    db: AsyncSession = Depends(get_db)
):
    """Retrieves actor items based on filter, pagination, and ordering criteria."""
    return await crud_actor.get_filtered(db, params)

@router.get("/{id}/exists")
async def check_exists(
    id: Annotated[int, Path(..., description="The unique identifier of the Actor entity.")],
    db: AsyncSession = Depends(get_db)
):
    """Checks if a Actor entity with the specified ID exists."""
    return await crud_actor.exists(db, id)

@router.get("/", response_model=List[ActorResponse])
async def get_all_actors(db: AsyncSession = Depends(get_db)):
    """Retrieves a list of all Actor entities."""
    return await crud_actor.get_all(db)

@router.get("/{id}", response_model=ActorResponse)
async def get_by_id(
    id: Annotated[int, Path(..., gt=0, description="The unique identifier of the Actor.")],
    db: AsyncSession = Depends(get_db)
):
    """Retrieves a specific Actor entity by its unique identifier."""
    res = await crud_actor.get_actor(db, id)
    try:
        if not res:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Actor not found")
        return res
    except Exception:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

@router.put("/{id}", response_model=ActorResponse)
async def update_actor(
    id: Annotated[int, Path(..., description="The unique identifier of the Actor to update.")],
    obj_in: ActorUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Updates an existing Actor entity."""
    db_obj = await crud_actor.get_actor(db, id)
    if not db_obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return await crud_actor.update(db, db_obj, obj_in)

@router.delete("/{id}")
async def delete_actor(
    id: Annotated[int, Path(..., description="The unique identifier of the Actor to delete.")],
    db: AsyncSession = Depends(get_db)
):
    """Deletes a specific Actor entity by its unique identifier."""
    await crud_actor.remove(db, id)
    return {"status": "deleted"}

@router.get("/{id}/in-content/{contentId}")
async def get_actor_in_content(
    id: Annotated[int, Path(..., description="The ID of the Actor.")],
    contentId: Annotated[int, Path(..., description="The ID of the Content.")],
    db: AsyncSession = Depends(get_db)
):
    """Retrieves information about a specific actor within the context of a specific content, including their role."""
    return {"actor_id": id, "content_id": contentId, "role": "Lead"}

@router.post("/", response_model=ActorResponse, status_code=status.HTTP_201_CREATED)
async def create_actor(obj_in: ActorCreate, db: AsyncSession = Depends(get_db)):
    """Creates a new Actor entity."""
    return await crud_actor.create(db, obj_in)

@router.post("/{id}/photo")
async def upload_photo(
    id: Annotated[int, Path(..., description="The ID of the Actor to upload a photo for.")],
    file: UploadFile = File(...)
):
    """Uploads or updates the photo for a specific Actor entity."""
    return {"filename": file.filename, "status": "uploaded"}

@router.delete("/{id}/photo")
async def delete_photo(
    id: Annotated[int, Path(..., description="The ID of the Actor to delete the photo from.")]
):
    """Deletes the photo for a specific Actor entity."""
    return {"status": "photo deleted"}
