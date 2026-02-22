from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud import utils as crud_utils
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

router = APIRouter(
    prefix="/api/v1/utils",
    tags=["Seed"],
    dependencies=[Depends(oauth2_scheme)]
)

@router.post("/seed", status_code=status.HTTP_201_CREATED)
async def seed_db(db: AsyncSession = Depends(get_db)):
    """
    Seeds the database with fake data.
    Restricted to Admins and Development environment or explicit config enable.
    """
    success = await crud_utils.seed_database(db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while seeding database"
        )
    return {"message": "Database seeded successfully"}
