from pydantic import BaseModel, field_validator

from exerciseAPI.schemas.validators import create_title_validator, empty_str_to_none


class CourseBase(BaseModel):
    title: str
    description: str | None = None
    image_url: str | None = None

    _normalize_description = field_validator("description", "image_url", mode="before")(
        empty_str_to_none
    )

    _validate_title = field_validator("title")(create_title_validator(min_length=5))


class CourseCreate(CourseBase):
    pass


class CourseUpdate(CourseBase):
    pass


class CourseOut(BaseModel):
    id: int
    title: str
    description: str | None = None
    image_url: str | None = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "Precalculus",
                    "description": "Curso de precálculo",
                    "image_url": "http://example.com/image.jpg",
                }
            ],
        },
    }

    @field_validator("title")
    def capitalize_title(cls, value):
        return value.capitalize()
