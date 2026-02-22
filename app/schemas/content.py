from pydantic import BaseModel
from typing import Optional

class ContentBase(BaseModel):
    title: str
    description: Optional[str] = None
    release_date: Optional[str] = None

class ContentCreate(ContentBase):
    pass

class ContentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class ContentResponse(ContentBase):
    id: int
    poster_url: Optional[str] = None
    banner_url: Optional[str] = None

    class Config:
        from_attributes = True
