from pydantic import BaseModel, ConfigDict, field_validator

from exerciseAPI.schemas.topic import TopicOut
from exerciseAPI.schemas.validators import create_title_validator, empty_str_to_none


class LessonBase(BaseModel):
    title: str
    description: str | None = None
    topic_id: int
    _validate_title = field_validator("title")(create_title_validator(min_length=5))
    _normalize_description = field_validator("description", mode="before")(
        empty_str_to_none
    )


class LessonCreate(LessonBase):
    pass


class LessonUpdate(LessonBase):
    pass


class LessonDetailOut(BaseModel):
    id: int
    title: str
    description: str | None = None
    topic: TopicOut
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "Solving linear equations",
                    "description": "Learn how to solve linear equations step by step.",
                    "topic_title": "Linear equations",
                }
            ],
        },
    }


class LessonOut(BaseModel):
    id: int
    title: str

    model_config = ConfigDict(from_attributes=True)
