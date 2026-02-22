from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime

class OrderType(str, Enum):
    OrderBy = "OrderBy"
    OrderByDescending = "OrderByDescending"
    ThenBy = "ThenBy"
    ThenByDescending = "ThenByDescending"

class BookingStatus(str, Enum):
    Pending = "Pending"
    Confirmed = "Confirmed"
    Canceled = "Canceled"

class BookingBase(BaseModel):
    session_id: int
    row_number: int
    seat_number: int
    user_id: str

class BookingCreate(BookingBase):
    """Схема для POST запиту."""
    pass

class BookingFilterParams(BaseModel):
    pageSize: int = Field(10, gt=0)
    orderField: Optional[List[str]] = None
    orderType: Optional[List[OrderType]] = None
    UserId: Optional[str] = None
    SessionId: Optional[int] = None
    Statuses: Optional[List[BookingStatus]] = None
    MinCreatedAt: Optional[datetime] = None
    MaxCreatedAt: Optional[datetime] = None
    PageIndex: int = Field(0, ge=0)

class BookingResponse(BookingBase):
    id: int
    status: BookingStatus
    created_at: datetime

    class Config:
        from_attributes = True
