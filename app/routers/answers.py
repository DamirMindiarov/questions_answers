from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.functions import get_session
from app.database.models import Answer
from app.schemas.questions_answers import AnswerPydentic, AnswerText

answers = APIRouter()


@answers.post("/questions/{id}/answers/", status_code=status.HTTP_201_CREATED)
async def add_answer_to_question(id: int, answer: AnswerText, session: AsyncSession = Depends(get_session)) -> AnswerPydentic:
    answer = Answer(question_id=id, text=answer.text)
    session.add(answer)
    await session.commit()

    return AnswerPydentic(**answer.__dict__)


@answers.get("/answers/{id}")
async def get_answer_by_id(id: int, session: AsyncSession = Depends(get_session)) -> AnswerPydentic:
    answer = await session.get(Answer, id)

    return AnswerPydentic(**answer.__dict__)


@answers.delete("/answers/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def del_answer_by_id(id: int, session: AsyncSession = Depends(get_session)) -> str:
    answer = await session.get(Answer, id)
    await session.delete(answer)
    await session.commit()

    return f"deleted answer with id {id}"