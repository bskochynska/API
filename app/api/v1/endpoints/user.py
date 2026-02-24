from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserInfoResponse, UserCreate, UserUpdate
from app.crud import user as crud
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
protected = Depends(oauth2_scheme)

router = APIRouter(
    prefix="/api/v1/users",
    tags=["User"]
)

@router.post("/admins/register", response_model=UserResponse)
async def register_admin(obj_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """Реєстрація адміна з автоматичним заповненням технічних полів."""
    try:
        # Перевірка на дублікат імейлу
        res = await db.execute(select(User).where(User.email == obj_in.email))
        if res.scalar_one_or_none():
            raise HTTPException(status.status_code == 400, detail="Користувач з таким email вже існує")

        new_admin = User(
            email=obj_in.email,
            username=obj_in.email, # Використовуємо email як username для надійності
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
        raise HTTPException(status_code=500, detail=f"Admin registration error: {str(e)}")

@router.post("/customer/register", response_model=UserResponse)
async def register_customer(obj_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """Реєстрація звичайного користувача з виправленими полями моделі."""
    try:
        # 1. Перевірка на унікальність email
        res = await db.execute(select(User).where(User.email == obj_in.email))
        if res.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="User with this email already exists")

        # 2. Створення об'єкта User (використовуємо існуючі в моделі поля)
        # УВАГА: Замінив full_name на first_name/last_name, як у вашій базі
        new_user = User(
            email=obj_in.email,
            username=obj_in.email,
            hashed_password=obj_in.password,
            first_name=getattr(obj_in, 'full_name', 'Customer'), # Заглушка, якщо немає полів
            last_name="User",
            role="Customer",
            is_superuser=False,
            is_active=True
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    except Exception as e:
        await db.rollback()
        # Тепер ви побачите реальну помилку у вкладці Response!
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/my-info", response_model=UserInfoResponse, dependencies=[protected])
async def get_my_info(db: AsyncSession = Depends(get_db)):
    """Повертає інформацію про поточного користувача."""
    # Тут має бути логіка отримання поточного юзера з токена
    return {}

@router.get("/{id}/exists")
async def user_exists(id: int, db: AsyncSession = Depends(get_db)):
    """Перевіряє існування користувача."""
    return await crud.check_exists(db, id)

@router.delete("/{id}", dependencies=[protected])
async def delete_user(id: int, db: AsyncSession = Depends(get_db)):
    """Видалення користувача. Потребує токен."""
    await crud.remove(db, id)
    return {"status": "deleted"}
