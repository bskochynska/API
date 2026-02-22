from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: str
    is_active: bool

    class Config:
        from_attributes = True

class UserInfoResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

class UserRoleResponse(BaseModel):
    id: int
    name: str
