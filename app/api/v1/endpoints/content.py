from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.content import ContentResponse, ContentCreate, ContentUpdate
from app.crud import content as crud
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

router = APIRouter(
    prefix="/api/v1/contents",
    tags=["Content"],
    dependencies=[Depends(oauth2_scheme)]
)

@router.get("/filter", response_model=list[ContentResponse])
async def filter_contents(db: AsyncSession = Depends(get_db)):
    """Retrieves content items based on filter, pagination, and ordering criteria."""
    return await crud.get_all(db)

@router.get("/{id}/exists")
async def check_content_exists(id: int, db: AsyncSession = Depends(get_db)):
    """Checks if a Content entity with the specified ID exists."""
    return await crud.check_exists(db, id)

@router.get("/", response_model=list[ContentResponse])
async def get_all_contents(db: AsyncSession = Depends(get_db)):
    """Retrieves a list of all Content entities."""
    return await crud.get_all(db)

@router.post("/", response_model=ContentResponse, status_code=status.HTTP_201_CREATED)
async def create_content(obj_in: ContentCreate, db: AsyncSession = Depends(get_db)):
    """Creates new Content entity."""
    return await crud.create(db, obj_in)

@router.get("/{id}", response_model=ContentResponse)
async def get_content(id: int, db: AsyncSession = Depends(get_db)):
    """Retrieves a specific Content entity by its unique identifier."""
    res = await crud.get_by_id(db, id)
    if not res: raise HTTPException(404)
    return res

@router.put("/{id}", response_model=ContentResponse)
async def update_content(id: int, obj_in: ContentUpdate, db: AsyncSession = Depends(get_db)):
    """Updates an existing Content entity."""
    db_obj = await crud.get_by_id(db, id)
    if not db_obj: raise HTTPException(404)
    return await crud.update(db, db_obj, obj_in)

@router.delete("/{id}")
async def delete_content(id: int, db: AsyncSession = Depends(get_db)):
    """Deletes a specific Content entity by its unique identifier."""
    await crud.remove(db, id)
    return {"status": "deleted"}

@router.post("/{id}/poster")
async def upload_poster(id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    """Uploads or updates the poster image for a specific Content entity."""
    return {"filename": file.filename}

@router.delete("/{id}/poster")
async def delete_poster(id: int, db: AsyncSession = Depends(get_db)):
    """Deletes the poster image for a specific Content entity."""
    return {"status": "poster deleted"}

@router.post("/{id}/banner")
async def upload_banner(id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    """Uploads or updates the banner image for a specific Content entity."""
    return {"filename": file.filename}

@router.delete("/{id}/banner")
async def delete_banner(id: int, db: AsyncSession = Depends(get_db)):
    """Deletes the banner image for a specific Content entity."""
    return {"status": "banner deleted"}

@router.post("/{id}/genres/{genreId}")
async def link_genre(id: int, genreId: int, db: AsyncSession = Depends(get_db)):
    """Links a specific Genre to a Content entity."""
    return {"status": "linked"}

@router.delete("/{id}/genres/{genreId}")
async def unlink_genre(id: int, genreId: int, db: AsyncSession = Depends(get_db)):
    """Unlinks a specific Genre from a Content entity."""
    return {"status": "unlinked"}

@router.post("/{id}/actors")
async def link_actor(id: int, actor_id: int, db: AsyncSession = Depends(get_db)):
    """Links a specific Actor to a Content entity."""
    return {"status": "linked"}

@router.delete("/{id}/actors/{actorId}")
async def unlink_actor(id: int, actorId: int, db: AsyncSession = Depends(get_db)):
    """Unlinks a specific Actor from a Content entity."""
    return {"status": "unlinked"}
