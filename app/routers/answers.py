from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.functions import get_session
from app.database.models import Answer

answers = APIRouter()


@answers.post("/questions/{id}/answers/")
async def add_answer_to_question(id: int, session: AsyncSession = Depends(get_session)):
    answer = Answer(question_id=id, text="my answer")
    session.add(answer)
    await session.commit()

    return answer


@answers.get("/answers/{id}")
async def get_answer_by_id(id: int, session: AsyncSession = Depends(get_session)):
    answer = await session.get(Answer, id)

    return answer


@answers.delete("/answers/{id}")
async def del_answer_by_id(id: int, session: AsyncSession = Depends(get_session)):
    answer = await session.get(Answer, id)
    await session.delete(answer)
    await session.commit()

    return f"deleted answer with id {id}"