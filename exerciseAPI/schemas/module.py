from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator

from exerciseAPI.schemas.exercise import ExerciseOut
from exerciseAPI.schemas.validators import create_title_validator, empty_str_to_none


class ModuleBase(BaseModel):
    title: str
    description: str
    course_id: str
    exercises: List[int] = []


class ModuleCreate(ModuleBase):
    pass


class ModuleUpdate(BaseModel):
    title: str
    description: str | None = None
    course_id: str | None = None
    exercises: List[str] | None = None

    _normalize_description = field_validator("description", mode="before")(
        empty_str_to_none
    )

    _validate_title = field_validator("title")(create_title_validator(min_length=5))


class ModuleListOut(BaseModel):
    id: str
    title: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ModuleOut(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    course_id: int
    exercises: List[ExerciseOut]

    model_config = ConfigDict(from_attributes=True)
