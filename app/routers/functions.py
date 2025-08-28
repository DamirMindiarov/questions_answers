from app.database.models import Question
from app.schemas.questions_answers import QuestionPydentic, AnswerPydentic


async def get_pydentic_question(
    question: Question, answer=None
) -> QuestionPydentic:
    """Получает объект Question преобразует в QuestionPydentic"""
    if answer is None:
        list_answer_pydentic = [
            AnswerPydentic(**answer.__dict__) for answer in question.answer
        ]
    else:
        list_answer_pydentic = []

    question_pydentic = QuestionPydentic(
        id=question.id,
        text=question.text,
        created_at=question.created_at,
        answer=list_answer_pydentic,
    )

    return question_pydentic
