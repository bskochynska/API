from pydantic import BaseModel

class ContentBase(BaseModel):
    title: str
    description: str  
    rating: float | None = None
    age_rating: int
    release_year: int
    director_full_name: str
    trailer_url: str | None = None
    poster_url: str | None = None
    banner_url: str | None = None
    duration_minutes: int

class ContentCreate(ContentBase):
    pass

class ContentUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    rating: float | None = None
    age_rating: int | None = None
    release_year: int | None = None
    director_full_name: str | None = None
    trailer_url: str | None = None
    poster_url: str | None = None
    banner_url: str | None = None
    duration_minutes: int | None = None

class ContentResponse(ContentBase):
    id: int
    
    class Config:
        from_attributes = True
