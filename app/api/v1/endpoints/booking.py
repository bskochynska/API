from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List, Optional
from app.db.session import get_db
from app.schemas.booking import BookingResponse, BookingCreate, BookingFilterParams
from app.crud import booking as crud
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
router = APIRouter(
    prefix="/api/v1/bookings",
    tags=["Booking"],
    dependencies=[Depends(oauth2_scheme)]
)

@router.get("/filter", response_model=List[BookingResponse])
async def filter_bookings(
    params: Annotated[BookingFilterParams, Depends()],
    db: AsyncSession = Depends(get_db)
):
    """
    Get bookings list
    """
    return await crud.get_filtered(db, params)

@router.get("/{id}/exists")
async def check_exists(
    id: Annotated[int, Path(..., description="Унікальний ідентифікатор бронювання")],
    db: AsyncSession = Depends(get_db)
):
    """Checks if booking exists"""
    return await crud.exists_booking(db, id)

@router.get("/", response_model=List[BookingResponse])
async def get_all_admin(db: AsyncSession = Depends(get_db)):
    """Gets bookings list(for admin-users only"""
    return await crud.get_filtered(db, BookingFilterParams(pageSize=100))

@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    obj_in: BookingCreate,
    db: AsyncSession = Depends(get_db)
):
    """Creates new booking"""

    is_booked = await crud.is_seat_booked(
        db,
        obj_in.session_id,
        obj_in.row_number,
        obj_in.seat_number
    )

    if is_booked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Це місце вже заброньоване іншим користувачем або вами"
        )

    return await crud.create(db, obj_in)

@router.get("/{id}", response_model=BookingResponse)
async def get_booking(
    id: Annotated[int, Path(..., description="ID бронювання")],
    db: AsyncSession = Depends(get_db)
):
    """Gets detailed info about booking"""
    res = await crud.get_by_id(db, id)
    if not res:
        raise HTTPException(status_code=404, detail="Booking not found")
    return res

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_booking(
    id: Annotated[int, Path(...)],
    db: AsyncSession = Depends(get_db)
):
    deleted_booking = await crud.remove(db, booking_id=id)
    if not deleted_booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бронювання не знайдено"
        )
        
    return {
        "status": "success", 
        "message": f"Бронювання з ID {id} остаточно видалено з бази"
    }

@router.put("/{id}/cancel", response_model=BookingResponse)
async def cancel_booking(
    id: Annotated[int, Path(...)],
    db: AsyncSession = Depends(get_db)
):
    """Cancels booking"""
    res = await crud.cancel(db, id)
    if not res:
        raise HTTPException(status_code=404, detail="Booking not found or already canceled")
    return res

@router.get("/sessions/{sessionId}/seats/{rowNumber}/{seatNumber}/is-booked")
async def check_seat(
    sessionId: int,
    rowNumber: int,
    seatNumber: int,
    db: AsyncSession = Depends(get_db)
):
    """Checks if the place is vacant"""
    return await crud.is_seat_booked(db, sessionId, rowNumber, seatNumber)
