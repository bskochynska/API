from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class OrderType(str, Enum):
    OrderBy = "OrderBy"
    OrderByDescending = "OrderByDescending"
    ThenBy = "ThenBy"
    ThenByDescending = "ThenByDescending"

class ActorFilterParams(BaseModel):
    pageSize: int = Field(10, gt=0, description="Кількість елементів на сторінку (має бути > 0).")
    orderField: Optional[List[str]] = Field(None, description="Поля для сортування (напр. 'id', 'first_name').")
    orderType: Optional[List[OrderType]] = Field(None, description="Типи сортування для відповідних полів.")
    SearchTerms: Optional[str] = Field(None, description="Пошуковий запит (ім'я або біографія).")
    HasPhoto: Optional[bool] = Field(None, description="Фільтр: true - тільки з фото, false - без фото, null - ігнорувати.")
    ContentId: Optional[int] = Field(None, description="Фільтр за ID контенту, у якому знімався актор.")
    PageIndex: int = Field(0, ge=0, description="Індекс сторінки для повернення.")

# Ваші існуючі схеми
class ActorBase(BaseModel):
    first_name: str
    last_name: str
    biography: Optional[str] = None

class ActorCreate(ActorBase):
    pass

class ActorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    biography: Optional[str] = None

class ActorResponse(ActorBase):
    id: int
    photo_url: Optional[str] = None

    class Config:
        from_attributes = True
