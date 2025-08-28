from datetime import datetime
from uuid import uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Question(Base):
    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    answer: Mapped[list["Answer"]] = relationship(
        "Answer",
        back_populates="question",
        cascade="all, delete-orphan",
        uselist=True,
        lazy="selectin",
    )


class Answer(Base):
    __tablename__ = "answers"
    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE")
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), unique=True, default=uuid4
    )
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    question: Mapped["Question"] = relationship(
        "Question", back_populates="answer"
    )
