from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.content import ContentResponse

class SessionBase(BaseModel):
    content_id: int
    cinema_hall_id: int
    start_time: datetime
    ticket_price: float

class SessionCreate(SessionBase):
    pass

class SessionUpdate(BaseModel):
    content_id: Optional[int] = None
    cinema_hall_id: Optional[int] = None
    start_time: Optional[datetime] = None
    ticket_price: float

class SessionResponse(SessionBase):
    id: int

    class Config:
        from_attributes = True

class SessionWithContentResponse(SessionResponse):
    content: ContentResponse
