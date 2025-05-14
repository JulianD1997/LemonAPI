from api.v1.endpoints import courses, exercises, lessons, topics
from fastapi import FastAPI

app = FastAPI()

app.include_router(courses.router, prefix="/api/v1/courses", tags=["courses"])
app.include_router(topics.router, prefix="/api/v1/topics", tags=["topics"])
app.include_router(lessons.router, prefix="/api/v1/lessons", tags=["lessons"])
app.include_router(exercises.router, prefix="/api/v1/exercises", tags=["exercises"])
