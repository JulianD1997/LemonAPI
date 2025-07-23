from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError

from exerciseAPI.api.v1.endpoints import courses, exercises, lessons, modules, topics
from exerciseAPI.api.v1.exception_handlers import sqlalchemy_exception_handler
from exerciseAPI.core.cors import add_cors_middleware
from exerciseAPI.core.http_client import get_http_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with get_http_client():
        yield


app = FastAPI(title="Lemon API", lifespan=lifespan)

add_cors_middleware(app)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)

app.include_router(courses.router, prefix="/api/v1/courses", tags=["courses"])
app.include_router(topics.router, prefix="/api/v1/topics", tags=["topics"])
app.include_router(lessons.router, prefix="/api/v1/lessons", tags=["lessons"])
app.include_router(exercises.router, prefix="/api/v1/exercises", tags=["exercises"])
app.include_router(modules.router, prefix="/api/v1/modules", tags=["modules"])


@app.get("/")
def read_root():
    return {"message": "Welcome to Lemon API"}
