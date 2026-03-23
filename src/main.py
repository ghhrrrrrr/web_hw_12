from contextlib import asynccontextmanager
from fastapi import FastAPI

from contactbook.router import router as contactbook_router
from auth.router import router as auth_router
from database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(contactbook_router, prefix="/api/contacts", tags=["contacts"])
app.include_router(auth_router, prefix='/api/auth', tags=['auth'])