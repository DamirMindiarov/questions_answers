from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.functions import get_session

answers = APIRouter()


@answers.post("/questions/{id}/answers/")
async def add_answer_to_question(id: int, session: AsyncSession = Depends(get_session)):
    pass


@answers.get("/answers/{id}")
async def get_answer_by_id(id: int, session: AsyncSession = Depends(get_session)):
    pass


@answers.delete("/answers/{id}")
async def del_answer_by_id(id: int, session: AsyncSession = Depends(get_session)):
    pass