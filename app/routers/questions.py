from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.functions import get_session
from app.database.models import Question
from app.schemas.questions import QuestionText, QuestionPydentic, Answer

questions = APIRouter()


@questions.get("/questions/")
async def get_list_all_questions(session: AsyncSession = Depends(get_session)) -> list[QuestionPydentic]:
    questions_list = await session.execute(select(Question))
    questions_list = questions_list.scalars().all()

    list_question_pydentic = [QuestionPydentic(
        id=question.id,
        text=question.text,
        created_at=question.created_at,
        answer=[Answer(**answer.__dict__) for answer in question.answer]
    ) for question in questions_list]

    return list_question_pydentic


@questions.post("/questions/")
async def create_new_question(question: QuestionText, session: AsyncSession = Depends(get_session)) -> QuestionPydentic:
    question = Question(text=question.text)
    session.add(question)
    await session.commit()

    return QuestionPydentic(id=question.id, text=question.text, created_at=question.created_at, answer=[])


@questions.get("/questions/{id}")
async def get_question_by_id(id: int, session: AsyncSession = Depends(get_session)):
    question = await session.get(Question, id)
    answers = question.answer

    return answers


@questions.delete("/questions/{id}")
async def delete_question_by_id(id: int, session: AsyncSession = Depends(get_session)):
    question = await session.get(Question, id)
    await session.delete(question)
    await session.commit()

    return f"deleted question with id {id}"


