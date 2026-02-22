import random
import os
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.models.content import Content
from app.models.actor import Actor
from app.models.genre import Genre
from app.models.cinema_hall import CinemaHall
from app.models.booking import Booking
from app.models.session import Session

async def seed_database(db: AsyncSession) -> bool:
    """Повне наповнення бази з гарантованим створенням користувача та контенту."""
    try:
        admin_email = "admin@moviehub.com"
        res_user = await db.execute(select(User).where(User.email == admin_email))
        user = res_user.scalar_one_or_none()

        if not user:
            user = User(
                email=admin_email,
                username="superadmin",
                hashed_password="admin_password_hash",
                role="Admin",
                is_superuser=True,
                is_active=True,
                # Обов'язкові поля, які були None
                first_name="Admin",  
                last_name="Super"
            )
            db.add(user)
            await db.flush()

        genres_list = ["Sci-Fi", "Action", "Drama"]
        for g_name in genres_list:
            res = await db.execute(select(Genre).where(Genre.name == g_name))
            if not res.scalar_one_or_none():
                db.add(Genre(name=g_name))

        res_actor = await db.execute(select(Actor).limit(1))
        if not res_actor.scalar_one_or_none():
            db.add(Actor(
                first_name="Leonardo", 
                last_name="DiCaprio", 
                photo_url="https://image.tmdb.org/t/p/w500/lrsfP0BT96veSBrnuMsSTvi8Dvi.jpg",
                biography="American actor and film producer." # Додано для уникнення null
            ))

        res_hall = await db.execute(select(CinemaHall).limit(1))
        hall = res_hall.scalar_one_or_none()
        if not hall:
            hall = CinemaHall(
                name="Grand Hall", 
                number_of_rows=5, 
                seats_per_row=10, 
                total_capacity=50
            )
            db.add(hall)

        res_content = await db.execute(select(Content).limit(1))
        movie = res_content.scalar_one_or_none()
        if not movie:
            movie = Content(
                title="Inception", 
                release_year=2010, 
                rating=8.8, 
                age_rating="13",
                description="A thief who steals corporate secrets through the use of dream-sharing technology.",
                director_full_name="Christopher Nolan",
                duration_minutes=148,
                trailer_url="https://www.youtube.com/watch?v=YoHD9XEInc0",
                poster_url="https://image.tmdb.org/t/p/w500/edv5CZv0jH9NX1o6mGZivQMvI70.jpg",
                banner_url="https://image.tmdb.org/t/p/original/8Z99vYmda69uQOGne9M0CODrp3Z.jpg"
            )
            db.add(movie)

        await db.flush()

        res_session = await db.execute(select(Session).limit(1))
        movie_session = res_session.scalar_one_or_none()
        if not movie_session:
            movie_session = Session(
                content_id=movie.id,
                cinema_hall_id=hall.id,
                start_time=datetime.now() + timedelta(days=1),
                ticket_price=150.0,
                status="PLANNED"
            )
            db.add(movie_session)
            await db.flush()

        res_booking = await db.execute(select(Booking).limit(1))
        if not res_booking.scalar_one_or_none() and user and movie_session:
            for _ in range(10):
                db.add(Booking(
                    user_id=user.id,
                    session_id=movie_session.id,
                    row_number=random.randint(1, 5),
                    seat_number=random.randint(1, 10),
                    status="Confirmed"
                ))

        await db.commit()
        return True

    except Exception as e:
        await db.rollback()
        print(f"Seed Error: {str(e)}") 
        return False
