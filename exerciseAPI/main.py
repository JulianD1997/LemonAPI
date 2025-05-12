from fastapi import FastAPI

from exerciseAPI.api.v1.endpoints import courses

app = FastAPI()

app.include_router(courses.router, prefix="/api/v1/courses", tags=["courses"])


@app.get("/")
async def root():
    return {"message": "Hello World"}
