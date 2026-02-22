from fastapi import FastAPI
from app.api.v1.endpoints import  booking, utils, auth, user, session, genre, content, actor, cinema_hall
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="MovieHub API", version="1.0.0")

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(session.router)
app.include_router(content.router)
app.include_router(actor.router)
app.include_router(genre.router)
app.include_router(cinema_hall.router)
app.include_router(utils.router)
app.include_router(booking.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
