from fastapi import FastAPI
from app.api.v1.endpoints import booking, utils, auth, user, session, genre, content, actor, cinema_hall
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.db.base import Base

app = FastAPI(title="MovieHub API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(user.router, prefix="/api/v1/users", tags=["users"])
app.include_router(session.router, prefix="/api/v1/sessions", tags=["sessions"])
app.include_router(content.router, prefix="/api/v1/content", tags=["content"])
app.include_router(actor.router, prefix="/api/v1/actors", tags=["actors"])
app.include_router(genre.router, prefix="/api/v1/genres", tags=["genres"])
app.include_router(cinema_hall.router, prefix="/api/v1/halls", tags=["halls"])
app.include_router(utils.router, prefix="/api/v1/utils", tags=["utils"])
app.include_router(booking.router, prefix="/api/v1/bookings", tags=["bookings"])
