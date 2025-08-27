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
    pass


