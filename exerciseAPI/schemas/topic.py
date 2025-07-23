from pydantic import BaseModel, ConfigDict, field_validator

from exerciseAPI.schemas.course import CourseOut
from exerciseAPI.schemas.validators import create_title_validator, empty_str_to_none


class TopicBase(BaseModel):
    title: str
    description: str | None = None
    course_id: int
    _normalize_description = field_validator("description", mode="before")(
        empty_str_to_none
    )

    _validate_title = field_validator("title")(create_title_validator(min_length=5))


class TopicCreate(TopicBase):
    pass


class TopicUpdate(TopicBase):
    pass


class TopicDetailOut(BaseModel):
    id: int
    title: str
    description: str | None = None

    course: CourseOut

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "course": {"id": 1, "title": "Precalculus"},
                    "description": "A topic on linear equations",
                    "title": "linear equations",
                }
            ],
        },
    }


class TopicOut(BaseModel):
    id: int
    title: str

    model_config = ConfigDict(from_attributes=True)
