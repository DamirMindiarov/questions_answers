from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.functions import create_db
from app.routers.questions import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)

