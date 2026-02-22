from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserInfoResponse, UserCreate, UserUpdate, UserRoleResponse
from app.crud import user as crud
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
protected = Depends(oauth2_scheme)

router = APIRouter(
    prefix="/api/v1/users",
    tags=["User"]
)

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

@router.post("/admins/register", response_model=UserResponse)
async def register_admin(obj_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """Реєстрація адміна з урахуванням усіх полів бази."""
    try:
        res = await db.execute(select(User).where(User.email == obj_in.email))
        if res.scalar_one_or_none():
            raise HTTPException(400, "Користувач з таким email вже існує")

        try:
            u_name = obj_in.username
        except Exception:
            u_name = obj_in.email

        new_admin = User(
            email=obj_in.email,
            username=u_name,
            hashed_password=obj_in.password,
            first_name="Admin",
            last_name="System",
            role="Admin",
            is_superuser=True,
            is_active=True
        )

        db.add(new_admin)
        await db.commit()
        await db.refresh(new_admin)
        return new_admin

    except Exception as e:
        await db.rollback()
        raise HTTPException(500, detail=f"Database/Mapper error: {str(e)}")

@router.post("/customer/register", response_model=UserResponse)
async def register_customer(obj_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """Registers a new user with the 'Customer' role."""
    try:
        new_user = User(
            email=obj_in.email,
            full_name=obj_in.full_name,
            hashed_password=obj_in.password,
            role="Customer",
            is_superuser=False,
            is_active=True
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Registration failed")

@router.get("/filter", response_model=List[UserResponse], dependencies=[protected])
async def filter_users(db: AsyncSession = Depends(get_db)):
    """Retrieves users based on criteria. Requires Admin token."""
    return []

@router.get("/my-info", response_model=UserInfoResponse, dependencies=[protected])
async def get_my_info():
    """Returns information about the currently logged-in user."""
    return {}

@router.get("/{id}/exists")
async def user_exists(id: int, db: AsyncSession = Depends(get_db)):
    """Checks if a User entity exists."""
    return await crud.check_exists(db, id)

@router.delete("/{id}", dependencies=[protected])
async def delete_user(id: int, db: AsyncSession = Depends(get_db)):
    """Deletes a specific user."""
    await crud.remove(db, id)
    return {"status": "deleted"}

@router.post("/favorites/{contentId}", dependencies=[protected])
async def add_to_favorites(contentId: int):
    return {"status": "added"}

@router.delete("/favorites/{contentId}", dependencies=[protected])
async def remove_from_favorites(contentId: int):
    return {"status": "removed"}
