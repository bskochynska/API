from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists, and_, desc, asc
from app.models.booking import Booking
from app.schemas.booking import BookingFilterParams, BookingStatus, BookingCreate

async def create(db: AsyncSession, obj_in: BookingCreate):
    """
    Створює новий запис бронювання в базі даних.
    """
    try:
        db_obj = Booking(
            user_id=obj_in.user_id,
            session_id=obj_in.session_id,
            row_number=obj_in.row_number,
            seat_number=obj_in.seat_number,
            status=BookingStatus.Pending
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    except Exception:
        await db.rollback()
        return None

async def get_filtered(db: AsyncSession, params: BookingFilterParams):
    """
    Отримує список бронювань за 8 параметрами фільтрації.
    """
    try:
        query = select(Booking)

        if params.UserId:
            query = query.where(Booking.user_id == params.UserId)
        if params.SessionId:
            query = query.where(Booking.session_id == params.SessionId)
        if params.Statuses:
            query = query.where(Booking.status.in_(params.Statuses))
        if params.MinCreatedAt:
            query = query.where(Booking.created_at >= params.MinCreatedAt)
        if params.MaxCreatedAt:
            query = query.where(Booking.created_at <= params.MaxCreatedAt)

        sort_map = {
            "Id": Booking.id,
            "CreatedAt": Booking.created_at,
            "Status": Booking.status
        }

        if params.orderField and params.orderType:
            for field, o_type in zip(params.orderField, params.orderType):
                col = sort_map.get(field)
                if col is not None:
                    if "Descending" in o_type:
                        query = query.order_by(desc(col))
                    else:
                        query = query.order_by(asc(col))

        query = query.offset(params.PageIndex * params.pageSize).limit(params.pageSize)

        result = await db.execute(query)
        return result.scalars().all()
    except Exception:
        return []

async def get_by_id(db: AsyncSession, booking_id: int):
    """Отримує бронювання за його унікальним ідентифікатором."""
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    return result.scalar_one_or_none()

async def exists_booking(db: AsyncSession, booking_id: int) -> bool:
    """Перевіряє існування бронювання."""
    stmt = select(exists().where(Booking.id == booking_id))
    result = await db.execute(stmt)
    return result.scalar() or False

async def cancel(db: AsyncSession, booking_id: int):
    """Скасовує бронювання через зміну статусу."""
    try:
        db_obj = await get_by_id(db, booking_id)
        if db_obj:
            db_obj.status = BookingStatus.Canceled
            await db.commit()
            await db.refresh(db_obj)
        return db_obj
    except Exception:
        await db.rollback()
        return None

async def is_seat_booked(db: AsyncSession, session_id: int, row: int, seat: int) -> bool:
    """Перевіряє, чи зайняте місце."""
    stmt = select(exists().where(and_(
        Booking.session_id == session_id,
        Booking.row_number == row,
        Booking.seat_number == seat,
        Booking.status != BookingStatus.Canceled
    )))
    result = await db.execute(stmt)
    return result.scalar() or False
