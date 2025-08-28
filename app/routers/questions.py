from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.functions import get_session
from app.database.models import Question
from app.schemas.questions_answers import QuestionText, QuestionPydentic, AnswerPydentic

questions = APIRouter()


async def get_pydentic_question(question: Question, answer=None) -> QuestionPydentic:
    if answer is None:
        list_answer_pydentic = [AnswerPydentic(**answer.__dict__) for answer in question.answer]
    else:
        list_answer_pydentic = []

    question_pydentic = QuestionPydentic(
        id=question.id,
        text=question.text,
        created_at=question.created_at,
        answer=list_answer_pydentic
    )

    return question_pydentic


@questions.get("/questions/")
async def get_list_all_questions(session: AsyncSession = Depends(get_session)) -> list[QuestionPydentic]:
    questions_list = await session.execute(select(Question))
    questions_list = questions_list.scalars().all()

    list_question_pydentic = [await get_pydentic_question(question) for question in questions_list]

    return list_question_pydentic


@questions.post("/questions/")
async def create_new_question(question: QuestionText, session: AsyncSession = Depends(get_session)) -> QuestionPydentic:
    question = Question(text=question.text)
    session.add(question)
    await session.commit()

    question_pydentic = await get_pydentic_question(question, answer=[])

    return question_pydentic


@questions.get("/questions/{id}")
async def get_question_by_id(id: int, session: AsyncSession = Depends(get_session)) -> QuestionPydentic:
    question = await session.get(Question, id)

    if not question:
        raise HTTPException(status_code=400, detail="Вопроса с таким id нет")

    question_pydentic = await get_pydentic_question(question)

    return question_pydentic


@questions.delete("/questions/{id}")
async def delete_question_by_id(id: int, session: AsyncSession = Depends(get_session)) -> str:
    question = await session.get(Question, id)

    if not question:
        raise HTTPException(status_code=400, detail="Вопроса с таким id нет")

    await session.delete(question)
    await session.commit()

    return f"deleted question with id {id}"
