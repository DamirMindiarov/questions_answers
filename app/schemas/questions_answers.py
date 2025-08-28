from datetime import datetime

from pydantic import BaseModel
from pydantic import UUID4


class Answer(BaseModel):
    id: int
    question_id: int
    user_id: UUID4
    text: str
    created_at: datetime


class QuestionText(BaseModel):
    text: str


class QuestionPydentic(BaseModel):
    id: int
    text: str
    created_at: datetime
    answer: list[Answer]
