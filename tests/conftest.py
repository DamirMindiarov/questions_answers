import asyncio
import datetime

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.database.functions import get_session
from app.database.models import Base, Question, Answer
from app.main import app

db_url_async = (
    "postgresql+asyncpg://admin:admin@localhost:5433/questions_answers"
)
engine_async = create_async_engine(url=db_url_async, echo=True)
session_async = async_sessionmaker(bind=engine_async, expire_on_commit=False)


async def new_get_session():
    async with session_async() as session:
        yield session


async def create_table():
    async with engine_async.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.dependency_overrides[get_session] = new_get_session


@pytest_asyncio.fixture(scope="session")
async def async_client(create_db):
    async with AsyncClient(transport=ASGITransport(app=app)) as async_client:
        yield async_client


@pytest_asyncio.fixture(scope="session")
async def create_db():
    async with engine_async.begin() as conn:
        await create_table()
        yield
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def get_new_question():
    async with engine_async.begin() as conn:
        async with session_async() as s:
            question = Question(text="text")
            answer = Answer(question_id=question.id, text="answer text")
            question.answer.append(answer)
            s.add(question)
            await s.commit()

            yield question


@pytest_asyncio.fixture(scope="session")
async def get_session():
    async with session_async() as session:
        yield session


@pytest_asyncio.fixture(scope="session")
async def get_question_response(get_new_question, get_session):
    question = get_new_question
    question = await get_session.get(Question, question.id)

    answers = [
        {
            "id": answer.id,
            "created_at": datetime.datetime.isoformat(answer.created_at),
            "question_id": answer.question_id,
            "text": answer.text,
            "user_id": str(answer.user_id),
        }
        for answer in question.answer
    ]

    question_response = {
        "answer": answers,
        "created_at": datetime.datetime.isoformat(question.created_at),
        "id": question.id,
        "text": question.text,
    }

    yield question_response
