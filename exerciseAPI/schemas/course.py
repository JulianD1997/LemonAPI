import re

from pydantic import BaseModel, Field, field_validator


class CourseBase(BaseModel):
    name: str = Field(default=None, examples=["Precálculo"])

    @field_validator("name")
    def validate_name(cls, value):
        value = value.lower()
        if len(value) < 5:
            raise ValueError("El nombre del curso debe tener al menos 5 caracteres.")
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúñÑ0-9 ]+", value):
            print(f"aca, {value}")
            raise ValueError(
                "El nombre del curso no puede contener caracteres especiales."
            )
        return value.lower()


class CourseCreate(CourseBase):
    pass


class CourseUpdate(CourseBase):
    pass


class CourseOut(CourseBase):
    id: int

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [{"id": 1, "name": "Precálculo"}],
        },
    }

    @field_validator("name")
    def capitalize_name(cls, value):
        return value.capitalize()
