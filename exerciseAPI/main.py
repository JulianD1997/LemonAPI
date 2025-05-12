from api.v1.endpoints import courses, topics
from fastapi import FastAPI

app = FastAPI()

app.include_router(courses.router, prefix="/api/v1/courses", tags=["courses"])
app.include_router(topics.router, prefix="/api/v1/topics", tags=["topics"])


@app.get("/")
async def root():
    return {"message": "Hello World"}
