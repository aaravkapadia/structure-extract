from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from app.database import engine, async_session
from app import models
from app.routers import documents

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(documents.router)

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/db-check")
async def db_check():
    async with async_session() as session:
        result = await session.execute(text("SELECT 1"))
        value = result.scalar()
        return {"db": "connected", "result": value}
    
    
