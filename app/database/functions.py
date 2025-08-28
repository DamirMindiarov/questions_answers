from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_questions_answers import session_async, engine_async
from app.database.models import Base


async def get_session():
    async with session_async() as session:
        yield session


async def create_db():
    async with engine_async.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)