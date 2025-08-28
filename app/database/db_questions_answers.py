from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

db_url_async = (
    "postgresql+asyncpg://admin:admin@database:5432/questions_answers"
)
engine_async = create_async_engine(url=db_url_async, echo=True)
session_async = async_sessionmaker(bind=engine_async, expire_on_commit=False)
