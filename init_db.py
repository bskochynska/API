import asyncio
from app.db.session import engine
from app.db.base import Base
from app.models.user import User 

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Таблиці успішно створені!")

if __name__ == "__main__":
    asyncio.run(init())
