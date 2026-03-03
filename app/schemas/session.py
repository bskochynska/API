from pydantic import BaseModel
from datetime import datetime
from app.schemas.content import ContentResponse
from app.models.enums import SessionStatus

class SessionBase(BaseModel):
    content_id: int
    cinema_hall_id: int
    start_time: datetime
    ticket_price: float
    status: SessionStatus = SessionStatus.PLANNED  

class SessionCreate(SessionBase):
    pass

class SessionUpdate(BaseModel):
    content_id: int | None = None
    cinema_hall_id: int | None = None
    start_time: datetime | None = None
    ticket_price: float | None = None 
    status: SessionStatus | None = None 
    
class SessionResponse(SessionBase):
    id: int

    class Config:
        from_attributes = True

class SessionWithContentResponse(SessionResponse):
    content: ContentResponse
