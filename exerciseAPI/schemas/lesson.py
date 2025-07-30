from pydantic import BaseModel, ConfigDict, field_validator

from exerciseAPI.schemas.topic import TopicDetailOut, TopicExerciseOut
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
    topic: TopicDetailOut
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "Solving linear equations",
                    "topic_title": "Linear equations",
                }
            ],
        },
    }


class LessonExerciseOut(BaseModel):
    id: int
    title: str
    topic: TopicExerciseOut
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "Solving linear equations",
                    "topic_title": "Linear equations",
                }
            ],
        },
    }

    @field_validator("title")
    def capitalize_title(cls, value):
        return value.capitalize()


class LessonOut(BaseModel):
    id: int
    title: str
    description: str | None = None
    model_config = ConfigDict(from_attributes=True)
