from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.functions import get_session
from app.database.models import Answer
from app.schemas.questions_answers import AnswerPydentic, AnswerText

answers = APIRouter()


@answers.post("/questions/{id}/answers/", status_code=status.HTTP_201_CREATED)
async def add_answer_to_question(
    id: int, answer: AnswerText, session: AsyncSession = Depends(get_session)
) -> AnswerPydentic:
    """Добавить ответ к вопросу по его id"""
    if len(answer.text) == 0:
        raise HTTPException(
            status_code=400, detail="Текст ответа не может быть пустым"
        )

    answer = Answer(question_id=id, text=answer.text, user_id=answer.user_id)

    try:
        session.add(answer)
        await session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="Нет такого вопроса с таким id"
        )

    return AnswerPydentic(**answer.__dict__)


@answers.get("/answers/{id}")
async def get_answer_by_id(
    id: int, session: AsyncSession = Depends(get_session)
) -> AnswerPydentic:
    """Получить ответ по id"""
    answer = await session.get(Answer, id)

    if not answer:
        raise HTTPException(status_code=400, detail="Ответа с таким id нет")

    return AnswerPydentic(**answer.__dict__)


@answers.delete("/answers/{id}")
async def del_answer_by_id(
    id: int, session: AsyncSession = Depends(get_session)
) -> str:
    """Удалить ответ по id"""
    answer = await session.get(Answer, id)

    if not answer:
        raise HTTPException(status_code=400, detail="Ответа с таким id нет")

    await session.delete(answer)
    await session.commit()

    return f"deleted answer with id {id}"
