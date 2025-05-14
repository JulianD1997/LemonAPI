from pydantic import BaseModel


class LessonBase(BaseModel):
    name: str
    topic_id: int


class LessonCreate(LessonBase):
    pass


class LessonUpdate(LessonBase):
    pass


class LessonOut(BaseModel):
    id: int
    topic_name: str
    name: str
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "Solving linear equations",
                    "topic_name": "Linear equations",
                }
            ],
        },
    }
