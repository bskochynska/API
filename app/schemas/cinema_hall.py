from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID 

class CinemaHallBase(BaseModel):
    name: str
    number_of_rows: int
    seats_per_row: int
    total_capacity: Optional[int] = None

class CinemaHallCreate(CinemaHallBase):
    pass

class CinemaHallUpdate(BaseModel):
    name: Optional[str] = None
    number_of_rows: Optional[int] = None
    seats_per_row: Optional[int] = None
    total_capacity: Optional[int] = None

class CinemaHallResponse(CinemaHallBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
