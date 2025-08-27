from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.functions import get_session
from app.database.models import Question

router = APIRouter()


@router.get("/questions/")
async def get_list_all_questions(session: AsyncSession = Depends(get_session)):
    pass


@router.post("/questions/")
async def create_new_question(session: AsyncSession = Depends(get_session)):
    question = Question(text="111")
    session.add(question)
    await session.commit()
    return question


@router.get("/questions/{id}")
async def get_question_by_id(id: int, session: AsyncSession = Depends(get_session)):
    pass


@router.delete("/questions/{id}")
async def delete_question_by_id(id: int, session: AsyncSession = Depends(get_session)):
    pass