from fastapi import FastAPI
from app.api.v1.endpoints import booking, utils, auth, user, session, genre, content, actor, cinema_hall
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.db.base import Base

app = FastAPI(title="MovieHub API", version="1.0.0")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://cinema-website-oop-project-ei3nouf62-bskochynskas-projects.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(session.router) 
app.include_router(content.router)
app.include_router(actor.router)
app.include_router(genre.router)
app.include_router(cinema_hall.router)
app.include_router(utils.router)
app.include_router(booking.router)
